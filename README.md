# Docker Notes

Notes, hands-on projects, and Python utilities for learning Docker.

## Start Here

1. Read the [introduction](notes/01_intro.md) and [installation guide](notes/02_installation.md).
2. Practice the [basic commands](notes/03_basic_commands.md), then build the included [Apache website](projects/apache/README.md).
3. Run the [Flask Compose lab](projects/flask/README.md), then explore [networking](notes/05_networking.md) and [security](notes/06_security.md).

Commands use the Compose plugin syntax, docker compose. Check docker version
and docker compose version before starting a lab.

## Notes

| Topic | Description |
|-------|-------------|
| [Introduction](notes/01_intro.md) | Images, containers, and containerization. |
| [Installation](notes/02_installation.md) | Platform-specific setup and verification. |
| [Basic commands](notes/03_basic_commands.md) | Build, run, inspect, persist data, and clean up. |
| [Dockerfiles](notes/04_docker_file.md) | Build context, caching, runtime commands, and secrets. |
| [Networking](notes/05_networking.md) | Bridge DNS, namespace sharing, published ports, and Swarm overlays. |
| [Security](notes/06_security.md) | Daemon access, runtime permissions, images, and secrets. |
| [Swarm](notes/07_swarm.md) | Nodes, services, managers, and quorum. |
| [Events](notes/08_docker_events.md) | Live streams, bounded history, and event filters. |
| [Command reference](notes/all_comands.md) | A compact CLI lookup table. |

## Projects

| Project | Description |
|---------|-------------|
| [Apache](projects/apache/README.md) | Build and serve the included static website. |
| [Flask](projects/flask/README.md) | A runnable app, Dockerfile, health check, and Compose file. |
| [Nginx](projects/nginx/README.md) | Serve static content from a read-only bind mount. |
| [Node.js](projects/nodejs/README.md) | An application behind an Nginx reverse proxy. |
| [MySQL](projects/mysql/README.md) | A local relational database with persistent storage. |
| [PostgreSQL](projects/postgresql/README.md) | A local database and sample SQL. |
| [MongoDB](projects/mongodb/README.md) | Document storage and a named data volume. |
| [VirtualBox networking](projects/networking/virutalbox_lan/README.md) | Publish a VM-hosted container to the LAN. |

## Scripts and Checks

See the [script guide](scripts/README.md) for dependencies, examples, and behavior.
With Python 3.10 or later, run from the repository root:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python -m compileall -q scripts projects/flask tests
```

The unit tests do not require Docker. CI also validates Compose output and
builds and serves the Apache and Flask projects.

## Assessing Your Docker Proficiency

Evaluate your Docker understanding and skills using the following benchmarks:

### Fundamental Concepts

1. **Containerization vs. Virtualization**:
   - Distinguish between containers and traditional virtual machines.
   - Recognize how containers optimize performance by sharing the host system's kernel, whereas VMs require their own OS instance.

2. **Linux Kernel Components**:
   - Understand critical Linux kernel components that power containerization, like cgroups and namespaces.

### Practical Knowledge

3. **Utilizing Public Docker Images**:
   - Pull and execute containers from images on Docker Hub or other public repositories.

4. **Crafting Dockerfiles**:
   - Write Dockerfiles that adhere to best practices:
     - Optimize layer ordering for caching.
     - Leverage multi-stage builds to reduce image size.
     - Ensure the usage of secure base images and up-to-date dependencies.

5. **Docker Compose Mastery**:
   - Create `docker compose` configurations to manage multiple containerized applications, easing local development and testing setups.

6. **Docker Networking**:
   - Understand Docker's various networking modes, such as bridge, host, and overlay.
   - Set up communication between containers and define how external systems access them.

### Advanced Practices

7. **Docker Security**:
   - Enforce Docker security best practices:
     - Operate containers as non-root users.
     - Opt for secure and lightweight base images.
     - Consistently scan images for potential vulnerabilities.
     - Use read-only filesystems when suitable.

8. **Alternative Containerization Tools**:
   - Get acquainted with other container tools beyond Docker:
     - `buildkit`: A modern approach to building container images.
     - `buildah`: Constructs OCI-compatible container images.

## Contributing

Your contributions are valued! For significant updates or changes, initiate an issue for discussion.

Ensure that you adapt tests to reflect your changes where necessary.

## License
[MIT License](https://choosealicense.com/licenses/mit/)
