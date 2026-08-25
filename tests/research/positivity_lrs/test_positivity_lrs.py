"""Frozen-engine campaign on companion-window first-coordinate nonnegativity."""

from __future__ import annotations

from pathlib import Path

from research.literature import get_reference
from research.open_problems import get_problem
from research.positivity_lrs.discovery import evidence_state, falsify_claims
from research.positivity_lrs.lean_export import LEAN_MODULE, THEOREMS
from research.positivity_lrs.problem import PROBLEM
from research.positivity_lrs.runner import TARGETS, run_campaign
from research.positivity_lrs.spec import (
    CENSUS_CUBE_SIDE,
    MAX_CENSUS_CELLS,
    early_negative_spec,
    finite_negative_spec,
    next_window,
    nonneg_small_spec,
    order10_spec,
    order3_spec,
    periodic_sign_spec,
    skip_attacks_for_dimension,
)
from research_engine.memory.types import FailureClass
from research_engine.planner.orchestrator import DEFAULT_ATTACK_ORDER

ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "src" / "research" / "positivity_lrs"
FORBIDDEN_SPEC = (
    "positivity",
    "Positivity",
    "characteristic",
    "closed form",
    "p-adic",
    "padic",
    "Baker",
    "Ouaknine",
    "Bacik",
    "Skolem",
    "skolem",
    "unresolved",
    "Gaussian",
    "7i",
    "8+i",
    "MSTV",
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
            if "positivity_lrs.scout" in stripped:
                raise AssertionError(f"{name} imports scout")
    spec = _source_lines("spec.py")
    for token in FORBIDDEN_SPEC:
        assert token not in spec, f"spec.py contains forbidden token {token!r}"


def test_problem_descriptor_and_prior_art():
    assert get_problem("positivity_lrs") is PROBLEM
    assert PROBLEM.docs == ("docs/problems/positivity_lrs.md",)
    assert get_reference("bacik-et-al-2026-skolem-positivity-survey")["project_relationship"] == "known"
    assert get_reference("ouaknine-worrell-2014-simple-positivity")["year"] == 2014


def test_attack_architecture_remains_frozen():
    assert DEFAULT_ATTACK_ORDER[-1] == "symmetry"
    assert "vector_affine" in DEFAULT_ATTACK_ORDER
    assert skip_attacks_for_dimension(2) == ()
    assert skip_attacks_for_dimension(3) == ()
    assert "vector_affine" in skip_attacks_for_dimension(10)
    assert CENSUS_CUBE_SIDE**10 > MAX_CENSUS_CELLS


def test_windows_satisfy_the_declared_linear_step():
    grow = nonneg_small_spec()
    assert next_window(grow.window, grow.last_row) == (1, 2)
    assert evidence_state(grow)["first_negative"] is None
    assert evidence_state(grow)["status"] == "CERTIFIED_ON_WINDOW"
    assert evidence_state(grow)["universal_nonneg"] is False
    early = evidence_state(early_negative_spec())
    assert early["first_negative"] == 1
    assert early["status"] == "NEGATIVE_WITNESS"
    periodic = evidence_state(periodic_sign_spec())
    assert periodic["first_negative"] == 2
    mixed = evidence_state(finite_negative_spec())
    assert mixed["first_negative"] == 1
    assert mixed["last_negative"] == 3
    assert mixed["eventual_nonneg_candidate"] is True
    assert min(evidence_state(order3_spec())["values"]) > 0
    flag = evidence_state(order10_spec())
    assert flag["values"][:10] == (
        35,
        574,
        34592,
        8999992,
        115734548,
        5682747424,
        1837938758372,
        13061285121472,
        397924220049188,
        290333397927490624,
    )
    assert flag["first_negative"] is None
    assert flag["status"] == "CERTIFIED_ON_WINDOW"
    assert flag["computation"] == "COMPUTATION_EXHAUSTED"
    assert flag["universal"] == "UNKNOWN"


def test_falsification_distinguishes_witness_from_universal():
    early = falsify_claims(early_negative_spec())
    assert early["all_terms_nonneg"]["status"] == "REFUTED"
    assert early["all_terms_nonneg"]["counterexample"] == 1
    mixed = falsify_claims(finite_negative_spec())
    assert mixed["eventual_nonneg_from_n0"]["status"] == "REFUTED"
    flag = falsify_claims(order10_spec())
    assert flag["all_terms_nonneg"]["status"] == "INCONCLUSIVE"
    assert flag["positive_orthant_invariant"]["status"] == "REFUTED"
    assert flag["residue_quotient_proves_nonneg"]["status"] == "INCONCLUSIVE"


def test_lean_identities_are_known_and_sorry_free():
    path = ROOT / "formal" / "Problems" / "Engine" / "CompanionObservation.lean"
    text = path.read_text(encoding="utf-8")
    assert "sorry" not in text
    assert "admit" not in text
    assert LEAN_MODULE.replace(".", "/") in "formal/Problems/Engine/CompanionObservation.lean"
    for name in THEOREMS:
        assert name in text
    assert "not a Positivity theorem" in text


def test_campaign_runs_unmodified_loop():
    _, report = run_campaign()
    grow = report.by_target("companion_obs_nonneg_small")
    early = report.by_target("companion_obs_early_negative")
    periodic = report.by_target("companion_obs_periodic_sign")
    mixed = report.by_target("companion_obs_finite_negative")
    order3 = report.by_target("companion_obs_order3")
    flagship = report.by_target("companion_obs_order10")

    assert grow.extra["yield"]["evidence"]["status"] == "CERTIFIED_ON_WINDOW"
    assert grow.extra["yield"]["evidence"]["orthant_invariant"] is True
    assert early.extra["yield"]["evidence"]["status"] == "NEGATIVE_WITNESS"
    assert early.extra.get("closure_negative") is True
    assert periodic.extra["yield"]["evidence"]["first_negative"] == 2
    assert mixed.extra["yield"]["evidence"]["eventual_nonneg_candidate"] is True
    assert mixed.extra["yield"]["evidence"]["status"] == "NEGATIVE_WITNESS"
    assert order3.census_kind in {"", "UNRESOLVED"}
    assert flagship.extra["skip_attacks"]
    assert flagship.extra["attack_table"].get("vector_affine") == "COMPUTATION_EXHAUSTED"
    assert flagship.extra["yield"]["evidence"]["first_negative"] is None
    assert flagship.extra["yield"]["evidence"]["universal_nonneg"] is False
    assert FailureClass.GLOBAL_REASONING.value in flagship.extra["failure_classes"]
    assert flagship.extra["yield"]["Engineering changes"] == 0
    assert report.selection
    assert report.next_target_overridden is False
    next_summary = next(item for item in report.summaries if item.extra.get("role") == "researchloop_next")
    assert next_summary.extra.get("selection")
    assert TARGETS[-1][0] == "open_flagship"
    assert report.memory is not None
    stored = report.memory.get("companion_obs_order10")
    assert any(item.failure_class is FailureClass.GLOBAL_REASONING for item in stored.failures)
