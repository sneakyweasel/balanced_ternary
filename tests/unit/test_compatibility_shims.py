"""Compatibility façades stay thin re-exports of the canonical packages."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
COLLATZ_SHIM = SRC / "collatz"
COLLATZ_CANON = SRC / "research" / "collatz"
BT_SHIM = SRC / "balanced_ternary"
ALLOW_NO_SHIM = frozenset({"problem.py"})


def _py_files(root: Path) -> list[Path]:
    return sorted(p for p in root.rglob("*.py") if p.name != "__pycache__")


def test_collatz_shim_files_are_reexports():
    missing_targets = []
    not_shims = []
    for path in _py_files(COLLATZ_SHIM):
        text = path.read_text(encoding="utf-8")
        if "from research.collatz" not in text:
            not_shims.append(str(path.relative_to(ROOT)))
            continue
        rel = path.relative_to(COLLATZ_SHIM)
        if rel.as_posix() == "__init__.py":
            continue
        target = COLLATZ_CANON / rel
        if not target.exists():
            missing_targets.append(str(rel))
    assert not_shims == []
    assert missing_targets == []


def test_canonical_collatz_modules_have_shims():
    missing = []
    for path in _py_files(COLLATZ_CANON):
        rel = path.relative_to(COLLATZ_CANON)
        if rel.as_posix() in ALLOW_NO_SHIM:
            continue
        shim = COLLATZ_SHIM / rel
        if not shim.exists():
            missing.append(str(rel))
    assert missing == []


def test_balanced_ternary_submodules_are_reexports():
    not_shims = []
    for path in _py_files(BT_SHIM):
        if path.name == "__init__.py":
            continue
        text = path.read_text(encoding="utf-8")
        if "Compatibility shim" not in text:
            not_shims.append(str(path.relative_to(ROOT)))
    assert not_shims == []


def test_automata_root_reexports_bt():
    text = (SRC / "automata" / "__init__.py").read_text(encoding="utf-8")
    assert "from bt.automata import" in text


def test_flattened_invariants_keep_legacy_path():
    from research.collatz.invariants import verify_collatz_invariants as canonical
    from research.collatz.research.invariants import verify_collatz_invariants as nested

    assert nested is canonical
