"""Old compatibility packages must not exist."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"


def test_legacy_shim_packages_are_gone():
    assert not (SRC / "collatz").exists()
    assert not (SRC / "balanced_ternary").exists()
    assert not (SRC / "automata").exists()
    assert not (SRC / "research" / "collatz" / "research").exists()
    assert not (SRC / "research" / "collatz" / "bt_arithmetic.py").exists()
    assert not (ROOT / "formal" / "CollatzDual.lean").exists()
    assert not (ROOT / "formal" / "CollatzDual").exists()
