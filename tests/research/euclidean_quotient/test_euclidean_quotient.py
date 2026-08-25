"""Hint-free Euclidean remainder adapter. Quotient is not a control."""

from __future__ import annotations

from pathlib import Path

from research.euclidean_quotient.discovery import orbit_of, terminates
from research.euclidean_quotient.problem import PROBLEM
from research.euclidean_quotient.spec import euclidean_spec, euclidean_step
from research.literature import get_reference
from research.open_problems import get_problem


def test_adapter_does_not_expose_quotient():
    src = Path(__file__).resolve().parents[3] / "src" / "research" / "euclidean_quotient" / "spec.py"
    text = src.read_text(encoding="utf-8")
    assert "a // b" not in text
    assert "floor" not in text.lower()
    spec = euclidean_spec()
    assert spec.affine_system() is None
    assert spec.dimension == 2
    assert spec.legal_controls(spec.initial_state, spec.initial_phase()) == (0,)


def test_transition_is_remainder_only():
    assert euclidean_step((1071, 462)) == (462, 147)
    assert terminates((1071, 462))
    orbit = orbit_of((1071, 462), max_steps=16)
    assert orbit[-1][1] == 0
    assert orbit[-1][0] == 21


def test_problem_descriptor():
    assert get_problem("euclidean_quotient") is PROBLEM
    assert get_reference("vallee-2006-euclidean-algorithm")["project_relationship"] == "known"
    assert get_reference("knuth-taocp-vol2")["project_relationship"] == "known"
