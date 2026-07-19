from __future__ import annotations

import hashlib
import shutil
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
release = root / "dist-release"
release.mkdir(exist_ok=True)
subprocess.run([sys.executable, "-m", "build"], cwd=root, check=True)
for artifact in (root / "dist").iterdir():
    shutil.copy2(artifact, release / f"secrettrail-graph-0.1.0-{artifact.name}")
subprocess.run(
    [
        sys.executable,
        "-m",
        "leakloom.cli",
        "analyze",
        "--gitleaks",
        "examples/gitleaks.json",
        "--trivy",
        "examples/trivy.json",
        "--git-log",
        "examples/git-log.json",
        "--artifacts",
        "examples/artifacts.json",
        "--workspace",
        "examples/current",
        "--html",
        "dist-release/demo-report.html",
        "--json",
        "dist-release/demo-report.json",
    ],
    cwd=root,
    check=True,
)
lines = [
    f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}"
    for path in sorted(release.iterdir())
    if path.name != "SHA256SUMS.txt"
]
(release / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
