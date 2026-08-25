"""Frozen-engine campaign on the BB-5 generalized Collatz map."""

from __future__ import annotations

from pathlib import Path

from research.bb5_map.discovery import falsify_claims, orbit
from research.bb5_map.lean_export import LEAN_MODULE, THEOREMS
from research.bb5_map.problem import PROBLEM
from research.bb5_map.runner import run_campaign
from research.bb5_map.spec import map_images, map_spec
from research.literature import get_reference
from research.open_problems import get_problem
from research_engine.planner.orchestrator import DEFAULT_ATTACK_ORDER

ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "src" / "research" / "bb5_map"
FORBIDDEN_SPEC = (
    "Collatz",
    "Michel",
    "Busy Beaver",
    "BB-5",
    "BB(5)",
    "residue class",
    "Marxen",
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
            if "bb5_map.scout" in stripped:
                raise AssertionError(f"{name} imports scout")
    spec = _source_lines("spec.py")
    for token in FORBIDDEN_SPEC:
        assert token not in spec


def test_problem_descriptor_and_prior_art():
    assert get_problem("bb5_map") is PROBLEM
    assert PROBLEM.docs == ("docs/problems/bb5_map.md",)
    rec = get_reference("yolcu-aaronson-heule-2023-automated-collatz")
    assert rec["year"] == 2023
    assert rec["project_relationship"] == "known"
    assert get_reference("michel-2015-busy-beaver-number-theory")["project_relationship"] == "known"
    assert get_reference("bbchallenge-2025-fifth-busy-beaver")["project_relationship"] == "known"


def test_attack_architecture_remains_frozen():
    assert DEFAULT_ATTACK_ORDER[-1] == "symmetry"
    assert "piecewise_affine" in DEFAULT_ATTACK_ORDER
    assert DEFAULT_ATTACK_ORDER.index("matrix_word_invariant") == DEFAULT_ATTACK_ORDER.index("vector_affine") + 1


def test_map_is_a_partial_function_on_nonnegatives():
    defined = {x: map_images(x) for x in range(0, 40)}
    assert defined[0] == (6,)
    assert defined[1] == (9,)
    assert defined[2] == ()
    assert defined[6] == (16,)
    assert map_images(-9) == ()
    for images in defined.values():
        assert len(images) <= 1


def test_seed_zero_orbit_reaches_an_empty_menu():
    spec = map_spec()
    path = orbit(spec, 0)
    assert path[0] == 0
    assert path[-1] == 12284
    assert spec.successors(path[-1]) == ()
    assert spec.affine_system() is None


def test_lean_identities_are_known_and_sorry_free():
    path = ROOT / "formal" / "Problems" / "Engine" / "BB5Map.lean"
    text = path.read_text(encoding="utf-8")
    assert "sorry" not in text
    assert "admit" not in text
    assert LEAN_MODULE.replace(".", "/") in "formal/Problems/Engine/BB5Map.lean"
    for name in THEOREMS:
        assert name in text
    assert "Busy Beaver" in text or "Collatz" in text


def test_campaign_runs_unmodified_loop():
    _, report = run_campaign()
    summary = report.by_target("partial_five_three")
    assert summary.census_kind == "FINITE_CENSUS"
    assert summary.extra["yield"]["structure_origin"] == "DISCOVERED"
    assert "control_word" not in summary.skipped
    assert "CLASS" in summary.obstruction_scopes
    branches = summary.extra.get("branches") or ()
    pairs = {(int(item["p"]), int(item["q"]), int(item["r"])) for item in branches}
    assert (5, 3, 18) in pairs
    assert (5, 3, 22) in pairs
    regions = {item["region"]["modulus"] for item in branches if item.get("region")}
    assert 3 in regions
    assert summary.extra.get("control_structure") == "SINGLETON"
    assert summary.extra["orbit_start"][-1] == 12284
    falsify = summary.extra["yield"]["falsify"]
    assert falsify["monotone_descent"]["holds_on_window"] is False
    assert falsify["empirical_termination"]["status"] == "CERTIFIED_ON_WINDOW"
    assert summary.decision in {"CONTINUE", "FAMILY_SATURATED"}
