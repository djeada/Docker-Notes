# Docker Security

Linux containers share a kernel. Namespace isolation and resource controls help
separate workloads, but daemon access, capabilities, mounts, and host configuration
determine what a container can do.

## Daemon and host access

Use rootless Docker where it fits the workload, and retain the engine's default
seccomp profile and the host's supported AppArmor or SELinux policy. Rootless
mode runs the daemon and containers without host root; user-namespace remapping
is a different configuration for a rootful daemon.

Control of a rootful Docker socket normally gives root-level control of its host.
A socket-mounted helper is therefore not an isolation boundary. Keep the
[local container-runner demo](../scripts/README.md) on loopback; its caller can
ask Docker to start processes, so it is not a public application endpoint.

```bash
docker info --format '{{json .SecurityOptions}}'
```

The reported options depend on the host. AppArmor and SELinux are platform
choices, not two policies every installation must enable simultaneously.

## Runtime permissions

| Option | Purpose |
|--------|---------|
| --user UID:GID | Select a non-root container identity when the image supports it. |
| --cap-drop ALL | Remove Linux capabilities; add back only those the workload requires. |
| --security-opt no-new-privileges=true | Prevent exec-time privilege gain through setuid/setgid or file capabilities. |
| --read-only | Make the container root filesystem read-only. |
| --tmpfs /tmp | Supply a writable temporary filesystem for software that needs it. |
| --memory and --cpus | Bound resource use. |

The Flask lab already sets a non-root USER. After building its image, try:

```bash
docker run --rm --cap-drop ALL \
  --security-opt no-new-privileges=true \
  --read-only --tmpfs /tmp:size=64m \
  --memory 256m --cpus 1 \
  --publish 127.0.0.1:5000:5000 docker-notes-flask
```

Whether an image works with a read-only root depends on its write paths. PID 1
has signal-handling responsibilities; its PID alone does not grant root privileges.

## Images and build inputs

Use maintained base images, review dependencies, and rebuild as fixes become
available. Tags can change; digests identify exact image content. An SBOM
describes components but does not itself prove authenticity or absence of
vulnerabilities. Verification requires a trusted source and an explicit
verification policy.

BuildKit can attach SBOM attestations to an image pushed to a registry you
control:

```bash
docker buildx build --sbom=true --tag YOUR_REGISTRY/YOUR_IMAGE:TAG --push .
```

SBOM generation and image scanning tools are additional capabilities; a bare
Docker CLI does not guarantee that a docker sbom command is installed.

## Networks and secrets

Publish only the ports the application needs. Use loopback bindings for local
labs. User-defined networks separate unrelated stacks by default, but services
sharing a network can reach each other's listening ports.

Swarm encrypts management traffic. Overlay application traffic needs
--opt encrypted to enable data-plane encryption. Application TLS is a separate
decision.

Swarm secrets are distributed to authorized services and mounted in memory for
Linux containers. Local Compose file-backed secrets are mounted from host files;
they do not provide the same encrypted Swarm distribution and storage guarantees.
Do not commit the source secret file. ENV and build arguments are visible to
users with suitable image/daemon access and are not secret stores.

## Observability

Use [Docker events](08_docker_events.md) alongside application and host logs.
The event stream has limited history and does not reliably identify the human
behind every action; it is not a complete audit trail.

## References

- [Docker Engine security](https://docs.docker.com/engine/security/)
- [Rootless mode](https://docs.docker.com/engine/security/rootless/)
- [Swarm secrets](https://docs.docker.com/engine/swarm/secrets/)
- [Compose secrets](https://docs.docker.com/compose/how-tos/use-secrets/)
- [SBOM attestations](https://docs.docker.com/build/metadata/attestations/sbom/)
