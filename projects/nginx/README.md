## Setting Up an Nginx Docker Container

This guide will walk you through deploying an Nginx container using Docker and hosting a simple static web page.

### Creating a Static Web Page

For this demonstration, let's start by creating a simple HTML file that we wish to serve via our Nginx server:

Create a directory for your project:

```bash
mkdir nginx_sample_site
cd nginx_sample_site
```

Now, create a index.html file:

```bash
echo "<h1>Welcome to our Nginx Docker Container!</h1>" > index.html
```

### Setting Up Nginx Docker Container

Now, we'll run an Nginx Docker container and mount our static site to it:

```bash
docker run --name nginx_container -p 127.0.0.1:8080:80 -v "$(pwd):/usr/share/nginx/html:ro" -d nginx:stable-alpine
```

- `--name nginx_container`: Names our container "nginx_container" for easy reference.
- `-p 127.0.0.1:8080:80`: Maps local host port 8080 to container port 80.
- `-v "$(pwd):/usr/share/nginx/html:ro"`: Mounts the current directory at Nginx's content directory. Quoting preserves paths containing spaces; :ro makes the mount read-only.

### Accessing the Static Site

Once the container is up and running, you can access your static website by navigating to:

```
http://localhost:8080
```

You should see a message saying "Welcome to our Nginx Docker Container!"
