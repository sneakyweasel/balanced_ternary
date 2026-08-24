"""Phase-0 tests for Erdős distinct subset sums."""

from __future__ import annotations

import pytest

from research.erdos_distinct_subset_sums.problem import PROBLEM
from research.erdos_distinct_subset_sums.triage import (
    A276661_PREFIX,
    CONWAY_GUY_A,
    FAST_N,
    MAX_N,
    a276661_extremal,
    all_signed_sums_distinct,
    balanced_relation_tree,
    bt_length,
    concentration_at_zero,
    conway_guy_a,
    conway_guy_set,
    is_sum_distinct,
    magnitude_length_bound,
    magnitude_valuation_bridge,
    mod_3k_relation_profile,
    powers_of_three,
    powers_of_two,
    relation_witness,
    signed_relations,
    signed_sum,
    signed_sum_histogram,
    triage_report,
    valuation_histogram,
    word_stats,
)


def test_problem_is_registered():
    from research.literature import get_reference
    from research.open_problems import get_problem

    assert get_problem("erdos_distinct_subset_sums") is PROBLEM
    assert PROBLEM.status == "EXPLORATORY"
    assert PROBLEM.docs == ("docs/problems/erdos_distinct_subset_sums.md",)
    assert get_reference("dubroff-fox-xu-2021")["year"] == 2021
    assert get_reference("bohman-1998-construction")["id"] == "bohman-1998-construction"
    assert get_reference("oeis-A276661")["identifiers"]["oeis"] == "A276661"
    assert get_reference("avizienis-1961-signed-digit")["year"] == 1961


def test_three_predicates_are_not_the_same():
    binary = (1, 2, 4)
    colliding = (1, 2, 3)

    assert is_sum_distinct(binary)
    assert concentration_at_zero(binary) == 1
    assert relation_witness(binary) is None
    assert not all_signed_sums_distinct(binary)
    assert signed_sum(binary, (1, 0, 1)) == signed_sum(binary, (-1, 1, 1)) == 5

    assert not is_sum_distinct(colliding)
    witness = relation_witness(colliding)
    assert witness in ((1, 1, -1), (-1, -1, 1))
    kernel = signed_relations(colliding)
    assert (0, 0, 0) in kernel
    assert (1, 1, -1) in kernel
    assert (-1, -1, 1) in kernel


def test_powers_of_three_are_sum_distinct_and_signed_distinct():
    A = powers_of_three(5)
    assert is_sum_distinct(A)
    assert all_signed_sums_distinct(A)
    assert max(A) > max(powers_of_two(5))


def test_conway_guy_matches_a005318():
    for n, expected in enumerate(CONWAY_GUY_A):
        assert conway_guy_a(n) == expected
    cg4 = conway_guy_set(4)
    assert cg4 == (3, 5, 6, 7)
    assert is_sum_distinct(cg4)
    assert max(a276661_extremal(4)) == A276661_PREFIX[4] == 7
    assert max(a276661_extremal(8)) == 84
    assert max(a276661_extremal(9)) == 161


def test_relation_tree_merges_by_partial_sum():
    tree = balanced_relation_tree((1, 2, 4))
    assert tree["R_j"][0] == 1
    assert tree["final_distinct_sums"] < tree["signed_space"]
    assert tree["all_signed_sums_distinct"] is False
    p3 = balanced_relation_tree(powers_of_three(4))
    assert p3["final_distinct_sums"] == 3**4
    assert p3["all_signed_sums_distinct"] is True


def test_modular_hits_are_labelled_modular_only():
    profile = mod_3k_relation_profile((1, 2, 4), 1)
    assert profile["label"] == "MODULAR ONLY"
    assert profile["exact_zero"] == 1
    assert profile["modular_only_kernel"] >= 1
    assert profile["injective"] is False


def test_magnitude_valuation_bridge_is_the_kernel():
    for A in ((1, 2, 4), (1, 2, 3), (3, 5, 6, 7), powers_of_two(5)):
        bridge = magnitude_valuation_bridge(A, 2)
        assert bridge["equals_kernel"] is True
        assert bridge["nonzero_forced_zero"] is True
        assert bridge["hit_count"] == concentration_at_zero(A)


def test_canonical_word_is_a_function_of_the_integer():
    for s in range(-40, 41):
        stats = word_stats(s)
        assert bt_length(s) == magnitude_length_bound(s)
        assert stats["length"] == bt_length(s)
        if s == 0:
            assert stats["v3"] is None
            assert stats["leading_trit"] == 0
        else:
            assert stats["leading_trit"] in (-1, 1)


def test_valuation_histogram_separates_exact_zero():
    hist = valuation_histogram((1, 2, 4))
    assert hist["exact_zero"] == 1
    assert "1" in hist
    assert signed_sum_histogram((1, 2, 3))[0] == 3


def test_triage_report_shape():
    report = triage_report(max_n=4, k=2)
    assert report["max_n"] == 4
    audit = report["audit"]
    assert audit["all_signed_sums_strictly_stronger"]
    assert audit["powers3_worse_than_powers2"]
    assert audit["length_is_magnitude_bound"]
    assert audit["high_v3_without_relation"]
    assert audit["bridge_equals_kernel_on_powers2"]
    assert audit["cannot_reproduce_dfx"]
    names = {row["name"] for row in report["rows"]}
    assert "binary_124" in names
    assert "relation_123" in names
    assert "conway_guy_n4" in names
    assert report["a276661_equals_conway_guy"]
    assert FAST_N == 7
    assert MAX_N == 12


@pytest.mark.slow
def test_phase0_constructions_through_n_twelve():
    from research.erdos_distinct_subset_sums.triage import construction_row

    audit = triage_report(max_n=FAST_N, k=2)["audit"]
    assert audit["powers3_all_signed_sums_distinct"]
    assert audit["high_v3_without_relation"]
    p2 = construction_row("powers2_n12", powers_of_two(12), k=2)
    cg = construction_row("conway_guy_n12", conway_guy_set(12), k=2)
    p3 = construction_row("powers3_n12", powers_of_three(12), k=2)
    assert p2["sum_distinct"]
    assert cg["sum_distinct"]
    assert p3["all_signed_sums_distinct"]
    assert p3["max"] > p2["max"]
    assert cg["max"] < p2["max"]
    assert p2["R_j"][-1] == 8191
    assert cg["R_j"][-1] == 16995
    assert p3["R_j"][-1] == 3**12
    assert p2["bridge"]["equals_kernel"]
    assert cg["bridge"]["equals_kernel"]
