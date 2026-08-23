"""Rewrite, carry, and depth measures for coefficient normalization.

No log-depth claim. Parallel depth is the number of Strategy C rounds.
"""

from __future__ import annotations

from dataclasses import dataclass
import random

from bt.normtheory.coeffword import CoeffWord
from bt.normtheory.strategies import (
    StrategyTrace,
    all_strategies,
    normalize_lsd_to_msd,
    normalize_parallel,
)


@dataclass(frozen=True)
class ComplexityReport:
    word: tuple[int, ...]
    value: int
    excess: int
    l1: int
    sequential_depth: int
    parallel_depth: int
    rewrite_A: int
    rewrite_B: int
    rewrite_C: int
    rewrite_D: int
    peak_abs_A: int
    peak_width_A: int
    strategies_agree: bool

    def as_dict(self) -> dict[str, object]:
        return {
            "word": list(self.word),
            "value": self.value,
            "excess": self.excess,
            "l1": self.l1,
            "sequential_depth": self.sequential_depth,
            "parallel_depth": self.parallel_depth,
            "rewrite_A": self.rewrite_A,
            "rewrite_B": self.rewrite_B,
            "rewrite_C": self.rewrite_C,
            "rewrite_D": self.rewrite_D,
            "peak_abs_A": self.peak_abs_A,
            "peak_width_A": self.peak_width_A,
            "strategies_agree": self.strategies_agree,
        }


def measure(word: CoeffWord) -> ComplexityReport:
    traces = all_strategies(word)
    results = {name: t.result.coeffs for name, t in traces.items()}
    agree = len(set(results.values())) == 1
    return ComplexityReport(
        word=word.coeffs,
        value=word.value(),
        excess=word.excess(),
        l1=word.l1(),
        sequential_depth=traces["A"].rewrite_count,
        parallel_depth=traces["C"].passes,
        rewrite_A=traces["A"].rewrite_count,
        rewrite_B=traces["B"].rewrite_count,
        rewrite_C=traces["C"].rewrite_count,
        rewrite_D=0,
        peak_abs_A=traces["A"].peak_abs,
        peak_width_A=traces["A"].peak_width,
        strategies_agree=agree,
    )


def family_power(k: int) -> CoeffWord:
    """Coefficient word whose value is ``3^k``: singleton at index ``k``."""
    if k < 0:
        raise ValueError("k must be >= 0")
    return CoeffWord((0,) * k + (1,))


def family_power_plus(k: int, delta: int) -> CoeffWord:
    return CoeffWord.from_value(3**k + delta)


def family_all_c(width: int, c: int) -> CoeffWord:
    if width < 1:
        raise ValueError("width must be >= 1")
    return CoeffWord((c,) * width)


def family_alternating(width: int, c: int) -> CoeffWord:
    if width < 1:
        raise ValueError("width must be >= 1")
    return CoeffWord(tuple(c if i % 2 == 0 else -c for i in range(width)))


def family_sparse_product(left: int, right: int) -> CoeffWord:
    """Convolution of two singleton words, before normalization."""
    return CoeffWord.from_value(left * right)


def random_word(width: int, bound: int, rng: random.Random | None = None) -> CoeffWord:
    if width < 1:
        raise ValueError("width must be >= 1")
    if bound < 0:
        raise ValueError("bound must be >= 0")
    r = rng or random.Random(0)
    return CoeffWord(tuple(r.randint(-bound, bound) for _ in range(width)))


def enumerate_words(width: int, bound: int) -> list[CoeffWord]:
    """All words of exact width with coefficients in ``[-bound, bound]``.

    Practical domains: ``width<=5`` and ``|c|<=3``, or ``width<=8`` and
    ``|c|<=2``. Larger boxes are not exact-enumerable here.
    """
    if width < 1 or bound < 0:
        raise ValueError("width >= 1 and bound >= 0 required")
    if width > 8 or (width > 5 and bound > 2) or bound > 3:
        raise ValueError(
            f"enumeration box width={width} bound={bound} is not in the "
            "practical exhaustive range"
        )
    alphabet = list(range(-bound, bound + 1))
    out: list[CoeffWord] = []

    def rec(prefix: list[int]) -> None:
        if len(prefix) == width:
            out.append(CoeffWord(tuple(prefix)))
            return
        for c in alphabet:
            prefix.append(c)
            rec(prefix)
            prefix.pop()

    rec([])
    return out


def worst_case(words: list[CoeffWord], key: str = "rewrite_A") -> tuple[CoeffWord, ComplexityReport]:
    best_word = words[0]
    best = measure(words[0])
    best_val = getattr(best, key)
    for w in words[1:]:
        rep = measure(w)
        val = getattr(rep, key)
        if val > best_val:
            best_word, best, best_val = w, rep, val
    return best_word, best


def profile_families(max_k: int = 8) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for k in range(max_k + 1):
        for name, word in (
            (f"3^{k}", family_power(k)),
            (f"3^{k}+1", family_power_plus(k, 1)),
            (f"3^{k}-1", family_power_plus(k, -1)),
            (f"all-2@{k or 1}", family_all_c(max(k, 1), 2)),
            (f"alt-2@{k or 1}", family_alternating(max(k, 1), 2)),
        ):
            row = measure(word).as_dict()
            row["family"] = name
            rows.append(row)
    return rows


def sequential_vs_parallel(word: CoeffWord) -> tuple[StrategyTrace, StrategyTrace]:
    return normalize_lsd_to_msd(word), normalize_parallel(word)
