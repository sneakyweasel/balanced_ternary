"""Feature transitions ``n -> 3n+1 -> T(n)``.

Primary dataset row schema (exact column names):

    n
    balanced_ternary_n
    three_n_plus_one
    balanced_ternary_three_n_plus_one
    v2_three_n_plus_one
    T_n
    balanced_ternary_T_n

then, for each stage prefix in ``(n, three_n_plus_one, T_n)`` and each
name in ``FEATURE_NAMES``:

    {prefix}_{name}

then deltas of numeric features, always ``F(T(n)) - F(n)``:

    delta_length
    delta_weight
    delta_weight_parity
    delta_signed_digit_sum
    delta_positive_digit_count
    delta_negative_digit_count
    delta_zero_count
    delta_number_of_runs
    delta_max_run_length
    delta_zero_run   (alias of max-zero-run delta; stored as delta_max_zero_run)

Deltas are empirical differences along one accelerated step. They are not
Lyapunov decreases.

Claim classification for the weight-parity bridge (see
``collatz.research.invariants`` and ``docs/collatz_mathematics.md``):

    odd n  =>  weight(BT(n)) odd          PROVED
    3n+1 even => weight(BT(3n+1)) even    PROVED (same identity)
"""

from __future__ import annotations

from dataclasses import dataclass

from balanced_ternary.representation import encode
from collatz.bt_arithmetic import lsd_add_one_case, three_n_plus_one_word
from collatz.core import collatz_step, collatz_valuation, require_positive_odd, three_n_plus_one
from collatz.features import (
    FEATURE_NAMES,
    NUMERIC_FEATURE_NAMES,
    BalancedTernaryFeatures,
    extract_features,
)
from collatz.theorems import append_plus, predicted_features_after_append_plus

STAGE_PREFIXES: tuple[str, ...] = ("n", "three_n_plus_one", "T_n")

CORE_COLUMNS: tuple[str, ...] = (
    "n",
    "balanced_ternary_n",
    "three_n_plus_one",
    "balanced_ternary_three_n_plus_one",
    "v2_three_n_plus_one",
    "T_n",
    "balanced_ternary_T_n",
    "lsd_add_one_case",
    "ternary_shift_add_one_matches",
    "append_plus_matches",
    "append_plus_features_match",
)

DELTA_COLUMNS: tuple[str, ...] = tuple(
    f"delta_{name}" for name in NUMERIC_FEATURE_NAMES
)

FEATURE_COLUMNS: tuple[str, ...] = tuple(
    f"{prefix}_{name}"
    for prefix in STAGE_PREFIXES
    for name in FEATURE_NAMES
)

ROW_COLUMNS: tuple[str, ...] = CORE_COLUMNS + FEATURE_COLUMNS + DELTA_COLUMNS


@dataclass(frozen=True)
class CollatzFeatureTransition:
    n: int
    balanced_ternary_n: str
    three_n_plus_one: int
    balanced_ternary_three_n_plus_one: str
    v2_three_n_plus_one: int
    T_n: int
    balanced_ternary_T_n: str
    lsd_add_one_case: str
    ternary_shift_add_one_matches: bool
    append_plus_matches: bool
    append_plus_features_match: bool
    features_n: BalancedTernaryFeatures
    features_three_n_plus_one: BalancedTernaryFeatures
    features_T_n: BalancedTernaryFeatures
    predicted_features_three_n_plus_one: BalancedTernaryFeatures
    deltas: dict[str, int]

    def to_row(self) -> dict[str, object]:
        row: dict[str, object] = {
            "n": self.n,
            "balanced_ternary_n": self.balanced_ternary_n,
            "three_n_plus_one": self.three_n_plus_one,
            "balanced_ternary_three_n_plus_one": self.balanced_ternary_three_n_plus_one,
            "v2_three_n_plus_one": self.v2_three_n_plus_one,
            "T_n": self.T_n,
            "balanced_ternary_T_n": self.balanced_ternary_T_n,
            "lsd_add_one_case": self.lsd_add_one_case,
            "ternary_shift_add_one_matches": self.ternary_shift_add_one_matches,
            "append_plus_matches": self.append_plus_matches,
            "append_plus_features_match": self.append_plus_features_match,
        }
        row.update(self.features_n.prefixed_dict("n"))
        row.update(self.features_three_n_plus_one.prefixed_dict("three_n_plus_one"))
        row.update(self.features_T_n.prefixed_dict("T_n"))
        row.update(self.deltas)
        return row


def _numeric_deltas(
    src: BalancedTernaryFeatures, dst: BalancedTernaryFeatures
) -> dict[str, int]:
    src_d = src.as_dict()
    dst_d = dst.as_dict()
    return {
        f"delta_{name}": int(dst_d[name]) - int(src_d[name])
        for name in NUMERIC_FEATURE_NAMES
    }


def feature_transition(n: int) -> CollatzFeatureTransition:
    """Exact feature record of one accelerated step starting at odd ``n``."""
    n = require_positive_odd(n)
    word_n = encode(n)
    y = three_n_plus_one(n)
    word_y = encode(y)
    k = collatz_valuation(n)
    t = collatz_step(n)
    word_t = encode(t)
    via_ternary = three_n_plus_one_word(word_n)
    via_append = append_plus(word_n)
    feat_n = extract_features(word_n)
    feat_y = extract_features(word_y)
    feat_t = extract_features(word_t)
    predicted_y = predicted_features_after_append_plus(word_n)
    return CollatzFeatureTransition(
        n=n,
        balanced_ternary_n=word_n.word(),
        three_n_plus_one=y,
        balanced_ternary_three_n_plus_one=word_y.word(),
        v2_three_n_plus_one=k,
        T_n=t,
        balanced_ternary_T_n=word_t.word(),
        lsd_add_one_case=lsd_add_one_case(word_n),
        ternary_shift_add_one_matches=(via_ternary == word_y),
        append_plus_matches=(via_append == word_y),
        append_plus_features_match=(predicted_y == feat_y),
        features_n=feat_n,
        features_three_n_plus_one=feat_y,
        features_T_n=feat_t,
        predicted_features_three_n_plus_one=predicted_y,
        deltas=_numeric_deltas(feat_n, feat_t),
    )
