"""Evidence-based research decisions. No theorem is not an engine limitation."""

from __future__ import annotations

from research_engine.attacks.result import AttackStatus
from research_engine.core.semantics import SearchScope
from research_engine.diagnosis.types import (
    DeltaLevel,
    FamilyStatus,
    RegimeFingerprint,
    ResearchDecision,
    StructuralDelta,
)
from research_engine.planner.hypothesis import HypothesisStatus
from research_engine.planner.orchestrator import PlannerReport


def _has_exact_support(report: PlannerReport) -> bool:
    return any(
        item.status is AttackStatus.SUPPORTED and item.scope is SearchScope.EXACT
        for item in report.results
    )


def _has_refutation(report: PlannerReport) -> bool:
    if any(item.status is AttackStatus.REFUTED for item in report.results):
        return True
    return any(item.status is HypothesisStatus.REFUTED for item in report.hypotheses)


def decide_research(
    fingerprint: RegimeFingerprint,
    family_status: FamilyStatus,
    delta: StructuralDelta | None,
    report: PlannerReport,
) -> tuple[ResearchDecision, str]:
    recovered = fingerprint.piecewise_affine_structure in {"FINITE", "PARAMETERIZED"}
    hidden_branching = (
        fingerprint.control_structure == "SINGLETON"
        and fingerprint.numerical_contraction == "MIXED_MAGNITUDE"
        and fingerprint.eventual_region == "UNBOUNDED_SAMPLE"
        and fingerprint.modular_structure in {"INAPPLICABLE", "SAMPLED_RESTRICTION"}
        and fingerprint.block_structure == "INAPPLICABLE"
        and fingerprint.spectral_structure == "INAPPLICABLE"
        and not recovered
    )
    if hidden_branching:
        return (
            ResearchDecision.ENGINE_LIMITATION,
            "singleton control with mixed magnitude and truncated reachable "
            "sets: one-step growth and contraction are visible, but no generic "
            "control/affine language represents the hidden partition",
        )

    if family_status in {FamilyStatus.SATURATED, FamilyStatus.EXHAUSTED}:
        return (
            ResearchDecision.FAMILY_SATURATED,
            "core fingerprint matches a saturated family; further variants "
            "of this regime are low-value",
        )

    similar = delta is not None and delta.level is DeltaLevel.LOW

    if similar and family_status is FamilyStatus.SATURATING:
        return (
            ResearchDecision.CLOSE,
            "experiment reproduces a previously observed regime and exposes "
            "no new certified structure",
        )

    far = delta is None or delta.level is DeltaLevel.HIGH
    vector_language = fingerprint.affine_control_type in {
        "VECTOR",
        "MATRIX_PARAMETERIZED",
    }
    # Vector/matrix latent control is a new language even when core
    # contraction fields only differ at MEDIUM from a scalar family.
    novel_recovery = far or (
        vector_language and delta is not None and delta.level is not DeltaLevel.LOW
    )
    if recovered and novel_recovery:
        if fingerprint.piecewise_affine_structure == "PARAMETERIZED":
            if fingerprint.parameter_domain == "EXACT":
                if fingerprint.latent_control_algebra == "EXPLOITABLE":
                    if fingerprint.latent_control_obstruction in {
                        "RECURSIVE_INVARIANT",
                        "SYMBOLIC_CLASS",
                        "CLASS",
                        "PROVED",
                    }:
                        extra = {
                            "RECURSIVE_INVARIANT": "a recursive remainder invariant is proved",
                            "SYMBOLIC_CLASS": "a symbolic multi-step class obstruction is proved",
                        }.get(
                            fingerprint.latent_control_obstruction,
                            "a class-level obstruction is proved",
                        )
                        return (
                            ResearchDecision.CONTINUE,
                            "latent parameterized family recovered, domain "
                            f"certified, control-word algebra exploitable, and {extra}; "
                            "map globality on Z remains empirical",
                        )
                    return (
                        ResearchDecision.CONTINUE,
                        "latent parameterized family recovered, the arithmetic "
                        "domain is certified, and control-word algebra is "
                        "exploitable; map globality on Z remains empirical",
                    )
                return (
                    ResearchDecision.CONTINUE,
                    "latent parameterized family recovered and the arithmetic "
                    "domain of the relation is certified; map globality on Z "
                    "remains empirical",
                )
            return (
                ResearchDecision.CONTINUE,
                "family recovered, domain uncertified: window agreement of a "
                "parameterized family is not a global domain theorem",
            )
        return (
            ResearchDecision.CONTINUE,
            "finite piecewise-affine census on a structurally distant regime; "
            "window agreement is not a Z-theorem",
        )
    if far and fingerprint.eventual_region == "UNBOUNDED_SAMPLE":
        if _has_exact_support(report):
            return (
                ResearchDecision.CONTINUE,
                "structurally distant non-finite regime with at least one "
                "exact certificate",
            )
        return (
            ResearchDecision.ESCALATE,
            "structurally distant non-finite regime whose generic attacks "
            "do not yet yield an exact reusable identity",
        )

    if far and _has_exact_support(report):
        return (
            ResearchDecision.CONTINUE,
            "new structural regime with an exact certificate",
        )

    if _has_refutation(report) and fingerprint.eventual_region == "FINITE_SEED_CLOSURE":
        return (
            ResearchDecision.CLOSE,
            "finite per-seed closure with local refutations and no new "
            "reusable abstraction",
        )

    return (
        ResearchDecision.CLOSE,
        "no new structural regime relative to the certified evidence",
    )
