from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from leakloom.domain.models import FindingInput, SourceKind
from leakloom.domain.privacy import fingerprint


class InputFormatError(ValueError):
    """Raised when an imported scanner payload lacks a usable secret finding."""


def load_gitleaks(path: Path) -> list[FindingInput]:
    data = _read_json(path)
    rows = data.get("findings", data) if isinstance(data, dict) else data
    if not isinstance(rows, list):
        raise InputFormatError("Gitleaks JSON must contain a list of findings.")
    return [_finding(row, SourceKind.SCANNER, "gitleaks") for row in rows]


def load_trivy(path: Path) -> list[FindingInput]:
    data = _read_json(path)
    results = data.get("Results", []) if isinstance(data, dict) else []
    findings: list[FindingInput] = []
    for result in results:
        target = str(result.get("Target", "unknown-target"))
        for secret in result.get("Secrets", []):
            enriched = dict(secret)
            enriched.setdefault("Target", target)
            findings.append(_finding(enriched, SourceKind.SCANNER, "trivy"))
    return findings


def load_git_log(path: Path) -> list[FindingInput]:
    rows = _read_json(path)
    if not isinstance(rows, list):
        raise InputFormatError("Git log JSON must be a list.")
    return [_finding(row, SourceKind.COMMIT, "git") for row in rows]


def load_artifacts(path: Path) -> list[FindingInput]:
    rows = _read_json(path)
    if not isinstance(rows, list):
        raise InputFormatError("Artifact manifest must be a list.")
    return [_finding(row, SourceKind.ARTIFACT, "artifact-manifest") for row in rows]


def scan_workspace(path: Path) -> set[str]:
    """Read deterministic `LLM_FAKE_` samples from a current workspace only."""
    if not path.is_dir():
        raise FileNotFoundError(f"Workspace does not exist: {path}")
    tokens: set[str] = set()
    for item in path.rglob("*"):
        if item.is_file() and item.stat().st_size < 1_000_000:
            for word in item.read_text(encoding="utf-8", errors="ignore").split():
                candidate = word.strip("'\".,;:()[]{}")
                if candidate.startswith("LLM_FAKE_") and len(candidate) >= 16:
                    tokens.add(fingerprint(candidate))
    return tokens


def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise
    except json.JSONDecodeError as exc:
        raise InputFormatError(f"Invalid JSON in {path}: {exc.msg}") from exc


def _finding(row: dict[str, Any], source: SourceKind, detector: str) -> FindingInput:
    if not isinstance(row, dict):
        raise InputFormatError("Each finding must be an object.")
    secret = row.get("Secret") or row.get("Match") or row.get("secret") or row.get("token")
    if not isinstance(secret, str) or not secret:
        raise InputFormatError("Finding is missing a secret value.")
    timestamp = (
        row.get("Date") or row.get("occurred_at") or row.get("created_at") or "2026-01-01T00:00:00Z"
    )
    try:
        occurred_at = datetime.fromisoformat(str(timestamp).replace("Z", "+00:00"))
    except ValueError as exc:
        raise InputFormatError(f"Invalid finding timestamp: {timestamp}") from exc
    location = (
        row.get("File")
        or row.get("Target")
        or row.get("location")
        or row.get("name")
        or "unknown-location"
    )
    return FindingInput(
        secret=secret,
        occurred_at=occurred_at.replace(tzinfo=occurred_at.tzinfo or UTC),
        location=str(location),
        source=source,
        detector=detector,
        revision=row.get("Commit") or row.get("revision"),
    )
