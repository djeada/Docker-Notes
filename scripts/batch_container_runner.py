#!/usr/bin/env python3
"""Run containers described as image,name=NAME,port=PORT,env=KEY:VALUE,volume=SOURCE:TARGET.

The port is published to 127.0.0.1 with the same host/container port number.
Quote each specification; commas delimit options and cannot appear in values.
"""

import argparse
import re
import subprocess
import sys


def parse_image(spec):
    image, *options = spec.split(",")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._/:@+-]*", image):
        raise ValueError("A valid image reference is required.")
    result = {"image": image, "name": None, "port": None, "envs": {}, "volumes": []}
    for option in options:
        key, separator, value = option.partition("=")
        if not separator or not value:
            raise ValueError(f"Invalid option: {option!r}")
        if key == "name":
            if result["name"] is not None or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", value):
                raise ValueError("Provide one valid container name.")
            result["name"] = value
        elif key == "port":
            if result["port"] is not None:
                raise ValueError("Provide only one port per container.")
            port = int(value)
            if not 1 <= port <= 65535:
                raise ValueError("Port must be between 1 and 65535.")
            result["port"] = port
        elif key == "env":
            env_key, colon, env_value = value.partition(":")
            if not colon or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", env_key):
                raise ValueError("Environment entries must use KEY:VALUE.")
            result["envs"][env_key] = env_value
        elif key == "volume":
            result["volumes"].append(value)
        else:
            raise ValueError(f"Unknown option: {key!r}")
    return result


def run_container(image, name=None, port=None, envs=None, volumes=None):
    cmd = ["docker", "run", "-d"]
    if name:
        cmd += ["--name", name]
    if port:
        cmd += ["-p", f"127.0.0.1:{port}:{port}"]
    for key, value in (envs or {}).items():
        cmd += ["-e", f"{key}={value}"]
    for volume in volumes or []:
        cmd += ["-v", volume]
    cmd.append(image)
    subprocess.run(cmd, check=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("images", nargs="+")
    args = parser.parse_args(argv)
    try:
        # Validate every specification before starting the first container.
        containers = [parse_image(spec) for spec in args.images]
    except ValueError as exc:
        parser.error(str(exc))
    try:
        for container in containers:
            run_container(**container)
    except (OSError, subprocess.CalledProcessError) as exc:
        print(f"Docker failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
