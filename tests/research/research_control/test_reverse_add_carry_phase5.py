"""Live Phase-5 reverse-add balanced-ternary carry falsifier."""

from __future__ import annotations

import json

from bt.normalization import add_with_trace
from bt.representation import decode, encode
from bt.sequences import bt_length, bt_reverse
from research.research_control.ranking_phase0 import JSON_PATH as PHASE0_JSON
from research.research_control.ranking_phase1 import JSON_PATH as PHASE1_JSON
from research.research_control.reverse_add_carry_phase5 import (
    DOC_PATH,
    JSON_PATH,
    SPECIAL_PROBE_ROLES,
    carry_statistic,
    frozen_seeds,
    reverse_samples,
    run_phase5,
    successor_from_trace,
    write_artifacts,
)
from research.research_control.reverse_add_composition_phase4 import JSON_PATH as PHASE4_JSON
from research.research_control.symbolic_composition_phase2 import JSON_PATH as PHASE2_JSON
from research.research_control.symbolic_composition_phase3 import JSON_PATH as PHASE3_JSON
from research.reverse_and_add_base3.discovery import WINDOW as REVERSE_WINDOW
from research.reverse_and_add_base3.discovery import orbit as reverse_orbit
from research.reverse_and_add_base3.spec import ReverseAddSpec, map_images
from research_engine.control.baseline import load_v2_3_baseline, verify_manifest
from research_engine.control.reverse_add_carry import CarryClass, carry_chain_length, ranked_candidates
from research_engine.control.types import ENGINE_CONTROL_VERSION
from research_engine.planner.orchestrator import DEFAULT_ATTACK_ORDER, EXPERIMENTAL_ATTACKS


def test_carry_statistic_canonical_and_successor_agreement():
    assert carry_statistic(0) == 0
    assert successor_from_trace(0) == 0
    assert carry_statistic(1) == 2
    assert successor_from_trace(1) == 2
    assert carry_statistic(-1) == carry_statistic(1)
    assert successor_from_trace(-1) == -2
    assert carry_statistic(2) == 0
    assert successor_from_trace(2) == 0
    assert carry_statistic(-2) == 0
    assert decode(encode(5)) == 5
    assert decode(encode(-5)) == -5
    spec = ReverseAddSpec(start=5)
    assert spec.successors(5) == map_images(5) == (successor_from_trace(5),)
    assert successor_from_trace(5) == 5 + bt_reverse(5)
    trace = add_with_trace(encode(5), encode(bt_reverse(5)))
    steps = tuple((step.carry_in, step.carry_out) for step in trace.steps)
    assert carry_statistic(5) == carry_chain_length(steps, final_carry=trace.final_carry)
    assert carry_statistic(5) == carry_statistic(5)
    assert bt_reverse(-8) == -bt_reverse(8)


def test_phase5_three_candidates_and_artifacts():
    samples, outcomes, classification, _reason = run_phase5()
    assert [item.rank for item in outcomes] == [1, 2, 3]
    assert len(ranked_candidates()) == 3
    by_name = {item.name: item for item in outcomes}
    growth = by_name["carry_bounds_length_growth"]
    zero = by_name["zero_carry_preserves_length"]
    positive = by_name["positive_carry_forces_length_plus_one"]
    assert growth.survived is True
    assert growth.counterexample is None
    assert zero.survived is False
    assert zero.failure_class == "REVERSAL_DEPENDENCE"
    assert zero.counterexample is not None
    assert zero.counterexample.source == 2
    assert zero.counterexample.image == 0
    assert positive.survived is False
    assert positive.failure_class == "LENGTH_DECOUPLING"
    assert positive.counterexample is not None
    assert positive.counterexample.source == 5
    assert classification is CarryClass.CARRY_NEEDS_RICHER_STATE
    payload = write_artifacts(samples)
    assert payload["engine_control_version"] == ENGINE_CONTROL_VERSION
    assert payload["source_engine"] == "v2.3"
    assert payload["experimental_status"] == "PHASE_5_REVERSE_ADD_CARRY_FALSIFIER"
    assert payload["decision"] == "CARRY_NEEDS_RICHER_STATE"
    assert payload["green_loot"] == "NO_NEW_LOOT"
    assert payload["lean_status"] == "FORMALIZATION_BLOCKED"
    assert payload["composition_depth"] == 1
    assert payload["target"] == "reverse_and_add_base3"
    assert payload["carry_definition"]["selected"] == "carry_chain_length"
    assert payload["canonicalization"]["msd_carry_counts"] is True
    assert {probe["source"] for probe in payload["special_probes"]} == set(SPECIAL_PROBE_ROLES)
    names = [item["attack_name"] for item in payload["top3_update"]["proposals"]]
    assert names[0] == "symbolic_nonlinear_composition"
    assert "carry_structure_analysis" not in names
    assert "balanced_ternary_carry_attack" not in names
    assert JSON_PATH.is_file()
    assert DOC_PATH.is_file()
    text = DOC_PATH.read_text(encoding="utf-8")
    assert "CARRY_NEEDS_RICHER_STATE" in text
    assert "NO_NEW_LOOT" in text
    assert payload["transition_window"]["sample_count"] == len(samples)
    assert payload["transition_window"]["composition_depth"] == 1


def test_phase5_does_not_expand_census_or_composition_depth():
    allowed = set(REVERSE_WINDOW) | {int(item) for item in reverse_orbit(196)["path"]}
    seeds = frozen_seeds()
    assert set(seeds) <= allowed
    samples = reverse_samples()
    assert {item.source for item in samples} <= allowed
    assert all(item.image == ReverseAddSpec(start=item.source).successors(item.source)[0] for item in samples)
    assert all(item.len_source == bt_length(item.source) for item in samples)
    assert not any(hasattr(item, "mid") and item.as_dict().get("mid") is not None for item in samples)


def test_phase5_does_not_thaw_or_rewrite_history():
    assert "carry_phase5" not in DEFAULT_ATTACK_ORDER
    assert "balanced_ternary_carry_attack" not in DEFAULT_ATTACK_ORDER
    assert "carry_phase5" not in EXPERIMENTAL_ATTACKS
    assert "balanced_ternary_carry_attack" not in EXPERIMENTAL_ATTACKS
    assert DEFAULT_ATTACK_ORDER[-1] == "symmetry"
    verify_manifest(load_v2_3_baseline().manifest)
    phase0 = json.loads(PHASE0_JSON.read_text(encoding="utf-8"))
    phase1 = json.loads(PHASE1_JSON.read_text(encoding="utf-8"))
    phase2 = json.loads(PHASE2_JSON.read_text(encoding="utf-8"))
    phase3 = json.loads(PHASE3_JSON.read_text(encoding="utf-8"))
    phase4 = json.loads(PHASE4_JSON.read_text(encoding="utf-8"))
    assert phase0["experimental_status"] == "PHASE_0_FALSIFIER"
    assert phase1["ranking_phase1_decision"] == "MIXED"
    assert phase2["phase2_decision"] == "MIXED"
    assert phase3["decision"] == "PROMOTE_RESTRICTED"
    assert phase3["experimental_status"] == "PHASE_3_RESTRICTED_SYMBOLIC_ATTACK"
    assert phase4["experimental_status"] == "PHASE_4_REVERSE_ADD_COMPOSITION_FALSIFIER"
    assert phase4["decision"] == "REVERSE_COMPOSITION_NEEDS_RICHER_STRUCTURE"
