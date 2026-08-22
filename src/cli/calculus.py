"""CLI for the balanced-ternary calculus."""

from __future__ import annotations

import argparse
import json

from bt.calculus.complexity import measure
from bt.calculus.derivative import D, lsd
from bt.calculus.discovery import discover_closed
from bt.calculus.expressions import ED, EInt
from bt.calculus.locality import all_profiles, profile
from bt.calculus.normalization import normal_form
from bt.calculus.order import cmp3
from bt.calculus.select import select3
from bt.calculus.semantics import evaluate
from bt.calculus.trit import algebraic_name
from bt.calculus.vm import evaluate_direct, run_postfix


def add_calculus_subparser(subparsers: argparse._SubParsersAction) -> None:
    p = subparsers.add_parser(
        "calculus",
        help="balanced-ternary calculus (trit, D/I_a, rewrite, VM)",
    )
    c = p.add_subparsers(dest="cal_cmd", required=True)

    p_ev = c.add_parser("eval", help="evaluate D / lsd of an integer")
    p_ev.add_argument("n", type=int)

    p_rw = c.add_parser("rewrite", help="normalize D(I+(n)) as a demo")
    p_rw.add_argument("n", type=int)

    p_cmp = c.add_parser("cmp3", help="three-way comparison")
    p_cmp.add_argument("x", type=int)
    p_cmp.add_argument("y", type=int)

    p_sel = c.add_parser("select3", help="select3(c, xm, xz, xp)")
    p_sel.add_argument("c", type=int)
    p_sel.add_argument("x_minus", type=int)
    p_sel.add_argument("x_zero", type=int)
    p_sel.add_argument("x_plus", type=int)

    p_vm = c.add_parser("vm", help="evaluate a postfix calculus program")
    p_vm.add_argument("program", nargs="+")

    p_disc = c.add_parser("discover", help="bounded closed-term identity clusters")
    p_disc.add_argument("--depth", type=int, default=2)
    p_disc.add_argument("--seed", type=int, default=5)

    p_pr = c.add_parser("profile", help="information profile of an operator")
    p_pr.add_argument("symbol", nargs="?", default="")
    p_pr.add_argument("--json", action="store_true")


def run_calculus(args: argparse.Namespace) -> int:
    cmd = args.cal_cmd
    if cmd == "eval":
        n = args.n
        print(f"n = {n}")
        print(f"lsd = {int(lsd(n))}")
        print(f"D(n) = {D(n)}")
        print(f"n = lsd + 3 D(n): {n == int(lsd(n)) + 3 * D(n)}")
        print(f"trit algebra: {algebraic_name()}")
        return 0
    if cmd == "rewrite":
        from bt.calculus.expressions import EIm, EIp, render

        demo = ED(EIp(ED(EIm(EInt(args.n)))))
        nf = normal_form(demo)
        print(f"expr value = {evaluate(demo)}")
        print(f"normal form value = {evaluate(nf)}")
        print(f"normal form = {render(nf)}")
        print(f"measure = {measure(demo)}")
        return 0
    if cmd == "cmp3":
        print(int(cmp3(args.x, args.y)))
        return 0
    if cmd == "select3":
        print(select3(args.c, args.x_minus, args.x_zero, args.x_plus))
        return 0
    if cmd == "vm":
        program = " ".join(args.program)
        rec = run_postfix(program)
        print(f"value = {rec.value}")
        print(f"stack_depth = {rec.stack_depth}")
        print(f"expression_size = {rec.expression_size}")
        print(f"trit_ops = {rec.trit_ops}")
        print(f"carry_ops = {rec.carry_ops}")
        print(f"direct = {evaluate_direct(program)}")
        return 0
    if cmd == "discover":
        hits = discover_closed(max_depth=args.depth, seed=args.seed)
        print(f"candidates: {len(hits)}")
        for cand in hits[:20]:
            print(f"  {cand.left} ~ {cand.right}  [{cand.status}]")
            print(f"    {cand.notes}")
        return 0
    if cmd == "profile":
        if args.symbol:
            rec = profile(args.symbol)
            rows = [rec]
        else:
            rows = list(all_profiles())
        if args.json:
            print(json.dumps([r.as_dict() for r in rows], indent=2))
            return 0
        for rec in rows:
            print(
                f"{rec.operator}: {rec.locality_class} "
                f"(states={rec.state_complexity}, delay={rec.delay})"
            )
        return 0
    raise ValueError(f"unknown calculus command {cmd}")
