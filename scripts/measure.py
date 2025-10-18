#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to measure wall time, peak RAM, and digits/s for a command.
Example: python scripts/measure.py 1000 "python code/pi_engine.py chud --digits 1000 --chunk 1000 --out runs/out/pi_1k.txt"
"""

import sys
import time
import psutil
import subprocess
import os

def measure_command(digits, command):
    process = psutil.Process()
    start_time = time.time()
    peak_ram = 0

    # Run the command
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Command failed: {result.stderr}", file=sys.stderr)
        sys.exit(2)

    end_time = time.time()
    wall_time = end_time - start_time

    # Get peak RAM (in MB)
    peak_ram = process.memory_info().rss / 1024 / 1024  # MB

    digits_per_s = digits / wall_time if wall_time > 0 else 0

    print(f"Wall time: {wall_time:.2f}s")
    print(f"Peak RAM: {peak_ram:.2f}MB")
    print(f"Digits/s: {digits_per_s:.2f}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python scripts/measure.py <digits> <command>")
        sys.exit(1)
    digits = int(sys.argv[1])
    command = " ".join(sys.argv[2:])
    measure_command(digits, command)
