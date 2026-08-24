"""Run the cheap-attack planner on the five synthetic benchmarks."""

from __future__ import annotations

from collections.abc import Callable

from research_engine.attacks.result import AttackContext, AttackStatus
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


def load_benchmark(letter: str) -> tuple[ProblemSpec, AttackContext]:
    for name, spec_cls, context_fn in BENCHMARK_BUILDERS:
        if name == letter:
            return spec_cls(), context_fn()
    raise KeyError(f"unknown benchmark {letter!r}")


def run_benchmark(letter: str, ledger: ResearchLedger | None = None) -> PlannerReport:
    for name, spec_cls, context_fn in BENCHMARK_BUILDERS:
        if name != letter:
            continue
        planner = AttackPlanner(ledger if ledger is not None else ResearchLedger())
        return planner.run(spec_cls(), context_fn())
    raise KeyError(f"unknown benchmark {letter!r}")


def run_all_benchmarks() -> dict[str, PlannerReport]:
    return {letter: run_benchmark(letter) for letter, _spec, _ctx in BENCHMARK_BUILDERS}


def reproduce_checks(letter: str, report: PlannerReport) -> tuple[str, ...]:
    """Known fingerprints. Failures are strings; empty means reproduction ok."""
    by = {item.name: item for item in report.results}
    failures: list[str] = []
    if any(item.kind is ClaimKind.LIVE for item in report.results):
        failures.append(f"{letter}: emitted a LIVE claim")
    recon = by.get("reconnaissance")
    if letter == "A":
        if (
            recon is None
            or recon.evidence.get("union_size") != 1
            or recon.evidence.get("complete") is not True
        ):
            failures.append("A: expected complete live closure of size 1")
    elif letter == "B":
        if (
            recon is None
            or recon.scope is not SearchScope.BOUNDED
            or recon.evidence.get("complete") is not False
            or recon.kind is not ClaimKind.LIVE_SLICE
        ):
            failures.append("B: expected incomplete BOUNDED LIVE_SLICE census")
    elif letter == "C":
        blocked = {item.id for item in report.blocked_jumps}
        if "unbounded_words_not_unbounded_terminals" not in blocked:
            failures.append("C: expected word/terminal non-implication")
        if recon is None or recon.evidence.get("terminal_image_size") != 1:
            failures.append("C: expected one terminal")
    elif letter == "D":
        modular = by.get("modular")
        if (
            modular is None
            or modular.status is not AttackStatus.SUPPORTED
            or modular.scope is not SearchScope.EXACT
            or modular.kind is not ClaimKind.REACHABLE
        ):
            failures.append("D: expected exact modular map law")
    elif letter == "E":
        if recon is None or recon.evidence.get("rejected_images", 0) < 1:
            failures.append("E: expected expanding escape from the live box")
    else:
        failures.append(f"unknown benchmark {letter!r}")
    return tuple(failures)


def live_infinite_hypothesis(problem: str) -> Hypothesis:
    return Hypothesis(
        id=f"{problem}_live_infinite",
        statement="the live set is infinite",
        kind=ClaimKind.LIVE,
        intended_scope=SearchScope.EXACT,
        status=HypothesisStatus.OPEN,
        problem=problem,
    )
