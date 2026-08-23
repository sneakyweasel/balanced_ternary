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

    p_state = c.add_parser(
        "state",
        help="valuation, Phi_r, and minimal behaviour classes of a lifting tree",
    )
    p_state.add_argument("--poly", required=True)
    p_state.add_argument("--k", type=int, default=4)
    p_state.add_argument("--r", type=int, default=3)
    p_state.add_argument(
        "--allow-expensive",
        action="store_true",
        help="permit r >= 6, which enumerates 3^(2r) linear states",
    )
    p_state.add_argument("--json", action="store_true")

    p_dist = c.add_parser(
        "distinguish",
        help="compare two residual states: valuations, Phi_(r-1), Phi_r, behaviour",
        epilog=(
            "A polynomial starting with a minus sign looks like an option, so put "
            "it after a bare --, as in: distinguish --r 4 -- x -x"
        ),
    )
    p_dist.add_argument("left")
    p_dist.add_argument("right")
    p_dist.add_argument("--r", type=int, default=3)


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
    if cmd == "state":
        return _run_state(args)
    if cmd == "distinguish":
        return _run_distinguish(args)
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


def _run_state(args: argparse.Namespace) -> int:
    from bt.calculus.lifting_state import (
        behaviour_class,
        behaviour_count_formula,
        dominated_count,
        is_dead,
        is_dominated,
        minimal_state_key,
        undominated_count,
    )
    from research.lifting.state_complexity import quotient_chain

    f = parse_poly(args.poly)
    r = max(int(args.r), 1)
    nodes = lift_tree(f, args.k)
    rows = []
    for level in range(args.k + 1):
        layer = level_nodes(nodes, level)
        if not layer:
            continue
        row = {
            "level": level,
            "nodes": len(layer),
            "valuation_classes": len(
                {(_cap(n.v3_f, r), _cap(n.v3_f_prime, r)) for n in layer}
            ),
            "phi_classes": len({phi_k(n.residual, r) for n in layer}),
            "behaviours": len({behaviour_class(n.residual, r) for n in layer}),
            "deep": level >= r,
        }
        if level >= r:
            # In the deep regime the node is its linear surrogate modulo 3^r,
            # so the normal form applies verbatim.
            pairs = [(n.scaled_value, n.f_prime) for n in layer]
            row["dominated_nodes"] = sum(1 for c, b in pairs if is_dominated(c, b, r))
            row["normal_forms"] = len({minimal_state_key(c, b, r) for c, b in pairs})
        rows.append(row)
    try:
        chain = quotient_chain(r, allow_expensive=args.allow_expensive)
    except ValueError as exc:
        chain = {"error": str(exc)}
    payload = {
        "poly": f.render(),
        "k": args.k,
        "r": r,
        "levels": rows,
        "deep_regime": chain,
        "deep_bound": behaviour_count_formula(r),
        "strata": {
            "dominated": dominated_count(r),
            "undominated": undominated_count(r),
        },
        "dead_nodes": sum(1 for n in nodes if is_dead(n.residual)),
    }
    if args.json:
        print(json.dumps(payload, indent=2))
        return 0
    print(f"f = {f.render()}")
    print(f"horizon r = {r}, levels k = 0..{args.k}")
    print("level  nodes  valuation  Phi_r  behaviour  dominated  regime")
    for row in rows:
        dominated = row.get("dominated_nodes")
        print(
            f"{row['level']:>5}  {row['nodes']:>5}  {row['valuation_classes']:>9}  "
            f"{row['phi_classes']:>5}  {row['behaviours']:>9}  "
            f"{'-' if dominated is None else dominated:>9}  "
            f"{'deep' if row['deep'] else 'shallow'}"
        )
    print(f"dead nodes (no surviving branch) = {payload['dead_nodes']}")
    if "error" in chain:
        print(f"deep regime: {chain['error']}")
    else:
        print(
            f"deep regime at r = {r}: Phi_r has {chain['phi_states']} states, "
            f"unit orbits {chain['unit_orbits']}, minimal L_r = {chain['behaviours']}"
        )
        print(f"closed form (3^(r+1)-1)/2 + r holds = {str(chain['formula_holds']).lower()}")
    print(
        f"L_r splits as {dominated_count(r)} dominated (v3(c) < v3(b), behaviour is the "
        f"truncated tree of depth v3(c)) + {undominated_count(r)} undominated "
        "(behaviour is exactly the unit-scaling orbit)."
    )
    print("Phi_r is sufficient but not minimal: unit scaling moves it and not the subtree.")
    return 0


def _run_distinguish(args: argparse.Namespace) -> int:
    from bt.calculus.lifting_state import (
        behaviour_class,
        behaviour_depth,
        is_dead,
        unit_scale,
    )
    from bt.calculus.poly_congruence import phi_equal

    left, right = parse_poly(args.left), parse_poly(args.right)
    r = max(int(args.r), 1)
    print(f"left  = {left.render()}")
    print(f"right = {right.render()}")
    for name, g in (("left", left), ("right", right)):
        print(
            f"{name}: dead={str(is_dead(g)).lower()} "
            f"depth={behaviour_depth(g, r)} "
            f"phi_{r}={list(phi_k(g, r))}"
        )
    for horizon in range(1, r + 1):
        print(
            f"r = {horizon}: phi equal = {str(phi_equal(left, right, horizon)).lower()}, "
            f"behaviour equal = "
            f"{str(behaviour_class(left, horizon) == behaviour_class(right, horizon)).lower()}"
        )
    first = next(
        (
            d
            for d in range(1, r + 1)
            if behaviour_class(left, d) != behaviour_class(right, d)
        ),
        None,
    )
    print(f"first distinguishing depth = {'none' if first is None else first}")
    scalar = next(
        (
            lam
            for lam in (-1, 2, -2, 4, -4, 5, -5, 7, -7, 8, -8)
            if unit_scale(left, lam).coeffs == right.coeffs
        ),
        None,
    )
    if scalar is not None:
        print(f"right = {scalar} * left, a unit multiple, so the behaviours must agree")
    if is_dead(left) and is_dead(right):
        print("both states are dead, so agreement is vacuous and proves nothing")
    return 0


def _cap(val: int | None, r: int) -> int:
    return r if val is None else min(val, r)


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
