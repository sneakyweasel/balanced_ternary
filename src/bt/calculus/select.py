"""Three-way selection and piecewise arithmetic via trits.

The primitive is ``select3(c, x_minus, x_zero, x_plus)``. Other
``trit_if`` sketches are documented only; they are not competing primitives.
"""

from __future__ import annotations

from bt.calculus.order import cmp3
from bt.calculus.trit import Trit, as_trit, sign_trit


def _require_int(n: int, name: str = "n") -> int:
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"{name} must be int, got {type(n).__name__}")
    return n


def select3(c: Trit | int, x_minus: int, x_zero: int, x_plus: int) -> int:
    """Select by trit: ``c=-1 → x_minus``, ``c=0 → x_zero``, ``c=+1 → x_plus``."""
    t = as_trit(int(c))
    xm = _require_int(x_minus, "x_minus")
    xz = _require_int(x_zero, "x_zero")
    xp = _require_int(x_plus, "x_plus")
    if t is Trit.MINUS:
        return xm
    if t is Trit.ZERO:
        return xz
    return xp


def abs_z(n: int) -> int:
    n = _require_int(n)
    return select3(sign_trit(n), -n, 0, n)


def max_z(x: int, y: int) -> int:
    x = _require_int(x, "x")
    y = _require_int(y, "y")
    return select3(cmp3(x, y), y, x, x)


def min_z(x: int, y: int) -> int:
    x = _require_int(x, "x")
    y = _require_int(y, "y")
    return select3(cmp3(x, y), x, x, y)


def sign_z(n: int) -> int:
    return int(sign_trit(_require_int(n)))


def clamp_z(n: int, lo: int, hi: int) -> int:
    n = _require_int(n)
    lo = _require_int(lo, "lo")
    hi = _require_int(hi, "hi")
    if hi < lo:
        raise ValueError(f"clamp requires lo <= hi, got {lo} > {hi}")
    return min_z(max_z(n, lo), hi)


def median_z(x: int, y: int, z: int) -> int:
    x = _require_int(x, "x")
    y = _require_int(y, "y")
    z = _require_int(z, "z")
    return max_z(min_z(x, y), min_z(max_z(x, y), z))
