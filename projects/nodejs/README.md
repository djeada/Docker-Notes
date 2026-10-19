## Setting Up a Node.js Application with Nginx in Docker

This guide will walk you through the deployment of a Node.js application using Docker, with Nginx acting as a reverse proxy.

### Create a Node.js Application

Let's begin by creating a simple `Express.js` app:

app.js:

```javascript
const express = require('express');

const app = express();
const PORT = 3000;

app.get('/', (req, res) => {
    res.send('Hello from Node.js running in Docker!');
});

app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
```

And a `package.json` file:

```json
{
  "name": "docker-node-app",
  "version": "1.0.0",
  "main": "app.js",
  "scripts": {
    "start": "node app.js"
  },
  "dependencies": {
    "express": "^4.17.1"
  }
}
```

### Dockerizing the Node.js App

For this step, you'll need a Dockerfile:

```Dockerfile
FROM node:24-slim

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 3000
CMD ["npm", "start"]
```

### Setting up Nginx

First, create an Nginx configuration file named `nginx.conf`:

```nginx
server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://node_app:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Next, you'll need a `docker-compose.yml` file to orchestrate the Node.js app and the Nginx containers:

```yaml
services:
  node_app:
    build: .

  nginx:
    image: nginx:latest
    ports:
      - "127.0.0.1:8080:80"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf:ro
    depends_on:
      - node_app
```

### Deploying with Docker Compose

With the files set up, use Docker Compose to deploy both the Node.js app and the Nginx server:

```bash
docker compose up --build
```

Open `http://localhost:8080` to see the Node.js response through Nginx. The app's
port 3000 is reached by service name on the Compose network and does not need
publishing on the host. depends_on controls startup order but does not wait for
HTTP readiness; use health checks and application retries when readiness matters.

Stop the project with `docker compose down`. See [Node.js release support](https://nodejs.org/en/about/previous-releases)
and [Compose startup order](https://docs.docker.com/compose/how-tos/startup-order/).
