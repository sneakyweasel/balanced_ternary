"""Phase 0 triage of the 3-adic lifting hypotheses."""

from __future__ import annotations

import pytest

from bt.calculus.section import parse_poly
from research.lifting.families import (
    NONSINGULAR_IDS,
    SINGULAR_IDS,
    all_families,
    all_polys,
    family,
)
from research.lifting.problem import PROBLEM
from research.lifting.triage import (
    cap_v3,
    h1_identification,
    h2_taylor_jet,
    h3_trichotomy,
    linear_state_determinacy,
    unordered_shape_census,
    linearization,
    pair_determinacy,
    phi_determinacy,
    phi_sharpness,
    state_census,
    triage_report,
    valuation_determinacy,
)

SAMPLE = [parse_poly(t) for t in ("x^2-1", "x^2-9", "x^2+9", "x^3-x", "x^3-9", "x^4-1")]


def test_problem_descriptor():
    assert PROBLEM.id == "lifting"
    assert PROBLEM.status == "EXPLORATORY"
    assert "no improvement" in PROBLEM.statement.lower()


def test_problem_is_registered():
    from research.open_problems import get_problem

    assert get_problem("lifting") is PROBLEM


def test_families_are_named_and_unique():
    fams = all_families()
    assert len({fam.id for fam in fams}) == len(fams)
    assert len({fam.poly.render() for fam in fams}) == len(fams)
    for fam in fams:
        assert fam.note


def test_named_families_resolve():
    for fam_id in NONSINGULAR_IDS + SINGULAR_IDS:
        assert family(fam_id).poly.degree >= 2


def test_cap_v3_treats_zero_as_saturated():
    assert cap_v3(0, 3) == 3
    assert cap_v3(9, 3) == 2
    assert cap_v3(1, 3) == 0


# H1, H2, H3

def test_h1_identification_holds():
    rec = h1_identification(SAMPLE, k_max=6, word_depth=4)
    assert rec["ok"]
    assert rec["failures"] == []


def test_h2_taylor_jet_holds():
    rec = h2_taylor_jet(SAMPLE, word_depth=3)
    assert rec["ok"]
    assert rec["classification"] == "REPARAMETERIZATION"


def test_h3_trichotomy_holds_above_the_root():
    rec = h3_trichotomy(SAMPLE, k_max=5)
    assert rec["ok"]
    assert set(rec["child_count_census"]) <= {0, 1, 3}
    assert rec["classification"] == "KNOWN"


def test_h3_root_census_records_forbidden_counts():
    # The trichotomy is a statement about levels above the root; level 0
    # really does produce counts of 2.
    rec = h3_trichotomy(all_polys(), k_max=3)
    assert 2 in rec["level_zero_census"]


# H4

@pytest.mark.parametrize("r", (1, 2, 3))
def test_phi_r_determines_the_depth_r_subtree(r):
    rec = phi_determinacy(SAMPLE, k_max=5, r=r)
    assert rec["ok"]
    assert rec["violations"] == 0


@pytest.mark.parametrize("r", (2, 3))
def test_phi_r_is_sharp(r):
    rec = phi_sharpness(all_polys(), k_max=4, r=r)
    assert rec["ok"]
    assert rec["separation"] is not None


@pytest.mark.parametrize("r", (2, 3))
def test_valuations_are_insufficient_in_the_shallow_regime(r):
    rec = valuation_determinacy(all_polys(), k_max=4, r=r, regime="shallow")
    assert not rec["determined"]
    assert rec["separation"] is not None


@pytest.mark.parametrize("r", (1, 2, 3))
def test_valuations_suffice_in_the_deep_regime(r):
    rec = valuation_determinacy(all_polys(), k_max=5, r=r, regime="deep")
    assert rec["determined"]


@pytest.mark.parametrize("r", (1, 2, 3))
def test_pair_of_residues_determines_the_deep_subtree(r):
    rec = pair_determinacy(all_polys(), k_max=5, r=r, regime="deep")
    assert rec["determined"]


@pytest.mark.parametrize("r", (1, 2, 3))
def test_deep_linearization(r):
    rec = linearization(all_polys(), k_max=5, r=r)
    assert rec["ok"]
    assert rec["checked"] > 0


@pytest.mark.parametrize("r", (1, 2, 3))
def test_linear_states_are_valuation_determined(r):
    rec = linear_state_determinacy(r, c_bound=40, b_bound=27)
    assert rec["determined"]
    assert rec["witness"] is None


def test_linear_states_are_not_digit_determined_by_valuations():
    rec = linear_state_determinacy(3, c_bound=40, b_bound=27, mode="digits")
    assert not rec["determined"]
    assert rec["witness"] is not None


@pytest.mark.parametrize("r", (1, 2, 3, 4))
def test_unordered_shape_formula_on_complete_residues(r):
    rec = unordered_shape_census(r)
    assert rec["formula_holds"]
    assert rec["determined"]
    assert rec["formula_mismatches"] == 0
    assert rec["states"] == 3 ** (2 * r)


def test_state_census_is_bounded_in_k():
    census = state_census(all_polys(), k_max=6, r=2)
    deep = [row["distinct_subtrees"] for row in census["rows"] if row["level"] >= 2]
    assert max(deep) <= 3 * min(deep)


def test_triage_report_proceeds():
    rep = triage_report(k_max=4, r_max=2)
    assert rep["proceed"]
    verdict = rep["verdict"]
    assert verdict["h1"] and verdict["h2"] and verdict["h3"]
    assert verdict["phi_determinacy"] and verdict["phi_sharp"]
    assert verdict["deep_linearization"]
    assert verdict["deep_valuation_determinacy"]
    assert verdict["shallow_valuation_insufficient"]
