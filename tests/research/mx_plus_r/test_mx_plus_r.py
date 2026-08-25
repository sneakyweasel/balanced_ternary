"""Hint-free accelerated (mx+r) adapter. Does not import research.collatz."""

from __future__ import annotations

from pathlib import Path

from research.literature import get_reference
from research.mx_plus_r.problem import PROBLEM
from research.mx_plus_r.spec import mx_plus_r_spec, mx_plus_r_step
from research.open_problems import get_problem


def test_adapter_sources_do_not_import_collatz():
    root = Path(__file__).resolve().parents[3] / "src" / "research" / "mx_plus_r"
    for path in root.glob("*.py"):
        for line in path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped.startswith("from research.collatz") or stripped.startswith("import research.collatz"):
                raise AssertionError(f"{path.name} imports research.collatz")


def test_step_preserves_positive_odds():
    for m, r in ((3, 1), (3, -1), (5, 1), (5, 3), (7, 1)):
        for n in range(1, 40, 2):
            image = mx_plus_r_step(n, m, r)
            assert image > 0 and image % 2 == 1


def test_spec_withholds_affine_and_valuation():
    spec = mx_plus_r_spec(5, 1)
    assert spec.affine_system() is None
    assert spec.dimension == 1
    src = Path(__file__).resolve().parents[3] / "src" / "research" / "mx_plus_r" / "spec.py"
    text = src.read_text(encoding="utf-8")
    assert "padic" not in text
    assert "v_2" not in text
    assert "v2(" not in text


def test_problem_descriptor_and_prior_art():
    assert get_problem("mx_plus_r") is PROBLEM
    assert PROBLEM.docs == ("docs/problems/engine_campaign.md",)
    assert get_reference("crandall-1978-3x+1")["project_relationship"] == "known"
    assert get_reference("chamberland-2003-3x+1-survey")["project_relationship"] == "known"
    assert get_reference("lagarias-2010-3x+1-survey")["project_relationship"] == "known"


def test_lean_specialization_is_generic():
    path = Path(__file__).resolve().parents[3] / "formal" / "Problems" / "Engine" / "MxPlusR.lean"
    text = path.read_text(encoding="utf-8")
    assert "sorry" not in text
    assert "admit" not in text
    assert "mxPlusR_parameter_iff" in text
    assert "mxPlusR_compose_two" in text
    assert "mul_pow_eq_iff_padicValInt" in text
    assert "acceleratedT" not in text
