"""MongoDB-backed REST resources for the band's song catalogue."""
import json
import os
from pathlib import Path
from flask import jsonify, request, url_for
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from . import app

host = os.environ.get("MONGODB_SERVICE", "localhost:27017")
options = {"serverSelectionTimeoutMS": 5000}
if os.environ.get("MONGODB_USERNAME"):
    options.update(username=os.environ["MONGODB_USERNAME"], password=os.environ.get("MONGODB_PASSWORD", ""))
client = MongoClient("mongodb://" + host, **options)
db = client.songs
db.songs.create_index("id", unique=True)
if db.songs.count_documents({}) == 0:
    with (Path(__file__).parent / "data/songs.json").open(encoding="utf-8") as source:
        db.songs.insert_many(json.load(source))


@app.route("/health")
def health():
    client.admin.command("ping")
    return jsonify(status="OK"), 200


@app.route("/count")
def count():
    return jsonify(length=db.songs.count_documents({})), 200


@app.route("/song", methods=["GET"])
def get_songs():
    return jsonify(songs=list(db.songs.find({}, {"_id": 0}).sort("id", 1))), 200


@app.route("/song/<int:id>", methods=["GET"])
def get_song_by_id(id):
    song = db.songs.find_one({"id": id}, {"_id": 0})
    return (jsonify(song), 200) if song else (jsonify(Message=f"song with id {id} not found"), 404)


@app.route("/song", methods=["POST"])
def create_song():
    song = request.get_json(silent=True)
    if not isinstance(song, dict) or not isinstance(song.get("id"), int):
        return jsonify(Message="A JSON song with an integer id is required"), 400
    if not all(isinstance(song.get(key), str) for key in ["title", "lyrics"]):
        return jsonify(Message="title and lyrics must be strings"), 400
    song = {key: song[key] for key in ["id", "title", "lyrics"]}
    try:
        db.songs.insert_one(dict(song))
    except DuplicateKeyError:
        return jsonify(Message=f"song with id {song['id']} already present"), 302
    response = jsonify(song)
    response.status_code = 201
    response.headers["Location"] = url_for("get_song_by_id", id=song["id"])
    return response


@app.route("/song/<int:id>", methods=["PUT"])
def update_song(id):
    song = request.get_json(silent=True)
    if not isinstance(song, dict):
        return jsonify(Message="A JSON song is required"), 400
    update = {key: song[key] for key in ["title", "lyrics"] if key in song}
    if not update or not all(isinstance(value, str) for value in update.values()):
        return jsonify(Message="title or lyrics must contain text"), 400
    result = db.songs.update_one({"id": id}, {"$set": update})
    if result.matched_count == 0:
        return jsonify(Message=f"song with id {id} not found"), 404
    return jsonify(db.songs.find_one({"id": id}, {"_id": 0})), 201


@app.route("/song/<int:id>", methods=["DELETE"])
def delete_song(id):
    result = db.songs.delete_one({"id": id})
    if result.deleted_count == 0:
        return jsonify(Message=f"song with id {id} not found"), 404
    return "", 204
