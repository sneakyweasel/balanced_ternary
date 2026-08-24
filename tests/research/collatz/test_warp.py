"""Domain-aware W/T warp identities, counterexamples, and censuses."""

from __future__ import annotations

import pytest

from bt.sequences import bt_digit_sum, bt_is_palindrome, bt_reverse
from bt.representation import encode
from research.collatz.core import collatz_step
from research.collatz.experiments.bt_warp import (
    run_bt_warp_census,
    run_bt_warp_realizer,
    semigroup_agreement_sample,
)
from research.experiments.schema import (
    BT_WARP_SCHEMA_VERSION,
    validate_bt_warp_row,
)
from research.collatz.theorems import append_plus
from research.collatz.warp import (
    apply_word,
    commutator_census,
    is_positive_odd,
    palindrome_along_trajectory,
    preserved_counterexamples,
    realizer_warp_row,
    smallest_disagreement,
    special_class_report,
    warp_state,
    warped_trajectory,
)


def test_warp_state_one_is_fixed():
    state = warp_state(1)
    assert state.W_n == 1
    assert state.T_n == 1
    assert state.T_W == 1
    assert state.Comm_WT == 0
    assert state.delta_s == bt_digit_sum(1) - bt_digit_sum(1) - 1
    assert state.palindrome_n


def test_t_undefined_off_positive_odd():
    even = warp_state(2)
    assert even.T_n is None
    assert even.Comm_WT is None
    assert not even.t_defined
    negative = warp_state(-5)
    assert negative.T_n is None
    assert negative.W_n == -bt_reverse(5)


def test_published_reverse_then_collatz_domain():
    state = warp_state(21)
    assert state.W_n == 7
    assert state.t_of_W_defined
    assert state.T_W == collatz_step(7)
    assert state.T_n == collatz_step(21)
    assert state.Comm_WT == bt_reverse(state.T_n) - state.T_W


def test_delta_s_is_odd_part_only():
    for n in range(1, 401, 2):
        state = warp_state(n)
        y = 3 * n + 1
        assert bt_digit_sum(y) == bt_digit_sum(n) + 1
        assert state.delta_s == bt_digit_sum(state.T_n) - bt_digit_sum(y)
        assert state.L3_T - len(append_plus(encode(n))) == state.delta_L - 1


def test_preserved_naive_counterexamples():
    examples = preserved_counterexamples()
    assert examples["W_W_equals_id"]["counterexample"] == 3
    assert bt_reverse(bt_reverse(3)) != 3
    assert examples["W_3n_equals_3_W_n"]["counterexample"] == 1
    assert bt_reverse(3) != 3 * bt_reverse(1)
    commute = smallest_disagreement(("W", "T"), ("T", "W"), 5_000)
    assert commute is not None
    assert commute == examples["W_T_equals_T_W"]["counterexample"]
    left = apply_word(("W", "T"), commute)
    right = apply_word(("T", "W"), commute)
    assert left is not None and right is not None and left != right


def test_wt_is_involution_on_odds():
    assert smallest_disagreement(("Wt", "Wt"), (), 2_000) is None


def test_commutator_census_small():
    census = commutator_census(200)
    assert census["odd_count"] == 100
    assert census["commutator_defined"] >= 1
    assert census["smallest_zero"] == 1
    assert 0 <= census["commutator_zero"] <= census["commutator_defined"]
    assert census["delta_L_min"] is not None
    assert census["delta_L_max"] is not None


def test_special_classes_preserve_nonzero_or_empty_domain():
    report = special_class_report(500)
    assert report["palindrome"]["smallest_member"] == 1
    assert report["trailing_zero"]["smallest_member"] % 3 == 0
    # Palindromes have W(n)=n, so Comm is defined whenever n is positive odd,
    # and equals 0 iff W(T(n))=T(n). That is not automatic.
    assert report["palindrome"]["commutator_defined"] >= 1


def test_warped_trajectory_starts_with_reverse():
    traj = warped_trajectory(21, 8)
    assert traj.values[0] == 21
    assert traj.values[1] == 7
    assert traj.t_started
    blocked = warped_trajectory(5, 8)
    assert blocked.values == (5, bt_reverse(5))
    assert not blocked.t_started


def test_palindrome_along_one():
    rows = palindrome_along_trajectory(1, 4)
    assert rows[0]["n"] == 1
    assert rows[0]["palindrome"]


def test_realizer_warp_preserves_counterexamples():
    row = realizer_warp_row((1,))
    validate_bt_warp_row(row, cylinder=True)
    assert row["R"] == row["n"]
    result = run_bt_warp_realizer(3, 3)
    assert result.report["smallest_reverse_counterexample"] is not None
    assert result.report["smallest_tail_counterexample"] is not None
    assert not result.report["smallest_reverse_counterexample"]["W_R_equals_R_reverse"]
    assert not result.report["smallest_tail_counterexample"]["W_R_equals_R_tail"]


def test_bt_warp_census_schema(tmp_path):
    result = run_bt_warp_census(50, identity_length=3, output_dir=tmp_path)
    assert result.schema_version == BT_WARP_SCHEMA_VERSION
    assert len(result.rows) == 25
    for row in result.rows:
        validate_bt_warp_row(row)
    assert result.paths["jsonl"]
    ww = next(
        record
        for record in result.identities["naive_identities"]
        if record["name"].startswith("W W")
    )
    assert ww["smallest_counterexample"] == 3


def test_semigroup_sample_records_involution_split():
    sample = semigroup_agreement_sample(3, 40)
    assert sample["word_count"] == 1 + 3 + 9 + 27
    assert sample["W_W_counterexample"] == 3
    assert sample["Wt_Wt_counterexample"] is None


def test_lsd_msd_swap_does_not_predict_valuation():
    """W exchanges LSD and MSD; k remains a 2-adic quantity."""
    from research.collatz.core import collatz_valuation

    pairs = []
    for n in range(1, 400, 2):
        w = bt_reverse(n)
        if not is_positive_odd(w):
            continue
        pairs.append((collatz_valuation(n), collatz_valuation(w)))
    assert pairs
    assert len({k for k, _ in pairs}) > 1
    assert any(k != kw for k, kw in pairs)


@pytest.mark.slow
def test_exhaustive_odd_warp_identities_to_one_million():
    """Exact local identities on every positive odd n <= 10^6.

    Commutation of W and T is not among those identities.
    """
    first_nonzero = None
    defined = 0
    zero = 0
    for n in range(1, 1_000_001, 2):
        state = warp_state(n)
        y = 3 * n + 1
        assert state.delta_s == bt_digit_sum(state.T_n) - bt_digit_sum(y)
        assert (bt_reverse(bt_reverse(n)) == n) == (n % 3 != 0)
        if bt_is_palindrome(n):
            assert state.W_n == n
        if n % 3 == 1:
            assert state.W_n > 0
            assert state.t_of_W_defined
        elif n % 3 == 2:
            assert state.W_n < 0
            assert not state.t_of_W_defined
        if state.t_of_W_defined:
            defined += 1
            assert state.Comm_WT == state.W_T - state.T_W
            if state.Comm_WT == 0:
                zero += 1
                assert state.palindrome_n
            elif first_nonzero is None:
                first_nonzero = n
            defined += 1
            assert state.Comm_WT == state.W_T - state.T_W
            if state.Comm_WT == 0:
                zero += 1
            elif first_nonzero is None:
                first_nonzero = n
    assert defined > 0
    assert zero >= 1
    assert first_nonzero is not None
