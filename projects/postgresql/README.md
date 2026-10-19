## Setting Up a PostgreSQL Docker Container

In this guide, we'll demonstrate how to deploy a PostgreSQL container using Docker and establish a sample database with tables to help you start.

### Launching the PostgreSQL Container

Start by initiating a PostgreSQL container instance. Naming your container is beneficial as it enables easy referencing later:

```bash
docker run -d --name postgres_container -p 127.0.0.1:5432:5432 \
  -v postgres-data:/var/lib/postgresql/data -e POSTGRES_PASSWORD=secret_pass postgres:17
```

- `--name postgres_container`: Assigns the name "postgres_container" to our container.
- `-p 127.0.0.1:5432:5432`: Publishes PostgreSQL only on the local host.
- `-v postgres-data:/var/lib/postgresql/data`: Keeps database files in a named volume for this PostgreSQL 17 example.
- `-e POSTGRES_PASSWORD=secret_pass`: Sets the password for the default PostgreSQL user "postgres" to "secret_pass".

### Accessing PostgreSQL Inside the Container

Wait for initialization using `docker logs postgres_container`, then open psql:

```bash
docker exec -it postgres_container psql -U postgres
```

This local Unix-socket connection normally uses the image's local authentication
configuration and does not prompt for a password. A TCP client connecting to
127.0.0.1:5432 uses user postgres and the local exercise password secret_pass.

### Creating a Database

Within the PostgreSQL prompt, set up your database and tables:

```SQL
-- Create a new database named 'sample_db'
CREATE DATABASE sample_db;
-- Connect to 'sample_db' for subsequent operations
\c sample_db
```

### Setting up a Sample Table

Let's create a products table as an example:

```SQL
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    date_added TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

Now, you have a PostgreSQL container running with a sample_db database and a products table. This basic setup can be the foundation for various applications, from web platforms to data analysis tools. Modify the table structures to match the specific requirements of your projects.

Remove the container with `docker rm -f postgres_container`; postgres-data remains.
Use the same major image version when reusing its data. Major upgrades need an
upgrade procedure rather than changing the image tag alone. PostgreSQL 18+ images
use a different default data layout; follow the [official image guide](https://hub.docker.com/_/postgres).
