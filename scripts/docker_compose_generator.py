#!/usr/bin/env python3
"""Generate Compose files; start each service with --service-name.

Example (run from the repository root):
    python3 scripts/docker_compose_generator.py --networks webnet --volumes dbdata \
        --service-name web --service-image nginx:stable --service-ports 127.0.0.1:8080:80 \
        --service-name db --service-image mysql:8.4 \
        --service-volumes dbdata:/var/lib/mysql --service-env MYSQL_ROOT_PASSWORD:local-demo
"""

import argparse
from pathlib import Path
import re

import yaml


NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]*")


def split_items(value):
    items = [item.strip() for item in value.split(",")]
    if not all(items):
        raise ValueError("Comma-separated values must not contain empty entries.")
    return items


class ServiceOption(argparse.Action):
    """Attach options to the most recent --service-name, preserving CLI order."""

    def __call__(self, parser, namespace, values, option_string=None):
        services = getattr(namespace, self.dest, None)
        if services is None:
            services = []
            setattr(namespace, self.dest, services)
        field = option_string.removeprefix("--service-")
        if field == "name":
            services.append({"name": values})
        elif not services:
            parser.error(f"{option_string} must follow --service-name.")
        elif field in services[-1]:
            parser.error(f"{option_string} was repeated for the same service.")
        else:
            services[-1][field] = values


def create_service(service):
    if not service.get("image", "").strip():
        raise ValueError(f"Service {service['name']!r} requires --service-image.")
    result = {"image": service["image"]}
    for field in ("ports", "volumes"):
        if field in service:
            result[field] = split_items(service[field])
    if "env" in service:
        environment = {}
        for pair in split_items(service["env"]):
            key, separator, value = pair.partition(":")
            if not separator or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", key):
                raise ValueError("Environment entries must use KEY:VALUE.")
            if key in environment:
                raise ValueError(f"Duplicate environment key: {key}")
            environment[key] = value
        result["environment"] = environment
    return result


def build_compose(args):
    if not args.services:
        raise ValueError("At least one --service-name and --service-image are required.")
    networks = split_items(args.networks) if args.networks else []
    volumes = split_items(args.volumes) if args.volumes else []
    for name in networks + volumes:
        if not NAME.fullmatch(name):
            raise ValueError(f"Invalid network or volume name: {name!r}")

    compose = {"services": {}}
    for service in args.services:
        name = service["name"]
        if not NAME.fullmatch(name):
            raise ValueError(f"Invalid service name: {name!r}")
        if name in compose["services"]:
            raise ValueError(f"Duplicate service name: {name!r}")
        data = create_service(service)
        if networks:
            data["networks"] = networks.copy()
        # Named mounts need declarations; absolute and relative bind paths do not.
        for mount in data.get("volumes", []):
            source, separator, _ = mount.partition(":")
            windows_bind = re.match(r"^[A-Za-z]:[\\/]", mount)
            if separator and not windows_bind and NAME.fullmatch(source) and source not in volumes:
                volumes.append(source)
        compose["services"][name] = data
    if networks:
        compose["networks"] = {name: {} for name in networks}
    if volumes:
        compose["volumes"] = {name: {} for name in volumes}
    return compose


def make_parser():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--networks", help="Comma-separated networks attached to every service.")
    parser.add_argument("--volumes", help="Comma-separated named volume declarations.")
    parser.add_argument("--output", type=Path, default=Path("docker-compose.yml"))
    parser.add_argument("--force", action="store_true", help="Replace an existing output file.")
    for field in ("name", "image", "ports", "volumes", "env"):
        parser.add_argument(f"--service-{field}", dest="services", action=ServiceOption)
    return parser


def main(argv=None):
    parser = make_parser()
    args = parser.parse_args(argv)
    try:
        compose = build_compose(args)
        with args.output.open("w" if args.force else "x", encoding="utf-8") as output:
            yaml.safe_dump(compose, output, sort_keys=False)
    except (ValueError, OSError) as exc:
        parser.error(str(exc))
    print(f"Wrote {args.output}. Validate with: docker compose -f {args.output} config --quiet")


if __name__ == "__main__":
    main()
