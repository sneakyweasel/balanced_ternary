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

    p_st = c.add_parser("states", help="raw / semantic / Myhill–Nerode residual counts")
    p_st.add_argument("polynomial")
    p_st.add_argument("--depth", type=int, default=3)

    p_min = c.add_parser("minimize", help="exact finite-horizon Myhill–Nerode count")
    p_min.add_argument("polynomial")
    p_min.add_argument("--depth", type=int, default=3)

    p_dist = c.add_parser("distinguish", help="separating words for residual classes")
    p_dist.add_argument("polynomial")
    p_dist.add_argument("--depth", type=int, default=3)

    p_dp = c.add_parser("distinguish-pair", help="shortest and canonical words separating two polynomials")
    p_dp.add_argument("f")
    p_dp.add_argument("g")
    p_dp.add_argument("--depth", type=int, default=3)

    p_rf = c.add_parser("residual-formula", help="residual polynomials and coefficient triples")
    p_rf.add_argument("polynomial")
    p_rf.add_argument("--depth", type=int, default=3)

    p_wit = c.add_parser("witness", help="pairwise distinguishing words among residual states")
    p_wit.add_argument("polynomial")
    p_wit.add_argument("--depth", type=int, default=3)

    p_me = c.add_parser("merge-examples", help="distinct residuals that are equivalent at a finite horizon")
    p_me.add_argument("polynomial")
    p_me.add_argument("--depth", type=int, default=4)

    p_co = c.add_parser("compose", help="cascade complexity of f ∘ g")
    p_co.add_argument("f")
    p_co.add_argument("g")
    p_co.add_argument("--depth", type=int, default=3)

    p_cn = c.add_parser("compose-normalizer", help="residual machine vs bounded normalizer")
    p_cn.add_argument("polynomial")
    p_cn.add_argument("--depth", type=int, default=3)
    p_cn.add_argument("--bound", type=int, default=5)

    p_ps = c.add_parser("profile-states", help="R_k / M_k table up to a max depth")
    p_ps.add_argument("polynomial")
    p_ps.add_argument("--max-depth", type=int, default=5)

    p_pc = c.add_parser(
        "poly-congruence",
        help="function congruence of two polynomials modulo 3^k",
    )
    p_pc.add_argument("f")
    p_pc.add_argument("g")
    p_pc.add_argument("--k", type=int, required=True)

    p_vp = c.add_parser(
        "vanishing-poly",
        help="smallest polynomial that vanishes as a function modulo 3^k",
    )
    p_vp.add_argument("degree", type=int)
    p_vp.add_argument("--k", type=int, required=True)

    p_nc = c.add_parser(
        "newton-class",
        help="residual words of a polynomial with Newton class IDs modulo 3^k",
    )
    p_nc.add_argument("polynomial")
    p_nc.add_argument("--k", type=int, required=True)

    p_cc = c.add_parser(
        "class-collisions",
        help="Newton-class collisions among residual words modulo 3^k",
    )
    p_cc.add_argument("polynomial")
    p_cc.add_argument("--k", type=int, required=True)

    p_cf = c.add_parser(
        "cubic-fibres",
        help="fibre profile of the x^3 Newton image map F_k",
    )
    p_cf.add_argument("--k", type=int, required=True)

    p_cfo = c.add_parser(
        "cubic-fibre",
        help="complete ~_k class of one cubic residual parameter (m, p)",
    )
    p_cfo.add_argument("m", type=int)
    p_cfo.add_argument("p", type=int)
    p_cfo.add_argument("--k", type=int, required=True)

    p_cd = c.add_parser(
        "cubic-deepest",
        help="deepest-layer fibre profile of x^3 at horizon k",
    )
    p_cd.add_argument("--k", type=int, required=True)

    p_cdf = c.add_parser(
        "cubic-deepest-fibre",
        help="deepest-layer fibre of one prefix p at horizon k",
    )
    p_cdf.add_argument("p", type=int)
    p_cdf.add_argument("--k", type=int, required=True)

    p_cl = c.add_parser(
        "cubic-layer",
        help="x^3 residual layer at depth deficit 1 (m=k-2) or 2 (m=k-3)",
    )
    p_cl.add_argument("--k", type=int, required=True)
    p_cl.add_argument("--depth-deficit", type=int, default=1)

    p_clf = c.add_parser(
        "cubic-layer-fibre",
        help="fibre of one prefix p at depth deficit 1 or 2",
    )
    p_clf.add_argument("p", type=int)
    p_clf.add_argument("--k", type=int, required=True)
    p_clf.add_argument("--depth-deficit", type=int, default=1)


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
        from bt.calculus.automata import profile_states
        from bt.calculus.section import parse_poly

        f = parse_poly(args.polynomial)
        rec = profile_states(f, args.depth)
        print(f"raw = {rec.raw}")
        print(f"semantic = {rec.semantic}")
        print(f"Myhill-Nerode = {rec.myhill_nerode}")
        print(f"sample = {rec.sample}")
        print(f"levelled_mealy = {rec.levelled_mealy}")
        print(f"trie = {rec.trie}")
        print(f"compression = {rec.compression}")
        print(f"max_coeff = {rec.max_coeff}")
        return 0
    if cmd == "minimize":
        from bt.calculus.automata import profile_states
        from bt.calculus.section import parse_poly

        f = parse_poly(args.polynomial)
        rec = profile_states(f, args.depth)
        print(f"raw = {rec.raw}")
        print(f"semantic = {rec.semantic}")
        print(f"Myhill-Nerode = {rec.myhill_nerode}")
        print(f"sample = {rec.sample}")
        print("sample is not Myhill-Nerode")
        return 0
    if cmd == "distinguish":
        from bt.calculus.myhill_nerode import distinguishing_pairs
        from bt.calculus.section import parse_poly

        f = parse_poly(args.polynomial)
        pairs = distinguishing_pairs(f, args.depth, limit=8)
        if not pairs:
            print("no separating pair in range")
            return 0
        for row in pairs:
            print(f"r={row['remaining']}  {row['p']}  vs  {row['q']}  word={row['word']}")
        return 0
    if cmd == "distinguish-pair":
        from bt.calculus.myhill_nerode import distinguish_pair
        from bt.calculus.section import parse_poly

        rec = distinguish_pair(parse_poly(args.f), parse_poly(args.g), args.depth)
        print(f"f = {rec['f']}")
        print(f"g = {rec['g']}")
        print(f"f_coeffs = {rec['f_coeffs']}")
        print(f"g_coeffs = {rec['g_coeffs']}")
        inv_f = rec.get("invariant_f", rec.get("invariant_f"))
        inv_g = rec.get("invariant_g", rec.get("invariant_g"))
        print(f"invariant_f = {inv_f}")
        print(f"invariant_g = {inv_g}")
        print(f"equiv = {rec['equiv']}")
        print(f"shortest = {rec['shortest']}")
        print(f"canonical = {rec['canonical']}")
        depth = rec.get("shortest_depth", rec.get("shortest_depth"))
        print(f"shortest_depth = {depth}")
        return 0
    if cmd == "residual-formula":
        from bt.calculus.quadratic import residual_formula_table, rho_triples
        from bt.calculus.section import parse_poly

        f = parse_poly(args.polynomial)
        print(f"f = {f.render()}")
        print("word pack A B C poly closed_x2 closed_x2")
        for row in residual_formula_table(f, args.depth):
            packed = row.get("pack", row.get("pack"))
            closed = row.get("closed_x2", row.get("closed_x2"))
            print(
                f"{row['word']} {packed} {row['A']} {row['B']} {row['C']} "
                f"{row['poly']} {closed}"
            )
        nrho = len(rho_triples(f, args.depth))
        print(f"rho_triples = {nrho}")
        print(f"rho_triples = {nrho}")
        return 0
    if cmd == "witness":
        from bt.calculus.myhill_nerode import witness_table
        from bt.calculus.section import parse_poly

        f = parse_poly(args.polynomial)
        rows = witness_table(f, args.depth, limit=12)
        if not rows:
            print("no residual pair in range")
            return 0
        for row in rows:
            print(
                f"{row['word_p']} vs {row['word_q']}  "
                f"shortest={row['shortest']} canonical={row['canonical']}"
            )
        return 0
    if cmd == "merge-examples":
        from bt.calculus.myhill_nerode import merge_examples, myhill_nerode_count, raw_count
        from bt.calculus.section import parse_poly

        f = parse_poly(args.polynomial)
        print(f"f = {f.render()}")
        print(f"R = {raw_count(f, args.depth)}")
        print(f"M = {myhill_nerode_count(f, args.depth)}")
        rows = merge_examples(f, args.depth, limit=8)
        if not rows:
            print("no merge pair at this horizon")
            return 0
        for row in rows:
            print(
                f"{row.get('word_p', row.get('word_p'))} vs {row.get('word_q', row.get('word_q'))}  "
                f"{row['p']}  vs  {row['q']}  "
                f"diff={row.get('diff', row.get('diff_ABC'))} "
                f"split_next={row.get('split_at_k_plus_1', row.get('split_at_k_plus_1'))}"
            )
        return 0
    if cmd == "compose":
        from bt.calculus.composition import profile_composition
        from bt.calculus.section import parse_poly

        rec = profile_composition(parse_poly(args.f), parse_poly(args.g), args.depth)
        print(f"f = {rec.f}")
        print(f"g = {rec.g}")
        print(f"f∘g = {rec.fog}")
        print(f"M_f = {rec.M_f}")
        print(f"M_g = {rec.M_g}")
        print(f"M_fog = {rec.M_fog}")
        print(f"naive_product = {rec.naive_product}")
        return 0
    if cmd == "compose-normalizer":
        from bt.calculus.normalizer_compose import profile_compose_normalizer
        from bt.calculus.section import parse_poly

        rec = profile_compose_normalizer(parse_poly(args.polynomial), args.depth, args.bound)
        print(f"M = {rec.M}")
        print(f"normalizer_states = {rec.normalizer_states}")
        print(f"composed_upper = {rec.composed_upper}")
        print(f"max_coeff = {rec.max_coeff}")
        print(f"representable = {rec.representable}")
        if rec.obstruction:
            print(f"obstruction = {rec.obstruction}")
        return 0
    if cmd == "profile-states":
        from bt.calculus.automata import profile_states
        from bt.calculus.section import parse_poly

        f = parse_poly(args.polynomial)
        print("k raw semantic Myhill-Nerode sample trie compression")
        for k in range(0, args.max_depth + 1):
            rec = profile_states(f, k)
            print(
                f"{k} {rec.raw} {rec.semantic} {rec.myhill_nerode} "
                f"{rec.sample} {rec.trie} {rec.compression}"
            )
        return 0
    if cmd == "poly-congruence":
        from bt.calculus.poly_congruence import poly_congruence_report
        from bt.calculus.section import parse_poly

        rec = poly_congruence_report(parse_poly(args.f), parse_poly(args.g), args.k)
        yes = "YES" if rec["equivalent"] else "NO"
        print(f"Equivalent modulo 3^{args.k} as functions? {yes}")
        if rec["equivalent"]:
            print(f"coefficient difference = {rec['diff_coeffs']}")
            print(f"valuation profile = {rec['monomial_v3']}")
            print(f"finite-difference profile = {rec['newton']}")
            print(f"finite-difference v3 = {rec['newton_v3']}")
            print(f"candidate invariant = {rec['candidate_invariant']}")
            print(f"phi_f = {rec['phi_f']}")
            print(f"phi_g = {rec['phi_g']}")
            print(f"tau = {rec['tau']}")
        else:
            print(f"shortest distinguishing residue / probe = {rec['probe']}")
            print(f"coefficient difference = {rec['diff_coeffs']}")
            print(f"phi_f = {rec['phi_f']}")
            print(f"phi_g = {rec['phi_g']}")
            print(f"tau = {rec['tau']}")
        return 0
    if cmd == "vanishing-poly":
        from bt.calculus.poly_congruence import vanishing_poly

        rec = vanishing_poly(args.degree, args.k)
        print(f"degree ≤ {rec['degree']}  k = {rec['k']}  modulus = {rec['modulus']}")
        print(f"coeffwise kernel generator = {rec['coeffwise']}")
        if rec["invisible"] is None:
            print("invisible polynomial = none (coefficientwise criterion is exact)")
        else:
            print(f"invisible polynomial = {rec['invisible']}")
            print(f"invisible coeffs = {rec['invisible_coeffs']}")
            print(f"newton = {rec['invisible_newton']}")
            print(f"monomial v3 = {rec['invisible_monomial_v3']}")
            print(f"newton v3 = {rec['invisible_newton_v3']}")
            print(f"factorization = {rec['factorization']}")
        return 0
    if cmd == "newton-class":
        from bt.calculus.cubic import newton_class_table
        from bt.calculus.section import parse_poly

        f = parse_poly(args.polynomial)
        print(f"f = {f.render()}  k = {args.k}")
        print("word poly newton newton_mod_3^k class_id")
        for row in newton_class_table(f, args.k):
            print(
                f"{row['word']} {row['poly']} {row['newton']} "
                f"{row['phi']} {row['class_id']}"
            )
        return 0
    if cmd == "class-collisions":
        from bt.calculus.cubic import collision_table
        from bt.calculus.section import parse_poly

        f = parse_poly(args.polynomial)
        classes = collision_table(f, args.k)
        print(f"f = {f.render()}  k = {args.k}")
        print(f"collision_classes = {len(classes)}")
        for i, rec in enumerate(classes):
            print(f"class {i} size={rec['size']} phi={rec['phi']}")
            for member in rec["members"]:
                print(f"  {member['word']} p={member['p']} {member['poly']}")
        return 0
    if cmd == "cubic-fibres":
        from bt.calculus.cubic_fibres import fibre_report

        rec = fibre_report(args.k)
        print(f"k = {rec['k']}")
        print(f"R_k = {rec['R']}")
        print(f"M_k = {rec['M']}")
        print(f"per_depth = {rec['per_depth']}")
        print(f"sum_C = {rec['sum_C']}")
        print(f"cross_depth = {rec['cross_depth']}")
        print(f"largest_fibre = {rec['largest_fibre']}")
        print(f"histogram = {rec['histogram']}")
        print(f"zero_spine = {rec['zero_spine']}")
        print("examples")
        for fib in rec["examples"]:
            print(f"  {fib}")
        return 0
    if cmd == "cubic-fibre":
        from bt.calculus.cubic_fibres import fibre_of

        members = fibre_of(args.m, args.p, args.k)
        print(f"m = {args.m}  p = {args.p}  k = {args.k}")
        print(f"fibre_size = {len(members)}")
        for m, p in members:
            print(f"  ({m}, {p})")
        return 0
    if cmd == "cubic-deepest":
        from bt.calculus.cubic_deepest import deepest_report

        rec = deepest_report(args.k)
        print(f"k = {rec['k']}")
        print(f"raw prefixes = {rec['raw']}")
        print(f"C(k,k-1) = {rec['C']}")
        print(f"n_fibres = {rec['n_fibres']}")
        print(f"histogram = {rec['histogram']}")
        print(f"zero_fibre_size = {rec['zero_fibre_size']}")
        print(f"largest_fibre = {rec['largest_fibre']}")
        print(f"unit_sign_surplus = {rec['unit_sign_surplus']}")
        print("representatives")
        for fib in rec["examples"]:
            print(f"  {fib}")
        return 0
    if cmd == "cubic-deepest-fibre":
        from bt.calculus.cubic_deepest import deepest_fibre_of, deepest_phi

        members = deepest_fibre_of(args.p, args.k)
        print(f"p = {args.p}  k = {args.k}")
        print(f"phi = {deepest_phi(args.p, args.k)}")
        print(f"fibre_size = {len(members)}")
        for q in members:
            print(f"  {q}")
        return 0
    if cmd == "cubic-layer":
        if args.depth_deficit == 1:
            from bt.calculus.cubic_layer import layer_report

            rec = layer_report(args.k, 1)
            clabel = "C(k,k-2)"
        elif args.depth_deficit == 2:
            from bt.calculus.cubic_deficit_two import def2_report

            rec = def2_report(args.k)
            clabel = "C(k,k-3)"
        else:
            raise ValueError("only depth-deficit 1 or 2 is implemented")
        print(f"k = {rec['k']}")
        print(f"m = {rec['m']}")
        print(f"raw prefixes = {rec['raw']}")
        print(f"N2 classes = {rec['N2']}")
        print(f"N2+N1 classes = {rec['N21']}")
        print(f"full Newton classes = {rec['C']}")
        print(f"{clabel} = {rec['C']}")
        print(f"Delta = {rec['Delta']}")
        print(f"histogram = {rec['histogram']}")
        print(f"kinds = {rec['kinds']}")
        print("fibre types")
        for fib in rec["examples"]:
            print(f"  {fib}")
        return 0
    if cmd == "cubic-layer-fibre":
        if args.depth_deficit == 1:
            from bt.calculus.cubic_layer import inter_fibre_of

            members = inter_fibre_of(args.p, args.k)
            m = args.k - 2
        elif args.depth_deficit == 2:
            from bt.calculus.cubic_deficit_two import def2_fibre_of

            members = def2_fibre_of(args.p, args.k)
            m = args.k - 3
        else:
            raise ValueError("only depth-deficit 1 or 2 is implemented")
        print(f"p = {args.p}  k = {args.k}  m = {m}")
        print(f"fibre_size = {len(members)}")
        for q in members:
            print(f"  {q}")
        return 0
    raise ValueError(f"unknown calculus command {cmd}")
