from pathlib import Path

from fastapi.testclient import TestClient

from leakloom.api import app
from leakloom.cli import main

ROOT = Path(__file__).resolve().parents[2]


def test_cli_generates_offline_report(tmp_path: Path) -> None:
    html, payload = tmp_path / "output.html", tmp_path / "output.json"
    exit_code = main(
        [
            "analyze",
            "--gitleaks",
            str(ROOT / "examples/gitleaks.json"),
            "--trivy",
            str(ROOT / "examples/trivy.json"),
            "--git-log",
            str(ROOT / "examples/git-log.json"),
            "--artifacts",
            str(ROOT / "examples/artifacts.json"),
            "--workspace",
            str(ROOT / "examples/current"),
            "--html",
            str(html),
            "--json",
            str(payload),
        ]
    )
    assert exit_code == 0
    assert html.is_file() and payload.is_file()
    assert "LLM_FAKE_" not in html.read_text(encoding="utf-8")


def test_api_rejects_empty_and_returns_sanitized_result() -> None:
    client = TestClient(app)
    assert client.post("/api/analyze", json={"findings": []}).status_code == 422
    response = client.post(
        "/api/analyze",
        json={
            "findings": [
                {
                    "secret": "LLM_FAKE_ALPHA_7a9K2mP4qR8x",
                    "occurred_at": "2026-01-01T00:00:00Z",
                    "location": "app/.env",
                    "source": "commit",
                    "detector": "test",
                }
            ]
        },
    )
    assert response.status_code == 200
    assert "LLM_FAKE_" not in response.text


def test_health_and_index_are_usable() -> None:
    client = TestClient(app)
    assert client.get("/health").json() == {"status": "ok"}
    assert client.get("/").status_code == 200
