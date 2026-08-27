"""Phase-11 Juggler macro-dynamics falsifier. Not an attack.

Pairs the two proved k=2 branch laws and asks whether they induce an
exact macro-transition grammar. Depth frozen at 2. Not a termination
or divergence theorem. Combined direction alone is not new loot.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Mapping

from research_engine.control.juggler_odd_odd import (
    DEPTH as ODD_ODD_DEPTH,
    floor_power,
    in_d_oe,
    in_d_oo,
)
from research_engine.control.proposals import assert_not_executable
from research_engine.control.types import (
    ENGINE_CONTROL_VERSION,
    AttackProposal,
    AttackProposalDossier,
    Confidence,
    ImplementationScope,
    NoveltyRisk,
)

TARGET = "juggler_sequence"
EXPERIMENT_NAME = "juggler_macro_phase11"
LEAN_MODULE = "Problems.Juggler.Dynamics"
LEAN_COMBINED = "floorPower_odd_macro_direction"
LEAN_OE = "floorPower_odd_even_two_step_lt"
LEAN_OO = "floorPower_odd_odd_two_step_gt"
DEPTH = 2

assert DEPTH == ODD_ODD_DEPTH == 2


class MacroClass(str, Enum):
    MACRO_GRAMMAR_GREEN_LOOT = "MACRO_GRAMMAR_GREEN_LOOT"
    MACRO_GRAMMAR_PROMISING = "MACRO_GRAMMAR_PROMISING"
    MACRO_GRAMMAR_NEEDS_RICHER_STRUCTURE = "MACRO_GRAMMAR_NEEDS_RICHER_STRUCTURE"
    MACRO_GRAMMAR_REFUTED = "MACRO_GRAMMAR_REFUTED"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"


def branch_label(n: int) -> str | None:
    """B(n) for odd n with T(n) defined. E if T(n) even, O if T(n) odd."""

    if n < 1 or n % 2 == 0:
        return None
    mid = floor_power(n)
    return "E" if mid % 2 == 0 else "O"


def two_step(n: int) -> int | None:
    if n < 1:
        return None
    mid = floor_power(n)
    return floor_power(mid)


def macro_sample(n: int) -> MacroSample | None:
    label = branch_label(n)
    if label is None:
        return None
    mid = floor_power(n)
    return MacroSample(source=n, mid=mid, image=floor_power(mid), branch=label)


def complementary_odd_ge3(n: int) -> bool:
    """Odd n>=3 belongs to exactly one of D_OE or D_OO."""

    if n < 3 or n % 2 == 0:
        return False
    return (in_d_oe(n) and not in_d_oo(n)) or (in_d_oo(n) and not in_d_oe(n))


@dataclass(frozen=True)
class MacroSample:
    source: int
    mid: int
    image: int
    branch: str
    note: str = "juggler macro T^2"

    @property
    def exceptional_one(self) -> bool:
        return self.source == 1

    @property
    def image_odd(self) -> bool:
        return self.image % 2 == 1

    @property
    def contracts(self) -> bool:
        return self.image < self.source

    @property
    def expands(self) -> bool:
        return self.image > self.source

    @property
    def macro_state(self) -> tuple[int, str, int]:
        return (self.source % 2, self.branch, self.image % 2)

    def as_dict(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "mid": self.mid,
            "image": self.image,
            "branch": self.branch,
            "image_odd": self.image_odd,
            "contracts": self.contracts,
            "expands": self.expands,
            "exceptional_one": self.exceptional_one,
            "macro_state": list(self.macro_state),
            "composition_depth": DEPTH,
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
    holds: Callable[[MacroSample], bool]
    in_domain: Callable[[MacroSample], bool]


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
    counterexample: MacroSample | None
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
    """Exactly three candidates, frozen before evaluation. No fourth."""

    return (
        RankedCandidate(
            rank=1,
            name="combined_direction_law",
            exact_statement=(
                "For odd n>=3, B(n)=E => T^2(n)<n and B(n)=O => T^2(n)>n. "
                "Domains D_OE and D_OO are complementary on odd n>=3; n=1 is excluded."
            ),
            motivation=(
                "Canonical pairing of the two proved lemmas on a common domain. "
                "Survival here is COMPOSITION_OF_KNOWN_FACTS, not new loot."
            ),
            relevant_domain="odd n>=3 with T and T^2 defined",
            expected_yield="a combined direction lemma usable as input, not green loot",
            cheapest_falsifier="an odd n>=3 whose two-step direction disagrees with B(n)",
            failure_class="DEFINITIONAL_COMBINATION",
            in_domain=lambda item: item.source >= 3 and item.source % 2 == 1,
            holds=lambda item: (
                (item.branch == "E" and item.image < item.source)
                or (item.branch == "O" and item.image > item.source)
            ),
        ),
        RankedCandidate(
            rank=2,
            name="branch_determines_t2_parity",
            exact_statement=(
                "For odd n>=3, B(n)=E => T^2(n) even and B(n)=O => T^2(n) odd. "
                "The pair (P_E, P_O)=(even, odd) is the first-observation pair "
                "on the frozen mapping (n=7 even, n=3 odd), not a residue sweep."
            ),
            motivation=(
                "Does the contracting/expanding branch also determine whether "
                "the odd macro-state survives? Depth remains 2."
            ),
            relevant_domain="odd n>=3 with T and T^2 defined",
            expected_yield="a unique next parity for each branch label",
            cheapest_falsifier="the first frozen odd n>=3 whose T^2 parity disagrees with (P_E, P_O)",
            failure_class="MACRO_PARITY_NOT_DETERMINISTIC",
            in_domain=lambda item: item.source >= 3 and item.source % 2 == 1,
            holds=lambda item: (
                (item.branch == "E" and item.image % 2 == 0)
                or (item.branch == "O" and item.image % 2 == 1)
            ),
        ),
        RankedCandidate(
            rank=3,
            name="contraction_exits_odd_macro",
            exact_statement=(
                "For odd n>=3, B(n)=E => T^2(n) is even, i.e. the contracting "
                "branch leaves the odd macro domain. One-sided coupling; the "
                "expanding branch is not assumed to continue."
            ),
            motivation=(
                "The first frozen E-state n=7 has T^2=4 even. Ask whether "
                "contraction is coupled to exit from the odd macro description."
            ),
            relevant_domain="odd n>=3 with B(n)=E",
            expected_yield="deterministic exit of the odd macro after contraction",
            cheapest_falsifier="the first frozen E-state whose T^2 is odd",
            failure_class="DIRECTION_SURVIVAL_DECOUPLING",
            in_domain=lambda item: item.source >= 3 and item.branch == "E",
            holds=lambda item: item.image % 2 == 0,
        ),
    )


def evaluate_candidate(
    candidate: RankedCandidate,
    samples: tuple[MacroSample, ...],
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


def _mechanism(candidate: RankedCandidate, item: MacroSample) -> str:
    if candidate.name == "combined_direction_law":
        return (
            f"Direction disagrees with B({item.source})={item.branch}: "
            f"T^2={item.image}."
        )
    if candidate.name == "branch_determines_t2_parity":
        return (
            f"T^2 parity is not a function of B: B({item.source})={item.branch} "
            f"but T^2({item.source})={item.image} has parity {item.image % 2}. "
            f"Macro-state {item.macro_state} is not determined by (parity, B)."
        )
    return (
        f"Contraction does not exit the odd macro: B({item.source})=E and "
        f"T^2({item.source})={item.image} is odd, so the odd label sequence continues."
    )


def classify(outcomes: tuple[CandidateOutcome, ...]) -> tuple[MacroClass, str]:
    if all(item.checked < 1 for item in outcomes):
        return (
            MacroClass.INSUFFICIENT_DATA,
            "the frozen artifacts do not contain odd two-step samples",
        )
    by_name = {item.name: item for item in outcomes}
    combined = by_name.get("combined_direction_law")
    parity = by_name.get("branch_determines_t2_parity")
    survival = by_name.get("contraction_exits_odd_macro")
    new_survivors = [
        item for item in outcomes if item.survived and item.name != "combined_direction_law"
    ]
    if new_survivors and all(item.survived for item in outcomes):
        return (
            MacroClass.MACRO_GRAMMAR_GREEN_LOOT,
            "a nontrivial macro-transition law survived with the combined direction lemma",
        )
    if new_survivors:
        return (
            MacroClass.MACRO_GRAMMAR_PROMISING,
            "a macro implication survived on the frozen window but is not a full grammar",
        )
    if (
        combined is not None
        and combined.survived
        and parity is not None
        and not parity.survived
        and survival is not None
        and not survival.survived
    ):
        return (
            MacroClass.MACRO_GRAMMAR_NEEDS_RICHER_STRUCTURE,
            "paired direction is known; B does not determine T^2 parity or odd-macro survival",
        )
    if all(not item.survived for item in outcomes):
        return (
            MacroClass.MACRO_GRAMMAR_REFUTED,
            "all three macro candidates failed",
        )
    return (
        MacroClass.MACRO_GRAMMAR_NEEDS_RICHER_STRUCTURE,
        "the proved direction pair does not induce a next-branch grammar at this state",
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


def updated_proposals(classification: MacroClass) -> AttackProposalDossier:
    if classification is MacroClass.MACRO_GRAMMAR_GREEN_LOOT:
        items = (
            _proposal(
                1,
                "juggler_macro_grammar",
                "exact macro-transition law from the paired branch lemmas",
                "Package the survived macro implication. Do not claim termination.",
                "Keep k=2. Do not build a parity automaton.",
                "restricted symbolic composition",
                "Lean lemma on B(n) and the next odd-macro bit",
                "An odd n>=3 violating the macro implication.",
                novelty=NoveltyRisk.MEDIUM,
                scope=ImplementationScope.SMALL,
                confidence=Confidence.HIGH,
                reason="a new consequence of the paired lemmas, not their conjunction",
            ),
            _proposal(
                2,
                "odd_odd_symbolic_composition",
                "local odd-odd growth remains the complementary lemma",
                "Keep the odd-odd two-step growth lemma. Do not generalize it.",
                "odd_odd_symbolic_composition stays a proposal, not a flood attack.",
                "restricted symbolic composition",
                "unchanged T^2>n on D_OO, n>=3",
                "An n>=3 in D_OO with T^2(n)<=n.",
                novelty=NoveltyRisk.LOW,
                scope=ImplementationScope.SMALL,
                confidence=Confidence.HIGH,
                reason="floorPower_odd_odd_two_step_gt is unchanged",
            ),
            _proposal(
                3,
                "basin_preimage_grammar",
                "macro grammar is still local",
                "Phase-9 backup: basin/preimage on 7x+1 if Juggler macro stops.",
                "Do not raise k. Do not claim a halt theorem.",
                "symbolic predecessor construction",
                "regular-preimage lemma or a splitting pair",
                "Two predecessor states indistinguishable by the quotient.",
                novelty=NoveltyRisk.MEDIUM,
                scope=ImplementationScope.MEDIUM,
                confidence=Confidence.MEDIUM,
                reason="Phase-9 backup remains available",
            ),
        )
        notes = (
            "updated from Juggler macro Phase-11 falsifier; not executed",
            "juggler_macro_grammar is proposed, not registered",
            "global_consequence is LOCAL_BRANCH_LAW, not GLOBAL_TERMINATION",
        )
    else:
        items = (
            _proposal(
                1,
                "basin_preimage_grammar",
                "macro direction and macro survival are independent",
                "Promote the Phase-9 backup: basin/preimage on "
                "mx_plus_r_7x1_class_obstruction. Do not invent another "
                "Juggler micro-attack.",
                "Record macro_state_needs_richer_information. Do not add a history bit.",
                "symbolic predecessor construction",
                "regular-preimage lemma or a splitting pair for reachability of 1",
                "Two predecessor states indistinguishable by the proposed quotient.",
                novelty=NoveltyRisk.MEDIUM,
                scope=ImplementationScope.MEDIUM,
                confidence=Confidence.MEDIUM,
                reason="Phase-9 backup after a Juggler macro stop",
            ),
            _proposal(
                2,
                "odd_odd_symbolic_composition",
                "the paired local lemmas remain the Juggler green loot",
                "Keep odd-even and odd-odd two-step laws. Do not combine them into a grammar.",
                "Do not register juggler_macro_grammar.",
                "restricted symbolic composition",
                "unchanged local branch inequalities",
                "A domain element violating either proved two-step inequality.",
                novelty=NoveltyRisk.LOW,
                scope=ImplementationScope.SMALL,
                confidence=Confidence.HIGH,
                reason="the combined direction lemma is COMPOSITION_OF_KNOWN_FACTS",
            ),
            _proposal(
                3,
                "odd_even_symbolic_composition",
                "odd-even two-step decrease remains gated",
                "Keep odd_even_two_step_decrease gated. Do not thaw DEFAULT_ATTACK_ORDER.",
                "Do not raise composition depth to chase a grammar.",
                "restricted symbolic composition",
                "unchanged odd-even two-step decrease",
                "An odd-even domain element with T^2(n)>=n.",
                novelty=NoveltyRisk.LOW,
                scope=ImplementationScope.SMALL,
                confidence=Confidence.HIGH,
                reason="floorPower_odd_even_two_step_lt is unchanged",
            ),
        )
        notes = (
            "updated from Juggler macro Phase-11 falsifier; not executed",
            "macro_state_needs_richer_information",
            "juggler_macro_grammar is not registered",
            "do not invent another Juggler micro-attack",
        )
    return AttackProposalDossier(
        proposals=items,
        campaign_id=TARGET,
        notes=notes,
    )


def exceptional_one_record(samples: tuple[MacroSample, ...]) -> dict[str, Any]:
    ones = [item for item in samples if item.source == 1]
    item = ones[0] if ones else None
    return {
        "state": 1,
        "role": "exceptional terminal odd fixed point",
        "present": item is not None,
        "transition": None if item is None else item.as_dict(),
        "reason": (
            "1->1->1 is why T^2(n)>n cannot hold on all of D_OO. "
            "The combined direction lemma uses n>=3. This is not a termination result."
        ),
        "not_termination_theorem": True,
    }


def phase11_payload(samples: tuple[MacroSample, ...]) -> dict[str, Any]:
    outcomes = tuple(evaluate_candidate(item, samples) for item in ranked_candidates())
    classification, reason = classify(outcomes)
    dossier = updated_proposals(classification)
    new_survivors = [item for item in outcomes if item.survived and item.name != "combined_direction_law"]
    loot = "MACRO_GRAMMAR_GREEN_LOOT" if new_survivors and classification is MacroClass.MACRO_GRAMMAR_GREEN_LOOT else "NO_NEW_LOOT"
    lean_status = "COMPOSITION_OF_KNOWN_FACTS"
    if classification is MacroClass.MACRO_GRAMMAR_GREEN_LOOT:
        lean_status = "FORMALIZATION_READY"
    macro_insufficient = any(
        not item.survived and item.name in {"branch_determines_t2_parity", "contraction_exits_odd_macro"}
        for item in outcomes
    )
    payload: dict[str, Any] = {
        "engine_control_version": ENGINE_CONTROL_VERSION,
        "source_engine": "v2.3",
        "experimental_status": "PHASE_11_JUGGLER_MACRO_GRAMMAR_FALSIFIER",
        "experiment_name": EXPERIMENT_NAME,
        "target": TARGET,
        "composition_depth": DEPTH,
        "gated": True,
        "branch_definition": {
            "B": "E if T(n) even, O if T(n) odd, on odd n",
            "D_OE": "odd n with B(n)=E",
            "D_OO": "odd n with B(n)=O",
            "complementary_on_odd_n_ge_3": True,
        },
        "macro_state": {
            "definition": "M(n)=(parity(n), B(n), parity(T^2(n)))",
            "sufficient": not macro_insufficient,
            "status": "MACRO_STATE_INSUFFICIENT" if macro_insufficient else "MACRO_STATE_SUFFICIENT",
            "no_extra_components": True,
        },
        "candidates": [item.as_dict() for item in outcomes],
        "candidate_freeze": {
            "count": 3,
            "no_adaptive_fourth": True,
            "parity_pair": {
                "P_E": "even",
                "P_O": "odd",
                "first_E_observation": {"n": 7, "T": 18, "T2": 4},
                "first_O_observation": {"n": 3, "T": 5, "T2": 11},
            },
            "survival_coupling": {
                "branch": "E",
                "claim": "T^2 even, contraction exits odd macro",
                "first_E_observation": {"n": 7, "T": 18, "T2": 4},
            },
        },
        "domains": {
            "combined": "odd n>=3",
            "parity_pair": "odd n>=3",
            "contraction_exit": "odd n>=3 with B(n)=E",
            "exceptional": "n=1",
        },
        "existing_lemmas": {
            "odd_even": f"{LEAN_MODULE}.{LEAN_OE}",
            "odd_odd": f"{LEAN_MODULE}.{LEAN_OO}",
            "combined": f"{LEAN_MODULE}.{LEAN_COMBINED}",
        },
        "frozen_samples": [item.as_dict() for item in samples],
        "survivors": [item.as_dict() for item in outcomes if item.survived],
        "counterexamples": [
            {
                "name": item.name,
                "rank": item.rank,
                "failure_class": item.failure_class,
                "counterexample": None if item.counterexample is None else item.counterexample.as_dict(),
            }
            for item in outcomes
            if not item.survived
        ],
        "failure_mechanisms": [
            {"name": item.name, "class": item.failure_class, "text": item.failure_mechanism}
            for item in outcomes
            if not item.survived
        ],
        "exceptional_state": exceptional_one_record(samples),
        "anti_overclaim": {
            "global_termination": False,
            "global_divergence": False,
            "global_parity_grammar": False,
            "scope": "LOCAL_BRANCH_LAW",
            "combined_is_new_loot": False,
            "combined_status": "COMPOSITION_OF_KNOWN_FACTS",
        },
        "lean_status": lean_status,
        "loot_status": loot,
        "attack_proposal_update": dossier.as_dict(),
        "classification": classification.value,
        "decision": classification.value,
        "decision_reason": reason,
        "green_loot": loot,
        "mathematical_status": "none" if loot == "NO_NEW_LOOT" else "NEW_STRUCTURAL_LEMMA",
        "global_consequence": "LOCAL_BRANCH_LAW",
        "laboratory_decision": "PARK",
        "top3_update": dossier.as_dict(),
    }
    return payload


def render_phase11_markdown(payload: Mapping[str, Any]) -> str:
    lines = [
        "# Juggler macro-dynamics Phase-11 falsifier",
        "",
        "Status: **PHASE_11_JUGGLER_MACRO_GRAMMAR_FALSIFIER**",
        "",
        "This is not a termination attack, not a divergence theorem, and not a",
        "parity automaton. Depth is frozen at `k=2`. It asks whether the paired",
        "odd-even contraction and odd-odd expansion lemmas induce an exact",
        "macro-transition grammar.",
        "",
        "## Branch budget",
        "",
        "```text",
        "Mathematical target     Do the paired OE/OO two-step laws imply an exact",
        "                        macro-transition grammar for odd Juggler states?",
        "Novelty hypothesis      Direction may determine whether the odd macro-state",
        "                        survives after T^2.",
        "Falsifier               Frozen odd n>=3 whose T^2 parity or survival is not",
        "                        a function of B(n).",
        "Existing machinery      FloorPower, two proved lemmas, WINDOW+orbit 13.",
        "Maximum Phase-11 scope  Combined direction + two pre-ranked macro implications.",
        "Promotion criterion     Nontrivial B-to-next-bit law with a Lean path.",
        "Stop criterion          k>2, automaton, census growth, restatement billed as loot.",
        "```",
        "",
        "## Metadata",
        "",
        f"- engine_control_version: `{payload['engine_control_version']}`",
        f"- source_engine: `{payload['source_engine']}`",
        f"- experimental_status: `{payload['experimental_status']}`",
        f"- target: `{payload['target']}`",
        f"- composition depth: `{payload['composition_depth']}`",
        f"- classification: **{payload['classification']}**",
        f"- lean: `{payload['lean_status']}`",
        f"- loot: `{payload['loot_status']}`",
        f"- macro-state: `{payload['macro_state']['status']}`",
        f"- decision reason: {payload['decision_reason']}",
        "",
        "Candidate 1 survival is `COMPOSITION_OF_KNOWN_FACTS`, not new loot.",
        "`DEFAULT_ATTACK_ORDER` is unchanged. No production macro attack.",
        "",
        "## Branch definition",
        "",
        f"- B: {payload['branch_definition']['B']}",
        f"- Complementary on odd n>=3: `{payload['branch_definition']['complementary_on_odd_n_ge_3']}`",
        "",
        f"Macro-state `M(n)=(parity(n), B(n), parity(T^2(n)))`. "
        f"Status: `{payload['macro_state']['status']}`.",
        "",
        "## Existing lemmas",
        "",
        f"- `{payload['existing_lemmas']['odd_even']}`",
        f"- `{payload['existing_lemmas']['odd_odd']}`",
        f"- combined: `{payload['existing_lemmas']['combined']}`",
        "",
        "## Exceptional state",
        "",
        payload["exceptional_state"]["reason"],
        "",
    ]
    for item in payload.get("candidates") or []:
        status = "survived" if item["survived"] else "failed"
        lines.extend(
            [
                f"## Candidate {item['rank']}: `{item['name']}` ({status})",
                "",
                f"- Statement: {item['exact_statement']}",
                f"- Domain: {item['relevant_domain']}",
                f"- Motivation: {item['motivation']}",
                f"- Checked: {item['checked']}",
                "",
            ]
        )
        if not item["survived"]:
            cex = item.get("counterexample") or {}
            lines.append(
                f"- Counterexample: `{cex.get('source')} -> {cex.get('mid')} -> {cex.get('image')}` "
                f"(B={cex.get('branch')})"
            )
            lines.append(f"- Failure class: `{item['failure_class']}`")
            lines.append(f"- Mechanism: {item['failure_mechanism']}")
            lines.append("")
    lines.extend(
        [
            "## Decision",
            "",
            f"**{payload['decision']}**",
            "",
            payload["decision_reason"] + ".",
            "",
            f"Loot: `{payload['loot_status']}`. Lean: `{payload['lean_status']}`.",
            "Scope: `LOCAL_BRANCH_LAW`. Not `GLOBAL_TERMINATION`.",
            "`juggler_macro_grammar` is not registered.",
            "`macro_state_needs_richer_information`.",
            "",
            "## Best next question",
            "",
            "Promote the Phase-9 backup `basin_preimage_grammar` on 7x+1. "
            "Do not invent another Juggler micro-attack.",
            "",
        ]
    )
    return "\n".join(lines)
