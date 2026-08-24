"""Forward reachability on a ``ProblemSpec``.

Finite-horizon exploration is ``BOUNDED``. Exhausting a countdown DAG
is completeness for that horizon, not infinitude of the live set.
"""

from __future__ import annotations

from collections import defaultdict, deque
from typing import TypeVar

from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import ClaimKind, SearchScope
from research_engine.reachability.result import DynamicsResult

S = TypeVar("S")
C = TypeVar("C")
P = TypeVar("P")


def forward_search(
    spec: ProblemSpec[S, C, P],
    *,
    live_only: bool = False,
    max_steps: int | None = None,
) -> DynamicsResult[S, C, P]:
    """BFS from ``(initial_state, initial_phase)``.

    ``live_only=True`` enqueues only terminal successors. That is a
    live-staying graph, not automatically ``R ∩ C(K)``.
    """
    start_state = spec.canonicalize(spec.initial_state)
    start_phase = spec.initial_phase()
    start = (start_state, start_phase)
    if live_only and not spec.is_terminal(start_state, start_phase):
        return DynamicsResult(
            kind=ClaimKind.LIVE_SLICE if live_only else ClaimKind.REACHABLE,
            scope=SearchScope.BOUNDED,
            complete=True,
            horizon=0 if max_steps is None else max_steps,
            live_start=False,
        )

    seen: set[tuple[S, P]] = {start}
    queue: deque[tuple[S, P]] = deque([start])
    visit_order: list[tuple[S, P]] = [start]
    parents: dict[tuple[S, P], tuple[tuple[S, P], C]] = {}
    steps_from_start: dict[tuple[S, P], int] = {start: 0}
    rejected = 0
    truncated = False

    while queue:
        state, phase = queue.popleft()
        steps = steps_from_start[(state, phase)]
        if max_steps is not None and steps >= max_steps:
            if spec.legal_controls(state, phase):
                truncated = True
            continue
        for control in spec.legal_controls(state, phase):
            nxt_state = spec.canonicalize(spec.transition(state, control, phase))
            nxt_phase = spec.next_phase(phase, control)
            if live_only and not spec.is_terminal(nxt_state, nxt_phase):
                rejected += 1
                continue
            key = (nxt_state, nxt_phase)
            if key in seen:
                continue
            seen.add(key)
            parents[key] = ((state, phase), control)
            steps_from_start[key] = steps + 1
            queue.append(key)
            visit_order.append(key)

    layer_map: dict[object, set[S]] = defaultdict(set)
    union: set[S] = set()
    terminal_image: set[S] = set()
    live_union: set[S] = set()
    for state, phase in seen:
        layer_map[phase].add(state)
        union.add(state)
        if spec.is_terminal(state, phase):
            live_union.add(state)
        if spec.is_accepting(state, phase):
            terminal_image.add(state)

    horizon = max(steps_from_start.values(), default=0)
    if max_steps is not None:
        horizon = max_steps
    return DynamicsResult(
        kind=ClaimKind.LIVE_SLICE if live_only else ClaimKind.REACHABLE,
        scope=SearchScope.BOUNDED,
        complete=not truncated,
        horizon=horizon,
        configurations=frozenset(seen),
        layer={key: frozenset(values) for key, values in layer_map.items()},
        union=frozenset(union),
        terminal_image=frozenset(terminal_image),
        live_union=frozenset(live_union),
        rejected_images=rejected,
        visit_order=tuple(visit_order),
        parents=parents,
        live_start=True,
    )
