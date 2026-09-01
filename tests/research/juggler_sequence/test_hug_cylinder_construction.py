"""Fast checks for the hug backward freedom-flow census."""

from __future__ import annotations

import math

from research.juggler_sequence.hug_cylinder_construction import (
    CLASS_FLOW_ANOMALY,
    CLASS_FLOW_CONFIRMED,
    classify,
    oe_pullback,
    ooe_census,
    parity_run_census,
)


def _floor_power(x: int) -> int:
    return math.isqrt(x * x * x) if x % 2 == 1 else math.isqrt(x)


def test_oe_pullback_matches_brute() -> None:
    for z in (101, 1000, 4097, 65539):
        row = oe_pullback(z)
        brute = 0
        # generous brute window around z^{4/3}
        lo = round(z ** (4 / 3)) - 8
        hi = round((z + 1) ** (4 / 3)) + 8
        for x in range(lo | 1, hi, 2):
            x1 = math.isqrt(x**3)
            if x1 % 2 == 0 and math.isqrt(x1) == z:
                brute += 1
        assert row["survivors"] == brute
        # a survivor of the OE pullback realizes O then E onto z
        if brute:
            found = next(
                x
                for x in range(lo | 1, hi, 2)
                if math.isqrt(x**3) % 2 == 0
                and math.isqrt(math.isqrt(x**3)) == z
            )
            assert _floor_power(found) % 2 == 0
            assert _floor_power(_floor_power(found)) == z


def test_ooe_first_hit_realizes_block() -> None:
    rows = ooe_census(scales=(2**16,), anchor_run=400)
    hit_rows = [r for r in rows if r["first_hit"] is not None]
    assert hit_rows, "no OOE pullback found at the test scale"
    for row in hit_rows:
        w = row["first_hit"]["anchor"]
        x = row["first_hit"]["x"]
        assert x % 2 == 1
        x1 = _floor_power(x)
        assert x1 % 2 == 1
        x2 = _floor_power(x1)
        assert x2 % 2 == 0
        assert _floor_power(x2) == w


def test_parity_run_census_fields() -> None:
    rows = parity_run_census(scales=(2**16,), window=2_000)
    assert len(rows) == 1
    row = rows[0]
    assert row["max_parity_run"] >= 1
    assert row["work_window_x13"] > row["naive_budget_x14"]


def _window_parities(x0: int, count: int) -> set[int]:
    x = x0 if x0 % 2 == 1 else x0 + 1
    parities: set[int] = set()
    for _ in range(count):
        parities.add(math.isqrt(x * x * x) % 2)
        x += 2
    return parities


def test_depth1_window_both_parities() -> None:
    """Working windows at modest X hit both parities of floor(x^{3/2})."""
    for scale in (2**12, 2**14, 2**16):
        h = max(1, int((2.0 / 3.0) * scale ** (1.0 / 3.0)))
        starts = [scale + 1 if scale % 2 == 0 else scale]
        near_sq = int(scale**0.5) ** 2
        if near_sq % 2 == 0:
            near_sq += 1
        if scale <= near_sq <= 2 * scale:
            starts.append(near_sq)
        starts.append(scale + 2 * (h // 3) + 1)
        for x0 in starts:
            parities = _window_parities(x0, h)
            assert parities == {0, 1}, (scale, x0, h, parities)


def test_classify_gates() -> None:
    runs_ok = [{"run_over_work_window": 0.5}]
    oe_ok = [{"zero_survivor_anchors": 0, "anchors": 24}]
    ooe_ok = [
        {"offset": "generic", "anchors_with_pullback": 10, "hit_over_predicted": 0.8},
        # a dead resonant row must not trip the gate
        {"offset": "resonant", "anchors_with_pullback": 0, "hit_over_predicted": 0.0},
    ]
    assert classify(runs_ok, oe_ok, ooe_ok) == CLASS_FLOW_CONFIRMED
    runs_bad = [{"run_over_work_window": 1.4}]
    assert classify(runs_bad, oe_ok, ooe_ok) == CLASS_FLOW_ANOMALY
    ooe_bad = [
        {"offset": "generic", "anchors_with_pullback": 0, "hit_over_predicted": 0.0}
    ]
    assert classify(runs_ok, oe_ok, ooe_bad) == CLASS_FLOW_ANOMALY
