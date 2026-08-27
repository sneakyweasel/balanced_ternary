"""Landing-image geometry. Not an engine-control test."""

from __future__ import annotations

from pathlib import Path

from research.juggler_sequence.compensated_contraction import image_after
from research.juggler_sequence.landing_image import (
    image_of,
    image_row,
    lean_api_present,
    phi,
    selected_confirm,
)
from research.juggler_sequence.realization_geometry import collect_realizing


def test_phi_recurrence_and_no_inversion():
    realizing = collect_realizing(n_max=400, k_max=6)
    for word, starts in realizing.items():
        inv = image_row(word, starts)["inversion"]
        assert inv is None
        ys = image_of(word, starts)
        if starts:
            assert image_after(starts[0], word) == ys[0]
            assert image_after(starts[-1], word) == ys[-1]
        if len(word) >= 6:
            continue
        for letter in "OE":
            child = word + letter
            if child not in realizing:
                continue
            assert image_of(child, realizing[child]) == phi(ys, letter)


def test_pure_e_image_is_an_interval_pure_o_is_not():
    realizing = collect_realizing(n_max=4000, k_max=4)
    e = image_row("E", realizing["E"])
    assert e["interval_class"] == "SINGLE_INTERVAL"
    assert e["parity_support"] == "MIXED"
    assert e["degree"] == 2
    assert e["y_min"] == 1
    o = image_row("O", realizing["O"])
    assert o["component_count"] > 1
    assert o["interval_class"] != "SINGLE_INTERVAL"
    eeee = image_row("EEEE", realizing["EEEE"])
    assert eeee["y_size"] == 1
    assert eeee["degree"] == 1


def test_lean_api_no_halt():
    lean = lean_api_present()
    assert lean["sorry_free"] is True
    assert lean["floorPower"] is True
    assert lean["floorPower_even_mono"] is True
    assert lean["floorPower_odd_mono"] is True
    assert lean["image_monotone_of_follows"] is True
    assert lean["no_global_termination_theorem"] is True
    assert lean["no_forbidden_engines"] is True


def test_confirm_selected_stays_monotone():
    confirm = selected_confirm(n_max=2000)
    assert confirm["inversion_count"] == 0
    assert confirm["monotone_all"] is True
    assert confirm["n_words"] > 0


def test_dossier_parks_without_atlas_schema():
    root = Path(__file__).resolve().parents[3]
    dossier = (root / "docs" / "problems" / "juggler_landing_image.md").read_text(
        encoding="utf-8"
    )
    assert "**PARK**" in dossier
    assert "image_monotone_of_follows" in dossier
    assert "LANDING_IMAGE" in dossier
    assert "not added" in dossier
