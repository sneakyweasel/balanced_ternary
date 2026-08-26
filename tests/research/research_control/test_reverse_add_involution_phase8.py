"""Live Phase-8 reverse-add involution-interaction falsifier."""

from __future__ import annotations

import json

from bt.sequences import bt_reverse
from research.research_control.ranking_phase0 import JSON_PATH as PHASE0_JSON
from research.research_control.ranking_phase1 import JSON_PATH as PHASE1_JSON
from research.research_control.reverse_add_carry_phase5 import JSON_PATH as PHASE5_JSON
from research.research_control.reverse_add_composition_phase4 import JSON_PATH as PHASE4_JSON
from research.research_control.reverse_add_involution_phase8 import (
    DOC_PATH,
    JSON_PATH,
    SPECIAL_PROBE_ROLES,
    involution_sample_for,
    reverse_samples,
    run_phase8,
    write_artifacts,
)
from research.research_control.reverse_add_pair_interaction_phase6 import (
    JSON_PATH as PHASE6_JSON,
)
from research.research_control.reverse_add_pair_interaction_phase6 import frozen_seeds
from research.research_control.reverse_add_weighted_pair_phase7 import JSON_PATH as PHASE7_JSON
from research.research_control.symbolic_composition_phase2 import JSON_PATH as PHASE2_JSON
from research.research_control.symbolic_composition_phase3 import JSON_PATH as PHASE3_JSON
from research.reverse_and_add_base3.discovery import WINDOW as REVERSE_WINDOW
from research.reverse_and_add_base3.discovery import orbit as reverse_orbit
from research.reverse_and_add_base3.spec import ReverseAddSpec
from research_engine.control.baseline import load_v2_3_baseline, verify_manifest
from research_engine.control.reverse_add_involution import ReverseInvolutionClass, ranked_candidates
from research_engine.control.types import ENGINE_CONTROL_VERSION
from research_engine.planner.orchestrator import DEFAULT_ATTACK_ORDER, EXPERIMENTAL_ATTACKS


def test_involution_on_probes_and_canonical_negatives():
    assert bt_reverse(bt_reverse(0)) == 0
    assert bt_reverse(bt_reverse(1)) == 1
    assert bt_reverse(bt_reverse(-1)) == -1
    assert bt_reverse(bt_reverse(2)) == 2
    assert bt_reverse(bt_reverse(5)) == 5
    assert bt_reverse(bt_reverse(8)) == 8
    assert bt_reverse(bt_reverse(196)) == 196
    assert bt_reverse(bt_reverse(3)) != 3
    assert bt_reverse(bt_reverse(6)) != 6
    assert bt_reverse(bt_reverse(-672)) != -672
    pal = involution_sample_for(1, image=2)
    assert pal.involutive is True
    assert pal.w_source == 1
    six = involution_sample_for(6, image=4)
    assert six.involutive is False
    assert six.ww_source == 2


def test_phase8_three_candidates_and_artifacts():
    samples, outcomes, classification, _reason = run_phase8()
    assert [item.rank for item in outcomes] == [1, 2, 3]
    assert len(ranked_candidates()) == 3
    by_name = {item.name: item for item in outcomes}
    residual = by_name["reverse_sum_residual_bound"]
    gap = by_name["successor_reverse_gap_length_bound"]
    msd = by_name["successor_msd_from_operand_pair"]
    assert residual.survived is False
    assert residual.counterexample is not None
    assert residual.counterexample.source == 1
    assert residual.failure_class == "INVOLUTION_RESIDUAL_MISMATCH"
    assert gap.survived is False
    assert gap.counterexample is not None
    assert gap.counterexample.source == 1
    assert gap.failure_class == "SUCCESSOR_REVERSAL_UNCONTROLLED"
    assert msd.survived is True
    assert classification is ReverseInvolutionClass.REVERSE_INVOLUTION_REFUTED
    payload = write_artifacts(samples)
    assert payload["engine_control_version"] == ENGINE_CONTROL_VERSION
    assert payload["source_engine"] == "v2.3"
    assert payload["experimental_status"] == "PHASE_8_REVERSE_INVOLUTION_FALSIFIER"
    assert payload["decision"] == "REVERSE_INVOLUTION_REFUTED"
    assert payload["green_loot"] == "NO_NEW_LOOT"
    assert payload["lean_status"] == "FORMALIZATION_BLOCKED"
    assert payload["composition_depth"] == 1
    assert payload["anti_tautology_check"]["candidates_reconstruct_T"] is False
    assert payload["anti_tautology_check"]["not_investigated"] == "T^2(x)"
    assessed = {item["name"]: item["assessed"] for item in payload["reverse_specificity_check"]}
    assert assessed["successor_msd_from_operand_pair"] == "GENERAL_ARITHMETIC"
    assert {probe["source"] for probe in payload["special_probes"]} == set(SPECIAL_PROBE_ROLES)
    names = [item["attack_name"] for item in payload["top3_update"]["proposals"]]
    assert names[0] == "symbolic_nonlinear_composition"
    assert "reverse_involution_structure" not in names
    assert JSON_PATH.is_file()
    assert DOC_PATH.is_file()
    text = DOC_PATH.read_text(encoding="utf-8")
    assert "REVERSE_INVOLUTION_REFUTED" in text
    assert "NO_NEW_LOOT" in text


def test_phase8_does_not_expand_census_or_composition_depth():
    allowed = set(REVERSE_WINDOW) | {int(item) for item in reverse_orbit(196)["path"]}
    samples = reverse_samples()
    assert set(frozen_seeds()) <= allowed
    assert {item.source for item in samples} <= allowed
    assert all(item.image == ReverseAddSpec(start=item.source).successors(item.source)[0] for item in samples)
    assert all("mid" not in item.as_dict() for item in samples)
    assert all("t_squared" not in item.as_dict() for item in samples)


def test_phase8_does_not_thaw_or_rewrite_history():
    assert "reverse_involution_phase8" not in DEFAULT_ATTACK_ORDER
    assert "reverse_involution_structure" not in DEFAULT_ATTACK_ORDER
    assert "reverse_involution_phase8" not in EXPERIMENTAL_ATTACKS
    assert DEFAULT_ATTACK_ORDER[-1] == "symmetry"
    verify_manifest(load_v2_3_baseline().manifest)
    phase0 = json.loads(PHASE0_JSON.read_text(encoding="utf-8"))
    phase1 = json.loads(PHASE1_JSON.read_text(encoding="utf-8"))
    phase2 = json.loads(PHASE2_JSON.read_text(encoding="utf-8"))
    phase3 = json.loads(PHASE3_JSON.read_text(encoding="utf-8"))
    phase4 = json.loads(PHASE4_JSON.read_text(encoding="utf-8"))
    phase5 = json.loads(PHASE5_JSON.read_text(encoding="utf-8"))
    phase6 = json.loads(PHASE6_JSON.read_text(encoding="utf-8"))
    phase7 = json.loads(PHASE7_JSON.read_text(encoding="utf-8"))
    assert phase0["experimental_status"] == "PHASE_0_FALSIFIER"
    assert phase1["ranking_phase1_decision"] == "MIXED"
    assert phase2["phase2_decision"] == "MIXED"
    assert phase3["decision"] == "PROMOTE_RESTRICTED"
    assert phase4["experimental_status"] == "PHASE_4_REVERSE_ADD_COMPOSITION_FALSIFIER"
    assert phase5["experimental_status"] == "PHASE_5_REVERSE_ADD_CARRY_FALSIFIER"
    assert phase6["experimental_status"] == "PHASE_6_REVERSE_PAIR_INTERACTION_FALSIFIER"
    assert phase7["experimental_status"] == "PHASE_7_WEIGHTED_REVERSE_PAIR_FALSIFIER"
    assert phase7["decision"] == "WEIGHTED_PAIR_PROMISING"
