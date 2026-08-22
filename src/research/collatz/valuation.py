"""2-adic valuation and finite-precision classification of ``v2(3n+1)``.

``v2(n)`` is the largest ``k`` such that ``2^k`` divides ``n``. For ``n = 0``
this is ``+∞``, returned as ``None`` (same convention as ``v3``).

Precision convention for ``classify_collatz_valuation(residue, K)``:

Let ``r`` be a residue modulo ``2^K`` and ``y = (3r + 1) mod 2^K``.

- If ``y != 0``, then ``v2(3n+1) = v2(y)`` is **exact** and satisfies
  ``0 <= v2(y) < K``.
- If ``y == 0``, then ``v2(3n+1) >= K``. This is **not** an exact value:
  the cases ``v2 = K`` and ``v2 > K`` are indistinguishable modulo ``2^K``.

The label ``AT_LEAST_K`` means the second case. There is no exact-``K``
class at precision ``K``.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

AT_LEAST_K: Literal["AT_LEAST_K"] = "AT_LEAST_K"


def v2(n: int) -> int | None:
    """2-adic valuation ``v_2(n)``. ``None`` means ``v_2(0) = ∞``."""
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be int, got {type(n).__name__}")
    if n == 0:
        return None
    v = 0
    # Work with the integer as-is; sign does not affect 2-adic valuation.
    m = n if n > 0 else -n
    while m % 2 == 0:
        m //= 2
        v += 1
    return v


@dataclass(frozen=True)
class ValuationClassification:
    """Classification of ``v2(3n+1)`` from ``n mod 2^K``.

    ``exact_k`` is set iff the valuation is strictly less than ``precision``.
    Otherwise ``kind`` is ``AT_LEAST_K`` and the valuation is at least
    ``precision``.
    """

    precision: int
    exact_k: int | None

    @property
    def kind(self) -> str:
        return "EXACT" if self.exact_k is not None else AT_LEAST_K

    @property
    def is_exact(self) -> bool:
        return self.exact_k is not None

    def label(self) -> str:
        if self.exact_k is None:
            return AT_LEAST_K
        return str(self.exact_k)


def classify_collatz_valuation(
    residue: int, precision: int
) -> ValuationClassification:
    """Classify ``v2(3n+1)`` given ``n ≡ residue (mod 2^precision)``.

    ``residue`` is reduced modulo ``2^K`` into ``{0, ..., 2^K - 1}``.

    For odd residues, ``3r+1`` is even, so an exact result satisfies
    ``k >= 1``. For even residues, ``3r+1`` is odd and the exact result is
    ``k = 0`` (the accelerated odd-only map is not applied to even ``n``).
    """
    if isinstance(precision, bool) or not isinstance(precision, int) or precision < 1:
        raise ValueError(
            f"precision K must be an integer >= 1, got {precision!r}"
        )
    if isinstance(residue, bool) or not isinstance(residue, int):
        raise TypeError(f"residue must be int, got {type(residue).__name__}")

    modulus = 1 << precision
    r = residue % modulus
    y = (3 * r + 1) % modulus
    if y == 0:
        return ValuationClassification(precision=precision, exact_k=None)
    k = v2(y)
    assert k is not None and 0 <= k < precision
    return ValuationClassification(precision=precision, exact_k=k)
