"""Frozen-engine campaign on the stored order-2 companion window."""

from __future__ import annotations

from pathlib import Path

from research.literature import get_reference
from research.open_problems import get_problem
from research.skolem_lrs.spec import next_window, observation
from research.skolem_order2_known_zero.discovery import evidence_state, falsify_claims
from research.skolem_order2_known_zero.lean_export import LEAN_MODULE, LEAN_PATH, THEOREMS
from research.skolem_order2_known_zero.problem import PROBLEM
from research.skolem_order2_known_zero.runner import CURRENT, run_campaign
from research.skolem_order2_known_zero.spec import LAST_ROW, WINDOW, map_spec
from research_engine.memory.hygiene import leak_hits
from research_engine.memory.seed_targets import board_targets
from research_engine.memory.types import FailureClass
from research_engine.planner.orchestrator import DEFAULT_ATTACK_ORDER

ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "src" / "research" / "skolem_order2_known_zero"
FORBIDDEN_SPEC = (
    "ranking",
    "p-adic",
    "padic",
    "known zero",
    "known congruence",
    "open-problem",
    "Skolem Problem",
)


def _source_lines(name: str) -> str:
    return (SRC / name).read_text(encoding="utf-8")


def test_adapter_sources_are_blind_and_do_not_import_scout():
    for name in ("spec.py", "adapter.py", "planner.py"):
        text = _source_lines(name)
        for line in text.splitlines():
            stripped = line.strip()
            if "skolem_order2_known_zero.scout" in stripped:
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
    nxt = next_window(WINDOW, LAST_ROW)
    assert nxt == (-6, 3 * (-6) + (-2) * (-7))
    assert observation(WINDOW) == -7


def test_problem_descriptor_and_prior_art():
    assert get_problem("skolem_order2_known_zero") is PROBLEM
    assert PROBLEM.docs == ("docs/problems/skolem_order2_known_zero.md",)
    assert get_reference("kenison-et-al-2025-order-4-skolem")["year"] == 2025


def test_attack_architecture_remains_frozen():
    assert DEFAULT_ATTACK_ORDER[-1] == "symmetry"
    assert "vector_affine" in DEFAULT_ATTACK_ORDER
    assert "control_obstruction" in DEFAULT_ATTACK_ORDER


def test_post_run_zero_witness():
    spec = map_spec()
    report = evidence_state(spec)
    assert report["zero_at"] == 3
    assert report["status"] == "ZERO_WITNESS"
    assert report["universal_zero_free"] is False
    flag = falsify_claims(spec)
    assert flag["never_vanishes"]["status"] == "REFUTED"
    assert flag["never_vanishes"]["counterexample"] == 3


def test_lean_identity_is_known_and_sorry_free():
    path = ROOT / LEAN_PATH
    text = path.read_text(encoding="utf-8")
    assert "sorry" not in text
    assert "admit" not in text
    assert LEAN_MODULE.replace(".", "/") in LEAN_PATH.replace("\\", "/")
    for name in THEOREMS:
        assert name in text


def test_campaign_runs_unmodified_loop():
    _, report = run_campaign()
    flagship = report.by_target("companion_shift_order2")
    assert report.board_pick == CURRENT
    assert report.planner_unchanged_with_memory is True
    assert flagship.decision == "CONTINUE"
    assert flagship.census_kind == "FINITE_CENSUS"
    assert flagship.extra["yield"]["evidence"]["zero_at"] == 3
    assert flagship.extra["yield"]["engineering_changes"] == 0
    assert "vector_affine" in flagship.extra["attack_table"]
    assert report.next_target_overridden is False
    assert report.next_target_name
    assert report.next_target_name != CURRENT
    assert FailureClass.GLOBAL_REASONING.value not in flagship.extra["failure_classes"]
    assert report.memory is not None
    stored = report.memory.get("companion_shift_order2")
    assert stored.finalized
    assert stored.grey_loot
