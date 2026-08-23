"""Addition, convolution, and FMA via coefficients, then normalize.

Values always match ``encode`` of the integer result. Costs need not.
There is no generic sparsity-preservation theorem.
"""

from __future__ import annotations

from dataclasses import dataclass

from bt.normtheory.coeffword import CoeffWord
from bt.normtheory.strategies import StrategyTrace, normalize_lsd_to_msd
from bt.representation import encode


def add_coeff(p: CoeffWord, q: CoeffWord) -> CoeffWord:
    n = max(p.width(), q.width())
    return CoeffWord(tuple(p.coefficient(i) + q.coefficient(i) for i in range(n)))


def mul_coeff(p: CoeffWord, q: CoeffWord) -> CoeffWord:
    """Convolution. Does not require trit coefficients."""
    if p.coeffs == (0,) or q.coeffs == (0,):
        return CoeffWord((0,))
    out = [0] * (p.width() + q.width() - 1)
    for i, a in enumerate(p.coeffs):
        if a == 0:
            continue
        for j, b in enumerate(q.coeffs):
            out[i + j] += a * b
    return CoeffWord(tuple(out))


def normalize_add(p: CoeffWord, q: CoeffWord) -> StrategyTrace:
    return normalize_lsd_to_msd(add_coeff(p, q))


def normalize_mul(p: CoeffWord, q: CoeffWord) -> StrategyTrace:
    return normalize_lsd_to_msd(mul_coeff(p, q))


def fma_fused(p: CoeffWord, q: CoeffWord, r: CoeffWord) -> StrategyTrace:
    """``normalize(PQ + R)`` in one sweep."""
    return normalize_lsd_to_msd(add_coeff(mul_coeff(p, q), r))


def fma_staged(p: CoeffWord, q: CoeffWord, r: CoeffWord) -> StrategyTrace:
    """``normalize(normalize(PQ) + R)``."""
    pq = normalize_lsd_to_msd(mul_coeff(p, q)).result
    return normalize_lsd_to_msd(add_coeff(pq, r))


@dataclass(frozen=True)
class FMAComparison:
    fused: StrategyTrace
    staged: StrategyTrace
    values_equal: bool
    fused_cheaper: bool
    staged_cheaper: bool
    rewrite_gap: int

    def as_dict(self) -> dict[str, object]:
        return {
            "fused_rewrites": self.fused.rewrite_count,
            "staged_rewrites": self.staged.rewrite_count,
            "values_equal": self.values_equal,
            "fused_cheaper": self.fused_cheaper,
            "staged_cheaper": self.staged_cheaper,
            "rewrite_gap": self.rewrite_gap,
            "result": list(self.fused.result.coeffs),
        }


def compare_fma(p: CoeffWord, q: CoeffWord, r: CoeffWord) -> FMAComparison:
    fused = fma_fused(p, q, r)
    staged = fma_staged(p, q, r)
    gap = fused.rewrite_count - staged.rewrite_count
    return FMAComparison(
        fused=fused,
        staged=staged,
        values_equal=fused.result.coeffs == staged.result.coeffs
        and fused.result.value() == staged.result.value(),
        fused_cheaper=fused.rewrite_count < staged.rewrite_count,
        staged_cheaper=staged.rewrite_count < fused.rewrite_count,
        rewrite_gap=gap,
    )


def add_matches_encode(p: CoeffWord, q: CoeffWord) -> bool:
    nf = normalize_add(p, q).result
    return nf.coeffs == encode(p.value() + q.value()).digits_lsd()


def mul_matches_encode(p: CoeffWord, q: CoeffWord) -> bool:
    nf = normalize_mul(p, q).result
    return nf.coeffs == encode(p.value() * q.value()).digits_lsd()
