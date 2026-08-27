"""Phase-12 Juggler parity-drift / log-log energy falsifier. Not an attack.

Fixed parity words only. Depth at most 5. Exact surrogate is T^k(n)<n
or the floor-power inequalities T(n)^2 ≤ n^3 / T(n)^2 ≤ n. Floating-point
logarithms are heuristic motivation, never a theorem verdict.
Not a termination or divergence theorem. Not a parity-frequency theorem.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Mapping

from research_engine.control.juggler_odd_odd import floor_power
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
EXPERIMENT_NAME = "juggler_parity_drift_phase12"
LEAN_MODULE = "Problems.Juggler.Envelope"
LEAN_OOOEE = "floorPower_oooee_five_step_lt"
LEAN_OE = "floorPower_odd_even_two_step_lt"
LEAN_OO = "floorPower_odd_odd_two_step_gt"
MAX_DEPTH = 5
WORD_OOOEE = "OOOEE"
WORD_EE = "EE"
PRE_RANKED_WORDS = ("EE", "OEE", "OOOE", "OOOEE", "OOOEEE")


class DriftClass(str, Enum):
    PARITY_DRIFT_GREEN_LOOT = "PARITY_DRIFT_GREEN_LOOT"
    PARITY_DRIFT_PROMISING = "PARITY_DRIFT_PROMISING"
    PARITY_DRIFT_NEEDS_RICHER_ENERGY = "PARITY_DRIFT_NEEDS_RICHER_ENERGY"
    PARITY_DRIFT_REFUTED = "PARITY_DRIFT_REFUTED"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"


def exact_negative_drift(word: str) -> bool:
    """Exact sign of idealized drift: 3^o < 2^{e+o}, no floats."""

    odd = word.count("O")
    even = word.count("E")
    return 3 ** odd < 2 ** (even + odd)


def shortest_negative_word() -> str:
    """Select C3 before exact testing. Depth > 5 is excluded."""

    negative = [
        word for word in PRE_RANKED_WORDS if len(word) <= MAX_DEPTH and exact_negative_drift(word)
    ]
    if not negative:
        raise RuntimeError("no negative-drift word of depth <= 5 in the frozen list")
    return min(negative, key=len)


assert shortest_negative_word() == WORD_EE


def iterate(n: int, steps: int) -> tuple[int, ...]:
    if steps > MAX_DEPTH:
        raise ValueError("Phase-12 depth must be at most 5")
    if n < 1:
        raise ValueError("floor_power is defined on positive integers")
    path = [n]
    current = n
    for _ in range(steps):
        current = floor_power(current)
        path.append(current)
    return tuple(path)


def word_of(path: tuple[int, ...]) -> str:
    if len(path) < 2:
        return ""
    return "".join("O" if item % 2 else "E" for item in path[:-1])


def odd_power_bound(n: int) -> bool:
    image = floor_power(n)
    return image * image <= n * n * n


def even_power_bound(n: int) -> bool:
    image = floor_power(n)
    return image * image <= n


@dataclass(frozen=True)
class DriftSample:
    source: int
    path: tuple[int, ...]
    word: str
    note: str = "juggler parity-drift block"

    @property
    def image(self) -> int:
        return self.path[-1]

    @property
    def depth(self) -> int:
        return len(self.word)

    @property
    def exceptional_one(self) -> bool:
        return self.source == 1

    @property
    def contracts(self) -> bool:
        return self.image < self.source

    def as_dict(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "path": list(self.path),
            "word": self.word,
            "image": self.image,
            "contracts": self.contracts,
            "exceptional_one": self.exceptional_one,
            "composition_depth": self.depth,
            "note": self.note,
        }


def make_sample(n: int, steps: int, *, note: str = "juggler parity-drift block") -> DriftSample:
    path = iterate(n, steps)
    return DriftSample(source=n, path=path, word=word_of(path), note=note)


@dataclass(frozen=True)
class RankedCandidate:
    rank: int
    name: str
    exact_statement: str
    motivation: str
    relevant_domain: str
    expected_yield: str
    cheapest_falsifier: str
    idealized_drift: str
    parity_word: str
    failure_class: str
    loot_eligible: bool
    holds: Callable[[DriftSample], bool]
    in_domain: Callable[[DriftSample], bool]


@dataclass(frozen=True)
class CandidateOutcome:
    rank: int
    name: str
    exact_statement: str
    motivation: str
    relevant_domain: str
    expected_yield: str
    cheapest_falsifier: str
    idealized_drift: str
    parity_word: str
    survived: bool
    counterexample: DriftSample | None
    failure_mechanism: str
    failure_class: str
    checked: int
    loot_eligible: bool
    unobserved: bool

    def as_dict(self) -> dict[str, Any]:
        return {
            "rank": self.rank,
            "name": self.name,
            "exact_statement": self.exact_statement,
            "motivation": self.motivation,
            "relevant_domain": self.relevant_domain,
            "expected_yield": self.expected_yield,
            "cheapest_falsifier": self.cheapest_falsifier,
            "idealized_drift": self.idealized_drift,
            "parity_word": self.parity_word,
            "survived": self.survived,
            "counterexample": None if self.counterexample is None else self.counterexample.as_dict(),
            "failure_mechanism": self.failure_mechanism,
            "failure_class": self.failure_class,
            "checked": self.checked,
            "loot_eligible": self.loot_eligible,
            "unobserved": self.unobserved,
        }


def pre_rank_table() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for word in PRE_RANKED_WORDS:
        odd = word.count("O")
        even = word.count("E")
        rows.append(
            {
                "word": word,
                "length": len(word),
                "odd_steps": odd,
                "even_steps": even,
                "exact_negative": exact_negative_drift(word),
                "exact_comparison": f"3^{odd} {'<' if exact_negative_drift(word) else '>='} 2^{even + odd}",
                "depth_allowed": len(word) <= MAX_DEPTH,
                "selected_as_candidate_3": word == shortest_negative_word(),
            }
        )
    return rows


def ranked_candidates() -> tuple[RankedCandidate, ...]:
    """Exactly three candidates, frozen before evaluation. No fourth."""

    selected = shortest_negative_word()
    return (
        RankedCandidate(
            rank=1,
            name="one_step_increment_bounds",
            exact_statement=(
                "For odd n>=3, T(n)^2 <= n^3 and T(n)>n. "
                "For even n>=2, T(n)^2 <= n and T(n)<n. "
                "These are the exact power surrogates of the additive log-log increments."
            ),
            motivation=(
                "Ask whether fixed additive branch costs exist as exact inequalities. "
                "The power bounds are the floor-power definitions; the signs are the "
                "one-step expansion/contraction of the exact surrogate T."
            ),
            relevant_domain="odd n>=3 or even n>=2",
            expected_yield="formalizable branch costs, or a definitional restatement",
            cheapest_falsifier="the first frozen n in the domain violating a power bound or T-sign",
            idealized_drift="odd +log(3/2), even -log 2 (heuristic only)",
            parity_word="O|E",
            failure_class="DEFINITIONAL_RESTATEMENT",
            loot_eligible=False,
            in_domain=lambda item: item.depth == 1 and (
                (item.source >= 3 and item.source % 2 == 1)
                or (item.source >= 2 and item.source % 2 == 0)
            ),
            holds=lambda item: (
                odd_power_bound(item.source) and item.source < item.image
                if item.source % 2 == 1
                else even_power_bound(item.source) and item.image < item.source
            ),
        ),
        RankedCandidate(
            rank=2,
            name="oooee_conditional_contraction",
            exact_statement=(
                "If a trajectory follows the parity word OOOEE starting at n>=2, "
                "then T^5(n)<n. Conditional on the branch word; not a claim that "
                "every orbit contains OOOEE."
            ),
            motivation=(
                "OOOEE is the first mixed block whose idealized drift is negative: "
                "3^3=27 < 2^5=32. Exact surrogate T^5(n)<n."
            ),
            relevant_domain="n>=2 whose five successive branch parities are OOOEE",
            expected_yield="conditional five-step contraction, or a floor counterexample",
            cheapest_falsifier="the first frozen OOOEE seed with T^5(n)>=n",
            idealized_drift="3^3 < 2^{2+3} (exact negative)",
            parity_word=WORD_OOOEE,
            failure_class="BLOCK_NOT_CONTRACTIVE",
            loot_eligible=True,
            in_domain=lambda item: item.word == WORD_OOOEE and item.source >= 2,
            holds=lambda item: item.image < item.source,
        ),
        RankedCandidate(
            rank=3,
            name="shortest_negative_block",
            exact_statement=(
                f"If a trajectory follows the parity word {selected} starting at n>=2, "
                f"then T^{len(selected)}(n)<n. Selected as the shortest frozen-list "
                "word with exact negative idealized drift and depth<=5."
            ),
            motivation=(
                "Among EE, OEE, OOOE, OOOEE, OOOEEE, the shortest negative-drift "
                "word of depth<=5 is EE. Do not optimize over arbitrary words."
            ),
            relevant_domain=f"n>=2 whose successive branch parities are {selected}",
            expected_yield="a short contractive block, or a restatement of even contraction",
            cheapest_falsifier=f"the first frozen {selected} seed with T^{len(selected)}(n)>=n",
            idealized_drift="3^0 < 2^{2+0} (exact negative)",
            parity_word=selected,
            failure_class="DEFINITIONAL_RESTATEMENT",
            loot_eligible=False,
            in_domain=lambda item: item.word == selected and item.source >= 2,
            holds=lambda item: item.image < item.source,
        ),
    )


def evaluate_candidate(
    candidate: RankedCandidate,
    samples: tuple[DriftSample, ...],
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
            idealized_drift=candidate.idealized_drift,
            parity_word=candidate.parity_word,
            survived=False,
            counterexample=item,
            failure_mechanism=_mechanism(candidate, item),
            failure_class=candidate.failure_class,
            checked=checked,
            loot_eligible=candidate.loot_eligible,
            unobserved=False,
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
            idealized_drift=candidate.idealized_drift,
            parity_word=candidate.parity_word,
            survived=False,
            counterexample=None,
            failure_mechanism="no frozen sample realizes the branch word; census not enlarged",
            failure_class="BRANCH_DOMAIN_EMPTY",
            checked=checked,
            loot_eligible=candidate.loot_eligible,
            unobserved=True,
        )
    failure_class = ""
    mechanism = ""
    if not candidate.loot_eligible:
        failure_class = "DEFINITIONAL_RESTATEMENT"
        mechanism = (
            "survived, but the inequality is the floor-power definition or even-branch "
            "contraction already implied by T(n)<n. Not new compositional loot."
        )
    return CandidateOutcome(
        rank=candidate.rank,
        name=candidate.name,
        exact_statement=candidate.exact_statement,
        motivation=candidate.motivation,
        relevant_domain=candidate.relevant_domain,
        expected_yield=candidate.expected_yield,
        cheapest_falsifier=candidate.cheapest_falsifier,
        idealized_drift=candidate.idealized_drift,
        parity_word=candidate.parity_word,
        survived=True,
        counterexample=None,
        failure_mechanism=mechanism,
        failure_class=failure_class,
        checked=checked,
        loot_eligible=candidate.loot_eligible,
        unobserved=False,
    )


def _mechanism(candidate: RankedCandidate, item: DriftSample) -> str:
    if candidate.name == "one_step_increment_bounds":
        return (
            f"one-step bound failed at n={item.source}: T={item.image}, "
            f"odd={item.source % 2 == 1}"
        )
    return (
        f"block {item.word} from {item.source} ends at {item.image}, "
        f"not strictly below the source"
    )


def classify(
    outcomes: tuple[CandidateOutcome, ...],
    *,
    lean_proved: bool,
) -> tuple[DriftClass, str, str]:
    if all(item.checked < 1 for item in outcomes):
        return (
            DriftClass.INSUFFICIENT_DATA,
            "INSUFFICIENT_DATA",
            "the frozen artifacts do not contain evaluable samples",
        )
    by_name = {item.name: item for item in outcomes}
    block = by_name.get("oooee_conditional_contraction")
    if block is not None and block.unobserved:
        return (
            DriftClass.INSUFFICIENT_DATA,
            "INSUFFICIENT_DATA",
            "OOOEE is unobserved on the frozen window; census not enlarged",
        )
    if block is not None and not block.survived:
        return (
            DriftClass.PARITY_DRIFT_REFUTED,
            "NO_NEW_LOOT",
            "the first mixed negative-drift block is not exactly contractive",
        )
    if block is not None and block.survived and block.loot_eligible:
        if lean_proved:
            return (
                DriftClass.PARITY_DRIFT_GREEN_LOOT,
                "PARITY_DRIFT_GREEN_LOOT",
                "OOOEE is exactly contractive and Lean-proved as a conditional block law",
            )
        return (
            DriftClass.PARITY_DRIFT_PROMISING,
            "NO_NEW_LOOT",
            "OOOEE contracted on the frozen window but remains BOUNDED_SYMBOLIC_SURVIVOR",
        )
    return (
        DriftClass.PARITY_DRIFT_NEEDS_RICHER_ENERGY,
        "NO_NEW_LOOT",
        "one-step costs are definitional; no mixed block law survived",
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


def updated_proposals(classification: DriftClass) -> AttackProposalDossier:
    if classification is DriftClass.PARITY_DRIFT_GREEN_LOOT:
        items = (
            _proposal(
                1,
                "parity_drift_block",
                "OOOEE is an exact conditional contractive block",
                "Package further k<=5 mixed blocks only as Level B conditionals. "
                "Do not infer a global parity-frequency theorem.",
                "Keep depth <= 5. Do not build a parity automaton.",
                "restricted symbolic composition",
                "another exact block inequality, still not Level C",
                "A realizing state of the next frozen word with T^k(n)>=n.",
                novelty=NoveltyRisk.MEDIUM,
                scope=ImplementationScope.SMALL,
                confidence=Confidence.HIGH,
                reason="new compositional consequence of floor-power inequalities",
            ),
            _proposal(
                2,
                "odd_odd_symbolic_composition",
                "local odd-odd growth remains complementary loot",
                "Keep the odd-odd two-step growth lemma. Do not replace it by energy.",
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
                "Level C trajectory consequence remains open and out of scope",
                "Phase-9 backup: basin/preimage on mx_plus_r_7x1_class_obstruction "
                "if block-frequency is not pursued.",
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
            "updated from Juggler parity-drift Phase-12 falsifier; not executed",
            "parity_drift_block is proposed, not registered",
            "global_consequence is LOCAL_BRANCH_LAW, not GLOBAL_TERMINATION",
            "Level C frequency implication is out of scope",
        )
    elif classification in {
        DriftClass.PARITY_DRIFT_PROMISING,
        DriftClass.PARITY_DRIFT_NEEDS_RICHER_ENERGY,
    }:
        items = (
            _proposal(
                1,
                "parity_drift",
                "energy direction is visible but the exact block law is incomplete",
                "Keep parity_drift as a research hypothesis. Refine the energy, "
                "do not invent a fourth Juggler energy family.",
                "Do not search arbitrary words. Do not thaw DEFAULT_ATTACK_ORDER.",
                "restricted symbolic composition",
                "an exact non-definitional increment or a proved mixed block",
                "A frozen realizing state violating the refined inequality.",
                novelty=NoveltyRisk.MEDIUM,
                scope=ImplementationScope.SMALL,
                confidence=Confidence.MEDIUM,
                reason="log-log sign is right; floors or proof remain open",
            ),
            _proposal(
                2,
                "odd_odd_symbolic_composition",
                "existing Juggler green loot is unchanged",
                "Keep odd-even and odd-odd two-step laws.",
                "Do not register parity_drift_block.",
                "restricted symbolic composition",
                "unchanged local branch inequalities",
                "A domain element violating either proved two-step inequality.",
                novelty=NoveltyRisk.LOW,
                scope=ImplementationScope.SMALL,
                confidence=Confidence.HIGH,
                reason="the two-step lemmas are independent of the energy experiment",
            ),
            _proposal(
                3,
                "basin_preimage_grammar",
                "Phase-9 backup remains the non-Juggler frontier",
                "basin/preimage on mx_plus_r_7x1_class_obstruction.",
                "Do not create a fourth Juggler energy attack.",
                "symbolic predecessor construction",
                "regular-preimage lemma or a splitting pair",
                "Two predecessor states indistinguishable by the quotient.",
                novelty=NoveltyRisk.MEDIUM,
                scope=ImplementationScope.MEDIUM,
                confidence=Confidence.MEDIUM,
                reason="Phase-9 backup after an incomplete energy law",
            ),
        )
        notes = (
            "updated from Juggler parity-drift Phase-12 falsifier; not executed",
            "parity_drift remains a hypothesis, not a production attack",
            "do not invent a fourth Juggler energy attack",
        )
    else:
        items = (
            _proposal(
                1,
                "basin_preimage_grammar",
                "parity-drift exact tests failed or could not be evaluated",
                "Return to the Phase-9 backup: basin/preimage on "
                "mx_plus_r_7x1_class_obstruction. Do not create a fourth "
                "Juggler energy attack.",
                "Record the energy gap. Do not enlarge the Juggler census.",
                "symbolic predecessor construction",
                "regular-preimage lemma or a splitting pair for reachability of 1",
                "Two predecessor states indistinguishable by the proposed quotient.",
                novelty=NoveltyRisk.MEDIUM,
                scope=ImplementationScope.MEDIUM,
                confidence=Confidence.MEDIUM,
                reason="Phase-9 backup after a Juggler energy stop",
            ),
            _proposal(
                2,
                "odd_odd_symbolic_composition",
                "the paired local lemmas remain the Juggler green loot",
                "Keep odd-even and odd-odd two-step laws.",
                "Do not register parity_drift_block.",
                "restricted symbolic composition",
                "unchanged local branch inequalities",
                "A domain element violating either proved two-step inequality.",
                novelty=NoveltyRisk.LOW,
                scope=ImplementationScope.SMALL,
                confidence=Confidence.HIGH,
                reason="energy failure does not retract the two-step lemmas",
            ),
            _proposal(
                3,
                "odd_even_symbolic_composition",
                "odd-even two-step decrease remains gated",
                "Keep odd_even_two_step_decrease gated. Do not thaw DEFAULT_ATTACK_ORDER.",
                "Do not raise composition depth to chase frequencies.",
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
            "updated from Juggler parity-drift Phase-12 falsifier; not executed",
            "parity_drift_block is not registered",
            "do not invent a fourth Juggler energy attack",
        )
    return AttackProposalDossier(
        proposals=items,
        campaign_id=TARGET,
        notes=notes,
    )


def phase12_payload(
    samples: tuple[DriftSample, ...],
    *,
    lean_proved: bool,
) -> dict[str, Any]:
    outcomes = tuple(evaluate_candidate(item, samples) for item in ranked_candidates())
    classification, loot, reason = classify(outcomes, lean_proved=lean_proved)
    dossier = updated_proposals(classification)
    block = next(item for item in outcomes if item.name == "oooee_conditional_contraction")
    if block.survived and lean_proved:
        lean_status = "PROVED"
    elif block.survived:
        lean_status = "FORMALIZATION_READY"
    elif block.unobserved:
        lean_status = "NOT_YET_FORMALIZATION_READY"
    else:
        lean_status = "FORMALIZATION_BLOCKED"
    one_step = [item for item in samples if item.depth == 1]
    oooee = [item for item in samples if item.word == WORD_OOOEE]
    ee = [item for item in samples if item.word == WORD_EE]
    payload: dict[str, Any] = {
        "engine_control_version": ENGINE_CONTROL_VERSION,
        "source_engine": "v2.3",
        "experimental_status": "PHASE_12_JUGGLER_PARITY_DRIFT_FALSIFIER",
        "experiment_name": EXPERIMENT_NAME,
        "target": TARGET,
        "max_composition_depth": MAX_DEPTH,
        "gated": True,
        "energy_definition": "conceptual E(n)=log log n; odd +log(3/2), even -log 2",
        "exact_surrogate": (
            "T^k(n)<n for block contraction; T(n)^2<=n^3 (odd) and T(n)^2<=n (even) "
            "for one-step increments. No floating-point verdicts."
        ),
        "energy_exactly_formalizable": True,
        "candidate_statements": [item.as_dict() for item in outcomes],
        "candidates": [item.as_dict() for item in outcomes],
        "domains": {
            "one_step": "odd n>=3 or even n>=2",
            "oooee": "n>=2 with branch word OOOEE",
            "shortest_negative": f"n>=2 with branch word {shortest_negative_word()}",
            "exceptional": "n=1",
        },
        "parity_words": {
            "pre_ranked": list(PRE_RANKED_WORDS),
            "candidate_2": WORD_OOOEE,
            "candidate_3": shortest_negative_word(),
            "no_arbitrary_search": True,
        },
        "idealized_drifts": pre_rank_table(),
        "thresholds": {
            "one_step_odd": 3,
            "one_step_even": 2,
            "oooee": 2,
            "justification": "n>=2 is the exact obstruction n^5<=1 in the OOOEE power chain; n=1 is the odd fixed point; odd expansion uses the existing n>=3 lemma",
            "not_chosen_to_kill_counterexamples": True,
        },
        "frozen_samples": [item.as_dict() for item in samples],
        "sample_counts": {
            "one_step": len(one_step),
            "oooee": len(oooee),
            "ee": len(ee),
        },
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
            if item.failure_mechanism
        ],
        "exceptional_state": {
            "state": 1,
            "role": "exceptional terminal odd fixed point",
            "reason": "log-log energy is undefined/awkward at 1; T(1)=1. Not a termination theorem.",
            "not_termination_theorem": True,
        },
        "anti_overclaim": {
            "global_termination": False,
            "global_divergence": False,
            "parity_frequency_theorem": False,
            "level_c_out_of_scope": True,
            "scope": "LOCAL_BRANCH_LAW",
            "one_step_is_new_loot": False,
            "ee_is_new_loot": False,
        },
        "lean_status": lean_status,
        "loot_status": loot,
        "attack_proposal_update": dossier.as_dict(),
        "classification": classification.value,
        "decision": classification.value,
        "decision_reason": reason,
        "green_loot": loot,
        "mathematical_status": "NEW_STRUCTURAL_LEMMA" if loot == "PARITY_DRIFT_GREEN_LOOT" else "none",
        "global_consequence": "LOCAL_BRANCH_LAW",
        "laboratory_decision": "PROMOTE" if classification is DriftClass.PARITY_DRIFT_GREEN_LOOT else "PARK",
        "top3_update": dossier.as_dict(),
        "existing_lemmas": {
            "odd_even": f"{LEAN_MODULE}.{LEAN_OE}",
            "odd_odd": f"{LEAN_MODULE}.{LEAN_OO}",
            "oooee": f"{LEAN_MODULE}.{LEAN_OOOEE}",
        },
    }
    return payload


def render_phase12_markdown(payload: Mapping[str, Any]) -> str:
    lines = [
        "# Juggler parity-drift Phase-12 falsifier",
        "",
        "Status: **PHASE_12_JUGGLER_PARITY_DRIFT_FALSIFIER**",
        "",
        "This is not a termination attack, not a divergence theorem, and not a",
        "parity-frequency theorem. Depth is at most `k=5`. Fixed parity words only.",
        "The exact surrogate is `T^k(n)<n` or the floor-power inequalities, never a",
        "floating-point log-log comparison.",
        "",
        "## Branch budget",
        "",
        "```text",
        "Mathematical target     Can fixed parity blocks be certified as contractive",
        "                        for an exact log-log energy surrogate?",
        "Novelty hypothesis      Mixed odd/even blocks may contract even though odd",
        "                        steps expand, via additive log-log costs.",
        "Falsifier               A realizing frozen OOOEE state with T^5(n)>=n, or",
        "                        a one-step power-bound failure.",
        "Existing machinery      FloorPower, two k=2 lemmas, WINDOW+orbit 13.",
        "Maximum Phase-12 scope  Three pre-ranked words/bounds, depth<=5.",
        "Promotion criterion     Exact non-definitional block inequality with Lean path.",
        "Stop criterion          arbitrary words, k>5, frequency theorem, new energy family.",
        "```",
        "",
        "## Metadata",
        "",
        f"- engine_control_version: `{payload['engine_control_version']}`",
        f"- source_engine: `{payload['source_engine']}`",
        f"- experimental_status: `{payload['experimental_status']}`",
        f"- target: `{payload['target']}`",
        f"- max depth: `{payload['max_composition_depth']}`",
        f"- classification: **{payload['classification']}**",
        f"- lean: `{payload['lean_status']}`",
        f"- loot: `{payload['loot_status']}`",
        f"- decision reason: {payload['decision_reason']}",
        "",
        "Candidate 1 survival is a definitional restatement, not new loot.",
        "Candidate 3 (`EE`) is the shortest negative-drift word; even contraction",
        "is not new loot. `DEFAULT_ATTACK_ORDER` is unchanged.",
        "",
        "## Energy model",
        "",
        f"- Conceptual: {payload['energy_definition']}",
        f"- Exact surrogate: {payload['exact_surrogate']}",
        "",
        "## Pre-ranked words",
        "",
        "| Word | Length | Exact negative | Allowed | C3 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in payload.get("idealized_drifts") or []:
        lines.append(
            f"| `{row['word']}` | {row['length']} | `{row['exact_negative']}` | "
            f"`{row['depth_allowed']}` | `{row['selected_as_candidate_3']}` |"
        )
    lines.extend(
        [
            "",
            f"Thresholds: odd one-step `n>=3`, even/OOOEE `n>=2`. "
            f"{payload['thresholds']['justification']}",
            "",
            "## Exceptional state",
            "",
            payload["exceptional_state"]["reason"],
            "",
        ]
    )
    for item in payload.get("candidates") or []:
        status = "survived" if item["survived"] else ("unobserved" if item.get("unobserved") else "failed")
        lines.extend(
            [
                f"## Candidate {item['rank']}: `{item['name']}` ({status})",
                "",
                f"- Statement: {item['exact_statement']}",
                f"- Domain: {item['relevant_domain']}",
                f"- Word: `{item['parity_word']}`",
                f"- Idealized drift: {item['idealized_drift']}",
                f"- Motivation: {item['motivation']}",
                f"- Checked: {item['checked']}",
                f"- Loot-eligible: `{item['loot_eligible']}`",
                "",
            ]
        )
        if not item["survived"]:
            cex = item.get("counterexample") or {}
            if cex:
                lines.append(
                    f"- Counterexample: `{cex.get('source')}` word `{cex.get('word')}` "
                    f"path `{cex.get('path')}`"
                )
            lines.append(f"- Failure class: `{item['failure_class']}`")
            lines.append(f"- Mechanism: {item['failure_mechanism']}")
            lines.append("")
        elif item["failure_class"] == "DEFINITIONAL_RESTATEMENT":
            lines.append(f"- Note: {item['failure_mechanism']}")
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
            "Scope: `LOCAL_BRANCH_LAW`. Not `GLOBAL_TERMINATION`. Level C is out of scope.",
            "`parity_drift_block` is not a production attack.",
            "",
            "## Best next question",
            "",
            "Do not infer that every orbit contains OOOEE. That is Level C.",
            "The raised proposal is `parity_drift_block` as a target-specific",
            "conditional-block attack, not a halt theorem.",
            "",
        ]
    )
    return "\n".join(lines)
