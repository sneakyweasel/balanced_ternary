"""Regular languages ``L_k = { BT(n) : v2(n) = k }`` for each fixed k.

**PROVED:** for each fixed k, ``L_k`` is regular. An MSD Horner automaton
modulo ``2^{k+1}`` distinguishes ``v2(n) = k`` from ``v2(n) != k``, because
the valuation is exact precisely when it is strictly less than the
modulus exponent.

``L_0`` (odd integers) is the same language as odd weight, by the existing
parity theorem.

The union over unbounded k is not claimed to be regular as a single
language of "exactly-k for some k that the automaton computes".
"""

from __future__ import annotations

from bt.automata.modular import ModularAutomaton
from bt.representation import WordLike
from research.collatz.valuation import v2


class ValuationClassDFA:
    """MSD acceptor for ``v2(decode(w)) == k``."""

    def __init__(self, k: int):
        if isinstance(k, bool) or not isinstance(k, int) or k < 0:
            raise ValueError(f"k must be an integer >= 0, got {k!r}")
        self.k = k
        self.precision = k + 1
        self.modulus = 1 << self.precision
        self._auto = ModularAutomaton(self.modulus)

    def residue(self, word: WordLike) -> int:
        return self._auto.residue(word)

    def accepts(self, word: WordLike) -> bool:
        r = self.residue(word)
        if r == 0:
            return False
        return v2(r) == self.k

    def accept_states(self) -> tuple[int, ...]:
        out: list[int] = []
        for r in range(self.modulus):
            if r != 0 and v2(r) == self.k:
                out.append(r)
        return tuple(out)

    def minimized_state_count(self) -> int:
        """``A_k``: minimized DFA size. **VERIFIED COMPUTATIONALLY**."""
        from bt.automata.modular import ALPHABET
        from bt.automata.minimize import minimize_dfa

        return minimize_dfa(
            start=0,
            alphabet=ALPHABET,
            delta=self._auto.transition,
            accepts=self.accept_states(),
        ).state_count
