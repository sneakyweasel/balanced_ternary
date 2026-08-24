"""System-parameterized unread-tail alphabets, liveness, and live BFS.

Memoryless per-position difference alphabets, matching the previous
milestone: digits from Baranwal §5.3 rules 1–2, not rule 3. For the
Pisot/non-Pisot comparison pair both have ``d_1=2``, so the alphabets
agree. Finite depth is not a proof of infinitude.
"""

from __future__ import annotations

from collections import deque
from functools import lru_cache

from research.ostrowski.residual import residual_integer
from research.ostrowski.spectral import constant_digits
from research.ostrowski.spectral_residual import transition_affine
from research.ostrowski.system import OstrowskiSystem

State3 = tuple[int, int, int]
StatePos = tuple[State3, int]


def lsd_digit_max(system: OstrowskiSystem) -> int:
    """Largest legal ``a_0``: ``a_0 < d_{1,1}``."""
    return system.d(1, 1) - 1


def interior_digit_max(system: OstrowskiSystem, place: int) -> int:
    """Largest legal ``a_i`` at ``place = i >= 1``: ``a_i <= d_{1, i+1}``."""
    if place < 1:
        raise ValueError("interior place must be >= 1")
    return system.d(1, place + 1)


def difference_alphabet(digit_max: int) -> tuple[int, ...]:
    """``w = z-(x+y)`` for digits in ``{0, …, digit_max}``."""
    if digit_max < 0:
        raise ValueError("digit_max must be nonnegative")
    return tuple(range(-2 * digit_max, digit_max + 1))


def legal_w(system: OstrowskiSystem, place: int) -> tuple[int, ...]:
    """Memoryless difference alphabet at ``place`` (0 = LSD)."""
    if place < 0:
        raise ValueError("place must be nonnegative")
    if place == 0:
        return difference_alphabet(lsd_digit_max(system))
    return difference_alphabet(interior_digit_max(system, place))


@lru_cache(maxsize=None)
def unread_tail_bounds(system: OstrowskiSystem, remaining: int) -> tuple[int, int]:
    """Min and max of ``sum_{j<remaining} w_j q_j`` over memoryless difference words."""
    if remaining < 0:
        raise ValueError("remaining must be nonnegative")
    if remaining == 0:
        return (0, 0)
    qs = system.place_values(remaining)
    lo = hi = 0
    for j, q in enumerate(qs):
        alphabet = legal_w(system, j)
        lo += alphabet[0] * q
        hi += alphabet[-1] * q
    return (lo, hi)


def residual_is_live(system: OstrowskiSystem, state: State3, remaining: int) -> bool:
    lo, hi = unread_tail_bounds(system, remaining)
    return lo <= residual_integer(system, state, remaining) <= hi


def reachable_live(system: OstrowskiSystem, max_length: int) -> dict[str, object]:
    """Live MSD BFS from ``(0,0,0)`` with remaining length ``max_length``."""
    start: State3 = (0, 0, 0)
    if not residual_is_live(system, start, max_length):
        return {
            "max_length": max_length,
            "state_count": 0,
            "live_start": False,
        }
    seen: set[StatePos] = {(start, max_length)}
    states: set[State3] = {start}
    queue: deque[StatePos] = deque([(start, max_length)])
    new_at_depth: dict[int, int] = {max_length: 1}
    dead_images = 0
    max_abs = [0, 0, 0]
    max_norm = 0
    accepting = 0
    while queue:
        state, i = queue.popleft()
        for k in range(3):
            max_abs[k] = max(max_abs[k], abs(state[k]))
        max_norm = max(max_norm, abs(state[0]) + abs(state[1]) + abs(state[2]))
        if i == 0:
            if state[2] == 0:
                accepting += 1
            continue
        for w in legal_w(system, i - 1):
            nxt = transition_affine(system, state, w)
            if not residual_is_live(system, nxt, i - 1):
                dead_images += 1
                continue
            key = (nxt, i - 1)
            if key not in seen:
                seen.add(key)
                if nxt not in states:
                    states.add(nxt)
                    new_at_depth[i - 1] = new_at_depth.get(i - 1, 0) + 1
                queue.append(key)
    boundary = [
        s
        for s in states
        if abs(s[0]) == max_abs[0] or abs(s[1]) == max_abs[1] or abs(s[2]) == max_abs[2]
    ]
    return {
        "max_length": max_length,
        "raw_states": len(seen),
        "live_states": len(states),
        "new_live_states": new_at_depth,
        "max_abs_s1": max_abs[0],
        "max_abs_s2": max_abs[1],
        "max_abs_s3": max_abs[2],
        "max_l1": max_norm,
        "boundary_states": len(boundary),
        "accepting_states": accepting,
        "dead_images": dead_images,
        "states": frozenset(states),
        "live_start": True,
        "digits": constant_digits(system),
    }


def growth_table(system: OstrowskiSystem, max_depth: int) -> list[dict[str, object]]:
    """Live-closure scan by remaining length. Finite depth is not infinitude."""
    if max_depth < 1:
        raise ValueError("max_depth must be >= 1")
    rows: list[dict[str, object]] = []
    prev_live = 0
    for depth in range(1, max_depth + 1):
        report = reachable_live(system, depth)
        live = int(report.get("live_states", 0))
        rows.append(
            {
                "depth": depth,
                "raw_states": report.get("raw_states", 0),
                "live_states": live,
                "new_live_states": live - prev_live,
                "max_abs_s1": report.get("max_abs_s1", 0),
                "max_abs_s2": report.get("max_abs_s2", 0),
                "max_abs_s3": report.get("max_abs_s3", 0),
                "max_l1": report.get("max_l1", 0),
                "boundary_states": report.get("boundary_states", 0),
                "accepting_states": report.get("accepting_states", 0),
            }
        )
        prev_live = live
    return rows
