"""Lychrel dynamics is registered, not attacked."""

from __future__ import annotations

from pathlib import Path

import pytest

from research.literature import get_reference
from research.lychrel_dynamics.attack_families import (
    CANDIDATE_ATTACK_FAMILIES,
    CANDIDATE_ATTACK_FAMILY_IDS,
)
from research.lychrel_dynamics.problem import PROBLEM
from research.lychrel_dynamics.registry import (
    LEAN_PROSPECTIVE_OBJECTS,
    LITERATURE_IDS,
    PHASE_REPORT,
    RECORD,
    REQUIRED_SCHEMA_FIELDS,
)
from research.open_problems import get_problem
from research_engine.control.proposals import assert_not_executable
from research_engine.planner.orchestrator import (
    DEFAULT_ATTACK_ORDER,
    EXPERIMENTAL_ATTACKS,
    run_named_attack,
)

ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "src" / "research" / "lychrel_dynamics"


def test_problem_descriptor_is_registered():
    assert get_problem("lychrel_dynamics") is PROBLEM
    assert PROBLEM.id == "lychrel_dynamics"
    assert PROBLEM.status == "EXPLORATORY"
    assert PROBLEM.docs == ("docs/problems/lychrel_dynamics.md",)
    assert not PROBLEM.lean
    assert not PROBLEM.conjectures
    dossier = ROOT / "docs" / "problems" / "lychrel_dynamics.md"
    assert dossier.is_file()
    text = dossier.read_text(encoding="utf-8")
    assert "## Branch budget" in text
    assert "## Decision" in text
    assert "PARK" in text
    assert "## Publication assessment" in text


def test_pipeline_record_has_required_schema():
    payload = RECORD.as_dict()
    for field in REQUIRED_SCHEMA_FIELDS:
        assert field in payload
        assert getattr(RECORD, field) is not None
    assert RECORD.problem_id == "lychrel_dynamics"
    assert RECORD.status == "open"
    assert RECORD.difficulty == "high"
    assert RECORD.novelty_risk == "very_high"
    assert RECORD.attack_style == "structural"
    assert RECORD.primary_representation == "digit_transducer"
    assert RECORD.domain == (
        "discrete_dynamics",
        "automata",
        "number_theory",
        "symbolic_dynamics",
    )
    assert RECORD.canonical_parameters["canonical_base"] == 10
    assert RECORD.canonical_parameters["secondary_base"] == 3
    assert RECORD.canonical_parameters["balanced_ternary_branch"] == "exploratory"
    assert RECORD.distinct_from == "reverse_and_add_base3"
    assert RECORD.attack_executed is False
    assert "expected_research_value" not in payload
    assert "score_milli" not in payload


def test_novelty_review_is_required_and_incomplete():
    assert RECORD.novelty_review_required is True
    assert RECORD.novelty_review_complete is False
    assert PHASE_REPORT["novelty_review_required"] is True
    incomplete = [item for item in RECORD.novelty_review_checklist if not item.complete]
    assert incomplete
    assert any(item.item_id == "prior_fst_automata_formulations" for item in incomplete)


def test_qualitative_score_is_labels_only():
    score = RECORD.qualitative_score
    assert score.new_math_probability == "high"
    assert score.frontier_strength == "high"
    assert score.lean_path == "high"
    assert score.cost == "medium_high"
    assert score.novelty_risk == "very_high"
    assert "outrank" in score.intended_consequence


def test_known_instances_are_computational_candidates_not_theorems():
    by_id = {item.instance_id: item for item in RECORD.known_instances}
    decimal = by_id["decimal_196"]
    ternary = by_id["base3_103"]
    assert decimal.seed == 196
    assert decimal.base == 10
    assert decimal.evidence_kind == "known_computational_evidence"
    assert decimal.mathematical_status == "not_a_proof"
    assert decimal.conjectural_status == "literature_candidate"
    assert ternary.seed == 103
    assert ternary.base == 3
    assert ternary.mathematical_status == "not_a_proof"
    notes = RECORD.research_notes.lower()
    assert "computational evidence" in notes
    assert "mathematical proof" in notes
    assert "conjectural" in notes


def test_candidate_attack_families_are_registered_and_not_executable():
    assert PHASE_REPORT["new_attack_family_registered"] is True
    assert RECORD.recommended_attack_families == CANDIDATE_ATTACK_FAMILY_IDS
    assert CANDIDATE_ATTACK_FAMILY_IDS == (
        "digit_transducer",
        "residual_state_analysis",
        "palindrome_separation",
        "forbidden_pattern_search",
        "potential_energy",
    )
    assert len(CANDIDATE_ATTACK_FAMILIES) == 5
    for family in CANDIDATE_ATTACK_FAMILIES:
        assert family.executable is False
        assert family.family_id not in DEFAULT_ATTACK_ORDER
        assert family.family_id not in EXPERIMENTAL_ATTACKS
        assert_not_executable(family.family_id)
        with pytest.raises(KeyError):
            run_named_attack(family.family_id, None, None)


def test_attack_architecture_remains_frozen():
    assert PHASE_REPORT["default_attack_order_changed"] is False
    assert DEFAULT_ATTACK_ORDER[-1] == "symmetry"
    assert "piecewise_affine" in DEFAULT_ATTACK_ORDER
    assert "reverse" in DEFAULT_ATTACK_ORDER
    assert "reverse_add" not in DEFAULT_ATTACK_ORDER
    assert "lychrel" not in DEFAULT_ATTACK_ORDER
    assert "digit_transducer" not in DEFAULT_ATTACK_ORDER
    assert EXPERIMENTAL_ATTACKS == frozenset(
        {"restricted_symbolic_composition", "odd_even_two_step_decrease"}
    )


def test_no_attack_modules_or_execution():
    assert PHASE_REPORT["problem_registered"] is True
    assert PHASE_REPORT["attack_executed"] is False
    for name in ("runner.py", "adapter.py", "spec.py", "scout.py", "planner.py"):
        assert not (SRC / name).exists()
    assert RECORD.lean_prospective_objects == LEAN_PROSPECTIVE_OBJECTS
    assert "PalReach" in LEAN_PROSPECTIVE_OBJECTS


def test_literature_ids_resolve():
    assert RECORD.literature_ids == LITERATURE_IDS
    for ref_id in LITERATURE_IDS:
        rec = get_reference(ref_id)
        assert rec["id"] == ref_id
        assert rec["project_relationship"] == "known"
