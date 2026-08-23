"""Phase-0 tests for finite-context misere signatures."""

from __future__ import annotations

from research.misere_quotients.problem import PROBLEM
from research.misere_quotients.reference import (
    DAWSON_Q_CHECKPOINTS,
    Q123_ELEMENTS,
    Q123_P,
    q123_heap_phi,
    q123_multiply,
    q123_position_phi,
)
from research.misere_quotients.triage import (
    add_positions,
    bounded_positions,
    candidate_quotient,
    canonicalize,
    class_count,
    dawson_single_heap_check,
    distinguish,
    misere_outcome,
    options,
    q123_class_recovery,
    q123_monoid_self_check,
    q123_outcome_agreement,
    triage_report,
)


def test_problem_is_registered():
    from research.open_problems import get_problem

    assert get_problem("misere_quotients") is PROBLEM
    assert PROBLEM.status == "ARCHIVED"
    assert PROBLEM.docs == ("docs/problems/misere_quotients.md",)


def test_empty_and_dead_heaps_are_misere_N():
    assert options("0.123", ()) == ()
    assert misere_outcome("0.123", ()) == "N"
    assert options("0.123", (2,)) == ()
    assert misere_outcome("0.123", (2,)) == "N"
    assert options("0.07", (1,)) == ()
    assert misere_outcome("0.07", (1,)) == "N"
    assert misere_outcome("0.07", ()) == "N"


def test_0123_moves_match_plambeck_rules():
    assert set(options("0.123", (1,))) == {()}
    assert set(options("0.123", (3,))) == {(), (1,)}
    assert set(options("0.123", (4,))) == {(1,), (2,)}
    assert set(options("0.123", (1, 3))) == {(3,), (1, 1), (1,)}


def test_dawson_kayles_removes_two_adjacent():
    assert set(options("0.07", (2,))) == {()}
    assert set(options("0.07", (3,))) == {(1,)}
    assert set(options("0.07", (4,))) == {(2,), (1, 1)}
    assert set(options("0.07", (5,))) == {(3,), (1, 2)}


def test_canonicalize_and_disjunctive_sum():
    assert canonicalize((5, 0, 1, 3, 1)) == (1, 1, 3, 5)
    assert add_positions((1, 3), (1, 5)) == (1, 1, 3, 5)


def test_0123_published_outcomes_on_small_positions():
    assert misere_outcome("0.123", (1,)) == "P"
    assert misere_outcome("0.123", (5,)) == "P"
    assert misere_outcome("0.123", (3,)) == "N"
    assert misere_outcome("0.123", (1, 1)) == "N"
    assert q123_heap_phi(1) == "x"
    assert q123_heap_phi(6) == "b2"
    assert q123_heap_phi(8) == "a"
    assert q123_heap_phi(11) == "b2"
    assert q123_position_phi((1, 3, 4, 8, 9)) == q123_multiply(
        q123_multiply(q123_multiply(q123_multiply("x", "z"), "z"), "a"), "b"
    )


def test_published_0123_monoid_is_the_twenty_element_table():
    report = q123_monoid_self_check()
    assert report["order"] == 20
    assert report["p_size"] == 5
    assert report["relations_hold"]
    assert report["commutative"]
    assert set(Q123_P) <= set(Q123_ELEMENTS)


def test_finite_context_signature_is_not_the_true_quotient():
    universe = bounded_positions(8, 3, 12)
    empty_only = class_count("0.123", universe, ((),))
    heaps = class_count("0.123", universe, ((),) + tuple((n,) for n in range(1, 9)))
    richer = class_count("0.123", universe, bounded_positions(8, 3, 8))
    assert empty_only == 2
    assert heaps > empty_only
    assert richer >= heaps


def test_distinguish_finds_a_minimal_context():
    universe = bounded_positions(8, 3, 10)
    # (1,) = x and (6,) = b^2 are distinct published P-classes.
    assert q123_heap_phi(1) == "x"
    assert q123_heap_phi(6) == "b2"
    witness = distinguish("0.123", (1,), (6,), universe)
    assert witness is not None
    assert misere_outcome("0.123", add_positions((1,), witness)) != misere_outcome(
        "0.123", add_positions((6,), witness)
    )
    assert distinguish("0.123", (1,), (1,), universe) is None
    assert distinguish("0.123", (1,), (5,), universe) is None


def test_candidate_quotient_audit_is_well_defined_on_represented_products():
    universe = bounded_positions(6, 3, 10)
    contexts = bounded_positions(6, 3, 8)
    audit = candidate_quotient("0.123", universe, contexts)
    assert audit["classes"] >= 2
    assert audit["well_defined_on_represented_products"]
    assert audit["identity_acts"]
    assert audit["unresolved_products"] >= 0


def test_0123_finite_contexts_recover_published_classes_on_the_phase0_slice():
    universe = bounded_positions(12, 4, 18)
    contexts = bounded_positions(12, 4, 10)
    outcomes = q123_outcome_agreement(universe)
    recovery = q123_class_recovery(universe, contexts)
    assert outcomes["agrees"]
    assert recovery["recovers_published_classes"]
    assert recovery["missing_witnesses"] == 0
    assert recovery["finite_context_classes"] == recovery["published_elements_seen"]


def test_dawson_single_heaps_match_published_q33_phi_outcomes():
    report = dawson_single_heap_check(12)
    assert report["agrees"]
    assert 2 in report["p_heaps"]
    assert 3 in report["p_heaps"]
    assert 0 not in report["p_heaps"]
    assert DAWSON_Q_CHECKPOINTS[-1] == (33, 638)


def test_triage_report_closes_as_reparameterization():
    report = triage_report()
    assert report["gate"] == "CLOSE"
    assert report["classification"] == "REPARAMETERIZATION"
    assert report["same_as_published_algorithm"]
    assert report["q123"]["outcome_agreement"]["agrees"]
    assert report["q123"]["recovery"]["recovers_published_classes"]
    assert report["dawson"]["single_heap"]["agrees"]
    assert report["dawson"]["finite_context_boundary"]["q34_attempted"] is False
    assert report["method_transfer"]["bt_arithmetic_used"] is False
