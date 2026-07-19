from __future__ import annotations

import argparse
from pathlib import Path

from leakloom.adapters.report import write_html, write_json
from leakloom.services.analyze import analyze_files


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="secrettrail", description="Create a sanitized secret propagation report."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    analyze = subparsers.add_parser(
        "analyze", help="Analyze JSON inputs and write an offline report."
    )
    for option in ("gitleaks", "trivy", "git-log", "artifacts", "workspace"):
        analyze.add_argument(f"--{option}", type=Path)
    analyze.add_argument("--html", type=Path, default=Path("report.html"))
    analyze.add_argument("--json", type=Path, default=Path("report.json"))
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "analyze":
        report = analyze_files(
            args.gitleaks, args.trivy, args.git_log, args.artifacts, args.workspace
        )
        write_html(report, args.html)
        write_json(report, args.json)
        print(f"Wrote {len(report.timelines)} sanitized timelines to {args.html} and {args.json}.")
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
