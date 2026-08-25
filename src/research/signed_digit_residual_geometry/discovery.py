"""Origin-reachable geometry of ``F_{λ,U}`` inside a known finite envelope.

Reuses ``signed_step``. Does not reopen the finite/infinite phase law.
"""

from __future__ import annotations

from collections.abc import Sequence

from research.signed_digit_residual.discovery import (
    alphabet_m,
    lambda1_reachable_radius,
    lambda2_reachable_radius,
    mealy_count,
    reachable_from,
    signed_step,
    smallest_invariant_radius,
)

PROBES: tuple[tuple[int, ...], ...] = (
    (2,),
    (-2, 0, 2),
    (0, 1, 2),
    (-1, 0, 2),
)


def lattice_in_box(gain: int, lo: int, hi: int) -> tuple[int, ...]:
    return tuple(state for state in range(lo, hi + 1) if state % gain == 0)


def predicted_symmetric(gain: int, bound: int) -> tuple[int, ...]:
    if gain == 1:
        radius = lambda1_reachable_radius(bound)
        return tuple(range(-radius, radius + 1))
    if gain == 2:
        radius = lambda2_reachable_radius(bound)
        return tuple(range(-radius, radius + 1, 2))
    if gain >= 3 and bound <= 1:
        return (0,)
    raise ValueError("prediction is only for the known finite regimes")


def lambda1_climb(target: int) -> int:
    """Explicit word ``u=2,4,...,2|t|`` reaches ``t`` at ``λ=1``."""
    state = 0
    sign = 1 if target >= 0 else -1
    for step in range(1, abs(target) + 1):
        state, _out = signed_step(state, sign * 2 * step, 1)
    return state


def lambda2_even_climb(half: int) -> int:
    """Explicit word ``u=2,3,...,|h|+1`` reaches ``2h`` at ``λ=2``."""
    state = 0
    sign = 1 if half >= 0 else -1
    for step in range(abs(half)):
        state, _out = signed_step(state, sign * (step + 2), 2)
    return state


def geometry_report(gain: int, bound: int) -> dict[str, object]:
    alphabet = alphabet_m(bound)
    reached = reachable_from(0, alphabet, gain)
    assert reached is not None
    states = tuple(sorted(reached))
    box = smallest_invariant_radius(alphabet, gain)
    assert box is not None
    predicted = predicted_symmetric(gain, bound)
    missing = tuple(state for state in predicted if state not in reached)
    extra = tuple(state for state in states if state not in predicted)
    return {
        "gain": gain,
        "m": bound,
        "alphabet": alphabet,
        "invariant_radius": box,
        "reachable": states,
        "predicted_lattice_box": predicted,
        "missing": missing,
        "extra": extra,
        "matches_lattice_box": not missing and not extra,
        "gcd": 0 if not states else abs(states[0]) if len(states) == 1 else _gcd_all(states),
        "symmetric": states == tuple(-s for s in reversed(states)),
        "mealy": mealy_count(states, alphabet, gain),
        "reachable_count": len(states),
    }


def _gcd_all(values: Sequence[int]) -> int:
    acc = 0
    for value in values:
        acc = _gcd(acc, abs(int(value)))
    return acc


def _gcd(left: int, right: int) -> int:
    while right:
        left, right = right, left % right
    return left


def probe_report(alphabet: Sequence[int], gain: int) -> dict[str, object]:
    letters = tuple(int(letter) for letter in alphabet)
    reached = reachable_from(0, letters, gain)
    assert reached is not None
    states = tuple(sorted(reached))
    box = smallest_invariant_radius(letters, gain)
    assert box is not None
    predicted = lattice_in_box(gain, -box, box)
    missing = tuple(state for state in predicted if state not in reached)
    return {
        "alphabet": letters,
        "gain": gain,
        "invariant_radius": box,
        "reachable": states,
        "predicted_lattice_box": predicted,
        "missing": missing,
        "matches_lattice_box": not missing and states == predicted,
        "mealy": mealy_count(states, letters, gain),
        "reachable_count": len(states),
    }


def singleton_two_witness() -> dict[str, object]:
    """Smallest lattice-box failure: ``U={2}`` at ``λ=1`` misses ``-1``."""
    return probe_report((2,), 1)


def sign_symmetry_halves_mealy(gain: int, bound: int) -> bool:
    report = geometry_report(gain, bound)
    return report["mealy"] * 2 == report["reachable_count"] and report["reachable_count"] > 1
