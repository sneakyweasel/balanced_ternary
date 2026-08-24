"""Tests isolating the affine formula against raw T iteration."""

from __future__ import annotations

from itertools import product

from research.collatz.core import collatz_step
from research.collatz.cylinders import valuation_cylinder
from research.collatz.itinerary import ValuationItinerary, affine_constant, affine_constant_closed_form


def test_closed_form_on_all_short_words():
    for m in range(1, 5):
        for ks in product(range(1, 5), repeat=m):
            assert affine_constant(ks) == affine_constant_closed_form(ks)


def test_formula_on_all_length_three_kmax_four():
    for ks in product(range(1, 5), repeat=3):
        it = ValuationItinerary.from_ks(ks)
        r = valuation_cylinder(ks).residues[0]
        x = r
        for _ in ks:
            x = collatz_step(x)
        assert it.apply(r) == x
        assert it.apply(r + (1 << (it.K + 1))) == collatz_step(
            collatz_step(collatz_step(r + (1 << (it.K + 1))))
        )
