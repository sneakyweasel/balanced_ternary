"""In-memory research corpus. Session memory for selecting later experiments."""

from __future__ import annotations

from research_engine.diagnosis.compare import compare_fingerprints
from research_engine.diagnosis.types import ExperimentRecord, RegimeFingerprint, StructuralDelta


class ResearchCorpus:
    """Completed experiment records. Not the named theorem ledger."""

    def __init__(self, records: tuple[ExperimentRecord, ...] = ()) -> None:
        self._records: list[ExperimentRecord] = list(records)

    def add(self, record: ExperimentRecord) -> None:
        self._records.append(record)

    @property
    def records(self) -> tuple[ExperimentRecord, ...]:
        return tuple(self._records)

    def nearest(
        self,
        fingerprint: RegimeFingerprint,
        *,
        exclude: str = "",
    ) -> tuple[ExperimentRecord | None, StructuralDelta | None]:
        best: ExperimentRecord | None = None
        best_delta: StructuralDelta | None = None
        best_score = -1.0
        for record in self._records:
            if exclude and record.target == exclude:
                continue
            _similarity, delta = compare_fingerprints(fingerprint, record.fingerprint)
            if delta.similarity.score > best_score:
                best_score = delta.similarity.score
                best = record
                best_delta = delta
        return best, best_delta
