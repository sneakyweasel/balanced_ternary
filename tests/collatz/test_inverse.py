"""Tests for inverse accelerated Collatz predecessors."""

from __future__ import annotations

import pytest

from collatz.core import collatz_step, collatz_valuation
from collatz.inverse import (
    build_inverse_tree,
    collatz_predecessors,
    predecessor_exponent_parity,
)


def test_exponent_parity_from_mod_three():
    assert predecessor_exponent_parity(1) == "even"  # 1 ≡ 1 (mod 3)
    assert predecessor_exponent_parity(5) == "odd"  # 5 ≡ 2 (mod 3)
    assert predecessor_exponent_parity(7) == "even"  # 7 ≡ 1 (mod 3)
    assert predecessor_exponent_parity(9) == "none"


def test_predecessors_of_one():
    preds = collatz_predecessors(1, 20)
    pairs = dict(preds)
    assert pairs[2] == 1
    assert pairs[4] == 5
    assert pairs[6] == 21
    assert 1 not in pairs
    assert 3 not in pairs
    for k, n in preds:
        assert collatz_step(n) == 1
        assert collatz_valuation(n) == k
        assert k % 2 == 0


def test_predecessors_round_trip_range():
    for m in range(1, 400, 2):
        if m % 3 == 0:
            assert collatz_predecessors(m, 12) == []
            continue
        preds = collatz_predecessors(m, 16)
        assert preds
        parity = predecessor_exponent_parity(m)
        for k, n in preds:
            assert collatz_step(n) == m
            assert collatz_valuation(n) == k
            assert n % 2 == 1
            if parity == "even":
                assert k % 2 == 0
            else:
                assert k % 2 == 1


def test_every_forward_step_is_a_predecessor():
    for n in range(1, 500, 2):
        k = collatz_valuation(n)
        m = collatz_step(n)
        preds = dict(collatz_predecessors(m, max(k, 8)))
        assert preds[k] == n


def test_inverse_tree_bounded():
    tree = build_inverse_tree(1, depth=2, k_max=10, max_nodes=5000)
    assert tree.root.n == 1
    assert 2 in tree.root.cycle_ks
    child_values = {edge.child.n for edge in tree.root.children}
    assert 5 in child_values
    assert 1 not in child_values
    assert tree.node_count >= 1
    assert not tree.truncated


def test_inverse_tree_depth_zero_is_root_only():
    tree = build_inverse_tree(7, depth=0, k_max=8)
    assert tree.root.children == ()
    assert tree.node_count == 1


def test_inverse_rejects_even_root():
    with pytest.raises(ValueError):
        collatz_predecessors(2, 5)
    with pytest.raises(ValueError):
        build_inverse_tree(4, 1, 5)
