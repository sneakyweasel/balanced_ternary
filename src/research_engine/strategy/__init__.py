"""Opt-in research-strategy layer for Research Engine v2.3 Phase 1."""

from research_engine.strategy.capabilities import (
    ATTACK_CAPABILITIES,
    CENSUS_OBSTRUCTION_CHAIN,
    GLOBAL_INDUCTIVE_CHAIN,
    SEEDED_CHAINS,
    VECTOR_MATRIX_CHAIN,
    capability,
    freeze_attack_order,
)
from research_engine.strategy.falsify import falsify
from research_engine.strategy.hypotheses import (
    extract_from_results,
    generate_from_memory,
    remember_hypotheses,
)
from research_engine.strategy.planner import StrategyPlanner, select_chain
from research_engine.strategy.rank import rank_hypotheses, rank_hypothesis
from research_engine.strategy.types import (
    ENGINE_STRATEGY_VERSION,
    AttackCapability,
    AttackChain,
    ObligationKind,
    ProofObligation,
    ResearchGoal,
    ResearchHypothesis,
    ResearchHypothesisStatus,
    StrategyMetrics,
    StrategyPlan,
    StrategyReport,
)

__all__ = [
    "ATTACK_CAPABILITIES",
    "CENSUS_OBSTRUCTION_CHAIN",
    "ENGINE_STRATEGY_VERSION",
    "GLOBAL_INDUCTIVE_CHAIN",
    "SEEDED_CHAINS",
    "VECTOR_MATRIX_CHAIN",
    "AttackCapability",
    "AttackChain",
    "ObligationKind",
    "ProofObligation",
    "ResearchGoal",
    "ResearchHypothesis",
    "ResearchHypothesisStatus",
    "StrategyMetrics",
    "StrategyPlan",
    "StrategyPlanner",
    "StrategyReport",
    "capability",
    "extract_from_results",
    "falsify",
    "freeze_attack_order",
    "generate_from_memory",
    "rank_hypotheses",
    "rank_hypothesis",
    "remember_hypotheses",
    "select_chain",
]
