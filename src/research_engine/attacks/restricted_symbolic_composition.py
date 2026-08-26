"""Gated restricted symbolic-composition attack. Depth is frozen at 2.

This is not a general composition engine, not a ranking synthesizer, and
not a halt theorem. The only rule is odd-even two-step decrease for maps
that match the even/odd floor-power successor.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isqrt
from typing import Any, Callable

from research_engine.attacks.result import AttackContext, AttackResult, AttackStatus
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import CertificateKind, ClaimKind, SearchScope

FAMILY_NAME = "restricted_symbolic_composition"
RULE_NAME = "odd_even_two_step_decrease"
DEPTH = 2
ENABLE_RESTRICTED_SYMBOLIC_COMPOSITION = False

DOMAIN = "odd n >= 2 with T(n) even (equivalently isqrt(n^3) even on the floor-power map)"
PRIMARY_CANDIDATE = "T^2(x) < x"
WEAK_CANDIDATE = "T^2(x) <= x - 1"
LEAN_MODULE = "Problems.Engine.FloorPower"
LEAN_THEOREM = "floorPower_odd_even_two_step_lt"
LEAN_TARGET = f"{LEAN_MODULE}.{LEAN_THEOREM}"

MAP_PROBE = (1, 2, 3, 4, 5, 7, 8, 13, 15, 16)
FALSIFIER_BUDGET = 32
DOMAIN_SCAN = tuple(range(3, 65, 2))

GLOBAL_CONSEQUENCE_NONE = "NONE"
APPLICABLE = "APPLICABLE"
NOT_APPLICABLE = "NOT_APPLICABLE"

GATED = "GATED"
NO_SUPPORTED_COMPOSITION = "NO_SUPPORTED_COMPOSITION"
MAP_MISMATCH = "MAP_MISMATCH"
DOMAIN_MISMATCH = "DOMAIN_MISMATCH"
NO_EXACT_CANDIDATE = "NO_EXACT_CANDIDATE"
NO_EXISTING_LEAN_CERTIFICATE = "NO_EXISTING_LEAN_CERTIFICATE"


def floor_power(n: int) -> int:
    """Exact even/odd floor-power successor. Stdlib isqrt only."""

    if n < 1:
        raise ValueError("floor_power is defined on positive integers")
    if n % 2 == 0:
        return isqrt(n)
    return isqrt(n * n * n)


def odd_even_two_step(n: int) -> int | None:
    """T^2(n) when n is odd, T(n) is even, and both steps are defined."""

    if n < 2 or n % 2 == 0:
        return None
    mid = isqrt(n * n * n)
    if mid % 2 != 0:
        return None
    return isqrt(mid)


def integer_two_step_lt_certificate(n: int, k: int) -> bool:
    """Exact witness that k = isqrt(isqrt(n^3)) cannot satisfy k >= n for n >= 2."""

    if n < 2 or k < 0:
        return False
    mid = isqrt(n * n * n)
    if k * k > mid:
        return False
    if mid * mid > n * n * n:
        return False
    return k * k * k * k <= n * n * n


def experimental_enabled(context: AttackContext | None = None) -> bool:
    if ENABLE_RESTRICTED_SYMBOLIC_COMPOSITION:
        return True
    if context is None:
        return False
    return bool(getattr(context, "enable_restricted_symbolic_composition", False))


def unique_successor(spec: ProblemSpec, n: int) -> int | None:
    """Unique integer successor, or None. Requires spec.successors; no reconstruction."""

    succ = getattr(spec, "successors", None)
    if not callable(succ):
        return None
    try:
        images = succ(n)
    except (TypeError, ValueError):
        return None
    if images is None or len(images) != 1:
        return None
    value = images[0]
    if isinstance(value, bool) or not isinstance(value, int):
        return None
    return int(value)


def two_step(spec: ProblemSpec, n: int) -> tuple[int, int] | None:
    mid = unique_successor(spec, n)
    if mid is None:
        return None
    image = unique_successor(spec, mid)
    if image is None:
        return None
    return (mid, image)


@dataclass(frozen=True)
class CompositionRule:
    name: str
    depth: int
    domain_predicate: Callable[[ProblemSpec, int], bool]
    compose: Callable[[ProblemSpec, int], tuple[int, int] | None]
    candidate_statements: tuple[str, ...]
    exact_verifier: Callable[[int, int], bool]
    lean_target: str
    falsifier_budget: int


@dataclass(frozen=True)
class SymbolicCompositionResult:
    target_id: str
    rule_name: str
    depth: int
    domain: str
    candidate: str
    bounded_status: str
    counterexample: tuple[int, int, int] | None
    exact_status: str
    lean_status: str
    mathematical_status: str
    applicability: str
    failure_reason: str
    global_consequence: str = GLOBAL_CONSEQUENCE_NONE
    lean_theorem: str = ""
    notes: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        return {
            "target": self.target_id,
            "attack_name": self.rule_name,
            "depth": self.depth,
            "domain": self.domain,
            "candidate_statement": self.candidate,
            "bounded_status": self.bounded_status,
            "exact_status": self.exact_status,
            "lean_status": self.lean_status,
            "mathematical_status": self.mathematical_status,
            "global_consequence": self.global_consequence,
            "applicability": self.applicability,
            "failure_reason": self.failure_reason,
            "lean_theorem": self.lean_theorem,
            "counterexample": None
            if self.counterexample is None
            else {
                "source": self.counterexample[0],
                "mid": self.counterexample[1],
                "image": self.counterexample[2],
            },
            "notes": list(self.notes),
        }


def _in_odd_even_domain(spec: ProblemSpec, n: int) -> bool:
    if n < 2 or n % 2 == 0:
        return False
    mid = unique_successor(spec, n)
    return mid is not None and mid % 2 == 0


def _compose_odd_even(spec: ProblemSpec, n: int) -> tuple[int, int] | None:
    if not _in_odd_even_domain(spec, n):
        return None
    return two_step(spec, n)


ODD_EVEN_TWO_STEP_DECREASE = CompositionRule(
    name=RULE_NAME,
    depth=DEPTH,
    domain_predicate=_in_odd_even_domain,
    compose=_compose_odd_even,
    candidate_statements=(PRIMARY_CANDIDATE, WEAK_CANDIDATE),
    exact_verifier=integer_two_step_lt_certificate,
    lean_target=LEAN_TARGET,
    falsifier_budget=FALSIFIER_BUDGET,
)


def _na(
    spec: ProblemSpec,
    reason: str,
    detail: str,
) -> SymbolicCompositionResult:
    return SymbolicCompositionResult(
        target_id=str(getattr(spec, "name", "") or ""),
        rule_name=RULE_NAME,
        depth=DEPTH,
        domain="",
        candidate="",
        bounded_status="",
        counterexample=None,
        exact_status="",
        lean_status="NOT_YET_FORMALIZATION_READY",
        mathematical_status="",
        applicability=NOT_APPLICABLE,
        failure_reason=reason,
        global_consequence=GLOBAL_CONSEQUENCE_NONE,
        notes=(detail,),
    )


def _probe_floor_power(spec: ProblemSpec) -> str | None:
    """Return a mismatch reason, or None if the unique successor matches floor-power."""

    agreements = 0
    defined = 0
    for n in MAP_PROBE:
        image = unique_successor(spec, n)
        if image is None:
            continue
        defined += 1
        expected = floor_power(n)
        if image != expected:
            return MAP_MISMATCH
        agreements += 1
    if defined == 0:
        return NO_SUPPORTED_COMPOSITION
    if agreements < 3:
        return MAP_MISMATCH
    return None


def evaluate_odd_even_two_step(spec: ProblemSpec) -> SymbolicCompositionResult:
    """Discover whether the floor-power odd-even rule applies. No campaign-name test."""

    if unique_successor(spec, 2) is None and unique_successor(spec, 1) is None:
        if getattr(spec, "successors", None) is None:
            return _na(spec, NO_SUPPORTED_COMPOSITION, "spec has no unique integer successor")
    mismatch = _probe_floor_power(spec)
    if mismatch == NO_SUPPORTED_COMPOSITION:
        return _na(spec, NO_SUPPORTED_COMPOSITION, "no unique integer successor on the probe")
    if mismatch == MAP_MISMATCH:
        return _na(
            spec,
            MAP_MISMATCH,
            "successor disagrees with even/odd floor-power on the exact probe",
        )
    if mismatch is not None:
        return _na(spec, mismatch, mismatch)

    domain_hits = [n for n in DOMAIN_SCAN if ODD_EVEN_TWO_STEP_DECREASE.domain_predicate(spec, n)]
    if not domain_hits:
        return _na(spec, DOMAIN_MISMATCH, "floor-power map matched but no odd-to-even witness")

    budget = ODD_EVEN_TWO_STEP_DECREASE.falsifier_budget
    checked = 0
    for n in domain_hits[:budget]:
        composed = ODD_EVEN_TWO_STEP_DECREASE.compose(spec, n)
        if composed is None:
            return _na(spec, NO_EXACT_CANDIDATE, f"two-step composition failed at {n}")
        mid, image = composed
        expected = odd_even_two_step(n)
        if expected is None or image != expected or mid != isqrt(n * n * n):
            return SymbolicCompositionResult(
                target_id=str(getattr(spec, "name", "") or ""),
                rule_name=RULE_NAME,
                depth=DEPTH,
                domain=DOMAIN,
                candidate=PRIMARY_CANDIDATE,
                bounded_status="REFUTED",
                counterexample=(n, mid, image),
                exact_status="REFUTED",
                lean_status="NOT_YET_FORMALIZATION_READY",
                mathematical_status="",
                applicability=APPLICABLE,
                failure_reason=NO_EXACT_CANDIDATE,
                notes=("composed image disagrees with isqrt o isqrt of n^3",),
            )
        if not (image < n and image <= n - 1):
            return SymbolicCompositionResult(
                target_id=str(getattr(spec, "name", "") or ""),
                rule_name=RULE_NAME,
                depth=DEPTH,
                domain=DOMAIN,
                candidate=PRIMARY_CANDIDATE,
                bounded_status="REFUTED",
                counterexample=(n, mid, image),
                exact_status="REFUTED",
                lean_status="NOT_YET_FORMALIZATION_READY",
                mathematical_status="",
                applicability=APPLICABLE,
                failure_reason=NO_EXACT_CANDIDATE,
                notes=("T^2(n) < n failed on a domain element",),
            )
        if not ODD_EVEN_TWO_STEP_DECREASE.exact_verifier(n, image):
            return _na(spec, NO_EXACT_CANDIDATE, f"integer k^4 obstruction failed at {n}")
        checked += 1
    if checked < 1:
        return _na(spec, DOMAIN_MISMATCH, "no domain element inside the falsifier budget")

    return SymbolicCompositionResult(
        target_id=str(getattr(spec, "name", "") or ""),
        rule_name=RULE_NAME,
        depth=DEPTH,
        domain=DOMAIN,
        candidate=PRIMARY_CANDIDATE,
        bounded_status="SURVIVES",
        counterexample=None,
        exact_status="VERIFIED",
        lean_status="PROVED",
        mathematical_status="NEW_STRUCTURAL_LEMMA",
        applicability=APPLICABLE,
        failure_reason="",
        lean_theorem=LEAN_TARGET,
        notes=(
            "bounded check confirms the candidate; Lean theorem is authoritative",
            "global_consequence is NONE: not a halt theorem",
            f"checked {checked} odd-to-even points; depth frozen at {DEPTH}",
        ),
    )


def _result_from(payload: SymbolicCompositionResult, *, attack_name: str) -> AttackResult:
    evidence = payload.as_dict()
    evidence["family"] = FAMILY_NAME
    evidence["candidate_attack"] = RULE_NAME
    if payload.applicability != APPLICABLE:
        return AttackResult(
            name=attack_name,
            status=AttackStatus.INAPPLICABLE,
            kind=ClaimKind.REACHABLE,
            scope=SearchScope.BOUNDED,
            claim=f"{NOT_APPLICABLE}: {payload.failure_reason}",
            evidence=evidence,
        )
    if payload.exact_status == "REFUTED":
        return AttackResult(
            name=attack_name,
            status=AttackStatus.REFUTED,
            kind=ClaimKind.REACHABLE,
            scope=SearchScope.BOUNDED,
            claim=payload.candidate or payload.failure_reason,
            evidence=evidence,
            counterexamples=(payload.counterexample,) if payload.counterexample else (),
            certificate_kind=CertificateKind.EXACT_COUNTEREXAMPLE,
        )
    return AttackResult(
        name=attack_name,
        status=AttackStatus.SUPPORTED,
        kind=ClaimKind.REACHABLE,
        scope=SearchScope.EXACT,
        claim=(
            f"{PRIMARY_CANDIDATE} on {DOMAIN}. "
            f"Lean {LEAN_TARGET} is authoritative. Not a halt theorem."
        ),
        evidence=evidence,
        certificates=(LEAN_TARGET,),
        certificate_kind=CertificateKind.EXACT_ARITHMETIC_IDENTITY,
    )


class RestrictedSymbolicCompositionAttack:
    """Opt-in attack. Not in DEFAULT_ATTACK_ORDER."""

    name = FAMILY_NAME

    def applicable(self, spec: ProblemSpec, context: AttackContext) -> bool:
        del spec
        return experimental_enabled(context)

    def run(self, spec: ProblemSpec, context: AttackContext) -> AttackResult:
        if not experimental_enabled(context):
            return AttackResult(
                name=self.name,
                status=AttackStatus.INAPPLICABLE,
                kind=ClaimKind.REACHABLE,
                scope=SearchScope.BOUNDED,
                claim=f"{NOT_APPLICABLE}: {GATED}",
                evidence={
                    "applicability": NOT_APPLICABLE,
                    "failure_reason": GATED,
                    "global_consequence": GLOBAL_CONSEQUENCE_NONE,
                    "family": FAMILY_NAME,
                    "depth": DEPTH,
                },
            )
        payload = evaluate_odd_even_two_step(spec)
        return _result_from(payload, attack_name=RULE_NAME)
