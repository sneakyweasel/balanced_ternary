"""Tests for the exact affine itinerary formula."""

from __future__ import annotations

from collatz.core import collatz_step
from collatz.cylinders import belongs_to_cylinder, valuation_cylinder
from collatz.itinerary import (
    ValuationItinerary,
    affine_constant,
    affine_constant_closed_form,
    positivity_threshold,
    verify_affine_against_T,
)


def test_empty_constant_is_zero():
    assert affine_constant(()) == 0
    assert affine_constant_closed_form(()) == 0
    it = ValuationItinerary.from_ks(())
    assert it.C == 0 and it.K == 0 and it.m == 0
    assert it.apply(7) == 7


def test_recurrence_matches_closed_form():
    words = [(), (1,), (2,), (1, 1), (1, 2, 1), (3, 1, 2, 1), (1, 1, 1, 1, 1)]
    for ks in words:
        assert affine_constant(ks) == affine_constant_closed_form(ks)


def test_extend_recurrence():
    it = ValuationItinerary.from_ks((1, 2))
    nxt = it.extend(3)
    assert nxt.C == 3 * it.C + it.denominator
    assert nxt.K == it.K + 3
    assert nxt.valuations == (1, 2, 3)
    assert nxt.C == affine_constant((1, 2, 3))


def test_affine_matches_iteration_on_realizers():
    prefixes = [(1,), (2,), (1, 1), (1, 2), (2, 1), (1, 1, 1), (1, 2, 1), (3, 1)]
    for ks in prefixes:
        cyl = valuation_cylinder(ks)
        r = cyl.residues[0]
        assert belongs_to_cylinder(r, ks)
        assert verify_affine_against_T(r, ks)
        it = ValuationItinerary.from_ks(ks)
        x = r
        for _ in ks:
            x = collatz_step(x)
        assert it.apply(r) == x
        n2 = r + (1 << cyl.precision)
        assert verify_affine_against_T(n2, ks)


def test_affine_many_odd_starts():
    ks = (1, 1, 2)
    it = ValuationItinerary.from_ks(ks)
    cyl = valuation_cylinder(ks)
    r = cyl.residues[0]
    for t in range(0, 40):
        n = r + t * (1 << cyl.precision)
        assert verify_affine_against_T(n, ks)
        x = n
        for _ in ks:
            x = collatz_step(x)
        assert it.apply(n) == x


def test_partial_states():
    ks = (1, 2, 1)
    n = valuation_cylinder(ks).residues[0]
    it = ValuationItinerary.from_ks(ks)
    states = it.all_partial_states(n)
    assert states[0] == n
    x = n
    for i, k in enumerate(ks):
        x = collatz_step(x)
        assert states[i + 1] == x
        assert it.partial_state(n, i + 1) == x


def test_positivity_threshold_is_one():
    assert positivity_threshold(()) == 1
    assert positivity_threshold((1, 1, 2, 3)) == 1
    assert affine_constant((1, 2, 3)) > 0


def test_single_step_formula():
    # T(n) = (3n+1)/2^{k0}, so C=(1,) is 1 and K=k0
    it = ValuationItinerary.from_ks((1,))
    assert it.C == 1
    assert it.K == 1
    n = 3  # v2(10)=1, T=5
    assert it.apply(n) == 5
