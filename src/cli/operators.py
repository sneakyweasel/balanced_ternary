"""CLI for the balanced-ternary operator branch."""

from __future__ import annotations

import argparse
import json

from balanced_ternary.additive_sets import (
    smallest_r_covering_nonneg_interval,
    sparse_cubes,
    sparse_primes,
    sparse_squares,
    sumset_A_minus_A,
    sumset_A_plus_A,
    sumset_A_plus_B,
    sumset_B_plus_B,
    weight_one_squares,
)
from balanced_ternary.metrics import carry_defect, carry_defect_scan, d_bt, metric_properties
from balanced_ternary.operator_algebra import (
    census_compositions,
    classify_pair,
    parse_composition,
)
from balanced_ternary.operators import (
    OPERATORS,
    d_orbit,
    d_steps_to_zero,
    digit_derivative,
    get_operator,
    lsd_digit,
    recovered_digits,
    shift_feature_effects,
)
from balanced_ternary.polynomials import evaluation_identities, factor_small, mahler_measure, polynomial
from balanced_ternary.representation import encode
from balanced_ternary.sequences import all_dossiers
from balanced_ternary.transducer_zoo import h2_state_counts, m2_state_counts, zoo


def add_operators_subparser(subparsers: argparse._SubParsersAction) -> None:
    p = subparsers.add_parser(
        "operators",
        help="balanced-ternary operator algebra (not a Collatz search)",
    )
    c = p.add_subparsers(dest="op_cmd", required=True)

    p_ap = c.add_parser("apply", help="apply a named operator to an integer")
    p_ap.add_argument("symbol")
    p_ap.add_argument("n", type=int)

    p_der = c.add_parser("derivative", help="D-orbit and reconstruction")
    p_der.add_argument("n", type=int)

    p_shift = c.add_parser("shift", help="S(n)=3n and feature effects")
    p_shift.add_argument("n", type=int)

    p_comm = c.add_parser("commutator", help="classify A∘B vs B∘A")
    p_comm.add_argument("left")
    p_comm.add_argument("right")
    p_comm.add_argument("--limit", type=int, default=200)

    p_alg = c.add_parser("algebra", help="composition census (depth <= 3)")
    p_alg.add_argument("--depth", type=int, default=3)
    p_alg.add_argument("--sample-limit", type=int, default=20)

    p_poly = c.add_parser("poly", help="P_n(x) evaluations and small factors")
    p_poly.add_argument("n", type=int)

    p_add = c.add_parser("additive", help="digit-restricted sumsets")
    p_add.add_argument("--k", type=int, default=4)

    p_sp = c.add_parser("sparse", help="bounded-weight squares/cubes/primes")
    p_sp.add_argument("--k", type=int, default=2)
    p_sp.add_argument("--bound", type=int, default=10_000)

    p_met = c.add_parser("metrics", help="d_BT and carry_defect scan")
    p_met.add_argument("--limit", type=int, default=30)
    p_met.add_argument("a", nargs="?", type=int)
    p_met.add_argument("b", nargs="?", type=int)

    c.add_parser("zoo", help="finite-state classification table")
    p_st = c.add_parser("states", help="M2^k / H2^k reachable-state counts")
    p_st.add_argument("--max-k", type=int, default=6)

    c.add_parser("sequences", help="OEIS-style dossiers")

    p_id = c.add_parser("id", help="list built-in operators")
    p_id.add_argument("--json", action="store_true")


def run_operators(args: argparse.Namespace) -> int:
    cmd = args.op_cmd
    if cmd == "apply":
        op = get_operator(args.symbol)
        n = args.n
        word_in = encode(n).word()
        y = op.apply(n)
        word_out = op.apply_word(encode(n)).word()
        print(f"{op.symbol}({n}) = {y}")
        print(f"BT({n}) = {word_in}")
        print(f"apply_word = {word_out}")
        print(f"consistent = {str(op.consistent_on(n)).lower()}")
        return 0
    if cmd == "derivative":
        n = args.n
        print(f"n = {n}")
        print(f"BT(n) = {encode(n).word()}")
        print(f"a0 = {lsd_digit(n)}")
        print(f"D(n) = {digit_derivative(n)}")
        print(f"n = a0 + 3 D(n): {n == lsd_digit(n) + 3 * digit_derivative(n)}")
        print(f"steps_to_0 = {d_steps_to_zero(n)}")
        print(f"recovered_digits = {recovered_digits(n)}")
        print(f"orbit = {d_orbit(n)}")
        return 0
    if cmd == "shift":
        n = args.n
        print(f"S({n}) = {3 * n}")
        print(f"BT({n}) = {encode(n).word()}")
        print(f"BT(3n) = {encode(3 * n).word()}")
        fx = shift_feature_effects(n)
        for key, val in fx.items():
            print(f"  {key}: {val}")
        return 0
    if cmd == "commutator":
        rec = classify_pair(args.left, args.right, limit=args.limit)
        print(f"{rec.left} vs {rec.right}")
        print(f"class: {rec.classification}")
        print(f"identity: {rec.identity}")
        print(f"status: {rec.proof_status}")
        if rec.defect_formula:
            print(f"defect: {rec.defect_formula}")
        if rec.sample_defect is not None:
            print(f"sample_abs_defect: {rec.sample_defect}")
        print(rec.notes)
        return 0
    if cmd == "algebra":
        cen = census_compositions(max_depth=args.depth, sample_limit=args.sample_limit)
        print(f"depth: {cen.depth}")
        print(f"enumerated: {cen.enumerated}")
        print(f"simplified_classes: {cen.simplified_classes}")
        print(f"identities: {len(cen.identities)}")
        for a, b in cen.identities[:20]:
            print(f"  {a} ~ {b}")
        print(f"involutions (scan): {cen.involutions[:12]}")
        print(f"projections (scan): {cen.projections[:12]}")
        print(cen.notes)
        return 0
    if cmd == "poly":
        n = args.n
        ids = evaluation_identities(n)
        p = polynomial(n)
        print(f"n = {n}")
        print(f"BT = {encode(n).word()}")
        print(f"coeffs_lsd = {p.coeffs}")
        for key, val in ids.items():
            print(f"  {key}: {val}")
        print(f"factors: {factor_small(p)}")
        print(f"Mahler (numeric): {mahler_measure(p):.6f}")
        return 0
    if cmd == "additive":
        k = args.k
        for rep in (
            sumset_A_plus_A(k),
            sumset_A_minus_A(k),
            sumset_B_plus_B(k),
        ):
            print(
                f"{rep.name} k={k}: |set|={rep.cardinality} "
                f"[{rep.covered_min},{rep.covered_max}] interval={rep.interval} "
                f"E={rep.energy} status={rep.proof_status}"
            )
            print(f"  {rep.formula}")
        if k <= 8:
            ab = sumset_A_plus_B(k)
            print(
                f"{ab.name} k={k}: |set|={ab.cardinality} "
                f"[{ab.covered_min},{ab.covered_max}] interval={ab.interval}"
            )
        print(f"smallest r with r A_k covering [0,3^k-1]: {smallest_r_covering_nonneg_interval(k)}")
        return 0
    if cmd == "sparse":
        print(weight_one_squares())
        print(f"squares w<=k={args.k}, m<=sqrt({args.bound}): {sparse_squares(args.k, int(args.bound**0.5))}")
        print(f"cubes w<=k={args.k}, m<=cbrt({args.bound}): {sparse_cubes(args.k, int(args.bound ** (1 / 3)))}")
        print(f"primes w<=k={args.k}, n<={args.bound}: {sparse_primes(args.k, args.bound)}")
        return 0
    if cmd == "metrics":
        if args.a is not None and args.b is not None:
            print(f"d_BT({args.a},{args.b}) = {d_bt(args.a, args.b)}")
            print(f"carry_defect({args.a},{args.b}) = {carry_defect(args.a, args.b)}")
        scan = carry_defect_scan(args.limit)
        props = metric_properties(min(args.limit, 10))
        print(json.dumps({"scan": scan, "metric": props}, indent=2))
        return 0
    if cmd == "zoo":
        for e in zoo():
            fs = {True: "yes", False: "no", None: "?"}[e.finite_state]
            print(f"{e.function}: FST={fs} states={e.state_count} [{e.proof_status}]")
            print(f"  {e.notes}")
        return 0
    if cmd == "states":
        print("H2^k:", h2_state_counts(args.max_k))
        print("M2^k:", m2_state_counts(args.max_k))
        return 0
    if cmd == "sequences":
        for d in all_dossiers():
            print(f"{d.name} [{d.claim_status}] ~ {d.closest_oeis}")
            print(f"  {d.definition}")
            print(f"  terms: {d.terms[:16]}")
            print(f"  {d.notes}")
        return 0
    if cmd == "id":
        if args.json:
            print(json.dumps({k: v.metadata().as_dict() for k, v in OPERATORS.items()}, indent=2))
        else:
            for sym, op in OPERATORS.items():
                meta = op.metadata()
                print(f"{sym:4} {meta.integer_domain:12} FST={meta.finite_state}  {meta.notes}")
        return 0
    raise ValueError(f"unknown operators command {cmd!r}")
