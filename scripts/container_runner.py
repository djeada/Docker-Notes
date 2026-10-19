#!/usr/bin/env python3
"""Local Docker administration demo. Requires Flask and Docker CLI access."""

import re
import subprocess

from flask import Flask, jsonify, request


app = Flask(__name__)


@app.route("/launch_container", methods=["POST"])
def launch_container():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(message="A JSON object is required"), 400

    # Keep the original d1/d2 request keys as aliases.
    name = data.get("name", data.get("d1"))
    image = data.get("image", data.get("d2"))
    if not isinstance(name, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", name):
        return jsonify(message="A valid container name is required"), 400
    if not isinstance(image, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._/:@+-]*", image):
        return jsonify(message="A valid image reference is required"), 400

    try:
        result = subprocess.run(
            ["docker", "run", "-d", "--name", name, image],
            capture_output=True, text=True, check=True, timeout=60,
        )
    except subprocess.TimeoutExpired:
        return jsonify(message="Docker did not respond within 60 seconds"), 504
    except OSError:
        return jsonify(message="Docker CLI could not be started"), 503
    except subprocess.CalledProcessError as exc:
        return jsonify(message=f"Error launching container: {exc.stderr.strip()}"), 500
    return jsonify(message=f"Container {name} launched successfully",
                   container_id=result.stdout.strip())


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
