"""CLI smoke tests for ``btlab research``."""

from __future__ import annotations

import io
from contextlib import redirect_stdout

from cli.main import main


def _run(*args: str) -> str:
    buf = io.StringIO()
    with redirect_stdout(buf):
        code = main(list(args))
    assert code == 0
    return buf.getvalue()


def _run_code(*args: str) -> tuple[int, str]:
    buf = io.StringIO()
    with redirect_stdout(buf):
        code = main(list(args))
    return code, buf.getvalue()


def test_research_analyze_d_is_exact_modular_not_live():
    out = _run("research", "analyze", "D")
    assert "problem: D" in out
    assert "attack modular: SUPPORTED EXACT REACHABLE" in out
    assert "LIVE infinitude is not decided here" in out
    assert "SUPPORTED EXACT LIVE" not in out
    assert "sorry" not in out.lower()


def test_research_reproduce_b_stays_bounded():
    out = _run("research", "reproduce", "B")
    assert "reproduce: ok" in out
    assert "attack reconnaissance: OBSERVATION BOUNDED LIVE_SLICE" in out
    assert "sorry" not in out.lower()


def test_research_attack_ostrowski_modular_and_report_links_lean():
    out = _run("research", "attack", "ostrowski", "modular")
    assert "attack modular: SUPPORTED EXACT REACHABLE" in out
    report = _run("research", "report", "ostrowski")
    assert "origin_mod3_invariant" in report
    assert "Ostrowski.NP.step_fst_dvd_three" in report
    assert "hub_nonreset" in report
    assert "PARKED EXACT LIVE" in report
    assert "ostrowski_L0_infinite" in report
    assert "sorry" not in report.lower()
    assert "admit" not in report.lower()


def test_research_reproduce_ostrowski_keeps_l0_parked():
    out = _run("research", "reproduce", "ostrowski")
    assert "reproduce: ok" in out
    assert "hypothesis ostrowski_L0_infinite: PARKED EXACT LIVE" in out
    assert "LIVE infinitude is not decided here" in out


def test_research_attack_ostrowski_spectral_is_exact_map_class_not_live():
    out = _run("research", "attack", "ostrowski", "spectral")
    assert "attack spectral: SUPPORTED EXACT REACHABLE" in out
    assert "SUPPORTED EXACT LIVE" not in out
    assert "sorry" not in out.lower()


def test_research_deferred_attack_is_not_a_proof():
    code, out = _run_code("research", "attack", "D", "symbolic")
    assert code == 2
    assert "not implemented" in out
    unknown, text = _run_code("research", "analyze", "not-a-problem")
    assert unknown == 2
    assert "unknown problem" in text


def test_research_analyze_balanced_ternary_is_exact_closure_not_live():
    out = _run("research", "analyze", "balanced_ternary")
    assert "problem: balanced_ternary" in out
    assert "attack reconnaissance: OBSERVATION BOUNDED LIVE_SLICE" in out
    assert "attack closure: SUPPORTED EXACT REACHABLE" in out
    assert "SUPPORTED EXACT LIVE" not in out
    assert "sorry" not in out.lower()


def test_research_reproduce_balanced_ternary_links_lean():
    out = _run("research", "reproduce", "balanced_ternary")
    assert "reproduce: ok" in out
    assert "hypothesis balanced_ternary_finite_closure: SUPPORTED EXACT REACHABLE" in out
    report = _run("research", "report", "balanced_ternary")
    assert "doubledTrit_closure" in report
    assert "sorry" not in report.lower()
    assert "admit" not in report.lower()


def test_research_analyze_expanding_d_is_exact_lsd_closure_not_live():
    out = _run("research", "analyze", "expanding_d")
    assert "problem: expanding_d" in out
    assert "attack reconnaissance: OBSERVATION BOUNDED LIVE_SLICE" in out
    assert "attack closure: SUPPORTED EXACT REACHABLE" in out
    assert "SUPPORTED EXACT LIVE" not in out
    assert "sorry" not in out.lower()


def test_research_reproduce_expanding_d_links_lean():
    out = _run("research", "reproduce", "expanding_d")
    assert "reproduce: ok" in out
    assert "hypothesis expanding_d_lsd_closure: SUPPORTED EXACT REACHABLE" in out
    report = _run("research", "report", "expanding_d")
    assert "expandingD_residue_closure" in report
    assert "sorry" not in report.lower()
    assert "admit" not in report.lower()


def test_research_analyze_expanding_j2_is_exact_nine_not_live():
    out = _run("research", "analyze", "expanding_j2")
    assert "problem: expanding_j2" in out
    assert "attack reconnaissance: OBSERVATION BOUNDED LIVE_SLICE" in out
    assert "attack closure: SUPPORTED EXACT REACHABLE" in out
    assert "SUPPORTED EXACT LIVE" not in out
    assert "sorry" not in out.lower()


def test_research_reproduce_expanding_j2_links_lean():
    out = _run("research", "reproduce", "expanding_j2")
    assert "reproduce: ok" in out
    assert "hypothesis expanding_j2_closure: SUPPORTED EXACT REACHABLE" in out
    report = _run("research", "report", "expanding_j2")
    assert "jet2_residue_closure" in report
    assert "sorry" not in report.lower()
    assert "admit" not in report.lower()
