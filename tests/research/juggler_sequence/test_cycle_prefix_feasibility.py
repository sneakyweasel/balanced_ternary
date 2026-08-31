"""Prefix-expansion feasibility. Not a halt test."""

from __future__ import annotations

import json
from pathlib import Path

from research.juggler_sequence.cycle_christoffel import (
    bits_to_word,
    christoffel_bits,
)
from research.juggler_sequence.cycle_finance import (
    o_min_and_theta,
    sha256_int_list,
)
from research.juggler_sequence.cycle_prefix_feasibility import (
    ceiling_christoffel_word,
    extremal_word,
    first_isolated_oe_count,
    first_odd_run,
    first_oo_ok,
    isolated_oe_r_max,
    prefix_admissible,
    r_of,
    starts_oo,
)

REPO = Path(__file__).resolve().parents[3]


def test_small_envelope_and_extremal_start():
    assert [r_of(k) for k in range(6)] == [0, 1, 2, 2, 3, 4]
    assert extremal_word(6) == "OOEOOE"
    assert isolated_oe_r_max(2) == 0
    assert isolated_oe_r_max(3) == 1
    assert isolated_oe_r_max(4) == 3
    assert first_odd_run("OOEOOE") == 2
    assert first_isolated_oe_count("OOEOOE") == 0
    assert first_oo_ok("OOEOOE")
    assert not first_oo_ok("OOEOE")
    assert not first_oo_ok("OEOOEOE")
    assert starts_oo("OOEOOE")
    assert prefix_admissible("OOEOOE")


def test_spotlight_25781_and_55293_have_paths():
    odd_count, _theta = o_min_and_theta(25781)
    assert odd_count == 16266
    word = extremal_word(25781)
    assert word.startswith("OOE")
    assert not word.startswith("OOEOE")
    assert first_odd_run(word) == 2
    assert first_isolated_oe_count(word) == 0
    assert first_oo_ok(word)
    assert prefix_admissible(word)
    assert word.count("O") == 16266
    assert r_of(25781) == 16266

    tight = extremal_word(55293)
    odd_tight, _theta_tight = o_min_and_theta(55293)
    assert tight.startswith("OOE")
    assert not tight.startswith("OOEOE")
    assert first_oo_ok(tight)
    assert prefix_admissible(tight)
    assert tight.count("O") == odd_tight


def test_christoffel_matches_existing_formula_on_small_leftovers():
    for length in (11, 19, 84):
        odd_count, _theta = o_min_and_theta(length)
        ours = ceiling_christoffel_word(length, odd_count)
        theirs = bits_to_word(christoffel_bits(length, odd_count))
        assert ours == theirs
        assert prefix_admissible(ours)
        assert first_oo_ok(ours)


def test_prefix_feasibility_scan_closes():
    payload = json.loads(
        (
            REPO / "data" / "research" / "juggler" / "cycle_finance"
            / "prefix_feasibility.json"
        ).read_text(encoding="utf-8")
    )
    assert payload["survivor_count"] == 99
    assert payload["all_A_nonempty"] is True
    assert payload["A_empty"] == []
    assert payload["A_nonempty_count"] == 99
    assert payload["ends_at_o_min_failures"] == []
    assert payload["first_oo_failures"] == []
    assert payload["christoffel_failures"] == []
    assert payload["all_christoffel_admissible"] is True
    assert payload["R2"] == 0
    assert payload["R3"] == 1
    assert payload["R4"] == 3
    assert payload["small_r"] == [0, 1, 2, 2, 3, 4]
    assert payload["small_extremal"] == "OOEOOE"
    assert payload["halt_theorem"] is False
    assert payload["no_cycle_all_lengths"] is False
    assert payload["sha256_survivors"] == sha256_int_list(
        [row["L"] for row in payload["rows"]]
    )
    assert all(row["A_nonempty"] for row in payload["rows"])
    assert payload["spotlights"]["25781"]["L"] == 25781
    assert payload["spotlights"]["25781"]["o"] == 16266
    assert payload["spotlights"]["55293"]["L"] == 55293


def test_dossier_records_close():
    dossier = (
        REPO / "docs" / "problems" / "juggler_cycle_prefix_feasibility.md"
    ).read_text(encoding="utf-8")
    assert "prefix_feasibility.json" in dossier
    assert "juggler_cycle_prefix_feasibility_leftover_killer" in dossier
    assert "**CLOSE**" in dossier
