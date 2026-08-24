"""DFA minimization of a boxed residual adder.

Written only because the order-3 ``|t_m| ≤ 2`` graph is finite.
Hopcroft partition refinement; the sink (out-of-box) is kept.
"""

from __future__ import annotations

from collections import deque
from typing import Iterable

from research.ostrowski.residual import (
    CarryState,
    is_accepting,
    next_state,
    zero_state,
)
from research.ostrowski.system import OstrowskiSystem

SINK = None


def boxed_graph(
    system: OstrowskiSystem,
    tm_bound: int,
    alphabet: Iterable[int],
    i: int | None = None,
) -> tuple[frozenset[CarryState], dict[tuple[CarryState | None, int], CarryState | None]]:
    """Position-independent graph of transitions that keep ``|t_m| ≤ tm_bound``."""
    if i is None:
        i = system.order + 5
    alphabet = tuple(alphabet)
    start = zero_state(system.order)
    seen: set[CarryState] = {start}
    queue: deque[CarryState] = deque([start])
    delta: dict[tuple[CarryState | None, int], CarryState | None] = {}
    while queue:
        state = queue.popleft()
        for w in alphabet:
            nxt = next_state(system, state, w, i)
            if abs(nxt[-1]) > tm_bound:
                delta[(state, w)] = SINK
                continue
            delta[(state, w)] = nxt
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    for w in alphabet:
        delta[(SINK, w)] = SINK
    return frozenset(seen), delta


def hopcroft_minimize(
    states: frozenset[CarryState],
    delta: dict[tuple[CarryState | None, int], CarryState | None],
    alphabet: Iterable[int],
) -> dict[str, object]:
    """Minimize the boxed DFA, including the reject sink."""
    alphabet = tuple(alphabet)
    universe: set[CarryState | None] = set(states) | {SINK}

    def target(q: CarryState | None, w: int) -> CarryState | None:
        return delta.get((q, w), SINK)

    accepting = {s for s in states if is_accepting(s)}
    partition: list[set[CarryState | None]] = [
        p
        for p in (set(accepting), set(states) - accepting, {SINK})
        if p
    ]
    waiting = [set(p) for p in partition]
    while waiting:
        block = waiting.pop()
        for w in alphabet:
            pred = {q for q in universe if target(q, w) in block}
            new_parts: list[set[CarryState | None]] = []
            for part in partition:
                left = part & pred
                right = part - pred
                if left and right:
                    new_parts.extend([left, right])
                    if part in waiting:
                        waiting.remove(part)
                        waiting.extend([left, right])
                    else:
                        waiting.append(left if len(left) <= len(right) else right)
                else:
                    new_parts.append(part)
            partition = new_parts
    live_parts = [p for p in partition if p != {SINK}]
    return {
        "raw_states": len(states),
        "minimal_states": len(partition),
        "minimal_live": len(live_parts),
        "part_sizes": tuple(sorted(len(p) for p in partition)),
        "merged": any(len(p) > 1 for p in live_parts),
        "accepting_raw": len(accepting),
    }


def boxed_minimality(
    system: OstrowskiSystem,
    tm_bound: int,
    alphabet: tuple[int, ...] = tuple(range(-4, 3)),
) -> dict[str, object]:
    states, delta = boxed_graph(system, tm_bound, alphabet)
    report = hopcroft_minimize(states, delta, alphabet)
    coords = [abs(c) for s in states for c in s]
    report["tm_bound"] = tm_bound
    report["max_abs_coord"] = max(coords, default=0)
    report["alphabet"] = alphabet
    return report
