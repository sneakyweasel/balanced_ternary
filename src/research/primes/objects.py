"""Sparse-prime helpers already present in the repository."""

from __future__ import annotations

from bt.arithmetic import is_prime
from bt.metrics import weight
from bt.representation import encode


def _require_k(k: int) -> int:
    if isinstance(k, bool) or not isinstance(k, int) or k < 0:
        raise ValueError(f"k must be a nonnegative int, got {k!r}")
    return k


def sparse_primes(k: int, bound: int) -> tuple[int, ...]:
    k = _require_k(k)
    return tuple(n for n in range(2, bound + 1) if weight(encode(n)) <= k and is_prime(n))
