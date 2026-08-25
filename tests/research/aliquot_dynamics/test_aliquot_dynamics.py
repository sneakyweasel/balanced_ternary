"""Frozen-engine campaign on divisor-sum iteration."""

from __future__ import annotations

from pathlib import Path

from research.aliquot_dynamics.discovery import falsify_claims, orbit
from research.aliquot_dynamics.lean_export import LEAN_MODULE, THEOREMS
from research.aliquot_dynamics.problem import PROBLEM
from research.aliquot_dynamics.runner import TARGETS, run_campaign
from research.aliquot_dynamics.spec import MAX_N, map_images, map_spec, transition_status
from research.literature import get_reference
from research.open_problems import get_problem
from research_engine.planner.orchestrator import DEFAULT_ATTACK_ORDER

ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "src" / "research" / "aliquot_dynamics"
FORBIDDEN_SPEC = (
    "aliquot",
    "Catalan",
    "Dickson",
    "Lehmer",
    "amicable",
    "perfect number",
    "sociable",
    "abundant",
    "deficient",
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
            if "aliquot_dynamics.scout" in stripped:
                raise AssertionError(f"{name} imports scout")
    spec = _source_lines("spec.py")
    for token in FORBIDDEN_SPEC:
        assert token not in spec


def test_problem_descriptor_and_prior_art():
    assert get_problem("aliquot_dynamics") is PROBLEM
    assert PROBLEM.docs == ("docs/problems/aliquot_dynamics.md",)
    assert get_reference("oeis-A008892")["project_relationship"] == "known"
    assert get_reference("guy-selfridge-1975-aliquot-drivers")["project_relationship"] == "known"


def test_attack_architecture_remains_frozen():
    assert DEFAULT_ATTACK_ORDER[-1] == "symmetry"
    assert "piecewise_affine" in DEFAULT_ATTACK_ORDER


def test_map_is_a_partial_function_with_budget():
    assert map_images(1) == (0,)
    assert map_images(6) == (6,)
    assert map_images(12) == (16,)
    assert map_images(220) == (284,)
    assert map_images(276) == (396,)
    assert map_images(0) == ()
    assert transition_status(MAX_N + 1) == "TRANSITION_UNRESOLVED"
    assert map_images(MAX_N + 1) == ()


def test_control_orbits():
    halt = orbit(map_spec(start=12), 12)
    assert halt["kind"] == "halt"
    assert halt["path"][-1] == 0
    fixed = orbit(map_spec(start=6), 6)
    assert fixed["kind"] == "cycle"
    assert fixed["path"] == (6,)
    pair = orbit(map_spec(start=220), 220)
    assert pair["kind"] == "cycle"
    assert set(pair["path"]) == {220, 284}


def test_falsification_on_window():
    report = falsify_claims(map_spec(start=12))
    assert report["strict_descent"]["status"] == "REFUTED"
    assert report["strict_descent"]["counterexample"] == 12
    assert report["no_fixed_point"]["counterexample"] == 6


def test_lean_identities_are_known_and_sorry_free():
    path = ROOT / "formal" / "Problems" / "Engine" / "AliquotDynamics.lean"
    text = path.read_text(encoding="utf-8")
    assert "sorry" not in text
    assert "admit" not in text
    assert LEAN_MODULE.replace(".", "/") in "formal/Problems/Engine/AliquotDynamics.lean"
    for name in THEOREMS:
        assert name in text
    assert "Catalan" in text or "276" in text


def test_campaign_runs_unmodified_loop():
    _, report = run_campaign()
    twelve = report.by_target("sigma_minus_n_12")
    six = report.by_target("sigma_minus_n_6")
    pair = report.by_target("sigma_minus_n_220")
    flagship = report.by_target("sigma_minus_n_276")

    assert twelve.extra["yield"]["start_orbit"]["kind"] == "halt"
    assert twelve.extra.get("closure_complete") is True
    assert six.extra.get("closure_size") == 1
    assert pair.extra.get("closure_size") == 2
    assert flagship.decision == "ENGINE_LIMITATION"
    assert flagship.census_kind in {"", "UNRESOLVED"}
    assert "control_word" in flagship.skipped
    prefix = flagship.extra["yield"]["start_orbit"]["path"][:6]
    assert prefix == (276, 396, 696, 1104, 1872, 3770)
    assert flagship.extra["yield"]["start_orbit"]["kind"] == "truncated"
    assert flagship.extra["yield"]["start_status"] != "TRANSITION_UNRESOLVED"
    assert report.selection
    assert report.next_target_overridden is False
    next_summary = next(item for item in report.summaries if item.extra.get("role") == "researchloop_next")
    assert next_summary.extra.get("selection")
    assert TARGETS[-1][0] == "open_flagship"
