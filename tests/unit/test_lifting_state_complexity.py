"""State complexity experiments for the 3-adic lifting machine."""

from __future__ import annotations

import pytest

from bt.calculus.lifting_state import (
    behaviour_class,
    is_truncated_tree,
    linear_state,
    truncated_tree,
)
from research.lifting.state_complexity import (
    EXPENSIVE_R,
    attainment,
    behaviour_shapes_seen,
    deep_state_report,
    minimality_witness,
    normal_form,
    quotient_chain,
    realising_poly,
    row_structure,
    scaling_invariance,
    shallow_census,
    shift_law,
    shifted_family_injectivity,
    strata,
    truncated_tree_rows,
    valuation_rows,
)

# ------------------------------------------------------- quotient chain

@pytest.mark.parametrize("r", (1, 2, 3, 4))
def test_quotient_chain_is_strict_below_phi(r):
    row = quotient_chain(r)
    assert row["formula_holds"]
    assert not row["phi_is_minimal"]
    assert row["behaviours"] < row["phi_states"]
    assert row["behaviours"] <= row["unit_orbits"]


def test_unit_orbits_are_a_proper_intermediate_quotient():
    # Scaling explains part of the collapse, but not all of it from r = 2.
    assert quotient_chain(1)["orbits_are_minimal"]
    for r in (2, 3, 4):
        assert not quotient_chain(r)["orbits_are_minimal"]


def test_expensive_horizons_require_an_explicit_flag():
    with pytest.raises(ValueError):
        quotient_chain(EXPENSIVE_R)
    with pytest.raises(ValueError):
        valuation_rows(EXPENSIVE_R)
    with pytest.raises(ValueError):
        deep_state_report(EXPENSIVE_R)


# ----------------------------------------------------- valuation rows

@pytest.mark.parametrize("r", (1, 2, 3, 4))
def test_valuation_rows_and_overlap_hold(r):
    row = valuation_rows(r)
    assert row["rows_hold"]
    assert row["overlap_holds"]
    assert row["overlap"] == row["predicted_overlap"]


@pytest.mark.parametrize("e", (0, 1, 2, 3, 4))
def test_row_structure_theorem(e):
    row = row_structure(4, e)
    assert row["low_is_truncated_tree"]
    assert row["high_has_ternary_block"]
    assert row["low_count"] == row["low_predicted"]
    assert row["high_count"] == row["high_predicted"]
    assert row["total"] == row["total_predicted"]


def test_row_structure_rejects_e_above_r():
    with pytest.raises(ValueError):
        row_structure(2, 3)


@pytest.mark.parametrize("r", (1, 2, 3, 4))
def test_truncated_trees_explain_the_whole_overlap(r):
    row = truncated_tree_rows(r)
    assert row["rows_containing"] == row["predicted"]
    assert row["excess"] == row["row_overlap"]


def test_truncated_tree_is_fully_ternary_to_its_depth():
    for j in range(4):
        shape = truncated_tree(j, 3)
        assert is_truncated_tree(shape)
        assert shape == behaviour_class(linear_state(3**j, 0), 3)
    assert truncated_tree(0, 3) == ()
    assert len(truncated_tree(1, 3)) == 3


# ---------------------------------------------------------- witnesses

def test_minimality_witness_is_x_against_minus_x():
    row = minimality_witness(bound=6, r=3)
    assert row["found"]
    assert {row["left"], row["right"]} == {"x", "-x"}
    assert row["is_unit_multiple"] == -1
    assert row["phi_left"] != row["phi_right"]


def test_scaling_invariance_never_fails_but_moves_the_jet():
    row = scaling_invariance(k_max=3, r_max=2)
    assert row["ok"]
    assert row["failures"] == []
    assert row["phi_moved"] > 0
    assert row["checked"] > 1000


# --------------------------------------------------------- attainment

@pytest.mark.parametrize("r", (1, 2, 3))
def test_every_counted_behaviour_is_realised(r):
    row = attainment(r)
    assert row["attained"]
    assert row["missing"] == 0
    assert row["behaviours"] == row["realised"]


def test_attainment_is_not_an_artefact_of_degree_one():
    for r in (1, 2):
        row = attainment(r, degree=2)
        assert row["attained"]


def test_realising_poly_has_the_intended_node():
    from bt.calculus.lifting import node_at

    for r in (1, 2, 3):
        for c, b in ((0, 1), (1, 3), (4, 0), (7, 5)):
            f = realising_poly(c, b, r)
            node = node_at(f, (0,) * r)
            assert node.f_value % node.modulus == 0
            assert node.scaled_value == c
            assert node.f_prime == b
            assert node.residual.coeffs == linear_state(c, b).coeffs


def test_realising_poly_rejects_other_degrees():
    with pytest.raises(ValueError):
        realising_poly(1, 1, 2, degree=3)


# ----------------------------------------------------- shallow regime

def test_shallow_regime_has_more_behaviours_than_the_deep_bound_allows():
    row = shallow_census(k_max=4, r_max=3)
    assert row["polynomials"] > 40
    for entry in row["rows"]:
        assert entry["deep_within_bound"]
        assert entry["shallow_behaviours"] <= entry["shallow_phi"]
    # At r = 1 the shallow nodes already exceed the deep count of 5.
    assert row["rows"][0]["shallow_behaviours"] > row["rows"][0]["deep_behaviours"]


def test_behaviour_census_finds_all_four_shape_kinds():
    kinds = behaviour_shapes_seen(k_max=4, r=3)["kinds"]
    assert set(kinds) == {"dead", "path", "truncated_tree", "mixed"}
    assert all(count > 0 for count in kinds.values())


# ------------------------------------------------------------- report

def test_deep_state_report_verdict():
    report = deep_state_report(3)
    verdict = report["verdict"]
    assert verdict["closed_form"]
    assert verdict["rows_closed_form"]
    assert verdict["overlap_closed_form"]
    assert verdict["scaling_invariant"]
    assert verdict["attained"]
    assert not verdict["phi_minimal"]
    assert not verdict["orbits_minimal"]
    assert verdict["shift_is_the_balanced_value"]
    assert verdict["shift_is_not_the_digit_sum"]
    assert verdict["shifted_family_separates"]
    assert verdict["normal_form_is_complete"]
    assert verdict["dominated_collapses_to_valuation"]
    assert verdict["undominated_is_the_unit_orbit"]
    assert len(report["chain"]) == 3
    assert report["witness"]["found"]


# --------------------------------------------------- shift and separation

def test_shift_law_selects_the_balanced_value_over_the_digit_sum():
    row = shift_law(e_max=3)
    assert row["cases"] > 0
    assert row["packed_holds"]
    assert row["packed_failures"] == 0
    assert row["digit_sum_refuted"]
    assert all(row["window_is_complete_residue_system"].values())


def test_shifted_family_separates_every_residue():
    row = shifted_family_injectivity(e_max=3, budget=5)
    assert row["injective"]
    assert row["deepest_leaf_identified"]
    for entry in row["rows"]:
        assert entry["distinct"] == entry["states"]
        assert entry["collisions"] == []


def test_normal_form_is_a_complete_invariant():
    row = normal_form(r_max=3)
    assert row["bijective"]
    for entry in row["rows"]:
        assert entry["clashes"] == 0
        assert entry["dominated_not_a_tree"] == 0
        assert entry["keys"] == entry["behaviours"] == entry["formula"]
        assert entry["dominated"] + entry["undominated"] == entry["formula"]


def test_strata_split_into_valuation_collapse_and_orbit_rigidity():
    row = strata(r_max=3)
    assert row["dominated_collapses_to_valuation"]
    assert row["undominated_is_exactly_the_unit_orbit"]
    for entry in row["rows"]:
        assert entry["orbit_clashes"] == 0
        assert entry["undominated_orbits"] == entry["undominated_behaviours"]
