"""Phase-6 reverse-add pairwise word-interaction falsifier. Not an attack.

The coordinate is the pre-normalization pair sum of LSD-aligned
encode(x) and encode(W(x)). Composition depth is frozen at 1.
No ranking search. No production registry.
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
EXPERIMENT_NAME = "reverse_pair_phase6"


class ReversePairClass(str, Enum):
    REVERSE_PAIR_GREEN_LOOT = "REVERSE_PAIR_GREEN_LOOT"
    REVERSE_PAIR_PROMISING = "REVERSE_PAIR_PROMISING"
    REVERSE_PAIR_NEEDS_RICHER_STRUCTURE = "REVERSE_PAIR_NEEDS_RICHER_STRUCTURE"
    REVERSE_PAIR_REFUTED = "REVERSE_PAIR_REFUTED"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"


CANONICAL_DIGIT_CONVENTION = {
    "digit_index": "LSD-first: index i is the coefficient of 3^i",
    "alignment": (
        "LSD-align encode(x) with encode(W(x)); pad the shorter word with 0 "
        "on the MSD side, matching addition"
    ),
    "self_reverse": (
        "when bt_length(x)=bt_length(W(x)), s_i = d_i + d_{L-1-i} on the "
        "canonical word of x"
    ),
    "leading_zeros": "encode strips canonical leading zeros before pairing",
    "negatives": "encode is sign-aware; digits lie in {-1,0,+1}",
    "zero": "encode(0) is the one-digit word (0); s=(0,)",
}

PAIR_DEFINITION = {
    "s_i": "left_i + right_i, the raw aligned trit sum before rewrite_sum",
    "range": "s_i in {-2,-1,0,+1,+2}",
    "not_carry": "s_i does not include incoming carry and is not a carry statistic",
    "P0": "number of aligned positions with s_i = 0",
    "P2": "number of aligned positions with |s_i| = 2",
    "Pplus": "number of aligned positions with s_i > 0",
    "Pminus": "number of aligned positions with s_i < 0",
    "R": "largest LSD index i with s_i != 0, or -1 if every s_i = 0",
}


def sign_int(n: int) -> int:
    if n > 0:
        return 1
    if n < 0:
        return -1
    return 0


def pair_sums_lsd(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    """Raw LSD-aligned pair sums. Does not apply carry rewrite."""
    if not left and not right:
        return (0,)
    n = max(len(left), len(right))
    return tuple(
        (left[i] if i < len(left) else 0) + (right[i] if i < len(right) else 0)
        for i in range(n)
    )


def pair_aggregates(sums: tuple[int, ...]) -> dict[str, int]:
    p0 = sum(1 for item in sums if item == 0)
    p2 = sum(1 for item in sums if abs(item) == 2)
    p_plus = sum(1 for item in sums if item > 0)
    p_minus = sum(1 for item in sums if item < 0)
    last = -1
    for index, item in enumerate(sums):
        if item != 0:
            last = index
    return {
        "p0": p0,
        "p2": p2,
        "p_plus": p_plus,
        "p_minus": p_minus,
        "r_last": last,
        "aligned_length": len(sums),
    }


@dataclass(frozen=True)
class PairSample:
    source: int
    image: int
    w_source: int
    len_source: int
    len_image: int
    pair_sums: tuple[int, ...]
    p0: int
    p2: int
    p_plus: int
    p_minus: int
    r_last: int
    note: str = ""

    @property
    def length_delta(self) -> int:
        return self.len_image - self.len_source

    @property
    def pair_sign(self) -> int:
        return sign_int(self.p_plus - self.p_minus)

    @property
    def aligned_length(self) -> int:
        return len(self.pair_sums)

    def as_dict(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "image": self.image,
            "w_source": self.w_source,
            "len_source": self.len_source,
            "len_image": self.len_image,
            "length_delta": self.length_delta,
            "pair_sums": list(self.pair_sums),
            "p0": self.p0,
            "p2": self.p2,
            "p_plus": self.p_plus,
            "p_minus": self.p_minus,
            "r_last": self.r_last,
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
    holds: Callable[[PairSample], bool]
    in_domain: Callable[[PairSample], bool]


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
    counterexample: PairSample | None
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
            name="cancellation_majority_blocks_growth",
            exact_statement=(
                "P0(x) > P2(x) implies bt_length(T(x)) - bt_length(x) <= 0 "
                "for the one-step addition T(x)=x+W(x)"
            ),
            motivation=(
                "A reverse pairing with more cancelling positions (s_i=0) than "
                "constructive collisions (|s_i|=2) should not grow canonical length. "
                "K is not fitted: the relation is the direct P0/P2 comparison with ΔL."
            ),
            relevant_domain="one-step reverse-plus-add states with P0(x) > P2(x)",
            expected_yield="an exact cancellation-versus-construction law for length change",
            cheapest_falsifier="the first frozen seed with P0>P2 whose canonical length grows",
            failure_class="PAIR_CANCELLATION_MISMATCH",
            in_domain=lambda item: item.p0 > item.p2,
            holds=lambda item: item.length_delta <= 0,
        ),
        RankedCandidate(
            rank=2,
            name="pair_sign_imbalance_matches_successor_sign",
            exact_statement=(
                "If P+(x) != P-(x) then sign(T(x)) = sign(P+(x)-P-(x)) "
                "for the one-step addition T(x)=x+W(x)"
            ),
            motivation=(
                "Reversal preserves the trit multiset, so any sign of T must come "
                "from aligned constructive versus destructive pair sums, not from "
                "the digit inventory of x alone."
            ),
            relevant_domain="one-step reverse-plus-add states with P+ != P-",
            expected_yield="an exact pair-majority rule for sign(T)",
            cheapest_falsifier="the first frozen seed whose pair-sign majority disagrees with sign(T)",
            failure_class="SIGN_IMBALANCE_MISMATCH",
            in_domain=lambda item: item.p_plus != item.p_minus,
            holds=lambda item: sign_int(item.image) == item.pair_sign,
        ),
        RankedCandidate(
            rank=3,
            name="length_growth_requires_top_pair",
            exact_statement=(
                "bt_length(T(x)) - bt_length(x) >= 1 implies s_{n-1} != 0, "
                "where n is the LSD-aligned pair length and s_{n-1} is the "
                "highest aligned pair sum"
            ),
            motivation=(
                "If where the interaction occurs matters more than how often, "
                "length growth should require a nonzero pair at the MSD-aligned "
                "position rather than a count of |s_i|=2 anywhere."
            ),
            relevant_domain="one-step reverse-plus-add states with ΔL >= 1",
            expected_yield="an exact positional obstruction for length growth",
            cheapest_falsifier="the first frozen seed whose length grows while the highest pair is 0",
            failure_class="POSITIONAL_MISMATCH",
            in_domain=lambda item: item.length_delta >= 1,
            holds=lambda item: bool(item.pair_sums) and item.pair_sums[-1] != 0,
        ),
    )


def evaluate_candidate(
    candidate: RankedCandidate,
    samples: tuple[PairSample, ...],
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


def _mechanism(candidate: RankedCandidate, item: PairSample) -> str:
    if candidate.name == "cancellation_majority_blocks_growth":
        return (
            f"Cancellation majority still grows length: P0({item.source})={item.p0} > "
            f"P2={item.p2}, but {item.source}->{item.image} has bt_length "
            f"{item.len_source}->{item.len_image}."
        )
    if candidate.name == "pair_sign_imbalance_matches_successor_sign":
        return (
            f"Pair-sign majority disagrees with sign(T): P+={item.p_plus}, "
            f"P-={item.p_minus}, sign(T({item.source}))={sign_int(item.image)} "
            f"for {item.source}->{item.image}. Equal-weight pair counts ignore "
            f"place value 3^i."
        )
    top = item.pair_sums[-1] if item.pair_sums else None
    return (
        f"Length grows while the highest aligned pair is zero: "
        f"{item.source}->{item.image}, ΔL={item.length_delta}, "
        f"s_{{n-1}}={top}, R={item.r_last}."
    )


def classify(outcomes: tuple[CandidateOutcome, ...]) -> tuple[ReversePairClass, str]:
    if any(item.checked < 1 and not item.survived and item.counterexample is None for item in outcomes):
        if all(item.checked < 1 for item in outcomes):
            return (
                ReversePairClass.INSUFFICIENT_DATA,
                "the frozen artifacts do not contain enough one-step samples",
            )
    survivors = [item for item in outcomes if item.survived]
    failed = [item for item in outcomes if not item.survived]
    if all(item.survived for item in outcomes):
        return (
            ReversePairClass.REVERSE_PAIR_PROMISING,
            "all three reverse-pair statements survived the frozen sample",
        )
    if len(failed) == 3:
        return (
            ReversePairClass.REVERSE_PAIR_REFUTED,
            "the three natural reverse-pair successor relations all fail",
        )
    if survivors and failed:
        return (
            ReversePairClass.REVERSE_PAIR_NEEDS_RICHER_STRUCTURE,
            "pairwise reverse interaction is visible but no simple count or "
            "top-position aggregate determines the successor",
        )
    return (
        ReversePairClass.REVERSE_PAIR_REFUTED,
        "pairwise reverse interaction is not a useful exact coordinate at this level",
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


def _keep_composition_lead(*, pair_note: str) -> AttackProposalDossier:
    items = (
        _proposal(
            1,
            "symbolic_nonlinear_composition",
            "one-step reverse-pair aggregates did not produce a successor law",
            "Keep the leading reverse-add proposal on nonlinear composition of W.",
            "Do not register reverse_pair_interaction as a production attack.",
            "symbolic nonlinear branch composition",
            "an exact reverse identity that uses the word pair, not a count",
            "A reverse-add sample whose named identity fails.",
            novelty=NoveltyRisk.HIGH,
            scope=ImplementationScope.LARGE,
            confidence=Confidence.MEDIUM,
            reason="Phase-6 showed P0/P2, pair-sign, and top-pair position are not successor oracles",
        ),
        _proposal(
            2,
            "basin_preimage_grammar",
            "pair counts did not explain one-step representation change",
            "Characterize predecessors of 0 under reverse-plus-add.",
            "Bounded preimage with a residue/word quotient. Do not reopen reverse_gap.",
            "symbolic predecessor construction",
            "regular-preimage lemma or splitting pair",
            "Two predecessors indistinguishable by the quotient.",
            novelty=NoveltyRisk.MEDIUM,
            scope=ImplementationScope.MEDIUM,
            confidence=Confidence.MEDIUM,
            reason="basin language is independent of the one-step pair counts",
        ),
        _proposal(
            3,
            "ranking_function_synthesis",
            "do not reopen reverse_gap or scalar ranking",
            "Revisit ranking only after a coordinate richer than pair counts is named exactly.",
            "Keep ranking downstream. Do not enlarge the Phase-0 grid.",
            "ranking-function synthesis",
            "ranking certificate using a coordinate named after pair aggregates were tested",
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
            "updated from reverse-add pair-interaction Phase-6 falsifier; not executed",
            pair_note,
            "reverse_pair_interaction is not registered",
            "reverse_gap remains closed",
        ),
    )


def updated_proposals(classification: ReversePairClass) -> AttackProposalDossier:
    if classification is ReversePairClass.REVERSE_PAIR_GREEN_LOOT:
        items = (
            _proposal(
                1,
                "reverse_pair_interaction",
                "exact one-step reverse-pair law",
                "Package the survived pair/successor lemma as a later Phase, not a flood attack.",
                "Keep k=1. Do not start a general digit-language engine.",
                "pairwise reverse-word interaction of x and W(x)",
                "Lean lemma on aligned pair sums and T",
                "A domain element violating the lemma.",
                novelty=NoveltyRisk.LOW,
                scope=ImplementationScope.SMALL,
                confidence=Confidence.HIGH,
                reason="the statement is an exact pair identity, not a census",
            ),
            _proposal(
                2,
                "symbolic_nonlinear_composition",
                "pair interaction is a supporting coordinate, not a composition engine",
                "Ask whether the survived pair law composes with W.",
                "Keep composition gated. Do not thaw DEFAULT_ATTACK_ORDER.",
                "symbolic nonlinear branch composition",
                "a composition identity that uses the pair coordinate",
                "A reverse-add sample on which the pair law does not constrain T^2.",
                novelty=NoveltyRisk.MEDIUM,
                scope=ImplementationScope.MEDIUM,
                confidence=Confidence.MEDIUM,
                reason="pair loot is still one-step; composition remains open",
            ),
            _proposal(
                3,
                "proof_guided_hypothesis_refinement",
                "ReverseAdd Lean does not yet expose digit-pair traces",
                "Formalize the survived identity only if encode/btReverseZ suffice.",
                "Do not add a word-algebra framework solely to force a proof.",
                "proof-guided hypothesis refinement",
                "Lean lemma covering the English statement",
                "A domain element whose one-step image violates the identity.",
                novelty=NoveltyRisk.MEDIUM,
                scope=ImplementationScope.MEDIUM,
                confidence=Confidence.MEDIUM,
                reason="Problems.Engine.ReverseAdd has no pair-sum lemmas",
            ),
        )
        return AttackProposalDossier(
            proposals=items,
            campaign_id=TARGET,
            notes=(
                "updated from reverse-add pair-interaction Phase-6 falsifier; not executed",
                "reverse_pair_interaction is proposed, not registered",
            ),
        )
    if classification is ReversePairClass.REVERSE_PAIR_PROMISING:
        return _keep_composition_lead(
            pair_note=(
                "pair interaction correlates with successor properties on the frozen "
                "sample; keep symbolic_nonlinear_composition as the leading proposal "
                "and treat the pair coordinate as supporting"
            ),
        )
    if classification is ReversePairClass.REVERSE_PAIR_REFUTED:
        return _keep_composition_lead(
            pair_note=(
                "reverse_pair_interaction is not kept as a future attack; the "
                "simple pairwise-aggregate hypothesis was refuted"
            ),
        )
    return _keep_composition_lead(
        pair_note=(
            "pairwise reverse interaction is related to x+W(x) but is not a "
            "sufficient simple aggregate; keep symbolic_nonlinear_composition "
            "as the leading proposal"
        ),
    )


def lean_status_for(classification: ReversePairClass) -> str:
    if classification is ReversePairClass.INSUFFICIENT_DATA:
        return "NOT_YET_FORMALIZATION_READY"
    return "FORMALIZATION_BLOCKED"


def phase6_payload(
    outcomes: tuple[CandidateOutcome, ...],
    *,
    classification: ReversePairClass,
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
    green = classification is ReversePairClass.REVERSE_PAIR_GREEN_LOOT
    return {
        "engine_control_version": ENGINE_CONTROL_VERSION,
        "source_engine": "v2.3",
        "experimental_status": "PHASE_6_REVERSE_PAIR_INTERACTION_FALSIFIER",
        "target": TARGET,
        "composition_depth": DEPTH,
        "experiment_name": EXPERIMENT_NAME,
        "gated": True,
        "canonical_digit_convention": CANONICAL_DIGIT_CONVENTION,
        "pair_definition": PAIR_DEFINITION,
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
        "green_loot": "REVERSE_PAIR_GREEN_LOOT" if green else "NO_NEW_LOOT",
        "global_consequence": "NONE",
        "laboratory_decision": "CLOSE" if classification is ReversePairClass.REVERSE_PAIR_REFUTED else "PARK",
    }


def render_phase6_markdown(payload: Mapping[str, Any]) -> str:
    lines = [
        "# Reverse-add pairwise word-interaction Phase-6 falsifier",
        "",
        "Status: **PHASE_6_REVERSE_PAIR_INTERACTION_FALSIFIER**",
        "",
        "This is not a reverse-and-add solver, not a ranking synthesizer, and not a",
        "digit-language engine. It tests whether the pre-normalization alignment of",
        "`encode(x)` with `encode(W(x))` exposes an exact successor coordinate that",
        "magnitude, length, reverse-gap, two-step composition, and carry-chain",
        "length could not see.",
        "",
        "## Branch budget",
        "",
        "```text",
        "Mathematical target     Do aligned pair sums of encode(x) and encode(W(x))",
        "                        yield an exact successor law invisible to C, length,",
        "                        reverse_gap, and T^2?",
        "Novelty hypothesis      Pre-normalization reverse pairing, not the carry",
        "                        scalar, is the missing one-step coordinate.",
        "Falsifier               An exact one-step sample violating each candidate, or",
        "                        a survivor that is only the definition of s_i.",
        "Existing machinery      ReverseAddSpec, encode, bt_reverse, bt_length,",
        "                        add_with_trace, WINDOW, seed-196 orbit.",
        "Maximum Phase-6 scope   k=1; three pre-ranked pair candidates; frozen",
        "                        window+orbit.",
        "Promotion criterion     Exact nontrivial pair/successor law, Lean path.",
        "Stop criterion          digit-language engine, k>1, census growth, ranking,",
        "                        coefficient search.",
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
        "`DEFAULT_ATTACK_ORDER` is unchanged. No production pair attack.",
        "Phase-4/5 observations are not proved here.",
        "",
        "## Pair convention",
        "",
        f"- Digit index: {payload['canonical_digit_convention']['digit_index']}",
        f"- Alignment: {payload['canonical_digit_convention']['alignment']}",
        f"- Equal-length case: {payload['canonical_digit_convention']['self_reverse']}",
        f"- Pair sum: {payload['pair_definition']['s_i']}",
        f"- Range: {payload['pair_definition']['range']}",
        f"- Not carry: {payload['pair_definition']['not_carry']}",
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
                f"(P0={cex['p0']}, P2={cex['p2']}, P+={cex['p_plus']}, "
                f"P-={cex['p_minus']}, R={cex['r_last']}, "
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
            f"s={probe.get('pair_sums')}, P0={probe.get('p0')}, P2={probe.get('p2')}, "
            f"P+={probe.get('p_plus')}, P-={probe.get('p_minus')}, "
            f"R={probe.get('r_last')}, length {probe.get('len_source')}->{probe.get('len_image')}"
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
            "If simple pair counts and the top aligned position do not determine T, "
            "what exact remaining interaction of `x` and `W(x)` is still not a "
            "digit-language engine?",
            "",
        ]
    )
    return "\n".join(lines)
