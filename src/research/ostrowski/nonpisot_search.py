"""Live growth and exact hub lemmas for the non-Pisot comparison system.

Finite-depth growth is not a theorem. The hub ``(-3, -1, 0)`` is live at
every remaining length (integer inequalities) and is reached from
``(0,0,0)`` at remaining ``2m`` by the prefix ``(1, -2)``. An explicit
unbounded live family is not claimed.
"""

from __future__ import annotations

from research.ostrowski.live_growth import (
    legal_w,
    reachable_live,
    residual_is_live,
    transition_affine,
    unread_tail_bounds,
)
from research.ostrowski.spectral_residual import residual_matrix
from research.ostrowski.system import OstrowskiSystem, nonpisot_order3

State3 = tuple[int, int, int]

HUB: State3 = (-3, -1, 0)
HUB_PREFIX: tuple[int, int] = (1, -2)


def l1(state: State3) -> int:
    return abs(state[0]) + abs(state[1]) + abs(state[2])


def place_sum(system: OstrowskiSystem, i: int) -> int:
    """``S_i = sum_{j=0}^{i} q_j``, or 0 if ``i < 0``."""
    if i < 0:
        return 0
    return sum(system.place_values(i + 1))


def hub_live_certificate(system: OstrowskiSystem, remaining: int) -> bool:
    """Exact liveness of ``HUB`` at ``remaining``.

    For ``i >= 2``, ``E = -3 q_{i-2} - q_{i-1} < 0 <= hi``, and
    ``E - lo = 4 S_{i-1} - 3 q_{i-2} - q_{i-1} - 2`` is positive because
    ``S_{i-1} >= q_{i-1} + q_{i-2} + 1`` when ``i >= 3``. Direct check for
    ``i < 3``.
    """
    if remaining < 0:
        raise ValueError("remaining must be nonnegative")
    if remaining <= 2:
        return residual_is_live(system, HUB, remaining)
    qs = system.place_values(remaining)
    q_im2 = qs[remaining - 2]
    q_im1 = qs[remaining - 1]
    s_im1 = place_sum(system, remaining - 1)
    energy = -3 * q_im2 - q_im1
    lo, hi = unread_tail_bounds(system, remaining)
    lower_gap = 4 * s_im1 - 3 * q_im2 - q_im1 - 2
    return energy <= hi and lower_gap >= 0 and lo <= energy <= hi


def hub_reachable_at_even_remaining(remaining: int, system: OstrowskiSystem | None = None) -> bool:
    """Prefix ``(1, -2)`` from remaining ``remaining+2`` lands on the hub."""
    if remaining < 0 or remaining % 2 != 0:
        raise ValueError("remaining must be a nonnegative even integer")
    sys = system or nonpisot_order3()
    start_rem = remaining + 2
    s: State3 = (0, 0, 0)
    if not residual_is_live(sys, s, start_rem):
        return False
    s = transition_affine(sys, s, HUB_PREFIX[0])
    if not residual_is_live(sys, s, start_rem - 1):
        return False
    s = transition_affine(sys, s, HUB_PREFIX[1])
    return s == HUB and residual_is_live(sys, s, remaining)


def greedy_live_growth(
    system: OstrowskiSystem,
    max_length: int,
) -> dict[str, object]:
    """From ``(0,0,0)``, at each step keep a live image of maximal ``l1``."""
    state: State3 = (0, 0, 0)
    path = [state]
    norms = [0]
    for remaining in range(max_length, 0, -1):
        best: State3 | None = None
        best_norm = -1
        for w in legal_w(system, remaining - 1):
            nxt = transition_affine(system, state, w)
            if not residual_is_live(system, nxt, remaining - 1):
                continue
            nrm = l1(nxt)
            if nrm > best_norm:
                best_norm = nrm
                best = nxt
        if best is None:
            return {
                "max_length": max_length,
                "died_at_remaining": remaining,
                "path": tuple(path),
                "norms": tuple(norms),
                "max_l1": max(norms),
                "completed": False,
            }
        state = best
        path.append(state)
        norms.append(best_norm)
    return {
        "max_length": max_length,
        "died_at_remaining": None,
        "path": tuple(path),
        "norms": tuple(norms),
        "max_l1": max(norms),
        "completed": True,
        "terminal": state,
        "accepting": state[2] == 0,
    }


def live_maxima(system: OstrowskiSystem, max_length: int) -> dict[str, object]:
    report = reachable_live(system, max_length)
    states: frozenset[State3] = report["states"]  # type: ignore[assignment]
    if not states:
        return {"max_length": max_length, "empty": True}
    by_l1 = max(states, key=l1)
    return {
        "max_length": max_length,
        "live_states": len(states),
        "max_l1": l1(by_l1),
        "argmax_l1": by_l1,
        "max_abs": (
            max(abs(s[0]) for s in states),
            max(abs(s[1]) for s in states),
            max(abs(s[2]) for s in states),
        ),
        "matrix": residual_matrix(system),
    }


def comparison_scan(
    pisot_system: OstrowskiSystem,
    nonpisot_system: OstrowskiSystem,
    max_depth: int,
) -> dict[str, object]:
    """Side-by-side live growth. Finite depth is not infinitude."""
    from research.ostrowski.live_growth import growth_table

    return {
        "pisot": growth_table(pisot_system, max_depth),
        "nonpisot": growth_table(nonpisot_system, max_depth),
        "max_depth": max_depth,
        "finite_depth_is_not_infinitude": True,
    }
