"""Phase-0 locality of binary integer maps through D and the 1-jet.

``DLocal`` in Lean is ``H(x,y)=G(D(x),D(y))``. Here we also test
whether ``D ∘ H`` factors through ``(D(x),D(y))`` or through the
1-jet ``(D(x),D(y),lsd(x),lsd(y))``.
"""

from __future__ import annotations

from collections.abc import Callable
from itertools import product
from math import gcd

from bt.calculus.cubic import prefixes_at
from bt.calculus.derivative import D, lsd

BinOp = Callable[[int, int], int]
WINDOW = tuple(prefixes_at(3))


def _factors_through(H: BinOp, key_of, window: tuple[int, ...] = WINDOW) -> bool:
    seen: dict[object, int] = {}
    for x, y in product(window, window):
        key = key_of(x, y)
        val = H(x, y)
        prev = seen.get(key)
        if prev is None:
            seen[key] = val
        elif prev != val:
            return False
    return True


def is_d_local(H: BinOp, window: tuple[int, ...] = WINDOW) -> bool:
    """``H(x,y)`` is a function of ``(D(x), D(y))``."""

    return _factors_through(H, lambda x, y: (D(x), D(y)), window)


def is_lsd_local(H: BinOp, window: tuple[int, ...] = WINDOW) -> bool:
    """``H(x,y)`` is a function of ``(lsd(x), lsd(y))``."""

    return _factors_through(H, lambda x, y: (int(lsd(x)), int(lsd(y))), window)


def locality_row(name: str, H: BinOp, window: tuple[int, ...] = WINDOW) -> dict[str, object]:
    dH = lambda x, y: D(H(x, y))
    return {
        "name": name,
        "H_d_local": is_d_local(H, window),
        "H_lsd_local": is_lsd_local(H, window),
        "DH_d_local": is_d_local(dH, window),
        "DH_lsd_local": is_lsd_local(dH, window),
    }


def named_ops() -> list[tuple[str, BinOp]]:
    return [
        ("add", lambda x, y: x + y),
        ("sub", lambda x, y: x - y),
        ("mul", lambda x, y: x * y),
        ("max", max),
        ("min", min),
        ("gcd", lambda x, y: gcd(x, y)),
        ("D_add", lambda x, y: D(x + y)),
        ("D_mul", lambda x, y: D(x * y)),
        ("D_max", lambda x, y: D(max(x, y))),
        ("D_min", lambda x, y: D(min(x, y))),
    ]


def named_report(window: tuple[int, ...] = WINDOW) -> list[dict[str, object]]:
    return [locality_row(name, H, window) for name, H in named_ops()]


def affine_dH_d_local(window: tuple[int, ...] = WINDOW) -> list[tuple[int, int, int, int]]:
    """``(a,b,c,d)`` in ``[-2,2]`` for which ``D(axy+bx+cy+d)`` is D-local."""

    hits = []
    for a, b, c, d in product(range(-2, 3), repeat=4):
        H = lambda x, y, a=a, b=b, c=c, d=d: a * x * y + b * x + c * y + d
        if is_d_local(lambda x, y: D(H(x, y)), window):
            hits.append((a, b, c, d))
    return hits
