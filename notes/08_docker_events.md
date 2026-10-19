# Docker Events

docker events streams daemon events for container lifecycle, images, networks,
volumes, and other supported objects. It complements application logs.

## Live and historical queries

```bash
docker events --filter type=container
docker events --since 10m --until 0s --filter type=container
docker events --filter type=network --filter event=disconnect
docker events --format '{{json .}}'
```

The first and last commands keep streaming until interrupted. --since asks for
available historical events before continuing with live events. --until bounds
the stream; 0s means the current time when the command starts.

Only the last 256 events are available for historical retrieval. --since 24h
does not create a durable 24-hour event archive. Local-scope events belong to
their daemon; Swarm-scoped events are available through managers.

| Flag | Purpose |
|------|---------|
| --filter / -f | Select event types, actions, names/IDs, or supported attributes. |
| --since | Include retained events after a timestamp or duration. |
| --until | Stop at the specified timestamp or relative time. |
| --format | Format each event using a Go template, including JSON output. |

Filters with different keys combine with AND. Multiple values of the same key
combine with OR. For example, this watches container starts or deaths:

```bash
docker events --filter type=container --filter event=start --filter event=die
```

## JSON fields and API transport

The Engine GET /events endpoint streams JSON objects; it is not a browser
Server-Sent Events feed using text/event-stream and data: records.

A simplified event looks like this:

```json
{
  "Type": "container",
  "Action": "die",
  "Actor": {
    "ID": "container-id",
    "Attributes": {
      "name": "notes-web",
      "image": "nginx:stable-alpine",
      "exitCode": "1"
    }
  },
  "time": 1792458000,
  "timeNano": 1792458000000000000
}
```

Action and attribute names depend on the event. An oom event provides stronger
evidence of an out-of-memory condition than a kill event's signal alone.
An unhealthy status does not automatically make standalone Docker restart a
container; restart policies act on process exit.

## A two-terminal exercise

Start this in terminal 1:

```bash
docker events --filter type=container --filter container=notes-event-demo
```

In terminal 2, create a short-lived container:

```bash
docker run --rm --name notes-event-demo alpine:3.22 echo hello
```

Watch create, start, die, and destroy events, then stop the stream with Ctrl-C.
To retain a history, collect the stream in a persistent logging system. Events
are operational signals, not a complete record of authenticated user actions.
On Kubernetes nodes using other runtimes, use that runtime's tooling and
Kubernetes events rather than expecting Docker to see every pod.

## References

- [docker events CLI and filters](https://docs.docker.com/reference/cli/docker/system/events/)
- [Docker Engine API](https://docs.docker.com/reference/api/engine/)
- [Container restart policies](https://docs.docker.com/engine/containers/start-containers-automatically/)

