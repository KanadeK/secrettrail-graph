from __future__ import annotations

from datetime import UTC, datetime

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from leakloom.domain.models import FindingInput
from leakloom.domain.timeline import build_report

app = FastAPI(title="SecretTrail Graph", version="0.1.0")


class AnalyzeRequest(BaseModel):
    findings: list[FindingInput]


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/analyze")
def analyze(request: AnalyzeRequest) -> dict[str, object]:
    if not request.findings:
        raise HTTPException(status_code=422, detail="At least one finding is required.")
    return build_report(request.findings, now=datetime.now(UTC)).model_dump(mode="json")


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return """<!doctype html><title>SecretTrail Graph</title><main>
    <h1>SecretTrail Graph</h1>
    <p>POST findings to <code>/api/analyze</code> to build a sanitized timeline.</p>
    <p>Use the CLI for a downloadable offline HTML report.</p></main>"""
