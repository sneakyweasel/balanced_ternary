"""Expanding ``T(n)=3n-lsd(n)`` residual discovery and engine adapter."""

from __future__ import annotations

from bt.calculus.derivative import D
from bt.calculus.integral import I
from bt.operators import lsd_digit
from research.balanced_ternary.expanding_d import (
    as_section,
    discovery_report,
    expanding_d,
    expanding_d_from_quotient,
    integer_orbit,
    lsd_orbit,
    magnitude_contracts,
    predicted_lsd_orbit,
    residue_step,
    sample_range,
    separating_pair,
)
from research.balanced_ternary.expanding_spec import (
    CONTROLS,
    RESIDUES,
    T_CONTROL,
    ExpandingDIntegerSpec,
    ExpandingDResidueSpec,
    expanding_d_spec,
    minimized_state_count,
    output_signatures,
    raw_state_count,
)
from research.balanced_ternary.lean_export import closure_is_exact_three
from research.balanced_ternary.planner import plan_expanding_d, plan_expanding_gain
from research.balanced_ternary.problem import PROBLEM
from research_engine.attacks.closure import ExhaustiveClosureAttack
from research_engine.attacks.result import AttackStatus
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import ClaimKind, SearchScope
from research_engine.planner.hypothesis import HypothesisStatus


def test_uses_existing_lsd_and_section_not_lab_d():
    for n in sample_range(20):
        assert expanding_d(n) == 3 * n - lsd_digit(n)
        assert expanding_d(n) == as_section(n)
        assert expanding_d(n) == I(-lsd_digit(n), n)
        assert expanding_d(n) == expanding_d_from_quotient(n)
        assert D(expanding_d(n)) == n
        if n != 0:
            assert expanding_d(n) != D(n)


def test_section_action_is_independent_of_higher_digits():
    for a in (-1, 0, 1):
        for x in sample_range(12):
            value = expanding_d(I(a, x))
            assert value == 9 * x + 2 * a
            assert lsd_digit(value) == -a
            for k in range(6):
                current = I(a, x)
                for _ in range(k):
                    current = expanding_d(current)
                assert lsd_digit(current) == ((-1) ** k) * a


def test_discovery_finds_three_lsd_classes_not_mod9():
    report = discovery_report(limit=40, length=12, max_window=3)
    assert report["status"] == "OBSERVATION"
    assert report["scope"] == "BOUNDED"
    assert report["class_count"] == 3
    assert report["lsd_class_count"] == 3
    assert report["windows_sufficient"][1] is True
    assert report["windows_sufficient"][2] is True
    assert report["observation_implies_lsd"] is True
    assert report["predicted_matches_sample"] is True
    assert report["mod9_not_necessary"] is True
    assert report["lsd_separates_1_2"] is True
    assert separating_pair(1, 4, 12) is None
    assert separating_pair(1, 2, 12) is not None
    for n in sample_range(40):
        assert lsd_orbit(n, 10) == predicted_lsd_orbit(n, 10)


def test_magnitude_expansion_is_not_a_lyapunov():
    assert not magnitude_contracts(1)
    assert abs(expanding_d(1)) > abs(1)
    for n in sample_range(30):
        if n == 0:
            assert expanding_d(n) == 0
            continue
        assert abs(expanding_d(n)) > abs(n)
    orbit = integer_orbit(1, 8)
    assert len(set(orbit)) == 9
    assert abs(orbit[-1]) > abs(orbit[0])


def test_perturbation_changes_residue_map_not_state_count():
    assert residue_step(1, 1) == -1
    assert residue_step(1, 2) == 1
    assert residue_step(1, 3) == 0
    assert residue_step(-1, 3) == 0
    for n in sample_range(20):
        assert lsd_digit(expanding_d(n, 2)) == lsd_digit(n)
        assert lsd_digit(expanding_d(n, 3)) == 0
    for gain in (1, 2, 3):
        report = plan_expanding_gain(gain, remaining=4)
        closure = next(item for item in report.results if item.name == "closure")
        assert closure.status is AttackStatus.SUPPORTED
        assert closure.evidence["union_size"] == 3
        assert closure.evidence["complete"] is True


def test_residue_spec_is_problem_spec_and_minimal_mealy_is_three():
    spec = expanding_d_spec(4)
    assert isinstance(spec, ProblemSpec)
    assert spec.affine_system() is None
    nxt = spec.transition((1,), T_CONTROL, spec.initial_phase())
    assert nxt == (-1,)
    assert spec.transition((0,), ("I", 1), spec.initial_phase()) == (1,)
    assert raw_state_count() == 3
    assert minimized_state_count() == 3
    assert len(set(output_signatures().values())) == 3
    assert set(spec.legal_controls((0,), spec.initial_phase())) == set(CONTROLS)


def test_integer_state_hits_cap_lsd_residual_closes():
    integer_spec = ExpandingDIntegerSpec(start=1, start_remaining=32)
    integer_result = ExhaustiveClosureAttack().run(
        integer_spec,
        integer_spec.attack_context(),
    )
    assert integer_result.status is AttackStatus.INCONCLUSIVE
    assert integer_result.scope is SearchScope.BOUNDED
    residue_spec = ExpandingDResidueSpec(start_remaining=4)
    residue_result = ExhaustiveClosureAttack().run(
        residue_spec,
        residue_spec.attack_context(),
    )
    assert residue_result.status is AttackStatus.SUPPORTED
    assert residue_result.scope is SearchScope.EXACT
    assert set(residue_result.evidence["union"]) == set(RESIDUES)


def test_planner_certifies_lsd_closure_not_horizon():
    report = plan_expanding_d(4)
    recon = next(item for item in report.results if item.name == "reconnaissance")
    assert recon.status is AttackStatus.OBSERVATION
    assert recon.scope is SearchScope.BOUNDED
    assert recon.kind is ClaimKind.LIVE_SLICE
    assert closure_is_exact_three(report)
    hyp = next(item for item in report.hypotheses if item.id == "expanding_d_lsd_closure")
    assert hyp.status is HypothesisStatus.SUPPORTED
    skipped = {item.attack for item in report.skipped}
    assert "modular" in skipped
    assert "spectral" in skipped
    assert any(path.endswith("ExpandingD.lean") for path in PROBLEM.lean)
