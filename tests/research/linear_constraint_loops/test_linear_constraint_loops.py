"""Frozen-engine campaign on one-variable linear-constraint loops."""

from __future__ import annotations

from pathlib import Path

from research.linear_constraint_loops.lean_export import LEAN_MODULE, THEOREMS
from research.linear_constraint_loops.problem import PROBLEM
from research.linear_constraint_loops.runner import TARGETS, run_campaign
from research.linear_constraint_loops.spec import decrement_spec, rplus_images, rplus_spec
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
    next_summary = report.summaries[-1]
    assert next_summary.extra.get("role") == "researchloop_next"
    assert next_summary.extra.get("selection")


def test_decrement_spec_withholds_affine_system():
    spec = decrement_spec()
    assert spec.affine_system() is None
    assert spec.dimension == 1
    rplus = rplus_spec()
    assert rplus.affine_system() is None
    assert TARGETS[0][0] == "simple_termination"
    assert TARGETS[1][0] == "cycle_affine"
    assert TARGETS[2][0] == "open_strip"
