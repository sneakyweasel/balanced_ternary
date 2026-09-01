"""Fast checks for depth-2 cylinder geometry. Not a C_L theorem."""

from __future__ import annotations

from research.juggler_sequence.hug_flow_depth_two import (
    CLASS_IMAGE_FRAGMENTED,
    CLASS_INTERVAL_SURVIVES,
    _sqrt,
    classify,
    consecutive_image_gap,
    geometry_census,
    image_gap_lower_bound,
    scan_window,
    second_stage_window,
    work_window,
)


def test_image_gap_at_least_three_sqrt() -> None:
    for x in range(3, 5001, 2):
        assert consecutive_image_gap(x) >= image_gap_lower_bound(x)


def test_image_gap_exceeds_second_stage_window() -> None:
    for x in (15, 101, 1001, 4095, 65535):
        gap = consecutive_image_gap(x)
        y = _sqrt(x * x * x)
        assert gap > second_stage_window(y)


def test_scan_window_flags_fragmentation() -> None:
    scale = 2**12
    h = work_window(scale)
    row = scan_window(scale + 1, h)
    assert row["count"] == h
    assert row["n_even_y"] + row["n_odd_y"] == h
    assert row["gap_ge_3sqrt"]
    assert row["min_gap_gt_y_window"]
    assert row["min_gap_over_y_window"] > 1.0


def test_geometry_census_classifies_fragmented() -> None:
    rows = geometry_census(scales=(2**12, 2**16))
    assert classify(rows) == CLASS_IMAGE_FRAGMENTED
    assert classify(rows) != CLASS_INTERVAL_SURVIVES
    for row in rows:
        assert row["gap_over_y_window_pred"] == 4.5
        for window in row["windows"]:
            assert window["gap_ge_3sqrt"]
            assert window["min_gap_gt_y_window"]
