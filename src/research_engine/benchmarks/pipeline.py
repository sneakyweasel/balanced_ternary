"""Run the cheap-attack planner on the five synthetic benchmarks."""

from __future__ import annotations

from collections.abc import Callable

from research_engine.attacks.result import AttackContext
from research_engine.benchmarks.systems import (
    ExpandingEscapeSpec,
    FiniteClosureSpec,
    InfiniteTranslateSpec,
    ModularTripleSpec,
    ResetLoopSpec,
    context_expanding_escape,
    context_finite_closure,
    context_infinite_translate,
    context_modular_triple,
    context_reset_loop,
)
from research_engine.core.problem_spec import ProblemSpec
from research_engine.planner.hypothesis import Hypothesis, HypothesisStatus
from research_engine.planner.ledger import ResearchLedger
from research_engine.planner.orchestrator import AttackPlanner, PlannerReport
from research_engine.core.semantics import ClaimKind, SearchScope

BENCHMARK_BUILDERS: tuple[tuple[str, Callable[[], ProblemSpec], Callable[[], AttackContext]], ...] = (
    ("A", FiniteClosureSpec, context_finite_closure),
    ("B", InfiniteTranslateSpec, context_infinite_translate),
    ("C", ResetLoopSpec, context_reset_loop),
    ("D", ModularTripleSpec, context_modular_triple),
    ("E", ExpandingEscapeSpec, context_expanding_escape),
)


def run_benchmark(letter: str, ledger: ResearchLedger | None = None) -> PlannerReport:
    for name, spec_cls, context_fn in BENCHMARK_BUILDERS:
        if name != letter:
            continue
        planner = AttackPlanner(ledger if ledger is not None else ResearchLedger())
        return planner.run(spec_cls(), context_fn())
    raise KeyError(f"unknown benchmark {letter!r}")


def run_all_benchmarks() -> dict[str, PlannerReport]:
    return {letter: run_benchmark(letter) for letter, _spec, _ctx in BENCHMARK_BUILDERS}


def live_infinite_hypothesis(problem: str) -> Hypothesis:
    return Hypothesis(
        id=f"{problem}_live_infinite",
        statement="the live set is infinite",
        kind=ClaimKind.LIVE,
        intended_scope=SearchScope.EXACT,
        status=HypothesisStatus.OPEN,
        problem=problem,
    )
