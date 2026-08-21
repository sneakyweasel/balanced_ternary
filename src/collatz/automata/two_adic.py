"""2-adic digit automaton of precision ``K``.

States are residues ``{0, ..., 2^K - 1}``. The alphabet is the balanced
ternary digits ``{-, 0, +}``. The transition is the same Horner step used
by ``ModularAutomaton``:

    delta(r, a) = (3r + a) mod 2^K.

This class wraps ``ModularAutomaton(2^K)`` rather than duplicating it.

For completed words:

    automaton.residue(word) == decode(word) mod 2^K.

That identity is a special case of the existing modular-recurrence theorem.

Valuation classification of a state uses ``classify_collatz_valuation``.
It approximates the 2-adic information needed for the *valuation step* of
``T``. It is not a finite-state model of the full Collatz map: dividing by
``2^k`` is not well-defined modulo ``2^K``. See
``docs/collatz_mathematics.md``.
"""

from __future__ import annotations

from collections import defaultdict

from automata.modular import ModularAutomaton
from balanced_ternary.representation import WordLike
from collatz.valuation import ValuationClassification, classify_collatz_valuation


class TwoAdicDigitAutomaton:
    """Residue DFA modulo ``2^K`` with Collatz-valuation labels on states."""

    def __init__(self, precision: int):
        if isinstance(precision, bool) or not isinstance(precision, int) or precision < 1:
            raise ValueError(
                f"precision K must be an integer >= 1, got {precision!r}"
            )
        self.precision = precision
        self.modulus = 1 << precision
        self._inner = ModularAutomaton(self.modulus)

    def transition(self, state: int, digit: int) -> int:
        return self._inner.transition(state, digit)

    def run(self, word: WordLike) -> list[int]:
        return self._inner.run(word)

    def residue(self, word: WordLike) -> int:
        return self._inner.residue(word)

    def transition_table(self) -> dict[int, dict[int, int]]:
        return self._inner.transition_table()

    def reachable_states(self) -> frozenset[int]:
        return self._inner.reachable_states()

    def classify_state(self, residue: int) -> ValuationClassification:
        return classify_collatz_valuation(residue, self.precision)

    def odd_states(self) -> tuple[int, ...]:
        return tuple(r for r in range(self.modulus) if r % 2 == 1)

    def valuation_partition(self) -> dict[str, tuple[int, ...]]:
        """Partition of *odd* residues by classified ``v2(3n+1)``.

        Keys are ``"1"``, ``"2"``, ..., ``"{K-1}"`` for exact classes and
        ``"AT_LEAST_K"`` for the insufficient-precision class. Even residues
        are omitted: the accelerated map is defined on odd integers.
        """
        buckets: dict[str, list[int]] = defaultdict(list)
        for r in self.odd_states():
            buckets[self.classify_state(r).label()].append(r)
        return {key: tuple(vals) for key, vals in buckets.items()}

    def format_report(self, example_word: WordLike | None = None) -> str:
        part = self.valuation_partition()
        exact_keys = sorted(
            (k for k in part if k != "AT_LEAST_K"), key=lambda s: int(s)
        )
        lines = [
            f"TwoAdicDigitAutomaton  precision K={self.precision}  "
            f"modulus=2^{self.precision}={self.modulus}",
            f"Alphabet: -, 0, +",
            f"Transition: r' = (3r + a) mod {self.modulus}",
            f"States: {self.modulus}",
            f"Reachable from 0: {len(self.reachable_states())}",
            f"Odd states: {len(self.odd_states())}",
            "",
            "Valuation partition of odd residues (v2(3n+1)):",
        ]
        for key in exact_keys:
            lines.append(f"  v2 = {key}: {len(part[key])} odd residues")
        if "AT_LEAST_K" in part:
            lines.append(
                f"  v2 >= {self.precision} (AT_LEAST_K): "
                f"{len(part['AT_LEAST_K'])} odd residues"
            )
        lines.append("")
        lines.append(
            "Convention: exact k is reported only for 1 <= k < K. "
            f"The class AT_LEAST_K is v2(3n+1) >= {self.precision}."
        )
        if example_word is not None:
            path = self.run(example_word)
            word_s = str(example_word)
            lines.append("")
            lines.append(f"Path for word {word_s!r}:")
            lines.append("  start 0")
            digits = word_s if isinstance(example_word, str) else example_word.word()
            for ch, state in zip(digits, path[1:]):
                lines.append(f"  --{ch}--> {state}")
            final = path[-1]
            cls = self.classify_state(final)
            lines.append(
                f"Final residue {final}  valuation class {cls.label()}"
            )
        lines.append("")
        return "\n".join(lines)
