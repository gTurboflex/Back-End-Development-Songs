# Back-End-Development-Songs

Flask and MongoDB service for the band's song titles and lyrics.

## API
`GET /health`, `GET /count`, `GET /song`, `GET /song/<id>`,
`POST /song`, `PUT /song/<id>`, and `DELETE /song/<id>`.
MongoDB stores changes persistently. The fixture loads only into an empty collection,
and startup never drops an existing collection. An index prevents duplicate song IDs.
Health checks ping MongoDB. API responses exclude MongoDB's internal `_id` field.

## Configuration
Set `MONGODB_SERVICE` to the database host and port, for example `mongo:27017`.
Set `MONGODB_USERNAME` and `MONGODB_PASSWORD` only if authentication is enabled.
Pass credentials via environment variables, never through a committed file.
PyMongo 4.6.3 supports the lab's MongoDB 3.6 server.

## Run and test
```sh
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python -m pytest -v
flask --app app run --host 0.0.0.0 --port 8080
```
The supplied health test and two added lifecycle/validation tests cover all CRUD methods.
Local unit checks used mongomock. Cloud validation uses the lab's MongoDB server.

## Container
```sh
docker build -t songs:1 .
docker run --rm -p 8080:8080 --env MONGODB_SERVICE --env MONGODB_USERNAME --env MONGODB_PASSWORD songs:1
```

## Environment Setup
The project starts from the IBM Skills Network course template, retaining its license.
The original `bin/setup.sh` describes the Linux lab setup. For the current environment,
create a virtual environment and install `requirements.txt`. Containers use Python 3.9.16.
Local validation used Python 3.12. Cloud IDE provides Python 3.10.12.
Do not commit `.env`, database files, generated users, or registry credentials.
