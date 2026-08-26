"""Capability graph over the frozen 0.2.1 attack stack. No new attacks."""

from __future__ import annotations

from research_engine.planner.orchestrator import DEFAULT_ATTACK_ORDER
from research_engine.strategy.types import AttackCapability, AttackChain, ResearchGoal

_G_CYCLE = (
    ResearchGoal.CYCLE_EXCLUSION,
    ResearchGoal.ORIGIN_AVOIDANCE,
    ResearchGoal.REACHABILITY,
)
_G_TERM = (ResearchGoal.TERMINATION, ResearchGoal.BOUNDEDNESS, ResearchGoal.POSITIVITY)
_G_INDUCTIVE = (
    ResearchGoal.TERMINATION,
    ResearchGoal.BOUNDEDNESS,
    ResearchGoal.POSITIVITY,
    ResearchGoal.REACHABILITY,
)


def _cap(
    name: str,
    *,
    inputs: tuple[str, ...] = (),
    outputs: tuple[str, ...] = (),
    preconditions: tuple[str, ...] = (),
    evidence_requirements: tuple[str, ...] = (),
    cost: float = 1.0,
    known_failure_modes: tuple[str, ...] = (),
    goals_served: tuple[ResearchGoal, ...] = (),
    recommended_next: tuple[str, ...] = (),
) -> AttackCapability:
    return AttackCapability(
        name=name,
        inputs=inputs,
        outputs=outputs,
        preconditions=preconditions,
        evidence_requirements=evidence_requirements,
        cost=cost,
        known_failure_modes=known_failure_modes,
        goals_served=goals_served,
        recommended_next=recommended_next,
    )


ATTACK_CAPABILITIES: dict[str, AttackCapability] = {
    item.name: item
    for item in (
        _cap(
            "reconnaissance",
            outputs=("finite_census", "horizon"),
            cost=0.5,
            goals_served=_G_TERM + (ResearchGoal.REACHABILITY,),
            recommended_next=("modular", "functional", "affine"),
            known_failure_modes=("GLOBAL_REASONING",),
        ),
        _cap(
            "piecewise_affine",
            outputs=("affine_family", "latent_control"),
            cost=1.0,
            goals_served=_G_CYCLE + (ResearchGoal.TERMINATION,),
            recommended_next=("parameter_domain", "closure"),
            known_failure_modes=("DOMAIN_INFERENCE", "REPRESENTATION"),
        ),
        _cap(
            "parameter_domain",
            inputs=("affine_family",),
            outputs=("exact_domain",),
            preconditions=("piecewise_affine",),
            evidence_requirements=("SUPPORTED_BY_SAMPLES",),
            cost=1.0,
            goals_served=_G_CYCLE,
            recommended_next=("control_word", "closure"),
            known_failure_modes=("DOMAIN_INFERENCE", "CERTIFICATION"),
        ),
        _cap(
            "control_word",
            inputs=("exact_domain",),
            outputs=("composed_constraint",),
            preconditions=("parameter_domain",),
            cost=1.0,
            goals_served=_G_CYCLE,
            recommended_next=("control_obstruction", "closure", "modular", "block"),
            known_failure_modes=("QUANTIFIER", "COMPOSITION"),
        ),
        _cap(
            "control_obstruction",
            inputs=("composed_constraint",),
            outputs=("class_obstruction",),
            preconditions=("control_word",),
            cost=1.0,
            goals_served=_G_CYCLE,
            recommended_next=("closure",),
            known_failure_modes=("OBSTRUCTION", "GLOBAL_REASONING"),
        ),
        _cap(
            "vector_affine",
            outputs=("vector_family",),
            cost=1.2,
            goals_served=_G_CYCLE,
            recommended_next=("matrix_word_invariant",),
            known_failure_modes=("REPRESENTATION",),
        ),
        _cap(
            "matrix_word_invariant",
            inputs=("vector_family",),
            outputs=("matrix_obstruction",),
            preconditions=("vector_affine",),
            cost=1.2,
            goals_served=_G_CYCLE,
            known_failure_modes=("OBSTRUCTION",),
        ),
        _cap(
            "closure",
            outputs=("exact_reachable",),
            cost=1.5,
            goals_served=(ResearchGoal.BOUNDEDNESS, ResearchGoal.REACHABILITY),
            recommended_next=("reconnaissance", "reverse", "affine"),
            known_failure_modes=("REACHABILITY", "COMPUTATIONAL", "GLOBAL_REASONING"),
        ),
        _cap(
            "modular",
            outputs=("modular_invariant",),
            cost=0.8,
            goals_served=_G_TERM,
            recommended_next=("functional", "block"),
        ),
        _cap(
            "functional",
            outputs=("observed_bound",),
            cost=0.8,
            goals_served=_G_TERM,
            recommended_next=("affine", "block"),
            known_failure_modes=("GLOBAL_REASONING",),
        ),
        _cap(
            "affine",
            inputs=("candidate_region",),
            outputs=("region_leak_test",),
            preconditions=("candidate_region",),
            cost=0.8,
            goals_served=(ResearchGoal.BOUNDEDNESS, ResearchGoal.POSITIVITY),
            recommended_next=("functional", "modular"),
        ),
        _cap("reverse", outputs=("preimage_geometry",), cost=1.0, recommended_next=("block", "functional")),
        _cap("block", outputs=("block_action",), cost=1.0, recommended_next=("reverse", "reconnaissance")),
        _cap("spectral", outputs=("companion_modes",), cost=1.0, recommended_next=("modular", "block")),
        _cap("factorization", outputs=("factor_pattern",), cost=1.0),
        _cap("separation", outputs=("separating_word",), cost=1.0),
        _cap("quotient", outputs=("behavioral_quotient",), cost=1.0),
        _cap("symmetry", outputs=("symmetry_orbit",), cost=0.8),
    )
}


CENSUS_OBSTRUCTION_CHAIN = AttackChain(
    id="census_obstruction",
    attacks=("piecewise_affine", "parameter_domain", "control_word", "control_obstruction"),
    goals=_G_CYCLE + (ResearchGoal.TERMINATION,),
    expected_outputs=("affine_family", "exact_domain", "composed_constraint", "class_obstruction"),
    historical_yield=3.0,
    cost=4.0,
)

VECTOR_MATRIX_CHAIN = AttackChain(
    id="vector_matrix",
    attacks=("vector_affine", "matrix_word_invariant"),
    goals=_G_CYCLE,
    expected_outputs=("vector_family", "matrix_obstruction"),
    historical_yield=2.0,
    cost=2.4,
)

FINITE_CLOSURE_CHAIN = AttackChain(
    id="finite_closure",
    attacks=("reconnaissance", "closure"),
    goals=(ResearchGoal.BOUNDEDNESS, ResearchGoal.REACHABILITY),
    expected_outputs=("finite_census", "exact_reachable"),
    historical_yield=1.0,
    cost=2.0,
)

MODULAR_FUNCTIONAL_CHAIN = AttackChain(
    id="modular_functional",
    attacks=("reconnaissance", "modular", "functional"),
    goals=_G_TERM,
    expected_outputs=("finite_census", "modular_invariant", "observed_bound"),
    historical_yield=0.8,
    cost=2.1,
)

GLOBAL_INDUCTIVE_CHAIN = AttackChain(
    id="global_inductive",
    attacks=(),
    goals=_G_INDUCTIVE,
    expected_outputs=("inductive_certificate", "ranking_certificate"),
    historical_yield=8.0,
    cost=1.0,
)

LAW_DOMAIN_CHAIN = AttackChain(
    id="law_domain",
    attacks=(),
    goals=(ResearchGoal.CYCLE_EXCLUSION, ResearchGoal.ORIGIN_AVOIDANCE),
    expected_outputs=("affine_law", "domain_attachment"),
    historical_yield=4.0,
    cost=1.0,
)

QUANTIFIER_PROBE_CHAIN = AttackChain(
    id="quantifier_probe",
    attacks=(),
    goals=(ResearchGoal.CYCLE_EXCLUSION, ResearchGoal.TERMINATION, ResearchGoal.BOUNDEDNESS),
    expected_outputs=("existential_witness", "universal_window"),
    historical_yield=4.0,
    cost=1.0,
)

SEEDED_CHAINS: tuple[AttackChain, ...] = (
    GLOBAL_INDUCTIVE_CHAIN,
    LAW_DOMAIN_CHAIN,
    QUANTIFIER_PROBE_CHAIN,
    CENSUS_OBSTRUCTION_CHAIN,
    VECTOR_MATRIX_CHAIN,
    FINITE_CLOSURE_CHAIN,
    MODULAR_FUNCTIONAL_CHAIN,
)


def capability(name: str) -> AttackCapability:
    return ATTACK_CAPABILITIES[name]


def recommended_edges() -> dict[str, tuple[str, ...]]:
    """Local ``recommended_next_attacks`` edges. Not a flood order."""

    return {name: item.recommended_next for name, item in ATTACK_CAPABILITIES.items()}


def freeze_attack_order() -> tuple[str, ...]:
    """The flood order stays the 0.2.1 sequence. Strategy does not mutate it."""

    return DEFAULT_ATTACK_ORDER
