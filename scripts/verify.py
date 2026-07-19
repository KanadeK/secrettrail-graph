from __future__ import annotations

import subprocess
import sys

commands = [
    [sys.executable, "-m", "ruff", "check", "."],
    [sys.executable, "-m", "mypy", "src"],
    [
        sys.executable,
        "-m",
        "pytest",
        "-q",
        "--cov=src",
        "--cov-report=term-missing",
        "--cov-fail-under=80",
    ],
    [sys.executable, "-m", "build"],
]
for command in commands:
    subprocess.run(command, check=True)
