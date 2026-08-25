"""Finite-horizon census. Completeness of a DAG is not infinitude."""

from __future__ import annotations

from research_engine.attacks.result import AttackContext, AttackResult, AttackStatus, phase_key
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import CertificateKind, ClaimKind, SearchScope
from research_engine.reachability.forward import forward_search


class ReconnaissanceAttack:
    name = "reconnaissance"

    def applicable(self, spec: ProblemSpec, context: AttackContext) -> bool:
        del spec, context
        return True

    def run(self, spec: ProblemSpec, context: AttackContext) -> AttackResult:
        result = forward_search(
            spec,
            live_only=context.live_only,
            max_steps=context.max_steps,
        )
        layer_sizes = {
            phase_key(phase): len(states) for phase, states in result.layer.items()
        }
        kind = result.kind
        claim = (
            f"finite-horizon {kind.value} census at horizon {result.horizon}; "
            "union is not L_n and terminal_image is not live infinitude"
        )
        return AttackResult(
            name=self.name,
            status=AttackStatus.OBSERVATION,
            kind=kind,
            scope=SearchScope.BOUNDED,
            claim=claim,
            evidence={
                "horizon": result.horizon,
                "complete": result.complete,
                "layer_sizes": layer_sizes,
                "union_size": len(result.union),
                "live_union_size": len(result.live_union),
                "terminal_image_size": len(result.terminal_image),
                "rejected_images": result.rejected_images,
                "live_start": result.live_start,
            },
            recommended_next_attacks=("modular", "functional", "affine"),
            certificate_kind=CertificateKind.BOUNDED_RECONNAISSANCE,
        )
