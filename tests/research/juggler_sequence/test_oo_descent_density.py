"""Fixed-family OO descent density. Not a halt test and not Terras."""

from __future__ import annotations

import json

from research.juggler_sequence.compensated_contraction import follows_word, image_after
from research.juggler_sequence.oo_descent_density import (
    CLASS_LEFTOVER,
    CLASS_VANISHING,
    JSON_PATH,
    PROP45_N1000,
    WORD_OOEOE,
    WORD_OOOEE,
    classify,
    is_odd_odd,
    lean_api_present,
    render_markdown,
    reproduce_prop45,
    walk_prefix,
    window_census,
)
from research.juggler_sequence.power_words import ANTI_OVERCLAIM, floor_power


def test_oooee_and_ooeoe_are_the_shortest_contracting_oo_words():
    assert is_odd_odd(3)
    assert follows_word(3, WORD_OOOEE)
    assert image_after(3, WORD_OOOEE) < 3
    walked = walk_prefix(3)
    assert walked["oooee"] is True
    assert walked["ooeoe"] is False
    assert walked["tau"] == 5
    assert is_odd_odd(5)
    assert not follows_word(5, WORD_OOOEE)
    assert not follows_word(5, WORD_OOEOE)
    five = walk_prefix(5)
    assert five["oooee"] is False
    assert five["ooeoe"] is False
    assert five["tau"] == 4
    assert five["prefix"].startswith("OOEE")


def test_n1000_reproduces_proposition_45():
    rows = window_census(1_000, snapshots=(1_000,))
    assert len(rows) == 1
    row = rows[0]
    assert row["oo"] == PROP45_N1000["oo"]
    assert row["oo_return_20"] == PROP45_N1000["oo_return20"]
    assert row["all_return_20"] == PROP45_N1000["all_return20"]
    assert reproduce_prop45(rows)["ok"] is True
    assert row["oooee"] >= 1
    assert row["oooee"] < row["oo"]
    assert row["word_union"] < row["oo"]
    assert row["oo_leftover_rate_20"] > 0.1


def test_lean_witnesses_without_new_attack():
    lean = lean_api_present()
    assert lean["sorry_free"] is True
    assert lean["FiniteProgress"] is True
    assert lean["floorPower_oooee_of_follows"] is True
    assert lean["wordOOOEE"] is True
    assert lean["no_global_termination_theorem"] is True
    assert lean["no_all_finiteProgress_proved"] is True
    assert lean["no_progress_tactic"] is True
    assert lean["no_length_seven_cycle_theorem"] is True


def test_classify_small_window_is_not_vanishing():
    rows = window_census(10_000, snapshots=(1_000, 10_000))
    lean = lean_api_present()
    decision = classify(rows, lean)
    assert decision["classification"] != CLASS_VANISHING
    assert decision["last_leftover"]["oooee"] > 0.5
    assert decision["last_leftover"]["horizon_20"] > 0.1
    text = render_markdown(
        {
            "experiment": "juggler_oo_descent_density",
            "engine_control_layer_modified": False,
            "anti_overclaim": {
                **dict(ANTI_OVERCLAIM),
                "almost_all_finiteProgress": False,
                "terras_for_juggler": False,
            },
            "scan": {
                "basin": [1],
                "words": [WORD_OOOEE, WORD_OOEOE],
                "horizons": [5, 10, 20, 40],
                "rows": rows,
                "prop45": reproduce_prop45(rows),
            },
            "lean": lean,
            "decision": decision,
        }
    )
    assert "OOOEE" in text
    assert "not a halt result" in text


def test_committed_artifacts_schema():
    assert JSON_PATH.is_file()
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    assert data["experiment"] == "juggler_oo_descent_density"
    assert data["engine_control_layer_modified"] is False
    assert data["anti_overclaim"]["almost_all_finiteProgress"] is False
    assert data["anti_overclaim"]["terras_for_juggler"] is False
    assert data["anti_overclaim"]["global_termination"] is False
    assert data["scan"]["words"] == [WORD_OOOEE, WORD_OOEOE]
    assert data["scan"]["prop45"]["ok"] is True
    assert data["decision"]["classification"] == CLASS_LEFTOVER
    nmax = {row["n_max"] for row in data["scan"]["rows"]}
    assert {10_000, 100_000, 1_000_000} <= nmax
    last = next(row for row in data["scan"]["rows"] if row["n_max"] == 1_000_000)
    assert last["oo"] == 249926
    assert last["oo_leftover_20"] == 26243
    assert last["word_union_leftover_rate"] > 0.7
    assert last["oo_leftover_rate_40"] > 0.02
    assert floor_power(3) == 5
