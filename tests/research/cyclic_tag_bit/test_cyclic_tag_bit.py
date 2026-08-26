"""Frozen-engine campaign on the encoded binary-word rewrite."""

from __future__ import annotations

from pathlib import Path

from research.cyclic_tag_bit.discovery import evidence_state, falsify_claims
from research.cyclic_tag_bit.lean_export import LEAN_MODULE, LEAN_PATH, THEOREMS
from research.cyclic_tag_bit.planner import plan_strategy
from research.cyclic_tag_bit.problem import PROBLEM
from research.cyclic_tag_bit.runner import CURRENT, LIVE_ID, run_campaign
from research.cyclic_tag_bit.spec import encode_word, map_images, map_spec, step_word
from research.literature import get_reference
from research.open_problems import get_problem
from research_engine.memory.hygiene import leak_hits
from research_engine.memory.seed_targets import board_targets
from research_engine.memory.types import FailureClass
from research_engine.planner.orchestrator import DEFAULT_ATTACK_ORDER
from research_engine.strategy import ResearchGoal

ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "src" / "research" / "cyclic_tag_bit"
FORBIDDEN_SPEC = (
    "named conjectures",
    "open-problem",
    "universality",
    "Cocke",
    "Collatz",
    "Post tag",
)


def _source_lines(name: str) -> str:
    return (SRC / name).read_text(encoding="utf-8")


def test_adapter_sources_are_blind_and_do_not_import_scout():
    for name in ("spec.py", "adapter.py", "planner.py"):
        text = _source_lines(name)
        for line in text.splitlines():
            stripped = line.strip()
            if "cyclic_tag_bit.scout" in stripped:
                raise AssertionError(f"{name} imports scout")
        hits = leak_hits(text, FORBIDDEN_SPEC)
        assert hits == (), f"{name} leaked {hits}"


def test_blind_packet_matches_the_stored_board_definition():
    packet = next(item.blind_packet for item in board_targets() if item.name == CURRENT)
    spec = map_spec()
    assert spec.name == packet.spec_name
    assert spec.dimension == packet.dimension
    assert spec.start_word == "101"
    assert spec.start_remaining == packet.max_steps
    assert spec.state_cap == packet.max_states
    assert encode_word("101") == 13
    assert map_images(13) == (encode_word("0111"),)
    assert step_word("0") == "0"
    assert step_word("") is None
    assert spec.affine_system() is None


def test_problem_descriptor_and_prior_art():
    assert get_problem(CURRENT) is PROBLEM
    assert PROBLEM.docs == ("docs/problems/cyclic_tag_bit.md",)
    assert get_reference("baader-nipkow-1998-term-rewriting")["year"] == 1998


def test_attack_architecture_remains_frozen():
    assert DEFAULT_ATTACK_ORDER[-1] == "symmetry"
    assert "piecewise_affine" in DEFAULT_ATTACK_ORDER
    assert "tag" not in DEFAULT_ATTACK_ORDER
    assert "cyclic_tag" not in DEFAULT_ATTACK_ORDER


def test_post_run_seed_orbit_and_non_affine():
    spec = map_spec()
    report = evidence_state(spec)
    assert report["start_orbit"][:3] == ("101", "0111", "1110")
    assert report["hits_empty"] is False
    assert report["steps_to_empty"] is None
    assert report["empty_halt"] is True
    assert report["zero_fixed"] is True
    assert report["first_growth"] == "1"
    assert report["universal_empty"] is False
    flag = falsify_claims(spec)
    assert flag["residue_affine_cover"]["status"] == "REFUTED"
    assert flag["seed_halt_is_z_theorem"]["status"] == "REFUTED"
    assert flag["this_is_integer_affine"]["status"] == "REFUTED"
    assert flag["empty_from_nonempty"]["status"] == "REFUTED"
    assert flag["new_tag_attack"]["status"] == "REFUTED"


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
    flagship = report.by_target("cyclic_tag_bit")
    assert report.planner_unchanged_with_memory is True
    assert report.strategy_chain == "global_inductive"
    assert flagship.extra["piecewise_affine_status"] == "INCONCLUSIVE"
    assert flagship.extra["closure_status"] == "INCONCLUSIVE"
    assert flagship.extra["closure_complete"] is False
    assert flagship.extra["yield"]["evidence"]["hits_empty"] is False
    assert flagship.extra["yield"]["engineering_changes"] == 0
    assert report.next_target_overridden is False
    classes = flagship.extra["failure_classes"]
    assert FailureClass.REPRESENTATION.value in classes
    assert FailureClass.GLOBAL_REASONING.value not in classes
    assert report.memory is not None
    stored = report.memory.get(LIVE_ID)
    assert stored.finalized
    assert stored.grey_loot
