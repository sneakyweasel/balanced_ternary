"""Live Ext is the energy-slab interval in w. Not an L_0 bound.

V_n fills [lo,hi]. Width of the real w-interval is < 4 for n≤24.
u=s2+2s3 is E_1 only. Singleton (-3,) is missing on origin-reachable
and boxed K. Co-live holes were not found in the tested boxes.
"""

from __future__ import annotations

from research.ostrowski.control_language import FROZEN_EXT_TYPES
from research.ostrowski.energy_trajectory import remaining_one_form
from research.ostrowski.ext_feasibility import (
    GROWTH_NOT_INFINITUDE,
    KNOWN_PACKAGING,
    NORMALIZED_NOT_COORDINATE,
    ORIGIN,
    U_IS_E1,
    boxed_colive_search,
    formula_matches_oracle,
    frozen_window_description,
    live_ext,
    live_ext_by_oracle,
    origin_window_geometry,
    valuation_is_interval,
    valuations_fill_through,
    width_table,
)
from research.ostrowski.exceptional_kernel import W_LSD


def test_valuations_fill_lo_hi():
    report = valuations_fill_through(12)
    assert report["all_intervals"]
    assert report["first_hole_n"] is None
    row1 = valuation_is_interval(1)
    assert row1["lo"] == -2 and row1["hi"] == 1
    assert row1["is_interval"]


def test_live_ext_matches_terminal_oracle():
    samples = (
        (ORIGIN, 5),
        ((-3, -1, 0), 4),
        ((6, 5, 1), 3),
        ((-3, -37, 19), 1),
        ((2, -7, 3), 8),
    )
    for state, remaining in samples:
        assert formula_matches_oracle(state, remaining)
        ext = live_ext(state, remaining)
        assert ext == live_ext_by_oracle(state, remaining)
        if remaining == 1:
            u = remaining_one_form(state)
            if u in W_LSD:
                assert ext == (u,)
            else:
                assert ext == ()


def test_real_width_lt_4_through_24():
    report = width_table(24)
    assert report["all_width_lt_4"]
    assert report["first_width_ge_4"] is None
    assert report["max_width"] < 4
    assert abs(report["rows"][1]["width"] - 1.5) < 1e-12
    assert report["rows"][2]["width"] == 3.0
    assert report[NORMALIZED_NOT_COORDINATE]


def test_frozen_windows_are_consecutive_le4_minus_m3():
    desc = frozen_window_description()
    assert desc["count_including_m3"] == 23
    assert desc["count_without_m3"] == 22
    assert desc["matches_frozen"]
    assert not desc["singleton_m3_in_frozen"]
    assert FROZEN_EXT_TYPES[0] == ()
    assert (-3,) not in FROZEN_EXT_TYPES


def test_origin_geometry_no_m3_u_grows():
    geom = origin_window_geometry(12)
    assert geom["matches_frozen"]
    assert geom["origin_has_singleton_m3"] is False
    assert geom["formula_matches_on_dag"]
    assert geom["live_ne_colive_on_dag"] == 0
    assert geom["u_grows_on_some_window"]
    assert geom["s3_grows_on_some_window"]
    assert geom[U_IS_E1]
    assert geom[NORMALIZED_NOT_COORDINATE]
    assert geom[GROWTH_NOT_INFINITUDE]
    assert geom[KNOWN_PACKAGING]
    empty = geom["windows"][()]
    assert empty["min_s3"] == empty["max_s3"] == 0
    assert max(abs(empty["min_u"]), abs(empty["max_u"])) > 2


def test_boxed_colive_no_holes_no_m3():
    report = boxed_colive_search(4, 6)
    assert report["checked_in_K"] > 0
    assert report["colive_hole_count"] == 0
    assert report["live_ext_singleton_m3_count"] == 0
    assert report["max_live_ext_len"] <= 4
    assert report["live_ne_colive_count"] == 0
