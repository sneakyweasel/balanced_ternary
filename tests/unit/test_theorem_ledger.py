"""Theorem ledger paths must exist; markdown must match the JSON."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
JSON_PATH = ROOT / "docs" / "theory" / "theorem_ledger.json"
LEAN_VERIFIED = "EXACT — LEAN VERIFIED"


def _entries() -> list[dict]:
    return json.loads(JSON_PATH.read_text(encoding="utf-8"))


def test_ledger_ids_are_unique():
    ids = [row["id"] for row in _entries()]
    assert ids
    assert len(ids) == len(set(ids))


def test_ledger_required_fields():
    required = ("id", "tag", "statement", "source", "lean", "tests")
    for row in _entries():
        for key in required:
            assert key in row, f"{row.get('id')}: missing {key}"
        source = ROOT / str(row["source"])
        assert source.is_file(), f"{row['id']}: missing source {row['source']}"


def test_ledger_test_paths_exist():
    for row in _entries():
        tests = row.get("tests") or []
        assert tests, f"{row['id']}: tests must be a non-empty list"
        for rel in tests:
            path = ROOT / rel
            assert path.is_file(), f"{row['id']}: missing test {rel}"


def test_ledger_lean_paths_exist_when_required():
    for row in _entries():
        lean = str(row.get("lean") or "").strip()
        if not lean:
            assert row["tag"] != LEAN_VERIFIED, f"{row['id']}: LEAN VERIFIED needs a lean path"
            continue
        path = ROOT / "formal" / lean
        if not path.exists():
            path = ROOT / lean
        assert path.exists(), f"{row['id']}: missing lean {lean}"
        if row["tag"] == LEAN_VERIFIED:
            assert path.is_file() or path.is_dir(), f"{row['id']}: lean path is not a file or dir"


def test_ledger_markdown_is_generated():
    script = ROOT / "tools" / "render_theorem_ledger.py"
    result = subprocess.run(
        [sys.executable, str(script), "--check"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
