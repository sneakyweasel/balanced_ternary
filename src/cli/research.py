"""``btlab research`` — inspect engine sessions. Not a prover."""

from __future__ import annotations

import argparse

from research_engine.attacks.result import AttackStatus
from research_engine.benchmarks.pipeline import (
    load_benchmark,
    reproduce_checks,
    run_benchmark,
)
from research_engine.core.semantics import ClaimKind, SearchScope
from research_engine.planner.hypothesis import HypothesisStatus
from research_engine.planner.orchestrator import DEFERRED_ATTACKS, run_named_attack
from research_engine.report import (
    format_attack_result,
    format_planner_report,
    format_target_report,
)
from research_engine.verification.targets import targets_from_report


def add_research_subparser(subparsers: argparse._SubParsersAction) -> None:
    p = subparsers.add_parser(
        "research",
        help="experimental-dynamics planner and theorem targets",
    )
    c = p.add_subparsers(dest="research_cmd", required=True)
    p_an = c.add_parser("analyze", help="run the cheap-attack planner")
    p_an.add_argument("problem", help="ostrowski or benchmark A-E")
    p_an.add_argument("--remaining", type=int, default=4)
    p_at = c.add_parser("attack", help="run one named cheap attack")
    p_at.add_argument("problem")
    p_at.add_argument("attack")
    p_at.add_argument("--remaining", type=int, default=4)
    p_re = c.add_parser("reproduce", help="check known fingerprints")
    p_re.add_argument("problem")
    p_re.add_argument("--remaining", type=int, default=4)
    p_rp = c.add_parser("report", help="print exportable theorem targets")
    p_rp.add_argument("problem")
    p_rp.add_argument("--remaining", type=int, default=4)


def run_research(args: argparse.Namespace) -> int:
    try:
        cmd = args.research_cmd
        if cmd == "analyze":
            return _analyze(args.problem, args.remaining)
        if cmd == "attack":
            return _attack(args.problem, args.attack, args.remaining)
        if cmd == "reproduce":
            return _reproduce(args.problem, args.remaining)
        if cmd == "report":
            return _report(args.problem, args.remaining)
    except ValueError as exc:
        print(exc)
        return 2
    raise ValueError(f"unknown research command {cmd!r}")


def _normalize_problem(name: str) -> str:
    key = name.strip()
    if key.lower() == "ostrowski":
        return "ostrowski"
    letter = key.upper()
    if letter in {"A", "B", "C", "D", "E"}:
        return letter
    raise ValueError(f"unknown problem {name!r}; use ostrowski or A-E")


def _plan(problem: str, remaining: int):
    if problem == "ostrowski":
        from research.ostrowski.adapter import export_plan_targets, plan_np

        report = plan_np(remaining)
        targets = export_plan_targets(report)
        return report, targets
    report = run_benchmark(problem)
    return report, targets_from_report(report, problem=f"benchmark_{problem}")


def _analyze(problem_name: str, remaining: int) -> int:
    problem = _normalize_problem(problem_name)
    report, _targets = _plan(problem, remaining)
    print(format_planner_report(report, problem=problem), end="")
    return 0


def _attack(problem_name: str, attack: str, remaining: int) -> int:
    problem = _normalize_problem(problem_name)
    if problem == "ostrowski":
        from research.ostrowski.spec import ostrowski_spec
        from research.ostrowski.zero_value_kernel import SHORTEST_NONRESET
        from research_engine.algebra.linear_functionals import LinearFunctional

        spec = ostrowski_spec(remaining)
        context = spec.attack_context(
            functional=LinearFunctional((0, 0, 1)),
            word=SHORTEST_NONRESET,
        )
    else:
        spec, context = load_benchmark(problem)
    try:
        result = run_named_attack(attack, spec, context)
    except KeyError:
        print(f"unknown attack {attack!r}")
        return 2
    print(format_attack_result(result))
    if attack in DEFERRED_ATTACKS or result.status is AttackStatus.INAPPLICABLE:
        return 2
    return 0


def _reproduce(problem_name: str, remaining: int) -> int:
    problem = _normalize_problem(problem_name)
    report, targets = _plan(problem, remaining)
    print(format_planner_report(report, problem=problem), end="")
    if problem == "ostrowski":
        failures = _ostrowski_reproduce_failures(report, targets)
    else:
        failures = reproduce_checks(problem, report)
    if failures:
        print("reproduce: FAIL")
        for item in failures:
            print(f"  {item}")
        return 1
    print("reproduce: ok")
    return 0


def _report(problem_name: str, remaining: int) -> int:
    problem = _normalize_problem(problem_name)
    report, targets = _plan(problem, remaining)
    print(format_planner_report(report, problem=problem), end="")
    print(format_target_report(targets), end="")
    return 0


def _ostrowski_reproduce_failures(report, targets) -> tuple[str, ...]:
    from research.ostrowski.lean_export import HUB_THEOREM, STEP_FST_THEOREM
    from research.ostrowski.negative_knowledge import L0_HYPOTHESIS

    failures: list[str] = []
    live = next(
        (item for item in report.hypotheses if item.id == L0_HYPOTHESIS.id),
        None,
    )
    if (
        live is None
        or live.status is not HypothesisStatus.PARKED
        or live.kind is not ClaimKind.LIVE
        or live.intended_scope is not SearchScope.EXACT
    ):
        failures.append("ostrowski: |L_0| is not PARKED EXACT LIVE")
    modular = next((item for item in targets if item.attack == "modular"), None)
    if (
        modular is None
        or not modular.exportable
        or modular.lean_theorem != STEP_FST_THEOREM
    ):
        failures.append("ostrowski: modular is not linked to step_fst_dvd_three")
    block = next((item for item in targets if item.attack == "block"), None)
    if block is None or block.lean_theorem != HUB_THEOREM:
        failures.append("ostrowski: hub block is not linked to hub_nonreset")
    if any(item.kind is ClaimKind.LIVE and item.exportable for item in targets):
        failures.append("ostrowski: exported a LIVE target")
    return tuple(failures)
