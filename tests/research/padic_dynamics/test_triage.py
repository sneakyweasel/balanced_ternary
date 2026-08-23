"""Phase-0 tests for 3-adic polynomial cycle dynamics."""

from __future__ import annotations

import pytest

from bt.calculus.section import parse_poly
from research.padic_dynamics.families import all_families
from research.padic_dynamics.problem import PROBLEM
from research.padic_dynamics.triage import (
    behaviour_signature,
    canonical_cycle,
    classical_signature,
    comparison_report,
    cycle_lifts,
    cycles_mod,
    reduce_cycle,
    residual_signature,
    state_records,
)


def test_closed_problem_is_registered():
    from research.open_problems import get_problem

    assert PROBLEM.status == "ARCHIVED"
    assert get_problem("padic_dynamics") is PROBLEM


def test_canonical_cycle_is_rotation_invariant():
    expected = (1, 4, 7)
    assert canonical_cycle((1, 4, 7)) == expected
    assert canonical_cycle((4, 7, 1)) == expected
    assert canonical_cycle((7, 1, 4)) == expected


def test_cycle_enumeration_is_exact_on_small_graph():
    f = parse_poly("x^2-1")
    assert cycles_mod(f, 1) == ((0, 2),)
    for cycle in cycles_mod(f, 3):
        for x, image in zip(cycle, cycle[1:] + cycle[:1], strict=True):
            assert f.eval(x) % 27 == image


def test_cycle_lifts_reduce_to_the_parent():
    f = parse_poly("x^2-1")
    parent = (0, 2)
    children = cycle_lifts(f, parent, 1)
    assert children
    assert all(reduce_cycle(child, 1) == parent for child in children)
    assert all(len(child) % len(parent) == 0 for child in children)


def test_signatures_are_rotation_invariant():
    f = parse_poly("x^2-1")
    cycle = next(c for c in cycles_mod(f, 2) if len(c) == 2)
    rotated = cycle[1:] + cycle[:1]
    assert classical_signature(f, cycle, 2, 2) == classical_signature(f, rotated, 2, 2)
    assert residual_signature(f, cycle, 2, 2) == residual_signature(f, rotated, 2, 2)
    assert behaviour_signature(f, cycle, 2, 2) == behaviour_signature(f, rotated, 2, 2)


@pytest.fixture(scope="module")
def phase0_records():
    return state_records(k_max=3, r=3)


def test_corpus_contains_every_classical_one_level_type(phase0_records):
    assert {record.classical.lift_type for record in phase0_records} == {
        "grow",
        "split",
        "grow-tails",
        "partial-split",
    }


def test_periods_match_the_p3_classical_control_set(phase0_records):
    assert {record.period for record in phase0_records} == {1, 2, 3, 6, 9}
    assert {record.period for record in phase0_records} <= {1, 2, 3, 4, 6, 9}


def test_residual_function_class_determines_bounded_future_on_census(phase0_records):
    search = comparison_report(phase0_records)["search_b"]
    assert search["sufficient_on_census"]
    assert search["residual_classes_with_different_futures"] == 0
    assert search["classification"] == "REPARAMETERIZATION"


def test_coarse_multiplier_valuations_do_not_determine_future(phase0_records):
    search = comparison_report(phase0_records)["search_a"]
    assert search["coarse_classes_with_different_futures"] > 0
    witness = search["witness"]
    assert witness is not None
    assert {witness["left"]["family"], witness["right"]["family"]} == {"x^2-3", "x^2+3"}


def test_affine_data_misses_a_visible_higher_taylor_term():
    f = parse_poly("x^3-x")
    low = (0,)
    high = (0,)
    assert classical_signature(f, low, 1, 3).affine == classical_signature(f, high, 2, 3).affine
    assert residual_signature(f, low, 1, 3) != residual_signature(f, high, 2, 3)
    assert behaviour_signature(f, low, 1, 3) != behaviour_signature(f, high, 2, 3)


def test_bounded_behaviour_strictly_compresses_residual_states():
    by_id = {family.id: family.poly for family in all_families()}
    left = by_id["x^2-1"]
    right = by_id["x^2+2"]
    cycle = (0, 2)
    assert behaviour_signature(left, cycle, 1, 2) == behaviour_signature(right, cycle, 1, 2)
    assert residual_signature(left, cycle, 1, 2) != residual_signature(right, cycle, 1, 2)
