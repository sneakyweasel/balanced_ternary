"""Reverse basin of seeds. C(seed) is not the live set."""

from __future__ import annotations

from research_engine.attacks.result import AttackContext, AttackResult, AttackStatus, inapplicable
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import ClaimKind, SearchScope
from research_engine.reachability.reverse import reverse_closure


class ReverseGeometryAttack:
    name = "reverse"

    def applicable(self, spec: ProblemSpec, context: AttackContext) -> bool:
        del spec
        return context.reverse_preimage is not None and context.reverse_seeds is not None

    def run(self, spec: ProblemSpec, context: AttackContext) -> AttackResult:
        del spec
        if context.reverse_preimage is None or context.reverse_seeds is None:
            return inapplicable(
                self.name,
                "reverse attack needs reverse_seeds and reverse_preimage; C(seed) is not LIVE",
                ClaimKind.CO_REACHABLE,
            )
        result = reverse_closure(
            context.reverse_seeds,
            context.reverse_preimage,
            max_depth=context.reverse_max_depth,
        )
        claim = (
            f"co-reachability of {len(context.reverse_seeds)} seed(s), "
            f"union size {len(result.union)}, scope {result.scope.value}; "
            "this is not the adder live set"
        )
        status = (
            AttackStatus.OBSERVATION
            if result.scope is SearchScope.BOUNDED
            else AttackStatus.SUPPORTED
        )
        return AttackResult(
            name=self.name,
            status=status,
            kind=ClaimKind.CO_REACHABLE,
            scope=result.scope,
            claim=claim,
            evidence={
                "union_size": len(result.union),
                "horizon": result.horizon,
                "complete": result.complete,
                "seed_count": len(context.reverse_seeds),
            },
            recommended_next_attacks=("block", "functional"),
        )
