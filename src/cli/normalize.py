"""CLI for balanced-ternary normalization theory."""

from __future__ import annotations

import argparse
import json

from bt.normtheory.coeffword import CoeffWord
from bt.normtheory.complexity import measure, profile_families
from bt.normtheory.discovery import discover
from bt.normtheory.graph import rewrite_graph
from bt.normtheory.rewrite import legal_sites, normalize_step
from bt.normtheory.strategies import all_strategies, normal_form


def add_normalize_subparser(subparsers: argparse._SubParsersAction) -> None:
    p = subparsers.add_parser(
        "normalize",
        help="coefficient-word normalization theory (rewrite, strategies, graphs)",
    )
    c = p.add_subparsers(dest="norm_cmd", required=True)

    p_ev = c.add_parser("eval", help="value, canonical NF, and canonicity")
    p_ev.add_argument("coeffs", help="comma-separated integers, LSD-first")

    p_st = c.add_parser("step", help="one legal rewrite at an index")
    p_st.add_argument("coeffs")
    p_st.add_argument("index", type=int)

    p_str = c.add_parser("strategies", help="compare strategies A/B/C/D")
    p_str.add_argument("coeffs")

    p_g = c.add_parser("graph", help="small rewrite graph")
    p_g.add_argument("coeffs")

    p_d = c.add_parser("discover", help="bounded hypothesis explorer")
    p_d.add_argument("--width", type=int, default=3)
    p_d.add_argument("--bound", type=int, default=2)

    p_pr = c.add_parser("profile", help="complexity of a word or families")
    p_pr.add_argument("coeffs", nargs="?", default="")
    p_pr.add_argument("--families", action="store_true")
    p_pr.add_argument("--json", action="store_true")


def _parse_coeffs(text: str) -> CoeffWord:
    parts = [p.strip() for p in text.split(",") if p.strip() != ""]
    if not parts:
        raise ValueError("expected comma-separated integers")
    return CoeffWord(tuple(int(p) for p in parts))


def run_normalize(args: argparse.Namespace) -> int:
    cmd = args.norm_cmd
    if cmd == "eval":
        word = _parse_coeffs(args.coeffs)
        nf = normal_form(word)
        print(f"coeffs = {list(word.coeffs)}")
        print(f"value = {word.value()}")
        print(f"canonical = {word.is_canonical()}")
        print(f"normal form = {list(nf.coeffs)}")
        print(f"NF value = {nf.value()}")
        return 0
    if cmd == "step":
        word = _parse_coeffs(args.coeffs)
        nxt = normalize_step(word, args.index)
        print(f"sites = {list(legal_sites(word))}")
        print(f"after = {list(nxt.coeffs)}")
        print(f"value = {nxt.value()}")
        return 0
    if cmd == "strategies":
        word = _parse_coeffs(args.coeffs)
        traces = all_strategies(word)
        for name, tr in traces.items():
            print(
                f"{name}: result={list(tr.result.coeffs)} "
                f"rewrites={tr.rewrite_count} passes={tr.passes}"
            )
        return 0
    if cmd == "graph":
        word = _parse_coeffs(args.coeffs)
        g = rewrite_graph(word)
        print(json.dumps(g.as_dict(), indent=2))
        return 0
    if cmd == "discover":
        rows = [r.as_dict() for r in discover(args.width, args.bound)]
        print(json.dumps(rows, indent=2))
        return 0
    if cmd == "profile":
        if args.families:
            rows = profile_families(6)
            print(json.dumps(rows, indent=2) if args.json else rows)
            return 0
        word = _parse_coeffs(args.coeffs)
        rep = measure(word)
        print(json.dumps(rep.as_dict(), indent=2) if args.json else rep)
        return 0
    raise ValueError(f"unknown normalize command {cmd}")
