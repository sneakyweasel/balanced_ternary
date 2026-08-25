"""One-step candidate-region check. A leak-free sample is not an invariant theorem."""

from __future__ import annotations

from research_engine.attacks.result import AttackContext, AttackResult, AttackStatus, inapplicable
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import CertificateKind, ClaimKind, SearchScope, State


class AffineInvariantAttack:
    name = "affine"

    def applicable(self, spec: ProblemSpec, context: AttackContext) -> bool:
        del spec
        return context.candidate_region is not None

    def run(self, spec: ProblemSpec, context: AttackContext) -> AttackResult:
        region = context.candidate_region
        if region is None:
            return inapplicable(self.name, "affine attack needs candidate_region", ClaimKind.LIVE_SLICE)
        phases = context.phases if context.phases is not None else (spec.initial_phase(),)
        leaks: list[tuple[State, object, object, State]] = []
        checked = 0
        for phase in phases:
            for state in region:
                src = spec.canonicalize(state)
                for control in spec.legal_controls(src, phase):
                    nxt = spec.canonicalize(spec.transition(src, control, phase))
                    nxt_phase = spec.next_phase(phase, control)
                    checked += 1
                    if not spec.is_terminal(nxt, nxt_phase):
                        continue
                    if nxt not in region:
                        leaks.append((src, control, phase, nxt))
        if leaks:
            return AttackResult(
                name=self.name,
                status=AttackStatus.REFUTED,
                kind=ClaimKind.LIVE_SLICE,
                scope=SearchScope.BOUNDED,
                claim="candidate region leaks a live image at the tested phases",
                evidence={"region_size": len(region), "checked_edges": checked, "leak_count": len(leaks)},
                counterexamples=tuple(leaks[:8]),
                recommended_next_attacks=("reconnaissance", "reverse"),
                certificate_kind=CertificateKind.EXACT_COUNTEREXAMPLE,
            )
        return AttackResult(
            name=self.name,
            status=AttackStatus.OBSERVATION,
            kind=ClaimKind.LIVE_SLICE,
            scope=SearchScope.BOUNDED,
            claim=(
                "no live one-step leak of the candidate region at the tested phases; "
                "this is not an invariant theorem"
            ),
            evidence={"region_size": len(region), "checked_edges": checked, "leak_count": 0},
            recommended_next_attacks=("functional", "modular"),
        )
