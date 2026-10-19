# Dockerfiles

A Dockerfile describes how to build an image. Compilation and dependency
installation belong in the build when needed; multi-stage builds can keep
compilers and intermediate files out of the runtime image.

## Core instructions

| Instruction | Effect |
|-------------|--------|
| FROM | Starts a build stage from a base image. |
| WORKDIR | Sets the working directory for subsequent instructions. |
| COPY | Copies selected files from the build context or another stage. |
| ADD | Supports extra source handling, such as archive extraction; use COPY for ordinary local files. |
| RUN | Executes a build step that can change the stage's filesystem. |
| ENV | Sets an environment variable in the image and resulting containers. |
| USER | Selects the user for subsequent RUN instructions and the container process. |
| EXPOSE | Documents a listening port; does not publish it or change firewall rules. |
| CMD | Provides the default command/arguments; the last CMD in a stage takes effect. |
| ENTRYPOINT | Sets an executable that CMD or runtime arguments can supply arguments to. |

Metadata instructions do not each add a filesystem layer. Prefer the JSON exec
form for the runtime process so a shell does not obscure signal delivery.

## Included Flask example

The runnable files are in [projects/flask](../projects/flask/README.md):

```dockerfile
FROM python:3.13-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
USER 10001:10001
EXPOSE 5000
CMD ["gunicorn", "--bind=0.0.0.0:5000", "app:app"]
```

Copying dependency declarations before application code lets a source-only change
reuse the dependency installation layer. The numeric USER runs the web process
without root inside the container. The application must still have write access
to any paths it needs.

Run from the repository root:

```bash
docker build --pull -t docker-notes-flask projects/flask
docker run --rm --publish 127.0.0.1:5000:5000 docker-notes-flask
```

The application listens on 0.0.0.0 inside the container. Publishing a port does
not make a service bound only to container-local 127.0.0.1 reachable from the host.

## Build context, cache, and secrets

- Paths in COPY are relative to the build context, not the shell's current
  directory or the Dockerfile's location.
- A .dockerignore file excludes irrelevant files from the context.
- Version tags constrain a base image's release family but can move. Pin a digest
  when exact base-image content must be reproducible, and update it deliberately.
- Build arguments and ENV are not secret storage. Use BuildKit secret mounts
  for credentials needed during a build, and runtime secret mounts for the app.
- Combine apt-get update and apt-get install in one RUN when using APT, then
  remove package lists in that same step. Avoid installing unused packages.

## References

- [Dockerfile instruction reference](https://docs.docker.com/reference/dockerfile/)
- [Build best practices](https://docs.docker.com/build/building/best-practices/)
- [Build secrets](https://docs.docker.com/build/building/secrets/)
