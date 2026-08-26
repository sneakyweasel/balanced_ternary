"""Frozen-engine campaign on accelerated 7x+1 class obstruction."""

from __future__ import annotations

from pathlib import Path

from research.literature import get_reference
from research.mx_plus_r.spec import mx_plus_r_step
from research.mx_plus_r_7x1_class_obstruction.discovery import evidence_state, falsify_claims
from research.mx_plus_r_7x1_class_obstruction.lean_export import LEAN_MODULE, THEOREMS
from research.mx_plus_r_7x1_class_obstruction.planner import plan_strategy
from research.mx_plus_r_7x1_class_obstruction.problem import PROBLEM
from research.mx_plus_r_7x1_class_obstruction.runner import run_campaign
from research.mx_plus_r_7x1_class_obstruction.spec import map_spec
from research.open_problems import get_problem
from research_engine.memory.seed_targets import board_targets
from research_engine.memory.types import FailureClass
from research_engine.planner.orchestrator import DEFAULT_ATTACK_ORDER
from research_engine.strategy import ResearchGoal

ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "src" / "research" / "mx_plus_r_7x1_class_obstruction"
FORBIDDEN_SPEC = (
    "Crandall",
    "Collatz",
    "residue partition",
    "subgroup",
    "covering",
    "divergent",
)


def _source_lines(name: str) -> str:
    return (SRC / name).read_text(encoding="utf-8")


def test_adapter_sources_are_blind_and_do_not_import_scout():
    for name in ("spec.py", "adapter.py", "planner.py"):
        text = _source_lines(name)
        for line in text.splitlines():
            stripped = line.strip()
            if "mx_plus_r_7x1_class_obstruction.scout" in stripped:
                raise AssertionError(f"{name} imports scout")
        for token in FORBIDDEN_SPEC:
            assert token not in text, f"{name} contains forbidden token {token!r}"


def test_blind_packet_matches_the_stored_board_definition():
    packet = next(
        item.blind_packet
        for item in board_targets()
        if item.name == "mx_plus_r_7x1_class_obstruction"
    )
    spec = map_spec()
    assert spec.name == packet.spec_name
    assert spec.dimension == packet.dimension
    assert spec.start == 3
    assert spec.start_remaining == packet.max_steps
    assert spec.state_cap == packet.max_states
    assert mx_plus_r_step(3, 7, 1) == 11
    assert mx_plus_r_step(1, 7, 1) == 1


def test_problem_descriptor_and_prior_art():
    assert get_problem("mx_plus_r_7x1_class_obstruction") is PROBLEM
    assert PROBLEM.docs == ("docs/problems/mx_plus_r_7x1_class_obstruction.md",)
    assert get_reference("crandall-1978-3x+1")["year"] == 1978
    assert get_reference("chamberland-2003-3x+1-survey")["year"] == 2003


def test_attack_architecture_remains_frozen():
    assert DEFAULT_ATTACK_ORDER[-1] == "symmetry"
    assert "control_obstruction" in DEFAULT_ATTACK_ORDER
    assert DEFAULT_ATTACK_ORDER.index("control_obstruction") == DEFAULT_ATTACK_ORDER.index(
        "control_word"
    ) + 1


def test_post_run_image_class_and_counterexamples():
    spec = map_spec()
    report = evidence_state(spec)
    assert report["hits_one_horizon_16"] is False
    assert report["hits_one_horizon_32"] is False
    assert report["t_one"] == 1
    assert report["image_residues_mod7"] == (1, 2, 4)
    assert report["image_divisible_by_seven"] is False
    assert report["valuation_determines_image_class"] is True
    assert report["seventy_three"] == (73, 3, 1)
    assert report["multiple_of_seven_preimage"] == (299593, 0, 1)
    assert report["contrast_3x1_mod3"] == (1, 2)
    assert report["contrast_5x1_mod5"] == (1, 2, 3, 4)
    flag = falsify_claims(spec)
    assert flag["start_reaches_one_on_bound"]["status"] == "REFUTED"
    assert flag["out_class_cannot_reach_one"]["status"] == "REFUTED"
    assert flag["multiples_of_seven_cannot_reach_one"]["status"] == "REFUTED"
    assert flag["image_in_two_subgroup"]["status"] == "EXACT"
    assert flag["same_obstruction_as_3x1"]["status"] == "REFUTED"


def test_blind_strategy_selects_census_obstruction_without_memory():
    report = plan_strategy(goal=ResearchGoal.CYCLE_EXCLUSION, memory=None)
    assert report.plan.chain.id == "census_obstruction"
    names = [item.name for item in report.results]
    assert names == ["piecewise_affine", "parameter_domain", "control_word", "control_obstruction"]
    family = dict(report.results[0].evidence.get("family") or {})
    assert family.get("p") == 7
    assert family.get("r") == 1
    assert family.get("base") == 2


def test_lean_identities_are_known_and_sorry_free():
    path = ROOT / "formal" / "Problems" / "Engine" / "MxPlusR.lean"
    text = path.read_text(encoding="utf-8")
    assert "sorry" not in text
    assert "admit" not in text
    assert LEAN_MODULE.replace(".", "/") in "formal/Problems/Engine/MxPlusR.lean"
    for name in THEOREMS:
        assert name in text


def test_campaign_runs_unmodified_loop():
    _, report = run_campaign()
    flagship = report.by_target("mx_plus_r_7_1")
    assert report.planner_unchanged_with_memory is True
    assert report.strategy_chain == "census_obstruction"
    assert flagship.census_kind == "PARAMETERIZED_CENSUS"
    assert flagship.extra["yield"]["evidence"]["image_residues_mod7"] == (1, 2, 4)
    assert flagship.extra["yield"]["evidence"]["seventy_three"] == (73, 3, 1)
    assert flagship.extra["yield"]["engineering_changes"] == 0
    assert "control_obstruction" in flagship.extra["attack_table"]
    assert report.next_target_overridden is False
    assert report.next_target_name
    assert report.next_target_name != "mx_plus_r_7x1_class_obstruction"
    assert FailureClass.GLOBAL_REASONING.value not in flagship.extra["failure_classes"]
    assert report.memory is not None
    stored = report.memory.get("mx_plus_r_7_1")
    assert stored.finalized
    assert stored.grey_loot
