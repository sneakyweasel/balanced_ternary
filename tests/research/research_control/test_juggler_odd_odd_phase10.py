"""Live Phase-10 Juggler odd-odd composition falsifier."""

from __future__ import annotations

import json

from research.juggler_sequence.discovery import WINDOW as JUGGLER_WINDOW
from research.juggler_sequence.discovery import orbit as juggler_orbit
from research.research_control.juggler_odd_odd_phase10 import (
    DOC_PATH,
    JSON_PATH,
    LEAN_PATH,
    frozen_seeds,
    odd_even_samples,
    odd_odd_samples,
    run_phase10,
    write_artifacts,
)
from research.research_control.phase9_frontier_ranking import JSON_PATH as PHASE9_JSON
from research.research_control.ranking_phase0 import JSON_PATH as PHASE0_JSON
from research.research_control.ranking_phase1 import JSON_PATH as PHASE1_JSON
from research.research_control.reverse_add_involution_phase8 import JSON_PATH as PHASE8_JSON
from research.research_control.symbolic_composition_phase2 import JSON_PATH as PHASE2_JSON
from research.research_control.symbolic_composition_phase3 import JSON_PATH as PHASE3_JSON
from research_engine.control.baseline import load_v2_3_baseline, verify_manifest
from research_engine.control.juggler_odd_odd import DEPTH, OddOddClass, ranked_candidates
from research_engine.control.types import ENGINE_CONTROL_VERSION
from research_engine.planner.orchestrator import DEFAULT_ATTACK_ORDER, EXPERIMENTAL_ATTACKS


def test_phase10_three_candidates_and_artifacts():
    payload = write_artifacts()
    assert payload["engine_control_version"] == ENGINE_CONTROL_VERSION
    assert payload["source_engine"] == "v2.3"
    assert payload["experimental_status"] == "PHASE_10_JUGGLER_ODD_ODD_COMPOSITION_FALSIFIER"
    assert payload["target"] == "juggler_sequence"
    assert payload["attack"] == "odd_odd_branch_composition"
    assert payload["composition_depth"] == DEPTH == 2
    by_name = {item["name"]: item for item in payload["candidates"]}
    assert [item["rank"] for item in payload["candidates"]] == [1, 2, 3]
    assert len(ranked_candidates()) == 3
    strict = by_name["strict_two_step_growth"]
    growth = by_name["thresholded_two_step_growth"]
    preserve = by_name["odd_cylinder_preservation"]
    assert strict["survived"] is False
    assert strict["counterexample"]["source"] == 1
    assert growth["survived"] is True
    assert preserve["survived"] is False
    assert preserve["counterexample"]["source"] == 5
    assert payload["decision"] == OddOddClass.JUGGLER_ODD_ODD_GREEN_LOOT.value
    assert payload["green_loot"] == "JUGGLER_ODD_ODD_GREEN_LOOT"
    assert payload["lean_status"] == "PROVED"
    assert payload["global_consequence"] == "LOCAL_BRANCH_LAW"
    assert payload["anti_tautology_checks"]["global_termination_claimed"] is False
    assert payload["domains"]["odd_even_unchanged"] is True
    names = [item["attack_name"] for item in payload["top3_update"]["proposals"]]
    assert names[0] == "odd_odd_symbolic_composition"
    assert "odd_odd_branch_composition" not in names
    assert JSON_PATH.is_file()
    assert DOC_PATH.is_file()
    text = DOC_PATH.read_text(encoding="utf-8")
    assert "JUGGLER_ODD_ODD_GREEN_LOOT" in text
    assert "LOCAL_BRANCH_LAW" in text


def test_phase10_does_not_expand_census_or_depth():
    allowed = set(JUGGLER_WINDOW) | {int(item) for item in juggler_orbit(13)["path"]}
    assert set(frozen_seeds()) <= allowed
    oo = odd_odd_samples()
    oe = odd_even_samples()
    assert {item.source for item in oo} <= allowed
    assert {item.source for item in oe} <= allowed
    assert any(item.source == 3 and item.mid == 5 and item.image == 11 for item in oo)
    assert all(item.source % 2 == 1 and item.mid % 2 == 1 for item in oo)
    assert all(item.mid % 2 == 0 for item in oe)
    assert not ({item.source for item in oo} & {item.source for item in oe})
    assert DEPTH == 2
    assert oo[0].as_dict()["composition_depth"] == 2


def test_odd_even_lean_theorem_unchanged():
    text = LEAN_PATH.read_text(encoding="utf-8")
    assert "theorem floorPower_odd_even_two_step_lt" in text
    assert "exact sqrt_sqrt_n_cubed_lt hn" in text
    assert "theorem floorPower_odd_odd_two_step_gt" in text
    assert "sorry" not in text
    assert "admit" not in text


def test_phase10_does_not_thaw_or_rewrite_history():
    assert "juggler_odd_odd_phase10" not in DEFAULT_ATTACK_ORDER
    assert "odd_odd_branch_composition" not in DEFAULT_ATTACK_ORDER
    assert "odd_odd_symbolic_composition" not in DEFAULT_ATTACK_ORDER
    assert "juggler_odd_odd_phase10" not in EXPERIMENTAL_ATTACKS
    assert DEFAULT_ATTACK_ORDER[-1] == "symmetry"
    verify_manifest(load_v2_3_baseline().manifest)
    phase0 = json.loads(PHASE0_JSON.read_text(encoding="utf-8"))
    phase1 = json.loads(PHASE1_JSON.read_text(encoding="utf-8"))
    phase2 = json.loads(PHASE2_JSON.read_text(encoding="utf-8"))
    phase3 = json.loads(PHASE3_JSON.read_text(encoding="utf-8"))
    phase8 = json.loads(PHASE8_JSON.read_text(encoding="utf-8"))
    phase9 = json.loads(PHASE9_JSON.read_text(encoding="utf-8"))
    assert phase0["experimental_status"] == "PHASE_0_FALSIFIER"
    assert phase1["ranking_phase1_decision"] == "MIXED"
    assert phase2["phase2_decision"] == "MIXED"
    assert phase3["decision"] == "PROMOTE_RESTRICTED"
    assert phase8["decision"] == "REVERSE_INVOLUTION_REFUTED"
    assert phase9["decision"] == "SELECTED_FRONTIER"
    run_phase10()
    assert json.loads(PHASE9_JSON.read_text(encoding="utf-8"))["decision"] == "SELECTED_FRONTIER"
    assert json.loads(PHASE3_JSON.read_text(encoding="utf-8"))["attack_name"] == "odd_even_two_step_decrease"
