"""Canonical Lean paths for the Juggler layered formalization."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
JUGGLER_DIR = REPO_ROOT / "formal" / "Problems" / "Juggler"
JUGGLER_BARREL = REPO_ROOT / "formal" / "Problems" / "Juggler.lean"
ENGINE_DIR = REPO_ROOT / "formal" / "Problems" / "Engine"

LAYERS: dict[str, Path] = {
    "Dynamics": JUGGLER_DIR / "Dynamics.lean",
    "Iteration": JUGGLER_DIR / "Iteration.lean",
    "Termination": JUGGLER_DIR / "Termination.lean",
    "Itinerary": JUGGLER_DIR / "Itinerary.lean",
    "WordStats": JUGGLER_DIR / "WordStats.lean",
    "Envelope": JUGGLER_DIR / "Envelope.lean",
    "Equality": JUGGLER_DIR / "Equality.lean",
    "Defect": JUGGLER_DIR / "Defect.lean",
    "GlobalDefect": JUGGLER_DIR / "GlobalDefect.lean",
    "DefectLowerBound": JUGGLER_DIR / "DefectLowerBound.lean",
    "Cells": JUGGLER_DIR / "Cells.lean",
    "Collapse": JUGGLER_DIR / "Collapse.lean",
    "Drift": JUGGLER_DIR / "Drift.lean",
    "FirstPassage": JUGGLER_DIR / "FirstPassage.lean",
    "Certificates": JUGGLER_DIR / "Certificates.lean",
    "Progress": JUGGLER_DIR / "Progress.lean",
    "Minimal": JUGGLER_DIR / "Minimal.lean",
    "MinimalClosure": JUGGLER_DIR / "MinimalClosure.lean",
    "Scale": JUGGLER_DIR / "Scale.lean",
    "Residuals": JUGGLER_DIR / "Residuals.lean",
    "NormalizedDefect": JUGGLER_DIR / "NormalizedDefect.lean",
    "ExpansionBlocks": JUGGLER_DIR / "ExpansionBlocks.lean",
    "ExpansionSlack": JUGGLER_DIR / "ExpansionSlack.lean",
    "NearTightScale": JUGGLER_DIR / "NearTightScale.lean",
    "ExpandingGrammar": JUGGLER_DIR / "ExpandingGrammar.lean",
    "LandingParity": JUGGLER_DIR / "LandingParity.lean",
    "Cycles": JUGGLER_DIR / "Cycles.lean",
    "CycleDiophantine": JUGGLER_DIR / "CycleDiophantine.lean",
    "SequentialMordell": JUGGLER_DIR / "SequentialMordell.lean",
    "LandingValuation": JUGGLER_DIR / "LandingValuation.lean",
    "PreimageCylinders": JUGGLER_DIR / "PreimageCylinders.lean",
    "OddLandingSets": JUGGLER_DIR / "OddLandingSets.lean",
    "WordLanguage": JUGGLER_DIR / "WordLanguage.lean",
}

DYNAMICS = LAYERS["Dynamics"]
ITERATION = LAYERS["Iteration"]
TERMINATION = LAYERS["Termination"]
ITINERARY = LAYERS["Itinerary"]
WORD_STATS = LAYERS["WordStats"]
ENVELOPE = LAYERS["Envelope"]
EQUALITY = LAYERS["Equality"]
DEFECT = LAYERS["Defect"]
GLOBAL_DEFECT = LAYERS["GlobalDefect"]
DEFECT_LOWER_BOUND = LAYERS["DefectLowerBound"]
CELLS = LAYERS["Cells"]
COLLAPSE = LAYERS["Collapse"]
DRIFT = LAYERS["Drift"]
FIRST_PASSAGE = LAYERS["FirstPassage"]
CERTIFICATES = LAYERS["Certificates"]
PROGRESS = LAYERS["Progress"]
MINIMAL = LAYERS["Minimal"]
MINIMAL_CLOSURE = LAYERS["MinimalClosure"]
SCALE = LAYERS["Scale"]
RESIDUALS = LAYERS["Residuals"]
NORMALIZED_DEFECT = LAYERS["NormalizedDefect"]
EXPANSION_BLOCKS = LAYERS["ExpansionBlocks"]
EXPANSION_SLACK = LAYERS["ExpansionSlack"]
NEAR_TIGHT_SCALE = LAYERS["NearTightScale"]
EXPANDING_GRAMMAR = LAYERS["ExpandingGrammar"]
LANDING_PARITY = LAYERS["LandingParity"]
CYCLES = LAYERS["Cycles"]
CYCLE_DIOPHANTINE = LAYERS["CycleDiophantine"]
SEQUENTIAL_MORDELL = LAYERS["SequentialMordell"]
LANDING_VALUATION = LAYERS["LandingValuation"]
PREIMAGE_CYLINDERS = LAYERS["PreimageCylinders"]
ODD_LANDING_SETS = LAYERS["OddLandingSets"]
WORD_LANGUAGE = LAYERS["WordLanguage"]

DELETED_ENGINE = (
    ENGINE_DIR / "FloorPower.lean",
    ENGINE_DIR / "Progress.lean",
    ENGINE_DIR / "MinimalNonTerm.lean",
    ENGINE_DIR / "RepeatedOE.lean",
    ENGINE_DIR / "OddRunFinancing.lean",
    ENGINE_DIR / "OddOddFrontier.lean",
    ENGINE_DIR / "ResidualChain.lean",
    ENGINE_DIR / "ResidualPath.lean",
    ENGINE_DIR / "RepeatedBlock.lean",
    ENGINE_DIR / "CycleWord.lean",
    ENGINE_DIR / "CycleDiophantine.lean",
)


def juggler_sources() -> list[Path]:
    return [JUGGLER_BARREL, *LAYERS.values()]


def juggler_text() -> str:
    return "\n".join(path.read_text(encoding="utf-8") for path in juggler_sources())


def engine_juggler_gone() -> bool:
    return not any(path.is_file() for path in DELETED_ENGINE)


def engine_floor_text() -> str:
    """Body of the deleted Engine FloorPower file. Empty after the rewrite."""
    path = ENGINE_DIR / "FloorPower.lean"
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def has_named(text: str, name: str) -> bool:
    return any(
        f"{kind} {name}" in text
        for kind in ("theorem", "def", "inductive", "abbrev", "structure")
    )
