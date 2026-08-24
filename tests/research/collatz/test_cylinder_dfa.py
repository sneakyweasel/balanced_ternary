"""Cylinder DFA, minimization, and finite-L entropy."""

from __future__ import annotations

from itertools import product

from bt.representation import decode
from research.collatz.cylinders import valuation_cylinder
from research.collatz.languages.cylinder_dfa import CylinderDFA, entropy_report
from bt.automata.minimize import minimize_dfa
from research.collatz.transducers.valuation_languages import ValuationClassDFA


def test_minimize_two_state_odd_language():
    # Mod 2 Horner: r' = r + a (mod 2) since 3≡1.
    def delta(s: int, a: int) -> int:
        return (s + a) % 2

    m = minimize_dfa(start=0, alphabet=(-1, 0, 1), delta=delta, accepts=(1,))
    assert m.state_count == 2
    assert m.start == 0
    assert m.accepts == frozenset({1})


def test_dfa_accepts_iff_decode_in_cylinder():
    ks = (1, 1)
    cyl = valuation_cylinder(ks)
    dfa = CylinderDFA(ks)
    assert dfa.modulus == 8
    assert dfa.accept_residues == cyl.residues
    for digits in product((-1, 0, 1), repeat=4):
        word = "".join({-1: "-", 0: "0", 1: "+" }[d] for d in digits)
        n = decode(word)
        assert dfa.accepts(word) == cyl.contains_residue(n)


def test_empty_cylinder_accepts_odds():
    dfa = CylinderDFA(())
    assert dfa.count_words(1) == 2  # -, +
    assert dfa.count_canonical_words(1) == 2
    for word in ("-", "0", "+", "00", "0+", "+0"):
        n = decode(word)
        assert dfa.accepts(word) == (n % 2 != 0)


def test_conditioning_does_not_increase_padded_count():
    empty = CylinderDFA(()).count_words(5)
    one = CylinderDFA((1,)).count_words(5)
    two = CylinderDFA((1, 1)).count_words(5)
    assert one <= empty
    assert two <= one


def test_entropy_report_status():
    report = entropy_report((1,), 4)
    assert report.status == "VERIFIED COMPUTATIONALLY"
    assert report.word_count > 0
    assert report.minimized_states >= 1
    assert report.h_base3 is not None
    assert 0 < report.h_base3 <= 1
    assert report.empty_h_base3 is not None
    assert report.empty_h_base3 >= report.h_base3 - 1e-12


def test_valuation_class_a_k_positive():
    for k in range(0, 5):
        assert ValuationClassDFA(k).minimized_state_count() >= 1
