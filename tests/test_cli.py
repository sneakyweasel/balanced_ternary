"""CLI smoke tests for ``btprime``."""

from __future__ import annotations

import io
from contextlib import redirect_stdout

from balanced_ternary.cli import main
from balanced_ternary.representation import decode, encode


def _run(*args: str) -> str:
    buf = io.StringIO()
    with redirect_stdout(buf):
        code = main(list(args))
    assert code == 0
    return buf.getvalue()


def test_encode_decode_cli_round_trip():
    word = _run("encode", "42").strip()
    assert decode(word) == 42
    assert word == encode(42).word()
    value = _run("decode", word).strip()
    assert int(value) == 42


def test_analyze_uses_encoded_word():
    n = 42
    word = encode(n).word()
    out = _run("analyze", str(n))
    assert f"Integer: {n}" in out
    assert f"Balanced ternary: {word}" in out
    assert "Canonical: yes" in out
    assert "Prime: false" in out
    assert "Weight:" in out
    assert "v3(n):" in out
    assert "mod 7:" in out
    assert decode(word) == n


def test_analyze_zero_and_prime():
    out0 = _run("analyze", "0")
    assert "Balanced ternary: 0" in out0
    assert "v3(n): ∞" in out0
    assert "Prime: false" in out0

    out5 = _run("analyze", "5")
    assert f"Balanced ternary: {encode(5).word()}" in out5
    assert "Prime: true" in out5


def test_residue_cli():
    word = encode(19).word()
    out = _run("residue", word, "--mod", "7").strip()
    assert int(out) == 19 % 7


def test_test_invariants_cli():
    out = _run("test-invariants", "--limit", "200")
    assert "All invariants passed." in out
    assert "Checked 401 integers." in out


def test_reverse_cli_matches_a134028():
    assert _run("reverse", "21").strip() == "7"
    assert _run("reverse", "20").strip() == "-20"
    assert _run("reverse-tail", "224").strip() == "168"
