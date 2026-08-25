"""ResearchLoop candidate pool after the companion-observation portfolio."""

from __future__ import annotations

from typing import cast

from research.engine_campaign.candidates import IntegerPolynomialSpec
from research.linear_constraint_loops.spec import increment_spec
from research.mx_plus_r.spec import mx_plus_r_spec
from research_engine.benchmarks.hidden_piecewise import HiddenCongruenceASpec
from research_engine.benchmarks.hidden_vector_affine import HiddenParityShearSpec
from research_engine.core.problem_spec import ProblemSpec
from research_engine.diagnosis.corpus import ResearchCorpus
from research_engine.diagnosis.loop import diagnose
from research_engine.diagnosis.selection import score_candidate
from research_engine.diagnosis.types import CandidateSketch, SelectionReport
from research_engine.memory.store import ResearchMemory
from research_engine.planner.orchestrator import AttackPlanner


def _fingerprint_of(spec: ProblemSpec, corpus: ResearchCorpus):
    report = AttackPlanner().run(spec, spec.attack_context())
    return diagnose(spec, report, spec.attack_context(), corpus).fingerprint


def candidate_sketches(corpus: ResearchCorpus) -> tuple[CandidateSketch, ...]:
    increment = increment_spec()
    seven = mx_plus_r_spec(7, 1)
    seven_fp = None
    for record in corpus.records:
        if record.target == seven.name:
            seven_fp = record.fingerprint
            break
    if seven_fp is None:
        seven_fp = _fingerprint_of(cast(ProblemSpec, seven), corpus)
    return (
        CandidateSketch(
            name=increment.name,
            fingerprint=_fingerprint_of(cast(ProblemSpec, increment), corpus),
            exact_semantics=True,
            finite_horizon_tractable=True,
            lean_certifiable=True,
            prior_art_classified=True,
            experimental_cost=1.0,
            claimed_capabilities=("finite_closure", "cycle_obstruction"),
        ),
        CandidateSketch(
            name=seven.name,
            fingerprint=seven_fp,
            exact_semantics=True,
            finite_horizon_tractable=True,
            lean_certifiable=True,
            prior_art_classified=True,
            experimental_cost=1.0,
            claimed_capabilities=("latent_piecewise_affine_control",),
        ),
        CandidateSketch(
            name="hidden_congruence_a",
            fingerprint=_fingerprint_of(cast(ProblemSpec, HiddenCongruenceASpec()), corpus),
            exact_semantics=True,
            finite_horizon_tractable=True,
            lean_certifiable=True,
            prior_art_classified=True,
            experimental_cost=1.0,
        ),
        CandidateSketch(
            name="hidden_vector_parity_shear",
            fingerprint=_fingerprint_of(cast(ProblemSpec, HiddenParityShearSpec()), corpus),
            exact_semantics=True,
            finite_horizon_tractable=True,
            lean_certifiable=True,
            prior_art_classified=True,
            experimental_cost=1.5,
            claimed_capabilities=("latent_vector_affine_control",),
        ),
        CandidateSketch(
            name="integer_polynomial_x2_minus_2",
            fingerprint=_fingerprint_of(cast(ProblemSpec, IntegerPolynomialSpec()), corpus),
            exact_semantics=True,
            finite_horizon_tractable=True,
            lean_certifiable=True,
            prior_art_classified=True,
            experimental_cost=1.0,
        ),
    )


def score_pool(corpus: ResearchCorpus, memory: ResearchMemory | None = None) -> tuple[SelectionReport, ...]:
    reports = tuple(
        score_candidate(sketch, corpus, memory=memory) for sketch in candidate_sketches(corpus)
    )
    return tuple(sorted(reports, key=lambda item: (-item.value, item.name)))


def spec_for_selection(name: str) -> ProblemSpec:
    mapping: dict[str, ProblemSpec] = {
        increment_spec().name: cast(ProblemSpec, increment_spec()),
        mx_plus_r_spec(7, 1).name: cast(ProblemSpec, mx_plus_r_spec(7, 1)),
        "hidden_congruence_a": cast(ProblemSpec, HiddenCongruenceASpec()),
        "hidden_vector_parity_shear": cast(ProblemSpec, HiddenParityShearSpec()),
        "integer_polynomial_x2_minus_2": cast(ProblemSpec, IntegerPolynomialSpec()),
    }
    if name not in mapping:
        raise KeyError(name)
    return mapping[name]
