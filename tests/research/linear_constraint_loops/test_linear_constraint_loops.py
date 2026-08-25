"""Frozen-engine campaign on one-variable linear-constraint loops."""

from __future__ import annotations

from pathlib import Path

from research.linear_constraint_loops.discovery import existential_cycle_witness, quantifier_report, universal_termination_on_seeds
from research.linear_constraint_loops.lean_export import LEAN_MODULE, THEOREMS
from research.linear_constraint_loops.planner import plan_loop_session
from research.linear_constraint_loops.problem import PROBLEM
from research.linear_constraint_loops.runner import TARGETS, run_campaign
from research.linear_constraint_loops.spec import decrement_spec, rplus_images, rplus_spec, sum_strip_images, sum_strip_spec
from research.linear_constraint_loops.synthetics import (
    decrement_or_double_spec,
    dual_decrement_spec,
    stay_or_decrement_spec,
    two_affine_spec,
)
from research.literature import get_reference
from research.open_problems import get_problem
from research_engine.planner.orchestrator import DEFAULT_ATTACK_ORDER

ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "src" / "research" / "linear_constraint_loops"
FORBIDDEN_SPEC = (
    "Collatz",
    "Carelli",
    "Reachability",
    "residue class",
    "parity vector",
    "cyclic trace",
)


def _source_lines(name: str) -> str:
    return (SRC / name).read_text(encoding="utf-8")


def test_adapter_sources_are_blind_and_do_not_import_scout():
    for name in ("spec.py", "adapter.py", "planner.py"):
        text = _source_lines(name)
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.startswith("from research.collatz") or stripped.startswith("import research.collatz"):
                raise AssertionError(f"{name} imports research.collatz")
            if "linear_constraint_loops.scout" in stripped:
                raise AssertionError(f"{name} imports scout")
    spec = _source_lines("spec.py")
    for token in FORBIDDEN_SPEC:
        assert token not in spec


def test_problem_descriptor_and_prior_art():
    assert get_problem("linear_constraint_loops") is PROBLEM
    assert PROBLEM.docs == ("docs/problems/linear_constraint_loops.md",)
    rec = get_reference("carelli-2026-loop-termination")
    assert rec["year"] == 2026
    assert rec["project_relationship"] == "known"
    assert get_reference("matthews-watts-1984-generalization-hasse")["project_relationship"] == "known"
    assert get_reference("braverman-2006-termination-integer-linear")["project_relationship"] == "known"


def test_attack_architecture_remains_frozen():
    assert DEFAULT_ATTACK_ORDER[-1] == "symmetry"
    assert "piecewise_affine" in DEFAULT_ATTACK_ORDER
    assert DEFAULT_ATTACK_ORDER.index("matrix_word_invariant") == DEFAULT_ATTACK_ORDER.index("vector_affine") + 1


def test_rplus_integer_graph_is_a_partial_function():
    defined = {x: rplus_images(x) for x in range(0, 40)}
    assert defined[3] == ()
    assert defined[6] == ()
    assert defined[4] == (5,)
    assert defined[5] == (6,)
    assert defined[8] == (10,)
    for images in defined.values():
        assert len(images) <= 1


def test_lean_identities_are_known_and_sorry_free():
    path = ROOT / "formal" / "Problems" / "Engine" / "LinearConstraintLoops.lean"
    text = path.read_text(encoding="utf-8")
    assert "sorry" not in text
    assert "admit" not in text
    assert LEAN_MODULE.replace(".", "/") in "formal/Problems/Engine/LinearConstraintLoops.lean"
    for name in THEOREMS:
        assert name in text
    assert "Reachability Conjecture" in text or "Reachability" in text


def test_campaign_runs_unmodified_loop():
    _, report = run_campaign()
    decrement = report.by_target("slc_decrement")
    negation = report.by_target("slc_negation")
    rplus = report.by_target("slc_rplus")

    assert decrement.census_kind == "FINITE_CENSUS"
    assert decrement.extra["yield"]["structure_origin"] == "GIVEN BY THE ADAPTER"
    assert "control_word" not in decrement.skipped
    assert "WORD" in decrement.obstruction_scopes

    assert negation.census_kind in {"", "UNRESOLVED"}
    assert "control_word" in negation.skipped or negation.census_kind == "UNRESOLVED"
    assert "parameter_domain" in negation.skipped

    assert rplus.census_kind == "FINITE_CENSUS"
    assert rplus.extra["yield"]["structure_origin"] == "DISCOVERED"
    branches = rplus.extra.get("branches") or ()
    pairs = {(int(item["p"]), int(item["q"]), int(item["r"])) for item in branches}
    assert (4, 3, -1) in pairs
    assert (4, 3, -2) in pairs
    assert "CLASS" in rplus.obstruction_scopes
    regions = {item["region"]["modulus"] for item in branches if item.get("region")}
    assert 3 in regions

    assert report.selection
    assert report.selection[0].value > 0
    assert report.next_target_name == report.selection[0].name
    assert report.next_target_overridden is False
    assert report.next_target_name in {
        "slc_increment",
        "mx_plus_r_7_1",
        "hidden_congruence_a",
        "hidden_vector_parity_shear",
        "integer_polynomial_x2_minus_2",
    }
    next_summary = next(item for item in report.summaries if item.extra.get("role") == "researchloop_next")
    assert next_summary.extra.get("selection")

    strip = report.by_target("slc_sum_strip")
    assert strip.extra.get("role") == "nondeterministic_slc"
    assert strip.extra.get("control_structure") == "BRANCHING"
    assert "piecewise_affine" in strip.skipped
    assert "control_word" in strip.skipped
    assert "control_obstruction" in strip.skipped
    assert strip.extra.get("piecewise_affine_applicable") is False
    quant = strip.extra["yield"]["quantifiers"]
    assert quant["existential_cycle"]["status"] == "EXISTENTIAL_WITNESS"
    assert quant["universal_termination"]["status"] == "REFUTED"
    assert quant["universal_termination"]["holds"] is False
    assert quant["all_paths_cycle"]["status"] == "UNKNOWN"
    assert quant["discovered_result_class"] == "EXISTENTIAL"


def test_decrement_spec_withholds_affine_system():
    spec = decrement_spec()
    assert spec.affine_system() is None
    assert spec.dimension == 1
    rplus = rplus_spec()
    assert rplus.affine_system() is None
    assert TARGETS[0][0] == "simple_termination"
    assert TARGETS[1][0] == "cycle_affine"
    assert TARGETS[2][0] == "open_strip"


def test_sum_strip_is_a_three_valued_relation():
    assert sum_strip_images(5) == (-6, -5, -4)
    assert len(sum_strip_images(0)) == 3
    spec = sum_strip_spec()
    assert spec.affine_system() is None
    assert len(spec.legal_controls(spec.initial_state, spec.initial_phase())) == 3


def test_synthetics_preserve_quantifier_discipline():
    two = two_affine_spec()
    stay = stay_or_decrement_spec()
    dual = dual_decrement_spec()
    trap = decrement_or_double_spec()
    assert len(two.successors(3)) == 2
    cycle = existential_cycle_witness(stay)
    assert cycle is not None
    stay_univ = universal_termination_on_seeds(stay, window=tuple(range(0, 6)))
    assert stay_univ["status"] == "REFUTED"
    assert stay_univ["holds"] is False
    assert stay_univ["quantifier"] == "UNIVERSAL"
    dual_univ = universal_termination_on_seeds(dual, window=tuple(range(0, 8)), max_depth=12)
    assert dual_univ["status"] == "CERTIFIED_ON_WINDOW"
    assert dual_univ["holds"] is True
    dual_unknown = universal_termination_on_seeds(dual, window=tuple(range(0, 40)), max_depth=8)
    assert dual_unknown["status"] == "UNKNOWN"
    assert dual_unknown["holds"] is None
    trap_q = quantifier_report(trap)
    assert trap_q["existential_cycle"]["status"] == "EXISTENTIAL_WITNESS"
    assert trap_q["universal_termination"]["status"] == "REFUTED"
    two_q = quantifier_report(two)
    assert two_q["existential_cycle"]["status"] == "EXISTENTIAL_WITNESS"
    assert two_q["universal_termination"]["status"] == "REFUTED"
    assert two_q["all_paths_cycle"]["status"] == "UNKNOWN"


def test_frozen_census_is_inapplicable_on_branching_start():
    for spec in (
        two_affine_spec(),
        stay_or_decrement_spec(),
        dual_decrement_spec(),
        decrement_or_double_spec(),
        sum_strip_spec(),
    ):
        session = plan_loop_session(spec, record=False)
        skipped = {item.attack for item in session.attack_report.skipped}
        assert "piecewise_affine" in skipped
        assert "control_word" in skipped
        assert session.diagnosis.fingerprint.control_structure == "BRANCHING"
        assert session.diagnosis.fingerprint.transition_architecture == "BRANCHING"


def test_quotient_alphabet_is_start_local_on_finite_branching():
    spec = stay_or_decrement_spec()
    session = plan_loop_session(spec, record=False)
    closure = next(item for item in session.attack_report.results if item.name == "closure")
    quotient = next(item for item in session.attack_report.results if item.name == "quotient")
    assert closure.status.value == "SUPPORTED"
    assert closure.evidence.get("complete") is True
    assert quotient.status.value == "SUPPORTED"
    assert quotient.evidence.get("alphabet_size") == len(spec.successors(spec.start))
    assert spec.successors(1) != spec.successors(spec.start)
