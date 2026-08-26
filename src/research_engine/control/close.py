"""CLOSE taxonomy validation. Execution status never implies mathematical status."""

from __future__ import annotations

from research_engine.control.types import (
    CampaignControlRecord,
    CloseTag,
    ControlSchemaError,
    ExecutionStatus,
    MathematicalStatus,
)

FINITE_EVIDENCE_MARKERS: tuple[str, ...] = (
    "FINITE_CENSUS",
    "FINITE_SEED",
    "prefix",
    "horizon",
    "budget",
    "COMPUTATION_EXHAUSTED",
    "truncated",
)


def parse_close_tag(value: str) -> CloseTag:
    try:
        return CloseTag(value)
    except ValueError as exc:
        raise ControlSchemaError(f"invalid close tag {value!r}") from exc


def parse_mathematical_status(value: str) -> MathematicalStatus:
    try:
        return MathematicalStatus(value)
    except ValueError as exc:
        raise ControlSchemaError(f"invalid mathematical status {value!r}") from exc


def validate_pair(
    execution_status: ExecutionStatus,
    mathematical_status: MathematicalStatus,
    close_tag: CloseTag | None,
) -> None:
    """Independence rules. CLOSE does not imply RESOLVED."""

    if execution_status is ExecutionStatus.CLOSE and close_tag is None:
        raise ControlSchemaError("CLOSE execution requires exactly one primary close tag")
    if execution_status is not ExecutionStatus.CLOSE and close_tag is not None:
        raise ControlSchemaError("close_tag is allowed only when execution_status is CLOSE")
    if close_tag is not None and close_tag not in CloseTag:
        raise ControlSchemaError(f"invalid close tag {close_tag!r}")
    if (
        execution_status is ExecutionStatus.CLOSE
        and mathematical_status is MathematicalStatus.RESOLVED
        and close_tag
        in {
            CloseTag.CLOSE_FINITE_CENSUS,
            CloseTag.CLOSE_SKIP_BOUNDARY,
            CloseTag.CLOSE_NO_PROMOTION,
        }
    ):
        raise ControlSchemaError(
            f"{close_tag.value} must not be paired with RESOLVED; finite or skipped evidence is not a theorem"
        )


def validate_record(record: CampaignControlRecord) -> CampaignControlRecord:
    validate_pair(record.execution_status, record.mathematical_status, record.close_tag)
    if record.execution_status is ExecutionStatus.CLOSE:
        tags = [record.close_tag]
        if len([item for item in tags if item is not None]) != 1:
            raise ControlSchemaError("exactly one primary close tag is required")
    proposals = record.proposals.proposals
    if len(proposals) != 3:
        raise ControlSchemaError(f"expected exactly 3 proposals, got {len(proposals)}")
    ranks = [item.rank for item in proposals]
    if sorted(ranks) != [1, 2, 3]:
        raise ControlSchemaError(f"proposal ranks must be unique {{1,2,3}}, got {ranks}")
    return record


def refuse_resolved_from_finite(evidence_text: str) -> MathematicalStatus:
    """Finite/prefix/budget language never upgrades to RESOLVED."""

    lowered = evidence_text.lower()
    if any(marker.lower() in lowered for marker in FINITE_EVIDENCE_MARKERS):
        return MathematicalStatus.UNRESOLVED
    return MathematicalStatus.UNRESOLVED
