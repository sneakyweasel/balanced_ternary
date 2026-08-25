"""Diagnosis layer: fingerprints, families, coverage, and research decisions."""

from __future__ import annotations

from dataclasses import dataclass, replace

from research.balanced_ternary_digit_sum_dynamics.planner import plan_digit_sum_dynamics
from research.balanced_ternary_digit_sum_dynamics.spec import digit_sum_spec
from research.balanced_ternary_weight_drift.planner import plan_weight_drift
from research.balanced_ternary_weight_drift.spec import weight_drift_spec
from research.balanced_ternary_weight_dynamics.planner import plan_weight_dynamics
from research.balanced_ternary_weight_dynamics.spec import weight_dynamics_spec
from research.operator_dynamics.signed_p0.planner import plan_signed_p0
from research.operator_dynamics.signed_p0.spec import signed_p0_spec
from research_engine.attacks.result import AttackContext
from research_engine.core.phase import IntPhase
from research_engine.diagnosis.compare import compare_fingerprints, core_match
from research_engine.diagnosis.corpus import ResearchCorpus
from research_engine.diagnosis.decision import decide_research
from research_engine.diagnosis.family import family_status_for
from research_engine.diagnosis.fingerprint import fingerprint_from_report
from research_engine.diagnosis.loop import diagnose, record_from_session
from research_engine.diagnosis.types import (
    CAPABILITIES,
    CandidateSketch,
    CoverageStatus,
    DeltaLevel,
    FamilyStatus,
    RegimeFingerprint,
    ResearchDecision,
    UNOBSERVED,
)
from research_engine.diagnosis.selection import score_candidate
from research_engine.planner.orchestrator import AttackPlanner


@dataclass(frozen=True)
class FoldSpec:
    name: str = "fold_a"
    dimension: int = 1
    start: int = 8
    start_remaining: int = 6

    @property
    def initial_state(self) -> tuple[int, ...]:
        return (self.start,)

    def transition(self, state: tuple[int, ...], control: object, phase: IntPhase) -> tuple[int, ...]:
        del control, phase
        n = state[0]
        if n == 0:
            return (0,)
        return (n // 2 if abs(n) > 1 else 0,)

    def output(self, state: tuple[int, ...], control: object, phase: IntPhase | None = None) -> int:
        del control, phase
        return int(state[0])

    def legal_controls(self, state: tuple[int, ...], phase: IntPhase) -> tuple[object, ...]:
        del state
        if phase.value <= 0:
            return ()
        return (0,)

    def next_phase(self, phase: IntPhase, control: object) -> IntPhase:
        del control
        if phase.value > 0:
            return IntPhase(phase.value - 1)
        return phase

    def is_terminal(self, state: tuple[int, ...], phase: IntPhase) -> bool:
        del state
        return phase.value >= 0

    def is_accepting(self, state: tuple[int, ...], phase: IntPhase) -> bool:
        del state
        return phase.value == 0

    def initial_phase(self) -> IntPhase:
        return IntPhase(self.start_remaining)

    def canonicalize(self, state: tuple[int, ...]) -> tuple[int, ...]:
        return (int(state[0]),)

    def attack_context(self) -> AttackContext:
        return AttackContext(live_only=False, max_states=32, max_steps=self.start_remaining)


def _record_experiment(spec, report, corpus: ResearchCorpus, decision: ResearchDecision | None = None):
    diagnosis = diagnose(spec, report, spec.attack_context(), corpus)
    chosen, reason = decide_research(
        diagnosis.fingerprint,
        diagnosis.family_status,
        diagnosis.delta,
        report,
    )
    if decision is not None:
        chosen = decision
        reason = "seeded"
    record = record_from_session(spec, diagnosis, report, chosen, reason)
    corpus.add(record)
    return diagnosis, record


def test_fingerprint_ignores_spec_name():
    left = FoldSpec(name="alpha")
    right = FoldSpec(name="beta")
    planner = AttackPlanner()
    left_report = planner.run(left, left.attack_context())
    right_report = planner.run(right, right.attack_context())
    fp_left = fingerprint_from_report(left, left_report, left.attack_context())
    fp_right = fingerprint_from_report(right, right_report, right.attack_context())
    assert fp_left == fp_right
    assert "alpha" not in fp_left.as_dict().values()
    assert fp_left.numerical_contraction == "FINITE_CONTRACTING"
    assert fp_left.eventual_region == "FINITE_SEED_CLOSURE"


def test_unobserved_fields_stay_unset_without_evidence():
    spec = FoldSpec()
    report = AttackPlanner().run(spec, spec.attack_context())
    fingerprint = fingerprint_from_report(spec, report, spec.attack_context())
    assert fingerprint.block_structure == "INAPPLICABLE"
    assert fingerprint.spectral_structure == "INAPPLICABLE"
    assert fingerprint.modular_structure in {"INAPPLICABLE", "SAMPLED_RESTRICTION"}
    assert UNOBSERVED not in (
        fingerprint.state_space_type,
        fingerprint.control_structure,
        fingerprint.numerical_contraction,
    )


def test_digit_fold_family_saturates_without_name_special_cases():
    corpus = ResearchCorpus()
    specs_reports = (
        (signed_p0_spec(), plan_signed_p0()),
        (digit_sum_spec(), plan_digit_sum_dynamics()),
        (weight_dynamics_spec(), plan_weight_dynamics()),
    )
    fingerprints = []
    for spec, report in specs_reports:
        diagnosis, record = _record_experiment(
            spec, report, corpus, decision=ResearchDecision.CLOSE
        )
        fingerprints.append(diagnosis.fingerprint)
        assert record.decision is ResearchDecision.CLOSE
        assert diagnosis.fingerprint.numerical_contraction == "FINITE_CONTRACTING"
        assert diagnosis.fingerprint.eventual_region == "FINITE_SEED_CLOSURE"
        assert diagnosis.fingerprint.control_structure == "SINGLETON"
        assert diagnosis.fingerprint.state_space_type == "INTEGER_1D"

    assert core_match(fingerprints[0], fingerprints[1])
    assert core_match(fingerprints[1], fingerprints[2])
    similarity, delta = compare_fingerprints(fingerprints[0], fingerprints[2])
    assert similarity.score >= 0.55
    assert delta.level in {DeltaLevel.LOW, DeltaLevel.MEDIUM}
    status = family_status_for(fingerprints[2], corpus.records)
    assert status is FamilyStatus.SATURATED


def test_weight_drift_does_not_join_finite_contracting_family():
    corpus = ResearchCorpus()
    for spec, report in (
        (signed_p0_spec(), plan_signed_p0()),
        (digit_sum_spec(), plan_digit_sum_dynamics()),
        (weight_dynamics_spec(), plan_weight_dynamics()),
    ):
        _record_experiment(spec, report, corpus, decision=ResearchDecision.CLOSE)
    drift_spec = weight_drift_spec()
    drift_report = plan_weight_drift()
    diagnosis = diagnose(drift_spec, drift_report, drift_spec.attack_context(), corpus)
    assert diagnosis.fingerprint.numerical_contraction != "FINITE_CONTRACTING"
    assert diagnosis.fingerprint.eventual_region == "UNBOUNDED_SAMPLE"
    assert not core_match(diagnosis.fingerprint, corpus.records[0].fingerprint)
    assert diagnosis.family_status is FamilyStatus.ACTIVE
    assert diagnosis.delta is not None
    assert diagnosis.delta.level is DeltaLevel.HIGH


def test_saturated_family_discourages_similar_candidate():
    corpus = ResearchCorpus()
    for spec, report in (
        (signed_p0_spec(), plan_signed_p0()),
        (digit_sum_spec(), plan_digit_sum_dynamics()),
        (weight_dynamics_spec(), plan_weight_dynamics()),
    ):
        _record_experiment(spec, report, corpus, decision=ResearchDecision.CLOSE)
    similar = fingerprint_from_report(
        weight_dynamics_spec(),
        plan_weight_dynamics(),
        weight_dynamics_spec().attack_context(),
    )
    low = score_candidate(
        CandidateSketch(
            name="another_scalar_fold",
            fingerprint=similar,
            claimed_capabilities=("finite_closure", "numerical_contraction"),
            experimental_cost=1.0,
        ),
        corpus,
    )
    distant = score_candidate(
        CandidateSketch(
            name="noncontracting_integer_map",
            fingerprint=diagnose(
                weight_drift_spec(),
                plan_weight_drift(),
                weight_drift_spec().attack_context(),
                corpus,
            ).fingerprint,
            claimed_capabilities=tuple(CAPABILITIES),
            experimental_cost=1.0,
        ),
        corpus,
    )
    assert "saturated family" in low.explanation
    assert low.value < distant.value
    decision, _reason = decide_research(
        similar,
        FamilyStatus.SATURATED,
        compare_fingerprints(similar, corpus.records[0].fingerprint)[1],
        plan_weight_dynamics(),
    )
    assert decision is ResearchDecision.FAMILY_SATURATED


def test_coverage_marks_untested_capabilities():
    spec = signed_p0_spec()
    report = plan_signed_p0()
    diagnosis = diagnose(spec, report, spec.attack_context(), ResearchCorpus())
    assert diagnosis.coverage.status("finite_closure") == CoverageStatus.EXERCISED.value
    assert diagnosis.coverage.status("valuation_dynamics") == CoverageStatus.NOT_TESTED.value
    assert diagnosis.coverage.status("symbolic_control") == CoverageStatus.NOT_TESTED.value
    assert diagnosis.coverage.status("cycle_obstruction") == CoverageStatus.NOT_TESTED.value
