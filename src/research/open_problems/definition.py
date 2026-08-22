"""Lightweight research-problem descriptor. Not a framework."""

from __future__ import annotations

from dataclasses import dataclass

STATUSES = (
    "EXPLORATORY",
    "STRUCTURAL",
    "THEOREM",
    "PAPER_CANDIDATE",
    "ARCHIVED",
)


@dataclass(frozen=True)
class ProblemDefinition:
    id: str
    title: str
    status: str
    statement: str
    bt_relevance: str
    docs: tuple[str, ...] = ()
    lean: tuple[str, ...] = ()
    conjectures: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.status not in STATUSES:
            raise ValueError(f"unknown research status {self.status!r}")
