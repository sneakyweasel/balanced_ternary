"""Deterministic Ostrowski planner session. Does not decide |L_0|."""

from __future__ import annotations

from research.ostrowski.negative_knowledge import L0_HYPOTHESIS, OSTROWSKI_FORBIDDEN
from research.ostrowski.spec import ostrowski_spec
from research.ostrowski.system import OstrowskiSystem
from research.ostrowski.zero_value_kernel import SHORTEST_NONRESET
from research_engine.algebra.linear_functionals import LinearFunctional
from research_engine.planner.ledger import ResearchLedger
from research_engine.planner.negative import NegativeKnowledge
from research_engine.planner.orchestrator import AttackPlanner, PlannerReport


def ostrowski_ledger() -> ResearchLedger:
    ledger = ResearchLedger(knowledge=NegativeKnowledge().extend(OSTROWSKI_FORBIDDEN))
    ledger.add_hypothesis(L0_HYPOTHESIS)
    return ledger


def plan_np(
    remaining: int = 4,
    system: OstrowskiSystem | None = None,
) -> PlannerReport:
    """Run the six cheap attacks on Γ_NP. Spectral/symbolic are deferred."""
    ledger = ostrowski_ledger()
    spec = ostrowski_spec(remaining, system)
    return AttackPlanner(ledger).run(
        spec,
        spec.attack_context(
            functional=LinearFunctional((0, 0, 1)),
            word=SHORTEST_NONRESET,
        ),
    )
