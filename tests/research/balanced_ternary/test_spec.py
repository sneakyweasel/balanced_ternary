"""Doubled-trit adapter reuses the existing bounded normalizer."""

from __future__ import annotations

from research.balanced_ternary.adapter import BENCHMARK_MATRIX, plan_doubled_trit
from research.balanced_ternary.lean_export import closure_is_exact_three
from research.balanced_ternary.problem import PROBLEM
from research.balanced_ternary.spec import (
    CANONICAL_CARRIES,
    DoubledTritSpec,
    doubled_trit_spec,
    lyapunov_decreases_outside_box,
    minimized_state_count,
    output_signatures,
    raw_state_count,
    reference_normalize,
    sign_equivariant,
    sign_orbit_count,
)
from research_engine.attacks.result import AttackStatus
from research_engine.core.phase import IntPhase
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import ClaimKind, SearchScope
from research_engine.planner.hypothesis import HypothesisStatus


def test_spec_is_problem_spec_and_matches_existing_normalizer():
    from bt.normtheory.coeffword import CoeffWord
    from bt.normtheory.locality import BoundedNormalizeTransducer

    spec = doubled_trit_spec(4)
    assert isinstance(spec, ProblemSpec)
    assert spec.affine_system() is None
    trans = BoundedNormalizeTransducer(2)
    words = [(), (0,), (1,), (-1,), (1, 0, -1), (1, 1, 1, -1, 0)]
    for word in words:
        assert spec.apply_word(word) == reference_normalize(word)
        doubled = CoeffWord(tuple(2 * digit for digit in word))
        assert spec.apply_word(word) == trans.apply(doubled)


def test_carry_step_delegates_to_transducer():
    spec = DoubledTritSpec()
    from bt.normtheory.locality import BoundedNormalizeTransducer

    trans = BoundedNormalizeTransducer(2)
    for carry in (-1, 0, 1):
        for digit in (-1, 0, 1):
            nxt, out = spec.emit(carry, digit)
            expected_q, expected_r = trans.step(carry, 2 * digit)
            assert (nxt, out) == (expected_q, expected_r)


def test_phase_flush_and_acceptance():
    spec = doubled_trit_spec(2)
    assert spec.initial_phase() == IntPhase(2)
    assert spec.legal_controls((0,), IntPhase(2)) == (-1, 0, 1)
    nxt = spec.transition((0,), 1, IntPhase(2))
    assert nxt == (1,)
    flush_phase = spec.next_phase(IntPhase(1), 1)
    assert flush_phase == IntPhase(0)
    assert spec.legal_controls((1,), flush_phase) == (0,)
    assert spec.transition((1,), 0, flush_phase) == (0,)
    assert spec.is_accepting((0,), IntPhase(0))
    assert not spec.is_accepting((1,), IntPhase(0))
    assert spec.legal_controls((0,), IntPhase(0)) == ()


def test_sign_symmetry_and_lyapunov():
    spec = doubled_trit_spec()
    for carry in range(-8, 9):
        for digit in (-1, 0, 1):
            assert sign_equivariant(carry, digit)
            if abs(carry) >= 2:
                assert lyapunov_decreases_outside_box(carry, digit)
            if abs(carry) <= 1:
                nxt, _out = spec.emit(carry, digit)
                assert abs(nxt) <= 1


def test_minimal_machine_is_three_states():
    assert raw_state_count() == 3
    assert sign_orbit_count() == 2
    assert minimized_state_count() == 3
    signatures = output_signatures()
    assert len(set(signatures.values())) == 3


def test_planner_certifies_exact_closure_not_horizon_stabilization():
    report = plan_doubled_trit(4)
    recon = next(item for item in report.results if item.name == "reconnaissance")
    assert recon.status is AttackStatus.OBSERVATION
    assert recon.scope is SearchScope.BOUNDED
    assert recon.kind is ClaimKind.LIVE_SLICE
    assert closure_is_exact_three(report)
    closure = next(item for item in report.results if item.name == "closure")
    assert set(closure.evidence["union"]) == set(CANONICAL_CARRIES)
    hyp = next(item for item in report.hypotheses if item.id == "balanced_ternary_finite_closure")
    assert hyp.status is HypothesisStatus.SUPPORTED
    skipped = {item.attack for item in report.skipped}
    assert "modular" in skipped
    assert "spectral" in skipped
    assert "symbolic" in skipped
    affine = next(item for item in report.results if item.name == "affine")
    assert affine.status is AttackStatus.OBSERVATION
    assert affine.scope is SearchScope.BOUNDED


def test_problem_descriptor():
    assert PROBLEM.id == "balanced_ternary_finite_state_dynamics"
    assert PROBLEM.status == "STRUCTURAL"
    assert BENCHMARK_MATRIX[0]["name"] == "balanced_ternary_normalization"
    assert any(item["class"] == "synthetic_infinite" for item in BENCHMARK_MATRIX)
    assert any(item["name"] == "nonpisot_ostrowski" for item in BENCHMARK_MATRIX)
