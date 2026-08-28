"""Frozen-engine campaign on the 5x-4 one-variable strip."""

from __future__ import annotations

from pathlib import Path

from research.linear_constraint_loops.spec import rplus_images
from research.literature import get_reference
from research.open_problems import get_problem
from research.weak_collatz_floor_5x4_rplus.discovery import evidence_state, falsify_claims
from research.weak_collatz_floor_5x4_rplus.lean_export import LEAN_MODULE, THEOREMS
from research.weak_collatz_floor_5x4_rplus.planner import plan_strategy
from research.weak_collatz_floor_5x4_rplus.problem import PROBLEM
from research.weak_collatz_floor_5x4_rplus.runner import run_campaign
from research.weak_collatz_floor_5x4_rplus.spec import map_spec, strip_images
from research_engine.memory.seed_targets import board_targets
from research_engine.memory.types import FailureClass
from research_engine.planner.orchestrator import DEFAULT_ATTACK_ORDER
from research_engine.strategy import ResearchGoal

ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "src" / "research" / "weak_collatz_floor_5x4_rplus"
FORBIDDEN_SPEC = (
    "Carelli",
    "Collatz",
    "Reachability",
    "Matthews",
    "residue partition",
    "named conjectures",
)


def _source_lines(name: str) -> str:
    return (SRC / name).read_text(encoding="utf-8")


def test_adapter_sources_are_blind_and_do_not_import_scout():
    for name in ("spec.py", "adapter.py", "planner.py"):
        text = _source_lines(name)
        for line in text.splitlines():
            stripped = line.strip()
            if "weak_collatz_floor_5x4_rplus.scout" in stripped:
                raise AssertionError(f"{name} imports scout")
        for token in FORBIDDEN_SPEC:
            assert token not in text, f"{name} contains forbidden token {token!r}"


def test_blind_packet_matches_the_stored_board_definition():
    packet = next(
        item.blind_packet
        for item in board_targets()
        if item.name == "weak_collatz_floor_5x4_rplus"
    )
    spec = map_spec()
    assert spec.name == packet.spec_name
    assert spec.dimension == packet.dimension
    assert spec.start == 5
    assert spec.start_remaining == packet.max_steps
    assert spec.state_cap == packet.max_states
    assert strip_images(5) == (6,)
    assert strip_images(8) == (9,)
    assert strip_images(1) == ()
    assert rplus_images(8) == (10,)


def test_problem_descriptor_and_prior_art():
    assert get_problem("weak_collatz_floor_5x4_rplus") is PROBLEM
    assert PROBLEM.docs == ("docs/problems/weak_collatz_floor_5x4_rplus.md",)
    assert get_reference("carelli-2026-loop-termination")["year"] == 2026
    assert get_reference("matthews-watts-1984-generalization-hasse")["year"] == 1984
    assert get_reference("ben-amram-genaim-ouaknine-worrell-2025-termination-survey")["year"] == 2025


def test_attack_architecture_remains_frozen():
    assert DEFAULT_ATTACK_ORDER[-1] == "symmetry"
    assert "control_obstruction" in DEFAULT_ATTACK_ORDER
    assert DEFAULT_ATTACK_ORDER.index("control_obstruction") == DEFAULT_ATTACK_ORDER.index(
        "control_word"
    ) + 1


def test_post_run_uniqueness_and_counterexamples():
    spec = map_spec()
    report = evidence_state(spec)
    assert report["unique_on_window"] is True
    assert report["undefined_in_domain"] == ()
    assert report["path_undefined"] is False
    assert report["path32_undefined"] is False
    assert report["path_grows"] is True
    assert report["path"][0] == 5
    assert report["fixed_points_2_3_4"] == (2, 3, 4)
    assert report["maps_differ_at_8"] == (9, 10)
    assert report["rplus_can_be_undefined"] is True
    assert report["remainders_are_1_to_4"] is True
    flag = falsify_claims(spec)
    assert flag["every_orbit_loses_successor"]["status"] == "REFUTED"
    assert flag["this_is_the_four_thirds_loop"]["status"] == "REFUTED"
    assert flag["finite_halt_is_a_map_theorem"]["status"] == "REFUTED"
    assert flag["image_class_excludes_basin"]["status"] == "REFUTED"
    assert flag["unique_successor"]["status"] == "EXACT"
    assert flag["rplus_always_defined"]["status"] == "REFUTED"
    assert flag["horizon_changes_uniqueness"]["status"] == "REFUTED"


def test_blind_strategy_selects_census_obstruction_without_memory():
    report = plan_strategy(goal=ResearchGoal.CYCLE_EXCLUSION, memory=None)
    assert report.plan.chain.id == "census_obstruction"
    names = [item.name for item in report.results]
    assert names == ["piecewise_affine", "parameter_domain", "control_word", "control_obstruction"]
    assert report.results[0].evidence.get("census_kind") == "FINITE_CENSUS"
    branches = tuple(report.results[0].evidence.get("branches") or ())
    assert len(branches) == 4
    assert {int(item["p"]) for item in branches} == {5}
    assert {int(item["q"]) for item in branches} == {4}


def test_lean_identities_are_known_and_sorry_free():
    path = ROOT / "formal" / "Problems" / "Engine" / "LinearConstraintLoops.lean"
    text = path.read_text(encoding="utf-8")
    assert "sorry" not in text
    assert "admit" not in text
    assert LEAN_MODULE.replace(".", "/") in "formal/Problems/Engine/LinearConstraintLoops.lean"
    for name in THEOREMS:
        assert name in text


def test_campaign_runs_unmodified_loop():
    _, report = run_campaign()
    flagship = report.by_target("floor_5x4_strip")
    assert report.planner_unchanged_with_memory is True
    assert report.strategy_chain == "census_obstruction"
    assert flagship.census_kind == "FINITE_CENSUS"
    assert flagship.extra.get("branch_count") == 4
    assert flagship.extra["yield"]["evidence"]["unique_on_window"] is True
    assert flagship.extra["yield"]["evidence"]["fixed_points_2_3_4"] == (2, 3, 4)
    assert flagship.extra["yield"]["engineering_changes"] == 0
    assert "control_obstruction" in flagship.extra["attack_table"]
    assert report.next_target_overridden is False
    if report.next_target_name:
        assert report.next_target_name != "weak_collatz_floor_5x4_rplus"
    assert FailureClass.GLOBAL_REASONING.value not in flagship.extra["failure_classes"]
    assert report.memory is not None
    stored = report.memory.get("floor_5x4_strip")
    assert stored.finalized
    assert stored.grey_loot
