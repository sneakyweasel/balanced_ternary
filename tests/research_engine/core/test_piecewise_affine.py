"""Hidden piecewise-affine census. Ground truth lives here, not on the specs."""

from __future__ import annotations

from pathlib import Path

from research_engine.attacks.piecewise_affine import (
    CensusKind,
    PiecewiseAffineCensusAttack,
    RegionKind,
    branch_metrics,
    run_piecewise_affine_census,
)
from research_engine.attacks.result import AttackContext, AttackStatus
from research_engine.benchmarks.hidden_piecewise import (
    HiddenCongruenceASpec,
    HiddenNestedCSpec,
    HiddenPowerClearDSpec,
    HiddenSignBSpec,
)
from research_engine.core.affine_system import AffineSystem
from tests.research_engine.core.test_planner import CountdownSpec


# Ground truth for validation of the attack, not installed on the specs.
A_BRANCHES = ((2, 1, 1), (1, 1, -4), (3, 1, 0))
B_BRANCHES = ((2, 1, 3), (1, 1, -5))
C_BRANCHES = ((2, 1, 0), (1, 1, 3), (3, 1, -1), (1, 1, -2))
D_FAMILY = (1, 1)


def test_attack_source_does_not_seed_collatz_structure():
    text = Path(__file__).resolve().parents[3].joinpath(
        "src", "research_engine", "attacks", "piecewise_affine.py"
    ).read_text(encoding="utf-8")
    lowered = text.lower()
    assert "collatz" not in lowered
    assert "syracuse" not in lowered
    assert "3 * n + 1" not in text
    assert "v_2(3" not in text


def test_countdown_with_explicit_controls_is_inapplicable():
    spec = CountdownSpec()
    attack = PiecewiseAffineCensusAttack()
    assert attack.applicable(spec, AttackContext()) is False
    assert attack.applicable(spec, AttackContext(affine=AffineSystem(A=((1,),), translations={0: (0,)}))) is False


def test_congruence_map_a_recovers_three_residue_branches():
    spec = HiddenCongruenceASpec()
    census = run_piecewise_affine_census(spec, spec.attack_context())
    metrics = branch_metrics(census, A_BRANCHES)
    assert census.census_kind == CensusKind.FINITE_CENSUS.value
    assert metrics["branch_recall"] == 1.0
    assert metrics["branch_precision"] == 1.0
    assert metrics["coverage"] >= 0.95
    assert metrics["false_branch_rate"] == 0.0
    moduli = {
        int(branch.region.parameters["modulus"])
        for branch in census.branches
        if branch.region is not None
    }
    residues = {
        int(branch.region.parameters["residue"])
        for branch in census.branches
        if branch.region is not None and branch.region.kind == RegionKind.CONGRUENCE.value
    }
    assert moduli == {3}
    assert residues == {0, 1, 2}
    assert any(control.kind == "residue" for control in census.latent_controls)
    result = PiecewiseAffineCensusAttack().run(spec, spec.attack_context())
    assert result.status is AttackStatus.OBSERVATION
    assert result.evidence.get("reconstructed_affine") is None


def test_sign_map_b_recovers_sign_regions():
    spec = HiddenSignBSpec()
    census = run_piecewise_affine_census(spec, spec.attack_context())
    metrics = branch_metrics(census, B_BRANCHES)
    assert census.census_kind == CensusKind.FINITE_CENSUS.value
    assert metrics["branch_recall"] == 1.0
    assert metrics["branch_precision"] == 1.0
    kinds = {branch.region.kind for branch in census.branches if branch.region is not None}
    assert kinds == {RegionKind.SIGN.value}
    signs = {
        branch.region.parameters["sign"]
        for branch in census.branches
        if branch.region is not None
    }
    assert signs == {"nonneg", "neg"}


def test_nested_map_c_does_not_stop_at_parity():
    spec = HiddenNestedCSpec()
    census = run_piecewise_affine_census(spec, spec.attack_context())
    metrics = branch_metrics(census, C_BRANCHES)
    assert census.census_kind == CensusKind.FINITE_CENSUS.value
    assert metrics["branch_recall"] == 1.0
    assert metrics["branch_precision"] == 1.0
    odd_branches = [
        branch
        for branch in census.branches
        if branch.region is not None
        and branch.region.kind == RegionKind.CONGRUENCE.value
        and int(branch.region.parameters["residue"]) % 2 == 1
    ]
    assert len(odd_branches) == 3
    odd_moduli = {int(branch.region.parameters["modulus"]) for branch in odd_branches}
    assert 2 not in odd_moduli
    assert any(modulus % 2 == 0 and modulus > 2 for modulus in odd_moduli) or odd_moduli == {6}


def test_parameterized_map_d_does_not_emit_a_finite_table():
    spec = HiddenPowerClearDSpec()
    census = run_piecewise_affine_census(spec, spec.attack_context())
    assert census.census_kind == CensusKind.PARAMETERIZED_CENSUS.value
    assert census.family is not None
    assert census.family.p == D_FAMILY[0]
    assert census.family.r == D_FAMILY[1]
    assert len(census.family.observed_k) >= 3
    assert census.branches == ()
    assert census.coverage >= 0.6
    result = PiecewiseAffineCensusAttack().run(spec, spec.attack_context())
    assert result.status is AttackStatus.OBSERVATION
    assert "parameterized family" in result.claim


def test_lean_synthetic_a_has_no_sorry():
    path = Path(__file__).resolve().parents[3] / "formal" / "Problems" / "Engine" / "PiecewiseCensus.lean"
    text = path.read_text(encoding="utf-8")
    assert "sorry" not in text
    assert "admit" not in text
    assert "hiddenCongruenceA_mod0" in text
    assert "hiddenCongruenceA_mod1" in text
    assert "hiddenCongruenceA_mod2" in text


def test_planner_does_not_inject_affine_system():
    spec = HiddenCongruenceASpec()
    context = spec.attack_context()
    assert context.affine is None
    from research_engine.planner.orchestrator import AttackPlanner

    report = AttackPlanner().run(spec, context)
    names = [item.name for item in report.results]
    assert names[0] == "reconnaissance"
    assert "piecewise_affine" in names
    assert names.index("piecewise_affine") == 1
    assert names.index("parameter_domain") == 2
    assert names.index("control_word") == 3
    assert names.index("control_obstruction") == 4
    assert spec.attack_context().affine is None
    piecewise = next(item for item in report.results if item.name == "piecewise_affine")
    assert piecewise.evidence.get("reconstructed_affine") is None
