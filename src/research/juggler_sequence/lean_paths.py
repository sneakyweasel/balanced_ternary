"""Canonical Lean paths for the Juggler layered formalization."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
JUGGLER_DIR = REPO_ROOT / "formal" / "Problems" / "Juggler"
JUGGLER_BARREL = REPO_ROOT / "formal" / "Problems" / "Juggler.lean"
JUGGLER_PAPER_BARREL = REPO_ROOT / "formal" / "Problems" / "JugglerPaper.lean"
ENGINE_DIR = REPO_ROOT / "formal" / "Problems" / "Engine"

PAPER_MODULES: tuple[str, ...] = (
    "Dynamics",
    "Iteration",
    "Termination",
    "Itinerary",
    "WordStats",
    "Envelope",
    "Equality",
    "Defect",
    "GlobalDefect",
    "Cells",
    "Certificates",
    "Progress",
    "Cycles",
    "LeftoverEval",
    "LeftoverCell",
    "LeftoverShort",
    "LeftoverFamilies",
    "EvenCountThree",
    "SmallCycleCensus",
    "NormalizedDefect",
    "ExpansionSlack",
    "NearTightScale",
    "CycleFinance",
    "RunSurvivorLattice",
)

LAYERS: dict[str, Path] = {
    "Dynamics": JUGGLER_DIR / "Dynamics.lean",
    "Iteration": JUGGLER_DIR / "Iteration.lean",
    "Termination": JUGGLER_DIR / "Termination.lean",
    "TerminationFloor257": JUGGLER_DIR / "TerminationFloor257.lean",
    "Itinerary": JUGGLER_DIR / "Itinerary.lean",
    "WordStats": JUGGLER_DIR / "WordStats.lean",
    "Envelope": JUGGLER_DIR / "Envelope.lean",
    "Corridor": JUGGLER_DIR / "Corridor.lean",
    "CubeCorridor": JUGGLER_DIR / "CubeCorridor.lean",
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
    "FirstInternalOO": JUGGLER_DIR / "FirstInternalOO.lean",
    "MinimumRelative": JUGGLER_DIR / "MinimumRelative.lean",
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
    "CycleCore": JUGGLER_DIR / "CycleCore.lean",
    "CycleObstructions": JUGGLER_DIR / "CycleObstructions.lean",
    "CycleExtrema": JUGGLER_DIR / "CycleExtrema.lean",
    "Cycles": JUGGLER_DIR / "Cycles.lean",
    "LeftoverEval": JUGGLER_DIR / "LeftoverEval.lean",
    "LeftoverCell": JUGGLER_DIR / "LeftoverCell.lean",
    "LeftoverShort": JUGGLER_DIR / "LeftoverShort.lean",
    "FirstETransportEval": JUGGLER_DIR / "FirstETransportEval.lean",
    "BunchedEOEEEval": JUGGLER_DIR / "BunchedEOEEEval.lean",
    "BunchedEOOEEEval": JUGGLER_DIR / "BunchedEOOEEEval.lean",
    "BunchedEEOEEval": JUGGLER_DIR / "BunchedEEOEEval.lean",
    "BunchedEOEOEEval": JUGGLER_DIR / "BunchedEOEOEEval.lean",
    "BunchedEOOOEEEval": JUGGLER_DIR / "BunchedEOOOEEEval.lean",
    "BunchedTight": JUGGLER_DIR / "BunchedTight.lean",
    "BunchedEOOEOEEval": JUGGLER_DIR / "BunchedEOOEOEEval.lean",
    "LeftoverFamilies": JUGGLER_DIR / "LeftoverFamilies.lean",
    "PrefixTwoEvenEval": JUGGLER_DIR / "PrefixTwoEvenEval.lean",
    "PrefixTwoEven": JUGGLER_DIR / "PrefixTwoEven.lean",
    "PrefixBunchedEval": JUGGLER_DIR / "PrefixBunchedEval.lean",
    "PrefixBunched": JUGGLER_DIR / "PrefixBunched.lean",
    "SmallCycleCensus": JUGGLER_DIR / "SmallCycleCensus.lean",
    "LengthEightCensus": JUGGLER_DIR / "LengthEightCensus.lean",
    "CycleDiophantine": JUGGLER_DIR / "CycleDiophantine.lean",
    "EvenCountThree": JUGGLER_DIR / "EvenCountThree.lean",
    "CycleMinObstruction": JUGGLER_DIR / "CycleMinObstruction.lean",
    "O7EEEEGap": JUGGLER_DIR / "O7EEEEGap.lean",
    "CycleMinFudge": JUGGLER_DIR / "CycleMinFudge.lean",
    "SequentialMordell": JUGGLER_DIR / "SequentialMordell.lean",
    "LandingValuation": JUGGLER_DIR / "LandingValuation.lean",
    "PreimageCylinders": JUGGLER_DIR / "PreimageCylinders.lean",
    "OddLandingSets": JUGGLER_DIR / "OddLandingSets.lean",
    "WordLanguage": JUGGLER_DIR / "WordLanguage.lean",
    "GapCells": JUGGLER_DIR / "GapCells.lean",
    "Escape": JUGGLER_DIR / "Escape.lean",
    "CycleFinance": JUGGLER_DIR / "CycleFinance.lean",
    "RunSurvivorLattice": JUGGLER_DIR / "RunSurvivorLattice.lean",
    "CycleHeightFinance": JUGGLER_DIR / "CycleHeightFinance.lean",
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
MINIMUM_RELATIVE = LAYERS["MinimumRelative"]
RESIDUALS = LAYERS["Residuals"]
NORMALIZED_DEFECT = LAYERS["NormalizedDefect"]
EXPANSION_BLOCKS = LAYERS["ExpansionBlocks"]
EXPANSION_SLACK = LAYERS["ExpansionSlack"]
NEAR_TIGHT_SCALE = LAYERS["NearTightScale"]
EXPANDING_GRAMMAR = LAYERS["ExpandingGrammar"]
LANDING_PARITY = LAYERS["LandingParity"]
CYCLE_CORE = LAYERS["CycleCore"]
CYCLE_OBSTRUCTIONS = LAYERS["CycleObstructions"]
CYCLE_EXTREMA = LAYERS["CycleExtrema"]
CYCLES_BARREL = LAYERS["Cycles"]


class _CycleKernel:
    """`Cycles.lean` is a barrel. Probes that read `CYCLES` still see the kernel."""

    def read_text(self, encoding: str = "utf-8") -> str:
        return cycle_kernel_text()

    def is_file(self) -> bool:
        return (
            CYCLE_CORE.is_file()
            and CYCLE_OBSTRUCTIONS.is_file()
            and CYCLE_EXTREMA.is_file()
        )


CYCLES = _CycleKernel()
LEFTOVER_EVAL = LAYERS["LeftoverEval"]
LEFTOVER_CELL = LAYERS["LeftoverCell"]
LEFTOVER_SHORT = LAYERS["LeftoverShort"]
LEFTOVER_FAMILIES = LAYERS["LeftoverFamilies"]
PREFIX_TWO_EVEN_EVAL = LAYERS["PrefixTwoEvenEval"]
PREFIX_TWO_EVEN = LAYERS["PrefixTwoEven"]
PREFIX_BUNCHED_EVAL = LAYERS["PrefixBunchedEval"]
PREFIX_BUNCHED = LAYERS["PrefixBunched"]
# Historical names: leftover proofs now live in Short / Families.
LEFTOVER_CYCLES = LEFTOVER_SHORT
LEFTOVER_TWO_EVEN = LEFTOVER_FAMILIES
FIRST_E_TRANSPORT_EVAL = LAYERS["FirstETransportEval"]
FIRST_E_TRANSPORT = LEFTOVER_FAMILIES
GAPPED_CYCLE_WORD = LEFTOVER_FAMILIES
BUNCHED_EEE = LEFTOVER_FAMILIES
BUNCHED_EOEE_EVAL = LAYERS["BunchedEOEEEval"]
BUNCHED_EOEE = LEFTOVER_FAMILIES
BUNCHED_EOOEE_EVAL = LAYERS["BunchedEOOEEEval"]
BUNCHED_EOOEE = LEFTOVER_FAMILIES
BUNCHED_EEOE_EVAL = LAYERS["BunchedEEOEEval"]
BUNCHED_EEOE = LEFTOVER_FAMILIES
BUNCHED_EOEOE_EVAL = LAYERS["BunchedEOEOEEval"]
BUNCHED_EOEOE = LEFTOVER_FAMILIES
BUNCHED_EOOOEE_EVAL = LAYERS["BunchedEOOOEEEval"]
BUNCHED_TIGHT = LAYERS["BunchedTight"]
BUNCHED_EOOOEE = LEFTOVER_FAMILIES
BUNCHED_EOOEOE_EVAL = LAYERS["BunchedEOOEOEEval"]
BUNCHED_EOOEOE = LEFTOVER_FAMILIES
SMALL_CYCLE_CENSUS = LAYERS["SmallCycleCensus"]
LENGTH_EIGHT_CENSUS = LAYERS["LengthEightCensus"]
EVEN_COUNT_THREE = LAYERS["EvenCountThree"]
CYCLEMIN_OBSTRUCTION = LAYERS["CycleMinObstruction"]
FIRST_INTERNAL_OO = LAYERS["FirstInternalOO"]
O7EEEE_GAP = LAYERS["O7EEEEGap"]
CYCLEMIN_FUDGE = LAYERS["CycleMinFudge"]
CYCLE_DIOPHANTINE = LAYERS["CycleDiophantine"]
SEQUENTIAL_MORDELL = LAYERS["SequentialMordell"]
LANDING_VALUATION = LAYERS["LandingValuation"]
PREIMAGE_CYLINDERS = LAYERS["PreimageCylinders"]
ODD_LANDING_SETS = LAYERS["OddLandingSets"]
WORD_LANGUAGE = LAYERS["WordLanguage"]
GAP_CELLS = LAYERS["GapCells"]
ESCAPE = LAYERS["Escape"]
CYCLE_FINANCE = LAYERS["CycleFinance"]
RUN_SURVIVOR_LATTICE = LAYERS["RunSurvivorLattice"]
CYCLE_HEIGHT_FINANCE = LAYERS["CycleHeightFinance"]

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


def juggler_sources(*, exclude: tuple[str, ...] = ()) -> list[Path]:
    skip = set(exclude)
    return [
        JUGGLER_BARREL,
        JUGGLER_PAPER_BARREL,
        *[path for name, path in LAYERS.items() if name not in skip],
    ]


def juggler_text(*, exclude: tuple[str, ...] = ()) -> str:
    return "\n".join(
        path.read_text(encoding="utf-8") for path in juggler_sources(exclude=exclude)
    )


def pre_finance_text() -> str:
    """Laboratory corpus without CycleFinance.lean.

    Older leftover/census probes treat length-9/10 absence as “this
    branch did not add a census.” Finance later proved those lengths
    by a different inequality; they must not flip those probes.
    """
    return juggler_text(exclude=("CycleFinance", "CycleHeightFinance"))


def cycle_kernel_text() -> str:
    """`Cycles.lean` is a barrel. Kernel declarations live in Core + named words + Extrema."""
    return (
        CYCLE_CORE.read_text(encoding="utf-8")
        + "\n"
        + CYCLE_OBSTRUCTIONS.read_text(encoding="utf-8")
        + "\n"
        + CYCLE_EXTREMA.read_text(encoding="utf-8")
    )


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
