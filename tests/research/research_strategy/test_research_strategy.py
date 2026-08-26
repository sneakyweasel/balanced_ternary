"""Descriptor registration for v2.3 Phase 1 research strategy."""

from research.open_problems import get_problem
from research.research_strategy.problem import PROBLEM
from research_engine.planner.orchestrator import DEFAULT_ATTACK_ORDER
from research_engine.reasoning import ENGINE_REASONING_VERSION
from research_engine.strategy import ENGINE_STRATEGY_VERSION, freeze_attack_order


def test_problem_descriptor():
    assert get_problem("research_strategy") is PROBLEM
    assert PROBLEM.docs == ("docs/problems/research_strategy.md",)
    assert PROBLEM.status == "EXPLORATORY"


def test_attack_architecture_remains_frozen():
    assert DEFAULT_ATTACK_ORDER[-1] == "symmetry"
    assert freeze_attack_order() == DEFAULT_ATTACK_ORDER
    assert ENGINE_STRATEGY_VERSION == "0.2.3"
    assert ENGINE_REASONING_VERSION == "0.2.4"
    assert "vector_affine" in DEFAULT_ATTACK_ORDER
    assert DEFAULT_ATTACK_ORDER.index("control_obstruction") == DEFAULT_ATTACK_ORDER.index(
        "control_word"
    ) + 1
