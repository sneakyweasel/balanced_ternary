"""Shortest control words on a completed forward search."""

from __future__ import annotations

from typing import TypeVar

from research_engine.reachability.result import DynamicsResult

S = TypeVar("S")
C = TypeVar("C")
P = TypeVar("P")


def shortest_word(
    result: DynamicsResult[S, C, P],
    state: S,
    phase: P,
) -> tuple[C, ...] | None:
    """First-visit word from the search origin to ``(state, phase)``.

    ``None`` if the configuration was not reached. Length is shortest in
    the unweighted BFS that produced ``result``.
    """
    key = (state, phase)
    if key not in result.configurations:
        return None
    word: list[C] = []
    cur = key
    while cur in result.parents:
        prev, control = result.parents[cur]
        word.append(control)
        cur = prev
    word.reverse()
    return tuple(word)
