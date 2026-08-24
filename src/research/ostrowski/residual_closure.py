"""Reachable live residual states for the fixed order-3 Γ.

A state at remaining length ``i`` is live when its unread-tail value
lies between the digit-alphabet min and max. Live BFS from (0,0,0) is
the accepting-computation graph. Finite depth is not a proof.
"""

from __future__ import annotations

from collections import deque

from research.ostrowski.residual import CarryState, residual_integer, zero_state
from research.ostrowski.system import phase0_order3
from research.ostrowski.transition_extremals import (
    State3,
    legal_w,
    order3_transition,
    residual_is_live,
    unread_tail_bounds,
)

StatePos = tuple[State3, int]

# Live residual vectors reachable from (0,0,0) under legal w. Explicit
# finite set: the candidate B_min. Invariance is proved by the exterior
# deadness certificate in invariant_search, not by this listing alone.
B_MIN: frozenset[State3] = frozenset(
    (
        (-2, -3, -1),
        (-2, -3, 0),
        (-2, -2, -1),
        (-2, -2, 0),
        (-2, -2, 1),
        (-2, -1, -1),
        (-2, -1, 0),
        (-2, -1, 1),
        (-1, -3, -1),
        (-1, -3, 0),
        (-1, -3, 1),
        (-1, -2, -1),
        (-1, -2, 0),
        (-1, -2, 1),
        (-1, -2, 2),
        (-1, -1, -2),
        (-1, -1, -1),
        (-1, -1, 0),
        (-1, -1, 1),
        (-1, 0, -2),
        (-1, 0, -1),
        (-1, 0, 0),
        (-1, 0, 1),
        (0, -2, -1),
        (0, -2, 0),
        (0, -2, 1),
        (0, -2, 2),
        (0, -1, -2),
        (0, -1, -1),
        (0, -1, 0),
        (0, -1, 1),
        (0, 0, -2),
        (0, 0, -1),
        (0, 0, 0),
        (0, 0, 1),
        (0, 1, -2),
        (0, 1, -1),
        (0, 1, 0),
        (0, 2, -1),
        (0, 2, 0),
        (1, -1, -2),
        (1, -1, -1),
        (1, -1, 0),
        (1, -1, 1),
        (1, 0, -2),
        (1, 0, -1),
        (1, 0, 0),
        (1, 0, 1),
        (1, 1, -2),
        (1, 1, -1),
        (1, 1, 0),
        (1, 2, -1),
        (1, 2, 0),
        (2, 1, 0),
        (2, 2, 0),
    )
)


def as_state3(state: CarryState) -> State3:
    if len(state) != 3:
        raise ValueError("order-3 state required")
    return (int(state[0]), int(state[1]), int(state[2]))


def reachable_live(
    max_length: int,
) -> dict[str, object]:
    """Live MSD BFS from (0,0,0) with remaining length ``max_length``.

    At remaining ``i`` the consumed digit is ``w_{i-1}``, so the alphabet
    is ``legal_w(i-1)``.
    """
    start: State3 = (0, 0, 0)
    if not residual_is_live(start, max_length):
        return {
            "max_length": max_length,
            "state_count": 0,
            "positioned_count": 0,
            "live_start": False,
        }
    seen: set[StatePos] = {(start, max_length)}
    states: set[State3] = {start}
    queue: deque[StatePos] = deque([(start, max_length)])
    dead_images = 0
    abs_s3_ge3 = 0
    max_abs = [0, 0, 0]
    accepting = 0
    while queue:
        state, i = queue.popleft()
        for k in range(3):
            max_abs[k] = max(max_abs[k], abs(state[k]))
        if abs(state[2]) >= 3:
            abs_s3_ge3 += 1
        if i == 0:
            if state[2] == 0:
                accepting += 1
            continue
        for w in legal_w(i - 1):
            nxt = order3_transition(state, w)
            if not residual_is_live(nxt, i - 1):
                dead_images += 1
                continue
            key = (nxt, i - 1)
            if key not in seen:
                seen.add(key)
                states.add(nxt)
                queue.append(key)
    boundary = [
        s
        for s in states
        if abs(s[0]) == max_abs[0] or abs(s[1]) == max_abs[1] or abs(s[2]) == max_abs[2]
    ]
    return {
        "max_length": max_length,
        "raw_residual_states": len(states),
        "reachable_residual_states": len(states),
        "positioned_count": len(seen),
        "accepted_terminal": accepting,
        "max_abs_s1": max_abs[0],
        "max_abs_s2": max_abs[1],
        "max_abs_s3": max_abs[2],
        "states_with_abs_s3_ge_3": abs_s3_ge3,
        "dead_images": dead_images,
        "boundary_count": len(boundary),
        "states": frozenset(states),
        "live_start": True,
    }


def homogeneous_live(steps: int, remaining: int) -> dict[str, object]:
    """Position-independent live BFS using the interior alphabet.

    ``remaining`` is a large fixed unread length used only to test liveness
    of the integer residual against that length's tail bounds.
    """
    start: State3 = (0, 0, 0)
    seen: set[State3] = {start}
    queue: deque[tuple[State3, int]] = deque([(start, 0)])
    dead_images = 0
    max_abs = [0, 0, 0]
    overflow_s3 = 0
    while queue:
        state, depth = queue.popleft()
        for k in range(3):
            max_abs[k] = max(max_abs[k], abs(state[k]))
        if abs(state[2]) >= 3:
            overflow_s3 += 1
        if depth >= steps:
            continue
        for w in legal_w(1):
            nxt = order3_transition(state, w)
            if not residual_is_live(nxt, remaining):
                dead_images += 1
                continue
            if nxt not in seen:
                seen.add(nxt)
                queue.append((nxt, depth + 1))
    return {
        "steps": steps,
        "remaining": remaining,
        "state_count": len(seen),
        "max_abs_s1": max_abs[0],
        "max_abs_s2": max_abs[1],
        "max_abs_s3": max_abs[2],
        "states_with_abs_s3_ge_3": overflow_s3,
        "dead_images": dead_images,
        "states": frozenset(seen),
    }


def axis_box(a: int, b: int, c: int) -> frozenset[State3]:
    return frozenset(
        (x, y, z)
        for x in range(-a, a + 1)
        for y in range(-b, b + 1)
        for z in range(-c, c + 1)
    )


def closure_report(max_length: int = 10) -> dict[str, object]:
    live = reachable_live(max_length)
    sys = phase0_order3()
    lo, hi = unread_tail_bounds(max_length)
    return {
        "max_length": max_length,
        "q": sys.place_values(max_length),
        "tail_bounds": (lo, hi),
        "E0_live": residual_integer(sys, zero_state(3), max_length),
        **{k: live[k] for k in live if k != "states"},
        "states": live["states"],
    }
