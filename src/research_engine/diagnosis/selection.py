"""Transparent next-experiment scoring. Not an autonomous mathematician."""

from __future__ import annotations

from research_engine.diagnosis.family import family_status_for
from research_engine.diagnosis.types import (
    CAPABILITIES,
    CandidateSketch,
    CoverageStatus,
    FamilyStatus,
    SelectionReport,
)
from research_engine.diagnosis.corpus import ResearchCorpus


def _corpus_untested(corpus: ResearchCorpus) -> set[str]:
    exercised: set[str] = set()
    for record in corpus.records:
        for name in CAPABILITIES:
            if record.coverage.status(name) == CoverageStatus.EXERCISED.value:
                exercised.add(name)
    return set(CAPABILITIES) - exercised if corpus.records else set(CAPABILITIES)


def score_candidate(
    sketch: CandidateSketch,
    corpus: ResearchCorpus,
    memory: object | None = None,
) -> SelectionReport:
    nearest, delta = (
        corpus.nearest(sketch.fingerprint)
        if sketch.fingerprint is not None
        else (None, None)
    )
    if sketch.fingerprint is None or delta is None:
        distance = 1.0
        family = FamilyStatus.ACTIVE
    else:
        distance = 1.0 - delta.similarity.score
        family = family_status_for(sketch.fingerprint, corpus.records)
        if family in {FamilyStatus.SATURATED, FamilyStatus.EXHAUSTED} and distance < 0.25:
            distance = 0.05

    claimed = set(sketch.claimed_capabilities) if sketch.claimed_capabilities else set(CAPABILITIES)
    gap_pool = _corpus_untested(corpus)
    gap = (len(claimed & gap_pool) / len(claimed)) if claimed else 0.0

    novelty = 0.25 if sketch.prior_art_classified else 1.0
    if not sketch.exact_semantics:
        novelty *= 0.25
    if not sketch.finite_horizon_tractable:
        novelty *= 0.5
    if not sketch.lean_certifiable:
        novelty *= 0.7

    cost = sketch.experimental_cost if sketch.experimental_cost > 0 else 1.0
    failure_learning = 1.0
    flv_note = ""
    if memory is not None:
        from research_engine.memory.learning import failure_learning_value

        failure_learning, flv_note = failure_learning_value(sketch, memory)
    value = (distance * gap * novelty * failure_learning) / cost
    bits = [
        f"distance={distance:.2f}",
        f"capability_gap={gap:.2f}",
        f"novelty={novelty:.2f}",
        f"cost={cost:.2f}",
    ]
    if nearest is not None and delta is not None:
        bits.append(
            f"nearest={nearest.target} delta={delta.level.value} family={family.value}"
        )
    if family in {FamilyStatus.SATURATED, FamilyStatus.EXHAUSTED} and distance <= 0.05:
        bits.append("discouraged: saturated family with matching core fingerprint")
    if memory is not None:
        bits.append(f"failure_learning={failure_learning:.2f}")
        if flv_note:
            bits.append(flv_note)
    explanation = (
        f"{sketch.name}: ExpectedResearchValue={value:.3f} (" + ", ".join(bits) + ")"
    )
    return SelectionReport(
        name=sketch.name,
        value=value,
        structural_distance=distance,
        capability_gap=gap,
        novelty_potential=novelty,
        experimental_cost=cost,
        explanation=explanation,
        failure_learning_value=failure_learning,
    )
