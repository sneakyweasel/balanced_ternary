"""Evidence-driven v2.3 retrospective. Not a concatenation of campaign reports."""

from __future__ import annotations

from collections import Counter

from research_engine.control.types import (
    CampaignControlRecord,
    CloseTag,
    RetrospectiveReport,
    V2_3_CAMPAIGN_ORDER,
)
from research_engine.memory.types import MemoryExperiment

_FAILURE_FROM_TAG: dict[CloseTag, str] = {
    CloseTag.CLOSE_FALSE_OBSTRUCTION: (
        "image class or local invariant mistaken for a basin / avoider obstruction"
    ),
    CloseTag.CLOSE_REPARAMETERIZATION: "representation mistaken for mathematical yield",
    CloseTag.CLOSE_FINITE_CENSUS: "finite census, prefix, or seed orbit mistaken for a global theorem",
    CloseTag.CLOSE_SKIP_BOUNDARY: (
        "nonlinear or high-dimensional mapping reached an unimplemented global-inductive / matrix-word boundary"
    ),
    CloseTag.CLOSE_SPEC_MISMATCH: "integer encoding mistaken for the native word or rewrite specification",
    CloseTag.CLOSE_KNOWN: "known rediscovery billed as a new theorem",
    CloseTag.CLOSE_NO_PROMOTION: "continuing information with no promotion candidate",
}


def _successful_capabilities(
    experiments: tuple[MemoryExperiment, ...],
    records: tuple[CampaignControlRecord, ...],
) -> tuple[str, ...]:
    found: list[str] = []
    if experiments:
        found.append("problem normalization to ProblemSpec / BlindPacket")
    if any(item.diagnosis.fingerprint.populated() for item in experiments):
        found.append("mathematical fingerprinting (RegimeFingerprint)")
    if any(
        (item.run_artifact and item.run_artifact.census_kind)
        or item.diagnosis.fingerprint.piecewise_affine_structure not in {"UNOBSERVED", ""}
        for item in experiments
    ):
        found.append("finite exact exploration (census / residual prefix)")
    if any(item.mathematical_yield.new_counterexamples or item.diagnosis.strongest_falsification for item in experiments):
        found.append("candidate falsification by exact counterexample")
    if any(item.diagnosis.lean_certificate for item in experiments):
        found.append("Lean certification of identities (no sorry)")
    if any(item.scout is not None and item.blind_packet is not None for item in experiments):
        found.append("scout / blind isolation")
    if records:
        found.append("post-attack close taxonomy and Top-3 proposal preservation")
    return tuple(found)


def _failure_modes(records: tuple[CampaignControlRecord, ...]) -> tuple[str, ...]:
    seen: list[str] = []
    for record in records:
        if record.close_tag is None:
            continue
        mode = _FAILURE_FROM_TAG.get(record.close_tag)
        if mode and mode not in seen:
            seen.append(mode)
    return tuple(seen)


def _missing_capabilities(records: tuple[CampaignControlRecord, ...]) -> tuple[tuple[str, int], ...]:
    counts: Counter[str] = Counter()
    for record in records:
        for proposal in record.proposals.proposals:
            capability = proposal.required_capability.strip()
            if capability:
                counts[capability] += 1
    return tuple(counts.most_common())


def build_retrospective(
    experiments: tuple[MemoryExperiment, ...],
    records: tuple[CampaignControlRecord, ...],
) -> RetrospectiveReport:
    by_id = {item.experiment_id: item for item in experiments}
    ordered_experiments = tuple(
        by_id[name] for name in V2_3_CAMPAIGN_ORDER if name in by_id
    )
    ordered_records = tuple(
        item for name in V2_3_CAMPAIGN_ORDER for item in records if item.campaign_id == name
    )
    return RetrospectiveReport(
        successful_capabilities=_successful_capabilities(ordered_experiments, ordered_records),
        recurring_failure_modes=_failure_modes(ordered_records),
        recurring_missing_capabilities=_missing_capabilities(ordered_records),
        campaign_ids=tuple(item.campaign_id for item in ordered_records),
        notes=(
            "Missing capabilities are the union of Top-3 required_capability fields; they are not a new attack list.",
            "Do not implement ranking, basin, or symbolic composition in this milestone.",
        ),
    )
