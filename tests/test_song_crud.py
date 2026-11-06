def test_song_lifecycle(client):
    song = {"id": 200, "title": "Course test song", "lyrics": "A test verse."}
    assert client.get("/count").json["length"] == 20
    assert len(client.get("/song").json) == 20
    assert client.get("/song/1").status_code == 200
    assert client.get("/song/999").status_code == 404
    created = client.post("/song", json=song)
    assert created.status_code == 201
    assert created.json == song
    assert client.post("/song", json=song).status_code == 302
    assert client.put("/song/200", json={"title": "Updated verse"}).status_code == 201
    assert client.get("/song/200").json["title"] == "Updated verse"
    assert client.delete("/song/200").status_code == 204
    assert client.get("/count").json["length"] == 20
    assert client.delete("/song/200").status_code == 404


def test_reject_malformed_song(client):
    assert client.post("/song", json={"id": "invalid"}).status_code == 400
    assert client.put("/song/1", json={"lyrics": 5}).status_code == 400
