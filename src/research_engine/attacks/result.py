"""Typed attack reports. A finite census is not an asymptotic theorem."""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from enum import Enum
from types import MappingProxyType
from typing import Any, Protocol, TypeVar

from research_engine.algebra.linear_functionals import LinearFunctional
from research_engine.core.affine_system import AffineSystem
from research_engine.core.block import BlockAction
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import CertificateKind, ClaimKind, Control, SearchScope, State

S = TypeVar("S")
C = TypeVar("C")
P = TypeVar("P")


class AttackStatus(str, Enum):
    """Outcome of one attack on one stated claim.

    ``OBSERVATION`` is finite evidence. It is not ``SUPPORTED``.
    """

    INAPPLICABLE = "INAPPLICABLE"
    OBSERVATION = "OBSERVATION"
    SUPPORTED = "SUPPORTED"
    REFUTED = "REFUTED"
    INCONCLUSIVE = "INCONCLUSIVE"


@dataclass(frozen=True)
class AttackContext:
    """Optional extra data. Missing fields make some attacks inapplicable."""

    live_only: bool = True
    max_steps: int | None = None
    max_states: int | None = None
    affine: AffineSystem | None = None
    functional: LinearFunctional | None = None
    candidate_region: frozenset[State] | None = None
    phases: tuple[Any, ...] | None = None
    reverse_preimage: Callable[[State], Sequence[State]] | None = None
    reverse_seeds: tuple[State, ...] | None = None
    reverse_max_depth: int | None = None
    moduli: tuple[int, ...] = (2, 3, 4, 5)
    word: tuple[Control, ...] | None = None
    block: BlockAction | None = None
    pair: tuple[Any, Any] | None = None
    max_separation_depth: int | None = None
    symmetry_candidates: tuple[Any, ...] | None = None
    symmetry_domain: frozenset[Any] | None = None
    skip_attacks: tuple[str, ...] = ()
    descent_potential: Callable[[State], int] | None = None
    prior_results: tuple[Any, ...] = ()
    enable_restricted_symbolic_composition: bool = False


@dataclass(frozen=True)
class AttackResult:
    name: str
    status: AttackStatus
    kind: ClaimKind
    scope: SearchScope
    claim: str
    evidence: Mapping[str, Any] = field(default_factory=dict)
    counterexamples: tuple[Any, ...] = ()
    certificates: tuple[Any, ...] = ()
    recommended_next_attacks: tuple[str, ...] = ()
    certificate_kind: CertificateKind | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "evidence", MappingProxyType(dict(self.evidence)))
        object.__setattr__(self, "counterexamples", tuple(self.counterexamples))
        object.__setattr__(self, "certificates", tuple(self.certificates))
        object.__setattr__(self, "recommended_next_attacks", tuple(self.recommended_next_attacks))


class Attack(Protocol):
    name: str

    def applicable(self, spec: ProblemSpec[S, C, P], context: AttackContext) -> bool: ...

    def run(self, spec: ProblemSpec[S, C, P], context: AttackContext) -> AttackResult: ...


def inapplicable(name: str, reason: str, kind: ClaimKind) -> AttackResult:
    return AttackResult(
        name=name,
        status=AttackStatus.INAPPLICABLE,
        kind=kind,
        scope=SearchScope.BOUNDED,
        claim=reason,
    )


def phase_key(phase: Any) -> Any:
    return getattr(phase, "value", phase)
