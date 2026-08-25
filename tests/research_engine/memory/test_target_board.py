"""v2.2 target board: portfolio, loot, clusters, EV ranking, hygiene, non-goals."""

from __future__ import annotations

from research.engine_memory.problem import PROBLEM as MEMORY_PROBLEM
from research.open_problems import get_problem
from research.target_board.problem import PROBLEM
from research_engine.diagnosis.corpus import ResearchCorpus
from research_engine.diagnosis.selection import score_candidate
from research_engine.diagnosis.types import CandidateSketch
from research_engine.memory.board import assemble_board, recommend_campaign_order
from research_engine.memory.hygiene import leak_hits
from research_engine.memory.named_clusters import named_failure_clusters
from research_engine.memory.retrieval import assert_not_injected
from research_engine.memory.seed_records import historical_experiments
from research_engine.memory.seed_targets import board_targets
from research_engine.memory.store import ResearchMemory
from research_engine.memory.types import (
    EngineeringRecommendation,
    GreyLootStatus,
    TargetPool,
)
from research_engine.planner.orchestrator import DEFAULT_ATTACK_ORDER

_FORBIDDEN = (
    "Skolem",
    "Bacik",
    "p-adic",
    "Collatz",
    "Lychrel",
    "Catalan",
    "Reachability Conjecture",
)


def _memory() -> ResearchMemory:
    return ResearchMemory(historical_experiments())


def _corpus(memory: ResearchMemory) -> ResearchCorpus:
    return ResearchCorpus(tuple(item.diagnosis for item in memory.experiments))


def test_problem_descriptor():
    assert get_problem("target_board") is PROBLEM
    assert PROBLEM.docs == ("docs/problems/research_target_board.md",)
    assert PROBLEM.status == "EXPLORATORY"
    assert get_problem("engine_memory") is MEMORY_PROBLEM


def test_attack_architecture_remains_frozen():
    assert DEFAULT_ATTACK_ORDER[-1] == "symmetry"
    assert DEFAULT_ATTACK_ORDER.index("vector_affine") < DEFAULT_ATTACK_ORDER.index("matrix_word_invariant")


def test_board_has_three_pools_and_enough_candidates():
    targets = board_targets()
    assert len(targets) >= 15
    pools = {item.pool for item in targets}
    assert pools == {TargetPool.CALIBRATION, TargetPool.FRONTIER, TargetPool.WILDCARD}
    frontier = [item for item in targets if item.pool is TargetPool.FRONTIER]
    assert len(frontier) >= 5
    names = [item.name for item in targets]
    assert len(names) == len(set(names))
    for item in targets:
        assert item.canonical_definition
        assert item.open_question
        assert item.expected_research_value.reason
        assert item.novelty_potential.reason
        assert item.failure_learning_value.reason
        assert item.engine_fit.reason
        assert item.structural_distance.reason
        assert item.experimental_cost.reason


def test_frontier_targets_have_prior_art_and_blind_packets():
    for item in board_targets():
        if item.pool is not TargetPool.FRONTIER:
            continue
        assert item.prior_art is not None
        assert item.prior_art.open_question
        assert item.prior_art.last_checked == "2026-08-25"
        assert item.prior_art.literature_ids
        assert item.blind_packet is not None
        payload = repr(item.blind_packet.attack_payload())
        for token in _FORBIDDEN:
            assert token not in payload
        hits = leak_hits(item.blind_packet.allowed_definition, _FORBIDDEN)
        assert hits == ()


def test_grey_loot_covers_historical_lessons():
    memory = _memory()
    loot = memory.grey_loot()
    lessons = {item.reusable_lesson for item in loot if item.reusable_lesson}
    joined = " | ".join(lessons)
    for needle in (
        "(P)-band",
        "scalar digit-fold",
        "different attractor",
        "expanding perturbation",
        "latent affine",
        "maximal divisibility",
        "reasoning language",
        "infinite classes",
        "magnitude domination",
        "multi-dimensional control",
        "lattice/gcd",
        "global reachability remains",
        "quantifier",
        "sign-first",
        "no new mathematics",
        "outside the affine-control language",
        "infinite-time zero reachability",
        "identifier-aware",
    ):
        assert needle in joined
    statuses = {item.status for item in loot}
    assert GreyLootStatus.SATURATED in statuses
    assert GreyLootStatus.PARKED in statuses or GreyLootStatus.ACTIVE in statuses


def test_named_clusters_group_by_meaning():
    memory = _memory()
    clusters = {item.id: item for item in named_failure_clusters(memory)}
    assert "global_reachability" in clusters
    glob = clusters["global_reachability"]
    assert glob.target_diversity >= 3
    assert "companion_shift_order6" in glob.targets
    assert "companion_obs_order10" in glob.targets
    assert "rplus" in glob.targets
    assert "bb5_map" in glob.targets
    assert "sum_strip" not in glob.targets
    quant = clusters["branching_quantifier"]
    assert "sum_strip" in quant.targets
    assert clusters["non_affine_arithmetic"].current_decision.value in {"PARK", "WATCH", "RECORD"}
    assert clusters["census_domain"].targets
    assert "syracuse" in clusters["prior_art_saturation"].targets or "rplus" in clusters["prior_art_saturation"].targets


def test_engineering_candidates_do_not_auto_implement():
    memory = _memory()
    board = assemble_board(memory, _corpus(memory))
    recs = {item.failure_cluster: item for item in board.engineering_candidates}
    glob = recs["global_reachability"]
    assert glob.recommendation is EngineeringRecommendation.PROMOTE_TO_NEXT_VERSION
    assert "guidance" in glob.reason_not_implemented or "bottleneck" in glob.reason_not_implemented
    assert recs["census_domain"].recommendation is not EngineeringRecommendation.PROMOTE_TO_NEXT_VERSION
    assert recs["non_affine_arithmetic"].recommendation is not EngineeringRecommendation.PROMOTE_TO_NEXT_VERSION
    assert recs["branching_quantifier"].recommendation is not EngineeringRecommendation.PROMOTE_TO_NEXT_VERSION


def test_score_without_memory_matches_legacy_formula():
    corpus = ResearchCorpus()
    sketch = CandidateSketch(name="toy", experimental_cost=2.0, claimed_capabilities=("finite_closure",))
    report = score_candidate(sketch, corpus)
    assert report.value == (1.0 * 1.0 * 1.0 * 1.0) / 2.0
    assert report.failure_learning_value == 1.0
    assert "failure_learning" not in report.explanation


def test_expected_research_value_is_auditable():
    memory = _memory()
    corpus = _corpus(memory)
    board = assemble_board(memory, corpus)
    for item in board.targets:
        assert "ExpectedResearchValue=" in item.expected_research_value.reason
        sketch = item.as_sketch()
        report = score_candidate(sketch, corpus, memory=memory)
        assert item.expected_research_value.value == report.value


def test_campaign_order_protocol_and_research_loop_pick_is_computed():
    memory = _memory()
    corpus = _corpus(memory)
    targets = board_targets()
    order = recommend_campaign_order(targets, corpus, memory)
    assert order.calibration == ("slc_decrement", "euclidean_remainder", "aliquot_seed_12")
    assert 5 <= len(order.frontier) <= 8
    assert 3 <= len(order.wildcards) <= 5
    assert "aliquot_276" not in order.wildcards
    assert order.research_loop_pick
    used = set(order.calibration) | set(order.frontier) | set(order.wildcards)
    assert order.research_loop_pick not in used
    leftovers = [item for item in assemble_board(memory, corpus).targets if item.name not in used]
    best_value = max(item.expected_research_value.value for item in leftovers)
    winners = [
        item.name
        for item in leftovers
        if item.expected_research_value.value == best_value
    ]
    assert order.research_loop_pick in winners
    assert "known → frontier" in " ".join(order.explanations)


def test_blind_packets_do_not_absorb_grey_loot():
    memory = _memory()
    board = assemble_board(memory, _corpus(memory))
    loot = memory.grey_loot()
    for item in board.targets:
        if item.blind_packet is None:
            continue
        assert_not_injected(item.blind_packet, loot)
        assert "scout" not in item.blind_packet.as_dict()
        assert "literature" not in item.blind_packet.extra


def test_yield_separates_representation_from_mathematics():
    memory = _memory()
    bb5 = memory.get("bb5_map")
    assert bb5.representation_novelty.value == "HIGH"
    assert bb5.mathematical_novelty.value == "NONE"
    rows = memory.yield_corpus()
    assert any(row["experiment_id"] == "bb5_map" for row in rows)


def test_json_roundtrip_of_assembled_board(tmp_path):
    memory = _memory()
    board = assemble_board(memory, _corpus(memory))
    path = tmp_path / "board.json"
    path.write_text(__import__("json").dumps(board.as_dict(), indent=2), encoding="utf-8")
    loaded = ResearchMemory.load_board(path)
    assert len(loaded.targets) == len(board.targets)
    assert loaded.campaign_order is not None
    assert loaded.campaign_order.calibration == board.campaign_order.calibration
