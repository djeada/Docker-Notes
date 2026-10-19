# Installing Docker

Choose the instructions for your actual operating system and supported release.
Ubuntu and Debian use different package repositories; Ubuntu's repository is not
a general installation source for all Debian-based distributions.

| Platform | Official instructions |
|----------|-----------------------|
| Ubuntu | [Install Docker Engine on Ubuntu](https://docs.docker.com/engine/install/ubuntu/) |
| Debian | [Install Docker Engine on Debian](https://docs.docker.com/engine/install/debian/) |
| Windows | [Install Docker Desktop on Windows](https://docs.docker.com/desktop/setup/install/windows-install/) |
| macOS | [Install Docker Desktop on Mac](https://docs.docker.com/desktop/setup/install/mac-install/) |

## Linux

Follow the matching guide to check supported versions, remove conflicting packages,
configure Docker's signing key, and add the correct repository. After configuring
the official Ubuntu or Debian repository, install the engine and CLI plugins:

```bash
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo docker run --rm hello-world
```

Use the [Linux post-installation guide](https://docs.docker.com/engine/install/linux-postinstall/)
or [rootless mode](https://docs.docker.com/engine/security/rootless/) to configure
access. Membership in the docker group grants control of the daemon and normally
root-level power over a rootful Docker host.

## Windows and macOS

Install Docker Desktop using the platform guide above and start it before running
commands. On Windows, follow the current WSL 2 and virtualization requirements.
Windows Home can run Linux containers through WSL 2; Windows containers have
different edition and backend requirements.

## Verify the client, server, and plugins

```bash
docker version
docker info
docker buildx version
docker compose version
docker run --rm hello-world
```

A client version alone does not prove the daemon is reachable. If docker info
fails, check that Docker Desktop or the engine service is running and that your
selected context and permissions are correct:

```bash
docker context ls
docker context show
```

These notes use the Compose plugin command, docker compose. The older standalone
docker-compose executable is not required.
