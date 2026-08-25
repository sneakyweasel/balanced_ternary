"""Discovery of the missing residual for ``D(x+y)``.

The unary factorization ``D(x+y)=G(D(x),D(y))`` is already known false.
This module searches candidate residuals with existing ``D`` and ``lsd``
only. It does not install a carry table into the search.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable

from bt.calculus.derivative import D, lsd
from bt.calculus.jets import integer_jet
from bt.operators import lsd_digit

TRITS: tuple[int, int, int] = (-1, 0, 1)
Pair = tuple[int, int]
ResidualFn = Callable[[int, int], object]


def _lsd(n: int) -> int:
    return int(lsd(n))


def correction(x: int, y: int) -> int:
    """``D(x+y)-D(x)-D(y)``. Not assumed to be a carry table."""
    return D(x + y) - D(x) - D(y)


def r_digit_pair(x: int, y: int) -> Pair:
    return (_lsd(x), _lsd(y))


def r_lsd_sum(x: int, y: int) -> int:
    return _lsd(x + y)


def r_digit_sum(x: int, y: int) -> int:
    return _lsd(x) + _lsd(y)


def collisions(
    values: tuple[int, ...],
) -> dict[Pair, tuple[Pair, ...]]:
    """Pairs with the same ``(D(x),D(y))`` and more than one ``D(x+y)``."""
    buckets: dict[Pair, dict[int, list[Pair]]] = defaultdict(lambda: defaultdict(list))
    for x in values:
        for y in values:
            buckets[(D(x), D(y))][D(x + y)].append((x, y))
    out: dict[Pair, tuple[Pair, ...]] = {}
    for key, by_h in buckets.items():
        if len(by_h) < 2:
            continue
        witnesses: list[Pair] = []
        for group in by_h.values():
            witnesses.append(group[0])
        out[key] = tuple(witnesses)
    return out


def residual_collision(
    values: tuple[int, ...],
    residual: ResidualFn,
) -> tuple[Pair, Pair] | None:
    """Same ``(D(x),D(y),R)``, different ``D(x+y)``."""
    buckets: dict[tuple[object, ...], dict[int, Pair]] = defaultdict(dict)
    for x in values:
        for y in values:
            key = (D(x), D(y), residual(x, y))
            buckets[key][D(x + y)] = (x, y)
    for by_h in buckets.values():
        if len(by_h) > 1:
            first, second = list(by_h.values())[:2]
            return first, second
    return None


def sample_range(limit: int) -> tuple[int, ...]:
    return tuple(range(-limit, limit + 1))


def step(state: int, left: int, right: int) -> tuple[int, int]:
    """One LSD-first addition step from ``D`` and ``lsd``, not a lookup table."""
    total = state + left + right
    return D(total), lsd_digit(total)


def streaming_reachable(alphabet: tuple[int, ...], start: int = 0) -> frozenset[int]:
    seen: set[int] = {start}
    queue = [start]
    while queue:
        state = queue.pop()
        for left in alphabet:
            for right in alphabet:
                nxt, _out = step(state, left, right)
                if nxt not in seen:
                    seen.add(nxt)
                    queue.append(nxt)
    return frozenset(seen)


def stream_sum(x: int, y: int, length: int | None = None) -> tuple[int, ...]:
    """Canonical sum digits generated from the discovered residual step."""
    if length is None:
        bound = max(abs(x), abs(y), 1)
        length = 2
        span = 1
        while span <= 3 * bound:
            span *= 3
            length += 1
    ax = integer_jet(x, length)
    ay = integer_jet(y, length)
    state = 0
    out: list[int] = []
    for i in range(length):
        state, digit = step(state, ax[i], ay[i])
        out.append(digit)
    while state:
        state, digit = step(state, 0, 0)
        out.append(digit)
        if len(out) > 32:
            break
    return tuple(out)


def pack_digits(digits: tuple[int, ...]) -> int:
    acc = 0
    for digit in reversed(digits):
        acc = digit + 3 * acc
    return acc


def discovery_report(limit: int = 12) -> dict[str, object]:
    """Bounded residual search. Not an exact theorem."""
    values = sample_range(limit)
    coll = collisions(values)
    fiber = {
        (x, y): (D(x), D(y), D(x + y), correction(x, y))
        for x, y in ((0, 0), (1, 1), (-1, -1), (0, -1))
    }
    corrections = {correction(x, y) for x in values for y in values}
    digit_pair_ok = residual_collision(values, r_digit_pair) is None
    lsd_sum_hit = residual_collision(values, r_lsd_sum)
    digit_sum_ok = residual_collision(values, r_digit_sum) is None
    corr_ok = residual_collision(values, correction) is None
    reachable = streaming_reachable(TRITS)
    return {
        "scope": "BOUNDED",
        "status": "OBSERVATION",
        "sample_limit": limit,
        "naive_collision_count": len(coll),
        "naive_witness": (1, 1),
        "lsd_sum_collision": lsd_sum_hit,
        "digit_pair_separates": digit_pair_ok,
        "digit_sum_separates": digit_sum_ok,
        "correction_separates": corr_ok,
        "correction_values": tuple(sorted(corrections)),
        "streaming_reachable": tuple(sorted(reachable)),
        "fiber": fiber,
        "raw_digit_pairs": 9,
    }
