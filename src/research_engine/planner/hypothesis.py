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


class PriorArtStatus(str, Enum):
    """Session-ledger novelty field. Not a theorem-ledger tag."""

    UNKNOWN = "UNKNOWN"
    KNOWN = "KNOWN"
    REPARAMETERIZATION = "REPARAMETERIZATION"
    NEW_FORMULATION = "NEW_FORMULATION"
    PROJECT_SPECIFIC = "PROJECT-SPECIFIC"


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
    prior_art_status: PriorArtStatus = PriorArtStatus.UNKNOWN
    novelty_note: str = ""
