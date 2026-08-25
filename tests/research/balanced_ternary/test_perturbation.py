"""Carry-gain family: λ=1,2 finite; λ=3 unbounded. λ≠1 is synthetic."""

from __future__ import annotations

from research.balanced_ternary.perturbation import (
    family_fingerprint,
    is_plus_one_unbounded_witness,
    plus_one_orbit,
    reachable_box,
)
from research.balanced_ternary.planner import plan_gain
from research_engine.attacks.result import AttackStatus
from research_engine.core.semantics import SearchScope


def test_gain_one_and_two_are_finite():
    box1 = reachable_box(1)
    box2 = reachable_box(2)
    assert box1 == frozenset({(-1,), (0,), (1,)})
    assert box2 == frozenset({(-2,), (0,), (2,)})
    report1 = plan_gain(1, remaining=4)
    closure1 = next(item for item in report1.results if item.name == "closure")
    assert closure1.status is AttackStatus.SUPPORTED
    assert closure1.scope is SearchScope.EXACT
    report2 = plan_gain(2, remaining=4)
    closure2 = next(item for item in report2.results if item.name == "closure")
    assert closure2.status is AttackStatus.SUPPORTED
    assert closure2.evidence["union_size"] == 3


def test_gain_three_is_unbounded_along_plus_one():
    orbit = plus_one_orbit(3, 6)
    assert [state[0] for state in orbit] == [0, 3, 6, 9, 12, 15, 18]
    assert is_plus_one_unbounded_witness(3)
    assert reachable_box(3, cap=8) is None
    report = plan_gain(3, remaining=4)
    closure = next(item for item in report.results if item.name == "closure")
    assert closure.status is AttackStatus.INCONCLUSIVE
    assert closure.scope is SearchScope.BOUNDED
    affine = next(item for item in report.results if item.name == "affine")
    assert affine.status is AttackStatus.REFUTED


def test_family_fingerprint_labels_synthetic_gains():
    family = family_fingerprint()
    assert family[1]["value_preserving"] is True
    assert family[2]["value_preserving"] is False
    assert family[3]["value_preserving"] is False
    assert family[1]["finite"] is True
    assert family[2]["finite"] is True
    assert family[3]["finite"] is False
    assert family[3]["unbounded_witness"] is True
