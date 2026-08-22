"""Sparse perfect-power searches already present in the repository."""

from __future__ import annotations

from bt.metrics import weight
from bt.representation import encode


def _require_k(k: int) -> int:
    if isinstance(k, bool) or not isinstance(k, int) or k < 0:
        raise ValueError(f"k must be a nonnegative int, got {k!r}")
    return k


def sparse_squares(k: int, max_root: int) -> tuple[int, ...]:
    """Squares ``m^2`` with ``w(m^2) <= k`` and ``0 <= m <= max_root``."""
    k = _require_k(k)
    out = []
    for m in range(0, max_root + 1):
        sq = m * m
        if weight(encode(sq)) <= k:
            out.append(sq)
    return tuple(out)


def sparse_cubes(k: int, max_root: int) -> tuple[int, ...]:
    k = _require_k(k)
    out = []
    for m in range(0, max_root + 1):
        cu = m * m * m
        if weight(encode(cu)) <= k:
            out.append(cu)
    return tuple(out)


def weight_one_squares() -> str:
    """Closed form for squares in ``W_1``.

    ``w(n) <= 1`` means ``n = 0`` or ``n = ±3^a``. The only squares are
    ``0`` and ``(3^t)^2 = 3^{2t}``.
    """
    return "W_1 ∩ squares = {0} ∪ {3^{2t} : t >= 0}"
