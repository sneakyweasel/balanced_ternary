"""v2.3 Phase 4 quantifier types. EXISTS_PATH is not ALL_PATHS."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from research_engine.core.semantics import State
from research_engine.memory.types import NoveltyStatus

ENGINE_QUANTIFIER_VERSION = "0.2.6"

MappingLike = Mapping[str, Any]


class PathQuantifier(str, Enum):
    EXISTS_PATH = "EXISTS_PATH"
    ALL_PATHS = "ALL_PATHS"


class PathStatus(str, Enum):
    """Engine path evidence. NO_PATH_FOUND is not nonexistence."""

    EXISTENTIAL_WITNESS = "EXISTENTIAL_WITNESS"
    NO_PATH_FOUND = "NO_PATH_FOUND"
    REFUTED = "REFUTED"
    CERTIFIED_ON_WINDOW = "CERTIFIED_ON_WINDOW"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class RelationEdge:
    """One-step pair from legal_controls × transition. This is R ⊆ X×X."""

    src: State
    control: object
    dst: State

    def as_dict(self) -> dict[str, Any]:
        return {
            "src": list(self.src) if isinstance(self.src, tuple) else self.src,
            "control": self.control,
            "dst": list(self.dst) if isinstance(self.dst, tuple) else self.dst,
        }


@dataclass(frozen=True)
class PathClaim:
    """Named ∃/∀ claim. CERTIFIED_ON_WINDOW is not a Z-theorem."""

    name: str
    quantifier: PathQuantifier
    status: PathStatus
    witness: tuple[State, ...] = ()
    counterexample: tuple[State, ...] = ()
    window: tuple[int, ...] = ()
    cap: int = 0
    statement: str = ""
    source_target: str = ""
    novelty_status: NoveltyStatus = NoveltyStatus.UNKNOWN

    def as_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "quantifier": self.quantifier.value,
            "status": self.status.value,
            "witness": [list(item) if isinstance(item, tuple) else item for item in self.witness],
            "counterexample": [
                list(item) if isinstance(item, tuple) else item for item in self.counterexample
            ],
            "window": list(self.window),
            "cap": self.cap,
            "statement": self.statement,
            "source_target": self.source_target,
            "novelty_status": self.novelty_status.value,
        }


@dataclass(frozen=True)
class QuantifierReport:
    source_target: str
    claims: tuple[PathClaim, ...]
    relation_sample: tuple[RelationEdge, ...]
    census_skipped: bool
    closure_complete: bool = False
    version: str = ENGINE_QUANTIFIER_VERSION
    novelty_status: NoveltyStatus = NoveltyStatus.UNKNOWN

    def claim(self, name: str) -> PathClaim | None:
        for item in self.claims:
            if item.name == name:
                return item
        return None

    def as_dict(self) -> dict[str, Any]:
        return {
            "source_target": self.source_target,
            "claims": [item.as_dict() for item in self.claims],
            "relation_sample": [item.as_dict() for item in self.relation_sample],
            "census_skipped": self.census_skipped,
            "closure_complete": self.closure_complete,
            "version": self.version,
            "novelty_status": self.novelty_status.value,
        }
