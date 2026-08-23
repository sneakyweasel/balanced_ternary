"""CLI for polynomial congruences and 3-adic lifting trees.

The lifting tree, the singular/nonsingular split, and root counting
modulo ``3^k`` are classical. These commands expose the identification of
the tree with the zero-output subtree of the residual machine; they are
not offered as a faster root counter.
"""

from __future__ import annotations

import argparse
import json

from bt.calculus.lifting import (
    brute_force_roots,
    depth_r_shape,
    level_counts,
    level_nodes,
    lift_tree,
    node_at,
    shape_widths,
)
from bt.calculus.poly_congruence import phi_k
from bt.calculus.section import parse_poly

_KIND_MARK = {
    "unique": "unique",
    "splitting": "split",
    "terminal": "dead",
    "singular-persistent": "singular",
}


def add_congruence_subparser(subparsers: argparse._SubParsersAction) -> None:
    p = subparsers.add_parser(
        "congruence",
        help="solutions of f(x) = 0 mod 3^k and their lifting tree",
    )
    c = p.add_subparsers(dest="cong_cmd", required=True)

    p_roots = c.add_parser("roots", help="solutions modulo 3^k, tree against brute force")
    p_roots.add_argument("--poly", required=True)
    p_roots.add_argument("--k", type=int, default=3)

    p_lift = c.add_parser("lift", help="lifts of one residue to the next level")
    p_lift.add_argument("--poly", required=True)
    p_lift.add_argument("--k", type=int, default=2)
    p_lift.add_argument("--residue", type=int, required=True)

    p_tree = c.add_parser("tree", help="print the lifting tree level by level")
    p_tree.add_argument("--poly", required=True)
    p_tree.add_argument("--k", type=int, default=4)
    p_tree.add_argument("--json", action="store_true")

    p_cls = c.add_parser("classify", help="node kinds, states, and depth-r shapes")
    p_cls.add_argument("--poly", required=True)
    p_cls.add_argument("--k", type=int, default=4)
    p_cls.add_argument("--r", type=int, default=2)

    p_tri = c.add_parser("triage", help="Phase 0 hypothesis verdict over the test families")
    p_tri.add_argument("--k", type=int, default=5)
    p_tri.add_argument("--r", type=int, default=2)
    p_tri.add_argument("--json", action="store_true")


def run_congruence(args: argparse.Namespace) -> int:
    cmd = args.cong_cmd
    if cmd == "roots":
        return _run_roots(args)
    if cmd == "lift":
        return _run_lift(args)
    if cmd == "tree":
        return _run_tree(args)
    if cmd == "classify":
        return _run_classify(args)
    if cmd == "triage":
        return _run_triage(args)
    raise ValueError(f"unknown congruence command {cmd!r}")


def _run_roots(args: argparse.Namespace) -> int:
    f = parse_poly(args.poly)
    k = args.k
    nodes = lift_tree(f, k)
    tree = tuple(sorted(node.residue for node in level_nodes(nodes, k)))
    brute = brute_force_roots(f, k)
    print(f"f = {f.render()}")
    print(f"modulus = 3^{k} = {3 ** k}")
    print(f"roots (balanced residues) = {list(tree)}")
    print(f"count = {len(tree)}")
    print(f"level counts N_0..N_{k} = {list(level_counts(f, k))}")
    print(f"brute force agrees = {str(tree == brute).lower()}")
    return 0


def _run_lift(args: argparse.Namespace) -> int:
    f = parse_poly(args.poly)
    k = args.k
    residue = args.residue
    modulus = 3**k
    half = (modulus - 1) // 2
    if not -half <= residue <= half:
        print(f"residue must be a balanced residue in [{-half}, {half}] for k = {k}")
        return 2
    word = _word_of(residue, k)
    node = node_at(f, word)
    print(f"f = {f.render()}")
    print(f"node: level {k}, residue {residue}, digits {node.digits or 'e'}")
    print(f"f(n) = {node.f_value}, v3 = {_v(node.v3_f)}")
    print(f"f'(n) = {node.f_prime}, v3 = {_v(node.v3_f_prime)}")
    print(f"residual = {node.residual.render()}")
    if node.f_value % modulus:
        print("this residue is not a solution modulo 3^k, so it has no lifts")
        return 0
    print(f"scaled value f(n)/3^k = {node.scaled_value}")
    print(f"kind = {node.kind}")
    print(f"lifting trits = {list(node.children)}")
    for a in node.children:
        child = residue + a * modulus
        print(f"  t = {a:+d}: x = {child}, f(x) = {f.eval(child)}")
    if not node.children:
        print("  none")
    return 0


def _run_tree(args: argparse.Namespace) -> int:
    f = parse_poly(args.poly)
    nodes = lift_tree(f, args.k)
    if args.json:
        payload = {
            "poly": f.render(),
            "k": args.k,
            "level_counts": list(level_counts(f, args.k)),
            "nodes": [node.as_dict() for node in nodes],
        }
        print(json.dumps(payload, indent=2))
        return 0
    print(f"f = {f.render()}")
    for level in range(args.k + 1):
        layer = level_nodes(nodes, level)
        print(f"level {level} (mod 3^{level} = {3 ** level}): {len(layer)} node(s)")
        for node in layer:
            digits = node.digits or "e"
            kids = "".join(f"{a:+d}" for a in node.children) or "-"
            print(
                f"  {digits:>{max(args.k, 1)}}  x={node.residue:<6d} "
                f"v3(f)={_v(node.v3_f):<4} v3(f')={_v(node.v3_f_prime):<4} "
                f"{_KIND_MARK[node.kind]:<9} lifts={kids}"
            )
    return 0


def _run_classify(args: argparse.Namespace) -> int:
    f = parse_poly(args.poly)
    r = args.r
    nodes = lift_tree(f, args.k)
    print(f"f = {f.render()}")
    print(f"depth r = {r}")
    census: dict[str, int] = {}
    for node in nodes:
        census[node.kind] = census.get(node.kind, 0) + 1
    print(f"kind census = {dict(sorted(census.items()))}")
    for level in range(args.k + 1):
        layer = level_nodes(nodes, level)
        if not layer:
            continue
        phis = {phi_k(node.residual, r) for node in layer}
        shapes = {depth_r_shape(node.residual, r) for node in layer}
        print(
            f"level {level}: {len(layer)} node(s), "
            f"{len(phis)} Phi_{r} class(es), {len(shapes)} distinct depth-{r} subtree(s)"
        )
        for node in layer:
            print(
                f"  {node.digits or 'e'}: newton={list(node.newton)} "
                f"phi_{r}={list(phi_k(node.residual, r))} "
                f"widths={list(shape_widths(node.residual, r))}"
            )
    print("Phi_r determines the depth-r subtree; the two valuations do not.")
    return 0


def _run_triage(args: argparse.Namespace) -> int:
    from research.lifting.triage import triage_report

    report = triage_report(k_max=args.k, r_max=args.r)
    if args.json:
        print(json.dumps(report, indent=2))
        return 0
    print(f"polynomials: {report['polynomials']}")
    for key in ("h1", "h2", "h3"):
        rec = report[key]
        print(f"{rec['hypothesis']}: ok={str(rec['ok']).lower()} ({rec['claim']})")
    for row in report["determinacy"]:
        print(f"r = {row['r']}")
        print(f"  Phi_r determines subtree: {str(row['phi']['ok']).lower()}")
        print(f"  Phi_(r-1) insufficient:   {str(row['sharpness']['ok']).lower()}")
        print(f"  deep linearization:       {str(row['linearization']['ok']).lower()}")
        print(f"  valuations, deep k>=r:    {str(row['valuation_deep']['determined']).lower()}")
        print(f"  valuations, shallow k<r:  {str(row['valuation_shallow']['determined']).lower()}")
    print(f"verdict: {'proceed' if report['proceed'] else 'stop'}")
    print("No complexity claim: deterministic poly(deg f, k log 3) counting is known.")
    return 0


def _word_of(residue: int, k: int) -> tuple[int, ...]:
    from bt.calculus.section import rho_int

    out: list[int] = []
    n = residue
    for _ in range(k):
        a = rho_int(n)
        out.append(a)
        n = (n - a) // 3
    return tuple(out)


def _v(val: int | None) -> str:
    return "inf" if val is None else str(val)
