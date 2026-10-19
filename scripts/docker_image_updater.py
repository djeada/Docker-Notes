#!/usr/bin/env python3
"""Pull image references used by running containers.

Pulling an image does not update an existing container, and restarting it does
not apply the new image. Recreate services from their original configuration
(for Compose projects: docker compose pull && docker compose up -d).
"""

import argparse
import subprocess
import sys


def get_running_containers():
    result = subprocess.run(["docker", "ps", "-q"], capture_output=True, text=True, check=True)
    return result.stdout.split()


def get_container_image(container_id):
    result = subprocess.run(
        ["docker", "inspect", "--format", "{{.Config.Image}}", container_id],
        capture_output=True, text=True, check=True,
    )
    image = result.stdout.strip()
    if not image:
        raise ValueError(f"No image reference found for container {container_id}.")
    return image


def pull_image(image_name):
    subprocess.run(["docker", "pull", image_name], check=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--restart", action="store_true",
                        help="Unsupported: restarting does not apply image updates.")
    args = parser.parse_args(argv)
    if args.restart:
        parser.error("--restart cannot apply image updates. Recreate containers from their configuration.")
    try:
        images = dict.fromkeys(get_container_image(cid) for cid in get_running_containers())
        if not images:
            print("No running containers.")
        for image in images:
            if image.startswith("sha256:"):
                print(f"Skipping local image ID {image}; rebuild it from its source.")
                continue
            print(f"Pulling image: {image}")
            pull_image(image)
        if images:
            print("Existing containers keep their original image. Recreate them to apply updates.")
    except (OSError, subprocess.CalledProcessError, ValueError) as exc:
        print(f"Unable to pull container images: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
