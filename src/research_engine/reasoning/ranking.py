"""Ranking reconnaissance from a fixed catalog. Not an optimization solver."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import replace

from research_engine.algebra.linear_functionals import LinearFunctional
from research_engine.attacks.counterexample import DescentLeakAttack
from research_engine.attacks.result import AttackContext, AttackStatus
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import State
from research_engine.reasoning.regions import contains, probe_states
from research_engine.reasoning.types import (
    EvidenceState,
    InvariantCertificate,
    RankingCertificate,
    Region,
)


def _abs_sum(state: State) -> int:
    return sum(abs(int(part)) for part in state)


def _sum(state: State) -> int:
    return sum(int(part) for part in state)


def catalog(
    spec: ProblemSpec,
    context: AttackContext,
) -> tuple[tuple[str, Callable[[State], int | tuple[int, ...]]], ...]:
    dim = int(getattr(spec, "dimension", 1) or 1)
    items: list[tuple[str, Callable[[State], int | tuple[int, ...]]]] = []
    if context.descent_potential is not None:
        items.append(("context_potential", context.descent_potential))
    if context.functional is not None:
        form: LinearFunctional = context.functional

        def _functional(state: State, _form=form) -> int:
            return _form(state)

        items.append(("linear_functional", _functional))
    for index in range(dim):
        items.append((f"coord_{index}", lambda state, i=index: int(state[i]) if i < len(state) else 0))
        items.append(
            (
                f"abs_coord_{index}",
                lambda state, i=index: abs(int(state[i])) if i < len(state) else 0,
            )
        )
    items.append(("sum", _sum))
    items.append(("abs_sum", _abs_sum))
    return tuple(items)


def _with_lex(
    unary: tuple[tuple[str, Callable[[State], int | tuple[int, ...]]], ...],
) -> tuple[tuple[str, Callable[[State], int | tuple[int, ...]]], ...]:
    extras: list[tuple[str, Callable[[State], int | tuple[int, ...]]]] = []
    names = {item[0]: item[1] for item in unary}
    if "abs_sum" in names and "coord_0" in names:
        abs_sum = names["abs_sum"]
        coord0 = names["coord_0"]

        def _lex(state: State, _a=abs_sum, _b=coord0) -> tuple[int, ...]:
            left = _a(state)
            right = _b(state)
            return (int(left), int(right))  # type: ignore[arg-type]

        extras.append(("lex_abs_sum_coord0", _lex))
    return unary + tuple(extras)


def descent_leaks(
    spec: ProblemSpec,
    region: Region,
    evaluate: Callable[[State], int | tuple[int, ...]],
    context: AttackContext,
) -> tuple[tuple[State, State], ...]:
    """Wrap DescentLeakAttack; only in-region images count as ranking leaks."""

    sample = frozenset(probe_states(region))
    if not sample:
        return ()

    def _potential(state: State, _evaluate=evaluate):
        return _evaluate(state)

    ctx = replace(context, descent_potential=_potential, candidate_region=sample)
    result = DescentLeakAttack().run(spec, ctx)
    if result.status is AttackStatus.INAPPLICABLE:
        return ()
    leaks: list[tuple[State, State]] = []
    for item in result.counterexamples:
        src = item[0]
        nxt = item[2] if len(item) >= 3 else item[1]
        if contains(region, nxt):
            leaks.append((src, nxt))
    return tuple(leaks)


def synthesize_ranking(
    spec: ProblemSpec,
    context: AttackContext,
    invariant: InvariantCertificate | None,
) -> RankingCertificate | None:
    if invariant is None or not invariant.seeds_included:
        return None
    if invariant.evidence not in {
        EvidenceState.INDUCTIVE_CANDIDATE,
        EvidenceState.INDUCTIVE_CERTIFIED,
        EvidenceState.FINITE_EXACT,
    }:
        return None
    region = invariant.region
    target = str(getattr(spec, "name", "") or "")
    unary = catalog(spec, context)
    tried = _with_lex(unary) if all(
        descent_leaks(spec, region, fn, context) for _, fn in unary
    ) else unary
    best_candidate: RankingCertificate | None = None
    for name, evaluate in tried:
        leaks = descent_leaks(spec, region, evaluate, context)
        probe = probe_states(region)
        if leaks:
            continue
        if invariant.evidence is EvidenceState.INDUCTIVE_CERTIFIED:
            evidence = EvidenceState.RANKING_CERTIFIED
            statement = f"V={name} strictly descends on the certified region; not a Lyapunov theorem on Z"
        else:
            evidence = EvidenceState.RANKING_CANDIDATE
            statement = f"V={name} strictly descends on the probed region"
        cert = RankingCertificate(
            name=name,
            evaluate=evaluate,
            region=region,
            evidence=evidence,
            source_target=target,
            probe_size=len(probe),
            statement=statement,
        )
        if evidence is EvidenceState.RANKING_CERTIFIED:
            return cert
        if best_candidate is None:
            best_candidate = cert
    return best_candidate
