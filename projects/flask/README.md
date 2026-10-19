# Flask in Docker

This lab runs one Flask application with Gunicorn. The app, requirements,
Dockerfile, and Compose file are included; no reverse proxy is required.

## Run with Compose

From the repository root:

```bash
docker compose -f projects/flask/compose.yaml config --quiet
docker compose -f projects/flask/compose.yaml up --build --wait
curl --fail http://127.0.0.1:5000/
```

Expected response:

```text
Hello from Flask running in Docker!
```

The health check waits for an HTTP response. The host port is bound to loopback,
while Gunicorn listens on the container's 0.0.0.0:5000 interface. The image runs
as UID/GID 10001 rather than root.

## Inspect and clean up

```bash
docker compose -f projects/flask/compose.yaml ps
docker compose -f projects/flask/compose.yaml logs --tail 20
docker compose -f projects/flask/compose.yaml down
```

After changing app.py or dependencies, run up --build --wait again so the image
is rebuilt and the container is recreated as needed.

## Run without Compose

```bash
docker build -t docker-notes-flask projects/flask
docker run --rm --publish 127.0.0.1:5000:5000 docker-notes-flask
```

Use Ctrl-C to stop the foreground container. See the [Dockerfile notes](../../notes/04_docker_file.md)
for layer caching and build context, and the [Flask deployment guide](https://flask.palletsprojects.com/en/stable/deploying/gunicorn/)
for Gunicorn configuration.
