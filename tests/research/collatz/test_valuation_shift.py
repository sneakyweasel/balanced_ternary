"""Tests for admissible valuation prefixes and residue precision drop."""

from __future__ import annotations

from research.collatz.automata.valuation_shift import (
    AdmissibleValuationAutomaton,
    PrecisionState,
    exact_collatz_residue_step,
    forbidden_patterns,
    growth_budget,
    verify_residue_step_against_T,
)
from research.collatz.core import collatz_step, collatz_valuation


def test_growth_budget_exact_comparison():
    # k=1 once: 2^1=2 < 3 -> expanding
    b = growth_budget((1,))
    assert b.kind == "expanding"
    assert b.two_power == 2 and b.three_power == 3
    # k=2 once: 4 > 3 -> contracting
    assert growth_budget((2,)).kind == "contracting"
    # two 1's: 2^2=4 < 9 -> expanding
    assert growth_budget((1, 1)).kind == "expanding"
    # (2,2): 2^4=16 > 9 -> contracting


def test_residue_step_matches_T():
    for precision in (4, 6, 8, 10):
        for n in range(1, 2000, 2):
            assert verify_residue_step_against_T(n, precision)
            k = collatz_valuation(n)
            if k < precision:
                start = PrecisionState(n % (1 << precision), precision)
                nxt = exact_collatz_residue_step(start, k)
                assert nxt is not None
                assert collatz_step(n) % nxt.modulus() == nxt.residue
                assert nxt.precision == precision - k


def test_enumerate_admissible_small():
    auto = AdmissibleValuationAutomaton(precision=8, k_max=5)
    report = auto.enumerate_admissible(length=4)
    assert report.start_count == 128
    assert (1,) in report.prefixes
    assert report.contracting + report.expanding == len(report.prefixes)
    # n ≡ 3 (mod 4) has k=1. Residues 3,7,11,15 mod 16 already; at P=8 many.
    assert auto.classify_word((1,)) == "ADMISSIBLE"


def test_known_forbidden_or_admissible():
    auto = AdmissibleValuationAutomaton(precision=8, k_max=4)
    # A first step k=1 is admissible.
    assert auto.classify_word((1,)) == "ADMISSIBLE"
    forbidden = forbidden_patterns(auto, 1)
    # At P=8, k=1..4 are all realizable (standard geometric).
    assert (1,) not in forbidden


def test_insufficient_precision_is_inconclusive():
    auto = AdmissibleValuationAutomaton(precision=3, k_max=8)
    # k=5 cannot be tested exactly at P=3.
    assert auto.classify_word((5,)) == "INCONCLUSIVE"
