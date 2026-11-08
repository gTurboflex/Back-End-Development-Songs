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
bash bin/setup.sh
. backend-songs-venv/bin/activate
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
Use **Python 3.9.16** for the course setup. Run `bash bin/setup.sh` with Python 3.9.16 as `python3` to create the required **backend-songs-venv** environment and install the pinned dependencies. The script exits on errors and prints its completion status.
Do not commit `.env`, database files, generated users, or registry credentials.

## Verified setup — 8 November 2026
The setup script ran successfully with **Python 3.9.16** in the IBM cloud laboratory.
For reproducibility, an official `python:3.9.16-slim` container provided the interpreter;
inside that environment, the script created the separate **backend-songs-venv** virtual environment,
installed the requirements, and passed its Flask import check. This verifies the setup
script and virtual environment, in addition to the application's container runtime.
Actual setup output:
```text
Python 3.9.16
Flask import: OK
Environment Setup completed successfully: backend-songs-venv
Activate with: source backend-songs-venv/bin/activate
```
The three integration tests also passed against real MongoDB in the Cloud IDE's
Python 3.10.12 environment. PUT returns 201 CREATED and GET /song returns a JSON
object containing the `songs` list, as consumed by the Django application.
