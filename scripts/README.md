# Docker Utility Scripts

Use Python 3.10 or later. Run commands from the repository root. The Docker
daemon and CLI are needed for operational scripts; Compose generation and unit
tests can run without Docker.

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows, activate with .venv\Scripts\Activate.ps1 in PowerShell.

| Script | Purpose |
|--------|---------|
| [Compose generator](docker_compose_generator.py) | Generate a validated service model and write a Compose YAML file. |
| [Batch runner](batch_container_runner.py) | Launch containers from CLI specifications and report Docker failures. |
| [Resource monitor](container_resource_monitor.py) | Read Linux Docker stats percentages every 10 seconds. |
| [Image updater](docker_image_updater.py) | Pull distinct image references used by running containers. |
| [Image cleaner](image_cleaner.py) | Prune unreferenced images using Docker's own filtering. |
| [Local runner API](container_runner.py) | A loopback-only Flask demo that starts containers. |

## Compose generator

Start each service with --service-name. Its image, ports, environment, and mount
options apply to that service until the next --service-name. Commas separate
entries within an option; values containing commas are not supported.

```bash
python scripts/docker_compose_generator.py \
  --output compose.demo.yaml --networks appnet \
  --service-name web --service-image nginx:stable-alpine \
  --service-ports 127.0.0.1:8080:80 \
  --service-name db --service-image mysql:8.4 \
  --service-env MYSQL_ROOT_PASSWORD:local-demo \
  --service-volumes dbdata:/var/lib/mysql
docker compose -f compose.demo.yaml config --quiet
```

The generator attaches every service to the requested networks and declares
named volume sources automatically. Environment entries use KEY:VALUE; values
can contain additional colons, including URLs. Names and required images are
checked before writing. The output defaults to docker-compose.yml; an existing
file is replaced only with --force. Validate with Compose before starting
services; not every possible Compose option or mount form is supported.

## Batch runner

```bash
python scripts/batch_container_runner.py \
  'nginx:stable-alpine,name=notes-web,port=80' \
  'mysql:8.4,name=notes-db,env=MYSQL_ROOT_PASSWORD:local-demo,volume=notes-db:/var/lib/mysql'
```

port=80 means host 127.0.0.1:80 to container port 80. Use the Compose generator
for different host/container ports. env and volume can repeat; values cannot
contain commas. All specifications are parsed before launching any container.
Docker runtime failures stop the batch; containers already launched remain
running and can be inspected or removed by name.

## Monitoring and image maintenance

```bash
python scripts/container_resource_monitor.py
python scripts/docker_image_updater.py
python scripts/image_cleaner.py
python scripts/image_cleaner.py --days 30
```

The monitor uses Docker's CPUPerc and MemPerc fields rather than parsing
human-readable memory units. Its default alert thresholds are CPU 75% and memory
80%; Ctrl-C stops it. CPU percentages can exceed 100% on multicore workloads.

Pulling an image does not update a container created from an older image.
The updater rejects --restart because a restart cannot apply the new image.
For a Compose project, run these from its configuration directory instead:

```bash
docker compose pull
docker compose up -d
```

The cleaner normally prunes dangling images. --days 30 instead selects unused
images created more than 720 hours ago, not images last used 30 days ago. Docker
retains images referenced by running or stopped containers. The normal Docker
confirmation prompt remains; --force suppresses it for deliberate automation.

## Local runner API

This is a local administration exercise with the Docker privileges of its
process. It is not an authenticated service for remote clients. Keep the
default loopback binding and use a Docker context you control.

```bash
python scripts/container_runner.py
```

In another terminal:

```bash
curl --fail --request POST http://127.0.0.1:8080/launch_container \
  --header 'Content-Type: application/json' \
  --data '{"name":"notes-runner-web","image":"nginx:stable-alpine"}'
docker rm -f notes-runner-web
```

The original d1 (name) and d2 (image) JSON keys remain supported. Values are
validated and passed to Docker as separate arguments, without sudo or a shell.
Container creation errors return an HTTP failure response.

## Validation

```bash
python -m unittest discover -s tests -v
python -m compileall -q scripts projects/flask tests
```

The unit suite mocks Docker commands. CI additionally validates generated
Compose files and builds and serves the Apache and Flask examples with Docker.

## References

- [Compose specification](https://docs.docker.com/reference/compose-file/)
- [Docker stats](https://docs.docker.com/reference/cli/docker/container/stats/)
- [Image pruning and creation-age filters](https://docs.docker.com/reference/cli/docker/image/prune/)
