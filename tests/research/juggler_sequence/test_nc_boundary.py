"""Noncontracting realization boundary. Not an engine-control test."""

from __future__ import annotations

import json

from research.juggler_sequence.compensated_contraction import image_after
from research.juggler_sequence.nc_boundary import (
    CLASS_COMPLEX,
    JSON_PATH,
    LEAN_THEOREMS,
    collect_partition,
    extension_laws,
    first_inversion,
    lean_api_present,
    word_row,
    word_stats,
)
from research.juggler_sequence.near_extremal_prefixes import exponent_gap


def test_calibration_E_empty_O_all_odds():
    realizing, nc = collect_partition(n_max=80, k_max=4)
    assert nc.get("E", []) == []
    assert nc["O"] == realizing["O"]
    assert realizing["O"][0] == 1
    assert all(n % 2 == 1 for n in realizing["O"])


def test_formal_contraction_has_empty_N():
    realizing, nc = collect_partition(n_max=200, k_max=6)
    for word, starts in realizing.items():
        if exponent_gap(len(word), word.count("O")) <= 0:
            continue
        unexpected = [n for n in nc.get(word, []) if not (n == 1 and word == "O" * len(word))]
        assert unexpected == []
        if starts:
            n = starts[0]
            assert image_after(n, word) < n or n == 1


def test_definition_matches_image():
    realizing, nc = collect_partition(n_max=120, k_max=5)
    for word in ("OOE", "OEO", "OO"):
        starts = realizing[word]
        nc_set = set(nc[word])
        for n in starts:
            assert (image_after(n, word) >= n) == (n in nc_set)


def test_ooe_oeo_same_ko_can_split_or_match():
    realizing, nc = collect_partition(n_max=4000, k_max=3)
    ooe = word_row("OOE", realizing["OOE"], nc.get("OOE", []))
    oeo = word_row("OEO", realizing["OEO"], nc.get("OEO", []))
    assert ooe["k"] == oeo["k"] == 3
    assert ooe["o"] == oeo["o"] == 2
    assert ooe["expanding"] is True
    assert oeo["expanding"] is True


def test_inversion_helper():
    assert first_inversion([1, 3, 5, 7], {1, 3}) == {"n1": 1, "n2": 5}
    assert first_inversion([1, 3, 5], {1, 3, 5}) is None


def test_late_contract_and_late_expand():
    realizing, nc = collect_partition(n_max=40, k_max=5)
    ext = extension_laws(realizing, nc)
    assert ext["N_wb_subseteq_N_w"] is False
    assert ext["late_expand"] == {"parent": "EO", "child": "EOO", "n": 10}
    assert ext["late_contract"]["n"] == 3
    assert ext["late_contract"]["parent"] == "OOOE"
    assert ext["late_contract"]["child"] == "OOOEE"
    assert 7 in nc["O"] and 7 in realizing["OE"] and 7 not in nc.get("OE", [])


def test_expanding_gap_sign():
    assert word_stats("OOE")["gap"] < 0
    assert word_stats("E")["gap"] > 0
    assert word_stats("OE")["gap"] > 0


def test_lean_api_no_halt():
    lean = lean_api_present()
    assert lean["sorry_free"] is True
    for name in LEAN_THEOREMS:
        assert lean[name] is True
    assert lean["no_global_termination_theorem"] is True
    assert lean["no_forbidden_engines"] is True


def test_committed_artifacts_if_present():
    if not JSON_PATH.is_file():
        return
    payload = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    assert payload["engine_control_layer_modified"] is False
    assert payload["anti_overclaim"]["reopen_pe_factors"] is False
    assert payload["anti_overclaim"]["reopen_sum_rho"] is False
    assert payload["anti_overclaim"]["automaton"] is False
    if payload["decision"]["classification"] == CLASS_COMPLEX:
        assert payload["scan"]["contracting_exceptions"] == []
        assert payload["scan"]["calibration"]["N_E_empty"] is True
        assert payload["scan"]["diagnostic"]["inversion_count"] == 1
        assert payload["scan"]["diagnostic"]["smallest_inversion"]["word"] == "EOO"
        assert payload["scan"]["extension"]["late_expand"]["n"] == 10
        assert payload["scan"]["extension"]["late_contract"]["n"] == 3
