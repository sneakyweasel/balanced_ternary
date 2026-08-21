"""Bounded accelerated Collatz trajectories and stopping times.

Stopping-time conventions (accelerated map ``T``):

- **Stopping time** of ``n > 1``: smallest ``k >= 1`` with ``T^k(n) < n``.
  For ``n = 1`` this is ``0`` by convention (``1`` is the terminal odd
  positive integer of the cycle ``T(1) = 1``).
- **Total stopping time**: smallest ``k >= 0`` with ``T^k(n) = 1``.
  For ``n = 1`` this is ``0``.

If the bound ``max_steps`` is hit before the event, the corresponding
function returns ``None``. That is a computational bound, not a mathematical
claim that the orbit diverges.
"""

from __future__ import annotations

from dataclasses import dataclass

from balanced_ternary.representation import encode
from collatz.core import collatz_step, collatz_valuation, require_positive_odd, three_n_plus_one


@dataclass(frozen=True)
class TrajectoryStep:
    """One accelerated step ``n -> T(n)``."""

    n: int
    balanced_ternary_n: str
    three_n_plus_one: int
    v2_three_n_plus_one: int
    T_n: int
    balanced_ternary_T_n: str


@dataclass(frozen=True)
class Trajectory:
    start: int
    values: tuple[int, ...]
    steps: tuple[TrajectoryStep, ...]
    reached_one: bool
    truncated: bool
    max_steps: int


def _one_step(n: int) -> TrajectoryStep:
    y = three_n_plus_one(n)
    k = collatz_valuation(n)
    t = collatz_step(n)
    return TrajectoryStep(
        n=n,
        balanced_ternary_n=encode(n).word(),
        three_n_plus_one=y,
        v2_three_n_plus_one=k,
        T_n=t,
        balanced_ternary_T_n=encode(t).word(),
    )


def collatz_trajectory(n: int, max_steps: int) -> Trajectory:
    """Orbit of ``T`` including the start value, at most ``max_steps`` maps.

    The sequence of odd integers is ``values``. ``steps[i]`` is the
    transition ``values[i] -> values[i+1]``. Iteration stops when ``1`` is
    reached or ``max_steps`` transitions have been applied.
    """
    n = require_positive_odd(n)
    if isinstance(max_steps, bool) or not isinstance(max_steps, int) or max_steps < 0:
        raise ValueError(f"max_steps must be an integer >= 0, got {max_steps!r}")

    values = [n]
    steps: list[TrajectoryStep] = []
    if n == 1 or max_steps == 0:
        return Trajectory(
            start=n,
            values=tuple(values),
            steps=tuple(steps),
            reached_one=(n == 1),
            truncated=False,
            max_steps=max_steps,
        )

    current = n
    for _ in range(max_steps):
        rec = _one_step(current)
        steps.append(rec)
        current = rec.T_n
        values.append(current)
        if current == 1:
            return Trajectory(
                start=n,
                values=tuple(values),
                steps=tuple(steps),
                reached_one=True,
                truncated=False,
                max_steps=max_steps,
            )

    return Trajectory(
        start=n,
        values=tuple(values),
        steps=tuple(steps),
        reached_one=False,
        truncated=True,
        max_steps=max_steps,
    )


def collatz_stopping_time(n: int, max_steps: int) -> int | None:
    """Smallest ``k`` with ``T^k(n) < n``, or ``0`` if ``n == 1``.

    Returns ``None`` if no such ``k`` occurs within ``max_steps``.
    """
    n = require_positive_odd(n)
    if n == 1:
        return 0
    traj = collatz_trajectory(n, max_steps)
    for k, value in enumerate(traj.values[1:], start=1):
        if value < n:
            return k
    return None


def collatz_total_stopping_time(n: int, max_steps: int) -> int | None:
    """Smallest ``k`` with ``T^k(n) = 1``, or ``None`` if not reached in bound."""
    n = require_positive_odd(n)
    if n == 1:
        return 0
    traj = collatz_trajectory(n, max_steps)
    if traj.reached_one:
        return len(traj.steps)
    return None
