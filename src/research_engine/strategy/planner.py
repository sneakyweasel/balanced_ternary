"""Opt-in attack-chain planner. Default AttackPlanner flood order is unchanged."""

from __future__ import annotations

from dataclasses import replace

from research_engine.attacks.result import AttackContext, AttackResult, AttackStatus
from research_engine.core.problem_spec import ProblemSpec
from research_engine.planner.ledger import ResearchLedger
from research_engine.planner.orchestrator import (
    SkipRecord,
    run_named_attack,
)
from research_engine.strategy.capabilities import (
    ATTACK_CAPABILITIES,
    CENSUS_OBSTRUCTION_CHAIN,
    SEEDED_CHAINS,
)
from research_engine.strategy.hypotheses import extract_from_results, remember_hypotheses
from research_engine.strategy.types import (
    AttackChain,
    ObligationKind,
    ResearchGoal,
    ResearchHypothesisStatus,
    StrategyMetrics,
    StrategyPlan,
    StrategyReport,
)

_USEFUL = {AttackStatus.SUPPORTED, AttackStatus.OBSERVATION, AttackStatus.REFUTED}


def _dimension(spec: ProblemSpec) -> int:
    return int(getattr(spec, "dimension", 1) or 1)


def _memory_wants_inductive(memory: object) -> bool:
    failures = getattr(memory, "failures", lambda: ())()
    for item in failures:
        klass = getattr(item, "failure_class", None)
        value = klass.value if hasattr(klass, "value") else klass
        if value == "GLOBAL_REASONING":
            return True
    hypotheses = getattr(memory, "hypotheses", lambda: ())()
    wanted = {ObligationKind.INDUCTIVE_INCLUSION, ObligationKind.RANKING_DESCENT}
    for hyp in hypotheses:
        for obligation in getattr(hyp, "proof_obligations", ()):
            if getattr(obligation, "kind", None) in wanted:
                return True
    return False


def score_chain(
    chain: AttackChain,
    goal: ResearchGoal,
    spec: ProblemSpec,
    memory: object | None = None,
) -> float:
    if goal not in chain.goals:
        return 0.0
    cost = chain.cost if chain.cost > 0 else 1.0
    value = chain.historical_yield / cost
    if chain.id == "global_inductive":
        if memory is not None and _memory_wants_inductive(memory):
            value *= 1.25
        return value
    dim = _dimension(spec)
    if dim == 1 and chain.id == "census_obstruction":
        value *= 2.0
    if dim > 1 and chain.id == "vector_matrix":
        value *= 2.0
    if memory is not None:
        failures = getattr(memory, "failures", lambda: ())()
        modes = {item.failure_class.value for item in failures}
        for name in chain.attacks:
            cap = ATTACK_CAPABILITIES.get(name)
            if cap is None:
                continue
            if any(mode in modes for mode in cap.known_failure_modes):
                value *= 0.85
    return value


def select_chain(
    spec: ProblemSpec,
    goal: ResearchGoal,
    memory: object | None = None,
) -> StrategyPlan:
    scored = sorted(
        ((score_chain(chain, goal, spec, memory), chain) for chain in SEEDED_CHAINS),
        key=lambda item: item[0],
        reverse=True,
    )
    positive = [(score, chain) for score, chain in scored if score > 0]
    pool = positive if positive else scored
    best_score, best = pool[0]
    alternatives = tuple(chain for score, chain in pool[1:] if score > 0 or not positive)
    reason = (
        f"goal={goal.value} selected={best.id} score={best_score:.3f} "
        f"dimension={_dimension(spec)}"
    )
    return StrategyPlan(goal=goal, chain=best, alternatives=alternatives, reason=reason)


def _is_useful(result: AttackResult) -> bool:
    return result.status in _USEFUL and result.status is not AttackStatus.INAPPLICABLE


def _chain_failed(results: list[AttackResult]) -> bool:
    if not results:
        return True
    terminal = results[-1]
    if terminal.status is AttackStatus.INAPPLICABLE:
        return True
    if terminal.status is AttackStatus.INCONCLUSIVE:
        return True
    return False


def _run_chain(
    spec: ProblemSpec,
    context: AttackContext,
    chain: AttackChain,
    prior: list[AttackResult],
) -> tuple[list[AttackResult], list[SkipRecord], bool]:
    results: list[AttackResult] = []
    skipped: list[SkipRecord] = []
    ctx = context
    existing = {item.name for item in prior}
    for name in chain.attacks:
        if name in existing:
            continue
        if name in ctx.skip_attacks:
            skipped.append(SkipRecord(name, "skipped by adapter"))
            continue
        ctx = replace(ctx, prior_results=tuple(prior) + tuple(results))
        result = run_named_attack(name, spec, ctx)
        if result.status is AttackStatus.INAPPLICABLE:
            skipped.append(SkipRecord(name, result.claim or "inapplicable"))
            return results, skipped, True
        results.append(result)
        existing.add(name)
    failed = _chain_failed(results)
    return results, skipped, failed


def compute_metrics(
    results: tuple[AttackResult, ...] | list[AttackResult],
    hypotheses: tuple,
    executed: int,
) -> StrategyMetrics:
    useful = sum(1 for item in results if _is_useful(item))
    generated = len(hypotheses)
    surviving = sum(
        1
        for item in hypotheses
        if item.current_status is not ResearchHypothesisStatus.REFUTED
    )
    proof_ready = sum(
        1
        for item in hypotheses
        if item.current_status
        in {
            ResearchHypothesisStatus.PROOF_READY,
            ResearchHypothesisStatus.PROVED,
            ResearchHypothesisStatus.LEAN_CERTIFIED,
        }
    )
    proved = sum(
        1
        for item in hypotheses
        if item.current_status
        in {ResearchHypothesisStatus.PROVED, ResearchHypothesisStatus.LEAN_CERTIFIED}
    )
    cost = float(executed) if executed else 0.0
    yield_score = float(useful + surviving)
    efficiency = (yield_score / cost) if cost else 0.0
    hyp_yield = (surviving / generated) if generated else 0.0
    conversion = (proved / proof_ready) if proof_ready else 0.0
    chain_eff = (useful / executed) if executed else 0.0
    return StrategyMetrics(
        mathematical_yield=yield_score,
        engineering_cost=cost,
        strategy_efficiency=efficiency,
        hypothesis_yield=hyp_yield,
        proof_conversion=conversion,
        attack_chain_efficiency=chain_eff,
        attacks_executed=executed,
        useful_results=useful,
        generated_hypotheses=generated,
        surviving_hypotheses=surviving,
    )


class StrategyPlanner:
    """Select and run one attack chain. Does not replace AttackPlanner."""

    def __init__(self, ledger: ResearchLedger | None = None) -> None:
        self.ledger = ledger if ledger is not None else ResearchLedger()

    def plan(
        self,
        spec: ProblemSpec,
        goal: ResearchGoal,
        memory: object | None = None,
    ) -> StrategyPlan:
        return select_chain(spec, goal, memory)

    def run(
        self,
        spec: ProblemSpec,
        context: AttackContext,
        *,
        goal: ResearchGoal,
        memory: object | None = None,
    ) -> StrategyReport:
        plan = select_chain(spec, goal, memory)
        if plan.chain.id == "global_inductive":
            from research_engine.reasoning.analyze import analyze, hypotheses_from_report

            reasoning = analyze(spec, context)
            hypotheses = hypotheses_from_report(reasoning)
            if memory is not None and hasattr(memory, "add_hypothesis"):
                remember_hypotheses(memory, hypotheses)
            return StrategyReport(
                plan=plan,
                results=(),
                hypotheses=hypotheses,
                metrics=compute_metrics((), hypotheses, 1),
                attempted_chains=("global_inductive",),
                reasoning=reasoning,
            )
        attempted: list[str] = []
        collected: list[AttackResult] = []
        skipped: list[SkipRecord] = []
        chosen = plan.chain
        for chain in (plan.chain, *plan.alternatives):
            if chain.id == "global_inductive":
                continue
            attempted.append(chain.id)
            chunk, skip, failed = _run_chain(spec, context, chain, collected)
            skipped.extend(skip)
            new_items = [item for item in chunk if item.name not in {r.name for r in collected}]
            collected.extend(new_items)
            if not failed:
                chosen = chain
                break
        executed = [item for item in collected if item.status is not AttackStatus.INAPPLICABLE]
        hypotheses = extract_from_results(
            getattr(spec, "name", ""),
            collected,
            chain=chosen.attacks,
            memory=memory if memory is not None else None,
        )
        if memory is not None and hasattr(memory, "add_hypothesis"):
            remember_hypotheses(memory, hypotheses)
        metrics = compute_metrics(collected, hypotheses, len(executed))
        return StrategyReport(
            plan=replace(plan, chain=chosen) if chosen.id != plan.chain.id else plan,
            results=tuple(collected),
            skipped=tuple(skipped),
            hypotheses=hypotheses,
            metrics=metrics,
            attempted_chains=tuple(attempted),
        )


DEFAULT_STRATEGY_CHAIN = CENSUS_OBSTRUCTION_CHAIN
