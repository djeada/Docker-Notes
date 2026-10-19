#!/usr/bin/env python3
"""Print Linux container CPU/memory percentages every 10 seconds."""

import json
import subprocess
import sys
import time


def get_container_stats():
    result = subprocess.run(
        ["docker", "stats", "--no-stream", "--format", "{{json .}}"],
        capture_output=True, text=True, check=True,
    )
    return [json.loads(line) for line in result.stdout.splitlines() if line.strip()]


def report_stats(stats, cpu_threshold, mem_threshold):
    for stat in stats:
        name = stat["Name"]
        cpu_percent = float(stat["CPUPerc"].removesuffix("%"))
        # Docker already calculates this percentage. MemUsage can contain
        # decimals and mixed B/KiB/MiB/GiB units, so do not parse it as integers.
        mem_percent = float(stat["MemPerc"].removesuffix("%"))
        print(f"{name} - CPU: {cpu_percent}%, Memory: {mem_percent:.2f}%")
        if cpu_threshold is not None and cpu_percent > cpu_threshold:
            print(f"ALERT: {name} has exceeded the CPU threshold!")
        if mem_threshold is not None and mem_percent > mem_threshold:
            print(f"ALERT: {name} has exceeded the Memory threshold!")


def monitor_containers(cpu_threshold, mem_threshold):
    while True:
        report_stats(get_container_stats(), cpu_threshold, mem_threshold)
        time.sleep(10)


def main():
    try:
        monitor_containers(75.0, 80.0)
    except KeyboardInterrupt:
        return 0
    except (OSError, subprocess.CalledProcessError, ValueError, KeyError) as exc:
        print(f"Unable to monitor Docker containers: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
