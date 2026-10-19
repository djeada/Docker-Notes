# Docker Networking

For ordinary Linux bridge networking, a container has its own network namespace
and interface. Docker connects it to a host bridge and configures routing and
port publishing. Docker Desktop runs Linux containers in a VM, so container
addresses are not generally addresses you can reach directly from the desktop.

## Drivers and namespace modes

| Driver or mode | Behavior |
|----------------|----------|
| bridge | Connects containers on one Docker host. User-defined bridges provide name/alias resolution. |
| host | Shares the host's network namespace; other namespaces are still separate. Port publishing is ignored. |
| overlay | Connects Swarm services across Docker hosts; standalone containers need an attachable network. |
| macvlan | Gives containers separate MAC addresses on an existing Layer 2 network. |
| ipvlan | Connects containers through a parent interface without requiring a distinct MAC per container. |
| none | Leaves only loopback in the container's network namespace. |
| container:NAME | Shares another container's network namespace, including its IP addresses, ports, and loopback. |

Docker overlay networking requires Swarm mode, even for standalone containers.
Kubernetes CNI networking is separate from Docker's overlay driver. Overlay
application traffic is not encrypted by default; --opt encrypted enables
encryption on supported Linux overlay networks.

Host networking is supported on Linux Docker Engine and, when enabled, on
supported Docker Desktop versions. It removes network isolation, not every
form of container isolation.

## Default bridge versus a user-defined bridge

The default bridge is normally named bridge and its Linux bridge interface is
usually docker0. Inspect its configured subnet instead of assuming it is always
172.17.0.0/16:

```bash
docker network inspect bridge
```

Containers on the default bridge can communicate by IP. Automatic container-name
resolution is a feature of user-defined bridge networks; the old --link feature
is unnecessary for new examples.

Try this on one Docker host:

```bash
docker network create notes-net
docker run --detach --name notes-server --network notes-net nginx:stable-alpine
docker run --rm --network notes-net alpine:3.22 wget -qO- http://notes-server/
docker network inspect notes-net
```

The client uses notes-server:80, the container's listening port. No host port
needs publishing for this communication. Compose creates a project network and
makes services discoverable by service name by default.

Clean up the resources created above:

```bash
docker rm -f notes-server
docker network rm notes-net
```

## Publishing ports

```bash
docker run --detach --name notes-web --publish 127.0.0.1:8080:80 nginx:stable-alpine
docker port notes-web
curl --fail http://127.0.0.1:8080/
docker rm -f notes-web
```

The order is HOST_IP:HOST_PORT:CONTAINER_PORT. Omitting HOST_IP normally publishes
on all host interfaces. EXPOSE in a Dockerfile is documentation; -p publishes a
port, and -P publishes documented ports on automatically selected host ports.

Inside a container, localhost refers to that container's network namespace.
For containers on a shared bridge, use the other container's name, not localhost.
A service must listen on a container interface such as 0.0.0.0 to receive requests
from other containers.

Containers in container:NAME mode instead share localhost and cannot independently
bind the same address/port. For example, a diagnostic container sharing a web
server's namespace can reach that server at localhost.

## Cross-host Swarm networking

Run these on an initialized Swarm manager with worker connectivity configured:

```bash
docker network create --driver overlay --attachable --opt encrypted notes-overlay
docker service create --name notes-web --network notes-overlay \
  --publish published=8080,target=80 --replicas 2 nginx:stable-alpine
docker service ps notes-web
docker service rm notes-web
docker network rm notes-overlay
```

Swarm ingress publishing accepts connections on participating nodes, including
workers, and routes them to service tasks. This is different from publishing a
standalone container port. Removing a service and its tasks is asynchronous; wait
for endpoints to disappear before removing its network.

## Troubleshooting

1. Check state with docker ps -a and application output with docker logs.
2. Use docker port to confirm the host mapping.
3. Use docker network inspect to check network membership and subnet overlaps.
4. Test service DNS names from a container on the same user-defined network.
5. Check that the application listens on the expected port and interface.

ICMP reachability does not establish that a TCP service is accepting requests.
Many minimal images do not include ping or curl; use a temporary diagnostic
container rather than assuming those tools exist in every image.

## References

- [Networking overview and container namespace sharing](https://docs.docker.com/engine/network/)
- [Bridge driver](https://docs.docker.com/engine/network/drivers/bridge/)
- [Host driver](https://docs.docker.com/engine/network/drivers/host/)
- [Overlay driver and encryption](https://docs.docker.com/engine/network/drivers/overlay/)
