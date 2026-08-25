"""Machinery-inflation guard. Recommendations are guidance, never auto-implementation."""

from __future__ import annotations

from research_engine.memory.types import (
    ClusterDecision,
    EngineeringBacklogItem,
    EngineeringCandidate,
    EngineeringRecommendation,
    FailureCluster,
    ImportanceLevel,
)

PROMOTE_MIN_RECURRENCE = 3
PROMOTE_MIN_DIVERSITY = 2


def recommend_cluster(cluster: FailureCluster) -> EngineeringRecommendation:
    """A single failure never justifies a new attack."""

    generic = bool(cluster.suggested_future_abstraction) and cluster.mathematical_importance is ImportanceLevel.HIGH
    if (
        cluster.recurrence_count >= PROMOTE_MIN_RECURRENCE
        and cluster.target_diversity >= PROMOTE_MIN_DIVERSITY
        and cluster.mathematical_importance is ImportanceLevel.HIGH
        and generic
    ):
        return EngineeringRecommendation.PROMOTE_TO_NEXT_VERSION
    if cluster.recurrence_count >= 2 and cluster.target_diversity >= 2:
        if cluster.mathematical_importance is ImportanceLevel.HIGH:
            return EngineeringRecommendation.WATCH
        return EngineeringRecommendation.PARK
    if cluster.recurrence_count == 1:
        if cluster.current_decision is ClusterDecision.PARK:
            return EngineeringRecommendation.PARK
        return EngineeringRecommendation.IGNORE
    return EngineeringRecommendation.WATCH


def engineering_candidate(cluster: FailureCluster) -> EngineeringCandidate:
    recommendation = recommend_cluster(cluster)
    cost = "high" if cluster.mathematical_importance is ImportanceLevel.HIGH else "medium"
    return EngineeringCandidate(
        failure_cluster=cluster.id,
        recurrence_count=cluster.recurrence_count,
        target_diversity=cluster.target_diversity,
        mathematical_importance=cluster.mathematical_importance,
        expected_research_value=cluster.mathematical_importance,
        implementation_cost=cost,
        reusable_scope=cluster.suggested_future_abstraction or "target-specific",
        recommendation=recommendation,
        generic_abstraction=bool(cluster.suggested_future_abstraction),
        possible_generic_abstraction=cluster.suggested_future_abstraction,
        implementation_cost_estimate=cost,
        current_decision=recommendation,
        reason_not_implemented=_reason_not_implemented(recommendation),
    )


def _reason_not_implemented(recommendation: EngineeringRecommendation) -> str:
    if recommendation is EngineeringRecommendation.PROMOTE_TO_NEXT_VERSION:
        return "open mathematics may be the true bottleneck"
    if recommendation is EngineeringRecommendation.WATCH:
        return "insufficient recurrence or awaiting a generic abstraction"
    if recommendation is EngineeringRecommendation.PARK:
        return "insufficient recurrence"
    if recommendation is EngineeringRecommendation.IGNORE:
        return "single failure; do not implement"
    if recommendation is EngineeringRecommendation.PROTOTYPE_LATER:
        return "prototype deferred; not an implementation instruction"
    if recommendation is EngineeringRecommendation.PROTOTYPE:
        return "prototype deferred; not an implementation instruction"
    return "low expected yield"


def backlog_item(cluster: FailureCluster) -> EngineeringBacklogItem:
    recommendation = recommend_cluster(cluster)
    return EngineeringBacklogItem(
        failure_cluster=cluster.id,
        evidence="; ".join(cluster.member_ids),
        affected_targets=cluster.targets,
        proposed_abstraction=cluster.suggested_future_abstraction,
        expected_scope="generic" if cluster.suggested_future_abstraction else "target-specific",
        expected_research_value=cluster.mathematical_importance,
        implementation_complexity="high" if cluster.mathematical_importance is ImportanceLevel.HIGH else "medium",
        reason_not_implemented_yet=_reason_not_implemented(recommendation),
    )


def candidates_from_clusters(
    clusters: tuple[FailureCluster, ...] | list[FailureCluster],
) -> tuple[EngineeringCandidate, ...]:
    return tuple(engineering_candidate(item) for item in clusters)
