"""Lift tree and bounded precision dual model."""

from __future__ import annotations

from itertools import product

from research.collatz.dual_code import CollatzDualCode
from research.collatz.lift_tree import (
    DualPrecisionState,
    LiftEdgeClass,
    build_lift_tree,
    follow_dual_precision,
    precision_agrees_with_exact,
    precision_transition,
)


def test_lift_tree_shape_and_edge_classification():
    tree = build_lift_tree(max_depth=3, k_max=3)
    assert not tree.truncated
    assert len(tree.nodes) == 1 + 3 + 9 + 27
    assert len(tree.edges) == len(tree.nodes) - 1
    by_parent: dict[tuple[int, ...], list] = {}
    for edge in tree.edges:
        by_parent.setdefault(edge.parent, []).append(edge)
        assert edge.edge_class in {
            LiftEdgeClass.ZERO_LIFT,
            LiftEdgeClass.POSITIVE_LIFT,
        }
        assert edge.child_R >= next(
            node.R for node in tree.nodes if node.itinerary == edge.parent
        )
    # Exactly one zero-lift child exists mathematically; within a bounded
    # alphabet it appears iff its valuation is <= k_max.
    for parent, edges in by_parent.items():
        zeros = [edge for edge in edges if edge.edge_class is LiftEdgeClass.ZERO_LIFT]
        assert len(zeros) <= 1
        if CollatzDualCode.from_valuations(parent).steps:
            assert all(edge.edge_class.value != "FORBIDDEN" for edge in edges)


def test_root_zero_lift_and_positive_edges():
    tree = build_lift_tree(max_depth=1, k_max=4)
    edges = {edge.next_k: edge for edge in tree.edges}
    assert edges[2].edge_class is LiftEdgeClass.ZERO_LIFT
    assert edges[2].lift_digit == 0
    assert all(
        edges[k].edge_class is LiftEdgeClass.POSITIVE_LIFT for k in (1, 3, 4)
    )


def test_tree_truncation_is_explicit():
    tree = build_lift_tree(max_depth=5, k_max=5, max_nodes=12)
    assert tree.truncated
    assert len(tree.nodes) == 12


def test_precision_transition_root():
    state = DualPrecisionState.initial(8)
    transition = precision_transition(state, 2)
    assert transition.lift_digit == 0
    assert transition.target.endpoint_residue == 1
    assert transition.target.precision == 6


def test_precision_model_exhaustive_when_enough_bits_remain():
    for m in range(1, 6):
        for ks in product(range(1, 4), repeat=m):
            precision = sum(ks) + 2
            assert precision_agrees_with_exact(ks, precision)
            digits, state = follow_dual_precision(ks, precision)
            exact = CollatzDualCode.from_valuations(ks)
            assert digits == exact.lift_digits
            assert state.precision == 2
