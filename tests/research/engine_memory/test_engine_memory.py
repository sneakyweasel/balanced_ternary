"""Descriptor registration for the v2.2 memory campaign."""

from research.engine_memory.problem import PROBLEM
from research.open_problems import get_problem
from research_engine.planner.orchestrator import DEFAULT_ATTACK_ORDER


def test_problem_descriptor():
    assert get_problem("engine_memory") is PROBLEM
    assert PROBLEM.docs == ("docs/problems/engine_memory.md",)
    assert PROBLEM.status == "EXPLORATORY"


def test_attack_architecture_remains_frozen():
    assert DEFAULT_ATTACK_ORDER[-1] == "symmetry"
    assert "vector_affine" in DEFAULT_ATTACK_ORDER
