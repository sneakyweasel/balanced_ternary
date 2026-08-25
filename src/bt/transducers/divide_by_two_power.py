"""Fixed-k LSD transducer for division by ``2^k``.

Implemented as the k-fold product of the 3-state ``/2`` machine. Naive
state bound is ``3^k``. Reachable and minimized sizes are reported as
**COMPUTATIONALLY VERIFIED**, not as a closed-form theorem.

The map is only applied to integers divisible by ``2^k``.
"""

from __future__ import annotations

from collections import deque

from bt.representation import (
    BalancedTernary,
    WordLike,
    decode,
    digits,
    encode,
    from_digits_lsd,
    normalize,
)
from bt.transducers.divide_by_two import divide_by_two_step
from bt.metrics import v2
from bt.transducers.mealy import minimize_mealy_count

ALPHABET: tuple[int, int, int] = (-1, 0, 1)


def _compose_step(carries: tuple[int, ...], digit: int) -> tuple[tuple[int, ...], int]:
    """Feed ``digit`` through a pipeline of k divide-by-two carries."""
    current = digit
    next_carries: list[int] = []
    for c in carries:
        nxt, out = divide_by_two_step(c, current)
        next_carries.append(nxt)
        current = out
    return tuple(next_carries), current


class DivideByTwoPowerTransducer:
    """Product of k copies of ``DivideByTwoTransducer``."""

    def __init__(self, k: int):
        if isinstance(k, bool) or not isinstance(k, int) or k < 1:
            raise ValueError(f"k must be an integer >= 1, got {k!r}")
        self.k = k
        self.start: tuple[int, ...] = (0,) * k

    def step(self, state: tuple[int, ...], digit: int) -> tuple[tuple[int, ...], int]:
        if len(state) != self.k:
            raise ValueError(f"state length {len(state)} != k={self.k}")
        if digit not in ALPHABET:
            raise ValueError(f"digit must be in {{-1,0,+1}}, got {digit!r}")
        return _compose_step(state, digit)

    def apply(self, word: WordLike) -> BalancedTernary:
        n = decode(word)
        val = v2(n)
        if n == 0:
            return encode(0)
        if val is None or val < self.k:
            raise ValueError(
                f"{n} is not divisible by 2^{self.k} (v2={val!r})"
            )
        lsd = digits(normalize(word))
        state = self.start
        out: list[int] = []
        for d in lsd:
            state, a = _compose_step(state, d)
            out.append(a)
        if any(state):
            raise ValueError(
                f"leftover carry tuple {state} after dividing {normalize(word).word()!r} "
                f"by 2^{self.k}"
            )
        return from_digits_lsd(out)

    def reachable_states(self) -> frozenset[tuple[int, ...]]:
        seen: set[tuple[int, ...]] = {self.start}
        queue: deque[tuple[int, ...]] = deque([self.start])
        while queue:
            st = queue.popleft()
            for a in ALPHABET:
                nxt, _ = _compose_step(st, a)
                if nxt not in seen:
                    seen.add(nxt)
                    queue.append(nxt)
        return frozenset(seen)

    def minimized_state_count(self) -> int:
        """Mealy minimization of the reachable product (computational)."""
        reachable = self.reachable_states()
        return minimize_mealy_count(reachable, ALPHABET, _compose_step)

    def complexity_report(self) -> dict[str, int]:
        reachable = self.reachable_states()
        return {
            "k": self.k,
            "naive_bound": 3**self.k,
            "reachable": len(reachable),
            "minimized": minimize_mealy_count(reachable, ALPHABET, _compose_step),
        }


def apply_divisible(word: WordLike, k: int) -> BalancedTernary:
    return DivideByTwoPowerTransducer(k).apply(word)


def _minimize_mealy(k: int, reachable: frozenset[tuple[int, ...]]) -> int:
    """Compatibility wrapper around the generic Mealy minimizer."""
    del k
    return minimize_mealy_count(reachable, ALPHABET, _compose_step)
