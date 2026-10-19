"""A small Flask application served by Gunicorn in the Docker lab."""

from flask import Flask


app = Flask(__name__)


@app.get("/")
def home():
    return "Hello from Flask running in Docker!\n", 200, {"Content-Type": "text/plain; charset=utf-8"}
