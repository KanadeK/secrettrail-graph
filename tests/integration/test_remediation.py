import shutil
from pathlib import Path

from leakloom.services.analyze import analyze_files

ROOT = Path(__file__).resolve().parents[2]


def test_removing_current_source_marks_timeline_resolved(tmp_path: Path) -> None:
    workspace = tmp_path / "current"
    shutil.copytree(ROOT / "examples/current", workspace)
    (workspace / "active.txt").write_text("", encoding="utf-8")
    report = analyze_files(ROOT / "examples/gitleaks.json", workspace=workspace)
    assert {item.status for item in report.timelines} == {"resolved"}
