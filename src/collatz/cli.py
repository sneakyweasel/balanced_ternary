"""CLI subcommands: ``btprime collatz ...``."""

from __future__ import annotations

import argparse
from pathlib import Path

from balanced_ternary.representation import encode
from collatz.automata.joint_graph import layer_d_report
from collatz.automata.symbolic_graph import build_symbolic_graph
from collatz.automata.two_adic import TwoAdicDigitAutomaton
from collatz.automata.valuation_shift import AdmissibleValuationAutomaton
from collatz.cylinders import valuation_cylinder
from collatz.experiments.complexity_spectrum import run_complexity_spectrum
from collatz.languages.cylinder_dfa import entropy_report
from collatz.bt_arithmetic import lsd_add_one_case, multiply_by_three
from collatz.core import require_positive_odd
from collatz.experiments.exhaustive import run_exhaustive_experiment
from collatz.features import extract_features
from collatz.inverse import build_inverse_tree, format_inverse_tree
from collatz.research.invariants import verify_collatz_invariants
from collatz.theorems import append_plus, predicted_features_after_append_plus
from collatz.trajectory import collatz_trajectory
from collatz.transducers.divide_by_two import DivideByTwoTransducer, LeftoverCarryError
from collatz.transducers.divide_by_two_power import DivideByTwoPowerTransducer
from collatz.transducers.odd_part import odd_part_word
from collatz.transitions import NUMERIC_FEATURE_NAMES, feature_transition
from collatz.valuation import v2


def add_collatz_subparser(subparsers: argparse._SubParsersAction) -> None:
    p = subparsers.add_parser(
        "collatz",
        help="Accelerated Collatz research module (balanced ternary / 2-adic)",
    )
    c = p.add_subparsers(dest="collatz_cmd", required=True)

    p_an = c.add_parser("analyze", help="one accelerated step and feature transition")
    p_an.add_argument("n", type=int)

    p_tr = c.add_parser("trajectory", help="bounded accelerated trajectory")
    p_tr.add_argument("n", type=int)
    p_tr.add_argument("--max-steps", type=int, default=100)

    p_inv = c.add_parser("inverse", help="bounded inverse predecessor tree")
    p_inv.add_argument("m", type=int)
    p_inv.add_argument("--depth", type=int, default=5)
    p_inv.add_argument("--k-max", type=int, default=20, dest="k_max")
    p_inv.add_argument("--max-nodes", type=int, default=50_000, dest="max_nodes")

    p_invar = c.add_parser(
        "test-invariants",
        help="verify Milestone 1 identities on odd n in [1, limit]",
    )
    p_invar.add_argument("--limit", type=int, default=100_000)

    p_auto = c.add_parser(
        "automaton",
        help="inspect TwoAdicDigitAutomaton(K)",
    )
    p_auto.add_argument("--precision", type=int, default=8)
    p_auto.add_argument(
        "--word",
        default=None,
        help="optional balanced ternary word to trace (default: encode(27))",
    )

    p_exp = c.add_parser(
        "experiment",
        help="exhaustive feature-transition experiment A (optional write)",
    )
    p_exp.add_argument("--limit", type=int, default=1000)
    p_exp.add_argument(
        "--write",
        action="store_true",
        help="write JSONL/JSON under experiments/collatz/",
    )

    p_th = c.add_parser("theorems", help="Layer A: BT(3n+1) = BT(n)+")
    p_th.add_argument("n", type=int)

    p_op = c.add_parser("odd-part", help="Layer B: x -> x/2^{v2(x)} on a BT word")
    p_op.add_argument("x", type=int)

    p_tu = c.add_parser("transducer", help="verify /2^k transducer vs integer arithmetic")
    p_tu.add_argument("--k", type=int, default=3)
    p_tu.add_argument("--limit", type=int, default=5000)

    p_vs = c.add_parser(
        "valuation-shift",
        help="Layer C: admissible valuation prefixes and growth budget",
    )
    p_vs.add_argument("--precision", type=int, default=12)
    p_vs.add_argument("--k-max", type=int, default=6, dest="k_max")
    p_vs.add_argument("--length", type=int, default=5)

    p_jg = c.add_parser("joint", help="Layer D: truncated w --k--> w' graph")
    p_jg.add_argument("--limit", type=int, default=500)
    p_jg.add_argument("--k-max", type=int, default=8, dest="k_max")
    p_jg.add_argument("--precision", type=int, default=8)
    p_jg.add_argument("--pattern-length", type=int, default=2, dest="pattern_length")
    p_jg.add_argument("--sync-length", type=int, default=2, dest="sync_length")

    p_cyl = c.add_parser(
        "cylinder",
        help="Milestone 3: valuation cylinder residues, density, budget",
    )
    p_cyl.add_argument(
        "--ks",
        required=True,
        help="comma-separated valuation prefix, e.g. 1,2,1",
    )
    p_cyl.add_argument("--leftover", type=int, default=1, dest="leftover")

    p_ent = c.add_parser(
        "entropy",
        help="Milestone 3: padded BT word counts and H_L of a cylinder",
    )
    p_ent.add_argument("--ks", default="", help="valuation prefix (empty = all odds)")
    p_ent.add_argument("--length", type=int, default=6)
    p_ent.add_argument("--leftover", type=int, default=1, dest="leftover")

    p_cx = c.add_parser(
        "complexity",
        help="Milestone 3: /2^k and L_k complexity spectrum",
    )
    p_cx.add_argument("--k-max", type=int, default=6, dest="k_max")
    p_cx.add_argument(
        "--write",
        action="store_true",
        help="write JSON under experiments/collatz/reports/",
    )

    p_sg = c.add_parser(
        "symbolic-graph",
        help="Milestone 3: symbolic futures (prefix, r, P)",
    )
    p_sg.add_argument("--max-length", type=int, default=4, dest="max_length")
    p_sg.add_argument("--k-max", type=int, default=5, dest="k_max")
    p_sg.add_argument("--leftover", type=int, default=1, dest="leftover")

    c.add_parser("ui", help="open the Streamlit research explorer")


def run_collatz(args: argparse.Namespace) -> int:
    cmd = args.collatz_cmd
    if cmd == "analyze":
        return _analyze(args.n)
    if cmd == "trajectory":
        return _trajectory(args.n, args.max_steps)
    if cmd == "inverse":
        return _inverse(args.m, args.depth, args.k_max, args.max_nodes)
    if cmd == "test-invariants":
        return _invariants(args.limit)
    if cmd == "automaton":
        return _automaton(args.precision, args.word)
    if cmd == "experiment":
        return _experiment(args.limit, args.write)
    if cmd == "theorems":
        return _theorems(args.n)
    if cmd == "odd-part":
        return _odd_part(args.x)
    if cmd == "transducer":
        return _transducer(args.k, args.limit)
    if cmd == "valuation-shift":
        return _valuation_shift(args.precision, args.k_max, args.length)
    if cmd == "joint":
        return _joint(
            args.limit,
            args.k_max,
            args.precision,
            args.pattern_length,
            args.sync_length,
        )
    if cmd == "cylinder":
        return _cylinder(args.ks, args.leftover)
    if cmd == "entropy":
        return _entropy(args.ks, args.length, args.leftover)
    if cmd == "complexity":
        return _complexity(args.k_max, args.write)
    if cmd == "symbolic-graph":
        return _symbolic_graph(args.max_length, args.k_max, args.leftover)
    if cmd == "ui":
        from visualization.app import launch

        return launch()
    raise SystemExit(f"unknown collatz command {cmd!r}")


def _analyze(n: int) -> int:
    n = require_positive_odd(n)
    trans = feature_transition(n)
    word_n = encode(n)
    shifted = multiply_by_three(word_n).word()
    lines = [
        "Accelerated Collatz analysis (odd-only map T)",
        f"n = {trans.n}",
        f"BT(n) = {trans.balanced_ternary_n}",
        "",
        f"3n+1 = {trans.three_n_plus_one}",
        f"BT(3n+1) = {trans.balanced_ternary_three_n_plus_one}",
        f"v2(3n+1) = {trans.v2_three_n_plus_one}",
        "",
        f"T(n) = {trans.T_n}",
        f"BT(T(n)) = {trans.balanced_ternary_T_n}",
        "",
        "Ternary decomposition of 3n+1:",
        f"  multiply-by-3 shift BT(3n) = {shifted}",
        f"  LSD add-+1 case (on n): {lsd_add_one_case(word_n)}",
        f"  shift-then-add-one matches BT(3n+1): "
        f"{str(trans.ternary_shift_add_one_matches).lower()}",
        f"  BT(3n+1) = BT(n)+  (append-plus theorem): "
        f"{str(trans.append_plus_matches).lower()}",
        f"  closed-form 3n+1 features match: "
        f"{str(trans.append_plus_features_match).lower()}",
        "",
        "Digit alignment (LSD / right-aligned):",
        *_digit_alignment(
            trans.balanced_ternary_n,
            shifted,
            trans.balanced_ternary_three_n_plus_one,
            trans.balanced_ternary_T_n,
        ),
        "",
        "Features (n -> 3n+1 -> T(n)) and deltas F(T(n)) - F(n):",
    ]
    fn = trans.features_n.as_dict()
    fy = trans.features_three_n_plus_one.as_dict()
    ft = trans.features_T_n.as_dict()
    for name in NUMERIC_FEATURE_NAMES:
        lines.append(
            f"  {name}: {fn[name]} -> {fy[name]} -> {ft[name]}  "
            f"delta={trans.deltas[f'delta_{name}']}"
        )
    lines.append("")
    print("\n".join(lines))
    return 0


def _digit_alignment(bt_n: str, bt_3n: str, bt_y: str, bt_t: str) -> list[str]:
    width = max(len(bt_n), len(bt_3n), len(bt_y), len(bt_t), 8)
    return [
        f"  BT(n)     {bt_n.rjust(width)}",
        f"  BT(3n)    {bt_3n.rjust(width)}",
        f"  BT(3n+1)  {bt_y.rjust(width)}",
        f"  BT(T(n))  {bt_t.rjust(width)}",
    ]


def _trajectory(n: int, max_steps: int) -> int:
    n = require_positive_odd(n)
    traj = collatz_trajectory(n, max_steps)
    print(
        f"Accelerated trajectory of {n}  max_steps={max_steps}  "
        f"reached_one={str(traj.reached_one).lower()}  "
        f"truncated={str(traj.truncated).lower()}"
    )
    print(f"{'i':>4}  {'n':>12}  {'BT(n)':<24}  {'v2':>4}  {'T(n)':>12}  deltas")

    for i, step in enumerate(traj.steps):
        rec = feature_transition(step.n)
        delta_bits = " ".join(
            f"{name}={rec.deltas[f'delta_{name}']:+d}"
            for name in ("length", "weight", "signed_digit_sum", "number_of_runs")
        )
        print(
            f"{i:>4}  {step.n:>12}  {step.balanced_ternary_n:<24}  "
            f"{step.v2_three_n_plus_one:>4}  {step.T_n:>12}  {delta_bits}"
        )
    if not traj.steps:
        print(f"   0  {n:>12}  {encode(n).word():<24}  (terminal or max_steps=0)")
    print(f"values: {', '.join(str(v) for v in traj.values)}")
    return 0


def _inverse(m: int, depth: int, k_max: int, max_nodes: int) -> int:
    tree = build_inverse_tree(m, depth=depth, k_max=k_max, max_nodes=max_nodes)
    print(format_inverse_tree(tree), end="")
    return 0


def _invariants(limit: int) -> int:
    print(f"Checking Collatz invariants for odd n in [1, {limit}] ...")
    report = verify_collatz_invariants(limit)
    print(f"Checked {report.checked_odd} odd integers.")
    if report.ok:
        print("All invariants passed.")
        return 0
    print(f"FAILED with {len(report.failures)} failure(s). First:")
    f = report.failures[0]
    print(f"  {f.name} at n={f.n}: {f.detail}")
    return 1


def _automaton(precision: int, word: str | None) -> int:
    auto = TwoAdicDigitAutomaton(precision)
    example = word if word is not None else encode(27)
    print(auto.format_report(example), end="")
    return 0


def _experiment(limit: int, write: bool) -> int:
    out_dir: Path | None = None
    if write:
        out_dir = Path("experiments") / "collatz"
    result = run_exhaustive_experiment(limit, output_dir=out_dir)
    print(f"experiment: {result.experiment_name}")
    print(f"range: {result.integer_range}")
    print(f"checked: {result.checked}")
    print(f"timestamp: {result.timestamp}")
    print(f"code_version: {result.code_version}")
    print(f"weight_parity_failures: {result.weight_parity_failures}")
    print(f"ternary_shift_failures: {result.ternary_shift_failures}")
    if result.output_metadata:
        print(f"metadata: {result.output_metadata}")
        print(f"rows: {result.output_rows}")
    status = (
        "ok" if result.weight_parity_failures == 0 and result.ternary_shift_failures == 0
        else "FAILED"
    )
    print(f"status: {status}")
    return 0 if status == "ok" else 1


def _theorems(n: int) -> int:
    if isinstance(n, bool) or not isinstance(n, int) or n == 0:
        raise SystemExit("n must be a nonzero integer")
    word = encode(n)
    plus = append_plus(word)
    actual = encode(3 * n + 1)
    pred = predicted_features_after_append_plus(word)
    feat = extract_features(actual)
    lines = [
        "Layer A: BT(3n+1) = BT(n)+   [PROVED for n != 0]",
        f"n = {n}",
        f"BT(n)  = {word.word()}",
        f"BT(n)+ = {plus.word()}",
        f"BT(3n+1) = {actual.word()}",
        f"append_plus matches encode(3n+1): {str(plus == actual).lower()}",
        "",
        "Closed-form features of 3n+1 vs extract(encode(3n+1)):",
        f"  predicted == actual: {str(pred == feat).lower()}",
        f"  length {feat.length} (n+1)",
        f"  weight {feat.weight} (n+1)",
        f"  signed_digit_sum {feat.signed_digit_sum} (n+1)",
        f"  positive {feat.positive_digit_count} (n+1)  "
        f"negative {feat.negative_digit_count} (unchanged)  "
        f"zeros {feat.zero_count} (unchanged)",
        f"  S^(2) {feat.position_class_sums_period_2}",
        f"  S^(3) {feat.position_class_sums_period_3}",
        "",
    ]
    print("\n".join(lines))
    return 0 if plus == actual and pred == feat else 1


def _odd_part(x: int) -> int:
    if isinstance(x, bool) or not isinstance(x, int):
        raise SystemExit("x must be int")
    word = encode(x)
    k = v2(x)
    print("Layer B: odd-part  x -> x / 2^{v2(x)}")
    print(f"x = {x}")
    print(f"BT(x) = {word.word()}")
    print(f"v2(x) = {'∞' if k is None else k}")
    if x == 0:
        print("odd part of 0 is 0 (valuation infinity)")
        return 0
    if x % 2 != 0:
        print("x is odd; odd-part is x itself.")
        print(f"BT(odd-part) = {odd_part_word(word).word()}")
        return 0
    trans = DivideByTwoTransducer()
    print("LSD /2 trace (carry_in, input, output, carry_out):")
    try:
        for row in trans.trace(word):
            print(f"  {row}")
        got = odd_part_word(word)
        print(f"BT(odd-part) = {got.word()}")
        print(f"integer odd-part = {x // (1 << k)}")
        print(f"match: {str(got == encode(x // (1 << k))).lower()}")
    except LeftoverCarryError as exc:
        print(f"leftover carry (not a finite even integer image): {exc}")
        return 1
    return 0


def _transducer(k: int, limit: int) -> int:
    machine = DivideByTwoPowerTransducer(k)
    report = machine.complexity_report()
    print(f"DivideByTwoPowerTransducer k={k}")
    print(
        f"naive_bound={report['naive_bound']}  reachable={report['reachable']}  "
        f"minimized={report['minimized']}  [reachable/minimized: VERIFIED COMPUTATIONALLY]"
    )
    failures = 0
    checked = 0
    for n in range(-limit, limit + 1):
        x = n * (1 << k)
        checked += 1
        if machine.apply(encode(x)) != encode(n):
            failures += 1
            if failures == 1:
                print(f"FAIL at n={n} x={x}")
    print(f"checked {checked} integers n in [{-limit}, {limit}], x=n*2^{k}")
    print("ok" if failures == 0 else f"FAILED ({failures})")
    return 0 if failures == 0 else 1


def _valuation_shift(precision: int, k_max: int, length: int) -> int:
    auto = AdmissibleValuationAutomaton(precision, k_max)
    report = auto.enumerate_admissible(length)
    print(report.format(), end="")
    return 0


def _joint(
    limit: int,
    k_max: int,
    precision: int,
    pattern_length: int,
    sync_length: int,
) -> int:
    print(
        layer_d_report(
            limit=limit,
            k_max=k_max,
            precision=precision,
            pattern_length=pattern_length,
            sync_length=sync_length,
        ),
        end="",
    )
    return 0


def _cylinder(ks: str, leftover: int) -> int:
    cyl = valuation_cylinder(ks, leftover_q=leftover)
    print(cyl.format(), end="")
    return 0


def _entropy(ks: str, length: int, leftover: int) -> int:
    report = entropy_report(ks, length, leftover_q=leftover)
    print(report.format(), end="")
    return 0


def _complexity(k_max: int, write: bool) -> int:
    out_dir = Path("experiments") / "collatz" if write else None
    result = run_complexity_spectrum(k_max, output_dir=out_dir)
    print(result.format(), end="")
    if result.output_path:
        print(f"wrote {result.output_path}")
    return 0


def _symbolic_graph(max_length: int, k_max: int, leftover: int) -> int:
    graph = build_symbolic_graph(
        max_length=max_length, k_max=k_max, leftover_q=leftover
    )
    print(graph.format(), end="")
    return 0
