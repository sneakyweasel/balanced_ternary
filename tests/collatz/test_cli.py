"""CLI smoke tests for ``btprime collatz ...``."""

from __future__ import annotations

import io
from contextlib import redirect_stdout

from balanced_ternary.cli import main
from balanced_ternary.representation import encode
from collatz.core import collatz_step


def _run(*args: str) -> str:
    buf = io.StringIO()
    with redirect_stdout(buf):
        code = main(list(args))
    assert code == 0
    return buf.getvalue()


def test_collatz_analyze_27():
    out = _run("collatz", "analyze", "27")
    word = encode(27).word()
    assert "n = 27" in out
    assert f"BT(n) = {word}" in out
    assert "T(n) = 41" in out
    assert f"BT(T(n)) = {encode(41).word()}" in out
    assert "v2(3n+1) = 1" in out
    assert "shift-then-add-one matches BT(3n+1): true" in out
    assert "BT(3n+1) = BT(n)+  (append-plus theorem): true" in out
    assert "delta=" in out


def test_collatz_trajectory_27():
    out = _run("collatz", "trajectory", "27", "--max-steps", "5")
    assert "Accelerated trajectory of 27" in out
    assert str(collatz_step(27)) in out
    assert "values:" in out


def test_collatz_inverse_one():
    out = _run("collatz", "inverse", "1", "--depth", "2", "--k-max", "10")
    assert "root=1" in out
    assert "cycle k=2 -> 1" in out
    assert "5" in out


def test_collatz_test_invariants():
    out = _run("collatz", "test-invariants", "--limit", "300")
    assert "All invariants passed." in out
    assert "Checked 150 odd integers." in out


def test_collatz_automaton():
    out = _run("collatz", "automaton", "--precision", "4")
    assert "precision K=4" in out
    assert "modulus=2^4=16" in out
    assert "AT_LEAST_K" in out
    assert "Path for word" in out
    assert "odd residues" in out


def test_collatz_theorems():
    out = _run("collatz", "theorems", "27")
    assert "BT(n)+" in out
    assert "append_plus matches encode(3n+1): true" in out


def test_collatz_odd_part():
    out = _run("collatz", "odd-part", "82")
    assert "v2(x) = 1" in out
    assert "BT(odd-part)" in out


def test_collatz_transducer():
    out = _run("collatz", "transducer", "--k", "2", "--limit", "80")
    assert "naive_bound=9" in out
    assert "ok" in out


def test_collatz_valuation_shift():
    out = _run(
        "collatz", "valuation-shift",
        "--precision", "6", "--k-max", "4", "--length", "3",
    )
    assert "Admissible valuation prefixes" in out
    assert "contracting=" in out


def test_collatz_joint():
    out = _run(
        "collatz", "joint",
        "--limit", "50", "--k-max", "4", "--precision", "6",
        "--pattern-length", "1", "--sync-length", "1",
    )
    assert "Joint digit/valuation graph" in out
    assert "images ≡ 0 (mod 3): 0" in out


def test_collatz_cylinder():
    out = _run("collatz", "cylinder", "--ks", "1,1")
    assert "ks=(1, 1)" in out
    assert "matches Haar" in out
    assert "admissible: true" in out


def test_collatz_entropy():
    out = _run("collatz", "entropy", "--ks", "1", "--length", "4")
    assert "H_L (base 3)" in out
    assert "VERIFIED COMPUTATIONALLY" in out


def test_collatz_complexity():
    out = _run("collatz", "complexity", "--k-max", "3")
    assert "N_k" in out
    assert "CONJECTURE" in out


def test_collatz_symbolic_graph():
    out = _run(
        "collatz", "symbolic-graph",
        "--max-length", "2", "--k-max", "3",
    )
    assert "Symbolic Collatz futures" in out
    assert "nodes=" in out
