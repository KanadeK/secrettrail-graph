from __future__ import annotations

import hashlib


def fingerprint(secret: str) -> str:
    """Return a stable, irreversible identifier for correlation."""
    return "sha256:" + hashlib.sha256(secret.encode("utf-8")).hexdigest()[:20]


def mask(secret: str) -> str:
    """Preserve only enough context for operators to distinguish findings."""
    if len(secret) <= 6:
        return "*" * len(secret)
    return f"{secret[:3]}{'*' * max(4, len(secret) - 6)}{secret[-3:]}"
