"""Core `bt` packages must not import research or UI layers."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
BT_ROOT = ROOT / "src" / "bt"
FORBIDDEN = ("research", "collatz", "visualization")


def _imported_roots(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                roots.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.module:
            roots.add(node.module.split(".")[0])
    return roots


def test_bt_core_does_not_import_research_layers():
    if not BT_ROOT.is_dir():
        pytest.skip("src/bt/ does not exist yet (Phase 1 placeholder)")
    files = list(BT_ROOT.rglob("*.py"))
    if not files:
        pytest.skip("src/bt/ has no Python modules yet")
    violations: list[str] = []
    encode_files: list[str] = []
    for path in files:
        rel = path.relative_to(ROOT)
        imported = _imported_roots(path)
        bad = imported.intersection(FORBIDDEN)
        if bad:
            violations.append(f"{rel}: {sorted(bad)}")
        source = path.read_text(encoding="utf-8")
        if "def encode(" in source:
            encode_files.append(str(rel))
    assert violations == []
    if encode_files:
        assert len(encode_files) == 1, f"duplicate encode implementations: {encode_files}"
