"""Research hypotheses with typed claim kinds.

Statuses are not interchangeable with attack outcomes. A bounded
``SUPPORTED`` attack does not prove an exact ``LIVE`` hypothesis.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from research_engine.core.semantics import ClaimKind, SearchScope


class HypothesisStatus(str, Enum):
    OPEN = "OPEN"
    SUPPORTED = "SUPPORTED"
    REFUTED = "REFUTED"
    SETTLED = "SETTLED"
    PARKED = "PARKED"
    CLOSED = "CLOSED"


class DecisionKind(str, Enum):
    PROMOTE = "PROMOTE"
    REFUTE = "REFUTE"
    PARK = "PARK"
    CLOSE = "CLOSE"
    SUPERSEDE = "SUPERSEDE"


@dataclass(frozen=True)
class Hypothesis:
    id: str
    statement: str
    kind: ClaimKind
    intended_scope: SearchScope
    status: HypothesisStatus = HypothesisStatus.OPEN
    problem: str = ""
    evidence: str = ""
    superseded_by: str = ""
