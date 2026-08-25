"""Persistent attack records for the weight-drift experiment."""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

from research_engine.planner.hypothesis import PriorArtStatus
from research_engine.planner.orchestrator import PlannerReport
from research_engine.planner.records import write_records as write_engine_records
from research_engine.verification.targets import TheoremTarget

RECORD_DIR = (
    Path(__file__).resolve().parents[3]
    / "experiments"
    / "balanced_ternary"
    / "weight_drift"
)


def write_records(
    report: PlannerReport,
    targets: Sequence[TheoremTarget],
    *,
    directory: Path | None = None,
    problem: str = "balanced_ternary_weight_drift",
) -> tuple[Path, ...]:
    folder = directory if directory is not None else RECORD_DIR
    return write_engine_records(
        report,
        targets,
        directory=folder,
        problem=problem,
        prior_art_status=PriorArtStatus.KNOWN.value,
        novelty_note="Kaprekar-type n+W(n) drift; CLOSE as known generator class",
        branch_status="CLOSE",
    )
