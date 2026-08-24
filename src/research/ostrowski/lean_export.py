"""Link Ostrowski exact certificates to existing Lean names.

This catalog does not generate proofs, does not write ``formal/``,
and does not decide |L_0|.
"""

from __future__ import annotations

from research_engine.planner.orchestrator import PlannerReport
from research_engine.verification.targets import (
    TheoremTarget,
    attach_lean,
    targets_from_report,
)

STEP_FST_MODULE = "Problems.Ostrowski.NP.Residual"
STEP_FST_THEOREM = "Ostrowski.NP.step_fst_dvd_three"
HUB_MODULE = "Problems.Ostrowski.NP.Energy"
HUB_THEOREM = "Ostrowski.NP.hub_nonreset"
HUB_TRANSLATION = (-3, -1, 0)


def _is_np_mod3(target: TheoremTarget) -> bool:
    return any(
        isinstance(item, dict) and item.get("coordinate") == 0 and item.get("gcd") == 3
        for item in target.certificates
    )


def _is_hub(target: TheoremTarget) -> bool:
    return any(
        isinstance(item, dict) and item.get("translation") == HUB_TRANSLATION
        for item in target.certificates
    )


def link_ostrowski_targets(targets: tuple[TheoremTarget, ...]) -> tuple[TheoremTarget, ...]:
    """Attach already-proved NP lemmas. Unmatched targets stay unlinked."""
    out: list[TheoremTarget] = []
    for target in targets:
        if target.attack == "modular" and _is_np_mod3(target):
            out.append(
                attach_lean(
                    target,
                    module=STEP_FST_MODULE,
                    theorem=STEP_FST_THEOREM,
                    name="origin_mod3_invariant",
                )
            )
            continue
        if target.attack == "block" and _is_hub(target):
            out.append(
                attach_lean(
                    target,
                    module=HUB_MODULE,
                    theorem=HUB_THEOREM,
                    name="hub_nonreset",
                )
            )
            continue
        out.append(target)
    return tuple(out)


def export_plan_targets(report: PlannerReport) -> tuple[TheoremTarget, ...]:
    """Targets from ``plan_np``. PARKED |L_0| is a hypothesis, not a target."""
    return link_ostrowski_targets(targets_from_report(report, problem="ostrowski"))
