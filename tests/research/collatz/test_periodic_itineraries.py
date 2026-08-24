"""Periodic itinerary compatibility."""

from __future__ import annotations

from research.collatz.periodic_itineraries import (
    eventually_periodic_realizer,
    periodic_candidate,
    preimage_along,
    search_periodic,
)


def test_one_cycle():
    cand = periodic_candidate((2,))
    assert cand.compatible
    assert cand.n == 1
    assert cand.gap == 1  # 4-3


def test_two_twos_is_still_one():
    cand = periodic_candidate((2, 2))
    assert cand.compatible
    assert cand.n == 1


def test_expanding_period_rejected():
    cand = periodic_candidate((1,))
    assert not cand.compatible
    assert cand.n is None
    assert "expanding" in cand.reason


def test_all_ones_not_a_cycle():
    cand = periodic_candidate((1, 1, 1, 1))
    assert not cand.compatible


def test_search_finds_only_powers_of_the_two_cycle():
    found = search_periodic(max_length=3, k_max=3)
    ns = {c.n for c in found}
    assert ns == {1}
    assert all(all(k == 2 for k in c.ks) for c in found)


def test_preimage_along_empty_is_identity():
    assert preimage_along((), 1) == 1
    assert preimage_along((), 5) == 5


def test_eventually_periodic_from_empty():
    cand = eventually_periodic_realizer((), (2,))
    assert cand.compatible
    assert cand.n == 1


def test_eventually_periodic_preimage_of_one_cycle():
    cand = eventually_periodic_realizer((4,), (2,))
    assert cand.compatible
    assert cand.n == 5
