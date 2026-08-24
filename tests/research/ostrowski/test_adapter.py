"""OstrowskiSpec is the problem adapter: q, energy, digits, affine, recurrence."""

from __future__ import annotations

from research.ostrowski.adapter import OstrowskiSpec, ostrowski_spec, plan_np
from research.ostrowski.live_growth import legal_w, residual_is_live
from research.ostrowski.live_layers import energy_canonical
from research.ostrowski.recurrence import companion_matches_residual, recurrence_spec
from research.ostrowski.residual import residual_integer
from research.ostrowski.spectral_residual import residual_matrix, transition_affine
from research.ostrowski.system import nonpisot_order3, phase0_order3
from research_engine.attacks.result import AttackStatus
from research_engine.core.phase import IntPhase
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import ClaimKind, SearchScope
from research_engine.planner.hypothesis import HypothesisStatus


def test_ostrowski_spec_is_a_problem_spec_and_keeps_energy_off_the_engine():
    for system in (nonpisot_order3(), phase0_order3()):
        spec = ostrowski_spec(4, system)
        assert isinstance(spec, ProblemSpec)
        assert spec.q(0) == 1
        assert spec.q(3) == system.place_value(3)
        state = (1, -2, 3)
        assert spec.energy(state, 5) == residual_integer(system, state, 5)
        assert spec.energy(state, 5) == energy_canonical(system, state, 5)
        phase = IntPhase(3)
        assert spec.legal_controls(spec.initial_state, phase) == legal_w(system, 2)
        assert spec.digit_realization(0, phase)
        assert spec.digit_realization(99, phase) is False
        assert spec.is_terminal((0, 0, 0), IntPhase(4)) == residual_is_live(system, (0, 0, 0), 4)
        assert spec.transition((0, 0, 0), 1, phase) == transition_affine(system, (0, 0, 0), 1)
        rec = spec.recurrence()
        assert rec is not None
        assert rec.companion_matrix() == residual_matrix(system)
        assert companion_matches_residual(system)
        affine = spec.affine_system()
        assert affine.A == residual_matrix(system)
        assert affine.translation(0) == (0, 0, 0)


def test_adapter_plan_does_not_promote_l0():
    report = plan_np(4)
    live = next(item for item in report.hypotheses if item.id == "ostrowski_L0_infinite")
    assert live.status is HypothesisStatus.PARKED
    assert live.kind is ClaimKind.LIVE
    assert live.intended_scope is SearchScope.EXACT
    spectral = next(item for item in report.results if item.name == "spectral")
    assert spectral.status is AttackStatus.SUPPORTED
    assert spectral.scope is SearchScope.EXACT
    assert spectral.kind is ClaimKind.REACHABLE
    assert spectral.kind is not ClaimKind.LIVE
    assert spectral.evidence["certificate"]["perron_non_pisot"]
    assert spectral.evidence["floats_are_labels_only"] is True
    assert isinstance(ostrowski_spec(2), OstrowskiSpec)
    assert recurrence_spec(nonpisot_order3()) is not None
