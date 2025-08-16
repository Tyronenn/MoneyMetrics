#!/usr/bin/env python3
"""
Bootstrap script to create a virtual environment and install dependencies.

Usage:
    python setup_env.py            # Install runtime dependencies
    python setup_env.py --dev      # Include dev dependencies (tests, etc.)
"""

from __future__ import annotations

import argparse
import os
import platform
import subprocess
import sys
import venv


def run(cmd: list[str]) -> None:
    """Run a subprocess and exit on failure."""
    subprocess.check_call(cmd)


def main() -> None:
    if sys.version_info < (3, 10):
        raise RuntimeError("Python 3.10+ is required.")

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dev",
        action="store_true",
        help="Install additional development requirements.",
    )
    args = parser.parse_args()

    env_dir = os.path.join(os.path.dirname(__file__), "venv")
    print(f"Creating virtual environment at {env_dir!r} …")
    venv.EnvBuilder(with_pip=True).create(env_dir)

    if platform.system() == "Windows":
        python = os.path.join(env_dir, "Scripts", "python.exe")
        pip = os.path.join(env_dir, "Scripts", "pip.exe")
    else:
        python = os.path.join(env_dir, "bin", "python")
        pip = os.path.join(env_dir, "bin", "pip")

    print("Installing runtime dependencies …")
    run([pip, "install", "--upgrade", "pip"])
    run([pip, "install", "-r", "requirements.txt"])

    if args.dev:
        print("Installing development dependencies …")
        run([pip, "install", "-r", "requirements-dev.txt"])

    print("\nSetup complete!")
    print(
        "Activate the environment with:\n  source venv/bin/activate (macOS/Linux)\n  venv\\Scripts\\activate (Windows)"
    )
    print(f"Run the application using:\n  {python} main.py")


if __name__ == "__main__":
    main()
