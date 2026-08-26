"""Phase-4 reverse-add two-step composition falsifier. Not an attack."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Mapping

from research_engine.control.proposals import assert_not_executable
from research_engine.control.types import (
    ENGINE_CONTROL_VERSION,
    AttackProposal,
    AttackProposalDossier,
    Confidence,
    ImplementationScope,
    NoveltyRisk,
)

TARGET = "reverse_and_add_base3"
DEPTH = 2
EXPERIMENT_NAME = "reverse_add_composition_phase4"


class ReverseCompositionClass(str, Enum):
    REVERSE_COMPOSITION_PROMISING = "REVERSE_COMPOSITION_PROMISING"
    REVERSE_COMPOSITION_GREEN_LOOT = "REVERSE_COMPOSITION_GREEN_LOOT"
    REVERSE_COMPOSITION_NEEDS_RICHER_STRUCTURE = "REVERSE_COMPOSITION_NEEDS_RICHER_STRUCTURE"
    REVERSE_COMPOSITION_REFUTED = "REVERSE_COMPOSITION_REFUTED"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"


def sign_int(n: int) -> int:
    if n > 0:
        return 1
    if n < 0:
        return -1
    return 0


@dataclass(frozen=True)
class ReverseSample:
    source: int
    mid: int
    image: int
    w_source: int
    w_mid: int
    len_source: int
    len_mid: int
    len_image: int
    note: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "mid": self.mid,
            "image": self.image,
            "w_source": self.w_source,
            "w_mid": self.w_mid,
            "len_source": self.len_source,
            "len_mid": self.len_mid,
            "len_image": self.len_image,
            "note": self.note,
        }


@dataclass(frozen=True)
class RankedCandidate:
    rank: int
    name: str
    exact_statement: str
    motivation: str
    relevant_domain: str
    expected_yield: str
    cheapest_falsifier: str
    failure_class: str
    holds: Callable[[ReverseSample], bool]
    in_domain: Callable[[ReverseSample], bool]


@dataclass(frozen=True)
class CandidateOutcome:
    rank: int
    name: str
    exact_statement: str
    motivation: str
    relevant_domain: str
    expected_yield: str
    cheapest_falsifier: str
    survived: bool
    counterexample: ReverseSample | None
    failure_mechanism: str
    failure_class: str
    checked: int

    def as_dict(self) -> dict[str, Any]:
        return {
            "rank": self.rank,
            "name": self.name,
            "exact_statement": self.exact_statement,
            "motivation": self.motivation,
            "relevant_domain": self.relevant_domain,
            "expected_yield": self.expected_yield,
            "cheapest_falsifier": self.cheapest_falsifier,
            "survived": self.survived,
            "counterexample": None if self.counterexample is None else self.counterexample.as_dict(),
            "failure_mechanism": self.failure_mechanism,
            "failure_class": self.failure_class,
            "checked": self.checked,
        }


def ranked_candidates() -> tuple[RankedCandidate, ...]:
    """Exactly three candidates, ranked before execution. Do not extend after failure."""

    return (
        RankedCandidate(
            rank=1,
            name="reverse_cancellation",
            exact_statement="W(x) + W(T(x)) = 0 whenever T and T^2 are defined",
            motivation=(
                "T^2(x) = x + W(x) + W(T(x)). The only simple algebraic simplification "
                "is cancellation of the two reverse terms, which would give T^2(x) = x."
            ),
            relevant_domain="integers with a defined two-step reverse-plus-add successor",
            expected_yield="an exact two-step identity T^2 = id, the reverse analog of Juggler T^2 < n",
            cheapest_falsifier="the first frozen-window seed with W(x) + W(T(x)) != 0",
            failure_class="CANCELLATION_FAILURE",
            in_domain=lambda _item: True,
            holds=lambda item: item.w_source + item.w_mid == 0,
        ),
        RankedCandidate(
            rank=2,
            name="two_step_sign_preservation",
            exact_statement="sign(T^2(x)) = sign(x) for x != 0 with T^2 defined",
            motivation=(
                "If two-step reverse-plus-add were a size-simplifying composition, it should "
                "at least preserve sign. This is the weakest exact Class-A relation that is "
                "not a reopened ranking template."
            ),
            relevant_domain="nonzero integers with a defined two-step successor",
            expected_yield="a sign law explaining two-step collapse versus growth",
            cheapest_falsifier="the smallest nonzero frozen seed whose two-step image has a different sign",
            failure_class="SIGN_REVERSAL",
            in_domain=lambda item: item.source != 0,
            holds=lambda item: sign_int(item.image) == sign_int(item.source),
        ),
        RankedCandidate(
            rank=3,
            name="two_step_length_plus_one",
            exact_statement="bt_length(T^2(x)) <= bt_length(x) + 1 whenever T^2 is defined",
            motivation=(
                "Reverse-plus-add is a digit-wise sum of a word and its reverse, so one step "
                "can create at most one extra trit. The strongest two-step length law that is "
                "not the trivial iterated bound +2 is that two steps still create at most one trit."
            ),
            relevant_domain="integers with a defined two-step successor",
            expected_yield="an exact length obstruction from reverse-add carry",
            cheapest_falsifier="the first frozen seed whose two-step canonical length grows by 2 or more",
            failure_class="DIGIT_GROWTH",
            in_domain=lambda _item: True,
            holds=lambda item: item.len_image <= item.len_source + 1,
        ),
    )


def evaluate_candidate(
    candidate: RankedCandidate,
    samples: tuple[ReverseSample, ...],
) -> CandidateOutcome:
    checked = 0
    for item in samples:
        if not candidate.in_domain(item):
            continue
        checked += 1
        if candidate.holds(item):
            continue
        return CandidateOutcome(
            rank=candidate.rank,
            name=candidate.name,
            exact_statement=candidate.exact_statement,
            motivation=candidate.motivation,
            relevant_domain=candidate.relevant_domain,
            expected_yield=candidate.expected_yield,
            cheapest_falsifier=candidate.cheapest_falsifier,
            survived=False,
            counterexample=item,
            failure_mechanism=_mechanism(candidate, item),
            failure_class=candidate.failure_class,
            checked=checked,
        )
    if checked < 3:
        return CandidateOutcome(
            rank=candidate.rank,
            name=candidate.name,
            exact_statement=candidate.exact_statement,
            motivation=candidate.motivation,
            relevant_domain=candidate.relevant_domain,
            expected_yield=candidate.expected_yield,
            cheapest_falsifier=candidate.cheapest_falsifier,
            survived=False,
            counterexample=None,
            failure_mechanism="fewer than three two-step samples on the stated domain",
            failure_class="OTHER",
            checked=checked,
        )
    return CandidateOutcome(
        rank=candidate.rank,
        name=candidate.name,
        exact_statement=candidate.exact_statement,
        motivation=candidate.motivation,
        relevant_domain=candidate.relevant_domain,
        expected_yield=candidate.expected_yield,
        cheapest_falsifier=candidate.cheapest_falsifier,
        survived=True,
        counterexample=None,
        failure_mechanism="",
        failure_class="",
        checked=checked,
    )


def _mechanism(candidate: RankedCandidate, item: ReverseSample) -> str:
    if candidate.name == "reverse_cancellation":
        return (
            f"The second reverse does not cancel the first: W({item.source})={item.w_source} and "
            f"W({item.mid})={item.w_mid}, so W(x)+W(T(x))={item.w_source + item.w_mid} and "
            f"T^2({item.source})={item.image} != {item.source}."
        )
    if candidate.name == "two_step_sign_preservation":
        return (
            f"Two-step reverse-plus-add changes sign: {item.source} -> {item.mid} -> {item.image} "
            f"has sign {sign_int(item.source)} -> {sign_int(item.image)}."
        )
    return (
        f"Two-step canonical length grows by more than one trit: "
        f"bt_length({item.source})={item.len_source}, bt_length({item.image})={item.len_image}."
    )


def classify(outcomes: tuple[CandidateOutcome, ...]) -> tuple[ReverseCompositionClass, str]:
    if any(item.checked < 3 and not item.survived and item.counterexample is None for item in outcomes):
        if all(item.checked < 3 for item in outcomes):
            return (
                ReverseCompositionClass.INSUFFICIENT_DATA,
                "fewer than three two-step samples",
            )
    survivors = [item for item in outcomes if item.survived]
    algebraic = [item for item in outcomes if item.name != "two_step_length_plus_one"]
    algebraic_failed = all(not item.survived for item in algebraic)
    length = next((item for item in outcomes if item.name == "two_step_length_plus_one"), None)
    if survivors and all(item.name == "two_step_length_plus_one" for item in survivors) and algebraic_failed:
        return (
            ReverseCompositionClass.REVERSE_COMPOSITION_NEEDS_RICHER_STRUCTURE,
            "algebraic cancellation and sign preservation fail; the +1 length bound is only a "
            "bounded observation and does not explain the reverse interaction",
        )
    if all(item.survived for item in outcomes):
        return (
            ReverseCompositionClass.REVERSE_COMPOSITION_PROMISING,
            "all three two-step statements survived the frozen sample",
        )
    if algebraic_failed and (length is None or not length.survived):
        return (
            ReverseCompositionClass.REVERSE_COMPOSITION_REFUTED,
            "the natural two-step cancellation, sign, and length laws all fail",
        )
    return (
        ReverseCompositionClass.REVERSE_COMPOSITION_NEEDS_RICHER_STRUCTURE,
        "simple two-step identities fail and no Lean-ready reverse lemma remains",
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


def updated_proposals(classification: ReverseCompositionClass) -> AttackProposalDossier:
    if classification is ReverseCompositionClass.REVERSE_COMPOSITION_GREEN_LOOT:
        items = (
            _proposal(
                1,
                "reverse_add_symbolic_composition",
                "exact two-step reverse identity",
                "Package the survived two-step reverse lemma as a gated experimental action.",
                "Keep k=2. Do not start a palindrome-language engine.",
                "symbolic nonlinear branch composition",
                "Lean lemma on W and T^2",
                "A domain element violating the lemma.",
                novelty=NoveltyRisk.LOW,
                scope=ImplementationScope.SMALL,
                confidence=Confidence.HIGH,
                reason="the statement is an exact reverse identity, not a census",
            ),
            _proposal(
                2,
                "proof_guided_hypothesis_refinement",
                "ReverseAdd Lean already expresses btReverseZ",
                "Formalize the survived identity from existing encodeZ / btReverseZ.",
                "Reuse Problems.Engine.ReverseAdd. No new residual state.",
                "proof-guided hypothesis refinement",
                "Lean lemma covering the English statement",
                "A domain element whose two-step image violates the identity.",
                novelty=NoveltyRisk.LOW,
                scope=ImplementationScope.SMALL,
                confidence=Confidence.HIGH,
                reason="btReverseZ is already the map definition",
            ),
            _proposal(
                3,
                "symbolic_nonlinear_composition",
                "Juggler remains the only gated composition attack",
                "Do not copy the Juggler domain. Keep reverse-add target-specific.",
                "Keep composition gated. Do not thaw DEFAULT_ATTACK_ORDER.",
                "symbolic nonlinear branch composition",
                "a second target-specific lemma or a closed obstruction",
                "A reverse-add sample on which the new identity fails.",
                novelty=NoveltyRisk.MEDIUM,
                scope=ImplementationScope.MEDIUM,
                confidence=Confidence.MEDIUM,
                reason="method transfer is still target-by-target",
            ),
        )
    else:
        items = (
            _proposal(
                1,
                "symbolic_nonlinear_composition",
                "two-step reverse cancellation and sign laws fail",
                "The missing coordinate is the balanced-ternary carry of x+W(x), not T^2 size.",
                "Keep k=2. Do not build a palindrome-language engine or reopen reverse_gap.",
                "symbolic nonlinear branch composition",
                "exact carry/word identity or a closed failing class",
                "A sample whose carry description disagrees with exact I/O.",
                novelty=NoveltyRisk.HIGH,
                scope=ImplementationScope.LARGE,
                confidence=Confidence.MEDIUM,
                reason="Phase-4 showed W(x)+W(T(x))=0 and sign(T^2)=sign(x) both fail",
            ),
            _proposal(
                2,
                "basin_preimage_grammar",
                "composition did not produce a reverse Lyapunov law",
                "Characterize predecessors of 0 under reverse-plus-add.",
                "Bounded preimage with a residue/word quotient.",
                "symbolic predecessor construction",
                "regular-preimage lemma or splitting pair",
                "Two predecessors indistinguishable by the quotient.",
                novelty=NoveltyRisk.MEDIUM,
                scope=ImplementationScope.MEDIUM,
                confidence=Confidence.MEDIUM,
                reason="basin language is independent of T^2 cancellation",
            ),
            _proposal(
                3,
                "ranking_function_synthesis",
                "do not reopen reverse_gap or scalar ranking",
                "Revisit ranking only if a carry coordinate is named exactly.",
                "Keep ranking downstream of composition. Do not enlarge the Phase-0 grid.",
                "ranking-function synthesis",
                "ranking certificate using a coordinate named by carry analysis",
                "The new coordinate still fails to decrease on an exact transition.",
                novelty=NoveltyRisk.HIGH,
                scope=ImplementationScope.LARGE,
                confidence=Confidence.LOW,
                reason="Phase 0/1 already falsified scalar ranking and reverse_gap",
            ),
        )
    return AttackProposalDossier(
        proposals=items,
        campaign_id=TARGET,
        notes=(
            "updated from reverse-add composition Phase-4 falsifier; not executed",
            "reverse_add_symbolic_composition is not registered as a production attack",
        ),
    )


def phase4_payload(
    outcomes: tuple[CandidateOutcome, ...],
    *,
    classification: ReverseCompositionClass,
    decision_reason: str,
    transition_window: dict[str, Any],
) -> dict[str, Any]:
    survivors = [item.as_dict() for item in outcomes if item.survived]
    counterexamples = [
        item.as_dict()["counterexample"]
        for item in outcomes
        if item.counterexample is not None
    ]
    dossier = updated_proposals(classification)
    green = classification is ReverseCompositionClass.REVERSE_COMPOSITION_GREEN_LOOT
    return {
        "engine_control_version": ENGINE_CONTROL_VERSION,
        "source_engine": "v2.3",
        "experimental_status": "PHASE_4_REVERSE_ADD_COMPOSITION_FALSIFIER",
        "target": TARGET,
        "composition_depth": DEPTH,
        "experiment_name": EXPERIMENT_NAME,
        "gated": True,
        "candidate_statements": [item.as_dict() for item in outcomes],
        "domains": [item.relevant_domain for item in outcomes],
        "transition_window": transition_window,
        "counterexamples": counterexamples,
        "failure_mechanisms": [
            {"name": item.name, "class": item.failure_class, "text": item.failure_mechanism}
            for item in outcomes
            if not item.survived
        ],
        "survivors": survivors,
        "lean_status": "NOT_YET_FORMALIZATION_READY",
        "mathematical_status": "none" if not green else "NEW_STRUCTURAL_LEMMA",
        "classification": classification.value,
        "decision": classification.value,
        "decision_reason": decision_reason,
        "green_loot": "NO_NEW_LOOT" if not green else "reverse two-step identity",
        "top3_attack_update": dossier.as_dict(),
        "global_consequence": "NONE",
    }


def render_phase4_markdown(payload: Mapping[str, Any]) -> str:
    lines = [
        "# Reverse-add two-step composition Phase-4 falsifier",
        "",
        "Status: **PHASE_4_REVERSE_ADD_COMPOSITION_FALSIFIER**",
        "",
        "This is not a reverse-and-add solver, not a termination attack, and not a",
        "general composition engine. It tests whether k=2 exposes an exact reverse",
        "relation that one-step ranking and reverse_gap could not see.",
        "",
        "## Branch budget",
        "",
        "```text",
        "Mathematical target     Does T^2(x)=x+W(x)+W(T(x)) have an exact structural",
        "                        relation invisible at one step?",
        "Novelty hypothesis      Two reverse terms cancel, preserve sign, or add at",
        "                        most one trit — the Juggler method on a different map.",
        "Falsifier               An exact two-step sample violating each candidate, or",
        "                        a survivor that is only a finite-table restatement.",
        "Existing machinery      ReverseAddSpec, bt_reverse, encode, bt_length, WINDOW,",
        "                        seed-196 orbit, Problems.Engine.ReverseAdd.",
        "Maximum Phase-4 scope   k=2; three pre-ranked candidates; frozen window+orbit.",
        "Promotion criterion     Exact reverse identity, natural domain, Lean path.",
        "Stop criterion          k>2, palindrome engine, coefficient search, census growth.",
        "```",
        "",
        "## Metadata",
        "",
        f"- engine_control_version: `{payload['engine_control_version']}`",
        f"- source_engine: `{payload['source_engine']}`",
        f"- experimental_status: `{payload['experimental_status']}`",
        f"- target: `{payload['target']}`",
        f"- composition depth: {payload['composition_depth']}",
        f"- classification: **{payload['classification']}**",
        f"- lean: `{payload['lean_status']}`",
        f"- green loot: `{payload['green_loot']}`",
        f"- decision reason: {payload['decision_reason']}",
        "",
        "Candidate list frozen at three. reverse_gap is not reopened.",
        "`DEFAULT_ATTACK_ORDER` is unchanged. No production reverse-add attack.",
        "",
    ]
    for item in payload["candidate_statements"]:
        mark = "survived" if item["survived"] else "failed"
        lines.extend(
            [
                f"## Candidate {item['rank']}: `{item['name']}` ({mark})",
                "",
                f"- Statement: {item['exact_statement']}",
                f"- Motivation: {item['motivation']}",
                f"- Domain: {item['relevant_domain']}",
                f"- Expected yield: {item['expected_yield']}",
                f"- Cheapest falsifier: {item['cheapest_falsifier']}",
                f"- Checked: {item['checked']}",
                "",
            ]
        )
        if item.get("counterexample"):
            cex = item["counterexample"]
            lines.append(
                f"- Counterexample: `{cex['source']} -> {cex['mid']} -> {cex['image']}` "
                f"(W={cex['w_source']}, W(T)={cex['w_mid']})"
            )
            lines.append(f"- Failure class: `{item['failure_class']}`")
            lines.append(f"- Mechanism: {item['failure_mechanism']}")
            lines.append("")
    window = payload.get("transition_window") or {}
    lines.extend(
        [
            "## Transition window",
            "",
            f"- Frozen discovery window: {window.get('window', '—')}",
            f"- Packet orbit seed: {window.get('orbit_seed', '—')}",
            f"- Two-step samples: {window.get('sample_count', '—')}",
            "",
            "## Decision",
            "",
            f"**{payload['decision']}**",
            "",
            payload["decision_reason"] + ".",
            "",
            f"Green loot: `{payload['green_loot']}`. Lean: `{payload['lean_status']}`.",
            "Not a halt theorem. Not a production attack.",
            "",
            "## Best next question",
            "",
            "Is the missing reverse-add coordinate the balanced-ternary carry of `x+W(x)`, "
            "and should that be a separate Phase-5 falsifier rather than a composition engine?",
            "",
        ]
    )
    return "\n".join(lines)
