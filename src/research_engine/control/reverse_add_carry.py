"""Phase-5 reverse-add balanced-ternary carry falsifier. Not an attack.

The statistic is carry-chain length of the single addition T(x)=x+W(x).
Composition depth is frozen at 1. No ranking search. No production registry.
"""

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
DEPTH = 1
EXPERIMENT_NAME = "carry_phase5"
STATISTIC_NAME = "carry_chain_length"


class CarryClass(str, Enum):
    CARRY_GREEN_LOOT = "CARRY_GREEN_LOOT"
    CARRY_PROMISING = "CARRY_PROMISING"
    CARRY_NEEDS_RICHER_STATE = "CARRY_NEEDS_RICHER_STATE"
    CARRY_REFUTED = "CARRY_REFUTED"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"


CARRY_DEFINITION = {
    "statistic": STATISTIC_NAME,
    "preference_order": [
        "carry_chain_length",
        "carry_event_count",
        "carry_weighted_span",
    ],
    "selected": "carry_chain_length",
    "source": "bt.normalization.add_with_trace",
    "formula": (
        "C(x) is the longest run of consecutive LSD-first positions affected "
        "by nonzero carry while adding the canonical words for x and W(x)."
    ),
}

CANONICALIZATION = {
    "digit_index": "LSD-first: index i is the coefficient of 3^i, matching add_with_trace",
    "leading_zeros": "encode and from_digits_lsd strip canonical leading zeros",
    "carry_values": "rewrite_sum produces carry in {-1, 0, +1}",
    "negatives": "encode is sign-aware; C is computed on encode(x) and encode(W(x))",
    "msd_carry_counts": True,
    "digit_cancellation": (
        "A position is affected iff carry_in != 0 or carry_out != 0. "
        "Opposite-trit cancellation with carry_in = carry_out = 0 is not a carry event. "
        "A nonzero final_carry creates an extra MSD position that counts."
    ),
    "zero": "encode(0) is the one-digit word (0); C(0)=0",
    "deterministic": "the same integer always yields the same C",
}


def carry_chain_length(
    steps: tuple[tuple[int, int], ...],
    final_carry: int = 0,
) -> int:
    """Longest consecutive affected-position run.

    ``steps`` are LSD-first ``(carry_in, carry_out)`` pairs from the existing
    addition trace. A nonzero ``final_carry`` counts as one extra MSD position.
    """
    flags: list[bool] = [cin != 0 or cout != 0 for cin, cout in steps]
    if final_carry != 0:
        flags.append(True)
    best = 0
    run = 0
    for flag in flags:
        if flag:
            run += 1
            if run > best:
                best = run
        else:
            run = 0
    return best


@dataclass(frozen=True)
class CarrySample:
    source: int
    image: int
    w_source: int
    len_source: int
    len_image: int
    carry_chain: int
    note: str = ""

    @property
    def length_delta(self) -> int:
        return self.len_image - self.len_source

    def as_dict(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "image": self.image,
            "w_source": self.w_source,
            "len_source": self.len_source,
            "len_image": self.len_image,
            "length_delta": self.length_delta,
            "carry_chain": self.carry_chain,
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
    holds: Callable[[CarrySample], bool]
    in_domain: Callable[[CarrySample], bool]


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
    counterexample: CarrySample | None
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
            name="carry_bounds_length_growth",
            exact_statement=(
                "C(x) >= max(0, bt_length(T(x)) - bt_length(x)) for the one-step "
                "addition T(x)=x+W(x)"
            ),
            motivation=(
                "A canonical word sum grows in length only when carry reaches a new "
                "MSD. Carry-chain length is therefore a lower bound on length growth."
            ),
            relevant_domain="integers with a defined one-step reverse-plus-add successor",
            expected_yield="an exact carry-to-length obstruction from the addition mechanism",
            cheapest_falsifier=(
                "the first frozen seed whose canonical length grows by more than C(x)"
            ),
            failure_class="LENGTH_DECOUPLING",
            in_domain=lambda _item: True,
            holds=lambda item: item.carry_chain >= max(0, item.length_delta),
        ),
        RankedCandidate(
            rank=2,
            name="zero_carry_preserves_length",
            exact_statement=(
                "C(x)=0 implies bt_length(T(x))=bt_length(x) for the one-step "
                "addition T(x)=x+W(x)"
            ),
            motivation=(
                "If no position is affected by carry, the digitwise sum never rewrites. "
                "The only remaining length change would be leading-digit cancellation, "
                "so zero carry should preserve canonical length exactly."
            ),
            relevant_domain="integers with C(x)=0 and a defined one-step successor",
            expected_yield="an exact zero-carry simplification of the reverse-plus-add word",
            cheapest_falsifier="the first frozen seed with C(x)=0 whose canonical length changes",
            failure_class="REVERSAL_DEPENDENCE",
            in_domain=lambda item: item.carry_chain == 0,
            holds=lambda item: item.len_image == item.len_source,
        ),
        RankedCandidate(
            rank=3,
            name="positive_carry_forces_length_plus_one",
            exact_statement=(
                "C(x)>0 implies bt_length(T(x))-bt_length(x)=1 for the one-step "
                "addition T(x)=x+W(x)"
            ),
            motivation=(
                "If carry were the hidden coordinate of representation change, a "
                "nonzero chain would force the only nontrivial one-step length delta "
                "available to a word sum: growth by exactly one trit."
            ),
            relevant_domain="integers with C(x)>0 and a defined one-step successor",
            expected_yield="a one-dimensional carry law determining successor length",
            cheapest_falsifier=(
                "the first frozen seed with C(x)>0 whose length delta is not +1"
            ),
            failure_class="LENGTH_DECOUPLING",
            in_domain=lambda item: item.carry_chain > 0,
            holds=lambda item: item.length_delta == 1,
        ),
    )


def evaluate_candidate(
    candidate: RankedCandidate,
    samples: tuple[CarrySample, ...],
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
    if checked < 1:
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
            failure_mechanism="no frozen samples on the stated domain",
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


def _mechanism(candidate: RankedCandidate, item: CarrySample) -> str:
    if candidate.name == "carry_bounds_length_growth":
        return (
            f"Length growth exceeds carry-chain length: C({item.source})="
            f"{item.carry_chain} but bt_length({item.image})-bt_length({item.source})"
            f"={item.length_delta}."
        )
    if candidate.name == "zero_carry_preserves_length":
        return (
            f"Zero carry still changes canonical length: C({item.source})=0, "
            f"W({item.source})={item.w_source}, {item.source}->{item.image}, "
            f"bt_length {item.len_source}->{item.len_image}. Opposite-trit "
            f"cancellation from reverse-as-negation collapses the word without carry."
        )
    return (
        f"Positive carry does not force +1 length: C({item.source})="
        f"{item.carry_chain}, {item.source}->{item.image} has "
        f"bt_length {item.len_source}->{item.len_image} (delta {item.length_delta})."
    )


def classify(outcomes: tuple[CandidateOutcome, ...]) -> tuple[CarryClass, str]:
    if any(item.checked < 1 and not item.survived and item.counterexample is None for item in outcomes):
        if all(item.checked < 1 for item in outcomes):
            return (
                CarryClass.INSUFFICIENT_DATA,
                "the frozen artifacts do not contain enough one-step samples",
            )
    survivors = [item for item in outcomes if item.survived]
    failed = [item for item in outcomes if not item.survived]
    by_name = {item.name: item for item in outcomes}
    growth = by_name.get("carry_bounds_length_growth")
    zero = by_name.get("zero_carry_preserves_length")
    positive = by_name.get("positive_carry_forces_length_plus_one")
    if all(item.survived for item in outcomes):
        return (
            CarryClass.CARRY_PROMISING,
            "all three one-step carry/length statements survived the frozen sample",
        )
    if len(failed) == 3:
        return (
            CarryClass.CARRY_REFUTED,
            "the three natural one-dimensional carry/length statements all fail",
        )
    if positive is not None and not positive.survived and any(item.survived for item in (growth, zero) if item is not None):
        return (
            CarryClass.CARRY_NEEDS_RICHER_STATE,
            "carry is related to the addition but a one-dimensional chain length "
            "does not determine the successor length delta",
        )
    if survivors and failed:
        return (
            CarryClass.CARRY_NEEDS_RICHER_STATE,
            "a one-dimensional carry statistic is not sufficient for the tested successor laws",
        )
    return (
        CarryClass.CARRY_REFUTED,
        "carry propagation is not a useful coordinate for the tested length questions",
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


def _keep_composition_lead(*, carry_note: str) -> AttackProposalDossier:
    items = (
        _proposal(
            1,
            "symbolic_nonlinear_composition",
            "one-step carry did not produce a successor law",
            "Keep the leading reverse-add proposal on nonlinear composition of W, not on C.",
            "Do not register carry_structure_analysis or a production carry attack.",
            "symbolic nonlinear branch composition",
            "an exact reverse identity that uses more than one carry number",
            "A reverse-add sample whose named identity fails.",
            novelty=NoveltyRisk.HIGH,
            scope=ImplementationScope.LARGE,
            confidence=Confidence.MEDIUM,
            reason="Phase-5 showed a 1-D carry statistic is not a ranking or length oracle",
        ),
        _proposal(
            2,
            "basin_preimage_grammar",
            "carry did not explain one-step representation change",
            "Characterize predecessors of 0 under reverse-plus-add.",
            "Bounded preimage with a residue/word quotient. Do not reopen reverse_gap.",
            "symbolic predecessor construction",
            "regular-preimage lemma or splitting pair",
            "Two predecessors indistinguishable by the quotient.",
            novelty=NoveltyRisk.MEDIUM,
            scope=ImplementationScope.MEDIUM,
            confidence=Confidence.MEDIUM,
            reason="basin language is independent of the one-step carry statistic",
        ),
        _proposal(
            3,
            "ranking_function_synthesis",
            "do not reopen reverse_gap or scalar ranking",
            "Revisit ranking only after a coordinate richer than C is named exactly.",
            "Keep ranking downstream. Do not enlarge the Phase-0 grid.",
            "ranking-function synthesis",
            "ranking certificate using a coordinate named after carry was falsified as 1-D",
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
            "updated from reverse-add carry Phase-5 falsifier; not executed",
            carry_note,
            "balanced_ternary_carry_attack is not registered",
            "reverse_gap remains closed",
        ),
    )


def updated_proposals(classification: CarryClass) -> AttackProposalDossier:
    if classification is CarryClass.CARRY_GREEN_LOOT:
        items = (
            _proposal(
                1,
                "carry_structure_analysis",
                "exact one-step carry law",
                "Package the survived carry/length lemma as a later Phase, not a flood attack.",
                "Keep k=1. Do not start a general digit-dynamics engine.",
                "balanced-ternary carry analysis of x+W(x)",
                "Lean lemma on C and bt_length",
                "A domain element violating the lemma.",
                novelty=NoveltyRisk.LOW,
                scope=ImplementationScope.SMALL,
                confidence=Confidence.HIGH,
                reason="the statement is an exact carry identity, not a census",
            ),
            _proposal(
                2,
                "symbolic_nonlinear_composition",
                "carry is a supporting coordinate, not a composition engine",
                "Ask whether the survived carry law composes with W.",
                "Keep composition gated. Do not thaw DEFAULT_ATTACK_ORDER.",
                "symbolic nonlinear branch composition",
                "a composition identity that uses C",
                "A reverse-add sample on which C does not constrain T^2.",
                novelty=NoveltyRisk.MEDIUM,
                scope=ImplementationScope.MEDIUM,
                confidence=Confidence.MEDIUM,
                reason="carry loot is still one-step; composition remains open",
            ),
            _proposal(
                3,
                "proof_guided_hypothesis_refinement",
                "ReverseAdd Lean does not yet expose carry traces",
                "Formalize the survived identity only if carry can be named in existing ReverseAdd.",
                "Do not add general carry-proof infrastructure solely to force a proof.",
                "proof-guided hypothesis refinement",
                "Lean lemma covering the English statement",
                "A domain element whose one-step image violates the identity.",
                novelty=NoveltyRisk.MEDIUM,
                scope=ImplementationScope.MEDIUM,
                confidence=Confidence.MEDIUM,
                reason="Problems.Engine.ReverseAdd has no carry-trace lemmas",
            ),
        )
        return AttackProposalDossier(
            proposals=items,
            campaign_id=TARGET,
            notes=(
                "updated from reverse-add carry Phase-5 falsifier; not executed",
                "carry_structure_analysis is proposed, not registered",
            ),
        )
    if classification is CarryClass.CARRY_PROMISING:
        return _keep_composition_lead(
            carry_note=(
                "carry correlates with length growth on the frozen sample; keep "
                "symbolic_nonlinear_composition as the leading proposal and treat "
                "C as a supporting coordinate"
            ),
        )
    if classification is CarryClass.CARRY_REFUTED:
        return _keep_composition_lead(
            carry_note=(
                "carry_structure_analysis is not kept as a future attack; the "
                "one-dimensional carry hypothesis was refuted"
            ),
        )
    return _keep_composition_lead(
        carry_note=(
            "carry is related to x+W(x) but is not a sufficient one-dimensional "
            "coordinate; keep symbolic_nonlinear_composition as the leading proposal"
        ),
    )


def lean_status_for(classification: CarryClass) -> str:
    if classification is CarryClass.INSUFFICIENT_DATA:
        return "NOT_YET_FORMALIZATION_READY"
    return "FORMALIZATION_BLOCKED"


def phase5_payload(
    outcomes: tuple[CandidateOutcome, ...],
    *,
    classification: CarryClass,
    decision_reason: str,
    transition_window: dict[str, Any],
    special_probes: list[dict[str, Any]],
) -> dict[str, Any]:
    survivors = [item.as_dict() for item in outcomes if item.survived]
    first_counterexamples = [
        {
            "name": item.name,
            "rank": item.rank,
            "failure_class": item.failure_class,
            "counterexample": item.as_dict()["counterexample"],
        }
        for item in outcomes
        if item.counterexample is not None
    ]
    dossier = updated_proposals(classification)
    green = classification is CarryClass.CARRY_GREEN_LOOT
    return {
        "engine_control_version": ENGINE_CONTROL_VERSION,
        "source_engine": "v2.3",
        "experimental_status": "PHASE_5_REVERSE_ADD_CARRY_FALSIFIER",
        "target": TARGET,
        "composition_depth": DEPTH,
        "experiment_name": EXPERIMENT_NAME,
        "gated": True,
        "carry_definition": CARRY_DEFINITION,
        "canonicalization": CANONICALIZATION,
        "candidate_statements": [item.as_dict() for item in outcomes],
        "domains": [item.relevant_domain for item in outcomes],
        "special_probes": special_probes,
        "transition_window": transition_window,
        "survivors": survivors,
        "first_counterexamples": first_counterexamples,
        "failure_mechanisms": [
            {"name": item.name, "class": item.failure_class, "text": item.failure_mechanism}
            for item in outcomes
            if not item.survived
        ],
        "lean_status": lean_status_for(classification),
        "mathematical_status": "none" if not green else "NEW_STRUCTURAL_LEMMA",
        "classification": classification.value,
        "top3_update": dossier.as_dict(),
        "decision": classification.value,
        "decision_reason": decision_reason,
        "green_loot": "CARRY_GREEN_LOOT" if green else "NO_NEW_LOOT",
        "global_consequence": "NONE",
        "laboratory_decision": "CLOSE" if classification is CarryClass.CARRY_REFUTED else "PARK",
    }


def render_phase5_markdown(payload: Mapping[str, Any]) -> str:
    lines = [
        "# Reverse-add balanced-ternary carry Phase-5 falsifier",
        "",
        "Status: **PHASE_5_REVERSE_ADD_CARRY_FALSIFIER**",
        "",
        "This is not a reverse-and-add solver, not a ranking synthesizer, and not a",
        "composition engine. It tests whether the existing addition trace of",
        "`T(x)=x+W(x)` exposes a one-dimensional carry coordinate that magnitude,",
        "length, parity, reverse-gap, and two-step composition could not see.",
        "",
        "## Branch budget",
        "",
        "```text",
        "Mathematical target     Does carry in x+W(x) have an exact structural signal",
        "                        invisible to magnitude, bt_length, reverse_gap, and T^2?",
        "Novelty hypothesis      Carry-chain length of the canonical addition is the",
        "                        missing one-step coordinate of representation change.",
        "Falsifier               An exact one-step sample violating each candidate, or",
        "                        a survivor that is only the definition of carry.",
        "Existing machinery      ReverseAddSpec, encode, bt_reverse, bt_length,",
        "                        add_with_trace, WINDOW, seed-196 orbit, ReverseAdd.",
        "Maximum Phase-5 scope   k=1; statistic A; three pre-ranked candidates;",
        "                        frozen window+orbit.",
        "Promotion criterion     Exact nontrivial carry law, not definitional, Lean path.",
        "Stop criterion          new arithmetic engine, k>1, census growth, ranking,",
        "                        digit-language framework.",
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
        "`DEFAULT_ATTACK_ORDER` is unchanged. No production carry attack.",
        "The Phase-4 two-step length bound is not proved here.",
        "",
        "## Carry definition",
        "",
        f"- Statistic: `{payload['carry_definition']['selected']}`",
        f"- Source: `{payload['carry_definition']['source']}`",
        f"- Formula: {payload['carry_definition']['formula']}",
        "",
        "## Canonicalization",
        "",
        f"- Digit index: {payload['canonicalization']['digit_index']}",
        f"- Leading zeros: {payload['canonicalization']['leading_zeros']}",
        f"- Carry values: {payload['canonicalization']['carry_values']}",
        f"- Negatives: {payload['canonicalization']['negatives']}",
        f"- Carry into a new MSD counts: `{payload['canonicalization']['msd_carry_counts']}`",
        f"- Cancellation: {payload['canonicalization']['digit_cancellation']}",
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
                f"- Counterexample: `{cex['source']} -> {cex['image']}` "
                f"(C={cex['carry_chain']}, W={cex['w_source']}, "
                f"length {cex['len_source']}->{cex['len_image']})"
            )
            lines.append(f"- Failure class: `{item['failure_class']}`")
            lines.append(f"- Mechanism: {item['failure_mechanism']}")
            lines.append("")
    lines.extend(
        [
            "## Special probes",
            "",
        ]
    )
    for probe in payload.get("special_probes") or []:
        lines.append(
            f"- `{probe.get('role', '')}`: x={probe.get('source')} -> "
            f"T={probe.get('image')}, W={probe.get('w_source')}, "
            f"C={probe.get('carry_chain')}, "
            f"length {probe.get('len_source')}->{probe.get('len_image')}"
        )
    window = payload.get("transition_window") or {}
    lines.extend(
        [
            "",
            "## Transition window",
            "",
            f"- Frozen discovery window: {window.get('window', '—')}",
            f"- Packet orbit seed: {window.get('orbit_seed', '—')}",
            f"- One-step samples: {window.get('sample_count', '—')}",
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
            "If carry is not a sufficient one-dimensional coordinate, what exact "
            "word-level interaction of `x` and `W(x)` should be named instead?",
            "",
        ]
    )
    return "\n".join(lines)
