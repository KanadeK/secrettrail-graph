from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class SourceKind(StrEnum):
    COMMIT = "commit"
    CI_LOG = "ci_log"
    ARTIFACT = "artifact"
    SCANNER = "scanner"


class FindingInput(BaseModel):
    """Raw secret is accepted only at the trust boundary and never serialized."""

    secret: str = Field(min_length=4, repr=False, exclude=True)
    occurred_at: datetime
    location: str = Field(min_length=1)
    source: SourceKind
    detector: str
    revision: str | None = None

    def normalized_time(self) -> datetime:
        return self.occurred_at.replace(tzinfo=self.occurred_at.tzinfo or UTC)


class Occurrence(BaseModel):
    fingerprint: str
    masked_secret: str
    occurred_at: datetime
    location: str
    source: SourceKind
    detector: str
    revision: str | None = None


class PropagationEdge(BaseModel):
    from_location: str
    to_location: str
    occurred_at: datetime
    relationship: str


class SecretTimeline(BaseModel):
    fingerprint: str
    masked_secret: str
    status: str
    first_seen: datetime
    last_seen: datetime
    root_cause_candidate: str
    affected_locations: list[str]
    recurrence_count: int
    checklist: list[str]
    occurrences: list[Occurrence]
    propagation: list[PropagationEdge]


class AnalysisReport(BaseModel):
    generated_at: datetime
    timelines: list[SecretTimeline]
    source_count: int
