"""Reachable residual box and bounded addition checks.

The transition is the recurrence in ``residual.next_state``. This
module only explores the graph that recurrence generates. Finite
exhaustive checks are verification evidence, not proofs.
"""

from __future__ import annotations

from collections import deque

from research.ostrowski.digits import (
    canonicality_census,
    enumerate_canonical,
    max_digit,
)
from research.ostrowski.residual import (
    CarryState,
    accepts_msd,
    accepts_msd_boxed,
    difference_word,
    lsd_to_msd,
    next_state,
    zero_state,
)
from research.ostrowski.system import OstrowskiSystem, characteristic_poly_coeffs, phase0_order3


def possible_w(system: OstrowskiSystem, i: int) -> range:
    """Possible ``z - (x+y)`` at place ``i`` from the digit alphabet."""
    cap = max_digit(system, i)
    return range(-2 * cap, cap + 1)


def reachable_states(
    system: OstrowskiSystem,
    max_length: int,
    *,
    coord_limit: int = 16,
    w_from_digits: bool = True,
) -> dict[str, object]:
    """BFS of carry states reachable from ``0`` by MSD-first words of length ≤ ``max_length``.

    If any coordinate exceeds ``coord_limit``, the search reports
    ``bounded=False`` and stops expanding that state. Constant-coefficient
    systems use the same ``d_{k,i}`` at every ``i≥1``, so the graph is
    position-independent after the first step; we still store the
    remaining length because early ``q_j=0`` makes coordinates
    non-unique near ``i=0``.
    """
    start = zero_state(system.order)
    # Node: (state, remaining length i). i=0 is a sink.
    seen: set[tuple[CarryState, int]] = {(start, max_length)}
    states: set[CarryState] = {start}
    queue: deque[tuple[CarryState, int]] = deque([(start, max_length)])
    overflow: list[CarryState] = []
    transitions = 0
    while queue:
        state, i = queue.popleft()
        if i == 0:
            continue
        ws = possible_w(system, i - 1) if w_from_digits else range(-8, 9)
        for w in ws:
            nxt = next_state(system, state, w, i)
            transitions += 1
            if any(abs(c) > coord_limit for c in nxt):
                overflow.append(nxt)
                continue
            key = (nxt, i - 1)
            if key not in seen:
                seen.add(key)
                states.add(nxt)
                queue.append(key)
    coords = [c for s in states for c in s]
    return {
        "order": system.order,
        "max_length": max_length,
        "coord_limit": coord_limit,
        "state_count": len(states),
        "positioned_count": len(seen),
        "transition_count": transitions,
        "max_abs_coord": max((abs(c) for c in coords), default=0),
        "bounded": not overflow,
        "overflow_sample": overflow[:5],
        "states": frozenset(states),
        "accepting_count": sum(1 for s in states if s[-1] == 0),
    }


def reachable_states_homogeneous(
    system: OstrowskiSystem,
    steps: int,
    *,
    coord_limit: int = 16,
) -> dict[str, object]:
    """Position-independent BFS using ``d_{k,i}`` at a fixed large ``i``.

    For purely periodic coefficients the transition does not depend on
    ``i`` once ``i`` is larger than the order. This is the candidate
    finite-state graph of Hypothesis 1.
    """
    i = system.order + 4
    start = zero_state(system.order)
    seen: set[CarryState] = {start}
    queue: deque[CarryState] = deque([start])
    overflow: list[CarryState] = []
    transitions = 0
    depth = {start: 0}
    while queue:
        state = queue.popleft()
        if depth[state] >= steps:
            continue
        for w in possible_w(system, 1):
            nxt = next_state(system, state, w, i)
            transitions += 1
            if any(abs(c) > coord_limit for c in nxt):
                overflow.append(nxt)
                continue
            if nxt not in seen:
                seen.add(nxt)
                depth[nxt] = depth[state] + 1
                queue.append(nxt)
    coords = [c for s in seen for c in s]
    return {
        "order": system.order,
        "steps": steps,
        "coord_limit": coord_limit,
        "state_count": len(seen),
        "transition_count": transitions,
        "max_abs_coord": max((abs(c) for c in coords), default=0),
        "bounded": not overflow,
        "overflow_sample": overflow[:5],
        "states": frozenset(seen),
    }


def value_map(
    system: OstrowskiSystem,
    length: int,
    *,
    order_m: bool = True,
) -> dict[int, tuple[int, ...]]:
    """One canonical word of exact ``length`` (padded) for each represented value."""
    mapping: dict[int, tuple[int, ...]] = {}
    for word in enumerate_canonical(system, length, order_m=order_m):
        mapping.setdefault(system.val(word), word)
    return mapping


def verify_boxed_addition(
    system: OstrowskiSystem,
    length: int,
    tm_bound: int,
    *,
    order_m: bool = True,
) -> dict[str, int | bool]:
    """Same as ``verify_addition`` but reject runs that leave the ``t_m`` box."""
    mapping = value_map(system, length, order_m=order_m)
    values = sorted(mapping)
    pairs = 0
    agree = 0
    false_accept = 0
    false_reject = 0
    missing_sum = 0
    for x in values:
        for y in values:
            pairs += 1
            z = x + y
            xw, yw = mapping[x], mapping[y]
            if z not in mapping:
                missing_sum += 1
                continue
            diffs = lsd_to_msd(difference_word(xw, yw, mapping[z]))
            if accepts_msd_boxed(system, diffs, tm_bound):
                agree += 1
            else:
                false_reject += 1
            if z + 1 in mapping:
                wrong = lsd_to_msd(difference_word(xw, yw, mapping[z + 1]))
                if accepts_msd_boxed(system, wrong, tm_bound):
                    false_accept += 1
    return {
        "pairs": pairs,
        "agree": agree,
        "false_accept": false_accept,
        "false_reject": false_reject,
        "missing_sum": missing_sum,
        "ok": false_accept == 0 and false_reject == 0,
        "tm_bound": tm_bound,
    }


def verify_addition(
    system: OstrowskiSystem,
    length: int,
    *,
    order_m: bool = True,
    max_pairs: int | None = None,
) -> dict[str, int | bool]:
    """Compare ``val(x)+val(y)=val(z)`` with MSD acceptance on padded words.

    Exhaustive over canonical values that have a length-``length`` word,
    restricted to pairs whose sum is also represented at that length.
    """
    mapping = value_map(system, length, order_m=order_m)
    values = sorted(mapping)
    pairs = 0
    agree = 0
    false_accept = 0
    false_reject = 0
    missing_sum = 0
    for x in values:
        for y in values:
            if max_pairs is not None and pairs >= max_pairs:
                return {
                    "pairs": pairs,
                    "agree": agree,
                    "false_accept": false_accept,
                    "false_reject": false_reject,
                    "missing_sum": missing_sum,
                    "ok": false_accept == 0 and false_reject == 0,
                    "truncated": True,
                }
            pairs += 1
            z = x + y
            xw, yw = mapping[x], mapping[y]
            if z not in mapping:
                missing_sum += 1
                continue
            zw = mapping[z]
            diffs = lsd_to_msd(difference_word(xw, yw, zw))
            accepted = accepts_msd(system, diffs)
            if accepted:
                agree += 1
            else:
                false_reject += 1
            # one wrong z, when available
            if z + 1 in mapping and z + 1 != z:
                wrong = lsd_to_msd(difference_word(xw, yw, mapping[z + 1]))
                if accepts_msd(system, wrong):
                    false_accept += 1
    return {
        "pairs": pairs,
        "agree": agree,
        "false_accept": false_accept,
        "false_reject": false_reject,
        "missing_sum": missing_sum,
        "ok": false_accept == 0 and false_reject == 0,
        "truncated": False,
    }


def polynomial_is_irreducible_cubic(coeffs: tuple[int, ...]) -> bool:
    """``x^3 + a x^2 + b x + c`` has no rational root, hence is irreducible over Q."""
    from research_engine.algebra.spectral import (
        polynomial_is_irreducible_cubic as engine_irreducible,
    )

    return engine_irreducible(coeffs)


def phase0_report(length: int = 6, box_steps: int = 8, coord_limit: int = 12) -> dict[str, object]:
    """Compact Phase-0 record for the chosen order-3 Γ."""
    system = phase0_order3()
    coeffs = characteristic_poly_coeffs(system)
    census = canonicality_census(system, length, order_m=True)
    box = reachable_states_homogeneous(system, steps=box_steps, coord_limit=coord_limit)
    positioned = reachable_states(system, max_length=length, coord_limit=coord_limit)
    addition = verify_addition(system, min(length, 5), order_m=True)
    boxed_one = verify_boxed_addition(system, min(length, 5), tm_bound=1, order_m=True)
    boxed_two = verify_boxed_addition(system, min(length, 5), tm_bound=2, order_m=True)
    from research.ostrowski.minimize import boxed_minimality

    minimality = boxed_minimality(system, tm_bound=2)
    qs = system.place_values(length)
    return {
        "order": 3,
        "parameter_definition": "Gamma=([0;2-bar],[0;1-bar],[0;1-bar])",
        "place_value_recurrence": "q_i=2 q_{i-1}+q_{i-2}+q_{i-3}",
        "place_values": qs,
        "characteristic_polynomial": coeffs,
        "irreducible_cubic": polynomial_is_irreducible_cubic(coeffs) if coeffs else False,
        "digit_constraints": "section 5.3 proposed rules",
        "canonicality": census,
        "direction": "MSD-first unread-tail residual",
        "homogeneous_box": {
            k: box[k]
            for k in (
                "state_count",
                "max_abs_coord",
                "bounded",
                "transition_count",
                "steps",
            )
        },
        "positioned_box": {
            k: positioned[k]
            for k in (
                "state_count",
                "max_abs_coord",
                "bounded",
                "accepting_count",
                "transition_count",
            )
        },
        "addition": addition,
        "boxed_tm_1": boxed_one,
        "boxed_tm_2": boxed_two,
        "minimality_tm_2": minimality,
        "final_state_condition": "s_m = 0",
        "proof_status": "COMPUTATIONALLY VERIFIED at the recorded bounds",
    }
