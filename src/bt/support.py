"""Support-set operations on canonical balanced ternary expansions."""

from __future__ import annotations

from bt.representation import digits, encode


def _require_int(n: int, name: str = "n") -> int:
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"{name} must be int, got {type(n).__name__}")
    return n


def support(n: int) -> tuple[int, ...]:
    """Positions ``i`` with ``a_i != 0``, LSD-first."""
    return tuple(i for i, a in enumerate(digits(encode(_require_int(n)))) if a != 0)


def gap_sequence(n: int) -> tuple[int, ...]:
    """Gaps between successive nonzero LSD indices. Empty if ``w(n) < 2``."""
    supp = support(n)
    if len(supp) < 2:
        return ()
    return tuple(supp[i + 1] - supp[i] - 1 for i in range(len(supp) - 1))


def support_union(*values: int) -> frozenset[int]:
    out: set[int] = set()
    for n in values:
        out.update(support(n))
    return frozenset(out)


def support_intersection(*values: int) -> frozenset[int]:
    if not values:
        return frozenset()
    sets = [set(support(n)) for n in values]
    return frozenset(sets[0].intersection(*sets[1:]))


def support_sumset(a: int, b: int) -> frozenset[int]:
    """``{i + j : i in supp(a), j in supp(b)}``."""
    return frozenset(i + j for i in support(a) for j in support(b))


def support_difference_set(a: int, b: int) -> frozenset[int]:
    """``{i - j : i in supp(a), j in supp(b)}``."""
    return frozenset(i - j for i in support(a) for j in support(b))


def support_reflection(n: int, *, pivot: int = 0) -> frozenset[int]:
    """Reflect support indices through ``pivot``."""
    return frozenset(2 * pivot - i for i in support(n))
