"""Partition-refinement DFA minimization.

Completeness of the input DFA is assumed. The algorithm is classical
Hopcroft/Moore partition refinement; a concrete state count for a given
machine is **COMPUTATIONALLY VERIFIED**.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Callable, Hashable, Iterable, Sequence

State = Hashable
Letter = Hashable
Delta = Callable[[State, Letter], State]


@dataclass(frozen=True)
class MinimizedDFA:
    state_count: int
    start: int
    accepts: frozenset[int]
    alphabet: tuple[Letter, ...]
    delta: tuple[tuple[int, ...], ...]  # delta[state][letter_index] -> state

    def transition(self, state: int, letter: Letter) -> int:
        idx = self.alphabet.index(letter)
        return self.delta[state][idx]


def reachable_states(
    start: State,
    alphabet: Sequence[Letter],
    delta: Delta,
) -> frozenset[State]:
    seen: set[State] = {start}
    queue: deque[State] = deque([start])
    while queue:
        s = queue.popleft()
        for a in alphabet:
            nxt = delta(s, a)
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return frozenset(seen)


def minimize_dfa(
    start: State,
    alphabet: Sequence[Letter],
    delta: Delta,
    accepts: Iterable[State],
) -> MinimizedDFA:
    """Minimize the reachable complete DFA. Empty language yields 1 state."""
    alphabet_t = tuple(alphabet)
    acc = frozenset(accepts)
    reachable = reachable_states(start, alphabet_t, delta)
    accept_r = frozenset(s for s in reachable if s in acc)
    reject_r = frozenset(s for s in reachable if s not in acc)
    blocks: list[frozenset[State]] = []
    if accept_r:
        blocks.append(accept_r)
    if reject_r:
        blocks.append(reject_r)
    if not blocks:
        blocks = [reachable]

    def block_index(partition: list[frozenset[State]]) -> dict[State, int]:
        idx: dict[State, int] = {}
        for i, block in enumerate(partition):
            for s in block:
                idx[s] = i
        return idx

    changed = True
    while changed:
        changed = False
        index = block_index(blocks)
        new_blocks: list[frozenset[State]] = []
        for block in blocks:
            buckets: dict[tuple[int, ...], list[State]] = {}
            for s in block:
                sig = tuple(index[delta(s, a)] for a in alphabet_t)
                buckets.setdefault(sig, []).append(s)
            if len(buckets) > 1:
                changed = True
            for group in buckets.values():
                new_blocks.append(frozenset(group))
        blocks = new_blocks

    index = block_index(blocks)
    start_id = index[start]
    # Relabel so the start state is 0.
    order = [start_id] + [i for i in range(len(blocks)) if i != start_id]
    remap = {old: new for new, old in enumerate(order)}
    n = len(blocks)
    table: list[list[int]] = []
    new_accept: set[int] = set()
    representatives = [next(iter(blocks[old])) for old in order]
    for new_id, old in enumerate(order):
        rep = next(iter(blocks[old]))
        row = [remap[index[delta(rep, a)]] for a in alphabet_t]
        table.append(row)
        if rep in acc:
            new_accept.add(new_id)
    _ = representatives
    return MinimizedDFA(
        state_count=n,
        start=0,
        accepts=frozenset(new_accept),
        alphabet=alphabet_t,
        delta=tuple(tuple(row) for row in table),
    )
