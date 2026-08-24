"""Identity discovery never auto-promotes to EXACT — HUMAN PROOF."""

from __future__ import annotations

from bt.calculus.discovery import discover_closed
from bt.calculus.locality import all_profiles, profile


def test_discover_closed_labels():
    hits = discover_closed(max_depth=2, seed=5)
    assert hits
    for cand in hits:
        assert cand.status in {
            "COMPUTATIONALLY VERIFIED",
            "CONJECTURE",
            "REFUTED",
        }
        assert "sorry" in cand.lean_skeleton
        assert "FORBIDDEN" in cand.lean_skeleton


def test_profiles_reuse_existing_classification():
    d = profile("D")
    assert d.locality_class == "sequential"
    assert d.state_complexity == 1
    w = profile("W")
    assert "not one-way sequential" in w.locality_class
    odd = profile("odd_part")
    assert "not one rational" in odd.locality_class
    t = profile("T")
    assert "composition" in t.locality_class
    names = {p.operator for p in all_profiles()}
    assert "D" in names and "odd_part" in names and "T" in names
