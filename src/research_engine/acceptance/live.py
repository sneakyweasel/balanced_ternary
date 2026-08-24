"""Live-set constructions.

``LIVE_SLICE`` is ``R ∩ K`` at the same phase. ``LIVE`` is
``R ∩ C(K)``. Neither is implied by unbounded terminal geometry.
"""

from __future__ import annotations

from collections import defaultdict
from typing import TypeVar

from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import ClaimKind, SearchScope
from research_engine.reachability.forward import forward_search
from research_engine.reachability.result import DynamicsResult
from research_engine.reachability.reverse import reverse_co_live_layers

S = TypeVar("S")
C = TypeVar("C")
P = TypeVar("P")


def _scope_meet(left: SearchScope, right: SearchScope) -> SearchScope:
    if SearchScope.APPROXIMATE in (left, right):
        return SearchScope.APPROXIMATE
    if left == SearchScope.EXACT and right == SearchScope.EXACT:
        return SearchScope.EXACT
    return SearchScope.BOUNDED


def filter_terminal(
    spec: ProblemSpec[S, C, P],
    reachable: DynamicsResult[S, C, P],
) -> DynamicsResult[S, C, P]:
    """Same-phase live slice ``R ∩ K``. Not ``R ∩ C(K)``."""
    configs = frozenset(
        (state, phase)
        for state, phase in reachable.configurations
        if spec.is_terminal(state, phase)
    )
    layer_map: dict[object, set[S]] = defaultdict(set)
    union: set[S] = set()
    terminal_image: set[S] = set()
    for state, phase in configs:
        layer_map[phase].add(state)
        union.add(state)
        if spec.is_accepting(state, phase):
            terminal_image.add(state)
    return DynamicsResult(
        kind=ClaimKind.LIVE_SLICE,
        scope=reachable.scope,
        complete=reachable.complete,
        horizon=reachable.horizon,
        configurations=configs,
        layer={key: frozenset(values) for key, values in layer_map.items()},
        union=frozenset(union),
        terminal_image=frozenset(terminal_image),
        live_union=frozenset(union),
        visit_order=tuple(cfg for cfg in reachable.visit_order if cfg in configs),
        parents=dict(reachable.parents),
        live_start=reachable.live_start,
    )


def live_intersection(
    reachable: DynamicsResult[S, C, P],
    co_reachable: DynamicsResult[S, C, P],
) -> DynamicsResult[S, C, P]:
    """State-level ``R ∩ C(K)``.

    If the two results use different phase models, only states are
    intersected. That is not a same-phase ``L_n``.
    """
    live_states = reachable.union & co_reachable.union
    if reachable.configurations and co_reachable.configurations:
        co_configs = co_reachable.configurations
        # Phase-free reverse closures store depth in the second coordinate.
        if reachable.kind != ClaimKind.CO_REACHABLE and co_reachable.kind == ClaimKind.CO_REACHABLE:
            co_states = co_reachable.union
            configs = frozenset(
                (state, phase)
                for state, phase in reachable.configurations
                if state in co_states
            )
        else:
            configs = frozenset(cfg for cfg in reachable.configurations if cfg in co_configs)
    else:
        configs = frozenset(
            (state, phase)
            for state, phase in reachable.configurations
            if state in live_states
        )
    layer_map: dict[object, set[S]] = defaultdict(set)
    for state, phase in configs:
        layer_map[phase].add(state)
    terminal_image = reachable.terminal_image & live_states
    return DynamicsResult(
        kind=ClaimKind.LIVE,
        scope=_scope_meet(reachable.scope, co_reachable.scope),
        complete=reachable.complete and co_reachable.complete,
        horizon=reachable.horizon,
        configurations=configs,
        layer={key: frozenset(values) for key, values in layer_map.items()},
        union=frozenset(live_states),
        terminal_image=frozenset(terminal_image),
        live_union=frozenset(live_states),
        visit_order=tuple(cfg for cfg in reachable.visit_order if cfg in configs),
        live_start=reachable.live_start,
    )


def forward_live_layers(
    spec: ProblemSpec[S, C, P],
    *,
    max_steps: int | None = None,
) -> DynamicsResult[S, C, P]:
    """Live-staying forward BFS. ``LIVE_SLICE``, ``BOUNDED``."""
    return forward_search(spec, live_only=True, max_steps=max_steps)


def live_from_spec(
    spec: ProblemSpec[S, C, P],
    *,
    max_steps: int | None = None,
) -> DynamicsResult[S, C, P]:
    """Finite-horizon ``R ∩ C(K)`` on the forward DAG of ``spec``."""
    reachable = forward_search(spec, live_only=False, max_steps=max_steps)
    colive = reverse_co_live_layers(spec, max_steps=max_steps)
    return live_intersection(reachable, colive)
