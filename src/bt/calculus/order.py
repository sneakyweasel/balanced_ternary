"""Three-way comparison as a trit-valued operation."""

from __future__ import annotations

from bt.calculus.trit import Trit, as_trit, sign_trit


def _require_int(n: int, name: str = "n") -> int:
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"{name} must be int, got {type(n).__name__}")
    return n


def cmp3(x: int, y: int) -> Trit:
    """``cmp3(x, y) = sign(x - y)`` in ``{-1, 0, +1}``."""
    return sign_trit(_require_int(x, "x") - _require_int(y, "y"))


def cmp3_trit(a: Trit | int, b: Trit | int) -> Trit:
    return sign_trit(int(as_trit(int(a))) - int(as_trit(int(b))))
