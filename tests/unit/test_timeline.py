from datetime import UTC, datetime

from leakloom.domain.models import FindingInput, SourceKind
from leakloom.domain.timeline import build_report


def finding(
    secret: str, hour: int, location: str, source: SourceKind = SourceKind.COMMIT
) -> FindingInput:
    return FindingInput(
        secret=secret,
        occurred_at=datetime(2026, 1, 1, hour, tzinfo=UTC),
        location=location,
        source=source,
        detector="test",
    )


def test_builds_ordered_propagation_and_recurrence() -> None:
    secret = "LLM_FAKE_ALPHA_7a9K2mP4qR8x"
    report = build_report(
        [
            finding(secret, 3, "ci/log", SourceKind.CI_LOG),
            finding(secret, 1, "app/.env"),
            finding(secret, 2, "app/.env"),
        ]
    )
    timeline = report.timelines[0]
    assert timeline.root_cause_candidate == "app/.env"
    assert [edge.relationship for edge in timeline.propagation] == ["reappeared", "propagated"]
    assert timeline.recurrence_count == 1
    assert timeline.status == "active"


def test_marks_absent_current_fingerprint_resolved() -> None:
    secret = "LLM_FAKE_BRAVO_5c8N1tV6yW3z"
    report = build_report([finding(secret, 1, "a")], active_fingerprints=set())
    assert report.timelines[0].status == "resolved"
    assert secret not in report.model_dump_json()
