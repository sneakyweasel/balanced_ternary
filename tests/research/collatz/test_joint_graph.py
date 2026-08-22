"""Tests for the joint digit/valuation graph."""

from __future__ import annotations

from balanced_ternary.representation import encode
from collatz.automata.joint_graph import (
    build_joint_graph,
    collatz_word_step,
    synchronizing_digit_contexts,
)
from collatz.core import collatz_step, collatz_valuation
from collatz.theorems import append_plus
from collatz.transducers.odd_part import odd_part_word


def test_word_step_matches_T():
    for n in range(1, 400, 2):
        w = encode(n).word()
        k, w_prime = collatz_word_step(w)
        assert k == collatz_valuation(n)
        assert w_prime == encode(collatz_step(n)).word()
        assert w_prime == odd_part_word(append_plus(w)).word()


def test_joint_graph_sample():
    graph = build_joint_graph(200)
    assert len(graph.edges) == 100
    assert graph.images_divisible_by_three() == ()
    by_k = graph.out_degree_by_k()
    assert 1 in by_k
    for e in graph.edges:
        assert e.n_prime == collatz_step(e.n)
        assert e.k == collatz_valuation(e.n)


def test_synchronizing_contexts_length_one():
    # A single right digit need not synchronize; just run the search.
    sync = synchronizing_digit_contexts(precision=4, length=1)
    assert isinstance(sync, tuple)
    # Longer strings can collapse; length 3 at K=3 is small enough.
    sync3 = synchronizing_digit_contexts(precision=3, length=2)
    assert isinstance(sync3, tuple)
