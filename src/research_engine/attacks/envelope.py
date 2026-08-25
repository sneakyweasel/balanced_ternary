"""Invariant envelope versus exact reachable set.

These objects wrap existing affine/closure certificates. A leak-free
candidate region is not an invariant theorem.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Hashable

from research_engine.attacks.affine import AffineInvariantAttack
from research_engine.attacks.closure import ExhaustiveClosureAttack
from research_engine.attacks.result import AttackContext, AttackResult, AttackStatus
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import CertificateKind, SearchScope


@dataclass(frozen=True)
class InvariantEnvelopeResult:
    candidate: frozenset[Hashable]
    status: AttackStatus
    scope: SearchScope
    inclusion: str
    certificate_kind: CertificateKind | None = None
    leaks: tuple[Any, ...] = ()
    parameterization: str = ""
    attack: AttackResult | None = None

    @property
    def size(self) -> int:
        return len(self.candidate)


@dataclass(frozen=True)
class ExactReachabilityResult:
    seed: Hashable
    reachable: frozenset[Hashable]
    complete: bool
    status: AttackStatus
    scope: SearchScope
    certificate_kind: CertificateKind | None = None
    statistics: Mapping[str, Any] = field(default_factory=dict)
    attack: AttackResult | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "statistics", MappingProxyType(dict(self.statistics)))

    @property
    def size(self) -> int:
        return len(self.reachable)


@dataclass(frozen=True)
class EnvelopeComparison:
    holes: frozenset[Hashable]
    extra: frozenset[Hashable]
    reachable_inside_envelope: bool
    envelope_equals_reachable: bool

    @property
    def hole_count(self) -> int:
        return len(self.holes)


def find_invariant(spec: ProblemSpec, context: AttackContext) -> InvariantEnvelopeResult:
    """One-step candidate-region check. Leak-free remains an observation."""
    region = context.candidate_region
    if region is None:
        return InvariantEnvelopeResult(
            candidate=frozenset(),
            status=AttackStatus.INAPPLICABLE,
            scope=SearchScope.BOUNDED,
            inclusion="unspecified",
        )
    result = AffineInvariantAttack().run(spec, context)
    leaks = tuple(result.counterexamples)
    if result.status is AttackStatus.REFUTED:
        inclusion = "candidate_does_not_contain_images"
    else:
        inclusion = "candidate_contains_tested_images"
    return InvariantEnvelopeResult(
        candidate=frozenset(region),
        status=result.status,
        scope=result.scope,
        inclusion=inclusion,
        certificate_kind=result.certificate_kind,
        leaks=leaks,
        attack=result,
    )


def compute_exact_reachable(
    spec: ProblemSpec,
    context: AttackContext | None = None,
) -> ExactReachabilityResult:
    """Residual-state BFS at the frozen initial phase."""
    ctx = context if context is not None else AttackContext()
    result = ExhaustiveClosureAttack().run(spec, ctx)
    union = result.evidence.get("union")
    if union is None:
        reached: frozenset[Hashable] = frozenset()
    else:
        reached = frozenset(union)
    complete = bool(result.evidence.get("complete"))
    return ExactReachabilityResult(
        seed=spec.canonicalize(spec.initial_state),
        reachable=reached,
        complete=complete,
        status=result.status,
        scope=result.scope,
        certificate_kind=result.certificate_kind,
        statistics={
            "union_size": result.evidence.get("union_size"),
            "state_cap": result.evidence.get("state_cap"),
            "complete": complete,
        },
        attack=result,
    )


def compare_envelope_to_reachable(
    envelope: InvariantEnvelopeResult,
    reachable: ExactReachabilityResult,
) -> EnvelopeComparison:
    holes = envelope.candidate - reachable.reachable
    extra = reachable.reachable - envelope.candidate
    return EnvelopeComparison(
        holes=holes,
        extra=extra,
        reachable_inside_envelope=not extra,
        envelope_equals_reachable=not holes and not extra,
    )


def envelope_from_interval(lo: int, hi: int, *, as_states: bool = True) -> InvariantEnvelopeResult:
    """Box ``[lo, hi]`` as a candidate envelope. Not a proof of invariance."""
    if as_states:
        candidate: frozenset[Hashable] = frozenset((n,) for n in range(lo, hi + 1))
    else:
        candidate = frozenset(range(lo, hi + 1))
    return InvariantEnvelopeResult(
        candidate=candidate,
        status=AttackStatus.OBSERVATION,
        scope=SearchScope.BOUNDED,
        inclusion="candidate_interval",
        parameterization=f"[{lo},{hi}]",
    )


def reachable_from_ints(
    values: Sequence[int],
    seed: int = 0,
    *,
    complete: bool = True,
    as_states: bool = True,
) -> ExactReachabilityResult:
    """Wrap an already-computed integer reachable set."""
    if as_states:
        reached: frozenset[Hashable] = frozenset((int(n),) for n in values)
        start: Hashable = (int(seed),)
    else:
        reached = frozenset(int(n) for n in values)
        start = int(seed)
    status = AttackStatus.SUPPORTED if complete else AttackStatus.INCONCLUSIVE
    scope = SearchScope.EXACT if complete else SearchScope.BOUNDED
    kind = CertificateKind.EXACT_CLOSURE if complete else None
    return ExactReachabilityResult(
        seed=start,
        reachable=reached,
        complete=complete,
        status=status,
        scope=scope,
        certificate_kind=kind,
        statistics={"union_size": len(reached), "complete": complete},
    )
