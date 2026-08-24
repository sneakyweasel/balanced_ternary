"""Suffix feasibility and one-step live extensions.

For a finite control alphabet this is exact recursive feasibility on
the remaining-phase DAG. It does not bake in an energy formula.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Hashable, TypeVar

from research_engine.core.problem_spec import ProblemSpec

S = TypeVar("S")
C = TypeVar("C")
P = TypeVar("P")


def live_extensions(
    spec: ProblemSpec[S, C, P],
    state: S,
    phase: P,
) -> tuple[C, ...]:
    """Controls whose successor is terminal. One-step live Ext."""
    letters: list[C] = []
    src = spec.canonicalize(state)
    for control in spec.legal_controls(src, phase):
        nxt = spec.canonicalize(spec.transition(src, control, phase))
        nxt_phase = spec.next_phase(phase, control)
        if spec.is_terminal(nxt, nxt_phase):
            letters.append(control)
    return tuple(letters)


def is_suffix_accepted(
    spec: ProblemSpec[S, C, P],
    state: S,
    phase: P,
    word: tuple[C, ...],
    *,
    require_live: bool = True,
) -> bool:
    """Whether ``word`` is a legal (and, by default, live) suffix."""
    cur = spec.canonicalize(state)
    cur_phase = phase
    if require_live and not spec.is_terminal(cur, cur_phase):
        return False
    for control in word:
        if control not in spec.legal_controls(cur, cur_phase):
            return False
        cur = spec.canonicalize(spec.transition(cur, control, cur_phase))
        cur_phase = spec.next_phase(cur_phase, control)
        if require_live and not spec.is_terminal(cur, cur_phase):
            return False
    return spec.is_accepting(cur, cur_phase)


def is_co_live(
    spec: ProblemSpec[S, C, P],
    state: S,
    phase: P,
    *,
    max_depth: int | None = None,
) -> bool:
    """Exists a live path from ``(state, phase)`` to an accepting configuration."""

    @lru_cache(maxsize=None)
    def search(cur: Hashable, depth: int) -> bool:
        cur_state, cur_phase = cur  # type: ignore[misc]
        if spec.is_accepting(cur_state, cur_phase):
            return True
        if not spec.is_terminal(cur_state, cur_phase):
            return False
        if max_depth is not None and depth >= max_depth:
            return False
        controls = spec.legal_controls(cur_state, cur_phase)
        if not controls:
            return spec.is_accepting(cur_state, cur_phase)
        for control in controls:
            nxt_state = spec.canonicalize(spec.transition(cur_state, control, cur_phase))
            nxt_phase = spec.next_phase(cur_phase, control)
            if search((nxt_state, nxt_phase), depth + 1):
                return True
        return False

    start = spec.canonicalize(state)
    return search((start, phase), 0)


def co_live_extensions(
    spec: ProblemSpec[S, C, P],
    state: S,
    phase: P,
    *,
    max_depth: int | None = None,
) -> tuple[C, ...]:
    """Controls whose successor is co-live."""
    letters: list[C] = []
    src = spec.canonicalize(state)
    remaining = None if max_depth is None else max(max_depth - 1, 0)
    for control in spec.legal_controls(src, phase):
        nxt = spec.canonicalize(spec.transition(src, control, phase))
        nxt_phase = spec.next_phase(phase, control)
        if is_co_live(spec, nxt, nxt_phase, max_depth=remaining):
            letters.append(control)
    return tuple(letters)


def extension_set(
    spec: ProblemSpec[S, C, P],
    state: S,
    phase: P,
) -> tuple[C, ...]:
    """One-step live Ext. Alias of ``live_extensions``."""
    return live_extensions(spec, state, phase)
