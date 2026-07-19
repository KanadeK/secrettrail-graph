from pathlib import Path

from leakloom.adapters.loaders import InputFormatError, load_gitleaks
from leakloom.adapters.report import write_html, write_json
from leakloom.services.analyze import analyze_files

ROOT = Path(__file__).resolve().parents[2]


def test_all_sample_sources_form_four_timelines_and_sanitize_output(tmp_path: Path) -> None:
    report = analyze_files(
        ROOT / "examples/gitleaks.json",
        ROOT / "examples/trivy.json",
        ROOT / "examples/git-log.json",
        ROOT / "examples/artifacts.json",
        ROOT / "examples/current",
    )
    html, payload = tmp_path / "report.html", tmp_path / "report.json"
    write_html(report, html)
    write_json(report, payload)
    combined = html.read_text(encoding="utf-8") + payload.read_text(encoding="utf-8")
    assert len(report.timelines) == 4
    assert sum(item.recurrence_count for item in report.timelines) == 2
    assert "LLM_FAKE_" not in combined
    assert all(item.status == "active" for item in report.timelines)


def test_loader_rejects_invalid_json(tmp_path: Path) -> None:
    invalid = tmp_path / "broken.json"
    invalid.write_text("{", encoding="utf-8")
    try:
        load_gitleaks(invalid)
    except InputFormatError as exc:
        assert "Invalid JSON" in str(exc)
    else:
        raise AssertionError("Expected InputFormatError")
