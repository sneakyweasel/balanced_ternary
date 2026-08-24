"""Inverse of the accelerated Collatz map.

If ``m = T(n)`` then

    n = (2^k m - 1) / 3

for some integer ``k >= 1`` such that the right-hand side is a positive odd
integer. Integrality is

    2^k m ≡ 1  (mod 3).

Since ``2 ≡ -1 (mod 3)``,

    (-1)^k m ≡ 1  (mod 3).

Hence, writing ``m mod 3``:

- ``m ≡ 0 (mod 3)``: no integer ``k`` works.
- ``m ≡ 1 (mod 3)``: ``k`` even.
- ``m ≡ 2 (mod 3)``: ``k`` odd.

**EXACT — HUMAN PROOF:** for every positive odd ``n``, ``T(n) ≢ 0 (mod 3)``, because
``3n+1 ≡ 1 (mod 3)`` and ``2^k`` is invertible modulo 3. Images of ``T``
therefore always have at least one valid exponent parity.

The only positive odd fixed point is ``T(1) = 1``, realised by ``k = 2``.
Inverse trees record that self-map as a cycle and do not recurse on it.
"""

from __future__ import annotations

from dataclasses import dataclass

from bt.representation import encode
from research.collatz.core import collatz_step, require_positive_odd


def predecessor_exponent_parity(m: int) -> str:
    """Required parity of ``k`` for predecessors of ``m``, or ``"none"``."""
    m = require_positive_odd(m, "m")
    r = m % 3
    if r == 0:
        return "none"
    if r == 1:
        return "even"
    return "odd"


def _k_start(m: int) -> int | None:
    parity = predecessor_exponent_parity(m)
    if parity == "none":
        return None
    return 2 if parity == "even" else 1


def collatz_predecessors(m: int, k_max: int) -> list[tuple[int, int]]:
    """Pairs ``(k, n)`` with ``1 <= k <= k_max`` and ``T(n) = m``.

    ``n = (2^k m - 1) / 3`` is formed with exact integer division after the
    divisibility check. Results are sorted by increasing ``k``.
    """
    m = require_positive_odd(m, "m")
    if isinstance(k_max, bool) or not isinstance(k_max, int) or k_max < 1:
        raise ValueError(f"k_max must be an integer >= 1, got {k_max!r}")

    start = _k_start(m)
    if start is None:
        return []

    out: list[tuple[int, int]] = []
    for k in range(start, k_max + 1, 2):
        num = (m << k) - 1
        if num % 3 != 0:
            continue
        n = num // 3
        if n > 0 and n % 2 == 1:
            out.append((k, n))
    return out


@dataclass
class InverseEdge:
    k: int
    child: "InverseNode"


@dataclass
class InverseNode:
    n: int
    balanced_ternary: str
    children: tuple[InverseEdge, ...]
    cycle_ks: tuple[int, ...]
    truncated: bool = False


@dataclass
class InverseTree:
    root: InverseNode
    depth: int
    k_max: int
    node_count: int
    truncated: bool
    max_nodes: int


def build_inverse_tree(
    root: int,
    depth: int,
    k_max: int,
    max_nodes: int = 50_000,
) -> InverseTree:
    """Bounded predecessor tree of the accelerated map.

    ``depth`` is the number of inverse layers below the root. Expansion
    stops at ``max_nodes`` (a computational bound, not a mathematical one).
    The self-map ``1 -> 1`` is recorded in ``cycle_ks`` and is not expanded.
    """
    root = require_positive_odd(root, "root")
    if isinstance(depth, bool) or not isinstance(depth, int) or depth < 0:
        raise ValueError(f"depth must be an integer >= 0, got {depth!r}")
    if isinstance(k_max, bool) or not isinstance(k_max, int) or k_max < 1:
        raise ValueError(f"k_max must be an integer >= 1, got {k_max!r}")
    if isinstance(max_nodes, bool) or not isinstance(max_nodes, int) or max_nodes < 1:
        raise ValueError(f"max_nodes must be an integer >= 1, got {max_nodes!r}")

    counter = {"n": 0, "truncated": False}

    def build(n: int, remaining: int) -> InverseNode:
        if counter["n"] >= max_nodes:
            counter["truncated"] = True
            return InverseNode(
                n=n,
                balanced_ternary=encode(n).word(),
                children=(),
                cycle_ks=(),
                truncated=True,
            )
        counter["n"] += 1
        if remaining <= 0:
            return InverseNode(
                n=n,
                balanced_ternary=encode(n).word(),
                children=(),
                cycle_ks=(),
            )
        edges: list[InverseEdge] = []
        cycles: list[int] = []
        for k, pred in collatz_predecessors(n, k_max):
            if pred == n:
                cycles.append(k)
                continue
            if counter["n"] >= max_nodes:
                counter["truncated"] = True
                break
            edges.append(InverseEdge(k=k, child=build(pred, remaining - 1)))
        return InverseNode(
            n=n,
            balanced_ternary=encode(n).word(),
            children=tuple(edges),
            cycle_ks=tuple(cycles),
            truncated=counter["truncated"],
        )

    node = build(root, depth)
    return InverseTree(
        root=node,
        depth=depth,
        k_max=k_max,
        node_count=counter["n"],
        truncated=counter["truncated"],
        max_nodes=max_nodes,
    )


def format_inverse_tree(tree: InverseTree) -> str:
    lines = [
        f"Inverse accelerated Collatz tree",
        f"root={tree.root.n}  depth={tree.depth}  k_max={tree.k_max}  "
        f"nodes={tree.node_count}  truncated={str(tree.truncated).lower()}",
        "",
    ]

    def walk(node: InverseNode, indent: str) -> None:
        flag = "  [truncated]" if node.truncated else ""
        lines.append(f"{indent}{node.n}  BT={node.balanced_ternary}{flag}")
        extra = indent + "  "
        for k in node.cycle_ks:
            lines.append(f"{extra}[cycle k={k} -> {node.n}]")
        for edge in node.children:
            lines.append(f"{extra}k={edge.k} ->")
            walk(edge.child, extra + "  ")

    walk(tree.root, "")
    lines.append("")
    return "\n".join(lines)
