"""Frozen-engine campaign on a declared order-5 companion window."""

from __future__ import annotations

from pathlib import Path

from research.literature import get_reference
from research.open_problems import get_problem
from research.skolem_lrs.spec import next_window, observation, skip_attacks_for_dimension
from research.skolem_order5_unconditional.discovery import evidence_state, falsify_claims
from research.skolem_order5_unconditional.lean_export import LEAN_MODULE, LEAN_PATH, THEOREMS
from research.skolem_order5_unconditional.planner import plan_strategy
from research.skolem_order5_unconditional.problem import PROBLEM
from research.skolem_order5_unconditional.runner import CURRENT, LIVE_ID, run_campaign
from research.skolem_order5_unconditional.spec import LAST_ROW, WINDOW, map_spec
from research_engine.memory.hygiene import leak_hits
from research_engine.memory.seed_targets import board_targets
from research_engine.memory.types import FailureClass
from research_engine.planner.orchestrator import DEFAULT_ATTACK_ORDER
from research_engine.strategy import ResearchGoal

ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "src" / "research" / "skolem_order5_unconditional"
FORBIDDEN_SPEC = (
    "interpolant",
    "known congruence of zeros",
    "named conjectures",
    "open-problem",
    "Skolem Problem",
    "p-adic",
)


def _source_lines(name: str) -> str:
    return (SRC / name).read_text(encoding="utf-8")


def test_adapter_sources_are_blind_and_do_not_import_scout():
    for name in ("spec.py", "adapter.py", "planner.py"):
        text = _source_lines(name)
        for line in text.splitlines():
            stripped = line.strip()
            if "skolem_order5_unconditional.scout" in stripped:
                raise AssertionError(f"{name} imports scout")
        hits = leak_hits(text, FORBIDDEN_SPEC)
        assert hits == (), f"{name} leaked {hits}"


def test_blind_packet_matches_the_stored_board_definition():
    packet = next(item.blind_packet for item in board_targets() if item.name == CURRENT)
    spec = map_spec()
    assert spec.name == packet.spec_name
    assert spec.dimension == packet.dimension
    assert spec.window == WINDOW
    assert spec.last_row == LAST_ROW
    assert spec.start_remaining == packet.max_steps
    assert spec.state_cap == packet.max_states
    assert observation(WINDOW) == -30
    assert next_window(WINDOW, LAST_ROW)[0] == WINDOW[1]
    assert skip_attacks_for_dimension(5) == ("vector_affine", "matrix_word_invariant")
    assert skip_attacks_for_dimension(5) == skip_attacks_for_dimension(6)


def test_problem_descriptor_and_prior_art():
    assert get_problem(CURRENT) is PROBLEM
    assert PROBLEM.docs == ("docs/problems/skolem_order5_unconditional.md",)
    assert get_reference("lipton-et-al-2022-skolem-conjecture")["year"] == 2022
    assert get_reference("kenison-et-al-2025-order-4-skolem")["year"] == 2025
    assert get_reference("bacik-et-al-2026-skolem-positivity-survey")["year"] == 2026


def test_attack_architecture_remains_frozen():
    assert DEFAULT_ATTACK_ORDER[-1] == "symmetry"
    assert "vector_affine" in DEFAULT_ATTACK_ORDER
    assert "matrix_word_invariant" in DEFAULT_ATTACK_ORDER


def test_post_run_zero_witness_and_same_skip_as_order6():
    spec = map_spec()
    report = evidence_state(spec)
    assert report["zero_at"] == 2
    assert report["status"] == "ZERO_WITNESS"
    assert report["dimension"] == 5
    assert report["matrix_word_skipped"] is True
    assert report["vector_census_skipped"] is True
    assert report["same_skip_as_dimension_6"] is True
    assert report["lattice_congruence"] is False
    assert report["uniqueness_from_prefix"] is False
    assert report["unconditional_decision"] is False
    flag = falsify_claims(spec)
    assert flag["never_vanishes"]["status"] == "REFUTED"
    assert flag["census_runs_at_dimension_5"]["status"] == "REFUTED"
    assert flag["this_is_the_order6_flagship"]["status"] == "REFUTED"
    assert flag["this_is_the_order2_competence_check"]["status"] == "REFUTED"
    assert flag["zero_witness_is_unconditional_decision"]["status"] == "REFUTED"
    assert flag["prefix_gives_uniqueness"]["status"] == "REFUTED"
    assert flag["same_skip_is_a_new_cluster"]["status"] == "REFUTED"
    assert flag["companion_is_the_yield"]["status"] == "REFUTED"


def test_blind_strategy_selects_vector_matrix_without_memory():
    report = plan_strategy(goal=ResearchGoal.ORIGIN_AVOIDANCE, memory=None)
    assert report.plan.chain.id == "vector_matrix"
    assert [item.name for item in report.results] == []


def test_lean_identities_are_known_and_sorry_free():
    path = ROOT / LEAN_PATH
    text = path.read_text(encoding="utf-8")
    assert "sorry" not in text
    assert "admit" not in text
    assert LEAN_MODULE.replace(".", "/") in LEAN_PATH.replace("\\", "/")
    for name in THEOREMS:
        assert name in text


def test_campaign_runs_unmodified_loop():
    _, report = run_campaign()
    flagship = report.by_target("companion_shift_order5")
    assert report.planner_unchanged_with_memory is True
    assert report.strategy_chain == "vector_matrix"
    assert flagship.extra["vector_affine_status"] == "COMPUTATION_EXHAUSTED"
    assert flagship.extra["matrix_word_status"] == "COMPUTATION_EXHAUSTED"
    assert flagship.extra["yield"]["evidence"]["zero_at"] == 2
    assert flagship.extra["yield"]["engineering_changes"] == 0
    assert report.next_target_overridden is False
    assert report.next_target_name
    assert report.next_target_name != CURRENT
    classes = flagship.extra["failure_classes"]
    assert FailureClass.COMPUTATIONAL.value in classes
    assert FailureClass.GLOBAL_REASONING.value not in classes
    assert report.memory is not None
    stored = report.memory.get(LIVE_ID)
    assert stored.finalized
    assert stored.grey_loot
