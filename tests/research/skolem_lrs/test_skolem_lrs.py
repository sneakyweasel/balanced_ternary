"""Frozen-engine campaign on companion-window first-coordinate reachability."""

from __future__ import annotations

from pathlib import Path

from research.literature import get_reference
from research.open_problems import get_problem
from research.skolem_lrs.discovery import evidence_state, falsify_claims
from research.skolem_lrs.lean_export import LEAN_MODULE, THEOREMS
from research.skolem_lrs.problem import PROBLEM
from research.skolem_lrs.runner import TARGETS, run_campaign
from research.skolem_lrs.spec import (
    CENSUS_CUBE_SIDE,
    MAX_CENSUS_CELLS,
    next_window,
    order3_spec,
    order6_spec,
    periodic_spec,
    positive_spec,
    skip_attacks_for_dimension,
    zero_small_spec,
)
from research_engine.planner.orchestrator import DEFAULT_ATTACK_ORDER

ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "src" / "research" / "skolem_lrs"
FORBIDDEN_SPEC = (
    "skolem",
    "Skolem",
    "characteristic",
    "closed form",
    "p-adic",
    "padic",
    "MSTV",
    "Baker",
    "Ouaknine",
    "7i",
    "8+i",
    "unresolved",
    "positivity",
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
            if "skolem_lrs.scout" in stripped:
                raise AssertionError(f"{name} imports scout")
    spec = _source_lines("spec.py")
    for token in FORBIDDEN_SPEC:
        assert token not in spec, f"spec.py contains forbidden token {token!r}"


def test_problem_descriptor_and_prior_art():
    assert get_problem("skolem_lrs") is PROBLEM
    assert PROBLEM.docs == ("docs/problems/skolem_lrs.md",)
    assert get_reference("bacik-et-al-2026-skolem-positivity-survey")["project_relationship"] == "known"
    assert get_reference("luca-ouaknine-worrell-2026-conjectural-decidability")["year"] == 2026


def test_attack_architecture_remains_frozen():
    assert DEFAULT_ATTACK_ORDER[-1] == "symmetry"
    assert "vector_affine" in DEFAULT_ATTACK_ORDER
    assert skip_attacks_for_dimension(2) == ()
    assert skip_attacks_for_dimension(3) == ()
    assert "vector_affine" in skip_attacks_for_dimension(6)
    assert CENSUS_CUBE_SIDE ** 6 > MAX_CENSUS_CELLS


def test_windows_satisfy_the_declared_linear_step():
    small = zero_small_spec()
    assert next_window(small.window, small.last_row) == (-6, -4)
    assert evidence_state(small)["zero_at"] == 3
    assert evidence_state(positive_spec())["zero_at"] is None
    assert evidence_state(periodic_spec())["zero_at"] == 1
    assert min(evidence_state(order3_spec())["values"]) > 0
    flag = evidence_state(order6_spec())
    assert flag["values"][:6] == (12, 49, 374, 6003, 21520, 150773)
    assert flag["first_negative"] == 11
    assert flag["zero_at"] is None
    assert flag["status"] == "FINITE_ZERO_FREE"
    assert flag["computation"] == "COMPUTATION_EXHAUSTED"
    assert flag["universal_zero_free"] is False


def test_falsification_distinguishes_witness_from_universal():
    small = falsify_claims(zero_small_spec())
    assert small["never_vanishes"]["status"] == "REFUTED"
    assert small["never_vanishes"]["counterexample"] == 3
    flag = falsify_claims(order6_spec())
    assert flag["fixed_sign"]["status"] == "REFUTED"
    assert flag["fixed_sign"]["counterexample"] == 11
    assert flag["modulus_excludes_zero"]["status"] == "NO_PREFIX_EXCLUSION"
    assert flag["never_vanishes"]["status"] == "INCONCLUSIVE"


def test_lean_identities_are_known_and_sorry_free():
    path = ROOT / "formal" / "Problems" / "Engine" / "CompanionShift.lean"
    text = path.read_text(encoding="utf-8")
    assert "sorry" not in text
    assert "admit" not in text
    assert LEAN_MODULE.replace(".", "/") in "formal/Problems/Engine/CompanionShift.lean"
    for name in THEOREMS:
        assert name in text
    assert "Skolem theorem" in text or "not a Skolem" in text


def test_campaign_runs_unmodified_loop():
    _, report = run_campaign()
    small = report.by_target("companion_shift_zero_small")
    positive = report.by_target("companion_shift_positive")
    periodic = report.by_target("companion_shift_periodic")
    order3 = report.by_target("companion_shift_order3")
    flagship = report.by_target("companion_shift_order6")

    assert small.extra["yield"]["evidence"]["status"] == "ZERO_WITNESS"
    assert small.extra.get("closure_zero") is True
    assert positive.extra["yield"]["evidence"]["zero_at"] is None
    assert positive.census_kind in {"FINITE_CENSUS", "PARAMETERIZED_CENSUS"}
    assert periodic.extra["yield"]["evidence"]["zero_at"] == 1
    assert order3.census_kind in {"", "UNRESOLVED"}
    assert flagship.extra["skip_attacks"]
    assert flagship.extra["attack_table"].get("vector_affine") == "COMPUTATION_EXHAUSTED"
    assert flagship.extra["yield"]["evidence"]["zero_at"] is None
    assert flagship.extra["yield"]["evidence"]["first_negative"] == 11
    assert flagship.extra["yield"]["Engineering changes"] == 0
    assert report.selection
    assert report.next_target_overridden is False
    next_summary = next(item for item in report.summaries if item.extra.get("role") == "researchloop_next")
    assert next_summary.extra.get("selection")
    assert TARGETS[-1][0] == "open_flagship"
