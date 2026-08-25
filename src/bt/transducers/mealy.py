"""Partition-refinement minimization of letter-to-letter Mealy machines.

A concrete state count is **COMPUTATIONALLY VERIFIED**, not a closed form.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Sequence
from typing import Hashable, TypeVar

S = TypeVar("S")
Letter = TypeVar("Letter")


def mealy_partition(
    states: Iterable[S],
    alphabet: Sequence[Letter],
    step: Callable[[S, Letter], tuple[S, Hashable]],
) -> tuple[frozenset[S], ...]:
    """Refine by output signature, then by successor blocks."""
    state_list = list(states)
    if not state_list:
        return ()
    alphabet_t = tuple(alphabet)
    buckets: dict[tuple[Hashable, ...], list[S]] = {}
    for state in state_list:
        sig = tuple(step(state, letter)[1] for letter in alphabet_t)
        buckets.setdefault(sig, []).append(state)
    partition = [frozenset(group) for group in buckets.values()]

    changed = True
    while changed:
        changed = False
        block_of: dict[S, int] = {}
        for index, block in enumerate(partition):
            for state in block:
                block_of[state] = index
        new_parts: list[frozenset[S]] = []
        for block in partition:
            split: dict[tuple[int, ...], list[S]] = {}
            for state in block:
                key = tuple(block_of[step(state, letter)[0]] for letter in alphabet_t)
                split.setdefault(key, []).append(state)
            if len(split) > 1:
                changed = True
            new_parts.extend(frozenset(group) for group in split.values())
        partition = new_parts
    return tuple(partition)


def minimize_mealy_count(
    states: Iterable[S],
    alphabet: Sequence[Letter],
    step: Callable[[S, Letter], tuple[S, Hashable]],
) -> int:
    """Number of future-equivalence classes of a complete Mealy machine."""
    return len(mealy_partition(states, alphabet, step))
