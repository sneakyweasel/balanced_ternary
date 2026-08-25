"""Failure clustering by mathematical signature, never by target name."""

from __future__ import annotations

from collections import defaultdict

from research_engine.memory.types import (
    ClusterDecision,
    FailureClass,
    FailureCluster,
    FailureRecord,
    ImportanceLevel,
    ResearchQuestion,
)

_IMPORTANCE_RANK = {
    ImportanceLevel.LOW: 0,
    ImportanceLevel.MEDIUM: 1,
    ImportanceLevel.HIGH: 2,
}

_ABSTRACTIONS: dict[str, str] = {
    "finite_to_infinite_certificate": (
        "an intermediate notion between finite reachability and universal reachability"
    ),
    "overlapping_existential_branches": (
        "a quantifier-aware consumption of overlapping nondeterministic branches"
    ),
    "outside_affine_valuation_control": (
        "a representation outside affine/valuation control, or an explicit PARK"
    ),
    "sign_first_region_inference": (
        "region inference that does not truncate globally valid affine laws"
    ),
    "finite_budget_exhausted": (
        "budgeted exact search with an explicit computational — not mathematical — status"
    ),
    "saturated_finite_contracting_regime": (
        "no new abstraction; saturated scalar fold"
    ),
    "identifier_token_false_positive": (
        "identifier-aware literature-leak matching"
    ),
}

_QUESTIONS: dict[str, str] = {
    "finite_to_infinite_certificate": (
        "Can the existing finite-state/lattice abstractions identify a reusable "
        "intermediate notion between finite reachability and universal reachability?"
    ),
    "overlapping_existential_branches": (
        "Can overlapping nondeterministic branches be consumed without a new "
        "deterministic control language?"
    ),
    "outside_affine_valuation_control": (
        "Is the representation mismatch a true language boundary, or a missing "
        "exact encoding of an already-known arithmetic map?"
    ),
}


def cluster_failures(
    failures: tuple[FailureRecord, ...] | list[FailureRecord],
    *,
    semantic_class_of: dict[str, str] | None = None,
) -> tuple[FailureCluster, ...]:
    groups: dict[tuple[str, str, str, str], list[FailureRecord]] = defaultdict(list)
    for item in failures:
        groups[item.cluster_key()].append(item)

    clusters: list[FailureCluster] = []
    for key, members in sorted(groups.items(), key=lambda pair: pair[0]):
        targets = tuple(sorted({item.target for item in members}))
        classes = tuple(
            sorted(
                {
                    (semantic_class_of or {}).get(item.experiment_id)
                    or (semantic_class_of or {}).get(item.target)
                    or item.representation_status
                    for item in members
                }
            )
        )
        importance = max(
            (item.research_value for item in members),
            key=lambda level: _IMPORTANCE_RANK[level],
        )
        bottleneck = key[2]
        abstraction = _ABSTRACTIONS.get(bottleneck, "")
        diversity = len(targets)
        recurrence = len(members)
        if recurrence == 1:
            decision = ClusterDecision.PARK
        elif importance is ImportanceLevel.HIGH and diversity >= 2:
            decision = ClusterDecision.WATCH
        else:
            decision = ClusterDecision.RECORD
        cluster_id = "|".join(key)
        questions: tuple[ResearchQuestion, ...] = ()
        template = _QUESTIONS.get(bottleneck)
        if template:
            questions = (
                ResearchQuestion(
                    id=f"{cluster_id}:q1",
                    cluster_id=cluster_id,
                    statement=template,
                    failure_class=FailureClass(key[0]),
                ),
            )
        clusters.append(
            FailureCluster(
                id=cluster_id,
                key=key,
                member_ids=tuple(item.id for item in members),
                targets=targets,
                recurrence_count=recurrence,
                target_diversity=diversity,
                semantic_classes=classes,
                mathematical_importance=importance,
                reproducibility="seed" if all(item.reproducibility == "seed" for item in members) else "mixed",
                suggested_future_abstraction=abstraction,
                current_decision=decision,
                research_questions=questions,
            )
        )
    return tuple(clusters)
