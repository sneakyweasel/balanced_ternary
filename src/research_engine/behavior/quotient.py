"""Exact behavioral quotient of a finite reachable Mealy system."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Hashable

from research_engine.attacks.closure import ExhaustiveClosureAttack
from research_engine.attacks.result import AttackContext, AttackResult, AttackStatus, inapplicable
from research_engine.behavior.mealy import mealy_partition
from research_engine.core.observation import ObservationCache, has_output, observe
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import CertificateKind, ClaimKind, SearchScope


def _stable(items: Sequence[Any]) -> tuple[Any, ...]:
    try:
        return tuple(sorted(items))
    except TypeError:
        return tuple(sorted(items, key=repr))


@dataclass(frozen=True)
class BehavioralQuotientResult:
    original_state_count: int
    reachable_state_count: int
    quotient_count: int
    classes: tuple[frozenset[Hashable], ...]
    exactness: SearchScope
    certificate_kind: CertificateKind | None
    alphabet: tuple[Hashable, ...]
    transition_quotient: Mapping[tuple[int, Hashable], int] = field(default_factory=dict)
    observation_quotient: Mapping[tuple[int, Hashable], Hashable] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "transition_quotient", MappingProxyType(dict(self.transition_quotient)))
        object.__setattr__(self, "observation_quotient", MappingProxyType(dict(self.observation_quotient)))


def quotient_from_states(
    spec: ProblemSpec,
    states: Sequence[Any],
    *,
    complete: bool,
    phase: Any | None = None,
) -> BehavioralQuotientResult:
    frozen_phase = phase if phase is not None else spec.initial_phase()
    start = spec.canonicalize(spec.initial_state)
    alphabet = _stable(spec.legal_controls(start, frozen_phase))
    canonical = tuple(spec.canonicalize(state) for state in states)
    cache = ObservationCache(spec) if has_output(spec) else None

    def step(state: Any, control: Any) -> tuple[Any, Hashable]:
        nxt = spec.canonicalize(spec.transition(state, control, frozen_phase))
        if cache is not None:
            out = cache(state, control, frozen_phase)
        else:
            out = observe(spec, state, control, frozen_phase)
        return nxt, out

    parts = mealy_partition(canonical, alphabet, step)
    block_of: dict[Any, int] = {}
    for index, block in enumerate(parts):
        for state in block:
            block_of[state] = index
    transitions: dict[tuple[int, Hashable], int] = {}
    observations: dict[tuple[int, Hashable], Hashable] = {}
    for index, block in enumerate(parts):
        representative = next(iter(block))
        for control in alphabet:
            nxt, out = step(representative, control)
            transitions[(index, control)] = block_of[nxt]
            observations[(index, control)] = out
    exactness = SearchScope.EXACT if complete else SearchScope.BOUNDED
    kind = CertificateKind.EXACT_CLOSURE if complete else None
    return BehavioralQuotientResult(
        original_state_count=len(canonical),
        reachable_state_count=len(canonical),
        quotient_count=len(parts),
        classes=parts,
        exactness=exactness,
        certificate_kind=kind,
        alphabet=alphabet,
        transition_quotient=transitions,
        observation_quotient=observations,
    )


class BehavioralQuotientAttack:
    name = "quotient"

    def applicable(self, spec: ProblemSpec, context: AttackContext) -> bool:
        del context
        return has_output(spec)

    def run(self, spec: ProblemSpec, context: AttackContext) -> AttackResult:
        if not has_output(spec):
            return inapplicable(self.name, "quotient needs an output map", ClaimKind.REACHABLE)
        closure = ExhaustiveClosureAttack().run(spec, context)
        union = closure.evidence.get("union")
        if not closure.evidence.get("complete") or union is None:
            return AttackResult(
                name=self.name,
                status=AttackStatus.INCONCLUSIVE,
                kind=ClaimKind.REACHABLE,
                scope=SearchScope.BOUNDED,
                claim="quotient requires an exact finite reachable set",
                evidence={"complete": False, "union_size": closure.evidence.get("union_size")},
            )
        result = quotient_from_states(spec, tuple(union), complete=True)
        return AttackResult(
            name=self.name,
            status=AttackStatus.SUPPORTED,
            kind=ClaimKind.REACHABLE,
            scope=SearchScope.EXACT,
            claim=(
                f"exact Mealy quotient has {result.quotient_count} classes "
                f"from {result.reachable_state_count} reachable states"
            ),
            evidence={
                "original_state_count": result.original_state_count,
                "reachable_state_count": result.reachable_state_count,
                "quotient_count": result.quotient_count,
                "alphabet_size": len(result.alphabet),
            },
            certificates=(result,),
            certificate_kind=CertificateKind.EXACT_CLOSURE,
        )
