# Basic Docker Commands

Commands below use a local Linux-container Docker engine. Run project build
commands from the repository root.

## Images and containers

An image is a read-only template. A container adds configuration and a writable
layer; it can be running or stopped. Pulling a newer tag does not replace the
image used by an existing container.

| Command | Purpose |
|---------|---------|
| `docker image ls` | List locally stored images. |
| `docker pull nginx:stable-alpine` | Refresh a local tag from its registry. |
| `docker ps` | List running containers. |
| `docker ps -a` | Include stopped containers that still exist. |
| `docker inspect CONTAINER` | Inspect configuration and state. |
| `docker image rm IMAGE` | Remove a tag or unused image; references may prevent deletion. |

A locally cached tag can be older than the registry's tag. Image IDs and digests
identify content; tags can move.

## Run and inspect a web server

```bash
docker run --detach --name notes-web \
  --publish 127.0.0.1:8080:80 nginx:stable-alpine
curl --fail http://127.0.0.1:8080/
docker logs --tail 20 notes-web
docker port notes-web
docker exec -it notes-web sh
```

Exit the shell with exit. docker exec starts an additional process in a running
container; it does not replace its main process. An image may have sh but no bash.
Interactive flags are unnecessary for a detached web server.

The published address restricts this example to the local host. Without a host
address, a published port normally binds all host interfaces.

```bash
docker stop notes-web
docker start notes-web
docker rm -f notes-web
```

docker stop sends the configured stop signal (normally SIGTERM), waits for the
grace period, and sends SIGKILL only if the process has not exited. docker rm -f
forcibly removes this example container.

## Build the included Apache project

```bash
docker build --pull -t notes-apache ./projects/apache/mywebsite
docker run --detach --name notes-apache \
  --publish 127.0.0.1:8080:80 notes-apache
curl --fail http://127.0.0.1:8080/
docker rm -f notes-apache
```

The build context is projects/apache/mywebsite; its html directory is copied
into Apache's document root. See the [Apache lab](../projects/apache/README.md).
Build steps can be reused from cache; --pull refreshes base-image references,
whereas --no-cache disables reuse of build steps.

## Persist data with a named volume

```bash
docker volume create notes-data
docker run --rm --mount type=volume,source=notes-data,target=/data \
  alpine:3.22 sh -c 'echo hello > /data/example.txt'
docker run --rm --mount type=volume,source=notes-data,target=/data \
  alpine:3.22 cat /data/example.txt
docker volume inspect notes-data
```

The second container reads data written by the first even though --rm removed
the first container. Volumes outlive containers. Remove this example's stored
data when finished:

```bash
docker volume rm notes-data
```

Docker refuses to remove a volume referenced by an existing container, including
a stopped one. A volume is persistent storage, not a backup.

## Compose lifecycle and image updates

```bash
docker compose -f projects/flask/compose.yaml config --quiet
docker compose -f projects/flask/compose.yaml up --build --wait
docker compose -f projects/flask/compose.yaml logs --tail 20
docker compose -f projects/flask/compose.yaml down
```

For services using registry images, docker compose pull followed by
docker compose up -d applies new images through container recreation.
docker restart and docker compose restart restart existing containers using
their existing image and configuration.

## Cleanup scope

| Command | Removes |
|---------|---------|
| `docker container prune` | All stopped containers, after confirmation. |
| `docker image prune` | Dangling images not referenced by containers. |
| `docker image prune -a` | All images not referenced by any container. |
| `docker volume prune` | Unused anonymous local volumes by default. |
| `docker volume prune -a` | Unused named and anonymous local volumes. |
| `docker system prune` | Stopped containers, unused networks, dangling images, and unused build cache. |
| `docker system df` | Reports disk use without deleting resources. |

Prune commands apply across the selected daemon, beyond the current project.
docker compose down keeps named volumes by default; adding --volumes deletes
that project's declared named and attached anonymous volumes.

## References

- [Container run](https://docs.docker.com/reference/cli/docker/container/run/)
- [Container stop](https://docs.docker.com/reference/cli/docker/container/stop/)
- [Image prune](https://docs.docker.com/reference/cli/docker/image/prune/)
- [Volume prune](https://docs.docker.com/reference/cli/docker/volume/prune/)
- [Compose up](https://docs.docker.com/reference/cli/docker/compose/up/)

