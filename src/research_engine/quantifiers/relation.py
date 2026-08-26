"""Explicit R ⊆ X×X from legal_controls × transition. No preferred successor."""

from __future__ import annotations

from research_engine.attacks.envelope import compute_exact_reachable
from research_engine.attacks.result import AttackContext
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import State
from research_engine.quantifiers.types import RelationEdge

DEFAULT_WINDOW = tuple(range(-12, 13))
EDGE_CAP = 128


def working_phase(spec: ProblemSpec, context: AttackContext | None = None):
    """Frozen initial phase. Residual-state relation, not countdown consumption."""

    if context is not None:
        phases = context.phases
        if phases:
            return phases[0]
    return spec.initial_phase()


def as_state(spec: ProblemSpec, seed: object) -> State:
    if isinstance(seed, tuple):
        return spec.canonicalize(seed)
    if spec.dimension == 1:
        return spec.canonicalize((int(seed),))
    return spec.canonicalize(seed)


def seed_states(
    spec: ProblemSpec,
    window: tuple[int, ...] | None = None,
    extra: tuple[State, ...] = (),
) -> tuple[State, ...]:
    window = DEFAULT_WINDOW if window is None else window
    found: list[State] = []
    seen: set[State] = set()

    def _add(state: State) -> None:
        if state in seen:
            return
        seen.add(state)
        found.append(state)

    try:
        _add(spec.canonicalize(spec.initial_state))
    except (TypeError, ValueError):
        pass
    if spec.dimension == 1:
        for value in window:
            try:
                _add(as_state(spec, value))
            except (TypeError, ValueError):
                continue
    for item in extra:
        try:
            _add(spec.canonicalize(item))
        except (TypeError, ValueError):
            continue
    return tuple(found)


def images_of(spec: ProblemSpec, state: State, phase) -> tuple[tuple[object, State], ...]:
    src = spec.canonicalize(state)
    found: list[tuple[object, State]] = []
    try:
        controls = spec.legal_controls(src, phase)
    except (TypeError, ValueError):
        return ()
    for control in controls:
        try:
            nxt = spec.canonicalize(spec.transition(src, control, phase))
        except (TypeError, ValueError):
            continue
        found.append((control, nxt))
    return tuple(found)


def legal_images(spec: ProblemSpec, state: State, phase) -> tuple[State, ...]:
    return tuple(dst for _control, dst in images_of(spec, state, phase))


def relation_edges(
    spec: ProblemSpec,
    states: tuple[State, ...] | list[State],
    phase,
    *,
    limit: int = EDGE_CAP,
) -> tuple[RelationEdge, ...]:
    """Enumerate one-step legal pairs. Does not collapse to a preferred successor."""

    edges: list[RelationEdge] = []
    for state in states:
        for control, dst in images_of(spec, state, phase):
            edges.append(RelationEdge(src=spec.canonicalize(state), control=control, dst=dst))
            if len(edges) >= limit:
                return tuple(edges)
    return tuple(edges)


def closure_states(spec: ProblemSpec, context: AttackContext) -> tuple[tuple[State, ...], bool]:
    """Reuse exhaustive closure when complete. Truncation is not infinitude."""

    result = compute_exact_reachable(spec, context)
    complete = bool(result.complete)
    if not result.reachable:
        return (), complete
    reached = tuple(result.reachable)
    if not complete:
        return reached, False
    return reached, True
