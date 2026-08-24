"""Candidate invariant regions and the exterior deadness certificate.

``B_MIN`` is the explicit 55-element live reachable set. Every legal
image of ``B_MIN`` is either in ``B_MIN`` or dead for every remaining
length: overflow/underflow gaps obey linear recurrences, so four
initial exact gaps imply all later gaps stay positive.
"""

from __future__ import annotations

from research.ostrowski.residual import residual_integer
from research.ostrowski.residual_closure import B_MIN, State3, axis_box, reachable_live
from research.ostrowski.system import phase0_order3
from research.ostrowski.transition_extremals import (
    INTERIOR_W,
    LSD_W,
    legal_w,
    order3_transition,
    residual_is_live,
    unread_tail_bounds,
)


def candidate_box(a: int, b: int, c: int) -> frozenset[State3]:
    return axis_box(a, b, c)


def exterior_images(region: frozenset[State3] = B_MIN) -> frozenset[State3]:
    """One-step images of ``region`` that leave ``region``."""
    out: set[State3] = set()
    for state in region:
        for w in set(INTERIOR_W + LSD_W):
            nxt = order3_transition(state, w)
            if nxt not in region:
                out.add(nxt)
    return frozenset(out)


def verify_invariant(
    region: frozenset[State3],
    remaining: int,
) -> dict[str, object]:
    """Live images at this remaining length stay in ``region``."""
    if remaining < 1:
        raise ValueError("remaining must be >= 1")
    leaks: list[tuple[State3, int, State3]] = []
    dead_images = 0
    live_images = 0
    for state in region:
        for w in legal_w(remaining - 1):
            nxt = order3_transition(state, w)
            if not residual_is_live(nxt, remaining - 1):
                dead_images += 1
                continue
            live_images += 1
            if nxt not in region:
                leaks.append((state, w, nxt))
    return {
        "region_size": len(region),
        "remaining": remaining,
        "live_images": live_images,
        "dead_images": dead_images,
        "leak_count": len(leaks),
        "leaks_sample": leaks[:8],
        "invariant": not leaks,
    }


def _overflow_gap(state: State3, i: int) -> int:
    sys = phase0_order3()
    e = residual_integer(sys, state, i)
    _lo, hi = unread_tail_bounds(i)
    return e - hi


def _underflow_gap(state: State3, i: int) -> int:
    sys = phase0_order3()
    e = residual_integer(sys, state, i)
    lo, _hi = unread_tail_bounds(i)
    return lo - e


def classify_exterior(state: State3) -> str:
    """Overflow if E exceeds hi at i=0 (i.e. s3>0); underflow if s3<0.

    At remaining 0, live iff s3=0. Every exterior image has s3≠0.
    """
    if state[2] > 0:
        return "overflow"
    if state[2] < 0:
        return "underflow"
    # s3=0 but not in B: still may be live at i=0. Treat by first gap.
    if _overflow_gap(state, 3) > 0:
        return "overflow"
    return "underflow"


def deadness_certificate(
    region: frozenset[State3] = B_MIN,
) -> dict[str, object]:
    """Finite initial gaps plus recurrences ⇒ exterior images are never live.

    For i≥4:

    * overflow gap ``G_i = E_i − hi(i)`` satisfies
      ``G_i = 2 G_{i-1} + G_{i-2} + G_{i-3} − 5``;
    * underflow gap ``H_i = lo(i) − E_i`` satisfies
      ``H_i = 2 H_{i-1} + H_{i-2} + H_{i-3} − 10``.

    Checking ``G_0,…,G_3 ≥ 1`` (resp. ``H ≥ 2``) on every exterior
    image therefore implies all later gaps stay positive.
    """
    ext = exterior_images(region)
    overflow: list[State3] = []
    underflow: list[State3] = []
    for state in ext:
        kind = classify_exterior(state)
        if kind == "overflow":
            overflow.append(state)
        else:
            underflow.append(state)
    g_init: dict[State3, tuple[int, int, int, int]] = {}
    h_init: dict[State3, tuple[int, int, int, int]] = {}
    g_fail: list[State3] = []
    h_fail: list[State3] = []
    for state in overflow:
        gaps = tuple(_overflow_gap(state, i) for i in range(4))
        g_init[state] = gaps  # type: ignore[assignment]
        if min(gaps) < 1:
            g_fail.append(state)
    for state in underflow:
        gaps = tuple(_underflow_gap(state, i) for i in range(4))
        h_init[state] = gaps  # type: ignore[assignment]
        if min(gaps) < 2:
            h_fail.append(state)
    # Recurrence identities on place values, independent of the state.
    recurrences_ok = _gap_recurrences_hold(12)
    return {
        "region_size": len(region),
        "exterior_count": len(ext),
        "overflow_count": len(overflow),
        "underflow_count": len(underflow),
        "overflow_min_initial_gap": min((min(g) for g in g_init.values()), default=None),
        "underflow_min_initial_gap": min((min(h) for h in h_init.values()), default=None),
        "overflow_initial_ok": not g_fail,
        "underflow_initial_ok": not h_fail,
        "recurrences_ok": recurrences_ok,
        "proved": not g_fail and not h_fail and recurrences_ok and (0, 0, 0) in region,
    }


def _gap_recurrences_hold(n: int) -> bool:
    """``hi``, ``lo``, and ``E`` recurrences used in the deadness certificate."""
    sys = phase0_order3()
    his = [unread_tail_bounds(i)[1] for i in range(n)]
    los = [unread_tail_bounds(i)[0] for i in range(n)]
    for i in range(4, n):
        if his[i] != 2 * his[i - 1] + his[i - 2] + his[i - 3] + 5:
            return False
        if los[i] != 2 * los[i - 1] + los[i - 2] + los[i - 3] - 10:
            return False
    probe = (1, -2, 3)
    es = [residual_integer(sys, probe, i) for i in range(n)]
    for i in range(4, n):
        if es[i] != 2 * es[i - 1] + es[i - 2] + es[i - 3]:
            return False
        g = es[i] - his[i]
        pred = 2 * (es[i - 1] - his[i - 1]) + (es[i - 2] - his[i - 2]) + (es[i - 3] - his[i - 3]) - 5
        if g != pred:
            return False
        h = los[i] - es[i]
        hpred = 2 * (los[i - 1] - es[i - 1]) + (los[i - 2] - es[i - 2]) + (los[i - 3] - es[i - 3]) - 10
        if h != hpred:
            return False
    return True


def compare_box_to_reach(
    max_length: int,
    a: int,
    b: int,
    c: int,
) -> dict[str, object]:
    reach = reachable_live(max_length)
    states: frozenset[State3] = reach["states"]  # type: ignore[assignment]
    box = candidate_box(a, b, c)
    extra_reach = states - box
    unused_box = box - states
    return {
        "max_length": max_length,
        "reach_size": len(states),
        "box_size": len(box),
        "reach_outside_box": len(extra_reach),
        "box_not_reached": len(unused_box),
        "reach_subset_of_box": not extra_reach,
        "reach_equals_b_min": states == B_MIN,
        "max_abs": (
            reach["max_abs_s1"],
            reach["max_abs_s2"],
            reach["max_abs_s3"],
        ),
    }
