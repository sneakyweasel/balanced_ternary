"""Sample max |ℓ| is not an invariant and not an asymptotic bound."""

from __future__ import annotations

from research_engine.attacks.result import AttackContext, AttackResult, AttackStatus, inapplicable
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import ClaimKind, SearchScope, State
from research_engine.reachability.forward import forward_search


class FunctionalBoundAttack:
    name = "functional"

    def applicable(self, spec: ProblemSpec, context: AttackContext) -> bool:
        del spec
        return context.functional is not None

    def run(self, spec: ProblemSpec, context: AttackContext) -> AttackResult:
        form = context.functional
        if form is None:
            return inapplicable(self.name, "functional attack needs LinearFunctional", ClaimKind.LIVE_SLICE)
        census = forward_search(
            spec,
            live_only=context.live_only,
            max_steps=context.max_steps,
        )
        start_layer = census.layer_at(spec.initial_phase())
        sample = start_layer or census.live_union or census.union
        bound = form.observed_bound(sample)
        leaks: list[tuple[State, object, State, int]] = []
        for state in sample:
            src = spec.canonicalize(state)
            phase = spec.initial_phase()
            for control in spec.legal_controls(src, phase):
                nxt = spec.canonicalize(spec.transition(src, control, phase))
                nxt_phase = spec.next_phase(phase, control)
                if context.live_only and not spec.is_terminal(nxt, nxt_phase):
                    continue
                value = form(nxt)
                if abs(value) > bound:
                    leaks.append((src, control, nxt, value))
        evidence = {
            "sample_size": len(sample),
            "observed_bound": bound,
            "union_size": len(census.union),
            "horizon": census.horizon,
        }
        if leaks:
            return AttackResult(
                name=self.name,
                status=AttackStatus.REFUTED,
                kind=ClaimKind.LIVE_SLICE,
                scope=SearchScope.BOUNDED,
                claim="|ℓ| on the start layer is not nonincreasing under one live step",
                evidence=evidence,
                counterexamples=tuple(leaks[:8]),
                recommended_next_attacks=("reconnaissance", "modular"),
            )
        return AttackResult(
            name=self.name,
            status=AttackStatus.OBSERVATION,
            kind=ClaimKind.LIVE_SLICE,
            scope=SearchScope.BOUNDED,
            claim=(
                f"max |ℓ| on the start-layer sample is {bound}; "
                "this is not an invariant and not an asymptotic bound"
            ),
            evidence=evidence,
            recommended_next_attacks=("affine", "block"),
        )
