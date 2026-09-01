"""Printed Lemma 3.7 / Lemma 5.2 hypotheses, not the sums."""

from __future__ import annotations

from research.juggler_sequence.kernel_p0_hypotheses import (
    ANTI,
    branch_run_count,
    first_integer_p0,
    first_paper_p0,
    freeze_window_count,
    integer_range_holds,
    paper_3a_majorant_holds,
    paper_slack_holds,
    stage3_s2_holds,
    th3_holds,
)


def test_anti_overclaim():
    assert ANTI["sums_evaluated"] is False
    assert ANTI["paper_b_modified"] is False
    assert ANTI["k3_reopened"] is False
    assert ANTI["step5b_computed"] is False
    assert ANTI["items_124_implemented"] is False


def test_stage3_s2_threshold():
    assert stage3_s2_holds(10**4) is False
    assert stage3_s2_holds(19**4) is True
    p0 = first_paper_p0()["parts"]["lemma52_s2"]
    assert p0 is not None
    assert 10**4 < p0 <= 19**4


def test_paper_3a_majorant():
    low = paper_3a_majorant_holds(10**5)
    mid = paper_3a_majorant_holds(300_000)
    high = paper_3a_majorant_holds(400_000)
    assert low["holds"] is False
    assert low["displayed_holds"] is False
    assert mid["displayed_holds"] is True
    assert high["holds"] is True
    assert high["displayed_holds"] is True
    p0 = first_paper_p0()["parts"]["lemma37_3a"]
    assert p0 is not None
    assert 10**5 < p0 < 400_000


def test_th3_small_and_corner():
    assert th3_holds(200, 1.0)["holds"] is True
    slack = paper_slack_holds(10**6)
    assert slack["lemma52_th3"]["holds"] is True
    assert slack["lemma52_th3_t1"]["holds"] is True
    integ = integer_range_holds(10**6)
    assert integ["lemma52_th3"]["holds"] is True
    assert integ["holds"] is True


def test_joint_paper_p0_is_the_3a_majorant():
    row = first_paper_p0()
    assert row["joint"] == row["parts"]["lemma37_3a"]
    assert row["joint"] is not None
    assert paper_slack_holds(row["joint"])["holds"] is True
    assert paper_slack_holds(row["joint"] - 1)["holds"] is False


def test_integer_p0_is_stage3_s2():
    row = first_integer_p0()
    assert row["joint"] == row["parts"]["lemma52_s2"]
    assert integer_range_holds(row["joint"])["holds"] is True


def test_inventories_short_prefix():
    fr = freeze_window_count(10**6, k=1, h1=1, h2=1, limit=4000)
    assert fr["steps"] == 4000
    assert fr["holds"] is True
    assert fr["lemma37_holds"] is True
    br = branch_run_count(10**6, h1=1, h2=1, limit=4000)
    assert br["steps"] == 4000
    assert br["holds"] is True
    assert br["Gprime_lt_1"] is True
    assert br["C2_j_le_3"] is True
