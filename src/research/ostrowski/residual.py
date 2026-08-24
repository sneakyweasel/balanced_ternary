"""Unread-tail residual and the order-(m) carry transition.

Analog of Baranwal thesis (2.1)–(2.3). State ``s = (s_1, …, s_m)`` at
remaining length ``i`` means

    E_i = sum_{j < i} w_j q_j = sum_{k=1}^m s_k q_{i-m+k},

with ``w_j = z_j - (x_j + y_j)``. Substituting the place-value
recurrence and reading ``w_{i-1}`` gives a deterministic next state.
Acceptance at ``i = 0`` is ``s_m = 0``, because ``q_j = 0`` for
``j < 0`` and ``q_0 = 1``.

This module does not invent a new carry: it writes the recurrence
implied by §5.3 and Theorem 2.2.
"""

from __future__ import annotations

from typing import Sequence

from research.ostrowski.system import OstrowskiSystem

CarryState = tuple[int, ...]


def zero_state(order: int) -> CarryState:
    return (0,) * order


def is_accepting(state: CarryState) -> bool:
    return state[-1] == 0


def residual_integer(system: OstrowskiSystem, state: CarryState, i: int) -> int:
    """Integer value of ``E_i(s) = sum_k s_k q_{i-m+k}``."""
    m = system.order
    if len(state) != m:
        raise ValueError(f"state length {len(state)} != order {m}")
    return sum(state[k] * system.place_value(i - m + 1 + k) for k in range(m))


def next_state(
    system: OstrowskiSystem,
    state: CarryState,
    w: int,
    i: int,
) -> CarryState:
    """Transition on difference digit ``w = w_{i-1}`` using ``d_{*,i}``.

    Derived from ``E_{i-1} = E_i - w q_{i-1}`` and
    ``q_i = sum_k d_{k,i} q_{i-k}``:

        t_1 = s_m d_{m,i}
        t_j = s_{j-1} + s_m d_{m-j+1,i}    (2 ≤ j ≤ m-1)
        t_m = s_{m-1} + s_m d_{1,i} - w
    """
    m = system.order
    if len(state) != m:
        raise ValueError(f"state length {len(state)} != order {m}")
    if i < 1:
        raise ValueError("remaining length i must be >= 1")
    s = state
    t = [0] * m
    t[0] = s[m - 1] * system.d(m, i)
    for j in range(2, m):
        t[j - 1] = s[j - 2] + s[m - 1] * system.d(m - j + 1, i)
    prev = s[m - 2] if m >= 2 else 0
    t[m - 1] = prev + s[m - 1] * system.d(1, i) - w
    return tuple(t)


def order2_transition(r: int, s: int, w: int, d_i: int) -> tuple[int, int]:
    """Closed form of Theorem 2.2: ``δ((r,s), r + s d_i - t) = (s, t)``."""
    t = r + s * d_i - w
    return (s, t)


def run_msd(
    system: OstrowskiSystem,
    diffs: Sequence[int],
    start: CarryState | None = None,
) -> CarryState:
    """Read ``diffs`` MSD-first: ``diffs[0] = w_{n-1}``, ``diffs[-1] = w_0``."""
    n = len(diffs)
    state = zero_state(system.order) if start is None else start
    for step, w in enumerate(diffs):
        i = n - step
        state = next_state(system, state, w, i)
    return state


def accepts_msd(system: OstrowskiSystem, diffs: Sequence[int]) -> bool:
    return is_accepting(run_msd(system, diffs))


def accepts_msd_boxed(
    system: OstrowskiSystem,
    diffs: Sequence[int],
    tm_bound: int,
) -> bool:
    """MSD run that rejects if any last coordinate leaves ``[-tm_bound, tm_bound]``."""
    n = len(diffs)
    state = zero_state(system.order)
    for step, w in enumerate(diffs):
        i = n - step
        state = next_state(system, state, w, i)
        if abs(state[-1]) > tm_bound:
            return False
    return is_accepting(state)


def difference_word(
    x: Sequence[int],
    y: Sequence[int],
    z: Sequence[int],
) -> tuple[int, ...]:
    """``w_i = z_i - (x_i + y_i)``, LSD-first words of equal length."""
    if not (len(x) == len(y) == len(z)):
        raise ValueError("x, y, z must have the same length")
    return tuple(zi - (xi + yi) for xi, yi, zi in zip(x, y, z))


def lsd_to_msd(word: Sequence[int]) -> tuple[int, ...]:
    return tuple(reversed(word))
