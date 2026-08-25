"""Score the target board with the existing ExpectedResearchValue formula.

EV(T) = (NoveltyPotential × StructuralDistance × CapabilityFit × FailureLearningValue)
        / ExperimentalCost
maps onto score_candidate: (novelty × distance × capability_gap × failure_learning) / cost.
"""

from __future__ import annotations

from research_engine.diagnosis.corpus import ResearchCorpus
from research_engine.diagnosis.selection import score_candidate
from research_engine.memory.named_clusters import engineering_from_named, named_failure_clusters
from research_engine.memory.types import (
    CampaignOrder,
    TargetBoard,
    TargetPool,
)

CALIBRATION_SEQUENCE = ("slc_decrement", "euclidean_remainder", "aliquot_seed_12")
WILDCARD_SEQUENCE = ("juggler_sequence", "reverse_and_add_base3", "home_prime_49")


def score_targets(targets, corpus: ResearchCorpus, memory: object | None = None):
    scored = []
    for target in targets:
        report = score_candidate(target.as_sketch(), corpus, memory=memory)
        reason = (
            f"{report.explanation}; qualitative novelty={target.novelty_potential.reason}; "
            f"distance={target.structural_distance.reason}; fit={target.engine_fit.reason}; "
            f"failure_learning={target.failure_learning_value.reason}; "
            f"cost={target.experimental_cost.reason}"
        )
        scored.append(target.with_expected_value(report.value, reason))
    return tuple(scored)


def recommend_campaign_order(targets, corpus: ResearchCorpus, memory: object | None = None) -> CampaignOrder:
    scored = score_targets(targets, corpus, memory)
    present = {item.name for item in scored}
    calibration = tuple(name for name in CALIBRATION_SEQUENCE if name in present)

    frontier_pool = [item for item in scored if item.pool is TargetPool.FRONTIER]
    frontier_ranked = sorted(
        frontier_pool, key=lambda item: (-item.expected_research_value.value, item.name)
    )
    frontier = tuple(item.name for item in frontier_ranked[:6])

    wildcard_names = [name for name in WILDCARD_SEQUENCE if name in present]
    for item in scored:
        if item.pool is not TargetPool.WILDCARD:
            continue
        if item.name in wildcard_names or item.name == "aliquot_276":
            continue
        if item.name == "cyclic_tag_bit" and item.failure_learning_value.value < 0.4:
            continue
        if len(wildcard_names) >= 5:
            break
        wildcard_names.append(item.name)
    wildcards = tuple(wildcard_names[:5])

    used = set(calibration) | set(frontier) | set(wildcards)
    leftovers = [item for item in scored if item.name not in used]
    leftovers.sort(key=lambda item: (-item.expected_research_value.value, item.name))
    pick = leftovers[0].name if leftovers else ""

    explanations = (
        "Protocol is known → frontier → structurally distant → ResearchLoop choice, not raw EV sort.",
        f"Calibration (fixed): {', '.join(calibration)}.",
        f"Frontier (memory-aware EV, top {len(frontier)} of Pool B): {', '.join(frontier)}.",
        f"Wildcards (protocol, aliquot_276 kept as historical baseline): {', '.join(wildcards)}.",
        f"ResearchLoop pick (max EV among leftovers): {pick or '(none)'}.",
    )
    return CampaignOrder(
        calibration=calibration,
        frontier=frontier,
        wildcards=wildcards,
        research_loop_pick=pick,
        explanations=explanations,
    )


def assemble_board(memory: object, corpus: ResearchCorpus | None = None) -> TargetBoard:
    from research_engine.memory.seed_targets import board_targets

    session = corpus if corpus is not None else ResearchCorpus(
        tuple(item.diagnosis for item in memory.experiments)
    )
    targets = score_targets(board_targets(), session, memory)
    clusters = named_failure_clusters(memory)
    engineering = engineering_from_named(clusters, auto_clusters=memory.clusters())
    order = recommend_campaign_order(targets, session, memory)
    return TargetBoard(
        targets=targets,
        named_clusters=clusters,
        engineering_candidates=engineering,
        campaign_order=order,
    )


def yield_corpus(memory: object) -> tuple[dict, ...]:
    rows = []
    for item in memory.experiments:
        rows.append(
            {
                "experiment_id": item.experiment_id,
                "target": item.target,
                "representation_novelty": item.representation_novelty.value,
                "mathematical_novelty": item.mathematical_novelty.value,
                "mathematical_yield": item.mathematical_yield.as_dict(),
            }
        )
    return tuple(rows)
