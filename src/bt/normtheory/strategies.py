"""Normalization strategies on coefficient words.

A — LSD→MSD (matches ``encode``).
B — highest noncanonical site first (MSD-downward).
C — parallel rounds: a maximal LSD-greedy set of non-adjacent legal sites.
D — ``encode(value)`` with zero rewrite steps.

All terminating strategies produce the same final word. Rewrite counts
need not agree.
"""

from __future__ import annotations

from dataclasses import dataclass

from bt.normtheory.coeffword import CoeffWord
from bt.normtheory.rewrite import legal_sites, normalize_step
from bt.representation import encode, from_digits_lsd


@dataclass(frozen=True)
class StrategyTrace:
    name: str
    start: CoeffWord
    result: CoeffWord
    steps: tuple[tuple[int, ...], ...]
    rewrite_count: int
    passes: int
    peak_abs: int
    peak_width: int
    max_carry_distance: int

    def as_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "start": list(self.start.coeffs),
            "result": list(self.result.coeffs),
            "rewrite_count": self.rewrite_count,
            "passes": self.passes,
            "peak_abs": self.peak_abs,
            "peak_width": self.peak_width,
            "max_carry_distance": self.max_carry_distance,
        }


def _peaks(word: CoeffWord, peak_abs: int, peak_width: int) -> tuple[int, int]:
    return max(peak_abs, word.peak()), max(peak_width, word.width())


def _apply_sites(word: CoeffWord, sites: tuple[int, ...]) -> CoeffWord:
    """Apply non-adjacent sites. Highest index first so lower writes stay valid."""
    out = word
    for i in sorted(sites, reverse=True):
        out = normalize_step(out, i)
    return out


def maximal_nonadjacent_sites(word: CoeffWord) -> tuple[int, ...]:
    """LSD-greedy maximal independent set of legal sites."""
    chosen: list[int] = []
    blocked: set[int] = set()
    for i in legal_sites(word):
        if i in blocked:
            continue
        chosen.append(i)
        blocked.add(i - 1)
        blocked.add(i + 1)
    return tuple(chosen)


def normalize_lsd_to_msd(word: CoeffWord) -> StrategyTrace:
    """Strategy A: always rewrite the lowest legal site."""
    current = word
    peak_abs, peak_width = current.peak(), current.width()
    steps: list[tuple[int, ...]] = []
    carry_dist = 0
    while True:
        sites = legal_sites(current)
        if not sites:
            break
        i = sites[0]
        current = normalize_step(current, i)
        peak_abs, peak_width = _peaks(current, peak_abs, peak_width)
        steps.append((i,))
        carry_dist = max(carry_dist, 1)
    return StrategyTrace(
        name="A",
        start=word,
        result=current,
        steps=tuple(steps),
        rewrite_count=len(steps),
        passes=len(steps),
        peak_abs=peak_abs,
        peak_width=peak_width,
        max_carry_distance=carry_dist,
    )


def normalize_msd_down(word: CoeffWord) -> StrategyTrace:
    """Strategy B: always rewrite the highest legal site."""
    current = word
    peak_abs, peak_width = current.peak(), current.width()
    steps: list[tuple[int, ...]] = []
    carry_dist = 0
    while True:
        sites = legal_sites(current)
        if not sites:
            break
        i = sites[-1]
        current = normalize_step(current, i)
        peak_abs, peak_width = _peaks(current, peak_abs, peak_width)
        steps.append((i,))
        carry_dist = max(carry_dist, 1)
    return StrategyTrace(
        name="B",
        start=word,
        result=current,
        steps=tuple(steps),
        rewrite_count=len(steps),
        passes=len(steps),
        peak_abs=peak_abs,
        peak_width=peak_width,
        max_carry_distance=carry_dist,
    )


def normalize_parallel(word: CoeffWord) -> StrategyTrace:
    """Strategy C: one maximal non-adjacent independent set per round."""
    current = word
    peak_abs, peak_width = current.peak(), current.width()
    steps: list[tuple[int, ...]] = []
    rewrite_count = 0
    carry_dist = 0
    while True:
        sites = maximal_nonadjacent_sites(current)
        if not sites:
            break
        current = _apply_sites(current, sites)
        peak_abs, peak_width = _peaks(current, peak_abs, peak_width)
        steps.append(sites)
        rewrite_count += len(sites)
        if sites:
            carry_dist = max(carry_dist, 1)
    return StrategyTrace(
        name="C",
        start=word,
        result=current,
        steps=tuple(steps),
        rewrite_count=rewrite_count,
        passes=len(steps),
        peak_abs=peak_abs,
        peak_width=peak_width,
        max_carry_distance=carry_dist,
    )


def normalize_encode(word: CoeffWord) -> StrategyTrace:
    """Strategy D: canonical encoder of ``value(P)``. Zero rewrite steps."""
    encoded = encode(word.value())
    result = CoeffWord(encoded.digits_lsd())
    return StrategyTrace(
        name="D",
        start=word,
        result=result,
        steps=(),
        rewrite_count=0,
        passes=0,
        peak_abs=word.peak(),
        peak_width=word.width(),
        max_carry_distance=0,
    )


def all_strategies(word: CoeffWord) -> dict[str, StrategyTrace]:
    return {
        "A": normalize_lsd_to_msd(word),
        "B": normalize_msd_down(word),
        "C": normalize_parallel(word),
        "D": normalize_encode(word),
    }


def normal_form(word: CoeffWord) -> CoeffWord:
    """Canonical coefficient word of ``value(P)`` via Strategy A."""
    return normalize_lsd_to_msd(word).result


def agrees_with_encode(word: CoeffWord) -> bool:
    nf = normal_form(word)
    encoded = encode(word.value())
    return from_digits_lsd(nf.coeffs) == encoded and nf.coeffs == encoded.digits_lsd()
