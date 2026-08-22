"""Command-line interface for balanced ternary and Collatz research tools."""

from __future__ import annotations

import argparse
import sys

from balanced_ternary.arithmetic import format_factorization, is_prime
from balanced_ternary.features import signed_digit_sum, weight
from balanced_ternary.invariants import (
    automaton_residue,
    lsd_nonzero_index,
    v3,
    verify_invariants,
)
from balanced_ternary.oeis_maps import bt_reverse, bt_reverse_tail
from balanced_ternary.representation import decode, encode, is_canonical
from collatz.cli import add_collatz_subparser, run_collatz


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="btprime",
        description=(
            "Balanced ternary arithmetic and Collatz exponent-code research. "
            "Inspect canonical words, modular residues, and exact Collatz models."
        ),
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_enc = sub.add_parser("encode", help="integer -> canonical balanced ternary")
    p_enc.add_argument("n", type=int)

    p_dec = sub.add_parser("decode", help="balanced ternary word -> integer")
    p_dec.add_argument("word")

    p_an = sub.add_parser("analyze", help="print features of an integer")
    p_an.add_argument("n", type=int)

    p_res = sub.add_parser(
        "residue", help="automaton residue of a word modulo q"
    )
    p_res.add_argument("word")
    p_res.add_argument("--mod", type=int, required=True, dest="modulus")

    p_inv = sub.add_parser(
        "test-invariants",
        help="exhaustively verify balanced-ternary identities on [-limit, limit]",
    )
    p_inv.add_argument("--limit", type=int, default=100_000)

    p_rev = sub.add_parser(
        "reverse",
        help="A134028: reverse canonical balanced ternary digits (W)",
    )
    p_rev.add_argument("n", type=int)

    p_revt = sub.add_parser(
        "reverse-tail",
        help="A351702: reverse all balanced ternary digits except the MSD",
    )
    p_revt.add_argument("n", type=int)

    add_collatz_subparser(sub)

    args = parser.parse_args(argv)

    if args.cmd == "encode":
        print(encode(args.n).word())
        return 0
    if args.cmd == "decode":
        print(decode(args.word))
        return 0
    if args.cmd == "analyze":
        print(_analyze_text(args.n), end="")
        return 0
    if args.cmd == "residue":
        print(automaton_residue(args.word, args.modulus))
        return 0
    if args.cmd == "test-invariants":
        return _run_invariants(args.limit)
    if args.cmd == "reverse":
        print(bt_reverse(args.n))
        return 0
    if args.cmd == "reverse-tail":
        print(bt_reverse_tail(args.n))
        return 0
    if args.cmd == "collatz":
        return run_collatz(args)
    parser.error(f"unknown command {args.cmd!r}")
    return 2


def _analyze_text(n: int) -> str:
    word = encode(n)
    displayed = word.word()
    canonical = "yes" if is_canonical(displayed) else "no"
    # Re-parse the displayed string so Canonical reflects the printed word.
    assert decode(displayed) == n
    w = weight(word)
    lsd_nz = lsd_nonzero_index(word)
    val3 = v3(n)
    v3_display = "∞" if val3 is None else str(val3)
    lsd_display = "none" if lsd_nz is None else str(lsd_nz)
    prime = is_prime(n)
    lines = [
        f"Integer: {n}",
        f"Balanced ternary: {displayed}",
        f"Canonical: {canonical}",
        "",
        f"Weight: {w}",
        f"Weight parity: {w % 2}",
        f"Signed digit sum: {signed_digit_sum(word)}",
        "",
        f"v3(n): {v3_display}",
        f"Least significant nonzero digit position: {lsd_display}",
        "",
        f"Prime: {str(prime).lower()}",
        f"Factorization: {format_factorization(n)}",
        "",
        "Residues:",
    ]
    for q in (2, 3, 5, 7):
        lines.append(f"  mod {q}: {n % q}")
    lines.append("")
    return "\n".join(lines)


def _run_invariants(limit: int) -> int:
    print(f"Checking invariants for n in [{-limit}, {limit}] ...")
    report = verify_invariants(limit)
    print(f"Checked {report.checked} integers.")
    if report.ok:
        print("All invariants passed.")
        return 0
    print(f"FAILED with {len(report.failures)} failure(s). First:")
    f = report.failures[0]
    print(f"  {f.name} at n={f.n}: {f.detail}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
