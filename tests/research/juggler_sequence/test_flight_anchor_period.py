"""Fast tests for the flight anchor-period branch."""

from __future__ import annotations

import json
import math

from research.juggler_sequence.cycle_finance import o_min_and_theta
from research.juggler_sequence.cycle_walk_competition import (
    dk_price,
    o_min_exact,
)
from research.juggler_sequence.flight_anchor_period import (
    ANCHOR,
    BLOCKER,
    CLASS_GREEN,
    JSON_PATH,
    NEXT_FAN,
    scan_range,
    theta_float_lower,
)

LN2 = math.log(2.0)


def test_o_min_exact_matches_incremental() -> None:
    for length in range(1, 300):
        odd, _theta = o_min_and_theta(length)
        assert o_min_exact(length) == odd


def test_theta_float_lower_is_conservative() -> None:
    for length in (19, 84, 1054, 25781):
        odd, theta = o_min_and_theta(length)
        delta = odd * math.log2(3.0) - length
        assert theta_float_lower(delta) <= theta


def test_narrow_scan_finds_leftover() -> None:
    # window around the parity survivor 504026 = 478245 + 25781
    scan = scan_range(504_000, 504_052, ANCHOR)
    lengths = [row["length"] for row in scan["parity_survivors"]]
    assert lengths == [504_026]
    assert (
        scan["float_killed"]
        + scan["exact_killed"]
        + len(scan["parity_survivors"])
        == scan["n_lengths"]
    )


def test_artifact_certifies_instance() -> None:
    summary = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    assert summary["classification"] == CLASS_GREEN
    assert summary["deep_sandwich_certified"] is True
    assert summary["first_survivor"] == NEXT_FAN
    scan = summary["scan"]
    assert scan["range"] == [BLOCKER, NEXT_FAN]
    assert scan["anchor"] == ANCHOR
    assert (
        scan["float_killed"]
        + scan["exact_killed"]
        + len(scan["parity_survivors"])
        == scan["n_lengths"]
    )
    rows = summary["dk_rows"]
    blocker = next(r for r in rows if r["length"] == BLOCKER)
    assert blocker["dk_kills"] is True
    assert 1.0 < blocker["dk_margin"] < 1.1  # just above break-even 3.48e8
    for row in rows:
        assert row["dk_kills"] is (row["length"] < NEXT_FAN)
    assert summary["monotonicity"]["all_increased"] is True
    anti = summary["anti_overclaim"]
    assert anti["halt_theorem"] is False
    assert anti["new_unconditional_period_bound"] is False
    assert anti["floor_raise"] is False
    assert anti["descent_verification_run"] is False


def test_dk_pricing_reproduces_artifact() -> None:
    # float-only re-pricing from the stored exact theta and digit sums
    summary = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    for row in summary["dk_rows"]:
        price = dk_price(
            row["length"],
            row["odd_count"],
            row["digit_sum"],
            row["theta"],
            float(ANCHOR),
        )
        assert abs(price["margin"] - row["dk_margin"]) < 1e-12 * max(
            1.0, row["dk_margin"]
        )
