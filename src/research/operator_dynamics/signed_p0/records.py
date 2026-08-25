"""Persistent attack records for the N∘I₀∘D benchmark."""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

from research_engine.planner.hypothesis import PriorArtStatus
from research_engine.planner.orchestrator import PlannerReport
from research_engine.planner.records import write_records as write_engine_records
from research_engine.verification.targets import TheoremTarget

RECORD_DIR = (
    Path(__file__).resolve().parents[4]
    / "experiments"
    / "balanced_ternary"
    / "operator_dynamics"
)


def write_records(
    report: PlannerReport,
    targets: Sequence[TheoremTarget],
    *,
    directory: Path | None = None,
    problem: str = "operator_dynamics_benchmark",
) -> tuple[Path, ...]:
    folder = directory if directory is not None else RECORD_DIR
    return write_engine_records(
        report,
        targets,
        directory=folder,
        problem=problem,
        prior_art_status=PriorArtStatus.NEW_FORMULATION.value,
        novelty_note="iteration of N∘P_0; F_a,b collapses to I_a",
        branch_status="CLOSE",
    )
