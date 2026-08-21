"""Valuation cylinders: unique residues and density 2^{-K}."""

from __future__ import annotations

import pytest

from collatz.automata.valuation_shift import PrecisionState, follow_path
from collatz.core import collatz_valuation
from collatz.cylinders import (
    belongs_to_cylinder,
    cylinder_residues,
    parse_ks,
    precision_cost,
    successive_valuations,
    valuation_cylinder,
    verify_cylinder_against_follow_path,
)


def _compositions(max_sum: int) -> list[tuple[int, ...]]:
    out: list[tuple[int, ...]] = []

    def rec(remaining: int, acc: list[int]) -> None:
        if remaining == 0:
            if acc:
                out.append(tuple(acc))
            return
        for k in range(1, remaining + 1):
            rec(remaining - k, acc + [k])

    for total in range(1, max_sum + 1):
        rec(total, [])
    return out


def test_parse_ks():
    assert parse_ks("1,2,1") == (1, 2, 1)
    assert parse_ks((2, 3)) == (2, 3)
    assert parse_ks("") == ()
    with pytest.raises(ValueError):
        parse_ks("1,0")


def test_known_single_step_residues():
    assert cylinder_residues((1,)) == (3,)
    assert cylinder_residues((2,)) == (1,)
    assert cylinder_residues((1, 1)) == (7,)
    cyl = valuation_cylinder((1,))
    assert cyl.precision == 2
    assert cyl.class_count == 1
    assert cyl.density_numerator == 1
    assert cyl.density_denominator == 2
    assert cyl.matches_haar
    assert cyl.budget.kind == "expanding"


def test_empty_cylinder_is_odds_mod_2():
    cyl = valuation_cylinder(())
    assert cyl.precision == 1
    assert cyl.residues == (1,)
    assert cyl.matches_haar
    assert precision_cost((), leftover_q=1) == 1
    assert precision_cost((1, 2), leftover_q=3) == 6


def test_density_is_exactly_two_to_minus_K():
    for ks in _compositions(6):
        cyl = valuation_cylinder(ks)
        k_sum = sum(ks)
        assert cyl.class_count == 1
        assert cyl.odd_residue_count == 1 << k_sum
        assert cyl.matches_haar
        assert cyl.admissible
        assert verify_cylinder_against_follow_path(ks)


def test_leftover_q_lifts():
    cyl = valuation_cylinder((1,), leftover_q=3)
    assert cyl.precision == 4
    assert cyl.class_count == 4  # 2^{Q-1}
    assert cyl.matches_haar
    assert verify_cylinder_against_follow_path((1,), leftover_q=3)


def test_belongs_to_cylinder_matches_residues():
    ks = (1, 2, 1)
    cyl = valuation_cylinder(ks)
    for n in range(-400, 401):
        if n % 2 == 0:
            assert not belongs_to_cylinder(n, ks)
            continue
        in_cyl = belongs_to_cylinder(n, ks)
        assert in_cyl == cyl.contains_residue(n)
        if in_cyl:
            assert successive_valuations(n, 3) == ks


def test_27_has_first_valuation_1():
    assert collatz_valuation(27) == 1
    assert belongs_to_cylinder(27, (1,))
    assert not belongs_to_cylinder(27, (2,))


def test_follow_path_ok_on_cylinder_residue():
    ks = (2, 1)
    cyl = valuation_cylinder(ks)
    r = cyl.residues[0]
    _, status = follow_path(PrecisionState(r, cyl.precision), ks)
    assert status == "ok"
