"""Grey-loot extraction from planner evidence. Items need not be theorems."""

from __future__ import annotations

from research_engine.attacks.result import AttackStatus
from research_engine.memory.types import (
    GreyLoot,
    GreyLootKind,
    LootEvidence,
    FailureClass,
)
from research_engine.planner.orchestrator import PlannerReport


def extract_grey_loot(
    report: PlannerReport,
    *,
    experiment_id: str,
    target: str,
) -> tuple[GreyLoot, ...]:
    items: list[GreyLoot] = []
    index = 0
    for result in report.results:
        kind = result.name
        evidence_map = dict(result.evidence)
        census_kind = str(evidence_map.get("census_kind") or "")
        if result.counterexamples:
            for witness in result.counterexamples[:8]:
                index += 1
                items.append(
                    GreyLoot(
                        id=f"{experiment_id}:cex:{index}",
                        kind=GreyLootKind.COUNTEREXAMPLE,
                        statement=f"{kind} counterexample {witness!r}",
                        evidence=LootEvidence.REFUTED if result.status is AttackStatus.REFUTED else LootEvidence.OBSERVED,
                        experiment_id=experiment_id,
                        target=target,
                        payload={"attack": kind, "witness": repr(witness)},
                    )
                )
        if result.status is AttackStatus.REFUTED:
            index += 1
            items.append(
                GreyLoot(
                    id=f"{experiment_id}:failed:{index}",
                    kind=GreyLootKind.FAILED_INVARIANT,
                    statement=result.claim,
                    evidence=LootEvidence.REFUTED,
                    experiment_id=experiment_id,
                    target=target,
                    payload={"attack": kind},
                )
            )
        if census_kind in {"UNRESOLVED", "UNCERTAIN"}:
            index += 1
            items.append(
                GreyLoot(
                    id=f"{experiment_id}:census:{index}",
                    kind=GreyLootKind.REPRESENTATION_MISMATCH,
                    statement=f"{kind} census {census_kind}",
                    evidence=LootEvidence.OBSERVED,
                    experiment_id=experiment_id,
                    target=target,
                    payload={"attack": kind, "census_kind": census_kind},
                )
            )
        if census_kind in {"PARAMETERIZED_CENSUS", "FINITE_CENSUS"}:
            index += 1
            items.append(
                GreyLoot(
                    id=f"{experiment_id}:pattern:{index}",
                    kind=GreyLootKind.LATENT_CONTROL_PATTERN,
                    statement=result.claim,
                    evidence=LootEvidence.SUPPORTED
                    if result.status is AttackStatus.SUPPORTED
                    else LootEvidence.OBSERVED,
                    experiment_id=experiment_id,
                    target=target,
                    payload={"attack": kind, "census_kind": census_kind},
                )
            )
        if evidence_map.get("unresolved"):
            index += 1
            items.append(
                GreyLoot(
                    id=f"{experiment_id}:unresolved:{index}",
                    kind=GreyLootKind.CANDIDATE_INVARIANT,
                    statement=f"unresolved census cells {evidence_map.get('unresolved')!r}",
                    evidence=LootEvidence.OBSERVED,
                    experiment_id=experiment_id,
                    target=target,
                    payload={"attack": kind, "unresolved": repr(evidence_map.get("unresolved"))},
                )
            )
        if kind == "parameter_domain" and result.status in {
            AttackStatus.INCONCLUSIVE,
            AttackStatus.INAPPLICABLE,
        }:
            index += 1
            items.append(
                GreyLoot(
                    id=f"{experiment_id}:domain:{index}",
                    kind=GreyLootKind.FAILED_DOMAIN_PREDICATE,
                    statement=result.claim,
                    evidence=LootEvidence.OBSERVED,
                    experiment_id=experiment_id,
                    target=target,
                    payload={"attack": kind},
                )
            )
        if "COMPUTATION_EXHAUSTED" in result.status.value or "COMPUTATION_EXHAUSTED" in result.claim:
            index += 1
            items.append(
                GreyLoot(
                    id=f"{experiment_id}:budget:{index}",
                    kind=GreyLootKind.COMPUTATIONAL_BOTTLENECK,
                    statement=result.claim,
                    evidence=LootEvidence.FINITE_RANGE,
                    experiment_id=experiment_id,
                    target=target,
                    failure_class=FailureClass.COMPUTATIONAL,
                    bottleneck="finite_budget_exhausted",
                    payload={"attack": kind},
                )
            )
        status_text = evidence_map.get("status")
        if status_text == "COMPUTATION_EXHAUSTED":
            index += 1
            items.append(
                GreyLoot(
                    id=f"{experiment_id}:budget-ev:{index}",
                    kind=GreyLootKind.COMPUTATIONAL_BOTTLENECK,
                    statement=f"{kind} COMPUTATION_EXHAUSTED",
                    evidence=LootEvidence.FINITE_RANGE,
                    experiment_id=experiment_id,
                    target=target,
                    failure_class=FailureClass.COMPUTATIONAL,
                    bottleneck="finite_budget_exhausted",
                    payload={"attack": kind},
                )
            )

    for skip in report.skipped:
        if "inapplicable" in skip.reason.lower():
            index += 1
            items.append(
                GreyLoot(
                    id=f"{experiment_id}:skip:{index}",
                    kind=GreyLootKind.USEFUL_NEGATIVE_RESULT,
                    statement=f"{skip.attack} inapplicable: {skip.reason}",
                    evidence=LootEvidence.OBSERVED,
                    experiment_id=experiment_id,
                    target=target,
                    payload={"attack": skip.attack, "reason": skip.reason},
                )
            )
    return tuple(items)
