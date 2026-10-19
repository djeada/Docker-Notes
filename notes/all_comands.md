# Docker Command Reference

CONTAINER, IMAGE, and uppercase paths are placeholders. Prune commands apply
across the selected Docker daemon. Use [basic commands](03_basic_commands.md)
for a guided exercise and cleanup scope. Publishing a port without a host IP
normally binds all interfaces; prefer 127.0.0.1 for local labs.

| Command Combination                                                                 | Description                                                                                     |
|-------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------|
| `docker ps`                                                                         | List all running containers.                                                                    |
| `docker ps -a`                                                                      | List all containers, including those that are stopped.                                          |
| `docker ps -q`                                                                      | List the IDs of all running containers.                                                         |
| `docker ps -aq`                                                                     | List the IDs of all containers, regardless of status.                                           |
| `docker stop CONTAINER` | Stop a selected container gracefully. |
| `docker rm CONTAINER` | Remove a selected stopped container and its writable layer. |
| `docker images -q`                                                                  | List the IDs of all images.                                                                     |
| `docker image rm IMAGE` | Remove a selected image/tag; references can prevent deletion. |
| `docker run -d -p 80:80 nginx`                                                      | Run a container in detached mode, mapping port 80 to the host.                                  |
| `docker run -it ubuntu bash`                                                        | Run an Ubuntu container and start an interactive bash shell.                                    |
| `docker run --name custom-name nginx`                                               | Run a container with a custom name.                                                             |
| `docker run -v /host/dir:/container/dir -p 80:80 nginx`                             | Run a container with a bound volume and port mapping.                                           |
| `docker exec -it container_name bash`                                               | Execute an interactive bash shell inside a running container.                                   |
| `docker logs -f container_name`                                                     | Follow the logs of a container.                                                                 |
| `docker build -t my_image:tag .`                                                    | Build an image from a Dockerfile in the current directory with a custom tag.                    |
| `docker compose up -d`                                                              | Start all services defined in docker-compose.yml in detached mode.                              |
| `docker compose down --volumes`                                                     | Stop and remove containers, networks, and volumes created by docker-compose.                    |
| `docker network ls`                                                                 | List all networks.                                                                              |
| `docker network inspect network_name`                                               | Display detailed information on a specific network.                                             |
| `docker volume ls`                                                                  | List all volumes.                                                                               |
| `docker volume rm volume_name`                                                      | Remove a specific volume.                                                                       |
| `docker system prune`                                                               | Remove all stopped containers, dangling images, and unused networks.                            |
| `docker system prune -a`                                                            | Remove all stopped containers, unused images (not just dangling), and unused networks.          |
| `docker system df`                                                                  | Show docker disk usage.                                                                         |
| `docker login`                                                                      | Log in to a Docker registry.                                                                    |
| `docker tag my_image:tag registry/my_image:tag`                                     | Tag an image for a registry.                                                                    |
| `docker push registry/my_image:tag`                                                 | Push an image to a registry.                                                                    |
| `docker pull registry/my_image:tag`                                                 | Pull an image from a registry.                                                                  |
| `docker cp container_name:/path/to/file /local/path`                                | Copy a file from a container to the local filesystem.                                           |
| `docker cp /local/path container_name:/path/to/file`                                | Copy a file from the local filesystem to a container.                                           |
| `docker save my_image:tag > my_image.tar`                                           | Save an image to a tar file.                                                                    |
| `docker load < my_image.tar`                                                        | Load an image from a tar file.                                                                  |
| `docker inspect --format '{{range .NetworkSettings.Networks}}{{println .IPAddress}}{{end}}' CONTAINER` | Print each attached network's IP address on its own line. |
| `docker run -d --restart=always --name container_name nginx`                        | Run a container with a restart policy.                                                          |
| `docker exec -it container_name /bin/bash`                                          | Access a bash shell in a running container (commonly used as an SSH-like method).                 |
| `docker run -d --name container1 nginx`                                             | Run a first container named `container1`.                                                         |
| `docker run -d --name container2 --network my_bridge nginx:stable-alpine` | Join an existing user-defined network; resolve peers by name. |
| `docker network create --driver bridge my_bridge`                                   | Create a new bridge network named `my_bridge`.                                                    |
| `docker run -d --name container3 --network my_bridge nginx`                         | Run a container named `container3` in the `my_bridge` network.                                    |
| `docker run -d --name container4 --network host nginx`                              | Run a container named `container4` using the host's network stack.                                |
| `docker run -d --name container5 --network none nginx`                              | Run a container named `container5` with no networking.                                            |
| `docker run -d --name container6 -p 8080:80 nginx`                                  | Run a container named `container6` with port 80 inside the container mapped to port 8080 outside. |
| `docker network connect network_name container_name`                                | Connect an existing container to a network.                                                       |
| `docker network disconnect network_name container_name`                             | Disconnect a container from a network.                                                            |
| `docker run --rm -it -v "$(pwd):/app" -w /app node:24-slim npm install` | Install dependencies into the host project directory, including node_modules. |
| `docker run -d --name notes-db -e POSTGRES_PASSWORD=local-demo -v dbdata:/var/lib/postgresql/data postgres:17` | Run PostgreSQL 17 with a named data volume and an example password. |
| `docker volume inspect dbdata` | Inspect a volume. Do not share one live database data directory between independent servers. |
| `docker port container_name`                                                        | List port mappings of a specific container.                                                       |
| `docker logs --tail 50 --follow --timestamps container_name`                        | Tail the last 50 log lines of a container and follow with timestamps.                             |
| `docker run -d -e "ENV_VAR_NAME=value" --name container_with_env nginx`             | Run a container with an environment variable set.                                                 |
| `docker inspect --format '{{json .NetworkSettings.Networks}}' CONTAINER` | Inspect network names and addresses, including user-defined networks. |
| `docker update --cpus=2 container_name`                                             | Limit the CPU usage of a container.                                                               |
| `docker compose -f docker-compose.prod.yml up -d`                                   | Start services using a specific Docker Compose file in detached mode.                             |
| `docker run -d --name container7 --restart=on-failure:5 nginx`                      | Run a container with a restart policy that retries 5 times on failure.                            |
| `docker run -d --name container8 --memory=500m nginx`                               | Run a container with a memory limit of 500 MB.                                                    |
| `docker run -d --name container9 -v /host/path:/container/path:ro nginx`            | Run a container with a read-only volume mount.                                                    |
| `docker save -o my_images.tar image1 image2`                                        | Save multiple images to a single tar archive.                                                     |
| `docker load -i my_images.tar`                                                      | Load images from a tar archive.                                                                   |
| `docker run -d --name container10 --log-driver=syslog --log-opt syslog-address=udp://1.2.3.4:1111 nginx` | Run a container with syslog logging. |
| `docker build --no-cache -t my_image:latest .`                                      | Build an image without using the cache.                                                           |
