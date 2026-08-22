"""Deterministic residue automaton for a single modulus q.

States are residues ``{0, ..., q-1}``. The automaton reads a balanced
ternary word most-significant digit first. If the current prefix has
residue ``r``, appending digit ``a in {-1, 0, +1}`` yields

    r' ≡ 3r + a  (mod q).

This is independent of whether ``q`` is 3. For ``q = 3`` the transition
collapses to ``r' ≡ a (mod 3)`` because ``3r ≡ 0``.
"""

from __future__ import annotations

from collections import deque

from balanced_ternary.representation import WordLike, msd_digits

ALPHABET: tuple[int, int, int] = (-1, 0, 1)


class ModularAutomaton:
    """Residue DFA for a fixed modulus ``q >= 2``."""

    def __init__(self, q: int):
        if isinstance(q, bool) or not isinstance(q, int) or q < 2:
            raise ValueError(f"modulus q must be an integer >= 2, got {q!r}")
        self.q = q

    def transition(self, state: int, digit: int) -> int:
        if digit not in ALPHABET:
            raise ValueError(f"digit must be in {{-1, 0, +1}}, got {digit!r}")
        return (3 * state + digit) % self.q

    def run(self, word: WordLike) -> list[int]:
        """State path, including the start state 0 before any digit."""
        r = 0
        path = [0]
        for a in msd_digits(word):
            r = self.transition(r, a)
            path.append(r)
        return path

    def residue(self, word: WordLike) -> int:
        return self.run(word)[-1]

    def is_divisible(self, word: WordLike) -> bool:
        return self.residue(word) == 0

    def transition_table(self) -> dict[int, dict[int, int]]:
        """``table[r][a] = (3r + a) mod q`` for every state and digit."""
        table: dict[int, dict[int, int]] = {}
        for r in range(self.q):
            table[r] = {a: self.transition(r, a) for a in ALPHABET}
        return table

    def reachable_states(self) -> frozenset[int]:
        """States reachable from 0 under the alphabet ``{-, 0, +}``."""
        seen: set[int] = {0}
        queue: deque[int] = deque([0])
        while queue:
            r = queue.popleft()
            for a in ALPHABET:
                nxt = self.transition(r, a)
                if nxt not in seen:
                    seen.add(nxt)
                    queue.append(nxt)
        return frozenset(seen)

    def minimize(self) -> None:
        raise NotImplementedError(
            "The generic residue automaton does not provide minimization; "
            "use a domain-specific DFA implementation when needed."
        )
