"""Frozen-engine campaign on the three-branch mod-3 avoider class."""

from __future__ import annotations

from pathlib import Path

from research.literature import get_reference
from research.matthews_prize_mod3_avoider.discovery import evidence_state, falsify_claims
from research.matthews_prize_mod3_avoider.lean_export import LEAN_MODULE, THEOREMS
from research.matthews_prize_mod3_avoider.planner import plan_strategy
from research.matthews_prize_mod3_avoider.problem import PROBLEM
from research.matthews_prize_mod3_avoider.runner import run_campaign
from research.matthews_prize_mod3_avoider.spec import SECOND_START, map_images, map_spec
from research.open_problems import get_problem
from research_engine.memory.seed_targets import board_targets
from research_engine.memory.types import FailureClass
from research_engine.planner.orchestrator import DEFAULT_ATTACK_ORDER
from research_engine.strategy import ResearchGoal

ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "src" / "research" / "matthews_prize_mod3_avoider"
FORBIDDEN_SPEC = (
    "Matthews",
    "Collatz",
    "prize claims",
    "known cycle theorem",
    "named conjectures",
    "open-problem",
)


def _source_lines(name: str) -> str:
    return (SRC / name).read_text(encoding="utf-8")


def test_adapter_sources_are_blind_and_do_not_import_scout():
    for name in ("spec.py", "adapter.py", "planner.py"):
        text = _source_lines(name)
        for line in text.splitlines():
            stripped = line.strip()
            if "matthews_prize_mod3_avoider.scout" in stripped:
                raise AssertionError(f"{name} imports scout")
        for token in FORBIDDEN_SPEC:
            assert token not in text, f"{name} contains forbidden token {token!r}"


def test_blind_packet_matches_the_stored_board_definition():
    packet = next(
        item.blind_packet
        for item in board_targets()
        if item.name == "matthews_prize_mod3_avoider"
    )
    spec = map_spec()
    assert spec.name == packet.spec_name
    assert spec.dimension == packet.dimension
    assert spec.start == 1
    assert spec.start_remaining == packet.max_steps
    assert spec.state_cap == packet.max_states
    assert map_images(1) == (3,)
    assert map_images(SECOND_START) == (1,)
    assert map_images(3) == (6,)
    assert map_images(0) == (0,)


def test_problem_descriptor_and_prior_art():
    assert get_problem("matthews_prize_mod3_avoider") is PROBLEM
    assert PROBLEM.docs == ("docs/problems/matthews_prize_mod3_avoider.md",)
    assert get_reference("matthews-watts-1984-generalization-hasse")["year"] == 1984


def test_attack_architecture_remains_frozen():
    assert DEFAULT_ATTACK_ORDER[-1] == "symmetry"
    assert "control_obstruction" in DEFAULT_ATTACK_ORDER
    assert DEFAULT_ATTACK_ORDER.index("control_obstruction") == DEFAULT_ATTACK_ORDER.index(
        "control_word"
    ) + 1


def test_post_run_seeds_cycles_and_counterexamples():
    spec = map_spec()
    report = evidence_state(spec)
    assert report["seed1_hits_zero_mod_three"] is True
    assert report["seed5_hits_zero_mod_three"] is True
    assert report["zero_class_closed"] is True
    assert report["units_forward_invariant"] is False
    assert report["t_neg_one"] == -1
    assert report["t_neg_two"] == -4
    assert report["t_neg_four"] == -2
    assert report["t_three"] == 6
    assert -28 in report["horizon_avoiders"]
    assert -10 in report["horizon_avoiders"]
    assert report["window_avoiders_reach_known_cycles"] is True
    flag = falsify_claims(spec)
    assert flag["packet_seeds_are_avoiders"]["status"] == "REFUTED"
    assert flag["units_cannot_reach_zero_mod_three"]["status"] == "REFUTED"
    assert flag["branches_are_the_yield"]["status"] == "REFUTED"
    assert flag["finite_cycle_visit_is_a_map_theorem"]["status"] == "REFUTED"
    assert flag["this_is_the_four_thirds_or_bb5_map"]["status"] == "REFUTED"
    assert flag["zero_class_invariant"]["status"] == "EXACT"
    assert flag["known_cycles"]["status"] == "EXACT"
    assert flag["horizon_avoiders_are_only_known_cycles"]["status"] == "REFUTED"


def test_blind_strategy_selects_census_obstruction_without_memory():
    report = plan_strategy(goal=ResearchGoal.CYCLE_EXCLUSION, memory=None)
    assert report.plan.chain.id == "census_obstruction"
    names = [item.name for item in report.results]
    assert names == ["piecewise_affine", "parameter_domain", "control_word", "control_obstruction"]
    assert report.results[0].evidence.get("census_kind") == "FINITE_CENSUS"
    branches = tuple(report.results[0].evidence.get("branches") or ())
    assert len(branches) == 3
    pairs = {(int(item["p"]), int(item["q"])) for item in branches}
    assert pairs == {(2, 1), (7, 3), (1, 3)}


def test_lean_identities_are_known_and_sorry_free():
    path = ROOT / "formal" / "Problems" / "Engine" / "MatthewsMod3.lean"
    text = path.read_text(encoding="utf-8")
    assert "sorry" not in text
    assert "admit" not in text
    assert LEAN_MODULE.replace(".", "/") in "formal/Problems/Engine/MatthewsMod3.lean"
    for name in THEOREMS:
        assert name in text


def test_campaign_runs_unmodified_loop():
    _, report = run_campaign()
    flagship = report.by_target("mod3_three_branch")
    assert report.planner_unchanged_with_memory is True
    assert report.strategy_chain == "census_obstruction"
    assert flagship.census_kind == "FINITE_CENSUS"
    assert flagship.extra.get("branch_count") == 3
    assert flagship.extra["yield"]["evidence"]["seed1_hits_zero_mod_three"] is True
    assert flagship.extra["yield"]["evidence"]["t_neg_one"] == -1
    assert flagship.extra["yield"]["engineering_changes"] == 0
    assert "control_obstruction" in flagship.extra["attack_table"]
    assert report.next_target_overridden is False
    if report.next_target_name:
        assert report.next_target_name != "matthews_prize_mod3_avoider"
    assert FailureClass.GLOBAL_REASONING.value not in flagship.extra["failure_classes"]
    assert report.memory is not None
    stored = report.memory.get("mod3_three_branch")
    assert stored.finalized
    assert stored.grey_loot
