"""Conservative CLOSE/math-status inference. Never mutates source records."""

from __future__ import annotations

from research_engine.control.close import refuse_resolved_from_finite
from research_engine.control.types import (
    CloseTag,
    ExecutionStatus,
    FieldProvenance,
    MathematicalStatus,
    V2_3_CAMPAIGN_ORDER,
)
from research_engine.memory.types import MemoryExperiment

# Explicit table for the nine frozen v2.3 campaigns. Provenance is INFERRED:
# the historical reports do not carry these fields.
V2_3_INFERENCE: dict[str, tuple[CloseTag, MathematicalStatus, str]] = {
    "mx_plus_r_7x1_class_obstruction": (
        CloseTag.CLOSE_FALSE_OBSTRUCTION,
        MathematicalStatus.STRONG_NEGATIVE,
        "T(73)=1 and T(299593)=1 kill the class-as-basin obstruction",
    ),
    "weak_collatz_floor_5x4_rplus": (
        CloseTag.CLOSE_REPARAMETERIZATION,
        MathematicalStatus.UNRESOLVED,
        "FINITE_CENSUS reparameterization of the 4/3 SLC language; do not upgrade the successor lemma",
    ),
    "matthews_prize_mod3_avoider": (
        CloseTag.CLOSE_FALSE_OBSTRUCTION,
        MathematicalStatus.STRONG_NEGATIVE,
        "packet seeds are not avoiders; {1,2} mod 3 is not a basin",
    ),
    "companion_shift_order6_zero_class": (
        CloseTag.CLOSE_SKIP_BOUNDARY,
        MathematicalStatus.FRONTIER,
        "matrix-word / 25^6 census skipped; vanishing on Z remains open",
    ),
    "skolem_order5_unconditional": (
        CloseTag.CLOSE_SKIP_BOUNDARY,
        MathematicalStatus.FRONTIER,
        "same skip pair as dimension 6; unconditional order-5 vanishing remains open",
    ),
    "juggler_sequence": (
        CloseTag.CLOSE_FINITE_CENSUS,
        MathematicalStatus.FRONTIER,
        "seed-13 orbit is not a map theorem on positive integers",
    ),
    "reverse_and_add_base3": (
        CloseTag.CLOSE_FINITE_CENSUS,
        MathematicalStatus.FRONTIER,
        "seed-196 orbit is not totality of reverse-fixed arrival",
    ),
    "home_prime_49": (
        CloseTag.CLOSE_FINITE_CENSUS,
        MathematicalStatus.FRONTIER,
        "budget-truncated prefix of seed 49 is not primality of the orbit",
    ),
    "cyclic_tag_bit": (
        CloseTag.CLOSE_SPEC_MISMATCH,
        MathematicalStatus.UNRESOLVED,
        "predicted word/integer mismatch; do not upgrade rewrite identities to RESOLVED",
    ),
}


def lookup_v2_3(experiment_id: str) -> tuple[CloseTag, MathematicalStatus, str] | None:
    return V2_3_INFERENCE.get(experiment_id)


def infer_classification(
    experiment: MemoryExperiment,
) -> tuple[CloseTag, MathematicalStatus, FieldProvenance, str]:
    """Derive a conservative close tag. Never returns RESOLVED."""

    keyed = lookup_v2_3(experiment.experiment_id)
    if keyed is not None:
        tag, status, reason = keyed
        return tag, status, FieldProvenance.INFERRED, reason

    yield_report = experiment.mathematical_yield
    artifact = experiment.run_artifact
    reason_code = experiment.decision_reason_code.value
    skipped = tuple(artifact.skipped) if artifact is not None else ()
    statuses = dict(artifact.attack_statuses) if artifact is not None else {}
    unresolved = tuple(yield_report.unresolved_questions)
    counterexamples = tuple(yield_report.new_counterexamples)
    census = (artifact.census_kind if artifact is not None else "") or ""
    evidence_blob = " ".join(
        [
            reason_code,
            census,
            experiment.diagnosis.decision_reason,
            " ".join(unresolved),
            " ".join(skipped),
            " ".join(statuses.values()),
        ]
    )
    finite_blocked = refuse_resolved_from_finite(evidence_blob)
    assert finite_blocked is not MathematicalStatus.RESOLVED

    skip_budget = any(
        name in skipped or statuses.get(name) == "COMPUTATION_EXHAUSTED"
        for name in ("vector_affine", "matrix_word_invariant")
    ) or experiment.decision_reason_code.value == "COMPUTATIONAL_BUDGET"
    if skip_budget and unresolved:
        return (
            CloseTag.CLOSE_SKIP_BOUNDARY,
            MathematicalStatus.FRONTIER,
            FieldProvenance.INFERRED,
            "skipped or budget-exhausted attack with an open question",
        )
    if counterexamples and (
        "obstruction" in evidence_blob.lower()
        or "avoider" in evidence_blob.lower()
        or "basin" in evidence_blob.lower()
        or yield_report.new_obstructions
    ):
        return (
            CloseTag.CLOSE_FALSE_OBSTRUCTION,
            MathematicalStatus.STRONG_NEGATIVE,
            FieldProvenance.INFERRED,
            "counterexamples kill the investigated obstruction",
        )
    if experiment.novelty_status.value == "KNOWN_REDISCOVERY" and "REPARAMETERIZATION" in (
        experiment.diagnosis.prior_art_status.upper(),
        reason_code,
    ):
        return (
            CloseTag.CLOSE_REPARAMETERIZATION,
            MathematicalStatus.UNRESOLVED,
            FieldProvenance.INFERRED,
            "reparameterization of a known representation",
        )
    mismatch = any(
        item.failure_class.value == "REPRESENTATION" for item in experiment.failures
    ) or reason_code == "REPRESENTATION_MISMATCH"
    if mismatch:
        return (
            CloseTag.CLOSE_SPEC_MISMATCH,
            MathematicalStatus.UNRESOLVED,
            FieldProvenance.INFERRED,
            "representation or spec mismatch",
        )
    if census in {"FINITE_CENSUS", "FINITE_SEED_CLOSURE"} or "FINITE" in census:
        status = MathematicalStatus.FRONTIER if unresolved else MathematicalStatus.UNRESOLVED
        return (
            CloseTag.CLOSE_FINITE_CENSUS,
            status,
            FieldProvenance.INFERRED,
            "evidence bounded by a finite census, prefix, or seed closure",
        )
    prior = (experiment.diagnosis.prior_art_status or "").upper()
    if prior in {"KNOWN", "REPARAMETERIZATION"} or reason_code == "KNOWN_REDISCOVERY":
        if prior == "REPARAMETERIZATION":
            return (
                CloseTag.CLOSE_REPARAMETERIZATION,
                MathematicalStatus.UNRESOLVED,
                FieldProvenance.INFERRED,
                "prior-art reparameterization",
            )
        return (
            CloseTag.CLOSE_KNOWN,
            MathematicalStatus.UNRESOLVED,
            FieldProvenance.INFERRED,
            "surviving statements tagged known / rediscovery",
        )
    return (
        CloseTag.CLOSE_NO_PROMOTION,
        MathematicalStatus.UNRESOLVED,
        FieldProvenance.INFERRED,
        "no more specific close tag is supported by the record",
    )


def default_execution_status(experiment: MemoryExperiment) -> ExecutionStatus:
    """Laboratory CLOSE for the nine v2.3 campaigns; otherwise conservative CLOSE."""

    if experiment.experiment_id in V2_3_CAMPAIGN_ORDER:
        return ExecutionStatus.CLOSE
    return ExecutionStatus.CLOSE
