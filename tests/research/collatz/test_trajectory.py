"""Tests for accelerated trajectories and stopping times."""

from __future__ import annotations

import pytest

from research.collatz.core import collatz_step
from research.collatz.trajectory import (
    collatz_stopping_time,
    collatz_total_stopping_time,
    collatz_trajectory,
)


def test_trajectory_of_one():
    traj = collatz_trajectory(1, 10)
    assert traj.values == (1,)
    assert traj.steps == ()
    assert traj.reached_one
    assert not traj.truncated
    assert collatz_stopping_time(1, 10) == 0
    assert collatz_total_stopping_time(1, 10) == 0


def test_trajectory_five_reaches_one():
    traj = collatz_trajectory(5, 10)
    assert traj.values[0] == 5
    assert traj.values[-1] == 1
    assert traj.reached_one
    assert collatz_step(5) == 1
    assert collatz_total_stopping_time(5, 10) == 1


def test_trajectory_matches_iterated_T():
    n = 27
    traj = collatz_trajectory(n, 50)
    current = n
    for step in traj.steps:
        assert step.n == current
        assert collatz_step(current) == step.T_n
        current = step.T_n
    assert traj.values[-1] == current


def test_stopping_time_is_first_decrease():
    n = 7
    k = collatz_stopping_time(n, 50)
    assert k is not None and k >= 1
    traj = collatz_trajectory(n, 50)
    assert traj.values[k] < n
    if k > 1:
        assert all(v >= n for v in traj.values[1:k])


def test_total_stopping_time_counts_steps_to_one():
    for n in range(1, 201, 2):
        total = collatz_total_stopping_time(n, 500)
        assert total is not None
        traj = collatz_trajectory(n, 500)
        assert traj.reached_one
        assert total == len(traj.steps)
        assert traj.values[-1] == 1


def test_truncation():
    traj = collatz_trajectory(27, 2)
    assert traj.truncated
    assert not traj.reached_one
    assert len(traj.steps) == 2
    assert collatz_total_stopping_time(27, 2) is None


def test_max_steps_zero():
    traj = collatz_trajectory(27, 0)
    assert traj.values == (27,)
    assert traj.steps == ()


def test_rejects_bad_bounds():
    with pytest.raises(ValueError):
        collatz_trajectory(3, -1)
    with pytest.raises(ValueError):
        collatz_step(4)
