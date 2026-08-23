"""CLI smoke tests for ``btprime congruence``."""

from __future__ import annotations

import io
import json
from contextlib import redirect_stdout

import pytest

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


@pytest.mark.slow
def test_triage_verdict_is_proceed():
    out = _run("congruence", "triage", "--k", "3", "--r", "2")
    assert "verdict: proceed" in out
    assert "H1: ok=true" in out
    assert "valuations, shallow k<r:  false" in out
    assert "No complexity claim" in out


def test_state_shows_the_quotient_chain():
    out = _run("congruence", "state", "--poly", "x^2-9", "--k", "4", "--r", "3")
    assert "Phi_r has 729 states" in out
    assert "unit orbits 53" in out
    assert "minimal L_r = 43" in out
    assert "closed form (3^(r+1)-1)/2 + r holds = true" in out
    assert "not minimal" in out


def test_state_json_carries_per_level_classes():
    out = _run("congruence", "state", "--poly", "x^2-9", "--k", "3", "--r", "2", "--json")
    payload = json.loads(out)
    assert payload["r"] == 2
    assert payload["deep_bound"] == 15
    assert payload["strata"] == {"dominated": 2, "undominated": 13}
    for row in payload["levels"]:
        assert row["behaviours"] <= row["phi_classes"]


@pytest.mark.parametrize("poly", ["x^2-9", "x^3-x", "x^2-7", "x^4-1"])
def test_state_normal_form_matches_the_behaviour_count_on_real_nodes(poly):
    # The normal-form theorem, exercised on genuine lifting nodes.
    out = _run("congruence", "state", "--poly", poly, "--k", "4", "--r", "2", "--json")
    for row in json.loads(out)["levels"]:
        if row["deep"]:
            assert row["normal_forms"] == row["behaviours"]
            assert 0 <= row["dominated_nodes"] <= row["nodes"]


def test_state_reports_the_strata_split():
    out = _run("congruence", "state", "--poly", "x^2-9", "--k", "3", "--r", "3")
    assert "L_r splits as 3 dominated" in out
    assert "40 undominated" in out
    assert "unit-scaling orbit" in out


def test_state_refuses_an_expensive_horizon_without_the_flag():
    out = _run("congruence", "state", "--poly", "x^3-x", "--k", "2", "--r", "6")
    assert "needs allow_expensive=True" in out


def test_distinguish_finds_the_canonical_live_witness():
    out = _run("congruence", "distinguish", "--r", "3", "--", "x", "-x")
    assert "left  = x" in out
    assert "right = -x" in out
    assert "phi equal = false, behaviour equal = true" in out
    assert "first distinguishing depth = none" in out
    assert "a unit multiple" in out
    assert "both states are dead" not in out


def test_distinguish_flags_the_vacuous_dead_pair():
    out = _run("congruence", "distinguish", "--r", "2", "--", "1", "-1")
    assert "both states are dead" in out
    assert "proves nothing" in out


def test_distinguish_reports_a_genuine_separation():
    out = _run("congruence", "distinguish", "--r", "2", "x^2", "x^2-3")
    assert "r = 1: phi equal = true, behaviour equal = true" in out
    assert "first distinguishing depth = 2" in out
