"""Research modules may use bt and shared utilities, not visualization."""

from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "src" / "research"
FORBIDDEN_IN_RESEARCH = ("visualization",)


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


def test_research_math_does_not_import_visualization():
    """CLI may launch the optional UI; mathematical modules may not."""
    violations = []
    for path in RESEARCH.rglob("*.py"):
        rel = path.relative_to(RESEARCH)
        if rel.parts[:2] == ("collatz", "cli"):
            continue
        bad = _imported_roots(path).intersection(FORBIDDEN_IN_RESEARCH)
        if bad:
            violations.append(f"{path.relative_to(ROOT)}: {sorted(bad)}")
    assert violations == []
