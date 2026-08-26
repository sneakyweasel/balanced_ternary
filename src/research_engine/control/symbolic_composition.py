"""Phase-2 symbolic composition falsifier. Not an attack and not a synthesizer."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import isqrt
from typing import Any, Mapping

from research_engine.control.proposals import assert_not_executable
from research_engine.control.types import (
    ENGINE_CONTROL_VERSION,
    AttackProposal,
    AttackProposalDossier,
    Confidence,
    ImplementationScope,
    NoveltyRisk,
)

JUGGLER = "juggler_sequence"
REVERSE = "reverse_and_add_base3"
HOME = "home_prime_49"


class JugglerClass(str, Enum):
    SYMBOLIC_COMPOSITION_PROMISING = "SYMBOLIC_COMPOSITION_PROMISING"
    SYMBOLIC_COMPOSITION_NEEDS_DOMAIN = "SYMBOLIC_COMPOSITION_NEEDS_DOMAIN"
    SYMBOLIC_COMPOSITION_NEEDS_RICHER_FORM = "SYMBOLIC_COMPOSITION_NEEDS_RICHER_FORM"
    SYMBOLIC_COMPOSITION_REFUTED = "SYMBOLIC_COMPOSITION_REFUTED"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"


class ReverseClass(str, Enum):
    REVERSE_COMPOSITION_PROMISING = "REVERSE_COMPOSITION_PROMISING"
    REVERSE_COMPOSITION_NEEDS_RICHER_STRUCTURE = "REVERSE_COMPOSITION_NEEDS_RICHER_STRUCTURE"
    REVERSE_COMPOSITION_REFUTED = "REVERSE_COMPOSITION_REFUTED"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"


class HomeClass(str, Enum):
    HOME_COMPOSITION_PROMISING = "HOME_COMPOSITION_PROMISING"
    HOME_COMPOSITION_NEEDS_RICHER_STRUCTURE = "HOME_COMPOSITION_NEEDS_RICHER_STRUCTURE"
    HOME_COMPOSITION_REFUTED = "HOME_COMPOSITION_REFUTED"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"


class Phase2Decision(str, Enum):
    PROMOTE_SYMBOLIC_COMPOSITION = "PROMOTE_SYMBOLIC_COMPOSITION"
    REFINE_SYMBOLIC_COMPOSITION = "REFINE_SYMBOLIC_COMPOSITION"
    ABANDON_SYMBOLIC_COMPOSITION = "ABANDON_SYMBOLIC_COMPOSITION"
    MIXED = "MIXED"


@dataclass(frozen=True)
class CompositionSample:
    source: int
    mid: int
    image: int
    note: str = ""
    extra: dict[str, int] = None  # type: ignore[assignment]

    def __post_init__(self):
        if self.extra is None:
            object.__setattr__(self, "extra", {})


@dataclass(frozen=True)
class CandidateCheck:
    name: str
    statement: str
    domain: str
    derivation: str
    survived: bool
    counterexample: CompositionSample | None
    failure_mechanism: str
    checked: int

    def as_dict(self) -> dict[str, Any]:
        cex = None
        if self.counterexample is not None:
            cex = {
                "source": self.counterexample.source,
                "mid": self.counterexample.mid,
                "image": self.counterexample.image,
                "note": self.counterexample.note,
                "extra": dict(self.counterexample.extra),
            }
        return {
            "name": self.name,
            "statement": self.statement,
            "domain": self.domain,
            "derivation": self.derivation,
            "survived": self.survived,
            "counterexample": cex,
            "failure_mechanism": self.failure_mechanism,
            "checked": self.checked,
        }


@dataclass(frozen=True)
class Phase2TargetReport:
    target: str
    composition_depth: int
    exact_domain: str
    candidate_statement: str
    derivation: str
    counterexamples: tuple[dict[str, Any], ...]
    failure_mechanism: str
    classification: str
    lean_status: str
    relation_to_phase1: str
    checks: tuple[CandidateCheck, ...]
    notes: tuple[str, ...] = ()
    next_proposal: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "target": self.target,
            "composition_depth": self.composition_depth,
            "exact_domain": self.exact_domain,
            "candidate_statement": self.candidate_statement,
            "derivation": self.derivation,
            "counterexamples": list(self.counterexamples),
            "failure_mechanism": self.failure_mechanism,
            "classification": self.classification,
            "lean_status": self.lean_status,
            "relation_to_phase1": self.relation_to_phase1,
            "checks": [item.as_dict() for item in self.checks],
            "notes": list(self.notes),
            "next_proposal": self.next_proposal,
        }


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
    """Exact witness that k = isqrt(isqrt(n^3)) cannot satisfy k >= n for n >= 2.

    k^2 <= m, m^2 <= n^3, hence k^4 <= n^3. If k >= n then n^4 <= n^3, so n <= 1.
    """

    if n < 2 or k < 0:
        return False
    mid = isqrt(n * n * n)
    if k * k > mid:
        return False
    if mid * mid > n * n * n:
        return False
    return k * k * k * k <= n * n * n


def check_juggler_t2_lt(samples: tuple[CompositionSample, ...]) -> CandidateCheck:
    statement = (
        "For integers n >= 2 with n odd and isqrt(n^3) even, "
        "T^2(n) = isqrt(isqrt(n^3)) < n."
    )
    domain = "odd n >= 3 with T(n) even (equivalently isqrt(n^3) even)"
    derivation = (
        "Let m = isqrt(n^3) and k = isqrt(m). Then k^2 <= m and m^2 <= n^3, "
        "so k^4 <= n^3. If k >= n then n^4 <= n^3, hence n <= 1, contradicting n >= 2. "
        "The evenness of m identifies T^2 with isqrt o isqrt on n^3; it is not used in the inequality."
    )
    checked = 0
    for item in samples:
        if item.source < 2 or item.source % 2 == 0:
            continue
        if item.mid % 2 != 0:
            continue
        checked += 1
        image = odd_even_two_step(item.source)
        if image is None or image != item.image:
            return CandidateCheck(
                name="t2_lt",
                statement=statement,
                domain=domain,
                derivation=derivation,
                survived=False,
                counterexample=item,
                failure_mechanism="sample disagrees with the exact composed map",
                checked=checked,
            )
        if not (image < item.source and integer_two_step_lt_certificate(item.source, image)):
            return CandidateCheck(
                name="t2_lt",
                statement=statement,
                domain=domain,
                derivation=derivation,
                survived=False,
                counterexample=item,
                failure_mechanism="floor rounding or domain leakage: T^2(n) >= n",
                checked=checked,
            )
    if checked < 3:
        return CandidateCheck(
            name="t2_lt",
            statement=statement,
            domain=domain,
            derivation=derivation,
            survived=False,
            counterexample=None,
            failure_mechanism="fewer than three odd-to-even composed samples",
            checked=checked,
        )
    return CandidateCheck(
        name="t2_lt",
        statement=statement,
        domain=domain,
        derivation=derivation,
        survived=True,
        counterexample=None,
        failure_mechanism="",
        checked=checked,
    )


def check_predicate(
    name: str,
    statement: str,
    domain: str,
    derivation: str,
    samples: tuple[CompositionSample, ...],
    holds,
    failure: str,
) -> CandidateCheck:
    checked = 0
    for item in samples:
        checked += 1
        if holds(item):
            continue
        return CandidateCheck(
            name=name,
            statement=statement,
            domain=domain,
            derivation=derivation,
            survived=False,
            counterexample=item,
            failure_mechanism=failure,
            checked=checked,
        )
    if checked < 3:
        return CandidateCheck(
            name=name,
            statement=statement,
            domain=domain,
            derivation=derivation,
            survived=False,
            counterexample=None,
            failure_mechanism="fewer than three composition samples",
            checked=checked,
        )
    return CandidateCheck(
        name=name,
        statement=statement,
        domain=domain,
        derivation=derivation,
        survived=True,
        counterexample=None,
        failure_mechanism="",
        checked=checked,
    )


def falsify_juggler(samples: tuple[CompositionSample, ...], *, lean_status: str) -> Phase2TargetReport:
    primary = check_juggler_t2_lt(samples)
    if primary.checked < 3:
        classification = JugglerClass.INSUFFICIENT_DATA.value
        next_name = "odd_even_composed_ranking"
        mechanism = primary.failure_mechanism
    elif primary.survived:
        classification = JugglerClass.SYMBOLIC_COMPOSITION_PROMISING.value
        next_name = "odd_even_symbolic_composition"
        mechanism = (
            "T^2(n) < n on the odd-to-even domain; Phase-1 V=log_bit is a downstream size consequence"
        )
    else:
        classification = JugglerClass.SYMBOLIC_COMPOSITION_REFUTED.value
        next_name = "odd_odd_branch_composition"
        mechanism = primary.failure_mechanism
    cex = ()
    if primary.counterexample is not None:
        cex = (primary.as_dict()["counterexample"],)
    return Phase2TargetReport(
        target=JUGGLER,
        composition_depth=2,
        exact_domain=primary.domain,
        candidate_statement=primary.statement,
        derivation=primary.derivation,
        counterexamples=cex,
        failure_mechanism=mechanism,
        classification=classification,
        lean_status=lean_status,
        relation_to_phase1=(
            "Phase-1 bounded T^2 ranking survived because the composed map is strictly "
            "smaller than n on the same odd-to-even domain, not because of a new ranking template."
            if primary.survived
            else "Phase-1 ranking signal is not explained by T^2(n) < n on the recorded samples."
        ),
        checks=(primary,),
        notes=(
            "k=2 only. Odd-to-odd one-step states such as 3->5 are outside this composition.",
            "The inequality does not imply termination of the full floor-power map.",
        ),
        next_proposal=next_name,
    )


def falsify_reverse(samples: tuple[CompositionSample, ...]) -> Phase2TargetReport:
    descent = check_predicate(
        "t2_lt",
        "T^2(x) < |x| for x != 0 with a two-step successor",
        "frozen reverse-add window/orbit, depth 2",
        "If reverse-plus-add simplified under composition, two-step size might drop toward 0.",
        samples,
        lambda item: item.source == 0 or abs(item.image) < abs(item.source),
        "two-step reverse-plus-add is not a global descent; composition can grow",
    )
    ascent = check_predicate(
        "t2_gt",
        "|T^2(x)| > |x| for x != 0 with a two-step successor",
        "frozen reverse-add window/orbit, depth 2",
        "If reverse-plus-add were uniformly expanding, two-step magnitude would increase.",
        samples,
        lambda item: item.source == 0 or abs(item.image) > abs(item.source),
        "two-step reverse-plus-add is not a global ascent; small palindromes can collapse",
    )
    length_ge = check_predicate(
        "t2_length_ge",
        "bt_length(T^2(x)) >= bt_length(x) whenever T^2 is defined",
        "frozen reverse-add window/orbit, depth 2",
        "Digit reverse-plus-add might be nondecreasing in canonical length after two steps.",
        samples,
        lambda item: item.extra.get("len_image", 0) >= item.extra.get("len_source", 0),
        "canonical BT length can drop under T^2",
    )
    checks = (descent, ascent, length_ge)
    if all(item.checked < 3 for item in checks):
        classification = ReverseClass.INSUFFICIENT_DATA.value
        statement = checks[0].statement
        derivation = checks[0].derivation
        mechanism = "fewer than three two-step samples"
        next_name = "symbolic_nonlinear_composition"
    elif not descent.survived and not ascent.survived:
        classification = ReverseClass.REVERSE_COMPOSITION_NEEDS_RICHER_STRUCTURE.value
        statement = (
            "Neither T^2(x) < |x| nor |T^2(x)| > |x| holds on the frozen two-step sample."
        )
        derivation = (
            "T^2(x) = x + W(x) + W(x+W(x)). One-step reverse_gap pointed at palindromes, "
            "but two-step composition both collapses some palindromes and expands other seeds. "
            "A window-local length inequality is not a two-step identity."
        )
        mechanism = (
            f"descent fails at {descent.counterexample.source}->{descent.counterexample.image}; "
            f"ascent fails at {ascent.counterexample.source}->{ascent.counterexample.image}"
            if descent.counterexample and ascent.counterexample
            else "two-step magnitude is not monotone"
        )
        next_name = "symbolic_nonlinear_composition"
    elif descent.survived or ascent.survived:
        classification = ReverseClass.REVERSE_COMPOSITION_PROMISING.value
        best = descent if descent.survived else ascent
        statement = best.statement
        derivation = best.derivation
        mechanism = "a two-step magnitude identity survived the frozen sample"
        next_name = "reverse_add_symbolic_composition"
    else:
        classification = ReverseClass.REVERSE_COMPOSITION_REFUTED.value
        failed = next(item for item in checks if not item.survived)
        statement = failed.statement
        derivation = failed.derivation
        mechanism = failed.failure_mechanism
        next_name = "symbolic_nonlinear_composition"
    cex = []
    for item in checks:
        if item.counterexample is not None:
            cex.append(item.as_dict()["counterexample"])
    return Phase2TargetReport(
        target=REVERSE,
        composition_depth=2,
        exact_domain="frozen reverse-add window/orbit; T(x)=x+bt_reverse(x); k=2",
        candidate_statement=statement,
        derivation=derivation,
        counterexamples=tuple(cex),
        failure_mechanism=mechanism,
        classification=classification,
        lean_status="NOT_YET_FORMALIZATION_READY",
        relation_to_phase1=(
            "Phase-1 reverse_gap failed because palindromes are not attractors. "
            "Two-step composition confirms mixed collapse and growth rather than a Lyapunov law."
        ),
        checks=checks,
        notes=("k=2 only. No palindrome-language engine. Length uses existing bt_length.",),
        next_proposal=next_name,
    )


def falsify_home(samples: tuple[CompositionSample, ...]) -> Phase2TargetReport:
    length_ge = check_predicate(
        "t2_decimal_length_ge",
        "decimal_length(T^2(x)) >= decimal_length(x) on composite two-step samples",
        "composite x with T(x) and T^2(x) defined, frozen window/orbit",
        "Factor-concatenation might be nondecreasing in decimal length after two steps.",
        samples,
        lambda item: item.extra.get("len_image", 0) >= item.extra.get("len_source", 0),
        "decimal length can drop or the two-step sample is too mixed for a length law",
    )
    length_gt_mid = check_predicate(
        "t_decimal_length_gt",
        "decimal_length(T(x)) > decimal_length(x) whenever T(x) is still composite",
        "composite-to-composite one-step inside the two-step sample",
        "If concatenation always lengthens composites, one-step decimal length would jump.",
        samples,
        lambda item: item.extra.get("len_mid", 0) > item.extra.get("len_source", 0)
        or item.extra.get("mid_prime", 0) == 1,
        "concatenation need not increase decimal length (e.g. 10->25)",
    )
    omega_ge = check_predicate(
        "t2_omega_ge",
        "Omega(T^2(x)) >= Omega(x) on composite two-step samples",
        "composite x with T^2 defined",
        "Factor-word composition might not decrease total factor count over two steps.",
        samples,
        lambda item: item.extra.get("omega_image", 0) >= item.extra.get("omega_source", 0)
        or item.extra.get("image_prime", 0) == 1,
        "total factor count can fall on a composite two-step, or is not a descent coordinate",
    )
    checks = (length_ge, length_gt_mid, omega_ge)
    survivors = [item for item in checks if item.survived]
    if all(item.checked < 3 for item in checks):
        classification = HomeClass.INSUFFICIENT_DATA.value
        statement = checks[0].statement
        derivation = checks[0].derivation
        mechanism = "fewer than three two-step samples"
        next_name = "concat_word_composition"
    elif survivors and not length_gt_mid.survived:
        classification = HomeClass.HOME_COMPOSITION_NEEDS_RICHER_STRUCTURE.value
        statement = survivors[0].statement
        derivation = (
            "A weak two-step length inequality may survive while the one-step concat-length "
            "law already fails. Aggregate Omega/omega/length still miss the factor-word rewrite."
        )
        mechanism = length_gt_mid.failure_mechanism
        next_name = "concat_word_composition"
    elif survivors:
        classification = HomeClass.HOME_COMPOSITION_PROMISING.value
        statement = survivors[0].statement
        derivation = survivors[0].derivation
        mechanism = "a two-step factor-word bound survived the frozen sample"
        next_name = "concat_word_composition"
    else:
        classification = HomeClass.HOME_COMPOSITION_REFUTED.value
        failed = checks[0]
        statement = failed.statement
        derivation = failed.derivation
        mechanism = failed.failure_mechanism
        next_name = "symbolic_nonlinear_composition"
    if not length_gt_mid.survived and classification == HomeClass.HOME_COMPOSITION_PROMISING.value:
        classification = HomeClass.HOME_COMPOSITION_NEEDS_RICHER_STRUCTURE.value
        next_name = "concat_word_composition"
    cex = []
    for item in checks:
        if item.counterexample is not None:
            cex.append(item.as_dict()["counterexample"])
    return Phase2TargetReport(
        target=HOME,
        composition_depth=2,
        exact_domain="frozen home-prime window/orbit; factor-concat word; k=2; primes are terminal",
        candidate_statement=statement,
        derivation=derivation,
        counterexamples=tuple(cex),
        failure_mechanism=mechanism,
        classification=classification,
        lean_status="NOT_YET_FORMALIZATION_READY",
        relation_to_phase1=(
            "Phase-1 V_C failed on 4->22 and 10->25. Two-step composition still sees concat "
            "as a word rewrite, not as a scalar descent on (length, Omega, omega)."
        ),
        checks=checks,
        notes=(
            "k=2 only. No new factorization engine. Terminal primes are not ranked.",
            "Factorization cap is not mathematical evidence.",
            "Two-step decimal-length nondecrease on this window is a BOUNDED_SYMBOLIC_SURVIVOR, not a theorem.",
        ),
        next_proposal=next_name,
    )


def decide_phase2(reports: tuple[Phase2TargetReport, ...]) -> tuple[Phase2Decision, str]:
    by = {item.target: item for item in reports}
    juggler = by.get(JUGGLER)
    reverse = by.get(REVERSE)
    home = by.get(HOME)
    j_ok = juggler is not None and juggler.classification == JugglerClass.SYMBOLIC_COMPOSITION_PROMISING.value
    others = [item for item in (reverse, home) if item is not None]
    other_ok = [item for item in others if item.classification.endswith("_PROMISING")]
    if j_ok and other_ok and len(other_ok) == len(others):
        return (
            Phase2Decision.PROMOTE_SYMBOLIC_COMPOSITION,
            "two-step composition yields exact laws on every tested target",
        )
    if j_ok:
        return (
            Phase2Decision.MIXED,
            "odd-even T^2 < n is an exact juggler lemma; reverse-add and home-prime do not share it",
        )
    richer = [item for item in reports if "RICHER" in item.classification or "DOMAIN" in item.classification]
    if richer:
        return (
            Phase2Decision.REFINE_SYMBOLIC_COMPOSITION,
            "composition is the right language but the exact two-step forms are not yet clean",
        )
    return (
        Phase2Decision.ABANDON_SYMBOLIC_COMPOSITION,
        "two-step composition does not produce an exact law on the primary target",
    )


def _proposal(
    rank: int,
    name: str,
    trigger: str,
    target: str,
    mechanism: str,
    capability: str,
    expected: str,
    falsifier: str,
    *,
    novelty: NoveltyRisk,
    scope: ImplementationScope,
    confidence: Confidence,
    reason: str,
) -> AttackProposal:
    assert_not_executable(name)
    return AttackProposal(
        rank=rank,
        attack_name=name,
        trigger=trigger,
        mathematical_target=target,
        mechanism=mechanism,
        required_capability=capability,
        expected_yield=expected,
        falsifier=falsifier,
        novelty_risk=novelty,
        implementation_scope=scope,
        confidence=confidence,
        novelty_risk_reason=reason,
    )


def updated_proposals(report: Phase2TargetReport) -> AttackProposalDossier:
    promising = report.classification.endswith("_PROMISING")
    if promising:
        items = (
            _proposal(
                1,
                report.next_proposal or "odd_even_symbolic_composition",
                "exact two-step inequality on a natural domain",
                report.candidate_statement,
                report.derivation,
                "symbolic nonlinear branch composition",
                "exact composed identity or inequality; ranking as a corollary",
                "An integer in the stated domain with T^2(n) >= n.",
                novelty=NoveltyRisk.LOW,
                scope=ImplementationScope.SMALL,
                confidence=Confidence.HIGH,
                reason="the inequality is exact integer arithmetic, not a census restatement",
            ),
            _proposal(
                2,
                "proof_guided_hypothesis_refinement",
                "the composed inequality is Lean-expressible from existing floorPower",
                "Package T^2(n) < n on the odd-to-even domain as the attack specification.",
                "Replay the integer k^4 <= n^3 obstruction.",
                "proof-guided hypothesis refinement",
                "Lean lemma covering the English statement",
                "A domain element whose composed image is at least n.",
                novelty=NoveltyRisk.LOW,
                scope=ImplementationScope.SMALL,
                confidence=Confidence.HIGH,
                reason="existing Nat.sqrt lemmas already match the map definition",
            ),
            _proposal(
                3,
                "odd_odd_branch_composition",
                "odd-to-odd one-step states remain outside this lemma",
                "Compose the odd-to-odd floor-power branch separately; do not claim full termination.",
                "Keep k=2. Do not enlarge depth to hide 3->5.",
                "symbolic nonlinear branch composition",
                "exact odd-odd identity or a closed obstruction",
                "An odd-to-odd pair on which every two-step size law fails.",
                novelty=NoveltyRisk.MEDIUM,
                scope=ImplementationScope.MEDIUM,
                confidence=Confidence.MEDIUM,
                reason="3->5 is still the complementary branch",
            ),
        )
    else:
        items = (
            _proposal(
                1,
                report.next_proposal or "symbolic_nonlinear_composition",
                report.failure_mechanism or "two-step composition is not a monotone law",
                "Treat T as a piecewise word/rewrite rather than searching T^2 size bounds.",
                "Keep composition target-specific. Do not start a universal composition engine.",
                "symbolic nonlinear branch composition",
                "exact rewrite identity or a closed failing class",
                "A sample whose composed expression disagrees with exact I/O.",
                novelty=NoveltyRisk.HIGH,
                scope=ImplementationScope.LARGE,
                confidence=Confidence.MEDIUM,
                reason="Phase-2 showed T^2 is not a uniform simplifying map",
            ),
            _proposal(
                2,
                "basin_preimage_grammar",
                "composition did not produce a Lyapunov law",
                "Characterize predecessors of the declared core.",
                "Bounded preimage with a residue/word quotient.",
                "symbolic predecessor construction",
                "regular-preimage lemma or splitting pair",
                "Two predecessors indistinguishable by the quotient.",
                novelty=NoveltyRisk.MEDIUM,
                scope=ImplementationScope.MEDIUM,
                confidence=Confidence.MEDIUM,
                reason="basin language is independent of T^2 collapse",
            ),
            _proposal(
                3,
                "ranking_function_synthesis",
                "ranking remains a corollary language, not the next attack",
                "Do not enlarge the Phase-0 grid. Revisit ranking only if a new exact coordinate appears.",
                "Keep ranking downstream of composition.",
                "ranking-function synthesis",
                "ranking certificate using a coordinate named by composition",
                "The new coordinate still fails to decrease on an exact transition.",
                novelty=NoveltyRisk.HIGH,
                scope=ImplementationScope.LARGE,
                confidence=Confidence.LOW,
                reason="Phase 0/1 already falsified scalar ranking on this target",
            ),
        )
    return AttackProposalDossier(
        proposals=items,
        campaign_id=report.target,
        notes=("updated from symbolic-composition Phase-2 falsifier; not executed",),
    )


def phase2_payload(
    reports: tuple[Phase2TargetReport, ...],
    *,
    decision: Phase2Decision,
    decision_reason: str,
    promoted_concept: str,
) -> dict[str, Any]:
    matrix = [
        {
            "target": item.target,
            "classification": item.classification,
            "candidate_statement": item.candidate_statement,
            "failure_mechanism": item.failure_mechanism,
            "lean_status": item.lean_status,
        }
        for item in reports
    ]
    return {
        "engine_control_version": ENGINE_CONTROL_VERSION,
        "source_engine": "v2.3",
        "experimental_status": "PHASE_2_SYMBOLIC_COMPOSITION_FALSIFIER",
        "phase2_decision": decision.value,
        "decision_reason": decision_reason,
        "promoted_concept": promoted_concept,
        "composition_depth": 2,
        "target_matrix": matrix,
        "targets": [item.as_dict() for item in reports],
        "updated_proposals": {item.target: updated_proposals(item).as_dict() for item in reports},
    }


def render_phase2_markdown(payload: Mapping[str, Any]) -> str:
    lines = [
        "# Symbolic-composition Phase-2 falsifier",
        "",
        "Status: **PHASE_2_SYMBOLIC_COMPOSITION_FALSIFIER**",
        "",
        "This is not a composition engine and not a termination proof.",
        "Phase 1 left a juggler `T^2` ranking signal. Phase 2 asks whether that",
        "signal is an exact two-step identity, and whether the same probe",
        "helps reverse-add and home-prime.",
        "",
        "## Branch budget",
        "",
        "```text",
        "Mathematical target     Does T^2 have an exact inequality/identity on a",
        "                        natural domain that explains the Phase-1 ranking?",
        "Novelty hypothesis      For juggler, T^2(n) < n on odd n with T(n) even.",
        "Falsifier               An odd-to-even n >= 2 with T^2(n) >= n, or a proof",
        "                        that the inequality is only a finite-table artifact.",
        "Existing machinery      floorPower / isqrt; bt_reverse; factor_trial concat.",
        "Maximum Phase-2 scope   k=2 only; frozen windows plus a small juggler check;",
        "                        one Lean lemma if the integer obstruction is short.",
        "Promotion criterion     Exact statement, natural domain, explains Phase-1,",
        "                        not a census restatement, Lean path.",
        "Stop criterion          k>2, general CAS, new residual state, termination claim.",
        "```",
        "",
        "## Metadata",
        "",
        f"- engine_control_version: `{payload['engine_control_version']}`",
        f"- source_engine: `{payload['source_engine']}`",
        f"- experimental_status: `{payload['experimental_status']}`",
        f"- family decision: **{payload['phase2_decision']}**",
        f"- promoted concept: `{payload['promoted_concept']}`",
        f"- decision reason: {payload['decision_reason']}",
        "",
    ]
    for report in payload["targets"]:
        lines.extend(_render_target(report))
    lines.extend(
        [
            "## Cross-target comparison",
            "",
            "| Target | Classification | Statement / failure | Lean |",
            "| --- | --- | --- | --- |",
        ]
    )
    labels = {JUGGLER: "Juggler", REVERSE: "Reverse-add", HOME: "Home Prime"}
    for row in payload["target_matrix"]:
        target = labels.get(row["target"], row["target"])
        text = (row.get("failure_mechanism") or row.get("candidate_statement") or "—").replace("|", "/")
        lines.append(
            f"| {target} | {row['classification']} | {text} | {row['lean_status']} |"
        )
    lines.extend(
        [
            "",
            "## Ranking versus symbolic explanation",
            "",
            "Phase-1 recorded a juggler ranking signal: `V = log_bit` decreases on odd-to-even `T^2`.",
            "Phase-2 explains that signal: on the same domain, `T^2(n) < n` is an exact integer lemma,",
            "so the ranking survivor is a downstream size consequence, not a new template.",
            "Reverse-add and home-prime have no such explanation: composition produces mixed collapse/growth",
            "and a factor-word rewrite, not a simpler exact bound.",
            "",
            "## Cross-target mechanism",
            "",
            "Juggler: composition → simpler state → exact bound (`T^2(n) < n`).",
            "Reverse-add: composition → new complexity (collapse at `1→2→0`, growth at `3→4→8`).",
            "Home Prime: composition → new complexity (concat is a word rewrite; `10→25` keeps length,",
            "`16→2222→211101` drops `Omega`).",
            "There is no shared three-target composition theory.",
            "",
            "## Decision",
            "",
            f"**{payload['phase2_decision']}**",
            "",
            payload["decision_reason"] + ".",
            "",
            f"Promoted concept (not an executable attack): `{payload['promoted_concept']}`.",
            "Not a universal symbolic-composition engine. Frozen v2.3 files unchanged.",
            "Laboratory decision: **PARK** specifying any new attack.",
            "",
            "## Best next question",
            "",
        ]
    )
    decision = payload["phase2_decision"]
    if decision == "MIXED":
        lines.append(
            "Should odd-even T^2 < n be specified as a tiny juggler attack, while "
            "reverse-add and home-prime move to target-specific rewrite composition?"
        )
    elif decision == "PROMOTE_SYMBOLIC_COMPOSITION":
        lines.append(
            "What is the smallest executable specification of the demonstrated "
            "two-step lemma, without a general composition engine?"
        )
    else:
        lines.append(
            "Is basin/preimage grammar a cheaper next falsifier than further composition depth?"
        )
    lines.append("")
    return "\n".join(lines)


def _render_target(report: Mapping[str, Any]) -> list[str]:
    lines = [
        f"## Target `{report['target']}`",
        "",
        f"- Composition depth: {report['composition_depth']}",
        f"- Exact domain: {report['exact_domain']}",
        f"- Candidate statement: {report['candidate_statement']}",
        f"- Derivation: {report['derivation']}",
        f"- Classification: **{report['classification']}**",
        f"- Lean: `{report['lean_status']}`",
        f"- Relation to Phase 1: {report['relation_to_phase1']}",
        f"- Next proposal: `{report.get('next_proposal') or '—'}`",
        "",
        "### Checks",
        "",
    ]
    for item in report.get("checks") or ():
        mark = "survived" if item["survived"] else "failed"
        lines.append(f"- `{item['name']}` ({mark}, n={item['checked']}): {item['statement']}")
        if item.get("counterexample"):
            cex = item["counterexample"]
            lines.append(
                f"  counterexample `{cex.get('source')} -> {cex.get('mid')} -> {cex.get('image')}` "
                f"({item.get('failure_mechanism')})"
            )
    lines.extend(["", "### Counterexamples", ""])
    cexs = report.get("counterexamples") or []
    if cexs:
        for cex in cexs:
            lines.append(f"- `{cex.get('source')} -> {cex.get('mid')} -> {cex.get('image')}`")
    else:
        lines.append("None on the stated domain.")
    lines.extend(["", "### Mechanism", "", report.get("failure_mechanism") or "none", ""])
    for note in report.get("notes") or ():
        lines.append(f"- {note}")
    lines.append("")
    return lines
