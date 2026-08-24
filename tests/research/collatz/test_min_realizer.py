"""Minimum realizers and nested R."""

from __future__ import annotations

from research.collatz.compatibility import child_realizer_delta, nested_cylinder_report
from research.collatz.core import collatz_valuation
from research.collatz.cylinders import belongs_to_cylinder, valuation_cylinder
from research.collatz.min_realizer import (
    count_cylinder_up_to,
    itinerary_signature,
    min_realizer,
    nested_realizers,
)


def test_known_residues_are_min_realizers():
    assert min_realizer(()) == 1
    assert min_realizer((1,)) == 3
    assert min_realizer((2,)) == 1
    assert min_realizer((1, 1)) == 7
    assert belongs_to_cylinder(3, (1,))
    assert collatz_valuation(3) == 1


def test_count_matches_scan():
    ks = (1, 2)
    x = 200
    r = min_realizer(ks)
    mod = 1 << (sum(ks) + 1)
    brute = sum(1 for n in range(1, x + 1, 2) if n % mod == r)
    assert count_cylinder_up_to(ks, x) == brute


def test_nested_r_monotone():
    ks = (1, 2, 1, 3)
    rs = nested_realizers(ks)
    assert rs[0] == 1
    for a, b in zip(rs, rs[1:]):
        assert a <= b
    report = nested_cylinder_report(ks)
    assert report.monotone


def test_child_is_lift():
    r_p, r_c, t = child_realizer_delta((1, 1), 2)
    assert t >= 0
    assert r_c == r_p + t * (1 << (2 + 1))  # K_parent=2, mod=2^{3}=8
    assert r_c >= r_p


def test_signature_bt_odd_weight():
    sig = itinerary_signature((1, 2, 1))
    assert sig.R == sig.residue
    assert sig.features.weight_parity == 1
    assert sig.positivity_threshold == 1


def test_low_K_caps_R_at_fixed_length():
    """H1 at fixed m is false as a 'larger R' claim: R < 2^{K+1}."""
    from itertools import product

    expanding = []
    contracting = []
    for ks in product(range(1, 4), repeat=3):
        r = min_realizer(ks)
        k_sum = sum(ks)
        assert r < (1 << (k_sum + 1))
        if k_sum == 3:
            expanding.append(r)
        if k_sum >= 6:
            contracting.append(r)
    assert expanding
    assert contracting
    assert max(expanding) < max(contracting)
