"""Seed the in-process research corpus from existing v2 sessions."""

from __future__ import annotations

from research.balanced_ternary_digit_sum_dynamics.planner import plan_digit_sum_dynamics
from research.balanced_ternary_digit_sum_dynamics.spec import digit_sum_spec
from research.balanced_ternary_weight_drift.planner import plan_weight_drift
from research.balanced_ternary_weight_drift.spec import weight_drift_spec
from research.balanced_ternary_weight_dynamics.planner import plan_weight_dynamics
from research.balanced_ternary_weight_dynamics.spec import weight_dynamics_spec
from research.operator_dynamics.signed_p0.planner import plan_signed_p0
from research.operator_dynamics.signed_p0.spec import signed_p0_spec
from research.syracuse.planner import plan_syracuse_session
from research_engine.core.problem_spec import ProblemSpec
from research_engine.diagnosis.corpus import ResearchCorpus
from research_engine.diagnosis.decision import decide_research
from research_engine.diagnosis.loop import diagnose, record_from_session
from research_engine.diagnosis.types import ResearchDecision
from research_engine.planner.orchestrator import PlannerReport


def add_report(
    spec: ProblemSpec,
    report: PlannerReport,
    corpus: ResearchCorpus,
    decision: ResearchDecision | None = None,
    reason: str = "",
) -> None:
    diagnosis = diagnose(spec, report, spec.attack_context(), corpus)
    chosen, chosen_reason = decide_research(
        diagnosis.fingerprint,
        diagnosis.family_status,
        diagnosis.delta,
        report,
    )
    if decision is not None:
        chosen = decision
        chosen_reason = reason or "seeded baseline"
    corpus.add(record_from_session(spec, diagnosis, report, chosen, chosen_reason))


def seed_baseline_corpus() -> ResearchCorpus:
    """Digit-fold SATURATED cores, WeightDrift, then Syracuse."""

    corpus = ResearchCorpus()
    for spec, report in (
        (signed_p0_spec(), plan_signed_p0()),
        (digit_sum_spec(), plan_digit_sum_dynamics()),
        (weight_dynamics_spec(), plan_weight_dynamics()),
    ):
        add_report(spec, report, corpus, ResearchDecision.CLOSE, "seeded digit-fold core")
    syracuse = plan_syracuse_session(corpus=corpus)
    corpus.add(syracuse.record)
    drift = weight_drift_spec()
    add_report(drift, plan_weight_drift(), corpus)
    return corpus
