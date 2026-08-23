"""CLI smoke tests for ``btprime congruence``."""

from __future__ import annotations

import io
import json
from contextlib import redirect_stdout

from cli.main import main


def _run(*args: str) -> str:
    buf = io.StringIO()
    with redirect_stdout(buf):
        code = main(list(args))
    assert code == 0
    return buf.getvalue()


def test_roots_agree_with_brute_force():
    out = _run("congruence", "roots", "--poly", "x^2-9", "--k", "4")
    assert "brute force agrees = true" in out
    assert "level counts N_0..N_4 = [1, 1, 3, 6, 6]" in out


def test_roots_of_a_polynomial_with_no_solutions():
    out = _run("congruence", "roots", "--poly", "x^2+3", "--k", "3")
    assert "count = 0" in out


def test_tree_marks_unique_lifts_of_the_fermat_cubic():
    out = _run("congruence", "tree", "--poly", "x^3-x", "--k", "3")
    assert out.count("unique") == 9
    assert "split" in out


def test_tree_json_carries_node_records():
    out = _run("congruence", "tree", "--poly", "x^2-1", "--k", "2", "--json")
    payload = json.loads(out)
    assert payload["k"] == 2
    assert payload["level_counts"] == [1, 2, 2]
    assert {node["kind"] for node in payload["nodes"]} <= {
        "unique",
        "splitting",
        "terminal",
        "singular-persistent",
    }


def test_lift_lists_the_three_singular_lifts():
    out = _run("congruence", "lift", "--poly", "x^2-9", "--k", "1", "--residue", "0")
    assert "kind = singular-persistent" in out
    assert "lifting trits = [-1, 0, 1]" in out
    assert "scaled value f(n)/3^k = -3" in out


def test_lift_reports_a_non_solution():
    out = _run("congruence", "lift", "--poly", "x^2+1", "--k", "1", "--residue", "0")
    assert "not a solution" in out


def test_lift_rejects_a_residue_outside_the_balanced_window():
    buf = io.StringIO()
    with redirect_stdout(buf):
        code = main(["congruence", "lift", "--poly", "x^2-1", "--k", "1", "--residue", "5"])
    assert code == 2
    assert "balanced residue" in buf.getvalue()


def test_classify_reports_phi_classes_and_widths():
    out = _run("congruence", "classify", "--poly", "x^2-9", "--k", "2", "--r", "2")
    assert "kind census" in out
    assert "Phi_2 class" in out
    assert "widths=" in out


def test_triage_verdict_is_proceed():
    out = _run("congruence", "triage", "--k", "3", "--r", "2")
    assert "verdict: proceed" in out
    assert "H1: ok=true" in out
    assert "valuations, shallow k<r:  false" in out
    assert "No complexity claim" in out
