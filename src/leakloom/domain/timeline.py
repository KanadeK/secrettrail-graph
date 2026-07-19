from __future__ import annotations

from collections import defaultdict
from datetime import UTC, datetime

import networkx as nx

from leakloom.domain.models import (
    AnalysisReport,
    FindingInput,
    Occurrence,
    PropagationEdge,
    SecretTimeline,
)
from leakloom.domain.privacy import fingerprint, mask


def build_report(
    findings: list[FindingInput],
    active_fingerprints: set[str] | None = None,
    now: datetime | None = None,
) -> AnalysisReport:
    """Group raw findings into sanitized propagation timelines."""
    grouped: dict[str, list[FindingInput]] = defaultdict(list)
    masked: dict[str, str] = {}
    for finding in findings:
        key = fingerprint(finding.secret)
        grouped[key].append(finding)
        masked[key] = mask(finding.secret)
    timelines = [
        _timeline(key, items, masked[key], active_fingerprints)
        for key, items in sorted(grouped.items())
    ]
    return AnalysisReport(
        generated_at=(now or datetime.now(UTC)).astimezone(UTC),
        timelines=timelines,
        source_count=len(findings),
    )


def _timeline(
    key: str, findings: list[FindingInput], masked_secret: str, active_fingerprints: set[str] | None
) -> SecretTimeline:
    ordered = sorted(findings, key=lambda item: item.normalized_time())
    occurrences = [
        Occurrence(
            fingerprint=key,
            masked_secret=masked_secret,
            occurred_at=item.normalized_time(),
            location=item.location,
            source=item.source,
            detector=item.detector,
            revision=item.revision,
        )
        for item in ordered
    ]
    graph: nx.DiGraph[int] = nx.DiGraph()
    edges: list[PropagationEdge] = []
    recurrence_count = 0
    seen_locations: set[str] = set()
    for index, occurrence in enumerate(occurrences):
        graph.add_node(index, location=occurrence.location)
        if index == 0:
            seen_locations.add(occurrence.location)
            continue
        prior = occurrences[index - 1]
        relationship = "propagated"
        if occurrence.location in seen_locations:
            relationship = "reappeared"
            recurrence_count += 1
        graph.add_edge(index - 1, index, relationship=relationship)
        edges.append(
            PropagationEdge(
                from_location=prior.location,
                to_location=occurrence.location,
                occurred_at=occurrence.occurred_at,
                relationship=relationship,
            )
        )
        seen_locations.add(occurrence.location)
    locations = list(dict.fromkeys(item.location for item in occurrences))
    status = "active" if active_fingerprints is None or key in active_fingerprints else "resolved"
    checklist = [
        f"Rotate the credential identified by {key}.",
        f"Remove it from {occurrences[0].location} and rewrite affected history if required.",
        "Invalidate CI logs and artifacts that contain the masked credential.",
        "Verify a clean scan and document the remediation owner.",
    ]
    return SecretTimeline(
        fingerprint=key,
        masked_secret=masked_secret,
        status=status,
        first_seen=occurrences[0].occurred_at,
        last_seen=occurrences[-1].occurred_at,
        root_cause_candidate=occurrences[0].location,
        affected_locations=locations,
        recurrence_count=recurrence_count,
        checklist=checklist,
        occurrences=occurrences,
        propagation=edges,
    )
