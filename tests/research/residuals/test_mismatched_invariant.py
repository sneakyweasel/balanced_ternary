"""Invariant decision for Q_{t,K,W}."""

from __future__ import annotations

import io
from contextlib import redirect_stdout

from balanced_ternary.cli import main
from research.residuals.mismatched_cubic import q_eq, q_mod, q_params
from research.residuals.mismatched_invariant import (
    B_t,
    information_exponents,
    invariant_compare,
    invariant_report,
    one_family,
    one_family_obstruction,
    psi4,
    q_expansion,
    score_candidate,
    split_two_scale,
)
from visualization.residual_explorer import quotient_compare_view, quotient_invariant_view


def test_two_scale_matches_q():
    t, K = 2, 7
    for u in range(-40, 41):
        a, b = split_two_scale(t, u)
        assert u == a + 3**t * b
        assert q_expansion(t, a, b) % (3**K) == q_mod(t, K, u)


def test_psi1_at_width_t_merges():
    t, K, W = q_params(6, 1)
    row = score_candidate("psi1", t, K, W, t)
    assert row["false_merges"] >= 1
    assert row["exact"] is False


def test_psi4_same_as_one_family_obstruction():
    t, K, W = q_params(6, 1)
    obst = one_family_obstruction(t, K, W)
    assert obst["shared_residue_mod_3^t"] is True
    assert obst["shared_B_t"] is True
    assert obst["q_classes"] == obst["family_size"]
    assert obst["q_classes"] >= 3
    fam = one_family(t, W)
    assert 1 in fam and 1 + 3**t in fam
    assert not q_eq(t, K, 1, 1 + 3**t)
    assert psi4(1, t, t, t) == psi4(1 + 3**t, t, t, t)


def test_full_width_psi1_does_not_merge():
    t, K, W = q_params(6, 1)
    row = score_candidate("psi1", t, K, W, W)
    assert row["false_merges"] == 0
    # Full-width residue refines Q, so nontrivial fibres become false splits.
    assert row["false_splits"] >= 1


def test_information_exponents_need_high_b():
    t, K, W = q_params(8, 1)
    alpha, beta = information_exponents(t, K)
    assert alpha == t
    assert beta >= K - 1
    assert beta > W - t


def test_high_valuation_zero_and_report():
    rec = invariant_report(1, 6, 3)
    assert rec["q_classes"] == 23
    assert rec["one_family"]["lower_bound_trits"] >= 1
    names = [row["candidate"] for row in rec["candidates"]]
    assert "psi4" in names
    weak = next(row for row in rec["candidates"] if row["candidate"] == "psi4")
    assert weak["false_merges"] >= 1


def test_compare_one_family():
    rec = invariant_compare(1, 6, 3, 1, 4)
    assert rec["same_Q"] is False
    assert rec["psi"]["psi4"]["same"] is True
    assert any("merges" in line or "carry" in line for line in rec["missing"])


def test_B_t_from_low_residue():
    t = 3
    s = t - 1
    for u in range(-20, 21):
        v = u + 3**s
        assert B_t(t, u) == B_t(t, v)


def test_cli_invariant_and_compare():
    def _run(*args: str) -> str:
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = main(["calculus", *args])
        assert code == 0
        return buf.getvalue()

    out = _run("cubic-quotient-invariant", "--t", "1", "--modulus", "6", "--width", "3")
    assert "exact Q-image size" in out
    assert "false_merges" in out
    cmp_ = _run(
        "cubic-quotient-compare",
        "1",
        "4",
        "--t",
        "1",
        "--modulus",
        "6",
        "--width",
        "3",
    )
    assert "same Q = False" in cmp_
    assert "same psi4 = True" in cmp_


def test_explorer_q_card():
    # (k,r)=(6,1) exhausted; p=3 is on the locus, u=1
    card = quotient_invariant_view(3, 6, 1)
    assert card.on_locus
    assert card.u == 1
    assert card.t == 1
    off = quotient_invariant_view(1, 6, 1)
    assert off.on_locus is False
    view = quotient_compare_view(1, 4, 1, 6, 3)
    assert view.same_Q is False
    assert view.same_psi4 is True
