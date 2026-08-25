"""Pair-state BFS for exact behavioral separation.

Empty-word observations, legal-control menus, and deadlock are compared
before successor expansion. A depth cap is never exact equivalence.
"""

from __future__ import annotations

from collections import deque
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Any, Hashable

from research_engine.attacks.result import (
    AttackContext,
    AttackResult,
    AttackStatus,
    inapplicable,
    phase_key,
)
from research_engine.core.observation import ObservationCache, has_output, observe
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import CertificateKind, ClaimKind, SearchScope

Predictor = Callable[[Any, Any], tuple[str, Any] | None]


def _stable(items: Sequence[Any]) -> tuple[Any, ...]:
    try:
        return tuple(sorted(items))
    except TypeError:
        return tuple(sorted(items, key=repr))


@dataclass(frozen=True)
class SeparationResult:
    left: Any
    right: Any
    separated: bool
    witness_word: tuple[Hashable, ...] | None
    witness_length: int | None
    status: AttackStatus
    scope: SearchScope
    certificate_kind: CertificateKind | None
    controls: tuple[Hashable, ...]
    predictor: tuple[str, Any] | None = None
    legal_mismatch: bool = False

    def as_attack_result(self, name: str = "separation") -> AttackResult:
        if self.separated:
            claim = (
                f"states {self.left!r} and {self.right!r} are separated "
                f"by a word of length {self.witness_length}"
            )
            kind = CertificateKind.EXACT_COUNTEREXAMPLE
        elif self.scope is SearchScope.EXACT:
            claim = f"states {self.left!r} and {self.right!r} are exactly equivalent"
            kind = CertificateKind.EXACT_CLOSURE
        else:
            claim = (
                f"no separating word found up to the configured bound; "
                f"this is not exact equivalence of {self.left!r} and {self.right!r}"
            )
            kind = None
        return AttackResult(
            name=name,
            status=self.status,
            kind=ClaimKind.REACHABLE,
            scope=self.scope,
            claim=claim,
            evidence={
                "separated": self.separated,
                "witness_length": self.witness_length,
                "legal_mismatch": self.legal_mismatch,
                "predictor": self.predictor,
            },
            certificates=(self.witness_word,) if self.witness_word is not None else (),
            certificate_kind=kind if self.scope is SearchScope.EXACT else kind,
        )


def separate_states(
    spec: ProblemSpec,
    left: Any,
    right: Any,
    *,
    phase: Any | None = None,
    max_depth: int | None = None,
    max_pairs: int | None = None,
    predictor: Predictor | None = None,
) -> SeparationResult:
    """BFS over ``(s, t, phase)``. Stops on the first witness."""
    frozen_phase = phase if phase is not None else spec.initial_phase()
    src = spec.canonicalize(left)
    tgt = spec.canonicalize(right)
    start_controls = _stable(spec.legal_controls(src, frozen_phase))
    prediction = predictor(src, tgt) if predictor is not None else None
    if src == tgt:
        return SeparationResult(
            left=src,
            right=tgt,
            separated=False,
            witness_word=None,
            witness_length=0,
            status=AttackStatus.SUPPORTED,
            scope=SearchScope.EXACT,
            certificate_kind=CertificateKind.EXACT_CLOSURE,
            controls=start_controls,
            predictor=prediction,
        )
    cache = ObservationCache(spec) if has_output(spec) else None
    queue: deque[tuple[Any, Any, Any, tuple[Hashable, ...]]] = deque(
        [(src, tgt, frozen_phase, ())]
    )
    seen = {(src, tgt, phase_key(frozen_phase))}
    truncated = False

    def current_observation(state: Any, current_phase: Any) -> tuple[bool, bool, bool]:
        return (
            spec.is_accepting(state, current_phase),
            spec.is_terminal(state, current_phase),
            len(spec.legal_controls(state, current_phase)) == 0,
        )

    while queue:
        if max_pairs is not None and len(seen) > max_pairs:
            truncated = True
            break
        state_l, state_r, current_phase, word = queue.popleft()
        if max_depth is not None and len(word) > max_depth:
            truncated = True
            continue
        if current_observation(state_l, current_phase) != current_observation(state_r, current_phase):
            return SeparationResult(
                left=src,
                right=tgt,
                separated=True,
                witness_word=word,
                witness_length=len(word),
                status=AttackStatus.SUPPORTED,
                scope=SearchScope.EXACT,
                certificate_kind=CertificateKind.EXACT_COUNTEREXAMPLE,
                controls=start_controls,
                predictor=prediction,
                legal_mismatch=True,
            )
        legal_l = spec.legal_controls(state_l, current_phase)
        legal_r = spec.legal_controls(state_r, current_phase)
        set_l = frozenset(legal_l)
        set_r = frozenset(legal_r)
        if set_l != set_r:
            return SeparationResult(
                left=src,
                right=tgt,
                separated=True,
                witness_word=word,
                witness_length=len(word),
                status=AttackStatus.SUPPORTED,
                scope=SearchScope.EXACT,
                certificate_kind=CertificateKind.EXACT_COUNTEREXAMPLE,
                controls=start_controls,
                predictor=prediction,
                legal_mismatch=True,
            )
        if max_depth is not None and len(word) >= max_depth:
            truncated = True
            continue
        common = _stable(set_l)
        for control in common:
            if cache is not None:
                out_l = cache(state_l, control, current_phase)
                out_r = cache(state_r, control, current_phase)
            elif has_output(spec):
                out_l = observe(spec, state_l, control, current_phase)
                out_r = observe(spec, state_r, control, current_phase)
            else:
                out_l = out_r = None
            nxt_word = word + (control,)
            if out_l != out_r:
                return SeparationResult(
                    left=src,
                    right=tgt,
                    separated=True,
                    witness_word=nxt_word,
                    witness_length=len(nxt_word),
                    status=AttackStatus.SUPPORTED,
                    scope=SearchScope.EXACT,
                    certificate_kind=CertificateKind.EXACT_COUNTEREXAMPLE,
                    controls=start_controls,
                    predictor=prediction,
                )
            next_l = spec.canonicalize(spec.transition(state_l, control, current_phase))
            next_r = spec.canonicalize(spec.transition(state_r, control, current_phase))
            next_phase = spec.next_phase(current_phase, control)
            pair = (next_l, next_r, phase_key(next_phase))
            if pair in seen:
                continue
            seen.add(pair)
            queue.append((next_l, next_r, next_phase, nxt_word))

    if truncated:
        return SeparationResult(
            left=src,
            right=tgt,
            separated=False,
            witness_word=None,
            witness_length=None,
            status=AttackStatus.INCONCLUSIVE,
            scope=SearchScope.BOUNDED,
            certificate_kind=None,
            controls=start_controls,
            predictor=prediction,
        )
    return SeparationResult(
        left=src,
        right=tgt,
        separated=False,
        witness_word=None,
        witness_length=None,
        status=AttackStatus.SUPPORTED,
        scope=SearchScope.EXACT,
        certificate_kind=CertificateKind.EXACT_CLOSURE,
        controls=start_controls,
        predictor=prediction,
    )


class BehavioralSeparationAttack:
    name = "separation"

    def applicable(self, spec: ProblemSpec, context: AttackContext) -> bool:
        del spec
        return context.pair is not None

    def run(self, spec: ProblemSpec, context: AttackContext) -> AttackResult:
        if context.pair is None:
            return inapplicable(self.name, "separation needs AttackContext.pair", ClaimKind.REACHABLE)
        left, right = context.pair
        result = separate_states(
            spec,
            left,
            right,
            max_depth=context.max_separation_depth,
            max_pairs=context.max_states,
        )
        return result.as_attack_result(self.name)
