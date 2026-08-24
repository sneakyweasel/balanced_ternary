"""Smoke tests for the documented package façades."""

from __future__ import annotations

from balanced_ternary import decode, digit_derivative, encode, lsd_digit, polynomial
from balanced_ternary.cli import main as shim_main
from cli.main import main
from collatz import (
    AffineCenterState,
    CompatibilityState,
    InfiniteTrajectoryAffineState,
    candidate_cycle,
    collatz_step,
)


def test_balanced_ternary_root_round_trip():
    word = encode(42)
    assert decode(word) == 42


def test_cli_shim_is_canonical_entry():
    assert shim_main is main


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
    rec = candidate_cycle((2,))
    assert rec.is_exact_cycle
    assert lsd_digit(5) + 3 * digit_derivative(5) == 5
    assert polynomial(13).evaluate(3) == 13
