"""Live Phase-6 reverse-add pairwise word-interaction falsifier."""

from __future__ import annotations

import json

from bt.normalization import add_with_trace
from bt.representation import digits, encode
from bt.sequences import bt_length, bt_reverse
from research.research_control.ranking_phase0 import JSON_PATH as PHASE0_JSON
from research.research_control.ranking_phase1 import JSON_PATH as PHASE1_JSON
from research.research_control.reverse_add_carry_phase5 import JSON_PATH as PHASE5_JSON
from research.research_control.reverse_add_composition_phase4 import JSON_PATH as PHASE4_JSON
from research.research_control.reverse_add_pair_interaction_phase6 import (
    DOC_PATH,
    JSON_PATH,
    SPECIAL_PROBE_ROLES,
    frozen_seeds,
    pair_sample_for,
    reverse_samples,
    run_phase6,
    write_artifacts,
)
from research.research_control.symbolic_composition_phase2 import JSON_PATH as PHASE2_JSON
from research.research_control.symbolic_composition_phase3 import JSON_PATH as PHASE3_JSON
from research.reverse_and_add_base3.discovery import WINDOW as REVERSE_WINDOW
from research.reverse_and_add_base3.discovery import orbit as reverse_orbit
from research.reverse_and_add_base3.spec import ReverseAddSpec, map_images
from research_engine.control.baseline import load_v2_3_baseline, verify_manifest
from research_engine.control.reverse_add_pair_interaction import (
    ReversePairClass,
    pair_sums_lsd,
    ranked_candidates,
)
from research_engine.control.types import ENGINE_CONTROL_VERSION
from research_engine.planner.orchestrator import DEFAULT_ATTACK_ORDER, EXPERIMENTAL_ATTACKS


def test_pair_construction_canonical_reversal_and_probes():
    zero = pair_sample_for(0, image=0)
    assert zero.pair_sums == (0,)
    pal = pair_sample_for(1, image=2)
    assert pal.pair_sums == (2,)
    assert pal.p2 == 1 and pal.p0 == 0
    neg = pair_sample_for(-1, image=-2)
    assert neg.pair_sums == (-2,)
    revneg = pair_sample_for(2, image=0)
    assert bt_reverse(2) == -2
    assert revneg.pair_sums == (0, 0)
    assert revneg.p0 == 2 and revneg.p2 == 0
    five = pair_sample_for(5, image=-6)
    assert five.image == 5 + bt_reverse(5)
    assert five.pair_sums == pair_sums_lsd(digits(encode(5)), digits(encode(bt_reverse(5))))
    trace = add_with_trace(encode(5), encode(bt_reverse(5)))
    assert five.pair_sums == tuple(step.left + step.right for step in trace.steps)
    assert ReverseAddSpec(start=5).successors(5) == map_images(5) == (five.image,)
    assert pair_sample_for(8, image=0).pair_sums == (0, 0, 0)
    seed = pair_sample_for(196, image=392)
    assert seed.w_source == 196
    assert seed.length_delta == 1


def test_phase6_three_candidates_and_artifacts():
    samples, outcomes, classification, _reason = run_phase6()
    assert [item.rank for item in outcomes] == [1, 2, 3]
    assert len(ranked_candidates()) == 3
    by_name = {item.name: item for item in outcomes}
    cancel = by_name["cancellation_majority_blocks_growth"]
    sign = by_name["pair_sign_imbalance_matches_successor_sign"]
    top = by_name["length_growth_requires_top_pair"]
    assert cancel.survived is True
    assert cancel.counterexample is None
    assert sign.survived is False
    assert sign.failure_class == "SIGN_IMBALANCE_MISMATCH"
    assert sign.counterexample is not None
    assert sign.counterexample.source == -672
    assert sign.counterexample.image == -448
    assert top.survived is True
    assert classification is ReversePairClass.REVERSE_PAIR_NEEDS_RICHER_STRUCTURE
    payload = write_artifacts(samples)
    assert payload["engine_control_version"] == ENGINE_CONTROL_VERSION
    assert payload["source_engine"] == "v2.3"
    assert payload["experimental_status"] == "PHASE_6_REVERSE_PAIR_INTERACTION_FALSIFIER"
    assert payload["decision"] == "REVERSE_PAIR_NEEDS_RICHER_STRUCTURE"
    assert payload["green_loot"] == "NO_NEW_LOOT"
    assert payload["lean_status"] == "FORMALIZATION_BLOCKED"
    assert payload["composition_depth"] == 1
    assert payload["target"] == "reverse_and_add_base3"
    assert "s_i" in payload["pair_definition"]
    assert payload["canonical_digit_convention"]["digit_index"].startswith("LSD-first")
    assert {probe["source"] for probe in payload["special_probes"]} == set(SPECIAL_PROBE_ROLES)
    names = [item["attack_name"] for item in payload["top3_update"]["proposals"]]
    assert names[0] == "symbolic_nonlinear_composition"
    assert "reverse_pair_interaction" not in names
    assert JSON_PATH.is_file()
    assert DOC_PATH.is_file()
    text = DOC_PATH.read_text(encoding="utf-8")
    assert "REVERSE_PAIR_NEEDS_RICHER_STRUCTURE" in text
    assert "NO_NEW_LOOT" in text
    assert payload["transition_window"]["sample_count"] == len(samples)
    assert payload["transition_window"]["composition_depth"] == 1


def test_phase6_does_not_expand_census_or_composition_depth():
    allowed = set(REVERSE_WINDOW) | {int(item) for item in reverse_orbit(196)["path"]}
    seeds = frozen_seeds()
    assert set(seeds) <= allowed
    samples = reverse_samples()
    assert {item.source for item in samples} <= allowed
    assert all(item.image == ReverseAddSpec(start=item.source).successors(item.source)[0] for item in samples)
    assert all(item.len_source == bt_length(item.source) for item in samples)
    assert all("mid" not in item.as_dict() for item in samples)


def test_phase6_does_not_thaw_or_rewrite_history():
    assert "reverse_pair_phase6" not in DEFAULT_ATTACK_ORDER
    assert "reverse_pair_interaction" not in DEFAULT_ATTACK_ORDER
    assert "reverse_pair_phase6" not in EXPERIMENTAL_ATTACKS
    assert "reverse_pair_interaction" not in EXPERIMENTAL_ATTACKS
    assert DEFAULT_ATTACK_ORDER[-1] == "symmetry"
    verify_manifest(load_v2_3_baseline().manifest)
    phase0 = json.loads(PHASE0_JSON.read_text(encoding="utf-8"))
    phase1 = json.loads(PHASE1_JSON.read_text(encoding="utf-8"))
    phase2 = json.loads(PHASE2_JSON.read_text(encoding="utf-8"))
    phase3 = json.loads(PHASE3_JSON.read_text(encoding="utf-8"))
    phase4 = json.loads(PHASE4_JSON.read_text(encoding="utf-8"))
    phase5 = json.loads(PHASE5_JSON.read_text(encoding="utf-8"))
    assert phase0["experimental_status"] == "PHASE_0_FALSIFIER"
    assert phase1["ranking_phase1_decision"] == "MIXED"
    assert phase2["phase2_decision"] == "MIXED"
    assert phase3["decision"] == "PROMOTE_RESTRICTED"
    assert phase3["experimental_status"] == "PHASE_3_RESTRICTED_SYMBOLIC_ATTACK"
    assert phase4["experimental_status"] == "PHASE_4_REVERSE_ADD_COMPOSITION_FALSIFIER"
    assert phase4["decision"] == "REVERSE_COMPOSITION_NEEDS_RICHER_STRUCTURE"
    assert phase5["experimental_status"] == "PHASE_5_REVERSE_ADD_CARRY_FALSIFIER"
    assert phase5["decision"] == "CARRY_NEEDS_RICHER_STATE"
