from __future__ import annotations

import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
if subprocess.run(
    ["git", "status", "--porcelain"], cwd=root, capture_output=True, text=True, check=True
).stdout:
    raise SystemExit("Working tree is not clean.")
if "## [0.1.0]" not in (root / "CHANGELOG.md").read_text(encoding="utf-8"):
    raise SystemExit("CHANGELOG is missing v0.1.0.")
if not (root / "dist-release" / "SHA256SUMS.txt").is_file():
    raise SystemExit("Release artifacts have not been packaged.")
subprocess.run([sys.executable, "scripts/verify.py"], cwd=root, check=True)
markers = (
    "TO" + "DO",
    "FIX" + "ME",
    "Not" + "Implemented",
    "place" + "holder",
    "coming" + " soon",
    "lorem" + " ipsum",
)
for marker in markers:
    result = subprocess.run(
        ["git", "grep", "-n", marker, "--", ":!docs/ROADMAP.md"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0:
        raise SystemExit(f"Forbidden marker found: {marker}\n{result.stdout}")
author = subprocess.run(
    ["git", "log", "-1", "--format=%an <%ae> | %cn <%ce>"],
    cwd=root,
    capture_output=True,
    text=True,
    check=True,
).stdout.strip()
if "KanadeK" not in author:
    raise SystemExit(f"Unexpected commit identity: {author}")
print("Release checks passed.")
