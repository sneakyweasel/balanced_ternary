"""The balanced trit as an algebraic type.

``Trit = {-1, 0, +1}`` with lattice operations ``min`` / ``max`` and
order-reversing involution ``neg``. This is not a Boolean algebra:
``max(a, neg(a))`` is not identically ``+1``.
"""

from __future__ import annotations

from enum import IntEnum


class Trit(IntEnum):
    """Canonical balanced trit. Values are ordinary integers ``-1, 0, +1``."""

    MINUS = -1
    ZERO = 0
    PLUS = 1


TRITS: tuple[Trit, Trit, Trit] = (Trit.MINUS, Trit.ZERO, Trit.PLUS)


def as_trit(value: int) -> Trit:
    """Coerce ``value in {-1, 0, +1}`` to :class:`Trit`. Does not reduce modulo 3."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"trit must be int in {{-1,0,+1}}, got {type(value).__name__}")
    if value not in (-1, 0, 1):
        raise ValueError(f"trit must be in {{-1,0,+1}}, got {value!r}")
    return Trit(value)


def neg(a: Trit | int) -> Trit:
    return as_trit(-int(as_trit(int(a))))


def trit_min(a: Trit | int, b: Trit | int) -> Trit:
    return as_trit(min(int(as_trit(int(a))), int(as_trit(int(b)))))


def trit_max(a: Trit | int, b: Trit | int) -> Trit:
    return as_trit(max(int(as_trit(int(a))), int(as_trit(int(b)))))


def sign_trit(n: int) -> Trit:
    """``sign(n)`` as a trit: ``-1`` if ``n<0``, ``0`` if ``n=0``, ``+1`` if ``n>0``."""
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be int, got {type(n).__name__}")
    if n < 0:
        return Trit.MINUS
    if n > 0:
        return Trit.PLUS
    return Trit.ZERO


def compare(a: Trit | int, b: Trit | int) -> Trit:
    """Three-way comparison of trits: ``sign(a-b)``."""
    return sign_trit(int(as_trit(int(a))) - int(as_trit(int(b))))


def le(a: Trit | int, b: Trit | int) -> bool:
    return int(as_trit(int(a))) <= int(as_trit(int(b)))


def is_bounded_lattice() -> bool:
    """``(Trit, min, max)`` is the 3-element chain, hence a bounded lattice."""
    bot, top = Trit.MINUS, Trit.PLUS
    for a in TRITS:
        if trit_min(bot, a) != bot or trit_max(top, a) != top:
            return False
        if trit_min(a, a) != a or trit_max(a, a) != a:
            return False
        for b in TRITS:
            if trit_min(a, b) != trit_min(b, a) or trit_max(a, b) != trit_max(b, a):
                return False
            for c in TRITS:
                if trit_min(a, trit_min(b, c)) != trit_min(trit_min(a, b), c):
                    return False
                if trit_max(a, trit_max(b, c)) != trit_max(trit_max(a, b), c):
                    return False
                if trit_max(a, trit_min(a, b)) != a or trit_min(a, trit_max(a, b)) != a:
                    return False
    return True


def is_distributive_lattice() -> bool:
    for a in TRITS:
        for b in TRITS:
            for c in TRITS:
                left = trit_min(a, trit_max(b, c))
                right = trit_max(trit_min(a, b), trit_min(a, c))
                if left != right:
                    return False
                left = trit_max(a, trit_min(b, c))
                right = trit_min(trit_max(a, b), trit_max(a, c))
                if left != right:
                    return False
    return True


def is_de_morgan() -> bool:
    """``neg`` is an order-reversing involution satisfying De Morgan laws."""
    for a in TRITS:
        if neg(neg(a)) != a:
            return False
        for b in TRITS:
            if neg(trit_min(a, b)) != trit_max(neg(a), neg(b)):
                return False
            if neg(trit_max(a, b)) != trit_min(neg(a), neg(b)):
                return False
            if le(a, b) != le(neg(b), neg(a)):
                return False
    return True


def is_kleene_algebra() -> bool:
    """Kleene inequality ``min(a, neg(a)) ≤ max(b, neg(b))`` on the 3-chain."""
    if not (is_bounded_lattice() and is_distributive_lattice() and is_de_morgan()):
        return False
    for a in TRITS:
        for b in TRITS:
            if not le(trit_min(a, neg(a)), trit_max(b, neg(b))):
                return False
    return True


def is_boolean_algebra() -> bool:
    """Complement law. False on ``Trit``: ``max(0, neg(0)) = 0 ≠ +1``."""
    for a in TRITS:
        if trit_max(a, neg(a)) != Trit.PLUS:
            return False
        if trit_min(a, neg(a)) != Trit.MINUS:
            return False
    return True


def algebraic_name() -> str:
    """Verified name after checking axioms. Not a Boolean algebra."""
    if is_kleene_algebra() and not is_boolean_algebra():
        return "3-element Kleene algebra (bounded distributive De Morgan lattice; not Boolean)"
    if is_bounded_lattice() and is_de_morgan() and not is_boolean_algebra():
        return "bounded De Morgan lattice (not Boolean)"
    if is_bounded_lattice():
        return "bounded lattice"
    return "ordered set {-1 < 0 < +1}"
