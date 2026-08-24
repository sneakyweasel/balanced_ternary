"""Order dependence of C and R."""

from __future__ import annotations

from itertools import product

from research.collatz.itinerary import affine_constant
from research.collatz.order_analysis import (
    adjacent_swap_delta_C,
    ascending_ks,
    descending_ks,
    extremal_orders,
    permutations_change_R,
    swap_adjacent,
    verify_swap_formula,
)


def test_swap_formula_all_short():
    for m in range(2, 5):
        for ks in product(range(1, 4), repeat=m):
            for t in range(m - 1):
                assert verify_swap_formula(ks, t)
                nxt = swap_adjacent(ks, t)
                assert affine_constant(nxt) - affine_constant(ks) == adjacent_swap_delta_C(ks, t)


def test_descending_maximises_C():
    ks = (1, 1, 2, 3)
    ext = extremal_orders(ks)
    assert ext["C_extremal_are_sorted"]
    assert ext["C_max"]["ks"] == list(descending_ks(ks))
    assert ext["C_min"]["ks"] == list(ascending_ks(ks))


def test_order_can_change_R():
    # Same (m,K)=(2,3): (1,2) vs (2,1)
    assert permutations_change_R((1, 2))
    assert min_realizer_pair()


def min_realizer_pair() -> bool:
    from research.collatz.min_realizer import min_realizer

    return min_realizer((1, 2)) != min_realizer((2, 1))
