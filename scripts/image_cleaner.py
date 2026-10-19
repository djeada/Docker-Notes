#!/usr/bin/env python3
"""Prune unused images using Docker's reference tracking and confirmation prompt.

Without --days, remove dangling images. With --days N, remove unused images
created more than N days ago. Creation age is not time since last use.
"""

import argparse
import subprocess
import sys


def positive_days(value):
    days = int(value)
    if days <= 0:
        raise argparse.ArgumentTypeError("--days must be a positive integer.")
    return days


def prune_images(days=None, force=False):
    cmd = ["docker", "image", "prune"]
    if days is not None:
        cmd += ["--all", "--filter", f"until={days * 24}h"]
    if force:
        cmd.append("--force")
    subprocess.run(cmd, check=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--days", type=positive_days,
                        help="Prune unused images created more than this many days ago.")
    parser.add_argument("--force", action="store_true", help="Skip Docker's confirmation prompt.")
    args = parser.parse_args(argv)
    try:
        prune_images(args.days, args.force)
    except (OSError, subprocess.CalledProcessError) as exc:
        print(f"Unable to prune Docker images: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
