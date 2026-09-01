"""Fast checks for the record-jump quantization probe."""

from __future__ import annotations

import json
import math

from research.juggler_sequence.flight_divergent_structure import trajectory
from research.juggler_sequence.flight_return_quantization import (
    CLASS_CONFIRMED,
    JSON_PATH,
    LOG2_3,
    delta_prime,
    lean_wired,
    return_set,
    segment_mirror,
    theta_p,
)

TEST_WINDOW = 200


def test_theta_is_hug_walk_height() -> None:
    # theta_19 = 12 log2(3) - 19, and 19 is the shortest near-return.
    assert abs(theta_p(19) - (12 * LOG2_3 - 19)) < 1e-12
    assert 0.0195 < theta_p(19) < 0.0196
    for p in range(1, 19):
        assert theta_p(p) > 0.05


def test_return_set_small() -> None:
    rs = return_set(250, 0.05)
    assert rs == [19, 38, 84, 103, 122, 168, 187, 206]
    gaps = sorted({b - a for a, b in zip(rs, rs[1:])})
    assert len(gaps) <= 3


def test_theta_exact_at_nineteen() -> None:
    # Exact big-int confirmation: 3^12 >= 2^19 and 3^11 < 2^19.
    assert 3**12 >= 2**19
    assert 3**11 < 2**19


def test_rigidity_nonvacuous_at_frontier() -> None:
    dp = delta_prime(19, 350_000_000)
    assert dp < 1e-8
    assert delta_prime(10**6, 350_000_000) / LOG2_3 < 1e-3
    assert math.isinf(delta_prime(10**10, 350_000_000))


def test_segment_mirror_on_window() -> None:
    for n in range(2, TEST_WINDOW + 1):
        row = segment_mirror(trajectory(n))
        assert row["upper_violations"] == 0
        assert row["lower_violations"] == 0


def test_lean_wiring() -> None:
    assert all(lean_wired().values())


def test_artifact_certifies_quantization() -> None:
    summary = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    assert summary["classification"] == CLASS_CONFIRMED
    assert summary["shortest_near_return"] == 19
    mirror = summary["window_mirror"]
    assert mirror["upper_violations"] == 0
    assert mirror["lower_violations"] == 0
    assert mirror["quantization_misses"] == 0
    # Realized near-returns only at quantized times.
    assert set(map(int, mirror["near_return_lengths"])) <= {19, 38}
    for row in summary["return_sets"]:
        assert row["three_gap_ok"] is True
    anti = summary["anti_overclaim"]
    assert anti["halt_theorem"] is False
    assert anti["divergence_excluded"] is False
    assert anti["dk_layer_extended"] is False
