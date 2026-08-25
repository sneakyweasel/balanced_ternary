"""Family status from accumulated fingerprints. No target-name special cases."""

from __future__ import annotations

from collections.abc import Sequence

from research_engine.diagnosis.compare import core_match
from research_engine.diagnosis.types import (
    ExperimentRecord,
    FamilyStatus,
    RegimeFingerprint,
    ResearchDecision,
)

SATURATED_MIN = 3


def family_id_of(fingerprint: RegimeFingerprint) -> str:
    key = fingerprint.core_key()
    if key is None:
        return "unclassified"
    return "|".join(key)


def records_in_family(
    records: Sequence[ExperimentRecord],
    fingerprint: RegimeFingerprint,
) -> tuple[ExperimentRecord, ...]:
    return tuple(item for item in records if core_match(item.fingerprint, fingerprint))


def family_status_for(
    fingerprint: RegimeFingerprint,
    records: Sequence[ExperimentRecord],
) -> FamilyStatus:
    members = records_in_family(records, fingerprint)
    if not members:
        return FamilyStatus.ACTIVE
    cores = {item.fingerprint.core_key() for item in members}
    if None in cores or len(cores) > 1:
        return FamilyStatus.CONTRADICTORY
    distinct = {item.target for item in members}
    closed_targets = {
        item.target
        for item in members
        if item.decision in {ResearchDecision.CLOSE, ResearchDecision.FAMILY_SATURATED}
    }
    if len(distinct) >= SATURATED_MIN and len(closed_targets) >= SATURATED_MIN:
        if any(item.decision is ResearchDecision.FAMILY_SATURATED for item in members):
            return FamilyStatus.EXHAUSTED
        return FamilyStatus.SATURATED
    if len(distinct) >= 2:
        return FamilyStatus.SATURATING
    return FamilyStatus.ACTIVE
