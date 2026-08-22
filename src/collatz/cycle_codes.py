"""Primitivity and canonical rotation of accelerated exponent codes.

A nonempty word ``k`` is primitive when it is not ``u`` repeated ``r``
times for any ``r > 1``. Equivalently, the shortest root of ``k`` is
``k`` itself.

Canonical representative of a rotation class: the lexicographically
minimal rotation. Ties keep the earliest index in the original word.
"""

from __future__ import annotations

from collatz.cylinders import parse_ks


def exponent_root(code: tuple[int, ...] | str | list[int]) -> tuple[int, ...]:
    """Shortest ``u`` such that ``code = u repeated r`` for some ``r >= 1``."""
    ks = parse_ks(code)
    p = len(ks)
    if p == 0:
        return ()
    for length in range(1, p + 1):
        if p % length != 0:
            continue
        root = ks[:length]
        if root * (p // length) == ks:
            return root
    return ks


def is_primitive(code: tuple[int, ...] | str | list[int]) -> bool:
    """True iff ``code`` is nonempty and equal to its shortest root."""
    ks = parse_ks(code)
    if not ks:
        return False
    return exponent_root(ks) == ks


def rotations(code: tuple[int, ...] | str | list[int]) -> tuple[tuple[int, ...], ...]:
    """All cyclic rotations, in order of the starting index."""
    ks = parse_ks(code)
    if not ks:
        return ()
    p = len(ks)
    return tuple(ks[i:] + ks[:i] for i in range(p))


def lex_min_rotation(code: tuple[int, ...] | str | list[int]) -> tuple[int, ...]:
    """Lexicographically minimal rotation of a nonempty code."""
    ks = parse_ks(code)
    if not ks:
        raise ValueError("canonical rotation is undefined for the empty word")
    return min(rotations(ks))


def rotation_index_of_canonical(code: tuple[int, ...] | str | list[int]) -> int:
    """Smallest index ``i`` whose rotation equals the lex-min rotation."""
    ks = parse_ks(code)
    canonical = lex_min_rotation(ks)
    for i, rot in enumerate(rotations(ks)):
        if rot == canonical:
            return i
    raise ArithmeticError("canonical rotation missing from the rotation list")
