from __future__ import annotations

import json
from pathlib import Path

from jinja2 import Environment, PackageLoader, select_autoescape

from leakloom.domain.models import AnalysisReport


def write_json(report: AnalysisReport, path: Path) -> None:
    path.write_text(report.model_dump_json(indent=2), encoding="utf-8")


def write_html(report: AnalysisReport, path: Path) -> None:
    environment = Environment(
        loader=PackageLoader("leakloom"), autoescape=select_autoescape(["html"])
    )
    template = environment.get_template("report.html.j2")
    payload = report.model_dump(mode="json")
    path.write_text(
        template.render(report=payload, report_json=json.dumps(payload)), encoding="utf-8"
    )
