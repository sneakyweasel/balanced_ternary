"""Shortcut Collatz finite-descent residual."""

from __future__ import annotations

from research.collatz_finite_descent.blocks import (
    all_odd_image,
    all_odd_witness,
    behavioral_classes,
    block_from_word,
    contraction_profile,
    enumerate_blocks,
    escape_residues,
    expanding_legal_witness,
    residue_of_word,
    separating_residues,
    unique_block,
)
from research.collatz_finite_descent.lean_export import (
    DESCENT_THEOREM,
    SHORTCUT_MODULE,
    closure_is_inconclusive,
    export_collatz_finite_descent_targets,
)
from research.collatz_finite_descent.planner import (
    INTEGER_RESIDUAL_HYPOTHESIS,
    ONE_STEP_LYAPUNOV_HYPOTHESIS,
    UNIFORM_DESCENT_HYPOTHESIS,
    plan_collatz_finite_descent,
    plan_perturbation_5_1,
    plan_terminal_cycle,
)
from research.collatz_finite_descent.problem import PROBLEM
from research.collatz_finite_descent.records import write_records
from research.collatz_finite_descent.shortcut import (
    CONTROL_EVEN,
    CONTROL_ODD,
    apply_word,
    cycle_containing,
    is_terminal,
    predecessors,
    shortcut_step,
)
from research.collatz_finite_descent.spec import shortcut_spec, terminal_spec
from research.open_problems import get_problem
from research_engine.attacks.result import AttackStatus
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import ClaimKind, SearchScope
from research_engine.planner.hypothesis import HypothesisStatus
from research_engine.planner.orchestrator import run_named_attack


def test_problem_is_registered():
    assert get_problem("collatz_finite_descent") is PROBLEM
    assert PROBLEM.status == "ARCHIVED"
    assert PROBLEM.docs == ("docs/problems/collatz_finite_descent.md",)


def test_shortcut_terminal_cycle_and_predecessors():
    assert shortcut_step(1) == 2
    assert shortcut_step(2) == 1
    assert is_terminal(1) and is_terminal(2)
    assert not is_terminal(3)
    assert cycle_containing(1) == frozenset({1, 2})
    assert predecessors(1) == (2,)
    assert predecessors(2) == (1, 4)
    assert predecessors(4) == (8,)
    assert 5 in predecessors(8)


def test_derived_blocks_match_the_map():
    even = block_from_word((CONTROL_EVEN,))
    assert even.slope == 1 and even.intercept == 0 and even.denominator == 2
    odd = block_from_word((CONTROL_ODD,))
    assert odd.slope == 3 and odd.intercept == 1 and odd.denominator == 2
    assert not odd.contracts(1)
    mixed = block_from_word((CONTROL_EVEN, CONTROL_ODD))
    assert mixed.residue == 2
    assert mixed.apply_legal(2) == apply_word(2, mixed.word)
    for block in enumerate_blocks(4):
        n = block.smallest_legal()
        assert unique_block(n, block.length).word == block.word
        assert residue_of_word(block.word) == n % block.modulus


def test_all_odd_word_is_the_uniform_descent_obstruction():
    for length in range(1, 13):
        n = all_odd_witness(length)
        image = all_odd_image(length)
        assert n == 2**length - 1
        assert image > n
        assert unique_block(n, length).word == (CONTROL_ODD,) * length
        assert n % (2**length) in escape_residues(length)
    witness, image, word = expanding_legal_witness(6)
    assert image >= witness
    assert word == unique_block(witness, 6).word


def test_behavioral_quotient_is_a_quotient_of_two_adic():
    classes = behavioral_classes(4)
    total = sum(len(residues) for residues in classes.values())
    assert total == 16
    assert len(classes) < 16
    pair = separating_residues(4)
    assert pair is not None
    left, right = pair
    assert contraction_profile(left, 4) == contraction_profile(right, 4)
    assert left != right


def test_spec_does_not_invent_an_affine_system():
    spec = shortcut_spec(4)
    assert isinstance(spec, ProblemSpec)
    assert spec.affine_system() is None
    assert spec.legal_controls((7,), spec.initial_phase()) == (CONTROL_ODD,)
    assert spec.legal_controls((8,), spec.initial_phase()) == (CONTROL_EVEN,)
    assert spec.transition((7,), CONTROL_ODD, spec.initial_phase()) == (11,)


def test_integer_closure_hits_the_cap_and_terminal_cycle_is_exact():
    report = plan_collatz_finite_descent(4)
    assert closure_is_inconclusive(report)
    recon = next(item for item in report.results if item.name == "reconnaissance")
    assert recon.status is AttackStatus.OBSERVATION
    assert recon.scope is SearchScope.BOUNDED
    skipped = {item.attack for item in report.skipped}
    assert "modular" in skipped
    assert "spectral" in skipped
    uniform = next(item for item in report.hypotheses if item.id == UNIFORM_DESCENT_HYPOTHESIS.id)
    assert uniform.status is HypothesisStatus.REFUTED
    lyapunov = next(item for item in report.hypotheses if item.id == ONE_STEP_LYAPUNOV_HYPOTHESIS.id)
    assert lyapunov.status is HypothesisStatus.REFUTED
    residual = next(item for item in report.hypotheses if item.id == INTEGER_RESIDUAL_HYPOTHESIS.id)
    assert residual.status is HypothesisStatus.PARKED
    terminal = plan_terminal_cycle(6)
    closure = next(item for item in terminal.results if item.name == "closure")
    assert closure.status is AttackStatus.SUPPORTED
    assert closure.scope is SearchScope.EXACT
    assert closure.evidence["union_size"] == 2
    spec = terminal_spec(6)
    result = run_named_attack("closure", spec, spec.attack_context())
    assert result.scope is SearchScope.EXACT


def test_perturbation_five_one_still_has_no_uniform_L_descent():
    report = plan_perturbation_5_1(4)
    uniform = next(item for item in report.hypotheses if item.id == UNIFORM_DESCENT_HYPOTHESIS.id)
    assert uniform.status is HypothesisStatus.REFUTED
    n, image, word = expanding_legal_witness(4, odd_mul=5, odd_add=1)
    assert image >= n
    assert word[0] == CONTROL_ODD or unique_block(n, 4, 5, 1).slope >= 16


def test_records_and_lean_export(tmp_path):
    report = plan_collatz_finite_descent(4)
    targets = export_collatz_finite_descent_targets(report)
    obstruction = next(item for item in targets if item.lean_theorem == DESCENT_THEOREM)
    assert obstruction.exportable
    assert obstruction.lean_module == SHORTCUT_MODULE
    assert not any(item.kind is ClaimKind.LIVE and item.exportable for item in targets)
    written = write_records(report, targets, directory=tmp_path)
    names = {path.name for path in written}
    assert "reconnaissance.yaml" in names
    assert "closure.yaml" in names
    assert "skipped.yaml" in names
    closure_text = (tmp_path / "closure.yaml").read_text(encoding="utf-8")
    assert "status: OBSERVED" in closure_text
    assert "scope: BOUNDED" in closure_text
    assert "PROVED" not in closure_text
