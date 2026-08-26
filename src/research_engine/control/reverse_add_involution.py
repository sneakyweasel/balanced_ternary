"""Phase-8 reverse-add involution-interaction falsifier. Not an attack.

Objects: x, W(x), T(x)=x+W(x), W(T(x)). Not T^2. Not a ranking search.
W(W(x))=x is definitional on its true domain and is not loot.
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
EXPERIMENT_NAME = "reverse_involution_phase8"

FORBIDDEN_STATISTIC_KEYS = frozenset(
    {
        "weighted_sum",
        "reconstructed_T",
        "reconstructed_WT",
        "full_word_hash",
        "t_squared",
    }
)


class ReverseInvolutionClass(str, Enum):
    REVERSE_INVOLUTION_GREEN_LOOT = "REVERSE_INVOLUTION_GREEN_LOOT"
    REVERSE_INVOLUTION_PROMISING = "REVERSE_INVOLUTION_PROMISING"
    REVERSE_INVOLUTION_NEEDS_RICHER_STRUCTURE = "REVERSE_INVOLUTION_NEEDS_RICHER_STRUCTURE"
    REVERSE_INVOLUTION_REFUTED = "REVERSE_INVOLUTION_REFUTED"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"


def reverse_gap_from_msd(msd: tuple[int, ...]) -> int:
    """L1 discrepancy between an MSD word and its reverse. Not a ranking."""
    rev = tuple(reversed(msd))
    return sum(abs(left - right) for left, right in zip(msd, rev))


def assert_not_reconstruction(payload: Mapping[str, Any]) -> None:
    overlap = set(payload) & FORBIDDEN_STATISTIC_KEYS
    if overlap:
        raise ValueError(f"definitional reconstruction keys present: {sorted(overlap)}")


@dataclass(frozen=True)
class InvolutionSample:
    source: int
    image: int
    w_source: int
    w_image: int
    ww_source: int
    len_source: int
    len_image: int
    gap_source: int
    gap_image: int
    msd_source: int
    msd_w: int
    msd_t: int
    note: str = ""

    @property
    def residual(self) -> int:
        return self.w_image - self.w_source

    @property
    def involutive(self) -> bool:
        return self.ww_source == self.source

    def as_dict(self) -> dict[str, Any]:
        payload = {
            "source": self.source,
            "image": self.image,
            "w_source": self.w_source,
            "w_image": self.w_image,
            "ww_source": self.ww_source,
            "residual": self.residual,
            "involutive": self.involutive,
            "len_source": self.len_source,
            "len_image": self.len_image,
            "gap_source": self.gap_source,
            "gap_image": self.gap_image,
            "msd_source": self.msd_source,
            "msd_w": self.msd_w,
            "msd_t": self.msd_t,
            "note": self.note,
        }
        assert_not_reconstruction(payload)
        return payload


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
    reverse_specificity: str
    holds: Callable[[InvolutionSample], bool]
    in_domain: Callable[[InvolutionSample], bool]


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
    counterexample: InvolutionSample | None
    failure_mechanism: str
    failure_class: str
    reverse_specificity: str
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
            "reverse_specificity": self.reverse_specificity,
            "checked": self.checked,
        }


def ranked_candidates() -> tuple[RankedCandidate, ...]:
    """Exactly three candidates, ranked before execution. Do not extend after failure."""

    return (
        RankedCandidate(
            rank=1,
            name="reverse_sum_residual_bound",
            exact_statement=(
                "|W(T(x)) - W(x)| <= |T(x) - x|, equivalently |R(x)| <= |W(x)| "
                "with R(x)=W(T(x))-W(x)"
            ),
            motivation=(
                "Reversing the newly formed sum should not create a residual "
                "larger than the original reverse contribution that produced T."
            ),
            relevant_domain="one-step reverse-plus-add states",
            expected_yield="an exact residual bound relating W(T) to W(x)",
            cheapest_falsifier="the first frozen seed with |W(T)-W(x)| > |W(x)|",
            failure_class="INVOLUTION_RESIDUAL_MISMATCH",
            reverse_specificity="REVERSE_SPECIFIC",
            in_domain=lambda _item: True,
            holds=lambda item: abs(item.residual) <= abs(item.w_source),
        ),
        RankedCandidate(
            rank=2,
            name="successor_reverse_gap_length_bound",
            exact_statement=(
                "reverse_gap(T(x)) <= reverse_gap(x) + bt_length(x), where "
                "reverse_gap is the L1 MSD-word discrepancy, not a ranking"
            ),
            motivation=(
                "Phase-1 reverse_gap ranking failed. The question here is only "
                "whether the successor's reversal defect is controlled by the "
                "original defect plus word length, the natural size of one word."
            ),
            relevant_domain="one-step reverse-plus-add states",
            expected_yield="an exact successor-gap relation without reopening ranking",
            cheapest_falsifier="the first frozen seed whose successor gap exceeds gap(x)+bt_length(x)",
            failure_class="SUCCESSOR_REVERSAL_UNCONTROLLED",
            reverse_specificity="REVERSE_SPECIFIC",
            in_domain=lambda _item: True,
            holds=lambda item: item.gap_image <= item.gap_source + item.len_source,
        ),
        RankedCandidate(
            rank=3,
            name="successor_msd_from_operand_pair",
            exact_statement=(
                "If T(x)!=0 then the MSD trit of T(x) lies in "
                "{MSD(x), MSD(W(x)), -MSD(x), -MSD(W(x))}"
            ),
            motivation=(
                "The summands are an involution pair, so the leading trit of the "
                "normalized sum should be inherited from one operand or its negative, "
                "not from a generic unrelated digit."
            ),
            relevant_domain="one-step reverse-plus-add states with T(x)!=0",
            expected_yield="an exact leading-trit constraint caused by the operand pairing",
            cheapest_falsifier="the first frozen nonzero successor whose MSD is outside the operand MSD set",
            failure_class="OPERAND_INTERACTION_MISMATCH",
            reverse_specificity="GENERIC_ARITHMETIC_RISK",
            in_domain=lambda item: item.image != 0,
            holds=lambda item: item.msd_t
            in {item.msd_source, item.msd_w, -item.msd_source, -item.msd_w},
        ),
    )


def evaluate_candidate(
    candidate: RankedCandidate,
    samples: tuple[InvolutionSample, ...],
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
            reverse_specificity=candidate.reverse_specificity,
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
            reverse_specificity=candidate.reverse_specificity,
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
        reverse_specificity=candidate.reverse_specificity,
        checked=checked,
    )


def _mechanism(candidate: RankedCandidate, item: InvolutionSample) -> str:
    if candidate.name == "reverse_sum_residual_bound":
        return (
            f"Reverse-sum residual exceeds the original reverse: R({item.source})="
            f"{item.residual}, |W({item.source})|={abs(item.w_source)}, "
            f"W(T)={item.w_image}."
        )
    if candidate.name == "successor_reverse_gap_length_bound":
        return (
            f"Successor reverse_gap is uncontrolled: gap(T({item.source}))="
            f"{item.gap_image} > gap({item.source})+L={item.gap_source}+{item.len_source}."
        )
    return (
        f"Successor MSD is not inherited from the involution pair: T({item.source})="
        f"{item.image} has MSD {item.msd_t}, operands MSD {item.msd_source} and "
        f"{item.msd_w}."
    )


def classify(outcomes: tuple[CandidateOutcome, ...]) -> tuple[ReverseInvolutionClass, str]:
    if any(item.checked < 1 and not item.survived and item.counterexample is None for item in outcomes):
        if all(item.checked < 1 for item in outcomes):
            return (
                ReverseInvolutionClass.INSUFFICIENT_DATA,
                "the frozen artifacts do not contain enough one-step samples",
            )
    survivors = [item for item in outcomes if item.survived]
    failed = [item for item in outcomes if not item.survived]
    specific = [
        item
        for item in survivors
        if item.reverse_specificity == "REVERSE_SPECIFIC"
    ]
    if all(item.survived for item in outcomes) and specific:
        return (
            ReverseInvolutionClass.REVERSE_INVOLUTION_PROMISING,
            "all three involution-interaction statements survived the frozen sample",
        )
    if specific and failed:
        return (
            ReverseInvolutionClass.REVERSE_INVOLUTION_NEEDS_RICHER_STRUCTURE,
            "reversal is involved but the tested compressed involution relations "
            "are not a reverse-specific law",
        )
    if survivors and not specific:
        return (
            ReverseInvolutionClass.REVERSE_INVOLUTION_REFUTED,
            "the only survivors are generic arithmetic, not reverse-involution loot",
        )
    if len(failed) == 3:
        return (
            ReverseInvolutionClass.REVERSE_INVOLUTION_REFUTED,
            "the three natural involution-interaction statements all fail",
        )
    return (
        ReverseInvolutionClass.REVERSE_INVOLUTION_NEEDS_RICHER_STRUCTURE,
        "involution structure is visible but no compressed reverse-specific law remains",
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


def _keep_composition_lead(*, note: str) -> AttackProposalDossier:
    items = (
        _proposal(
            1,
            "symbolic_nonlinear_composition",
            "compressed involution summaries did not produce reverse-add loot",
            "Keep the leading reverse-add proposal on nonlinear composition of W.",
            "Do not register reverse_involution_structure as a production attack.",
            "symbolic nonlinear branch composition",
            "an exact reverse identity that is not a scalar involution summary",
            "A reverse-add sample whose named identity fails.",
            novelty=NoveltyRisk.HIGH,
            scope=ImplementationScope.LARGE,
            confidence=Confidence.MEDIUM,
            reason="Phase-8 showed W(W(x))=x does not yield a compressed reverse-specific law",
        ),
        _proposal(
            2,
            "basin_preimage_grammar",
            "involution residuals do not explain basins",
            "Characterize predecessors of 0 under reverse-plus-add.",
            "Bounded preimage with a residue/word quotient. Do not reopen reverse_gap.",
            "symbolic predecessor construction",
            "regular-preimage lemma or splitting pair",
            "Two predecessors indistinguishable by the quotient.",
            novelty=NoveltyRisk.MEDIUM,
            scope=ImplementationScope.MEDIUM,
            confidence=Confidence.MEDIUM,
            reason="basin language is independent of one-step involution residuals",
        ),
        _proposal(
            3,
            "ranking_function_synthesis",
            "do not reopen reverse_gap or scalar ranking",
            "Revisit ranking only after a reverse-specific coordinate is named exactly.",
            "Keep ranking downstream. Do not enlarge the Phase-0 grid.",
            "ranking-function synthesis",
            "ranking certificate using a reverse-specific coordinate",
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
            "updated from reverse-add involution Phase-8 falsifier; not executed",
            note,
            "reverse_involution_structure is not registered",
            "reverse_gap remains closed as a ranking",
        ),
    )


def updated_proposals(classification: ReverseInvolutionClass) -> AttackProposalDossier:
    if classification is ReverseInvolutionClass.REVERSE_INVOLUTION_GREEN_LOOT:
        items = (
            _proposal(
                1,
                "reverse_involution_structure",
                "exact reverse-specific involution law",
                "Package the survived involution lemma as a later Phase, not a flood attack.",
                "Keep k=1. Do not start a digit-language engine.",
                "involution interaction of W with T(x)=x+W(x)",
                "Lean lemma on x, W(x), T(x), W(T(x))",
                "A domain element violating the lemma.",
                novelty=NoveltyRisk.LOW,
                scope=ImplementationScope.SMALL,
                confidence=Confidence.HIGH,
                reason="the statement is an exact reverse-specific identity, not a census",
            ),
            _proposal(
                2,
                "symbolic_nonlinear_composition",
                "involution loot is still one-step",
                "Ask whether the survived involution law composes.",
                "Keep composition gated. Do not thaw DEFAULT_ATTACK_ORDER.",
                "symbolic nonlinear branch composition",
                "a composition identity that uses the involution law",
                "A reverse-add sample on which the involution law does not constrain T^2.",
                novelty=NoveltyRisk.MEDIUM,
                scope=ImplementationScope.MEDIUM,
                confidence=Confidence.MEDIUM,
                reason="involution loot is still one-step; composition remains open",
            ),
            _proposal(
                3,
                "proof_guided_hypothesis_refinement",
                "ReverseAdd Lean already has btReverseZ",
                "Formalize the survived identity from existing encodeZ / btReverseZ.",
                "Do not add a word-algebra framework solely to force a proof.",
                "proof-guided hypothesis refinement",
                "Lean lemma covering the English statement",
                "A domain element whose one-step image violates the identity.",
                novelty=NoveltyRisk.MEDIUM,
                scope=ImplementationScope.MEDIUM,
                confidence=Confidence.MEDIUM,
                reason="btReverseZ is already the map definition",
            ),
        )
        return AttackProposalDossier(
            proposals=items,
            campaign_id=TARGET,
            notes=(
                "updated from reverse-add involution Phase-8 falsifier; not executed",
                "reverse_involution_structure is proposed, not registered",
            ),
        )
    if classification is ReverseInvolutionClass.REVERSE_INVOLUTION_REFUTED:
        return _keep_composition_lead(
            note="reverse_involution_not_sufficient_at_this_level; stop inventing scalar summaries",
        )
    if classification is ReverseInvolutionClass.REVERSE_INVOLUTION_PROMISING:
        return _keep_composition_lead(
            note=(
                "an involution relation survived on the frozen sample but is not "
                "green loot; keep symbolic_nonlinear_composition as the leading proposal"
            ),
        )
    return _keep_composition_lead(
        note=(
            "involution structure is involved but compressed summaries are insufficient; "
            "keep symbolic_nonlinear_composition as the leading proposal"
        ),
    )


def lean_status_for(classification: ReverseInvolutionClass) -> str:
    if classification is ReverseInvolutionClass.INSUFFICIENT_DATA:
        return "NOT_YET_FORMALIZATION_READY"
    return "FORMALIZATION_BLOCKED"


def anti_tautology_check() -> dict[str, Any]:
    return {
        "rejected_identities": [
            "W(W(x))=x",
            "T(x)=x+W(x)",
            "W(T(x))=bt_reverse(encode(T(x)))",
        ],
        "objects": ["x", "W(x)", "T(x)", "W(T(x))"],
        "not_investigated": "T^2(x)",
        "candidates_reconstruct_T": False,
        "candidates_reconstruct_WT": False,
        "forbidden_keys": sorted(FORBIDDEN_STATISTIC_KEYS),
    }


def reverse_specificity_check(outcomes: tuple[CandidateOutcome, ...]) -> list[dict[str, Any]]:
    items = []
    for outcome in outcomes:
        label = outcome.reverse_specificity
        if outcome.survived and outcome.name == "successor_msd_from_operand_pair":
            label = "GENERAL_ARITHMETIC"
        elif outcome.survived and label == "REVERSE_SPECIFIC":
            label = "BOUNDED_SURVIVOR"
        items.append(
            {
                "name": outcome.name,
                "survived": outcome.survived,
                "declared": outcome.reverse_specificity,
                "assessed": label if outcome.survived else "N/A",
                "reason": (
                    "generic leading-digit inheritance of a sum"
                    if label == "GENERAL_ARITHMETIC" and outcome.survived
                    else (
                        "uses W(T) and reverse_gap, but a finite bound is not loot"
                        if label == "BOUNDED_SURVIVOR"
                        else "failed before reverse-specificity loot could be claimed"
                    )
                ),
            }
        )
    return items


def phase8_payload(
    outcomes: tuple[CandidateOutcome, ...],
    *,
    classification: ReverseInvolutionClass,
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
    green = classification is ReverseInvolutionClass.REVERSE_INVOLUTION_GREEN_LOOT
    return {
        "engine_control_version": ENGINE_CONTROL_VERSION,
        "source_engine": "v2.3",
        "experimental_status": "PHASE_8_REVERSE_INVOLUTION_FALSIFIER",
        "target": TARGET,
        "composition_depth": DEPTH,
        "experiment_name": EXPERIMENT_NAME,
        "gated": True,
        "candidate_statements": [item.as_dict() for item in outcomes],
        "domains": [item.relevant_domain for item in outcomes],
        "special_probes": special_probes,
        "reverse_specificity_check": reverse_specificity_check(outcomes),
        "anti_tautology_check": anti_tautology_check(),
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
        "green_loot": "REVERSE_INVOLUTION_GREEN_LOOT" if green else "NO_NEW_LOOT",
        "global_consequence": "NONE",
        "laboratory_decision": "CLOSE" if classification is ReverseInvolutionClass.REVERSE_INVOLUTION_REFUTED else "PARK",
    }


def render_phase8_markdown(payload: Mapping[str, Any]) -> str:
    lines = [
        "# Reverse-add involution-interaction Phase-8 falsifier",
        "",
        "Status: **PHASE_8_REVERSE_INVOLUTION_FALSIFIER**",
        "",
        "This is not a reverse-and-add solver, not a ranking synthesizer, and not a",
        "digit-language engine. It tests whether the reversal involution produces a",
        "compressed exact relation among `x`, `W(x)`, `T(x)=x+W(x)`, and `W(T(x))`",
        "that is not generic balanced-ternary arithmetic.",
        "",
        "## Branch budget",
        "",
        "```text",
        "Mathematical target     Does W(W(x))=x create a non-generic exact law",
        "                        among x, W(x), T(x), W(T(x))?",
        "Novelty hypothesis      The useful reverse-and-add structure is the",
        "                        involution interaction, not a scalar summary.",
        "Falsifier               An exact one-step sample violating each candidate,",
        "                        a tautology, or a generic arithmetic restatement.",
        "Existing machinery      ReverseAddSpec, encode, bt_reverse, bt_length,",
        "                        reverse_gap L1, WINDOW, seed-196 orbit.",
        "Maximum Phase-8 scope   k=1; four objects; three pre-ranked candidates;",
        "                        frozen window+orbit.",
        "Promotion criterion     Reverse-specific non-tautological law, Lean path.",
        "Stop criterion          word algebra, T^2 attack, ranking, census growth,",
        "                        digit-language engine.",
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
        "Candidate list frozen at three. reverse_gap is not reopened as ranking.",
        "`DEFAULT_ATTACK_ORDER` is unchanged. No production involution attack.",
        "`W(W(x))=x` is not loot. Canonical reverse is involutive iff `x=0` or `3` does not divide `x`.",
        "",
        "## Anti-tautology",
        "",
        f"- Rejected identities: {payload['anti_tautology_check']['rejected_identities']}",
        f"- Objects: {payload['anti_tautology_check']['objects']}",
        f"- Not investigated: `{payload['anti_tautology_check']['not_investigated']}`",
        "",
    ]
    for item in payload["candidate_statements"]:
        mark = "survived" if item["survived"] else "failed"
        lines.extend(
            [
                f"## Candidate {item['rank']}: `{item['name']}` ({mark})",
                "",
                f"- Statement: {item['exact_statement']}",
                f"- Domain: {item['relevant_domain']}",
                f"- Motivation: {item['motivation']}",
                f"- Expected yield: {item['expected_yield']}",
                f"- Cheapest falsifier: {item['cheapest_falsifier']}",
                f"- Reverse-specificity (declared): `{item['reverse_specificity']}`",
                f"- Checked: {item['checked']}",
                "",
            ]
        )
        if item.get("counterexample"):
            cex = item["counterexample"]
            lines.append(
                f"- Counterexample: `{cex['source']} -> {cex['image']}` "
                f"(W={cex['w_source']}, W(T)={cex['w_image']}, R={cex['residual']}, "
                f"gap {cex['gap_source']}->{cex['gap_image']}, "
                f"WW={cex['ww_source']}, involutive={cex['involutive']})"
            )
            lines.append(f"- Failure class: `{item['failure_class']}`")
            lines.append(f"- Mechanism: {item['failure_mechanism']}")
            lines.append("")
    lines.extend(["## Reverse-specificity check", ""])
    for item in payload.get("reverse_specificity_check") or []:
        lines.append(
            f"- `{item['name']}`: survived={item['survived']}, "
            f"assessed=`{item['assessed']}` — {item['reason']}"
        )
    lines.extend(["", "## Special probes", ""])
    for probe in payload.get("special_probes") or []:
        lines.append(
            f"- `{probe.get('role', '')}`: x={probe.get('source')} -> T={probe.get('image')}, "
            f"W={probe.get('w_source')}, W(T)={probe.get('w_image')}, "
            f"WW={probe.get('ww_source')}, involutive={probe.get('involutive')}, "
            f"R={probe.get('residual')}, gap {probe.get('gap_source')}->{probe.get('gap_image')}"
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
            "Top-3 #1 remains `symbolic_nonlinear_composition`.",
            "`reverse_involution_not_sufficient_at_this_level`.",
            "`reverse_involution_structure` is not registered.",
            "",
            "## Best next question",
            "",
            "If compressed involution summaries fail, should reverse-and-add return "
            "to the existing symbolic-nonlinear frontier without a digit-language engine?",
            "",
        ]
    )
    return "\n".join(lines)
