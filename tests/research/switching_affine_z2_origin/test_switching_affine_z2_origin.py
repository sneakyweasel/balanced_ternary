"""Frozen-engine campaign on the stored two-path Z^2 map."""

from __future__ import annotations

from pathlib import Path

from research.literature import get_reference
from research.open_problems import get_problem
from research.switching_affine_z2_origin.discovery import evidence_state, falsify_claims
from research.switching_affine_z2_origin.lean_export import LEAN_MODULE, THEOREMS
from research.switching_affine_z2_origin.problem import PROBLEM
from research.switching_affine_z2_origin.runner import run_campaign
from research.switching_affine_z2_origin.spec import map_spec, next_state
from research_engine.memory.seed_targets import board_targets
from research_engine.memory.types import FailureClass
from research_engine.planner.orchestrator import DEFAULT_ATTACK_ORDER

ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "src" / "research" / "switching_affine_z2_origin"
FORBIDDEN_SPEC = (
    "ranking",
    "Carelli",
    "Ben-Amram",
    "termination",
    "2-adic",
    "padic",
    "SLC",
    "hybrid automaton",
    "unreachable",
    "origin-avoidance",
)


def _source_lines(name: str) -> str:
    return (SRC / name).read_text(encoding="utf-8")


def test_adapter_sources_are_blind_and_do_not_import_scout():
    for name in ("spec.py", "adapter.py", "planner.py"):
        text = _source_lines(name)
        for line in text.splitlines():
            stripped = line.strip()
            if "switching_affine_z2_origin.scout" in stripped:
                raise AssertionError(f"{name} imports scout")
    spec = _source_lines("spec.py")
    for token in FORBIDDEN_SPEC:
        assert token not in spec, f"spec.py contains forbidden token {token!r}"


def test_blind_packet_matches_the_stored_board_definition():
    packet = next(item.blind_packet for item in board_targets() if item.name == "switching_affine_z2_origin")
    spec = map_spec()
    assert spec.name == packet.spec_name
    assert spec.dimension == packet.dimension
    assert spec.start == (3, 2)
    assert spec.start_remaining == packet.max_steps
    assert spec.state_cap == packet.max_states
    assert next_state((3, 2)) == (5, 1)
    assert next_state((6, 0)) == (5, 6)
    assert next_state((0, 0)) is None


def test_problem_descriptor_and_prior_art():
    assert get_problem("switching_affine_z2_origin") is PROBLEM
    assert PROBLEM.docs == ("docs/problems/switching_affine_z2_origin.md",)
    assert get_reference("ben-amram-genaim-ouaknine-worrell-2025-termination-survey")["year"] == 2025


def test_attack_architecture_remains_frozen():
    assert DEFAULT_ATTACK_ORDER[-1] == "symmetry"
    assert "vector_affine" in DEFAULT_ATTACK_ORDER
    assert "control_obstruction" in DEFAULT_ATTACK_ORDER


def test_post_run_origin_and_cycle_facts():
    spec = map_spec()
    report = evidence_state(spec)
    assert report["origin_at"] is None
    assert report["universal_origin"] is False
    assert report["origin_preimages"] == ((-1, 1), (1, -1))
    assert report["n2_preimages_only_origin"] is True
    assert report["cycle_unit"] == ((0, 1), (1, 0))
    assert report["small_origin_hits"] == ()
    flag = falsify_claims(spec)
    assert flag["start_reaches_origin"]["status"] == "REFUTED"
    assert flag["no_finite_cycle"]["status"] == "REFUTED"
    assert flag["n2_preimage_is_origin_only"]["status"] == "EXACT"


def test_lean_identities_are_known_and_sorry_free():
    path = ROOT / "formal" / "Problems" / "Engine" / "TwoPathZ2.lean"
    text = path.read_text(encoding="utf-8")
    assert "sorry" not in text
    assert "admit" not in text
    assert LEAN_MODULE.replace(".", "/") in "formal/Problems/Engine/TwoPathZ2.lean"
    for name in THEOREMS:
        assert name in text


def test_campaign_runs_unmodified_loop():
    _, report = run_campaign()
    flagship = report.by_target("two_path_z2")
    assert report.planner_unchanged_with_memory is True
    assert flagship.decision == "CONTINUE"
    assert flagship.census_kind == "FINITE_CENSUS"
    assert flagship.extra["yield"]["evidence"]["origin_at"] is None
    assert flagship.extra["yield"]["evidence"]["n2_preimages_only_origin"] is True
    assert flagship.extra["yield"]["engineering_changes"] == 0
    assert "vector_affine" in flagship.extra["attack_table"]
    assert report.next_target_overridden is False
    assert report.next_target_name
    assert report.next_target_name != "switching_affine_z2_origin"
    assert FailureClass.GLOBAL_REASONING.value not in flagship.extra["failure_classes"]
    assert report.memory is not None
    stored = report.memory.get("two_path_z2")
    assert stored.finalized
    assert stored.grey_loot
