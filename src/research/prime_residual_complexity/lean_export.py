"""Link prime-residual certificates to Lean names. Does not generate proofs."""

from __future__ import annotations

from research_engine.attacks.result import AttackStatus
from research_engine.core.semantics import ClaimKind, SearchScope
from research_engine.planner.orchestrator import PlannerReport
from research_engine.verification.targets import (
    TheoremTarget,
    attach_lean,
    targets_from_report,
)

PRIME_MODULE = "Problems.Primes.Residual"
SEPARATOR_THEOREM = "sievePrime_I0_separator"
I0_THEOREM = "i0_not_prime_of_natAbs"
MOD_THEOREM = "iz_mod_of_congruent"


def sieve_closure_is_exact(report: PlannerReport) -> bool:
    closure = next((item for item in report.results if item.name == "closure"), None)
    return (
        closure is not None
        and closure.status is AttackStatus.SUPPORTED
        and closure.scope is SearchScope.EXACT
        and closure.kind is ClaimKind.REACHABLE
        and bool(closure.evidence.get("complete"))
    )


def integer_closure_is_inconclusive(spec_result) -> bool:
    return (
        spec_result.status is AttackStatus.INCONCLUSIVE
        and spec_result.scope is SearchScope.BOUNDED
        and spec_result.kind is ClaimKind.REACHABLE
    )


def link_prime_residual_targets(
    targets: tuple[TheoremTarget, ...],
) -> tuple[TheoremTarget, ...]:
    separator = TheoremTarget(
        name="sieve_prime_I0_separator",
        statement=(
            "I_0(1)=3 is prime and I_0(211)=633 is composite, with 1 ≡ 211 (mod 210)"
        ),
        kind=ClaimKind.REACHABLE,
        scope=SearchScope.EXACT,
        exportable=True,
        reason="exact supported certificate",
        attack="block",
        problem="prime_residual_complexity",
        finite_checks=("left=1", "right=211", "word=(0,)"),
    )
    linked = attach_lean(
        separator,
        module=PRIME_MODULE,
        theorem=SEPARATOR_THEOREM,
        name="sieve_prime_I0_separator",
    )
    return (linked,) + tuple(targets)


def export_prime_residual_targets(
    report: PlannerReport,
) -> tuple[TheoremTarget, ...]:
    return link_prime_residual_targets(
        targets_from_report(report, problem="prime_residual_complexity")
    )
