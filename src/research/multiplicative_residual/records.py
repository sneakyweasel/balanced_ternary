"""Persistent attack records. Not the named theorem ledger."""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

from research_engine.attacks.result import AttackResult
from research_engine.planner.orchestrator import PlannerReport
from research_engine.planner.records import record_status
from research_engine.planner.records import render_record as _render_record
from research_engine.planner.records import write_records as _write_records
from research_engine.verification.targets import TheoremTarget

RECORD_DIR = (
    Path(__file__).resolve().parents[3]
    / "experiments"
    / "balanced_ternary"
    / "multiplicative_residual"
)

__all__ = ["RECORD_DIR", "record_status", "render_record", "write_records"]


def render_record(
    result: AttackResult,
    *,
    problem: str = "multiplicative_residual",
    lean_theorem: str = "",
) -> str:
    return _render_record(
        result,
        problem=problem,
        lean_theorem=lean_theorem,
        prior_art_status="PROJECT-SPECIFIC",
        novelty_note="product controls factor through raw contribution",
        branch_status="PROMOTE",
    )


def write_records(
    report: PlannerReport,
    targets: Sequence[TheoremTarget],
    *,
    directory: Path | None = None,
    problem: str = "multiplicative_residual",
) -> tuple[Path, ...]:
    folder = directory if directory is not None else RECORD_DIR
    return _write_records(
        report,
        targets,
        directory=folder,
        problem=problem,
        prior_art_status="PROJECT-SPECIFIC",
        novelty_note="product controls factor through raw contribution",
        branch_status="PROMOTE",
    )
