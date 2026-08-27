"""Juggler Lean layers are one-way, Engine copies are gone, and no sorry."""

from __future__ import annotations

from research.juggler_sequence.lean_paths import (
    DELETED_ENGINE,
    JUGGLER_DIR,
    LAYERS,
    engine_juggler_gone,
    has_named,
    juggler_sources,
    juggler_text,
)

BOXED = (
    "HasFiniteStop",
    "HasFiniteCoeffStop",
    "FiniteCoeffStopConjecture",
    "DescentCertificate",
    "FiniteProgress",
    "MinimalNonTerm",
    "MinimalImpliesCoeffStop",
    "follows_iff_word",
    "coeffStop_implies_stop",
)

FORBIDDEN_ENGINE_NAMES = (
    "Problems.Engine.FloorPower",
    "Problems.Engine.Progress",
    "Problems.Engine.MinimalNonTerm",
    "Problems.Engine.RepeatedOE",
    "Problems.Engine.OddRunFinancing",
    "Problems.Engine.OddOddFrontier",
    "Problems.Engine.ResidualChain",
    "Problems.Engine.ResidualPath",
    "Problems.Engine.RepeatedBlock",
    "Problems.Engine.CycleWord",
    "Problems.Engine.CycleDiophantine",
)


def test_engine_juggler_files_are_gone():
    assert engine_juggler_gone()
    for path in DELETED_ENGINE:
        assert not path.is_file(), path


def test_layers_exist_and_are_sorry_free():
    assert JUGGLER_DIR.is_dir()
    text = juggler_text()
    assert "sorry" not in text
    assert "admit" not in text
    for name, path in LAYERS.items():
        assert path.is_file(), name
        body = path.read_text(encoding="utf-8")
        assert "sorry" not in body
        assert "admit" not in body


def test_boxed_implication_is_first_class():
    text = juggler_text()
    for name in BOXED:
        assert has_named(text, name), name
    assert "theorem juggler_reaches_one" not in text
    assert "theorem all_finiteProgress" not in text


def test_no_engine_juggler_names_in_live_sources():
    for path in juggler_sources():
        body = path.read_text(encoding="utf-8")
        assert "Problems.Engine" not in body, path.name
        for name in FORBIDDEN_ENGINE_NAMES:
            assert name not in body, f"{path.name} mentions {name}"
