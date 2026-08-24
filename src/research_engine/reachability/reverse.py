"""Reverse / co-reachability.

``C(seed)`` is not the live set. A finite reverse basin is not
``|L|=∞``, and it is not origin-reachable forward geometry.
"""

from __future__ import annotations

from collections import defaultdict, deque
from collections.abc import Callable, Iterable
from typing import TypeVar

from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import ClaimKind, SearchScope
from research_engine.reachability.result import DynamicsResult

S = TypeVar("S")
C = TypeVar("C")
P = TypeVar("P")


def reverse_predecessors_among(
    spec: ProblemSpec[S, C, P],
    state: S,
    phase: P,
    predecessor_phase: P,
    candidates: Iterable[S],
) -> tuple[tuple[S, C], ...]:
    """Exact predecessors of ``(state, phase)`` among ``candidates``."""
    target = spec.canonicalize(state)
    hits: list[tuple[S, C]] = []
    seen: set[tuple[S, C]] = set()
    for candidate in candidates:
        src = spec.canonicalize(candidate)
        for control in spec.legal_controls(src, predecessor_phase):
            nxt = spec.canonicalize(spec.transition(src, control, predecessor_phase))
            nxt_phase = spec.next_phase(predecessor_phase, control)
            if nxt == target and nxt_phase == phase:
                key = (src, control)
                if key not in seen:
                    seen.add(key)
                    hits.append(key)
    return tuple(hits)


def reverse_closure(
    seeds: Iterable[S],
    predecessors: Callable[[S], Iterable[S]],
    *,
    max_depth: int | None = None,
    canonicalize: Callable[[S], S] | None = None,
) -> DynamicsResult[S, object, int]:
    """Least fixed point of reverse images of ``seeds``.

    If the iteration empties without a depth cap, the result is ``EXACT``
    for co-reachability of those seeds under this predecessor relation.
    It is still not a live-set theorem.
    """
    norm = canonicalize if canonicalize is not None else (lambda state: state)
    start = [norm(seed) for seed in seeds]
    if not start:
        return DynamicsResult(
            kind=ClaimKind.CO_REACHABLE,
            scope=SearchScope.EXACT,
            complete=True,
            horizon=0,
        )
    seen: set[S] = set(start)
    layer: set[S] = set(start)
    layers: dict[int, set[S]] = {0: set(start)}
    visit_order: list[tuple[S, int]] = [(state, 0) for state in start]
    depth = 0
    truncated = False
    while True:
        if max_depth is not None and depth >= max_depth:
            truncated = True
            break
        nxt: set[S] = set()
        for state in layer:
            for pred in predecessors(state):
                key = norm(pred)
                if key not in seen:
                    seen.add(key)
                    nxt.add(key)
                    visit_order.append((key, depth + 1))
        if not nxt:
            break
        depth += 1
        layer = nxt
        layers[depth] = set(nxt)

    scope = SearchScope.BOUNDED if truncated else SearchScope.EXACT
    return DynamicsResult(
        kind=ClaimKind.CO_REACHABLE,
        scope=scope,
        complete=not truncated,
        horizon=depth if max_depth is None else max_depth,
        configurations=frozenset(visit_order),
        layer={key: frozenset(values) for key, values in layers.items()},
        union=frozenset(seen),
        visit_order=tuple(visit_order),
    )


def reverse_co_live_layers(
    spec: ProblemSpec[S, C, P],
    *,
    max_steps: int | None = None,
) -> DynamicsResult[S, C, P]:
    """Backward marks of configurations that can reach an accepting state.

    Built from a completed forward DAG of ``spec``. Scope remains
    ``BOUNDED`` in the start-phase horizon.
    """
    from research_engine.reachability.forward import forward_search

    fwd = forward_search(spec, live_only=False, max_steps=max_steps)
    reverse: dict[tuple[S, P], list[tuple[S, P]]] = defaultdict(list)
    for key, (prev, _control) in fwd.parents.items():
        reverse[key].append(prev)
    colive: set[tuple[S, P]] = {
        (state, phase)
        for state, phase in fwd.configurations
        if spec.is_accepting(state, phase)
    }
    queue: deque[tuple[S, P]] = deque(colive)
    while queue:
        cur = queue.popleft()
        for prev in reverse[cur]:
            if prev not in colive:
                colive.add(prev)
                queue.append(prev)
    layer_map: dict[object, set[S]] = defaultdict(set)
    union: set[S] = set()
    for state, phase in colive:
        layer_map[phase].add(state)
        union.add(state)
    return DynamicsResult(
        kind=ClaimKind.CO_REACHABLE,
        scope=SearchScope.BOUNDED,
        complete=fwd.complete,
        horizon=fwd.horizon,
        configurations=frozenset(colive),
        layer={key: frozenset(values) for key, values in layer_map.items()},
        union=frozenset(union),
        terminal_image=fwd.terminal_image,
        live_union=frozenset(union),
        visit_order=tuple(cfg for cfg in fwd.visit_order if cfg in colive),
        live_start=fwd.live_start,
    )
