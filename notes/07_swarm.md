## Docker Swarm

Docker Swarm is Docker's built-in solution for container orchestration, allowing for easy scaling and management of Docker containers across multiple hosts.

- **Definition**: Native clustering and orchestration tool integrated into the Docker Engine.
- **Objective**: Establish a self-organizing, self-healing swarm ensuring container high availability and scalability.

**Key Points**:
- Activating Swarm Mode: Use `docker swarm init`.
- Not mandatory for every project: Useful for specific workloads requiring orchestration.
- Availability: In Docker Desktop (Mac or Windows), Docker CE, and Docker EE.

```
+------------------------------------------------------------------------------+
|                                    Docker CLI                                |
|                                                                              |
|     +----------------------------+           +----------------------------+  |
|     |        Development         |           |         Production         |  |
|     |         "Cluster"          |           |         "Cluster"          |  |
|     |                            |           |                            |  |
|     |   +-------+    +-------+   |           |   +-------+    +-------+   |  |
|     |   |       |    |       |   |           |   |       |    |       |   |  |
|     |   | Node1 |    | Node2 |   |           |   | Node1 |    | Node2 |   |  |
|     |   |       |    |       |   |           |   |       |    |       |   |  |
|     |   +-------+    +-------+   |           |   +-------+    +-------+   |  |
|     |                            |           |                            |  |
|     +----------------------------+           +----------------------------+  |
|                                                                              |
+------------------------------------------------------------------------------+
```

### Docker Swarm vs. Kubernetes

**Docker Swarm**:
- Built-in orchestration tool for Docker.
- Simplified setup.
- Best for small to medium-sized projects.
- Limited advanced features.
- Smaller community support.

**Kubernetes**:
- Open-source, originally developed by Google.
- Complex initial setup.
- Ideal for complex, large-scale projects.
- Extensive feature set.
- Robust community support.

### Core Concepts

1. **Node**: 
   - Machine/VM running Docker. 
   - Types: **Manager** (orchestration) and **Worker** (run services).

2. **Service**: 
   - Definition of tasks for nodes.

3. **Task**: 
   - Container instance with specific commands.

4. **Load Balancing**: 
   - Expose services to external sources with ingress balancing.

5. **Swarm Mode**: 
   - Cluster management within Docker Engine.

6. **Overlay Network**: 
   - Network across all swarm nodes, allowing inter-container communication.

### Key Commands

- **Swarm Initialization**: `docker swarm init --advertise-addr <MANAGER-IP>`
- **Joining a Swarm**: `docker swarm join --token <TOKEN> <MANAGER-IP>:2377`
- **Node Listing**: `docker node ls`
- **Service Management**:
  - Deployment: `docker service create --name <SERVICE-NAME> --replicas <NUM> <IMAGE-NAME>`
  - Listing: `docker service ls`
  - Inspection: `docker service inspect --pretty <SERVICE-NAME>`
  - Updating: `docker service update <OPTIONS> <SERVICE-NAME>`
  - Removal: `docker service rm <SERVICE-NAME>`

### Advantages

- **High Availability**: Resilience against node failures.
- **Scalability**: Adjust services based on demand.
- **Management**: Run node and service management commands against a manager. Workers run tasks but do not perform cluster management.
- **Built-in Security**: Automatic security certificates for nodes.

### Challenges

- **Stateful Applications**: Databases and similar apps pose management issues.
- **Network Overhead**: Overlay networks introduce minor performance overheads.
- **Manager Nodes**: Cluster updates require a majority of managers. Three managers tolerate one manager failure; five tolerate two. Losing quorum prevents management changes even if existing tasks keep running.

### Best Practices

- **Limit Manager Nodes**: 3 to 5 managers are often enough.
- **Continuous Monitoring**: Check node health and service distribution regularly.
- **Backup**: Especially critical for manager nodes housing the swarm state.

### References

- [Swarm administration and quorum](https://docs.docker.com/engine/swarm/admin_guide/)
- [Overlay networks](https://docs.docker.com/engine/network/drivers/overlay/)
