"""Symbolic joint graph of valuation prefixes."""

from __future__ import annotations

from research.collatz.automata.symbolic_graph import (
    build_symbolic_graph,
    edge_agrees_with_follow_path,
)
from research.collatz.automata.valuation_shift import PrecisionState, follow_path
from research.collatz.cylinders import valuation_cylinder


def test_symbolic_graph_empty_start():
    g = build_symbolic_graph(max_length=0, k_max=3)
    assert len(g.nodes) == 1
    assert g.nodes[0].ks == ()
    assert g.nodes[0].residue == 1
    assert g.nodes[0].precision == 1
    assert not g.edges


def test_first_layer_matches_cylinders():
    g = build_symbolic_graph(max_length=1, k_max=4)
    by_ks = {n.ks: n for n in g.nodes if n.ks}
    for k in range(1, 5):
        cyl = valuation_cylinder((k,))
        node = by_ks[(k,)]
        assert node.residue == cyl.residues[0]
        assert node.precision == cyl.precision


def test_edges_agree_with_follow_path():
    g = build_symbolic_graph(max_length=3, k_max=4, leftover_q=1)
    assert g.edges
    for edge in g.edges:
        assert edge_agrees_with_follow_path(edge, leftover_q=1)
        _, status = follow_path(
            PrecisionState(edge.target.residue, edge.target.precision),
            edge.target.ks,
        )
        assert status == "ok"
        assert edge.target.residue % (1 << edge.source.precision) == edge.source.residue


def test_budget_split_recorded():
    g = build_symbolic_graph(max_length=3, k_max=4)
    assert g.expanding_nodes()
    assert g.contracting_nodes()
    text = g.format()
    assert "Symbolic Collatz futures" in text
    assert "not a Lyapunov" in text
