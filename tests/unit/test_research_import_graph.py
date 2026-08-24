"""Research, CLI, and UI modules use canonical packages, not compatibility façades."""

from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "src" / "research"
CLI = ROOT / "src" / "cli"
VIS = ROOT / "src" / "visualization"
FORBIDDEN_IN_RESEARCH = ("visualization", "balanced_ternary", "collatz", "automata")
FORBIDDEN_IN_EDGES = ("balanced_ternary", "collatz", "automata")


def _imported_roots(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                roots.add(alias.name.split(".", 1)[0])
        elif isinstance(node, ast.ImportFrom) and node.module:
            roots.add(node.module.split(".", 1)[0])
    return roots


def _violations(root: Path, forbidden: set[str] | tuple[str, ...], skip=None) -> list[str]:
    found = []
    for path in root.rglob("*.py"):
        rel = path.relative_to(root)
        if skip and skip(rel):
            continue
        bad = _imported_roots(path).intersection(forbidden)
        if bad:
            found.append(f"{path.relative_to(ROOT)}: {sorted(bad)}")
    return found


def test_research_math_does_not_import_visualization_or_shims():
    """CLI may launch the optional UI; mathematical modules may not."""
    found = []
    for path in RESEARCH.rglob("*.py"):
        rel = path.relative_to(RESEARCH)
        imported = _imported_roots(path)
        forbidden = set(FORBIDDEN_IN_RESEARCH)
        if rel.parts[:2] == ("collatz", "cli"):
            forbidden.discard("visualization")
        bad = imported.intersection(forbidden)
        if bad:
            found.append(f"{path.relative_to(ROOT)}: {sorted(bad)}")
    assert found == []


def test_cli_and_visualization_do_not_import_compatibility_shims():
    assert _violations(CLI, FORBIDDEN_IN_EDGES) == []
    assert _violations(VIS, FORBIDDEN_IN_EDGES) == []
