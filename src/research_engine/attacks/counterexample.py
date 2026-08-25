"""Small counterexample-first attacks. Not a theorem-proving DSL."""

from __future__ import annotations

from research_engine.attacks.affine import AffineInvariantAttack
from research_engine.attacks.closure import ExhaustiveClosureAttack
from research_engine.attacks.result import AttackContext, AttackResult, AttackStatus, inapplicable
from research_engine.attacks.separation import BehavioralSeparationAttack
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import CertificateKind, ClaimKind, SearchScope, State


class InvariantLeakAttack(AffineInvariantAttack):
    """Search ``s in S`` with ``F(s,u)`` outside ``S``."""

    name = "invariant_leak"


class ClosureLeakAttack:
    """Search ``s in R`` with ``F(s,u)`` outside ``R`` after exact closure."""

    name = "closure_leak"

    def applicable(self, spec: ProblemSpec, context: AttackContext) -> bool:
        del spec, context
        return True

    def run(self, spec: ProblemSpec, context: AttackContext) -> AttackResult:
        closure = ExhaustiveClosureAttack().run(spec, context)
        if not closure.evidence.get("complete"):
            return AttackResult(
                name=self.name,
                status=AttackStatus.INCONCLUSIVE,
                kind=ClaimKind.REACHABLE,
                scope=SearchScope.BOUNDED,
                claim="closure leak test needs exact reachable set",
                evidence={"complete": False},
            )
        reached = frozenset(closure.evidence.get("union", ()))
        phase = spec.initial_phase()
        leaks: list[tuple[State, object, State]] = []
        for state in reached:
            src = spec.canonicalize(state)
            for control in spec.legal_controls(src, phase):
                nxt = spec.canonicalize(spec.transition(src, control, phase))
                if nxt not in reached:
                    leaks.append((src, control, nxt))
        if leaks:
            return AttackResult(
                name=self.name,
                status=AttackStatus.REFUTED,
                kind=ClaimKind.REACHABLE,
                scope=SearchScope.EXACT,
                claim="reachable set is not closed",
                evidence={"leak_count": len(leaks), "union_size": len(reached)},
                counterexamples=tuple(leaks[:8]),
                certificate_kind=CertificateKind.EXACT_COUNTEREXAMPLE,
            )
        return AttackResult(
            name=self.name,
            status=AttackStatus.SUPPORTED,
            kind=ClaimKind.REACHABLE,
            scope=SearchScope.EXACT,
            claim="reachable set is closed under legal one-step images",
            evidence={"leak_count": 0, "union_size": len(reached)},
            certificate_kind=CertificateKind.EXACT_CLOSURE,
        )


class DescentLeakAttack:
    """Search ``V(F(s,u)) >= V(s)`` on the candidate or reachable sample."""

    name = "descent_leak"

    def applicable(self, spec: ProblemSpec, context: AttackContext) -> bool:
        del spec
        return context.descent_potential is not None or context.functional is not None

    def run(self, spec: ProblemSpec, context: AttackContext) -> AttackResult:
        potential = context.descent_potential
        if potential is None and context.functional is not None:
            form = context.functional

            def _abs_functional(state: State, _form=form) -> int:
                return abs(_form(state))

            potential = _abs_functional
        if potential is None:
            return inapplicable(self.name, "descent leak needs a potential", ClaimKind.LIVE_SLICE)
        region = context.candidate_region
        if region is None:
            region = frozenset((spec.canonicalize(spec.initial_state),))
        phase = spec.initial_phase()
        leaks: list[tuple[State, object, State, int, int]] = []
        for state in region:
            src = spec.canonicalize(state)
            before = potential(src)
            for control in spec.legal_controls(src, phase):
                nxt = spec.canonicalize(spec.transition(src, control, phase))
                after = potential(nxt)
                if after >= before:
                    leaks.append((src, control, nxt, before, after))
        if leaks:
            return AttackResult(
                name=self.name,
                status=AttackStatus.REFUTED,
                kind=ClaimKind.LIVE_SLICE,
                scope=SearchScope.BOUNDED,
                claim="potential does not strictly descend on the sample",
                evidence={"leak_count": len(leaks), "sample_size": len(region)},
                counterexamples=tuple(leaks[:8]),
                certificate_kind=CertificateKind.EXACT_COUNTEREXAMPLE,
            )
        return AttackResult(
            name=self.name,
            status=AttackStatus.OBSERVATION,
            kind=ClaimKind.LIVE_SLICE,
            scope=SearchScope.BOUNDED,
            claim="potential strictly descends on the tested sample; this is not a Lyapunov theorem",
            evidence={"leak_count": 0, "sample_size": len(region)},
            certificate_kind=CertificateKind.BOUNDED_RECONNAISSANCE,
        )


class EquivalenceSeparationAttack(BehavioralSeparationAttack):
    """Separating-word attack on a claimed equivalent pair."""

    name = "equivalence_separation"
