"""Live Phase-7 reverse-add weighted reverse-pair falsifier."""

from __future__ import annotations

import json

from bt.representation import digits, encode
from bt.sequences import bt_length, bt_reverse
from research.research_control.ranking_phase0 import JSON_PATH as PHASE0_JSON
from research.research_control.ranking_phase1 import JSON_PATH as PHASE1_JSON
from research.research_control.reverse_add_carry_phase5 import JSON_PATH as PHASE5_JSON
from research.research_control.reverse_add_composition_phase4 import JSON_PATH as PHASE4_JSON
from research.research_control.reverse_add_pair_interaction_phase6 import (
    JSON_PATH as PHASE6_JSON,
)
from research.research_control.reverse_add_pair_interaction_phase6 import frozen_seeds
from research.research_control.reverse_add_weighted_pair_phase7 import (
    DOC_PATH,
    JSON_PATH,
    SPECIAL_PROBE_ROLES,
    reverse_samples,
    run_phase7,
    weighted_sample_for,
    write_artifacts,
)
from research.research_control.symbolic_composition_phase2 import JSON_PATH as PHASE2_JSON
from research.research_control.symbolic_composition_phase3 import JSON_PATH as PHASE3_JSON
from research.reverse_and_add_base3.discovery import WINDOW as REVERSE_WINDOW
from research.reverse_and_add_base3.discovery import orbit as reverse_orbit
from research.reverse_and_add_base3.spec import ReverseAddSpec, map_images
from research_engine.control.baseline import load_v2_3_baseline, verify_manifest
from research_engine.control.reverse_add_pair_interaction import pair_sums_lsd
from research_engine.control.reverse_add_weighted_pair import (
    FORBIDDEN_STATISTIC_KEYS,
    WeightedPairClass,
    ranked_candidates,
)
from research_engine.control.types import ENGINE_CONTROL_VERSION
from research_engine.planner.orchestrator import DEFAULT_ATTACK_ORDER, EXPERIMENTAL_ATTACKS


def test_positional_construction_probes_and_padding():
    zero = weighted_sample_for(0, image=0)
    assert zero.h is None
    pal = weighted_sample_for(1, image=2)
    assert pal.pair_sums == (2,)
    assert pal.h == 0 and pal.sign_h == 1
    neg = weighted_sample_for(-1, image=-2)
    assert neg.sign_h == -1
    revneg = weighted_sample_for(2, image=0)
    assert bt_reverse(2) == -2
    assert revneg.h is None
    five = weighted_sample_for(5, image=-6)
    assert five.image == ReverseAddSpec(start=5).successors(5)[0] == map_images(5)[0]
    assert five.pair_sums == pair_sums_lsd(digits(encode(5)), digits(encode(bt_reverse(5))))
    assert five.h == 1 and five.sign_h == -1
    eight = weighted_sample_for(8, image=0)
    assert eight.h is None
    seed = weighted_sample_for(196, image=392)
    assert seed.h == 5 and seed.sign_h == 1
    fail6 = weighted_sample_for(-672, image=-448)
    assert fail6.h == 6 and fail6.sign_h == -1
    assert fail6.m_minus == 6 and fail6.m_plus == 5
    keys = set(fail6.as_dict())
    assert not (keys & FORBIDDEN_STATISTIC_KEYS)


def test_phase7_three_candidates_and_artifacts():
    samples, outcomes, classification, _reason = run_phase7()
    assert [item.rank for item in outcomes] == [1, 2, 3]
    assert len(ranked_candidates()) == 3
    by_name = {item.name: item for item in outcomes}
    top = by_name["highest_nonzero_pair_determines_sign"]
    dom = by_name["highest_positive_vs_highest_negative"]
    mag2 = by_name["highest_mag2_determines_sign"]
    assert top.survived is True
    assert dom.survived is True
    assert mag2.survived is False
    assert mag2.failure_class == "MULTI_POSITION_INTERFERENCE"
    assert mag2.counterexample is not None
    assert mag2.counterexample.source == 6
    assert mag2.counterexample.image == 4
    assert classification is WeightedPairClass.WEIGHTED_PAIR_PROMISING
    payload = write_artifacts(samples)
    assert payload["engine_control_version"] == ENGINE_CONTROL_VERSION
    assert payload["source_engine"] == "v2.3"
    assert payload["experimental_status"] == "PHASE_7_WEIGHTED_REVERSE_PAIR_FALSIFIER"
    assert payload["decision"] == "WEIGHTED_PAIR_PROMISING"
    assert payload["green_loot"] == "NO_NEW_LOOT"
    assert payload["lean_status"] == "FORMALIZATION_READY"
    assert payload["composition_depth"] == 1
    assert payload["tautology_checks"]["candidates_reconstruct_T"] is False
    assert {probe["source"] for probe in payload["special_probes"]} == set(SPECIAL_PROBE_ROLES)
    names = [item["attack_name"] for item in payload["top3_update"]["proposals"]]
    assert names[0] == "symbolic_nonlinear_composition"
    assert "weighted_reverse_pair_interaction" not in names
    assert JSON_PATH.is_file()
    assert DOC_PATH.is_file()
    text = DOC_PATH.read_text(encoding="utf-8")
    assert "WEIGHTED_PAIR_PROMISING" in text
    assert "NO_NEW_LOOT" in text
    assert payload["transition_window"]["sample_count"] == len(samples)
    assert payload["transition_window"]["composition_depth"] == 1


def test_phase7_does_not_expand_census_or_composition_depth():
    allowed = set(REVERSE_WINDOW) | {int(item) for item in reverse_orbit(196)["path"]}
    seeds = frozen_seeds()
    assert set(seeds) <= allowed
    samples = reverse_samples()
    assert {item.source for item in samples} <= allowed
    assert all(item.image == ReverseAddSpec(start=item.source).successors(item.source)[0] for item in samples)
    assert all(item.len_source == bt_length(item.source) for item in samples)
    assert all("mid" not in item.as_dict() for item in samples)
    assert all("weighted_sum" not in item.as_dict() for item in samples)


def test_phase7_does_not_thaw_or_rewrite_history():
    assert "reverse_pair_weighted_phase7" not in DEFAULT_ATTACK_ORDER
    assert "weighted_reverse_pair_interaction" not in DEFAULT_ATTACK_ORDER
    assert "reverse_pair_weighted_phase7" not in EXPERIMENTAL_ATTACKS
    assert "weighted_reverse_pair_interaction" not in EXPERIMENTAL_ATTACKS
    assert DEFAULT_ATTACK_ORDER[-1] == "symmetry"
    verify_manifest(load_v2_3_baseline().manifest)
    phase0 = json.loads(PHASE0_JSON.read_text(encoding="utf-8"))
    phase1 = json.loads(PHASE1_JSON.read_text(encoding="utf-8"))
    phase2 = json.loads(PHASE2_JSON.read_text(encoding="utf-8"))
    phase3 = json.loads(PHASE3_JSON.read_text(encoding="utf-8"))
    phase4 = json.loads(PHASE4_JSON.read_text(encoding="utf-8"))
    phase5 = json.loads(PHASE5_JSON.read_text(encoding="utf-8"))
    phase6 = json.loads(PHASE6_JSON.read_text(encoding="utf-8"))
    assert phase0["experimental_status"] == "PHASE_0_FALSIFIER"
    assert phase1["ranking_phase1_decision"] == "MIXED"
    assert phase2["phase2_decision"] == "MIXED"
    assert phase3["decision"] == "PROMOTE_RESTRICTED"
    assert phase3["experimental_status"] == "PHASE_3_RESTRICTED_SYMBOLIC_ATTACK"
    assert phase4["experimental_status"] == "PHASE_4_REVERSE_ADD_COMPOSITION_FALSIFIER"
    assert phase4["decision"] == "REVERSE_COMPOSITION_NEEDS_RICHER_STRUCTURE"
    assert phase5["experimental_status"] == "PHASE_5_REVERSE_ADD_CARRY_FALSIFIER"
    assert phase5["decision"] == "CARRY_NEEDS_RICHER_STATE"
    assert phase6["experimental_status"] == "PHASE_6_REVERSE_PAIR_INTERACTION_FALSIFIER"
    assert phase6["decision"] == "REVERSE_PAIR_NEEDS_RICHER_STRUCTURE"
