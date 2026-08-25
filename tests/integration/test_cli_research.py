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


def test_research_analyze_expanding_j3_is_exact_twenty_seven_not_live():
    out = _run("research", "analyze", "expanding_j3")
    assert "problem: expanding_j3" in out
    assert "attack reconnaissance: OBSERVATION BOUNDED LIVE_SLICE" in out
    assert "attack closure: SUPPORTED EXACT REACHABLE" in out
    assert "SUPPORTED EXACT LIVE" not in out
    assert "sorry" not in out.lower()


def test_research_reproduce_expanding_j3_links_lean():
    out = _run("research", "reproduce", "expanding_j3")
    assert "reproduce: ok" in out
    assert "hypothesis expanding_j3_closure: SUPPORTED EXACT REACHABLE" in out
    report = _run("research", "report", "expanding_j3")
    assert "jet3_residue_closure" in report
    assert "sorry" not in report.lower()
    assert "admit" not in report.lower()


def test_research_analyze_d_add_is_exact_three_not_live():
    out = _run("research", "analyze", "d_add")
    assert "problem: d_add" in out
    assert "attack reconnaissance: OBSERVATION BOUNDED LIVE_SLICE" in out
    assert "attack closure: SUPPORTED EXACT REACHABLE" in out
    assert "SUPPORTED EXACT LIVE" not in out
    assert "sorry" not in out.lower()


def test_research_reproduce_d_add_links_lean():
    out = _run("research", "reproduce", "d_add")
    assert "reproduce: ok" in out
    assert "hypothesis d_add_residual_closure: SUPPORTED EXACT REACHABLE" in out
    report = _run("research", "report", "d_add")
    assert "dAdd_residual_closure" in report
    assert "sorry" not in report.lower()
    assert "admit" not in report.lower()


def test_research_analyze_signed_digit_residual_is_exact_three_not_live():
    out = _run("research", "analyze", "signed_digit_residual")
    assert "problem: signed_digit_residual" in out
    assert "attack reconnaissance: OBSERVATION BOUNDED LIVE_SLICE" in out
    assert "attack closure: SUPPORTED EXACT REACHABLE" in out
    assert "SUPPORTED EXACT LIVE" not in out
    assert "sorry" not in out.lower()


def test_research_reproduce_signed_digit_residual_links_lean():
    out = _run("research", "reproduce", "sdr")
    assert "reproduce: ok" in out
    assert "hypothesis sdr_lambda1_u2_closure: SUPPORTED EXACT REACHABLE" in out
    assert "hypothesis sdr_scalar_lambda3: REFUTED" in out
    assert "hypothesis sdr_geometry_controls_phase: REFUTED" in out
    assert "hypothesis sdr_maxabs_determines_mealy: REFUTED" in out
    report = _run("research", "report", "signed_digit_residual")
    assert "lambda1_u2_residual_closure" in report
    assert "sorry" not in report.lower()
    assert "admit" not in report.lower()


def test_research_analyze_signed_digit_residual_geometry_is_exact_three_not_live():
    out = _run("research", "analyze", "signed_digit_residual_geometry")
    assert "problem: signed_digit_residual_geometry" in out
    assert "attack reconnaissance: OBSERVATION BOUNDED LIVE_SLICE" in out
    assert "attack closure: SUPPORTED EXACT REACHABLE" in out
    assert "SUPPORTED EXACT LIVE" not in out
    assert "sorry" not in out.lower()


def test_research_reproduce_signed_digit_residual_geometry_links_lean():
    out = _run("research", "reproduce", "sdrg")
    assert "reproduce: ok" in out
    assert "hypothesis sdrg_lambda1_u2_interval: SUPPORTED EXACT REACHABLE" in out
    assert "hypothesis sdrg_lattice_all_U: REFUTED" in out
    assert "hypothesis sdrg_sign_halves_mealy: REFUTED" in out
    report = _run("research", "report", "signed_digit_residual_geometry")
    assert "lambda1_interval_reachable" in report
    assert "sorry" not in report.lower()
    assert "admit" not in report.lower()


def test_research_analyze_signed_digit_residual_minimality_is_exact_three_not_live():
    out = _run("research", "analyze", "signed_digit_residual_minimality")
    assert "problem: signed_digit_residual_minimality" in out
    assert "attack reconnaissance: OBSERVATION BOUNDED LIVE_SLICE" in out
    assert "attack closure: SUPPORTED EXACT REACHABLE" in out
    assert "SUPPORTED EXACT LIVE" not in out
    assert "sorry" not in out.lower()


def test_research_reproduce_signed_digit_residual_minimality_links_lean():
    out = _run("research", "reproduce", "sdrm")
    assert "reproduce: ok" in out
    assert "hypothesis sdrm_lambda1_u2_minimal: SUPPORTED EXACT REACHABLE" in out
    assert "hypothesis sdrm_merge_exists: REFUTED" in out
    assert "hypothesis sdrm_mod3_merges: REFUTED" in out
    report = _run("research", "report", "signed_digit_residual_minimality")
    assert "residual_separation" in report
    assert "sorry" not in report.lower()
    assert "admit" not in report.lower()


def test_research_analyze_signed_digit_constrained_controls_is_exact_ten_not_live():
    out = _run("research", "analyze", "signed_digit_constrained_controls")
    assert "problem: signed_digit_constrained_controls" in out
    assert "attack reconnaissance: OBSERVATION BOUNDED LIVE_SLICE" in out
    assert "attack closure: SUPPORTED EXACT REACHABLE" in out
    assert "SUPPORTED EXACT LIVE" not in out
    assert "sorry" not in out.lower()


def test_research_reproduce_signed_digit_constrained_controls_links_lean():
    out = _run("research", "reproduce", "sdcc")
    assert "reproduce: ok" in out
    assert "hypothesis sdrc_norepeat_u2_product: SUPPORTED EXACT REACHABLE" in out
    assert "hypothesis sdrc_need_constant: REFUTED" in out
    assert "hypothesis sdrc_residual_merge: REFUTED" in out
    report = _run("research", "report", "signed_digit_constrained_controls")
    assert "any_word_separation" in report
    assert "sorry" not in report.lower()
    assert "admit" not in report.lower()


def test_research_analyze_signed_digit_short_horizon_is_exact_seven_not_live():
    out = _run("research", "analyze", "signed_digit_short_horizon")
    assert "problem: signed_digit_short_horizon" in out
    assert "attack reconnaissance: OBSERVATION BOUNDED LIVE_SLICE" in out
    assert "attack closure: SUPPORTED EXACT REACHABLE" in out
    assert "SUPPORTED EXACT LIVE" not in out
    assert "sorry" not in out.lower()


def test_research_reproduce_signed_digit_short_horizon_links_lean():
    out = _run("research", "reproduce", "sdsh")
    assert "reproduce: ok" in out
    assert "hypothesis sdsh_horizon_u2_product: SUPPORTED EXACT REACHABLE" in out
    assert "hypothesis sdsh_genuine_merge: SUPPORTED EXACT REACHABLE" in out
    assert "hypothesis sdsh_short_separator: REFUTED" in out
    assert "hypothesis sdsh_only_deadlock: REFUTED" in out
    report = _run("research", "report", "signed_digit_short_horizon")
    assert "truncated_3adic_equiv" in report
    assert "sorry" not in report.lower()
    assert "admit" not in report.lower()


def test_research_analyze_multiplicative_residual_is_exact_one_not_live():
    out = _run("research", "analyze", "multiplicative_residual")
    assert "problem: multiplicative_residual" in out
    assert "attack reconnaissance: OBSERVATION BOUNDED LIVE_SLICE" in out
    assert "attack closure: SUPPORTED EXACT REACHABLE" in out
    assert "SUPPORTED EXACT LIVE" not in out
    assert "sorry" not in out.lower()


def test_research_reproduce_multiplicative_residual_links_lean():
    out = _run("research", "reproduce", "mr")
    assert "reproduce: ok" in out
    assert "hypothesis mr_product_u1_closure: SUPPORTED EXACT REACHABLE" in out
    assert "hypothesis mr_factor_count_matters: REFUTED" in out
    report = _run("research", "report", "multiplicative_residual")
    assert "product_residual_closure" in report
    assert "sorry" not in report.lower()
    assert "admit" not in report.lower()


def test_research_analyze_collatz_is_inconclusive_not_live():
    out = _run("research", "analyze", "collatz")
    assert "problem: collatz_finite_descent" in out
    assert "attack reconnaissance: OBSERVATION BOUNDED" in out
    assert "attack closure: INCONCLUSIVE BOUNDED REACHABLE" in out
    assert "hypothesis collatz_uniform_L_descent: REFUTED" in out
    assert "SUPPORTED EXACT LIVE" not in out
    assert "sorry" not in out.lower()


def test_research_reproduce_collatz_links_lean():
    out = _run("research", "reproduce", "collatz")
    assert "reproduce: ok" in out
    assert "hypothesis collatz_uniform_L_descent: REFUTED" in out
    report = _run("research", "report", "collatz")
    assert "shortcutC_no_uniform_L_descent" in report
    assert "sorry" not in report.lower()
    assert "admit" not in report.lower()


def test_research_analyze_primes_sieve_is_exact_not_live():
    out = _run("research", "analyze", "primes")
    assert "problem: prime_residual_complexity" in out
    assert "attack reconnaissance: OBSERVATION BOUNDED" in out
    assert "attack closure: SUPPORTED EXACT REACHABLE" in out
    assert "hypothesis prc_sieve_equals_prime: REFUTED" in out
    assert "hypothesis prc_jet_equals_prime: REFUTED" in out
    assert "SUPPORTED EXACT LIVE" not in out
    assert "sorry" not in out.lower()


def test_research_reproduce_primes_links_lean():
    out = _run("research", "reproduce", "primes")
    assert "reproduce: ok" in out
    assert "hypothesis prc_sieve_equals_prime: REFUTED" in out
    report = _run("research", "report", "primes")
    assert "sievePrime_I0_separator" in report
    assert "sorry" not in report.lower()
    assert "admit" not in report.lower()
