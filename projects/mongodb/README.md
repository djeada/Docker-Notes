# Project: Setting Up MongoDB with Docker

## Objective

To set up and run a MongoDB database using Docker. This project aims to introduce the basics of Docker, managing MongoDB in a containerized environment, and performing basic database operations.

## Skills Learned

- Understanding Docker fundamentals
- Running MongoDB in a Docker container
- Basic MongoDB operations (CRUD - Create, Read, Update, Delete)
- Database management and maintenance in MongoDB
- Ensuring data persistence in Docker

## Tools Needed

- Docker installed on your system
- MongoDB Compass (optional) for a GUI-based interaction with the database
- Command line interface or terminal for executing Docker and MongoDB commands

## System Diagram

```
+--------------------------+
|  Local Machine           |
|  (Your Computer)         |
|  +--------------------+  |
|  | Docker             |  |
|  | +-----------+      |  |       +--------------------------------+
|  | | MongoDB   |<--------------->| MongoDB Client                 |
|  | | Container |      |  |       | (Accessing & Managing Database)|
|  | +-----------+      |  |       +--------------------------------+
|  |       ^            |  |
|  |       |            |  |
|  |       v            |  |
|  |  +--------------+  |  |
|  |  | Data Volume  |  |  |
|  |  | (For         |  |  |
|  |  | Persistence) |  |  |
|  |  +--------------+  |  |
|  +--------------------+  |
+--------------------------+
```

## Detailed Steps

1. **Pull MongoDB Image**

Pull the official MongoDB image from Docker Hub:

```bash
docker pull mongo
```

2. **Run MongoDB Container**

Start a MongoDB container with a specified data volume for data persistence:

```bash
docker run --name mongodb-container -d -v mongodb-data:/data/db -p 127.0.0.1:27017:27017 mongo
```

This command runs MongoDB in a container named `mongodb-container`, mapping port 27017 on your host to the container. It also creates a volume named `mongodb-data` for persisting data.

3. **Interact with MongoDB**

This local-only exercise does not enable authentication. Connect with MongoDB
Compass using `mongodb://127.0.0.1:27017`, or run `docker exec -it mongodb-container mongosh`.
Configure authentication before allowing other machines to access the database.

4. **Basic CRUD Operations**

Experiment with basic CRUD (Create, Read, Update, Delete) operations in MongoDB. Create a database and collections, insert documents, query data, update documents, and delete data.

5. **Database Management**

Learn basic database management tasks such as creating indexes, setting up users and roles, and understanding MongoDB's storage engine.

6. **Data Persistence**

Understand how the Docker volume (`mongodb-data`) is used for data persistence. Even if the container is stopped or removed, the data persists in the volume.

7. **Backup and Restore**

Practice backing up the MongoDB data using Docker volume backups. Learn to restore these backups to recover your database state.

8. **Monitoring and Logs**

Monitor the MongoDB container by checking logs:

```bash
docker logs mongodb-container
```

Understand the importance of logs for database administration and troubleshooting.
