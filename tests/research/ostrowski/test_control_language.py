"""Co-live control language: prefixes, Ext types, factors, occurring blocks.

Finite-horizon co-liveness is not ``|H(u)|=∞``. Expanding ``A^k`` is not
a live family. ``K_n`` is normalized, not coordinate-bounded.
"""

from __future__ import annotations

from research.ostrowski.control_language import (
    DAG_NOT_SCC,
    EXPANDING_NOT_OCCURRING,
    FROZEN_EXT_TYPES,
    GROWTH_NOT_INFINITUDE,
    HORIZON_NOT_INFINITY,
    HORIZON_SPECIFIC_LEN6,
    LIVE_NOT_COLIVE,
    N8_L_K,
    N12_L_K,
    NORMALIZED_NOT_COORDINATE,
    ORIGIN,
    W_INTERIOR,
    W_LSD,
    affine_holds,
    alphabet_at_remaining,
    compare_horizons,
    dag_at,
    ext_is_consecutive_interval,
    forbidden_factors,
    language_report,
    occurring_block_search,
    spectral_colive,
)
from research.ostrowski.energy_trajectory import apply_word
from research.ostrowski.live_layers import linf
from research.ostrowski.system import nonpisot_order3
from research.ostrowski.terminal_set import is_terminal


def test_lsd_alphabet_only_at_remaining_one():
    assert alphabet_at_remaining(1) == W_LSD
    assert alphabet_at_remaining(2) == W_INTERIOR
    assert alphabet_at_remaining(8) == W_INTERIOR
    assert alphabet_at_remaining(0) == ()


def test_n8_live_equals_colive_and_frozen_L_k():
    report = language_report(8)
    assert report["L_k"] == N8_L_K
    assert report["live_nodes"] == report["colive_nodes"]
    assert report["live_ne_colive_remainings"] == []
    assert report[LIVE_NOT_COLIVE] is False
    assert report["ext"]["dead_ends_on_colive_positive"] == 0
    assert report["ext"]["max_branching"] == 4
    assert report["lsd_only_at_remaining_1"]
    assert report[DAG_NOT_SCC]
    assert report[GROWTH_NOT_INFINITUDE]
    assert report[HORIZON_NOT_INFINITY]
    assert report[NORMALIZED_NOT_COORDINATE]


def test_n12_language_and_ext_intervals():
    report = language_report(12)
    assert report["L_k"] == N12_L_K
    assert report["ext"]["distinct_ext"] == 22
    assert tuple(report["ext"]["ext_types"]) == FROZEN_EXT_TYPES
    assert report["ext"]["all_consecutive_intervals"]
    assert report["ext"]["matches_frozen"]
    assert all(ext_is_consecutive_interval(t) for t in FROZEN_EXT_TYPES)
    assert (-3,) not in FROZEN_EXT_TYPES
    assert report[LIVE_NOT_COLIVE] is False


def test_all_interior_length_2_and_3_factors_occur():
    report = forbidden_factors((12,), (2, 3))
    assert report["all_short_factors_occur"]
    assert report["forbidden_counts"] == {2: 0, 3: 0}
    assert report["occurring_counts"][12] == {2: 49, 3: 343}
    assert report[HORIZON_NOT_INFINITY]


def test_horizon_specific_is_not_infinitude():
    cmp16 = compare_horizons(16, 20, max_k=6)
    assert cmp16["large_only"] == 0
    assert cmp16["both_horizons"] == 600
    assert cmp16["ext_types_stable"]
    assert cmp16[HORIZON_NOT_INFINITY]
    dag12 = dag_at(12)
    dag20 = dag_at(20)
    for word in HORIZON_SPECIFIC_LEN6:
        assert dag20.is_colive_prefix(word)
        assert not dag12.is_colive_prefix(word)


def test_occurring_blocks_return_or_leave_k():
    dag = dag_at(20)
    report = occurring_block_search(dag, (4, 5, 6), 3, 18)
    assert report["tested"] == 564
    assert (0, 0, 0, 0) in report["live_hit_blocks"]
    assert report["expanding_live"] == []
    assert report["has_unbounded_live_family"] is False
    assert report[EXPANDING_NOT_OCCURRING]
    assert report[GROWTH_NOT_INFINITUDE]
    sys = nonpisot_order3()
    for block in report["live_hit_blocks"]:
        state = ORIGIN
        remaining = 18
        for _ in range(3):
            state = apply_word(sys, state, block)
            remaining -= len(block)
            assert is_terminal(sys, state, remaining)
        assert state == ORIGIN
        assert linf(state) == 0
    dead = report["expanding_not_colive_sample"]
    assert dead
    witness = dead[0]["block"]
    assert affine_holds(witness, (2, -3, 1))
    state = ORIGIN
    remaining = 18
    live_all = True
    for _ in range(3):
        state = apply_word(sys, state, witness)
        remaining -= len(witness)
        if remaining < 0 or not is_terminal(sys, state, remaining):
            live_all = False
    assert not live_all
    assert linf(state) >= 8


def test_spectral_floats_are_not_a_theorem():
    spec = spectral_colive(dag_at(12))
    assert spec["not_a_spectral_theorem"]
    assert spec["floats_are_classification_only"]
    assert spec[GROWTH_NOT_INFINITUDE]
    assert spec["max_abs_by_remaining"][12] == 0.0
    assert spec["max_abs_by_remaining"][0] > 0.0
