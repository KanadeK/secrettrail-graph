from __future__ import annotations

from pathlib import Path

from leakloom.adapters.loaders import (
    load_artifacts,
    load_git_log,
    load_gitleaks,
    load_trivy,
    scan_workspace,
)
from leakloom.domain.models import AnalysisReport, FindingInput
from leakloom.domain.timeline import build_report


def analyze_files(
    gitleaks: Path | None = None,
    trivy: Path | None = None,
    git_log: Path | None = None,
    artifacts: Path | None = None,
    workspace: Path | None = None,
) -> AnalysisReport:
    findings: list[FindingInput] = []
    if gitleaks:
        findings.extend(load_gitleaks(gitleaks))
    if trivy:
        findings.extend(load_trivy(trivy))
    if git_log:
        findings.extend(load_git_log(git_log))
    if artifacts:
        findings.extend(load_artifacts(artifacts))
    if not findings:
        raise ValueError("Provide at least one input file.")
    active = scan_workspace(workspace) if workspace else None
    return build_report(findings, active_fingerprints=active)
