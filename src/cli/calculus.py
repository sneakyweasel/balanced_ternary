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

    p_sd = c.add_parser("section-deriv", help="section derivative 𝔇_a of a Z[x] polynomial")
    p_sd.add_argument("polynomial")
    p_sd.add_argument("--section", type=int, default=0)

    p_nd = c.add_parser("normalized-deriv", help="hat D of a raw coefficient word")
    p_nd.add_argument("coeffs", help="comma-separated LSD-first integers")

    p_jet = c.add_parser("jet", help="integer jet J_k(n)")
    p_jet.add_argument("n", type=int)
    p_jet.add_argument("--depth", type=int, default=4)

    p_fj = c.add_parser("function-jet", help="residual section jet of a polynomial along n")
    p_fj.add_argument("polynomial")
    p_fj.add_argument("n", type=int)
    p_fj.add_argument("--depth", type=int, default=3)

    p_cj = c.add_parser("compare-jets", help="compare function jets of two polynomials")
    p_cj.add_argument("f")
    p_cj.add_argument("g")
    p_cj.add_argument("--depth", type=int, default=3)
    p_cj.add_argument("--n", type=int, default=5)

    p_pj = c.add_parser("profile-jet", help="residual-state profile of a polynomial")
    p_pj.add_argument("polynomial")
    p_pj.add_argument("--depth", type=int, default=3)
    p_pj.add_argument("--json", action="store_true")

    p_st = c.add_parser("states", help="raw vs minimized residual-state counts")
    p_st.add_argument("polynomial")
    p_st.add_argument("--depth", type=int, default=3)


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
    if cmd == "section-deriv":
        from bt.calculus.section import parse_poly

        f = parse_poly(args.polynomial)
        a = args.section
        df = f.section_deriv(a)
        print(f"f = {f.render()}")
        print(f"a = {a}")
        print(f"rho = {f.rho(a)}")
        print(f"D_a f = {df.render()}")
        print(f"degree f = {f.degree} degree D_a = {df.degree}")
        print(f"reconstruction at x=0: {f.eval(a) == f.rho(a) + 3 * df.eval(0)}")
        return 0
    if cmd == "normalized-deriv":
        from bt.normtheory.coeffword import CoeffWord
        from bt.normtheory.calculus_link import D_coeff
        from bt.normtheory.hatd import hatD, hatD_raw

        parts = [p.strip() for p in args.coeffs.split(",") if p.strip() != ""]
        word = CoeffWord(tuple(int(p) for p in parts))
        print(f"P = {list(word.coeffs)} value = {word.value()}")
        print(f"D_coeff = {list(D_coeff(word).coeffs)} value = {D_coeff(word).value()}")
        print(f"hatD_raw = {list(hatD_raw(word).coeffs)} value = {hatD_raw(word).value()}")
        print(f"hatD = {list(hatD(word).coeffs)} value = {hatD(word).value()}")
        return 0
    if cmd == "jet":
        from bt.calculus.jets import integer_jet, residual_argument

        print(f"J_{args.depth}({args.n}) = {list(integer_jet(args.n, args.depth))}")
        print(f"D^{args.depth}({args.n}) = {residual_argument(args.n, args.depth)}")
        return 0
    if cmd == "function-jet":
        from bt.calculus.jets import function_jet_of_integer, reconstruction_holds
        from bt.calculus.section import parse_poly

        f = parse_poly(args.polynomial)
        jet = function_jet_of_integer(f, args.n, args.depth)
        print(f"f = {f.render()}")
        print(f"word = {list(jet.word)}")
        print(f"output trits = {list(jet.output_trits)}")
        print(f"residual = {jet.residual().render()}")
        print(f"reconstruction = {reconstruction_holds(f, args.n, args.depth)}")
        return 0
    if cmd == "compare-jets":
        from bt.calculus.jets import function_jet_of_integer
        from bt.calculus.section import parse_poly

        f = parse_poly(args.f)
        g = parse_poly(args.g)
        jf = function_jet_of_integer(f, args.n, args.depth)
        jg = function_jet_of_integer(g, args.n, args.depth)
        print(f"f output = {list(jf.output_trits)}")
        print(f"g output = {list(jg.output_trits)}")
        print(f"same path = {jf.word == jg.word}")
        return 0
    if cmd == "profile-jet":
        from bt.calculus.jet_locality import profile_jet
        from bt.calculus.section import parse_poly

        f = parse_poly(args.polynomial)
        rec = profile_jet(f, args.depth)
        if args.json:
            print(json.dumps(rec.as_dict(), indent=2))
        else:
            print(rec)
        return 0
    if cmd == "states":
        from bt.calculus.jet_locality import profile_jet
        from bt.calculus.section import parse_poly

        f = parse_poly(args.polynomial)
        rec = profile_jet(f, args.depth)
        print(f"raw = {rec.raw_states}")
        print(f"minimized = {rec.minimized_states}")
        print(f"max_coeff = {rec.max_coeff}")
        return 0
    raise ValueError(f"unknown calculus command {cmd}")
