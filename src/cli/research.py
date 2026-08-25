"""``btlab research`` — inspect engine sessions. Not a prover."""

from __future__ import annotations

import argparse
from typing import cast

from research_engine.attacks.result import AttackStatus
from research_engine.benchmarks.pipeline import (
    load_benchmark,
    reproduce_checks,
    run_benchmark,
)
from research_engine.core.problem_spec import ProblemSpec
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
    p_an.add_argument(
        "problem",
        help="ostrowski, balanced_ternary, expanding_d, expanding_j2, expanding_j3, d_add, collatz, primes, or benchmark A-E",
    )
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
    if key.lower() in {"balanced_ternary", "bt"}:
        return "balanced_ternary"
    if key.lower() in {"expanding_d", "expanding-d", "bt_expanding"}:
        return "expanding_d"
    if key.lower() in {"expanding_j2", "expanding-j2", "j2"}:
        return "expanding_j2"
    if key.lower() in {"expanding_j3", "expanding-j3", "j3"}:
        return "expanding_j3"
    if key.lower() in {"d_add", "d-add", "dadd"}:
        return "d_add"
    if key.lower() in {
        "collatz",
        "collatz_finite_descent",
        "collatz-finite-descent",
        "cfd",
    }:
        return "collatz_finite_descent"
    if key.lower() in {
        "primes",
        "prime_residual",
        "prime-residual",
        "prime_residual_complexity",
        "prime-residual-complexity",
        "prc",
    }:
        return "prime_residual_complexity"
    letter = key.upper()
    if letter in {"A", "B", "C", "D", "E"}:
        return letter
    raise ValueError(
        f"unknown problem {name!r}; use ostrowski, balanced_ternary, expanding_d, expanding_j2, expanding_j3, d_add, collatz, primes, or A-E"
    )


def _plan(problem: str, remaining: int):
    if problem == "ostrowski":
        from research.ostrowski.adapter import export_plan_targets, plan_np

        report = plan_np(remaining)
        targets = export_plan_targets(report)
        return report, targets
    if problem == "balanced_ternary":
        from research.balanced_ternary.adapter import export_plan_targets, plan_doubled_trit

        report = plan_doubled_trit(remaining)
        targets = export_plan_targets(report)
        return report, targets
    if problem == "expanding_d":
        from research.balanced_ternary.adapter import export_expanding_d_targets, plan_expanding_d

        report = plan_expanding_d(remaining)
        targets = export_expanding_d_targets(report)
        return report, targets
    if problem == "expanding_j2":
        from research.balanced_ternary.adapter import export_j2_targets, plan_expanding_j2

        report = plan_expanding_j2(remaining)
        targets = export_j2_targets(report)
        return report, targets
    if problem == "expanding_j3":
        from research.balanced_ternary.adapter import export_j3_targets, plan_expanding_j3

        report = plan_expanding_j3(remaining)
        targets = export_j3_targets(report)
        return report, targets
    if problem == "d_add":
        from research.balanced_ternary.adapter import export_d_add_targets, plan_d_add

        report = plan_d_add(remaining)
        targets = export_d_add_targets(report)
        return report, targets
    if problem == "collatz_finite_descent":
        from research.collatz_finite_descent.adapter import (
            export_collatz_finite_descent_targets,
            plan_collatz_finite_descent,
        )

        report = plan_collatz_finite_descent(remaining)
        targets = export_collatz_finite_descent_targets(report)
        return report, targets
    if problem == "prime_residual_complexity":
        from research.prime_residual_complexity.adapter import (
            export_prime_residual_targets,
            plan_prime_residual_complexity,
        )

        report = plan_prime_residual_complexity(remaining)
        targets = export_prime_residual_targets(report)
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
    elif problem == "balanced_ternary":
        from research.balanced_ternary.spec import doubled_trit_spec

        spec = doubled_trit_spec(remaining)
        context = spec.attack_context()
    elif problem == "expanding_d":
        from research.balanced_ternary.expanding_spec import expanding_d_spec

        spec = expanding_d_spec(remaining)
        context = spec.attack_context()
    elif problem == "expanding_j2":
        from research.balanced_ternary.expanding_j2_spec import expanding_j2_spec

        spec = expanding_j2_spec(remaining)
        context = spec.attack_context()
    elif problem == "expanding_j3":
        from research.balanced_ternary.expanding_j3_spec import expanding_j3_spec

        spec = expanding_j3_spec(remaining)
        context = spec.attack_context()
    elif problem == "d_add":
        from research.balanced_ternary.d_add_spec import d_add_spec

        spec = d_add_spec(remaining)
        context = spec.attack_context()
    elif problem == "collatz_finite_descent":
        from research.collatz_finite_descent.spec import shortcut_spec

        spec = shortcut_spec(remaining)
        context = spec.attack_context()
    elif problem == "prime_residual_complexity":
        from research.prime_residual_complexity.spec import sieve_spec

        spec = sieve_spec(remaining)
        context = spec.attack_context()
    else:
        spec, context = load_benchmark(problem)
    try:
        result = run_named_attack(attack, cast(ProblemSpec, spec), context)
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
    elif problem == "balanced_ternary":
        failures = _balanced_ternary_reproduce_failures(report, targets)
    elif problem == "expanding_d":
        failures = _expanding_d_reproduce_failures(report, targets)
    elif problem == "expanding_j2":
        failures = _expanding_j2_reproduce_failures(report, targets)
    elif problem == "expanding_j3":
        failures = _expanding_j3_reproduce_failures(report, targets)
    elif problem == "d_add":
        failures = _d_add_reproduce_failures(report, targets)
    elif problem == "collatz_finite_descent":
        failures = _collatz_finite_descent_reproduce_failures(report, targets)
    elif problem == "prime_residual_complexity":
        failures = _prime_residual_reproduce_failures(report, targets)
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


def _balanced_ternary_reproduce_failures(report, targets) -> tuple[str, ...]:
    from research.balanced_ternary.lean_export import CLOSURE_THEOREM, closure_is_exact_three
    from research.balanced_ternary.planner import CLOSURE_HYPOTHESIS

    failures: list[str] = []
    if not closure_is_exact_three(report):
        failures.append("balanced_ternary: closure is not EXACT size 3")
    recon = next((item for item in report.results if item.name == "reconnaissance"), None)
    if (
        recon is None
        or recon.status is not AttackStatus.OBSERVATION
        or recon.scope is not SearchScope.BOUNDED
    ):
        failures.append("balanced_ternary: reconnaissance is not a bounded observation")
    skipped = {item.attack for item in report.skipped}
    if "modular" not in skipped or "spectral" not in skipped:
        failures.append("balanced_ternary: modular/spectral should stay inapplicable")
    hyp = next(
        (item for item in report.hypotheses if item.id == CLOSURE_HYPOTHESIS.id),
        None,
    )
    if hyp is None or hyp.status is not HypothesisStatus.SUPPORTED:
        failures.append("balanced_ternary: finite-closure hypothesis is not SUPPORTED")
    closure = next((item for item in targets if item.attack == "closure"), None)
    if closure is None or not closure.exportable or closure.lean_theorem != CLOSURE_THEOREM:
        failures.append("balanced_ternary: closure is not linked to doubledTrit_closure")
    if any(item.kind is ClaimKind.LIVE and item.exportable for item in targets):
        failures.append("balanced_ternary: exported a LIVE target")
    return tuple(failures)


def _expanding_d_reproduce_failures(report, targets) -> tuple[str, ...]:
    from research.balanced_ternary.lean_export import (
        EXPANDING_CLOSURE_THEOREM,
        closure_is_exact_three,
    )
    from research.balanced_ternary.planner import EXPANDING_CLOSURE_HYPOTHESIS

    failures: list[str] = []
    if not closure_is_exact_three(report):
        failures.append("expanding_d: closure is not EXACT size 3")
    recon = next((item for item in report.results if item.name == "reconnaissance"), None)
    if (
        recon is None
        or recon.status is not AttackStatus.OBSERVATION
        or recon.scope is not SearchScope.BOUNDED
    ):
        failures.append("expanding_d: reconnaissance is not a bounded observation")
    skipped = {item.attack for item in report.skipped}
    if "modular" not in skipped or "spectral" not in skipped:
        failures.append("expanding_d: modular/spectral should stay inapplicable")
    hyp = next(
        (item for item in report.hypotheses if item.id == EXPANDING_CLOSURE_HYPOTHESIS.id),
        None,
    )
    if hyp is None or hyp.status is not HypothesisStatus.SUPPORTED:
        failures.append("expanding_d: LSD-closure hypothesis is not SUPPORTED")
    closure = next((item for item in targets if item.attack == "closure"), None)
    if (
        closure is None
        or not closure.exportable
        or closure.lean_theorem != EXPANDING_CLOSURE_THEOREM
    ):
        failures.append("expanding_d: closure is not linked to expandingD_residue_closure")
    if any(item.kind is ClaimKind.LIVE and item.exportable for item in targets):
        failures.append("expanding_d: exported a LIVE target")
    return tuple(failures)


def _expanding_j2_reproduce_failures(report, targets) -> tuple[str, ...]:
    from research.balanced_ternary.lean_export import (
        J2_CLOSURE_THEOREM,
        closure_is_exact_size,
    )
    from research.balanced_ternary.planner import J2_CLOSURE_HYPOTHESIS

    failures: list[str] = []
    if not closure_is_exact_size(report, 9):
        failures.append("expanding_j2: closure is not EXACT size 9")
    recon = next((item for item in report.results if item.name == "reconnaissance"), None)
    if (
        recon is None
        or recon.status is not AttackStatus.OBSERVATION
        or recon.scope is not SearchScope.BOUNDED
    ):
        failures.append("expanding_j2: reconnaissance is not a bounded observation")
    skipped = {item.attack for item in report.skipped}
    if "modular" not in skipped or "spectral" not in skipped:
        failures.append("expanding_j2: modular/spectral should stay inapplicable")
    hyp = next(
        (item for item in report.hypotheses if item.id == J2_CLOSURE_HYPOTHESIS.id),
        None,
    )
    if hyp is None or hyp.status is not HypothesisStatus.SUPPORTED:
        failures.append("expanding_j2: J2-closure hypothesis is not SUPPORTED")
    closure = next((item for item in targets if item.attack == "closure"), None)
    if (
        closure is None
        or not closure.exportable
        or closure.lean_theorem != J2_CLOSURE_THEOREM
    ):
        failures.append("expanding_j2: closure is not linked to jet2_residue_closure")
    if any(item.kind is ClaimKind.LIVE and item.exportable for item in targets):
        failures.append("expanding_j2: exported a LIVE target")
    return tuple(failures)


def _expanding_j3_reproduce_failures(report, targets) -> tuple[str, ...]:
    from research.balanced_ternary.lean_export import (
        J3_CLOSURE_THEOREM,
        closure_is_exact_size,
    )
    from research.balanced_ternary.planner import J3_CLOSURE_HYPOTHESIS

    failures: list[str] = []
    if not closure_is_exact_size(report, 27):
        failures.append("expanding_j3: closure is not EXACT size 27")
    recon = next((item for item in report.results if item.name == "reconnaissance"), None)
    if (
        recon is None
        or recon.status is not AttackStatus.OBSERVATION
        or recon.scope is not SearchScope.BOUNDED
    ):
        failures.append("expanding_j3: reconnaissance is not a bounded observation")
    skipped = {item.attack for item in report.skipped}
    if "modular" not in skipped or "spectral" not in skipped:
        failures.append("expanding_j3: modular/spectral should stay inapplicable")
    hyp = next(
        (item for item in report.hypotheses if item.id == J3_CLOSURE_HYPOTHESIS.id),
        None,
    )
    if hyp is None or hyp.status is not HypothesisStatus.SUPPORTED:
        failures.append("expanding_j3: J3-closure hypothesis is not SUPPORTED")
    closure = next((item for item in targets if item.attack == "closure"), None)
    if (
        closure is None
        or not closure.exportable
        or closure.lean_theorem != J3_CLOSURE_THEOREM
    ):
        failures.append("expanding_j3: closure is not linked to jet3_residue_closure")
    if any(item.kind is ClaimKind.LIVE and item.exportable for item in targets):
        failures.append("expanding_j3: exported a LIVE target")
    return tuple(failures)


def _d_add_reproduce_failures(report, targets) -> tuple[str, ...]:
    from research.balanced_ternary.lean_export import (
        DADD_CLOSURE_THEOREM,
        closure_is_exact_size,
    )
    from research.balanced_ternary.planner import DADD_CLOSURE_HYPOTHESIS

    failures: list[str] = []
    if not closure_is_exact_size(report, 3):
        failures.append("d_add: closure is not EXACT size 3")
    recon = next((item for item in report.results if item.name == "reconnaissance"), None)
    if (
        recon is None
        or recon.status is not AttackStatus.OBSERVATION
        or recon.scope is not SearchScope.BOUNDED
    ):
        failures.append("d_add: reconnaissance is not a bounded observation")
    skipped = {item.attack for item in report.skipped}
    if "modular" not in skipped or "spectral" not in skipped:
        failures.append("d_add: modular/spectral should stay inapplicable")
    hyp = next(
        (item for item in report.hypotheses if item.id == DADD_CLOSURE_HYPOTHESIS.id),
        None,
    )
    if hyp is None or hyp.status is not HypothesisStatus.SUPPORTED:
        failures.append("d_add: residual-closure hypothesis is not SUPPORTED")
    closure = next((item for item in targets if item.attack == "closure"), None)
    if (
        closure is None
        or not closure.exportable
        or closure.lean_theorem != DADD_CLOSURE_THEOREM
    ):
        failures.append("d_add: closure is not linked to dAdd_residual_closure")
    if any(item.kind is ClaimKind.LIVE and item.exportable for item in targets):
        failures.append("d_add: exported a LIVE target")
    return tuple(failures)


def _collatz_finite_descent_reproduce_failures(report, targets) -> tuple[str, ...]:
    from research.collatz_finite_descent.lean_export import (
        DESCENT_THEOREM,
        closure_is_inconclusive,
    )
    from research.collatz_finite_descent.planner import (
        INTEGER_RESIDUAL_HYPOTHESIS,
        ONE_STEP_LYAPUNOV_HYPOTHESIS,
        UNIFORM_DESCENT_HYPOTHESIS,
    )

    failures: list[str] = []
    if not closure_is_inconclusive(report):
        failures.append("collatz: integer-state closure is not INCONCLUSIVE")
    recon = next((item for item in report.results if item.name == "reconnaissance"), None)
    if (
        recon is None
        or recon.status is not AttackStatus.OBSERVATION
        or recon.scope is not SearchScope.BOUNDED
    ):
        failures.append("collatz: reconnaissance is not a bounded observation")
    skipped = {item.attack for item in report.skipped}
    if "modular" not in skipped or "spectral" not in skipped:
        failures.append("collatz: modular/spectral should stay inapplicable")
    uniform = next(
        (item for item in report.hypotheses if item.id == UNIFORM_DESCENT_HYPOTHESIS.id),
        None,
    )
    if uniform is None or uniform.status is not HypothesisStatus.REFUTED:
        failures.append("collatz: uniform L-descent is not REFUTED")
    lyapunov = next(
        (item for item in report.hypotheses if item.id == ONE_STEP_LYAPUNOV_HYPOTHESIS.id),
        None,
    )
    if lyapunov is None or lyapunov.status is not HypothesisStatus.REFUTED:
        failures.append("collatz: one-step Lyapunov is not REFUTED")
    residual = next(
        (item for item in report.hypotheses if item.id == INTEGER_RESIDUAL_HYPOTHESIS.id),
        None,
    )
    if residual is None or residual.status is not HypothesisStatus.PARKED:
        failures.append("collatz: integer residual is not PARKED")
    obstruction = next(
        (item for item in targets if item.lean_theorem == DESCENT_THEOREM),
        None,
    )
    if obstruction is None or not obstruction.exportable:
        failures.append("collatz: obstruction is not linked to shortcutC_no_uniform_L_descent")
    if any(item.kind is ClaimKind.LIVE and item.exportable for item in targets):
        failures.append("collatz: exported a LIVE target")
    return tuple(failures)


def _prime_residual_reproduce_failures(report, targets) -> tuple[str, ...]:
    from research.prime_residual_complexity.lean_export import (
        SEPARATOR_THEOREM,
        sieve_closure_is_exact,
    )
    from research.prime_residual_complexity.planner import (
        INTEGER_PRIME_HYPOTHESIS,
        JET_EQUALS_PRIME_HYPOTHESIS,
        SIEVE_EQUALS_PRIME_HYPOTHESIS,
        SIEVE_RESIDUAL_HYPOTHESIS,
    )
    from research.prime_residual_complexity.spec import prime_spec
    from research_engine.core.problem_spec import ProblemSpec
    from research_engine.planner.orchestrator import run_named_attack

    failures: list[str] = []
    if not sieve_closure_is_exact(report):
        failures.append("primes: sieve closure is not EXACT")
    recon = next((item for item in report.results if item.name == "reconnaissance"), None)
    if (
        recon is None
        or recon.status is not AttackStatus.OBSERVATION
        or recon.scope is not SearchScope.BOUNDED
    ):
        failures.append("primes: reconnaissance is not a bounded observation")
    sieve_hyp = next(
        (item for item in report.hypotheses if item.id == SIEVE_RESIDUAL_HYPOTHESIS.id),
        None,
    )
    if sieve_hyp is None or sieve_hyp.status is not HypothesisStatus.SUPPORTED:
        failures.append("primes: sieve residual is not SUPPORTED")
    jet_hyp = next(
        (item for item in report.hypotheses if item.id == JET_EQUALS_PRIME_HYPOTHESIS.id),
        None,
    )
    if jet_hyp is None or jet_hyp.status is not HypothesisStatus.REFUTED:
        failures.append("primes: jet=prime is not REFUTED")
    sieve_eq = next(
        (item for item in report.hypotheses if item.id == SIEVE_EQUALS_PRIME_HYPOTHESIS.id),
        None,
    )
    if sieve_eq is None or sieve_eq.status is not HypothesisStatus.REFUTED:
        failures.append("primes: sieve=prime is not REFUTED")
    integer_hyp = next(
        (item for item in report.hypotheses if item.id == INTEGER_PRIME_HYPOTHESIS.id),
        None,
    )
    if integer_hyp is None or integer_hyp.status is not HypothesisStatus.PARKED:
        failures.append("primes: integer prime residual is not PARKED")
    spec = prime_spec(4)
    integer_closure = run_named_attack(
        "closure",
        cast(ProblemSpec, spec),
        spec.attack_context(),
    )
    if (
        integer_closure.status is not AttackStatus.INCONCLUSIVE
        or integer_closure.scope is not SearchScope.BOUNDED
    ):
        failures.append("primes: integer-state closure is not INCONCLUSIVE")
    separator = next(
        (item for item in targets if item.lean_theorem == SEPARATOR_THEOREM),
        None,
    )
    if separator is None or not separator.exportable:
        failures.append("primes: separator is not linked to sievePrime_I0_separator")
    if any(item.kind is ClaimKind.LIVE and item.exportable for item in targets):
        failures.append("primes: exported a LIVE target")
    return tuple(failures)
