"""Fast tests for the exact odd fourth-power search tool."""

from __future__ import annotations

import ast
import json
import sqlite3
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
TOOLS = REPO / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import odd_fourth_power_search as ofs


def test_a97_is_even_cube():
    rec = ofs.evaluate_a(97)
    assert rec.classification == ofs.CLASS_EVEN
    assert rec.n == 198636
    assert rec.occupancy == 1
    assert rec.n_is_odd is False
    assert rec.interval_lower <= rec.n**3 < rec.interval_upper
    ofs.verify_hit(97, 198636)


def test_a27_is_odd_square():
    rec = ofs.evaluate_a(27)
    assert rec.classification == ofs.CLASS_ODD_SQUARE
    assert rec.n == 3**8
    assert rec.n_is_odd is True
    assert rec.n_is_square is True
    ofs.verify_hit(27, 3**8)


def test_a8_is_even_cube():
    rec = ofs.evaluate_a(8)
    assert rec.classification == ofs.CLASS_EVEN
    assert rec.n == 2**8
    assert rec.n_is_odd is False
    ofs.verify_hit(8, 256)


def test_occupancy_is_zero_or_one():
    seen = set()
    for a in range(1, 200):
        rec = ofs.evaluate_a(a)
        assert rec.occupancy in (0, 1)
        seen.add(rec.occupancy)
        if rec.n is not None:
            assert rec.interval_lower <= rec.n**3 < rec.interval_upper
            nxt = rec.n + 1
            assert nxt * nxt * nxt >= rec.interval_upper
    assert seen == {0, 1}


def test_walker_source_has_no_float_roots():
    src = Path(ofs.__file__).read_text(encoding="utf-8")
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute) and node.attr in {"sqrt", "log", "log2", "log10"}:
            if isinstance(node.value, ast.Name) and node.value.id == "math":
                raise AssertionError("math float root/log used in search tool")
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Pow):
            if isinstance(node.right, ast.Constant) and isinstance(node.right.value, float):
                raise AssertionError("float exponent in search tool")
    assert "import math" not in src
    assert "from math import" not in src


def test_chunk_resume_does_not_recompute_complete(tmp_path: Path):
    data_dir = tmp_path / "search"
    ofs.init_search(data_dir, a_start=1, a_end=81, chunk_size=20, workers=1)
    first = ofs.run_search(data_dir, workers=1, max_chunks=2, reset_stale=False)
    assert first["processed_chunks"] == 2

    conn = sqlite3.connect(str(data_dir / "search.sqlite"))
    complete_before = conn.execute(
        "SELECT chunk_id, checksum FROM chunks WHERE status = ? ORDER BY a_start",
        (ofs.STATUS_COMPLETE,),
    ).fetchall()
    assert complete_before
    pending = conn.execute(
        "SELECT chunk_id FROM chunks WHERE status = ? ORDER BY a_start",
        (ofs.STATUS_PENDING,),
    ).fetchall()
    assert pending
    conn.execute(
        "UPDATE chunks SET status = ? WHERE chunk_id = ?",
        (ofs.STATUS_FAILED, pending[0][0]),
    )
    conn.commit()
    conn.close()

    second = ofs.run_search(data_dir, workers=1, retry_failed=False, reset_stale=False)
    assert second["processed_chunks"] >= 1

    conn = sqlite3.connect(str(data_dir / "search.sqlite"))
    for chunk_id, digest in complete_before:
        row = conn.execute(
            "SELECT status, checksum FROM chunks WHERE chunk_id = ?",
            (chunk_id,),
        ).fetchone()
        assert row[0] == ofs.STATUS_COMPLETE
        assert row[1] == digest
    failed = conn.execute(
        "SELECT status FROM chunks WHERE chunk_id = ?",
        (pending[0][0],),
    ).fetchone()
    assert failed[0] == ofs.STATUS_FAILED
    conn.close()


def test_manifest_required_keys(tmp_path: Path):
    data_dir = tmp_path / "search"
    ofs.init_search(data_dir, a_start=1, a_end=40, chunk_size=10, workers=1)
    ofs.run_search(data_dir, workers=1)
    manifest = json.loads((data_dir / "manifest.json").read_text(encoding="utf-8"))
    for key in ofs.MANIFEST_KEYS:
        assert key in manifest
    assert manifest["problem"] == ofs.PROBLEM_ID
    assert manifest["parameter_s"] == 2
    assert manifest["algorithm_version"] == ofs.ALGORITHM_ALL
    assert manifest["arithmetic_method"] in {"python-int", "gmpy2-iroot"}


def test_summarize_matches_stored_hits(tmp_path: Path):
    data_dir = tmp_path / "search"
    ofs.init_search(data_dir, a_start=1, a_end=100, chunk_size=25, workers=1)
    ofs.run_search(data_dir, workers=1)
    summary = ofs.summarize(data_dir)
    expected = [ofs.evaluate_a(a) for a in range(1, 100)]
    expected_hits = [rec for rec in expected if rec.n is not None]
    assert summary["interval_cubes"] == len(expected_hits)
    assert summary["even_cubes"] == sum(1 for rec in expected_hits if rec.classification == ofs.CLASS_EVEN)
    assert summary["odd_squares"] == sum(
        1 for rec in expected_hits if rec.classification == ofs.CLASS_ODD_SQUARE
    )
    assert summary["odd_non_squares"] == 0
    summary_as = {int(hit["a"]) for hit in summary["hits"]}
    assert summary_as == {rec.a for rec in expected_hits}
    assert 8 in summary_as
    assert 27 in summary_as
    assert 97 in summary_as
    assert (data_dir / "summaries" / "summary.json").is_file()
    assert (data_dir / "summaries" / "summary.md").is_file()
    assert (data_dir / "hits" / "a_97.json").is_file()


def test_scan_range_rediscovers_known_hits():
    result = ofs.scan_range(1, 120)
    classes = {hit["a"]: hit["classification"] for hit in result["hits"]}
    assert classes[8] == ofs.CLASS_EVEN
    assert classes[27] == ofs.CLASS_ODD_SQUARE
    assert classes[97] == ofs.CLASS_EVEN
    assert result["n_odd_non_square"] == 0
    assert result["n_tested"] == 119
