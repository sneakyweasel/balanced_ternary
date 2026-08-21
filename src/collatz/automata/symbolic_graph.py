"""Symbolic Collatz futures: nodes ``(valuation prefix, r mod 2^P, P)``.

This is not the sampled integer graph in ``joint_graph``. Each admissible
prefix at leftover precision ``Q`` is a residue class modulo ``2^{Q+K}``.
Edges append one valuation symbol by recomputing the longer cylinder
(never dividing modulo ``2^P``).

Nodes are classified by the homogeneous budget ``2^K`` vs ``3^m``.
That comparison is **not** a Lyapunov function.
"""

from __future__ import annotations

from dataclasses import dataclass

from collatz.automata.valuation_shift import GrowthBudget, follow_path, growth_budget
from collatz.cylinders import precision_cost, valuation_cylinder


@dataclass(frozen=True)
class SymbolicNode:
    ks: tuple[int, ...]
    residue: int
    precision: int

    def budget(self) -> GrowthBudget:
        return growth_budget(self.ks)


@dataclass(frozen=True)
class SymbolicEdge:
    source: SymbolicNode
    k: int
    target: SymbolicNode


@dataclass
class SymbolicJointGraph:
    leftover_q: int
    max_length: int
    k_max: int
    nodes: tuple[SymbolicNode, ...]
    edges: tuple[SymbolicEdge, ...]

    def contracting_nodes(self) -> tuple[SymbolicNode, ...]:
        return tuple(n for n in self.nodes if n.ks and n.budget().kind == "contracting")

    def expanding_nodes(self) -> tuple[SymbolicNode, ...]:
        return tuple(n for n in self.nodes if n.ks and n.budget().kind == "expanding")

    def as_dict(self) -> dict[str, object]:
        return {
            "leftover_q": self.leftover_q,
            "max_length": self.max_length,
            "k_max": self.k_max,
            "node_count": len(self.nodes),
            "edge_count": len(self.edges),
            "contracting": len(self.contracting_nodes()),
            "expanding": len(self.expanding_nodes()),
            "nodes": [
                {
                    "ks": list(n.ks),
                    "residue": n.residue,
                    "precision": n.precision,
                    "budget": n.budget().kind if n.ks else "empty",
                }
                for n in self.nodes
            ],
            "edges": [
                {
                    "source": list(e.source.ks),
                    "k": e.k,
                    "target": list(e.target.ks),
                }
                for e in self.edges
            ],
        }

    def format(self) -> str:
        lines = [
            "Symbolic Collatz futures  "
            f"leftover_Q={self.leftover_q}  max_length={self.max_length}  "
            f"k_max={self.k_max}",
            f"nodes={len(self.nodes)}  edges={len(self.edges)}  "
            f"contracting={len(self.contracting_nodes())}  "
            f"expanding={len(self.expanding_nodes())}",
            "",
            "This is a graph of valuation prefixes, not of sampled integers.",
            "Budget 2^K vs 3^m is the homogeneous estimate, not a Lyapunov function.",
            "",
        ]
        shown = 0
        for node in self.nodes:
            if shown >= 24:
                lines.append(f"... ({len(self.nodes) - shown} more nodes)")
                break
            kind = node.budget().kind if node.ks else "empty"
            lines.append(
                f"  {node.ks}  r={node.residue}  P={node.precision}  {kind}"
            )
            shown += 1
        lines.append("")
        return "\n".join(lines)


def _nodes_for_prefix(ks: tuple[int, ...], leftover_q: int) -> tuple[SymbolicNode, ...]:
    cyl = valuation_cylinder(ks, leftover_q=leftover_q)
    return tuple(
        SymbolicNode(ks=ks, residue=r, precision=cyl.precision)
        for r in cyl.residues
    )


def build_symbolic_graph(
    max_length: int,
    k_max: int,
    leftover_q: int = 1,
) -> SymbolicJointGraph:
    if isinstance(max_length, bool) or not isinstance(max_length, int) or max_length < 0:
        raise ValueError(f"max_length must be an integer >= 0, got {max_length!r}")
    if isinstance(k_max, bool) or not isinstance(k_max, int) or k_max < 1:
        raise ValueError(f"k_max must be an integer >= 1, got {k_max!r}")
    if isinstance(leftover_q, bool) or not isinstance(leftover_q, int) or leftover_q < 1:
        raise ValueError(f"leftover_q must be an integer >= 1, got {leftover_q!r}")

    nodes: list[SymbolicNode] = []
    edges: list[SymbolicEdge] = []
    level = list(_nodes_for_prefix((), leftover_q))
    nodes.extend(level)
    for _ in range(max_length):
        nxt_level: list[SymbolicNode] = []
        seen: set[SymbolicNode] = set()
        for src in level:
            for k in range(1, k_max + 1):
                new_ks = src.ks + (k,)
                for tgt in _nodes_for_prefix(new_ks, leftover_q):
                    if tgt.residue % (1 << src.precision) != src.residue:
                        continue
                    edges.append(SymbolicEdge(source=src, k=k, target=tgt))
                    if tgt not in seen:
                        seen.add(tgt)
                        nxt_level.append(tgt)
        nodes.extend(nxt_level)
        level = nxt_level
    return SymbolicJointGraph(
        leftover_q=leftover_q,
        max_length=max_length,
        k_max=k_max,
        nodes=tuple(nodes),
        edges=tuple(edges),
    )


def edge_agrees_with_follow_path(edge: SymbolicEdge, leftover_q: int) -> bool:
    """The target residue realises the longer prefix at its own precision."""
    from collatz.automata.valuation_shift import PrecisionState

    _, status = follow_path(
        PrecisionState(edge.target.residue, edge.target.precision),
        edge.target.ks,
    )
    if status != "ok":
        return False
    p_src = precision_cost(edge.source.ks, leftover_q=leftover_q)
    return edge.source.precision == p_src
