# Hosting a Static Website using Docker and Apache

## Objective

The goal of this project is to host a static website (comprising HTML, CSS, and JavaScript files) using the Apache web server within a Docker container. This setup illustrates the principles of containerization and the basics of web hosting using Docker and Apache.

## Skills Learned

- Docker basics: Understanding Docker and its ecosystem.
- Containerizing Apache web server: Creating a Docker container specifically for running an Apache web server.
- Volume management in Docker: Learning how to manage data within Docker containers, especially for serving static website content.

## Tools Needed

- **Docker**: Ensure Docker is installed and running on your system.
- **Website Files**: HTML files are mandatory; CSS and JavaScript files are optional but recommended for a richer website.
- **Text Editor**: For writing the Dockerfile and editing configuration files.

## System Diagram

```
+---------------------+
|  Local Machine      |
|  (Your Computer)    |
|  +---------------+  |
|  | Docker        |  |
|  | +-----------+ |  |       +-----------------------------+
|  | | Apache    |<---------->| Browser (Accessing Website) |
|  | | Container | |  |       +-----------------------------+
|  | |           | |  |
|  | | /htdocs   | |  |   Port 8080
|  | +-----------+ |  |   (mapped to container's port 80)
|  |       ^       |  |
|  |       |       |  |
|  |       v       |  |
|  |  +---------+  |  |
|  |  | Website |  |  |
|  |  | Content |  |  |
|  |  | (HTML,  |  |  |
|  |  | CSS, JS)|  |  |
|  |  +---------+  |  |
|  +---------------+  |
+---------------------+
```

## Detailed Steps

### 1. Create Your Website Content

- Prepare your static website content including HTML, CSS, and JS files.
- Store them in a directory on your host system, for example, `~/mywebsite`.
- The structure of the `mywebsite` directory might look like this:

```
/mywebsite
│
├── html
│ ├── index.html
│ ├── about.html
│ ├── contact.html
│ └── styles
│ └── style.css
│
└── Dockerfile
```

### 2. Create a Dockerfile

- In your website directory (`~/mywebsite`), create a file named `Dockerfile`.
- Edit the Dockerfile to use the official Apache image and copy your website files into the image:

```
FROM httpd:2.4

COPY ./html/ /usr/local/apache2/htdocs/
```

This Dockerfile uses the official Apache (httpd) image as a base and copies the contents of your local `html` directory into the default Apache document root in the container.

### 3. Build Your Docker Image

- Use the included files by navigating to `projects/apache/mywebsite` from the repository root. If you created a separate site, use that site's directory instead.
- Build your Docker image with the command:

```
docker build -t mywebsite .
```

`mywebsite` is the tag/name for your Docker image.

### 4. Run Your Apache Container

- Run a container from your image with the command:

```
docker run -d --name my-apache-app -p 127.0.0.1:8080:80 mywebsite
```

This command starts a container named `my-apache-app`, mapping port 8080 on your host to port 80 in the container.

The binding makes this lab available on the local host. The website is copied into
the image; this example does not mount a content volume. Rebuild the image and
recreate the container after changing the HTML files.

### 5. Access Your Website

- Open a web browser and navigate to `http://localhost:8080`.
- You should now see your static website served by Apache running in a Docker container.

### 6. Clean Up

```bash
docker rm -f my-apache-app
```
