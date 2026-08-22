"""Smoke tests for the documented package façades."""

from __future__ import annotations

from balanced_ternary import decode, encode
from collatz import AffineCenterState, CompatibilityState, InfiniteTrajectoryAffineState, collatz_step


def test_balanced_ternary_root_round_trip():
    word = encode(42)
    assert decode(word) == 42


def test_collatz_root_exact_objects():
    assert collatz_step(27) == 41
    state = CompatibilityState.from_valuations((1, 4, 2))
    center = AffineCenterState.from_valuations((1, 4, 2))
    assert state.R == center.R
    assert state.M == center.M
    assert center.validates()
    fixed = InfiniteTrajectoryAffineState.prefix(27, 3)
    assert fixed.validates()
    assert fixed.n == 27
