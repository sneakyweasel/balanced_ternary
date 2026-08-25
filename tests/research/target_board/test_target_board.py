"""Descriptor registration for the v2.2 target board."""

from research.open_problems import get_problem
from research.target_board.problem import PROBLEM
from research_engine.planner.orchestrator import DEFAULT_ATTACK_ORDER


def test_problem_descriptor():
    assert get_problem("target_board") is PROBLEM
    assert PROBLEM.docs == ("docs/problems/research_target_board.md",)
    assert PROBLEM.status == "EXPLORATORY"


def test_attack_architecture_remains_frozen():
    assert DEFAULT_ATTACK_ORDER[-1] == "symmetry"
