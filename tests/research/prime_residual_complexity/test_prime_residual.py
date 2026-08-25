"""Prime residual complexity under balanced-ternary sections."""

from __future__ import annotations

from math import gcd

from bt.arithmetic import is_prime
from bt.calculus.integral import I
from bt.calculus.jets import integer_jet
from research.open_problems import get_problem
from research.prime_residual_complexity.distinguish import (
    jet_prime_separator,
    residual_count,
    residual_table,
    sieve_prime_separator,
)
from research.prime_residual_complexity.lean_export import (
    SEPARATOR_THEOREM,
    PRIME_MODULE,
    export_prime_residual_targets,
    sieve_closure_is_exact,
)
from research.prime_residual_complexity.planner import (
    INTEGER_PRIME_HYPOTHESIS,
    JET_EQUALS_PRIME_HYPOTHESIS,
    SIEVE_EQUALS_PRIME_HYPOTHESIS,
    SIEVE_RESIDUAL_HYPOTHESIS,
    plan_prime_residual_complexity,
)
from research.prime_residual_complexity.problem import PROBLEM
from research.prime_residual_complexity.records import write_records
from research.prime_residual_complexity.sections import (
    apply_section_word,
    i0_prime_only_at_one,
    value_from_jet,
)
from research.prime_residual_complexity.sieve import (
    SIEVE_CHAIN,
    sieve_census,
    sieve_chain_census,
    sieve_modulus,
    step_mod,
)
from research.prime_residual_complexity.spec import prime_spec, sieve_spec
from research_engine.attacks.result import AttackStatus
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import ClaimKind, SearchScope
from research_engine.planner.hypothesis import HypothesisStatus
from research_engine.planner.orchestrator import run_named_attack


def test_problem_is_registered():
    assert get_problem("prime_residual_complexity") is PROBLEM
    assert PROBLEM.status == "ARCHIVED"
    assert PROBLEM.docs == ("docs/problems/prime_residual_complexity.md",)


def test_sections_use_existing_I():
    assert apply_section_word(1, (0,)) == I(0, 1) == 3
    assert value_from_jet((1, 0)) == 1
    assert i0_prime_only_at_one(1)
    assert not i0_prime_only_at_one(2)
    assert not i0_prime_only_at_one(-1)
    assert not i0_prime_only_at_one(0)


def test_sieve_dfa_is_finite_and_minimized():
    chain = sieve_chain_census()
    assert [item.primes for item in chain] == list(SIEVE_CHAIN)
    for item in chain:
        assert item.raw_states == item.modulus
        assert item.reachable_states == item.modulus
        assert 1 <= item.minimized_states <= item.raw_states
        assert item.survival_numerator == item.accepting_states
        assert item.survival_denominator == item.modulus
    full = sieve_census()
    assert full.modulus == 210
    assert full.reachable_states == 210
    assert full.minimized_states <= 210


def test_sieve_step_is_section_mod_M():
    modulus = sieve_modulus()
    assert step_mod(1, 0, modulus) == I(0, 1) % modulus
    assert step_mod(1, 1, modulus) == I(1, 1) % modulus
    assert gcd(1, modulus) == 1
    assert gcd(211, modulus) == 1


def test_jet_and_sieve_separators():
    jet = jet_prime_separator(1)
    assert integer_jet(jet.left, 1) == integer_jet(jet.right, 1)
    assert is_prime(jet.left_image) != is_prime(jet.right_image)
    assert jet.word == (0,)
    jet4 = jet_prime_separator(4)
    assert integer_jet(jet4.left, 4) == integer_jet(jet4.right, 4)
    sieve = sieve_prime_separator()
    assert sieve.left % 210 == sieve.right % 210
    assert is_prime(sieve.left_image) != is_prime(sieve.right_image)


def test_residual_counts_are_bounded_observations():
    table = residual_table(3, 2)
    assert len(table) == 3
    assert table[0] >= 2
    assert residual_count(1, 1) >= 2
    for prev, nxt in zip(table, table[1:]):
        assert nxt >= prev


def test_sieve_spec_wires_affine_and_closes():
    spec = sieve_spec(4)
    assert isinstance(spec, ProblemSpec)
    assert spec.affine_system() is not None
    assert spec.affine_system().A == ((3,),)
    result = run_named_attack("closure", spec, spec.attack_context())
    assert result.status is AttackStatus.SUPPORTED
    assert result.scope is SearchScope.EXACT
    assert result.evidence["union_size"] == 210
    modular = run_named_attack("modular", spec, spec.attack_context())
    assert modular.status is AttackStatus.OBSERVATION
    assert modular.scope is SearchScope.EXACT


def test_integer_prime_spec_hits_the_cap():
    spec = prime_spec(4)
    result = run_named_attack("closure", spec, spec.attack_context())
    assert result.status is AttackStatus.INCONCLUSIVE
    assert result.scope is SearchScope.BOUNDED
    assert spec.is_accepting((3,), spec.initial_phase())
    assert not spec.is_accepting((1,), spec.initial_phase())


def test_planner_decides_the_hypotheses():
    report = plan_prime_residual_complexity(4)
    assert sieve_closure_is_exact(report)
    recon = next(item for item in report.results if item.name == "reconnaissance")
    assert recon.status is AttackStatus.OBSERVATION
    assert recon.scope is SearchScope.BOUNDED
    skipped = {item.attack for item in report.skipped}
    assert "modular" not in skipped
    assert "spectral" not in skipped
    sieve_hyp = next(item for item in report.hypotheses if item.id == SIEVE_RESIDUAL_HYPOTHESIS.id)
    assert sieve_hyp.status is HypothesisStatus.SUPPORTED
    jet_hyp = next(item for item in report.hypotheses if item.id == JET_EQUALS_PRIME_HYPOTHESIS.id)
    assert jet_hyp.status is HypothesisStatus.REFUTED
    sieve_eq = next(item for item in report.hypotheses if item.id == SIEVE_EQUALS_PRIME_HYPOTHESIS.id)
    assert sieve_eq.status is HypothesisStatus.REFUTED
    integer_hyp = next(item for item in report.hypotheses if item.id == INTEGER_PRIME_HYPOTHESIS.id)
    assert integer_hyp.status is HypothesisStatus.PARKED


def test_records_and_lean_export(tmp_path):
    report = plan_prime_residual_complexity(4)
    targets = export_prime_residual_targets(report)
    obstruction = next(item for item in targets if item.lean_theorem == SEPARATOR_THEOREM)
    assert obstruction.exportable
    assert obstruction.lean_module == PRIME_MODULE
    assert not any(item.kind is ClaimKind.LIVE and item.exportable for item in targets)
    written = write_records(report, targets, directory=tmp_path)
    names = {path.name for path in written}
    assert "reconnaissance.yaml" in names
    assert "closure.yaml" in names
    assert "skipped.yaml" in names
    closure_text = (tmp_path / "closure.yaml").read_text(encoding="utf-8")
    assert "status: EXACT" in closure_text
    assert "scope: EXACT" in closure_text
    assert "PROVED" not in closure_text
