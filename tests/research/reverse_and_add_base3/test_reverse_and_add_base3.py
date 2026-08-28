"""Frozen-engine campaign on the reverse-plus-add map."""

from __future__ import annotations

from pathlib import Path

from research.open_problems import get_problem
from research.reverse_and_add_base3.discovery import evidence_state, falsify_claims
from research.reverse_and_add_base3.lean_export import LEAN_MODULE, LEAN_PATH, THEOREMS
from research.reverse_and_add_base3.planner import plan_strategy
from research.reverse_and_add_base3.problem import PROBLEM
from research.reverse_and_add_base3.runner import CURRENT, LIVE_ID, run_campaign
from research.reverse_and_add_base3.spec import map_images, map_spec
from research.literature import get_reference
from research_engine.memory.hygiene import leak_hits
from research_engine.memory.seed_targets import board_targets
from research_engine.memory.types import FailureClass
from research_engine.planner.orchestrator import DEFAULT_ATTACK_ORDER
from research_engine.strategy import ResearchGoal

ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "src" / "research" / "reverse_and_add_base3"
FORBIDDEN_SPEC = (
    "named conjectures",
    "open-problem",
    "palindrome",
    "Lychrel",
    "base-10",
    "Collatz",
    "every integer",
    "every seed",
)


def _source_lines(name: str) -> str:
    return (SRC / name).read_text(encoding="utf-8")


def test_adapter_sources_are_blind_and_do_not_import_scout():
    for name in ("spec.py", "adapter.py", "planner.py"):
        text = _source_lines(name)
        for line in text.splitlines():
            stripped = line.strip()
            if "reverse_and_add_base3.scout" in stripped:
                raise AssertionError(f"{name} imports scout")
        hits = leak_hits(text, FORBIDDEN_SPEC)
        assert hits == (), f"{name} leaked {hits}"


def test_blind_packet_matches_the_stored_board_definition():
    packet = next(item.blind_packet for item in board_targets() if item.name == CURRENT)
    spec = map_spec()
    assert spec.name == packet.spec_name
    assert spec.dimension == packet.dimension
    assert spec.start == 196
    assert spec.start_remaining == packet.max_steps
    assert spec.state_cap == packet.max_states
    assert map_images(196) == (392,)
    assert map_images(0) == (0,)
    assert spec.affine_system() is None


def test_problem_descriptor_and_prior_art():
    assert get_problem(CURRENT) is PROBLEM
    assert PROBLEM.docs == ("docs/problems/reverse_and_add_base3.md",)
    assert get_reference("oeis-A134028")["id"] == "oeis-A134028"


def test_attack_architecture_remains_frozen():
    assert DEFAULT_ATTACK_ORDER[-1] == "symmetry"
    assert "piecewise_affine" in DEFAULT_ATTACK_ORDER
    assert "reverse" in DEFAULT_ATTACK_ORDER
    assert "reverse_add" not in DEFAULT_ATTACK_ORDER
    assert "lychrel" not in DEFAULT_ATTACK_ORDER


def test_post_run_seed_orbit_and_non_affine():
    spec = map_spec()
    report = evidence_state(spec)
    assert report["start_orbit"] == (196, 392, -672, -448, -824, 192, 280, 560, 0)
    assert report["steps_to_zero"] == 8
    assert report["fixed_zero"] is True
    assert report["reverse_fixed_start"] is True
    assert report["universal_reverse_fixed"] is False
    assert report["image_at_8"] == 0
    flag = falsify_claims(spec)
    assert flag["residue_affine_cover"]["status"] == "REFUTED"
    assert flag["seed_halt_is_z_theorem"]["status"] == "REFUTED"
    assert flag["this_is_digit_fold"]["status"] == "REFUTED"
    assert flag["this_is_aliquot"]["status"] == "REFUTED"
    assert flag["this_is_juggler"]["status"] == "REFUTED"
    assert flag["every_seed_reverse_fixed"]["status"] == "REFUTED"
    assert flag["new_reverse_attack"]["status"] == "REFUTED"


def test_blind_strategy_selects_termination_chain_without_memory():
    report = plan_strategy(goal=ResearchGoal.TERMINATION, memory=None)
    assert report.plan.chain.id == "global_inductive"
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
    flagship = report.by_target("reverse_add_bt")
    assert report.planner_unchanged_with_memory is True
    assert report.strategy_chain == "global_inductive"
    assert flagship.extra["piecewise_affine_status"] == "INCONCLUSIVE"
    assert flagship.extra["closure_status"] == "SUPPORTED"
    assert flagship.extra["closure_size"] == 9
    assert flagship.extra["yield"]["evidence"]["steps_to_zero"] == 8
    assert flagship.extra["yield"]["engineering_changes"] == 0
    assert report.next_target_overridden is False
    if report.next_target_name:
        assert report.next_target_name != CURRENT
    classes = flagship.extra["failure_classes"]
    assert FailureClass.REPRESENTATION.value in classes
    assert FailureClass.GLOBAL_REASONING.value not in classes
    assert report.memory is not None
    stored = report.memory.get(LIVE_ID)
    assert stored.finalized
    assert stored.grey_loot
