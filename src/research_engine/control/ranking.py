"""Phase-0 ranking-function falsifier. Not a synthesizer and not an attack."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from math import gcd
from typing import Any, Mapping

from research_engine.control.proposals import assert_not_executable, propose_attacks
from research_engine.control.types import (
    ENGINE_CONTROL_VERSION,
    AttackProposal,
    AttackProposalDossier,
    Confidence,
    ImplementationScope,
    NoveltyRisk,
    ProposalEvidence,
)

COEFF_GRID: tuple[int, ...] = (-3, -2, -1, 0, 1, 2, 3)
EXCEPTIONAL_K = 8
PRIMARY_TARGETS: tuple[str, ...] = (
    "juggler_sequence",
    "reverse_and_add_base3",
    "home_prime_49",
)
NEGATIVE_CONTROL = "cyclic_tag_bit"
PHASE0_TARGETS: tuple[str, ...] = PRIMARY_TARGETS + (NEGATIVE_CONTROL,)


class FailureClass(str, Enum):
    GROWTH_BURST = "GROWTH_BURST"
    PARITY_SWITCH = "PARITY_SWITCH"
    RESIDUE_REVERSAL = "RESIDUE_REVERSAL"
    DIGIT_REVERSAL = "DIGIT_REVERSAL"
    VALUATION_JUMP = "VALUATION_JUMP"
    BRANCH_SWITCH = "BRANCH_SWITCH"
    TERMINAL_CORE = "TERMINAL_CORE"
    FEATURE_INSUFFICIENT = "FEATURE_INSUFFICIENT"
    LENGTH_NONDECREASE = "LENGTH_NONDECREASE"
    OTHER = "OTHER"


class RankingVerdict(str, Enum):
    RANKING_PROMISING = "RANKING_PROMISING"
    RANKING_NEEDS_RICHER_STATE = "RANKING_NEEDS_RICHER_STATE"
    RANKING_IMPLAUSIBLE = "RANKING_IMPLAUSIBLE"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"


class Phase0Decision(str, Enum):
    PROMOTE = "PROMOTE"
    REFINE = "REFINE"
    ABANDON = "ABANDON"


@dataclass(frozen=True)
class FeatureVector:
    """Integer structural statistics already present on the campaign data."""

    log_bit: int
    digit: int
    residue: int
    abs_value: int
    extra: dict[str, int] = field(default_factory=dict)

    def as_dict(self) -> dict[str, int]:
        payload = {
            "log_bit": self.log_bit,
            "digit": self.digit,
            "residue": self.residue,
            "abs_value": self.abs_value,
        }
        payload.update(self.extra)
        return payload


@dataclass(frozen=True)
class ObservedTransition:
    source: int | str
    image: int | str
    source_features: FeatureVector
    image_features: FeatureVector
    note: str = ""


@dataclass(frozen=True)
class RankingCandidate:
    a: int
    b: int
    c: int

    @property
    def coeffs(self) -> tuple[int, int, int]:
        return (self.a, self.b, self.c)

    def evaluate(self, features: FeatureVector) -> int:
        """V = a * log_bit + b * digit + c * residue. Exact integer."""

        return self.a * features.log_bit + self.b * features.digit + self.c * features.residue

    def as_dict(self) -> dict[str, Any]:
        return {"a": self.a, "b": self.b, "c": self.c, "q": 0, "form": "a*log_bit + b*digit + c*residue"}


@dataclass(frozen=True)
class CandidateResult:
    candidate: RankingCandidate
    survived: bool
    counterexample: ObservedTransition | None
    v_source: int | None
    v_image: int | None
    failure_class: FailureClass | None
    failure_reason: str = ""

    def as_dict(self) -> dict[str, Any]:
        cex = None
        if self.counterexample is not None:
            cex = {
                "source": _json_state(self.counterexample.source),
                "image": _json_state(self.counterexample.image),
                "note": self.counterexample.note,
            }
        return {
            "candidate": self.candidate.as_dict(),
            "survived": self.survived,
            "counterexample": cex,
            "v_source": self.v_source,
            "v_image": self.v_image,
            "failure_class": None if self.failure_class is None else self.failure_class.value,
            "failure_reason": self.failure_reason,
        }


@dataclass(frozen=True)
class TargetRankingReport:
    target: str
    available_features: tuple[str, ...]
    candidate_count: int
    transitions_tested: int
    exceptional_set: tuple[str, ...]
    exactness: str
    survivors: tuple[CandidateResult, ...]
    failures: tuple[CandidateResult, ...]
    strongest: CandidateResult | None
    classification: RankingVerdict
    failure_mechanisms: tuple[str, ...]
    lexicographic_proposal: str
    formalization_ready: str
    notes: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        return {
            "target": self.target,
            "available_features": list(self.available_features),
            "candidate_count": self.candidate_count,
            "transitions_tested": self.transitions_tested,
            "exceptional_set": list(self.exceptional_set),
            "exactness": self.exactness,
            "survivors": [item.as_dict() for item in self.survivors],
            "first_counterexamples": [item.as_dict() for item in _representative_failures(self.failures)],
            "strongest": None if self.strongest is None else self.strongest.as_dict(),
            "classification": self.classification.value,
            "failure_mechanisms": list(self.failure_mechanisms),
            "lexicographic_proposal": self.lexicographic_proposal,
            "formalization_ready": self.formalization_ready,
            "notes": list(self.notes),
        }


def _json_state(value: int | str) -> int | str:
    return value


def integer_features(n: int, *, digit: int, residue: int, extra: dict[str, int] | None = None) -> FeatureVector:
    abs_n = abs(int(n))
    return FeatureVector(
        log_bit=(1 + abs_n).bit_length(),
        digit=int(digit),
        residue=int(residue),
        abs_value=abs_n,
        extra=dict(extra or {}),
    )


def canonicalize_coeffs(a: int, b: int, c: int) -> tuple[int, int, int] | None:
    """Drop the zero form and identify positive scalings / sign reversals."""

    if a == 0 and b == 0 and c == 0:
        return None
    scale = gcd(gcd(abs(a), abs(b)), abs(c))
    a, b, c = a // scale, b // scale, c // scale
    for value in (a, b, c):
        if value != 0:
            if value < 0:
                return (-a, -b, -c)
            return (a, b, c)
    return None


def candidate_grid() -> tuple[RankingCandidate, ...]:
    seen: set[tuple[int, int, int]] = set()
    items: list[RankingCandidate] = []
    for a in COEFF_GRID:
        for b in COEFF_GRID:
            for c in COEFF_GRID:
                canon = canonicalize_coeffs(a, b, c)
                if canon is None or canon in seen:
                    continue
                seen.add(canon)
                items.append(RankingCandidate(*canon))
    return tuple(items)


def classify_failure(transition: ObservedTransition, candidate: RankingCandidate) -> tuple[FailureClass, str]:
    src = transition.source_features
    img = transition.image_features
    grew = img.abs_value > src.abs_value or img.digit > src.digit or img.log_bit > src.log_bit
    if grew:
        if "reverse" in transition.note or "digit_reversal" in transition.note:
            return (
                FailureClass.DIGIT_REVERSAL,
                "digit reverse-plus-add increases magnitude or length",
            )
        if "concat" in transition.note or "factor" in transition.note:
            return (
                FailureClass.GROWTH_BURST,
                "factor concatenation increases decimal length",
            )
        if "odd" in transition.note or "floor" in transition.note:
            return (
                FailureClass.GROWTH_BURST,
                "odd floor-power branch increases magnitude, including odd-to-odd",
            )
        if "length" in transition.note or "rewrite" in transition.note:
            return (
                FailureClass.LENGTH_NONDECREASE,
                "rewrite length does not decrease",
            )
        if src.residue != img.residue:
            if src.residue % 2 != img.residue % 2:
                return (
                    FailureClass.BRANCH_SWITCH,
                    "parity/branch switch accompanies a size or digit-length increase",
                )
            return (
                FailureClass.RESIDUE_REVERSAL,
                "residue class changes while size or digit length increases",
            )
        return (FailureClass.GROWTH_BURST, "successor increases size or digit length")
    if src.residue != img.residue:
        return (FailureClass.PARITY_SWITCH, "residue/parity changes without a compensating size drop")
    if candidate.a == 0 and candidate.b == 0:
        return (
            FailureClass.FEATURE_INSUFFICIENT,
            "residue-only ranking cannot separate these states",
        )
    if img.digit >= src.digit and img.log_bit >= src.log_bit:
        return (
            FailureClass.FEATURE_INSUFFICIENT,
            "available scalar features do not strictly decrease",
        )
    return (FailureClass.OTHER, "V fails to decrease on this exact transition")


def evaluate_candidate(
    candidate: RankingCandidate,
    transitions: tuple[ObservedTransition, ...],
    exceptional: set[int | str],
) -> CandidateResult:
    for item in transitions:
        if item.source in exceptional:
            continue
        if item.source == item.image:
            continue
        v_src = candidate.evaluate(item.source_features)
        v_img = candidate.evaluate(item.image_features)
        if v_img < v_src:
            continue
        kind, reason = classify_failure(item, candidate)
        return CandidateResult(
            candidate=candidate,
            survived=False,
            counterexample=item,
            v_source=v_src,
            v_image=v_img,
            failure_class=kind,
            failure_reason=reason,
        )
    return CandidateResult(
        candidate=candidate,
        survived=True,
        counterexample=None,
        v_source=None,
        v_image=None,
        failure_class=None,
        failure_reason="",
    )


def _survivor_quality(result: CandidateResult) -> tuple[int, int, int, int, tuple[int, int, int]]:
    """Prefer a nonnegative size tilt, then fewer terms, then smaller coefficients."""

    candidate = result.candidate
    return (
        0 if candidate.a >= 0 else 1,
        0 if candidate.b >= 0 else 1,
        int(candidate.a != 0) + int(candidate.b != 0) + int(candidate.c != 0),
        abs(candidate.a) + abs(candidate.b) + abs(candidate.c),
        candidate.coeffs,
    )


def _representative_failures(failures: tuple[CandidateResult, ...]) -> tuple[CandidateResult, ...]:
    """One earliest counterexample per failure class."""

    best: dict[FailureClass, CandidateResult] = {}
    for item in failures:
        kind = item.failure_class
        if kind is None or item.counterexample is None:
            continue
        current = best.get(kind)
        if current is None or current.counterexample is None:
            best[kind] = item
            continue
        if _state_key(item.counterexample.source) < _state_key(current.counterexample.source):
            best[kind] = item
    return tuple(best[kind] for kind in FailureClass if kind in best)


def _state_key(value: int | str) -> tuple[int, str]:
    try:
        return (abs(int(value)), str(value))
    except (TypeError, ValueError):
        return (10**18, str(value))


def _coherent_survivor(result: CandidateResult, transitions: tuple[ObservedTransition, ...]) -> bool:
    """Reject expansion measures. log_bit and digit are both size statistics."""

    del transitions
    return result.candidate.a + result.candidate.b > 0


def classify_target(
    target: str,
    transitions: tuple[ObservedTransition, ...],
    results: tuple[CandidateResult, ...],
    *,
    is_negative_control: bool,
) -> tuple[RankingVerdict, tuple[str, ...], str]:
    tested = tuple(item for item in transitions if item.source != item.image)
    if len(tested) < 3:
        return (
            RankingVerdict.INSUFFICIENT_DATA,
            ("fewer than three non-fixed exact transitions",),
            "",
        )
    survivors = tuple(item for item in results if item.survived and _coherent_survivor(item, tested))
    by_reason: dict[str, FailureClass | None] = {}
    for item in results:
        if item.survived or item.failure_reason in by_reason:
            continue
        by_reason[item.failure_reason] = item.failure_class
    priority = {
        FailureClass.GROWTH_BURST: 0,
        FailureClass.DIGIT_REVERSAL: 1,
        FailureClass.LENGTH_NONDECREASE: 2,
        FailureClass.BRANCH_SWITCH: 3,
        FailureClass.RESIDUE_REVERSAL: 4,
        FailureClass.PARITY_SWITCH: 5,
        FailureClass.FEATURE_INSUFFICIENT: 6,
        FailureClass.VALUATION_JUMP: 7,
        FailureClass.TERMINAL_CORE: 8,
        FailureClass.OTHER: 9,
    }
    mechanisms = tuple(
        reason
        for reason, kind in sorted(
            by_reason.items(),
            key=lambda pair: priority.get(pair[1], 99),
        )
    )
    lex = ""
    if is_negative_control:
        return (
            RankingVerdict.RANKING_IMPLAUSIBLE,
            tuple(mechanisms[:6]) or ("length is nondecreasing under the rewrite",),
            "",
        )
    if survivors:
        return (RankingVerdict.RANKING_PROMISING, tuple(mechanisms[:6]), lex)
    classes = {item.failure_class for item in results if item.failure_class is not None}
    structured = {
        FailureClass.GROWTH_BURST,
        FailureClass.BRANCH_SWITCH,
        FailureClass.DIGIT_REVERSAL,
        FailureClass.PARITY_SWITCH,
        FailureClass.LENGTH_NONDECREASE,
        FailureClass.RESIDUE_REVERSAL,
    }
    if classes & structured:
        if FailureClass.GROWTH_BURST in classes and "odd" in " ".join(mechanisms):
            lex = (
                "composed odd-then-even ranking: size of the current state is not "
                "enough because odd-to-odd floor-power can grow"
            )
        elif FailureClass.DIGIT_REVERSAL in classes:
            lex = (
                "reverse-gap / palindrome-defect ranking; bt_length is unavailable "
                "as a descent coordinate because reverse-plus-add typically grows"
            )
        elif FailureClass.GROWTH_BURST in classes:
            lex = (
                "piecewise composite-versus-prime ranking; decimal length grows on "
                "factor concatenation and primes are an infinite halt set"
            )
        elif FailureClass.BRANCH_SWITCH in classes or FailureClass.PARITY_SWITCH in classes:
            lex = "V = (parity_or_branch, digit_length) lexicographic"
        return (RankingVerdict.RANKING_NEEDS_RICHER_STATE, tuple(mechanisms[:6]), lex)
    return (RankingVerdict.RANKING_IMPLAUSIBLE, tuple(mechanisms[:6]), lex)


def falsify_target(
    target: str,
    transitions: tuple[ObservedTransition, ...],
    *,
    available_features: tuple[str, ...],
    exceptional: tuple[int | str, ...],
    is_negative_control: bool = False,
    notes: tuple[str, ...] = (),
) -> TargetRankingReport:
    exceptional_set = set(exceptional)
    if len(exceptional_set) > EXCEPTIONAL_K:
        raise ValueError(f"exceptional set larger than K={EXCEPTIONAL_K}")
    candidates = candidate_grid()
    results = tuple(evaluate_candidate(item, transitions, exceptional_set) for item in candidates)
    tested = [item for item in transitions if item.source not in exceptional_set and item.source != item.image]
    survivors = tuple(
        sorted(
            (item for item in results if item.survived and _coherent_survivor(item, tuple(tested))),
            key=_survivor_quality,
        )
    )
    failures = tuple(item for item in results if not item.survived)
    strongest = survivors[0] if survivors else None
    verdict, mechanisms, lex = classify_target(
        target, transitions, results, is_negative_control=is_negative_control
    )
    exactness = (
        "V is an integer linear form in (bit_length(1+|x|), digit, residue); "
        "decrease is exact integer comparison. Discrete bit_length stands in "
        "for log(1+|x|) as the already-available exact log-class statistic."
    )
    formal = "not_yet_formalization_ready"
    if verdict is RankingVerdict.RANKING_PROMISING and strongest is not None:
        formal = "formalization_ready"
    return TargetRankingReport(
        target=target,
        available_features=available_features,
        candidate_count=len(candidates),
        transitions_tested=len(tested),
        exceptional_set=tuple(str(item) for item in exceptional),
        exactness=exactness,
        survivors=survivors,
        failures=failures,
        strongest=strongest,
        classification=verdict,
        failure_mechanisms=mechanisms,
        lexicographic_proposal=lex,
        formalization_ready=formal,
        notes=notes,
    )


def decide_phase0(reports: tuple[TargetRankingReport, ...]) -> tuple[Phase0Decision, str]:
    primary = tuple(item for item in reports if item.target in PRIMARY_TARGETS)
    if any(item.classification is RankingVerdict.INSUFFICIENT_DATA for item in primary):
        return (
            Phase0Decision.ABANDON,
            "a primary target lacked enough exact transitions for a meaningful falsifier",
        )
    promising = [item for item in primary if item.classification is RankingVerdict.RANKING_PROMISING]
    if promising:
        return (
            Phase0Decision.PROMOTE,
            "at least one primary target has a coherent exact survivor",
        )
    richer = [item for item in primary if item.classification is RankingVerdict.RANKING_NEEDS_RICHER_STATE]
    if len(richer) >= 2:
        return (
            Phase0Decision.REFINE,
            "scalar templates fail on multiple primary targets with structured branch/digit growth",
        )
    return (
        Phase0Decision.ABANDON,
        "simple candidates fail without a shared richer ranking language",
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


def updated_proposals(report: TargetRankingReport) -> AttackProposalDossier:
    """Rewrite Top-3 proposals from Phase-0 ranking evidence. Not executable."""

    if report.classification is RankingVerdict.RANKING_PROMISING:
        items = (
            _proposal(
                1,
                "ranking_function_synthesis",
                "scalar template survived the bounded exact transition set",
                "Synthesize a well-founded ranking outside a finite exceptional set.",
                "Enumerate a slightly larger exact template family around the surviving coefficients.",
                "ranking-function synthesis",
                "ranking certificate on the observed language",
                "Find a transition outside E on which every catalog measure fails.",
                novelty=NoveltyRisk.MEDIUM,
                scope=ImplementationScope.MEDIUM,
                confidence=Confidence.MEDIUM,
                reason="Phase-0 survivor is exact on a bounded sample only",
            ),
            _proposal(
                2,
                "proof_guided_invariant_refinement",
                "surviving inequalities are finite and exact",
                "Package the finite decrease identities as Lean obligations.",
                "Replay the exact V(T(x))<V(x) facts on the observed pairs.",
                "proof-guided hypothesis refinement",
                "formalization-ready finite lemma",
                "A listed pair violates the recorded inequality.",
                novelty=NoveltyRisk.LOW,
                scope=ImplementationScope.SMALL,
                confidence=Confidence.MEDIUM,
                reason="finite identities may already be the definition",
            ),
            _proposal(
                3,
                "basin_preimage_grammar",
                "ranking does not by itself characterize the basin of the attractor",
                "Couple the ranking sublevel sets with predecessor structure.",
                "Intersect {V < n} with exact preimages of the declared core.",
                "symbolic predecessor construction",
                "quotient or counterexample family for basin membership",
                "Two states with the same V-sublevel and different reachability.",
                novelty=NoveltyRisk.MEDIUM,
                scope=ImplementationScope.MEDIUM,
                confidence=Confidence.LOW,
                reason="basin language remains independent of a scalar ranking",
            ),
        )
    elif report.classification is RankingVerdict.RANKING_NEEDS_RICHER_STATE:
        name = "parity_conditioned_lexicographic_ranking"
        blob = " ".join(report.failure_mechanisms).lower() + " " + report.lexicographic_proposal.lower()
        if "odd" in blob or "floor-power" in blob or "composed odd" in blob:
            name = "odd_even_composed_ranking"
        elif "reverse" in blob or "palindrome" in blob:
            name = "reverse_gap_or_palindrome_ranking"
        elif "concat" in blob or "factor" in blob or "prime" in blob:
            name = "composite_concat_piecewise_ranking"
        items = (
            _proposal(
                1,
                name,
                report.failure_mechanisms[0] if report.failure_mechanisms else "scalar ranking fails structurally",
                report.lexicographic_proposal
                or "Construct a two-component lexicographic ranking from already available features.",
                "Keep the Phase-0 scalar features but condition the leading coordinate on branch/parity/digit structure.",
                "lexicographic / piecewise ranking",
                "ranking certificate outside a finite core, or a closed failing branch",
                "Produce a branch on which every lexicographic combination of the current features fails.",
                novelty=NoveltyRisk.MEDIUM,
                scope=ImplementationScope.MEDIUM,
                confidence=Confidence.HIGH,
                reason="Phase-0 failures already name the missing coordinate",
            ),
            _proposal(
                2,
                "ranking_function_synthesis",
                "scalar family is too weak; do not enlarge the coefficient grid",
                "Keep ranking as a family, but do not treat the 7^3 grid as exhausted mathematics.",
                "Replace scalar V with piecewise V_u on already recovered branches.",
                "ranking-function synthesis",
                "piecewise ranking certificate",
                "A recovered branch on which every piecewise catalog measure fails.",
                novelty=NoveltyRisk.HIGH,
                scope=ImplementationScope.LARGE,
                confidence=Confidence.MEDIUM,
                reason="general synthesis remains high rediscovery risk",
            ),
            _proposal(
                3,
                "symbolic_nonlinear_composition",
                "growth bursts are produced by the exact nonlinear successor",
                "Compose the nonlinear branch symbolically instead of ranking its I/O.",
                "Closed-form iterates on a cylinder would explain the observed growth.",
                "symbolic nonlinear branch composition",
                "exact iterate identity or growth law",
                "A cylinder whose composed expression disagrees with exact I/O.",
                novelty=NoveltyRisk.HIGH,
                scope=ImplementationScope.LARGE,
                confidence=Confidence.MEDIUM,
                reason="nonlinear composition is still unimplemented",
            ),
        )
    else:
        items = (
            _proposal(
                1,
                "symbolic_nonlinear_composition",
                "scalar ranking is implausible on the available features",
                "Compose the exact successor instead of searching a size ranking.",
                "Treat T as a piecewise nonlinear word and extract an invariant or grammar.",
                "symbolic nonlinear branch composition",
                "exact iterate identity, growth law, or spec-mismatch lemma",
                "A cylinder whose composed expression disagrees with exact I/O.",
                novelty=NoveltyRisk.HIGH,
                scope=ImplementationScope.LARGE,
                confidence=Confidence.MEDIUM,
                reason="ranking demoted after Phase-0 collapse",
            ),
            _proposal(
                2,
                "basin_preimage_grammar",
                "size ranking does not see the attractor",
                "Characterize predecessor states of the declared core.",
                "Bounded preimage with a residue/word quotient.",
                "symbolic predecessor construction",
                "regular-preimage lemma or splitting pair",
                "Two predecessor states indistinguishable by the quotient with different reachability.",
                novelty=NoveltyRisk.MEDIUM,
                scope=ImplementationScope.MEDIUM,
                confidence=Confidence.MEDIUM,
                reason="basin language is independent of ranking collapse",
            ),
            _proposal(
                3,
                "ranking_function_synthesis",
                "scalar templates failed; ranking is demoted, not deleted",
                "Revisit ranking only with a new feature that Phase-0 marked unavailable.",
                "Do not enlarge the coefficient grid of the same three features.",
                "ranking-function synthesis",
                "ranking certificate using a genuinely new coordinate",
                "The new coordinate still fails to decrease on an exact transition outside E.",
                novelty=NoveltyRisk.HIGH,
                scope=ImplementationScope.LARGE,
                confidence=Confidence.LOW,
                reason="Phase-0 showed the current feature set is insufficient",
            ),
        )
    return AttackProposalDossier(
        proposals=items,
        campaign_id=report.target,
        notes=("updated from ranking Phase-0 falsifier; not executed",),
    )


def fallback_proposals(campaign_id: str) -> AttackProposalDossier:
    return propose_attacks(ProposalEvidence(experiment_id=campaign_id, target=campaign_id), campaign_id=campaign_id)


def cross_target_evidence(reports: tuple[TargetRankingReport, ...]) -> tuple[str, ...]:
    """Report a pattern only when it appears in at least two primary targets."""

    primary = tuple(item for item in reports if item.target in PRIMARY_TARGETS)
    buckets = {
        "parity/branch dependence": 0,
        "digit-length jumps": 0,
        "factorization/concat discontinuity": 0,
        "digit reverse-plus-add expansion": 0,
        "lack of sufficient state variables": 0,
    }
    for report in primary:
        text = " ".join(report.failure_mechanisms).lower()
        if "parity" in text or "branch" in text:
            buckets["parity/branch dependence"] += 1
        if "digit" in text or "length" in text or "magnitude" in text:
            buckets["digit-length jumps"] += 1
        if "concat" in text or "factor" in text:
            buckets["factorization/concat discontinuity"] += 1
        if "reverse" in text:
            buckets["digit reverse-plus-add expansion"] += 1
        if report.classification is RankingVerdict.RANKING_NEEDS_RICHER_STATE:
            buckets["lack of sufficient state variables"] += 1
    return tuple(name for name, count in buckets.items() if count >= 2)


def phase0_payload(
    reports: tuple[TargetRankingReport, ...],
    *,
    decision: Phase0Decision,
    decision_reason: str,
) -> dict[str, Any]:
    matrix = []
    for item in reports:
        strongest = item.strongest
        best = "none"
        if item.target == NEGATIVE_CONTROL:
            best = "length ranking refuted (negative control)"
        elif strongest is not None:
            best = (
                f"V = {strongest.candidate.a}*log_bit + "
                f"{strongest.candidate.b}*digit + {strongest.candidate.c}*residue"
            )
        elif item.lexicographic_proposal:
            best = item.lexicographic_proposal
        matrix.append(
            {
                "target": item.target,
                "best_result": best,
                "failure_mechanism": item.failure_mechanisms[0] if item.failure_mechanisms else "",
                "classification": item.classification.value,
            }
        )
    return {
        "engine_control_version": ENGINE_CONTROL_VERSION,
        "source_engine": "v2.3",
        "experimental_status": "PHASE_0_FALSIFIER",
        "attack_family": "ranking_function_synthesis",
        "decision": decision.value,
        "decision_reason": decision_reason,
        "formalization_ready": "formalization_ready"
        if any(item.formalization_ready == "formalization_ready" for item in reports)
        else "not_yet_formalization_ready",
        "cross_target_evidence": list(cross_target_evidence(reports)),
        "target_matrix": matrix,
        "targets": [item.as_dict() for item in reports],
        "updated_proposals": {
            item.target: updated_proposals(item).as_dict() for item in reports
        },
    }


def render_phase0_markdown(payload: Mapping[str, Any]) -> str:
    lines = [
        "# Ranking-function Phase-0 falsifier",
        "",
        "Status: **PHASE_0_FALSIFIER**",
        "",
        "This is not a ranking synthesizer and not a termination proof.",
        "It asks whether frozen v2.3 transition data already contain enough",
        "monotone information for a tiny explicit template family to survive",
        "exact bounded falsification.",
        "",
        "## Branch budget",
        "",
        "```text",
        "Mathematical target     Do existing v2.3 transitions admit a simple",
        "                        scalar ranking V outside a finite exceptional set E?",
        "Novelty hypothesis      A tiny integer template family might already be",
        "                        visible on the frozen campaigns that stalled at",
        "                        global_inductive with no ranking attack.",
        "Falsifier               Every canonical candidate fails on an exact",
        "                        transition outside E, without a shared richer",
        "                        ranking language; or the only survivors are",
        "                        expansion anti-rankings / known halt restatements.",
        "Existing machinery      Frozen v2.3 discovery windows/orbits; integer",
        "                        bit_length, bt_length, decimal length, parity,",
        "                        word_length; AttackProposalDossier.",
        "Maximum Phase-0 scope   7^3 coefficient grid with gcd/sign canonicalization,",
        "                        K<=8 known cores, exact integer comparisons,",
        "                        four existing targets, no new state representation.",
        "Promotion criterion     A coherent exact survivor on a primary target,",
        "                        not a restatement of an existing invariant.",
        "Stop criterion          Silent grid enlargement, SMT/neural search, a new",
        "                        residual state, or thawing DEFAULT_ATTACK_ORDER.",
        "```",
        "",
        "## Metadata",
        "",
        f"- engine_control_version: `{payload['engine_control_version']}`",
        f"- source_engine: `{payload['source_engine']}`",
        f"- experimental_status: `{payload['experimental_status']}`",
        f"- attack_family: `{payload['attack_family']}`",
        f"- family decision: **{payload['decision']}**",
        f"- decision reason: {payload['decision_reason']}",
        f"- formalization: `{payload['formalization_ready']}`",
        "",
        "## Template family",
        "",
        "```text",
        "V(x) = a * log_bit(x) + b * d(x) + c * r(x)",
        "a, b, c in {-3,-2,-1,0,1,2,3}, q = 0",
        "log_bit(x) = bit_length(1+|x|)   # exact discrete stand-in for log(1+|x|)",
        "```",
        "",
        "Equivalent tuples are identified by positive scaling and sign reversal.",
        "A coherent termination ranking requires a+b > 0 so that V has a net",
        "positive size tilt. Expansion anti-rankings are rejected.",
        "Decrease is exact integer comparison. No floating-point verdict.",
        "",
    ]
    for report in payload["targets"]:
        lines.extend(_render_target(report))
    lines.extend(
        [
            "## Aggregate falsifier report",
            "",
            "### Target matrix",
            "",
            "| Target | Best result | Failure mechanism | Classification |",
            "| --- | --- | --- | --- |",
        ]
    )
    labels = {
        "juggler_sequence": "Juggler",
        "reverse_and_add_base3": "Reverse-add",
        "home_prime_49": "Home Prime 49",
        "cyclic_tag_bit": "Cyclic tag",
    }
    for row in payload["target_matrix"]:
        target = labels.get(row["target"], row["target"])
        mech = (row["failure_mechanism"] or "—").replace("|", "/")
        best = (row["best_result"] or "—").replace("|", "/")
        lines.append(f"| {target} | {best} | {mech} | {row['classification']} |")
    evidence = payload.get("cross_target_evidence") or []
    lines.extend(["", "### Cross-target evidence", ""])
    if evidence:
        for item in evidence:
            lines.append(f"- {item}")
    else:
        lines.append("No mechanism appeared in two or more primary targets.")
    lines.extend(
        [
            "",
            "## Decision",
            "",
            f"**{payload['decision']}** ranking-function synthesis as the first",
            "executable v2.4 attack family.",
            "",
            payload["decision_reason"] + ".",
            "",
            "This does not thaw `DEFAULT_ATTACK_ORDER`. It does not prove termination.",
            "Updated Top-3 proposals live in the machine-readable record and are not",
            "executed. Frozen v2.3 campaign files are unchanged.",
            "",
            "## Best next question",
            "",
        ]
    )
    decision = payload["decision"]
    if decision == "PROMOTE":
        lines.append(
            "What is the smallest exact template enlargement around a surviving "
            "coefficient triple that still falsifies on the same transition tables?"
        )
    elif decision == "REFINE":
        lines.append(
            "Can a deliberately small richer family — odd-even composition, "
            "reverse-gap/palindrome defect, and composite-versus-prime piecewise ranking — "
            "be falsified on the same exact transition tables without enlarging the coefficient grid?"
        )
    else:
        lines.append(
            "Should basin/preimage grammar or symbolic nonlinear composition be "
            "the next Phase-0 falsifier instead of ranking?"
        )
    lines.append("")
    return "\n".join(lines)


def _render_target(report: Mapping[str, Any]) -> list[str]:
    survivors = report.get("survivors") or []
    strongest = report.get("strongest")
    cex = report.get("first_counterexamples") or []
    lines = [
        f"## Target `{report['target']}`",
        "",
        f"- Available features: {', '.join(report['available_features'])}",
        f"- Candidate count: {report['candidate_count']}",
        f"- Transitions tested: {report['transitions_tested']}",
        f"- Exceptional set: {', '.join(report['exceptional_set']) or '(empty; fixed points already excluded by T(x)!=x)'}",
        f"- Exactness: {report['exactness']}",
        f"- Classification: **{report['classification']}**",
        f"- Formalization: `{report['formalization_ready']}`",
        "",
        "### Survivors",
        "",
    ]
    if survivors:
        for item in survivors:
            cand = item["candidate"]
            lines.append(
                f"- `V = {cand['a']}*log_bit + {cand['b']}*digit + {cand['c']}*residue`"
            )
    else:
        lines.append("None (no coherent scalar survivor).")
    lines.extend(["", "### Strongest candidate", ""])
    if strongest:
        cand = strongest["candidate"]
        lines.append(
            f"`V = {cand['a']}*log_bit + {cand['b']}*digit + {cand['c']}*residue`"
        )
    else:
        lines.append("None.")
    if report.get("lexicographic_proposal"):
        lines.extend(
            [
                "",
                "### Phase-1 lexicographic proposal (not executed)",
                "",
                report["lexicographic_proposal"],
            ]
        )
    lines.extend(["", "### First counterexamples", ""])
    if cex:
        for item in cex[:8]:
            counter = item.get("counterexample") or {}
            lines.append(
                f"- `V=({item['candidate']['a']},{item['candidate']['b']},{item['candidate']['c']})` "
                f"fails at `{counter.get('source')} -> {counter.get('image')}` "
                f"({item.get('failure_class')}: {item.get('failure_reason')})"
            )
    else:
        lines.append("No failed candidates in the recorded prefix.")
    lines.extend(["", "### Failure mechanisms", ""])
    mechs = report.get("failure_mechanisms") or []
    if mechs:
        for item in mechs:
            lines.append(f"- {item}")
    else:
        lines.append("- none recorded")
    for note in report.get("notes") or ():
        lines.append(f"- {note}")
    lines.append("")
    return lines
