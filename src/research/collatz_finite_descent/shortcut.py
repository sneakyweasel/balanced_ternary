"""Shortcut Collatz map. Not hailstone ``C`` and not odd-only ``T``.

Even: ``n' = n/2``. Odd: ``n' = (a n + b)/2`` with default ``(a,b)=(3,1)``.
The control is the parity of the current state, not a free letter.
"""

from __future__ import annotations

CONTROL_EVEN = "E"
CONTROL_ODD = "O"

TERMINAL_CYCLE_3_1: frozenset[int] = frozenset({1, 2})


def require_positive_int(n: int, name: str = "n") -> int:
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"{name} must be int, got {type(n).__name__}")
    if n <= 0:
        raise ValueError(f"{name} must be a positive integer, got {n}")
    return n


def parity_control(n: int) -> str:
    n = require_positive_int(n)
    return CONTROL_EVEN if n % 2 == 0 else CONTROL_ODD


def shortcut_step(n: int, odd_mul: int = 3, odd_add: int = 1) -> int:
    """One exact shortcut step. ``odd_mul`` must be odd so the image is an integer."""
    n = require_positive_int(n)
    if isinstance(odd_mul, bool) or not isinstance(odd_mul, int) or odd_mul % 2 == 0:
        raise ValueError(f"odd_mul must be an odd integer, got {odd_mul!r}")
    if isinstance(odd_add, bool) or not isinstance(odd_add, int) or odd_add % 2 == 0:
        raise ValueError(f"odd_add must be an odd integer, got {odd_add!r}")
    if n % 2 == 0:
        return n // 2
    return (odd_mul * n + odd_add) // 2


def iterate_shortcut(n: int, steps: int, odd_mul: int = 3, odd_add: int = 1) -> int:
    if isinstance(steps, bool) or not isinstance(steps, int) or steps < 0:
        raise ValueError(f"steps must be a nonnegative integer, got {steps!r}")
    current = require_positive_int(n)
    for _ in range(steps):
        current = shortcut_step(current, odd_mul, odd_add)
    return current


def parity_word(n: int, length: int, odd_mul: int = 3, odd_add: int = 1) -> tuple[str, ...]:
    """The unique length-``length`` parity word of ``n``."""
    if isinstance(length, bool) or not isinstance(length, int) or length < 0:
        raise ValueError(f"length must be a nonnegative integer, got {length!r}")
    current = require_positive_int(n)
    word: list[str] = []
    for _ in range(length):
        word.append(parity_control(current))
        current = shortcut_step(current, odd_mul, odd_add)
    return tuple(word)


def apply_word(
    n: int,
    word: tuple[str, ...],
    odd_mul: int = 3,
    odd_add: int = 1,
) -> int:
    """Apply ``word`` if and only if it is the actual parity sequence of ``n``."""
    current = require_positive_int(n)
    for control in word:
        actual = parity_control(current)
        if control != actual:
            raise ValueError(f"word {word!r} is not legal at {n}: expected {actual}")
        current = shortcut_step(current, odd_mul, odd_add)
    return current


def cycle_containing(start: int, odd_mul: int = 3, odd_add: int = 1) -> frozenset[int]:
    """Least cycle reached from ``start`` under the shortcut map."""
    current = require_positive_int(start)
    seen: dict[int, int] = {}
    step = 0
    while current not in seen:
        seen[current] = step
        current = shortcut_step(current, odd_mul, odd_add)
        step += 1
        if step > 10_000:
            raise RuntimeError("cycle search exceeded 10000 steps")
    cycle_start = seen[current]
    return frozenset(value for value, index in seen.items() if index >= cycle_start)


def is_terminal(n: int, odd_mul: int = 3, odd_add: int = 1) -> bool:
    if odd_mul == 3 and odd_add == 1:
        return require_positive_int(n) in TERMINAL_CYCLE_3_1
    return require_positive_int(n) in cycle_containing(1, odd_mul, odd_add)


def predecessors(m: int, odd_mul: int = 3, odd_add: int = 1) -> tuple[int, ...]:
    """Exact positive predecessors of ``m``.

    Always ``2m``. Also ``(2m - odd_add)/odd_mul`` when that value is a
    positive odd integer.
    """
    m = require_positive_int(m, "m")
    found = [2 * m]
    numerator = 2 * m - odd_add
    if numerator > 0 and numerator % odd_mul == 0:
        pred = numerator // odd_mul
        if pred > 0 and pred % 2 == 1:
            found.append(pred)
    return tuple(sorted(set(found)))
