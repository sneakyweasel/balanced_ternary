"""Semantic failure clusters. Grouped by mathematical meaning, not target names."""

from __future__ import annotations

from research_engine.memory.policy import recommend_cluster, _reason_not_implemented
from research_engine.memory.types import (
    ClusterDecision,
    EngineeringCandidate,
    EngineeringRecommendation,
    FailureClass,
    ImportanceLevel,
    NamedFailureCluster,
)


def named_failure_clusters(memory: object) -> tuple[NamedFailureCluster, ...]:
    auto = tuple(memory.clusters())
    by_class: dict[str, list] = {}
    for cluster in auto:
        by_class.setdefault(cluster.key[0], []).append(cluster)

    high_novelty = [
        item.target
        for item in memory.experiments
        if item.representation_novelty.value == "HIGH" and item.mathematical_novelty.value == "NONE"
    ]

    def _members(classes: tuple[str, ...], bottlenecks: tuple[str, ...] = ()) -> tuple:
        found = []
        for cluster in auto:
            if cluster.key[0] not in classes:
                continue
            if bottlenecks and cluster.key[2] not in bottlenecks:
                continue
            found.append(cluster)
        return tuple(found)

    global_members = _members((FailureClass.GLOBAL_REASONING.value,), ("finite_to_infinite_certificate",))
    branch_members = _members((FailureClass.QUANTIFIER.value,), ("overlapping_existential_branches",))
    affine_members = _members((FailureClass.REPRESENTATION.value,), ("outside_affine_valuation_control",))
    census_members = _members((FailureClass.DOMAIN_INFERENCE.value,), ("sign_first_region_inference",))

    def _named(
        cid: str,
        title: str,
        members: tuple,
        extra_targets: tuple[str, ...] = (),
        importance: ImportanceLevel = ImportanceLevel.MEDIUM,
        decision: ClusterDecision = ClusterDecision.RECORD,
        workarounds: tuple[str, ...] = (),
        abstraction: str = "",
        questions: tuple[str, ...] = (),
    ) -> NamedFailureCluster:
        targets = tuple(sorted({*(t for m in members for t in m.targets), *extra_targets}))
        recurrence = sum(m.recurrence_count for m in members) if members else len(extra_targets)
        return NamedFailureCluster(
            id=cid,
            title=title,
            member_cluster_ids=tuple(m.id for m in members),
            targets=targets,
            recurrence_count=max(recurrence, len(targets)),
            target_diversity=len(targets),
            mathematical_importance=importance,
            existing_workarounds=workarounds,
            current_decision=decision,
            possible_generic_abstraction=abstraction,
            research_questions=questions,
        )

    return (
        _named(
            "global_reachability",
            "Global-reachability cluster",
            global_members,
            extra_targets=(),
            importance=ImportanceLevel.HIGH,
            decision=ClusterDecision.WATCH,
            workarounds=("finite-window reachability; Lean for recovered identities only",),
            abstraction="an intermediate notion between finite reachability and universal reachability",
            questions=(
                "Can the existing finite-state/lattice abstractions identify a reusable "
                "intermediate notion between finite reachability and universal reachability?",
            ),
        ),
        _named(
            "branching_quantifier",
            "Branching/quantifier cluster",
            branch_members,
            importance=ImportanceLevel.MEDIUM,
            decision=ClusterDecision.PARK,
            workarounds=("explicit quantifier probes; skip the deterministic control stack",),
            abstraction="a quantifier-aware consumption of overlapping nondeterministic branches",
            questions=(
                "Can overlapping nondeterministic branches be consumed without a new "
                "deterministic control language?",
            ),
        ),
        _named(
            "non_affine_arithmetic",
            "Non-affine arithmetic cluster",
            affine_members,
            extra_targets=("home_prime_49",),
            importance=ImportanceLevel.HIGH,
            decision=ClusterDecision.PARK,
            workarounds=("finite known orbits; refuse a piecewise-affine cover",),
            abstraction="a representation outside affine/valuation control, or an explicit PARK",
            questions=(
                "Is the representation mismatch a true language boundary, or a missing "
                "exact encoding of an already-known arithmetic map?",
            ),
        ),
        _named(
            "census_domain",
            "Census-domain cluster",
            census_members,
            extra_targets=("negation",),
            importance=ImportanceLevel.MEDIUM,
            decision=ClusterDecision.PARK,
            workarounds=("post-run 2-cycle observation; do not implement a census fix",),
            abstraction="region inference that does not truncate globally valid affine laws",
        ),
        _named(
            "prior_art_saturation",
            "Prior-art saturation cluster",
            (),
            extra_targets=tuple(sorted(set(high_novelty) & {"syracuse", "rplus", "bb5_map"})),
            importance=ImportanceLevel.LOW,
            decision=ClusterDecision.RECORD,
            workarounds=("bill as KNOWN_REDISCOVERY; keep representation novelty separate",),
            questions=("Which new target is not a residue-controlled affine rediscovery?",),
        ),
    )


def engineering_from_named(
    clusters: tuple[NamedFailureCluster, ...] | list[NamedFailureCluster],
    *,
    auto_clusters: tuple = (),
) -> tuple[EngineeringCandidate, ...]:
    """Named-cluster engineering records. A single failure never auto-promotes."""

    auto_by_id = {item.id: item for item in auto_clusters}
    items: list[EngineeringCandidate] = []
    for cluster in clusters:
        if cluster.id == "global_reachability":
            recommendation = EngineeringRecommendation.PROMOTE_TO_NEXT_VERSION
            reason = (
                "recurrence across Skolem, R+, and BB-5; guidance only — open mathematics "
                "may be the true bottleneck; not an implementation instruction"
            )
        elif cluster.id == "prior_art_saturation":
            recommendation = EngineeringRecommendation.IGNORE
            reason = "competence already demonstrated; no new attack"
        elif cluster.recurrence_count <= 1 and cluster.target_diversity <= 1:
            recommendation = EngineeringRecommendation.IGNORE
            reason = "single failure; do not implement"
        elif cluster.current_decision is ClusterDecision.PARK:
            recommendation = EngineeringRecommendation.PARK
            reason = "parked mathematical limitation; no target-specific machinery"
        else:
            members = tuple(auto_by_id[cid] for cid in cluster.member_cluster_ids if cid in auto_by_id)
            recommendation = (
                recommend_cluster(members[0]) if members else EngineeringRecommendation.WATCH
            )
            reason = _reason_not_implemented(recommendation)
        cost = "high" if cluster.mathematical_importance is ImportanceLevel.HIGH else "medium"
        items.append(
            EngineeringCandidate(
                failure_cluster=cluster.id,
                recurrence_count=cluster.recurrence_count,
                target_diversity=cluster.target_diversity,
                mathematical_importance=cluster.mathematical_importance,
                expected_research_value=cluster.mathematical_importance,
                implementation_cost=cost,
                reusable_scope=cluster.possible_generic_abstraction or "target-specific",
                recommendation=recommendation,
                generic_abstraction=bool(cluster.possible_generic_abstraction),
                possible_generic_abstraction=cluster.possible_generic_abstraction,
                implementation_cost_estimate=cost,
                current_decision=recommendation,
                reason_not_implemented=reason,
            )
        )
    return tuple(items)
