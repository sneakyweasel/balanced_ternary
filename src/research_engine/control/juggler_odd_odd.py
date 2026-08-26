"""Phase-10 Juggler odd-odd k=2 composition falsifier. Not an attack.

Complementary cylinder D_OO = {odd x : T(x) odd, T^2 defined}.
Does not generalize odd_even_two_step_decrease. Depth frozen at 2.
Not a termination or divergence theorem.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import isqrt
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

TARGET = "juggler_sequence"
ATTACK = "odd_odd_branch_composition"
DEPTH = 2
EXPERIMENT_NAME = "juggler_odd_odd_phase10"
LEAN_MODULE = "Problems.Engine.FloorPower"
LEAN_ODD_EVEN = "floorPower_odd_even_two_step_lt"
LEAN_ODD_ODD = "floorPower_odd_odd_two_step_gt"

DOMAIN_OO = "D_OO = {odd x : T(x) odd and T^2(x) defined}"
DOMAIN_OE = "D_OE = {odd x : T(x) even and T^2(x) defined}"


class OddOddClass(str, Enum):
    JUGGLER_ODD_ODD_GREEN_LOOT = "JUGGLER_ODD_ODD_GREEN_LOOT"
    JUGGLER_ODD_ODD_PROMISING = "JUGGLER_ODD_ODD_PROMISING"
    JUGGLER_ODD_ODD_NEEDS_RICHER_STRUCTURE = "JUGGLER_ODD_ODD_NEEDS_RICHER_STRUCTURE"
    JUGGLER_ODD_ODD_REFUTED = "JUGGLER_ODD_ODD_REFUTED"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"


def floor_power(n: int) -> int:
    """Exact even/odd floor-power successor. Stdlib isqrt only."""

    if n < 1:
        raise ValueError("floor_power is defined on positive integers")
    if n % 2 == 0:
        return isqrt(n)
    return isqrt(n * n * n)


def odd_even_two_step(n: int) -> int | None:
    """T^2 on D_OE. Positive control; unchanged from the existing lemma."""

    if n < 2 or n % 2 == 0:
        return None
    mid = isqrt(n * n * n)
    if mid % 2 != 0:
        return None
    return isqrt(mid)


def odd_odd_two_step(n: int) -> int | None:
    """T^2 on D_OO. Depth is exactly 2."""

    if n < 1 or n % 2 == 0:
        return None
    mid = isqrt(n * n * n)
    if mid % 2 == 0:
        return None
    return isqrt(mid * mid * mid)


def in_d_oo(n: int) -> bool:
    return odd_odd_two_step(n) is not None


def in_d_oe(n: int) -> bool:
    return odd_even_two_step(n) is not None


@dataclass(frozen=True)
class OddOddSample:
    source: int
    mid: int
    image: int
    note: str = "juggler odd-odd T^2"

    def as_dict(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "mid": self.mid,
            "image": self.image,
            "note": self.note,
            "source_odd": self.source % 2 == 1,
            "mid_odd": self.mid % 2 == 1,
            "image_odd": self.image % 2 == 1,
            "composition_depth": DEPTH,
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
    arithmetic_class: str
    holds: Callable[[OddOddSample], bool]
    in_domain: Callable[[OddOddSample], bool]


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
    counterexample: OddOddSample | None
    failure_mechanism: str
    failure_class: str
    arithmetic_class: str
    assessed_arithmetic: str
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
            "arithmetic_class": self.arithmetic_class,
            "assessed_arithmetic": self.assessed_arithmetic,
            "checked": self.checked,
        }


def ranked_candidates() -> tuple[RankedCandidate, ...]:
    """Exactly three candidates, ranked before execution. Do not extend after failure."""

    return (
        RankedCandidate(
            rank=1,
            name="strict_two_step_growth",
            exact_statement="T^2(x) > x on D_OO",
            motivation=(
                "The odd branch is expanding. The smallest dual of the proved "
                "odd-even descent is strict two-step growth on the complementary cylinder."
            ),
            relevant_domain=DOMAIN_OO,
            expected_yield="exact two-step growth law, or a threshold/equality obstruction",
            cheapest_falsifier="the first frozen D_OO seed with T^2(x) <= x",
            failure_class="THRESHOLD_FAILURE",
            arithmetic_class="BRANCH_SPECIFIC",
            in_domain=lambda item: item.source % 2 == 1 and item.mid % 2 == 1,
            holds=lambda item: item.image > item.source,
        ),
        RankedCandidate(
            rank=2,
            name="thresholded_two_step_growth",
            exact_statement=(
                "For n in D_OO with n >= 3, T^2(n) > n. The threshold 3 is the "
                "exact comparison (n+1)^2 <= n^3, not a fitted constant."
            ),
            motivation=(
                "For n>=3, isqrt(n^3) >= n+1. If T(n) is odd then T is nondecreasing "
                "on that image, so two odd steps grow. Dual of T^2 < n on D_OE."
            ),
            relevant_domain="D_OO intersect {n >= 3}",
            expected_yield="exact complementary inequality with a derived threshold",
            cheapest_falsifier="the first frozen D_OO seed n>=3 with T^2(n) <= n",
            failure_class="GROWTH_NOT_UNIFORM",
            arithmetic_class="FLOOR_POWER_BRANCH_SPECIFIC",
            in_domain=lambda item: item.source >= 3 and item.source % 2 == 1 and item.mid % 2 == 1,
            holds=lambda item: item.image > item.source,
        ),
        RankedCandidate(
            rank=3,
            name="odd_cylinder_preservation",
            exact_statement="x in D_OO implies T^2(x) is odd",
            motivation=(
                "Parity is the floor-power branch bit. Two successive odd steps "
                "might remain in the odd cylinder. Modulus 2 is the branch mechanism, "
                "not a residue sweep."
            ),
            relevant_domain=DOMAIN_OO,
            expected_yield="exact T^2 parity / cylinder-invariance law",
            cheapest_falsifier="the first frozen D_OO seed whose T^2 is even",
            failure_class="PARITY_DOMAIN_LEAK",
            arithmetic_class="BRANCH_SPECIFIC",
            in_domain=lambda item: item.source % 2 == 1 and item.mid % 2 == 1,
            holds=lambda item: item.image % 2 == 1,
        ),
    )


def evaluate_candidate(
    candidate: RankedCandidate,
    samples: tuple[OddOddSample, ...],
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
            arithmetic_class=candidate.arithmetic_class,
            assessed_arithmetic="N/A",
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
            arithmetic_class=candidate.arithmetic_class,
            assessed_arithmetic="N/A",
            checked=checked,
        )
    assessed = "FLOOR_POWER_BRANCH_SPECIFIC"
    if candidate.name == "thresholded_two_step_growth":
        assessed = "FLOOR_POWER_BRANCH_SPECIFIC"
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
        arithmetic_class=candidate.arithmetic_class,
        assessed_arithmetic=assessed,
        checked=checked,
    )


def _mechanism(candidate: RankedCandidate, item: OddOddSample) -> str:
    if candidate.name == "strict_two_step_growth":
        return (
            f"Strict growth fails at {item.source}->{item.mid}->{item.image}: "
            f"T^2({item.source})={item.image} is not > {item.source}. Fixed point or threshold."
        )
    if candidate.name == "thresholded_two_step_growth":
        return (
            f"Thresholded growth fails at {item.source}->{item.mid}->{item.image}: "
            f"T^2={item.image} <= {item.source}."
        )
    return (
        f"Odd-cylinder leaks at {item.source}->{item.mid}->{item.image}: "
        f"T^2({item.source})={item.image} is even, so T^2 leaves D_OO."
    )


def classify(outcomes: tuple[CandidateOutcome, ...]) -> tuple[OddOddClass, str]:
    if all(item.checked < 1 for item in outcomes):
        return (
            OddOddClass.INSUFFICIENT_DATA,
            "the frozen artifacts do not contain odd-odd two-step samples",
        )
    by_name = {item.name: item for item in outcomes}
    growth = by_name.get("thresholded_two_step_growth")
    strict = by_name.get("strict_two_step_growth")
    preserve = by_name.get("odd_cylinder_preservation")
    if (
        growth is not None
        and growth.survived
        and strict is not None
        and not strict.survived
        and preserve is not None
        and not preserve.survived
    ):
        return (
            OddOddClass.JUGGLER_ODD_ODD_GREEN_LOOT,
            "thresholded T^2 > n on D_OO, n>=3 is the dual of odd-even descent; "
            "strict growth fails at the fixed point 1; T^2 is not odd-cylinder invariant",
        )
    if growth is not None and growth.survived:
        return (
            OddOddClass.JUGGLER_ODD_ODD_PROMISING,
            "thresholded two-step growth survived the frozen D_OO sample",
        )
    survivors = [item for item in outcomes if item.survived]
    if survivors:
        return (
            OddOddClass.JUGGLER_ODD_ODD_NEEDS_RICHER_STRUCTURE,
            "simple k=2 laws are mixed; failures identify branch leakage or a threshold",
        )
    return (
        OddOddClass.JUGGLER_ODD_ODD_REFUTED,
        "all three odd-odd k=2 candidates failed on the frozen cylinder",
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


def updated_proposals(classification: OddOddClass) -> AttackProposalDossier:
    if classification is OddOddClass.JUGGLER_ODD_ODD_GREEN_LOOT:
        items = (
            _proposal(
                1,
                "odd_odd_symbolic_composition",
                "exact T^2 > n on D_OO for n>=3",
                "Package the dual odd-odd two-step growth lemma. Do not claim divergence.",
                "Keep k=2. Do not generalize odd_even_two_step_decrease automatically.",
                "restricted symbolic composition",
                "Lean-certified local branch law T^2(n)>n on D_OO, n>=3",
                "An n>=3 in D_OO with T^2(n)<=n.",
                novelty=NoveltyRisk.LOW,
                scope=ImplementationScope.SMALL,
                confidence=Confidence.HIGH,
                reason="the inequality is the exact dual of the proved odd-even descent",
            ),
            _proposal(
                2,
                "basin_preimage_grammar",
                "odd-odd growth is local; basin of 1 remains open",
                "Characterize predecessors of 1 under floor-power. Not a halt attack.",
                "Do not use T^2>n as a Lyapunov function.",
                "symbolic predecessor construction",
                "regular-preimage lemma or a splitting pair for reachability of 1",
                "Two predecessor states indistinguishable by the proposed quotient.",
                novelty=NoveltyRisk.MEDIUM,
                scope=ImplementationScope.MEDIUM,
                confidence=Confidence.MEDIUM,
                reason="Phase-9 backup; image/basin is independent of the local growth law",
            ),
            _proposal(
                3,
                "proof_guided_hypothesis_refinement",
                "odd-even and odd-odd two-step lemmas are both local",
                "Ask whether mixed-parity words have an exact k=2 law without raising depth.",
                "If k>2 is required, PARK. Do not manufacture a survivor by depth.",
                "proof-guided hypothesis refinement",
                "a mixed-parity identity at depth 2, or a stop at richer structure",
                "A mixed-parity pair on which every k=2 size law fails.",
                novelty=NoveltyRisk.MEDIUM,
                scope=ImplementationScope.MEDIUM,
                confidence=Confidence.LOW,
                reason="cylinder leakage 5->11->36 already shows T^2 is not odd-invariant",
            ),
        )
        notes = (
            "updated from Juggler odd-odd Phase-10 falsifier; not executed",
            "odd_odd_symbolic_composition is proposed, not registered",
            "odd_even_two_step_decrease is unchanged",
            "global_consequence is LOCAL_BRANCH_LAW, not GLOBAL_TERMINATION",
        )
    else:
        items = (
            _proposal(
                1,
                "basin_preimage_grammar",
                "odd-odd k=2 did not yield a production Juggler attack",
                "Promote the Phase-9 backup: basin/preimage on 7x+1.",
                "Do not invent a fourth Juggler attack. Do not raise k.",
                "symbolic predecessor construction",
                "regular-preimage lemma or a splitting pair for reachability of 1",
                "Two predecessor states indistinguishable by the proposed quotient.",
                novelty=NoveltyRisk.MEDIUM,
                scope=ImplementationScope.MEDIUM,
                confidence=Confidence.MEDIUM,
                reason="Phase-9 backup frontier after a Juggler k=2 stop",
            ),
            _proposal(
                2,
                "odd_even_symbolic_composition",
                "the proved odd-even lemma remains the Juggler green loot",
                "Keep the existing gated odd-even primitive. Do not generalize it.",
                "odd_even_two_step_decrease stays gated and not in DEFAULT_ATTACK_ORDER.",
                "restricted symbolic composition",
                "unchanged odd-even two-step decrease",
                "An odd-even domain element with T^2(n)>=n.",
                novelty=NoveltyRisk.LOW,
                scope=ImplementationScope.SMALL,
                confidence=Confidence.HIGH,
                reason="floorPower_odd_even_two_step_lt is unchanged",
            ),
            _proposal(
                3,
                "basin_preimage_grammar",
                "Matthews mod-3 is the second Phase-9 backup",
                "If 7x+1 preimage is parked, use Matthews basin/preimage next.",
                "Do not reopen reverse-add. Do not raise Juggler depth.",
                "symbolic predecessor construction",
                "preimage quotient for the known Matthews cycles",
                "Two states with the same class and different avoider behavior.",
                novelty=NoveltyRisk.MEDIUM,
                scope=ImplementationScope.MEDIUM,
                confidence=Confidence.MEDIUM,
                reason="Phase-9 BACKUP_FRONTIER_2",
            ),
        )
        notes = (
            "updated from Juggler odd-odd Phase-10 falsifier; not executed",
            "odd_odd_branch_composition is not registered",
            "promote Phase-9 backup basin_preimage_grammar on 7x+1",
        )
    return AttackProposalDossier(
        proposals=items,
        campaign_id=TARGET,
        notes=notes,
    )


def anti_tautology_check(outcomes: tuple[CandidateOutcome, ...]) -> dict[str, Any]:
    growth = next((item for item in outcomes if item.name == "thresholded_two_step_growth"), None)
    return {
        "rejected_identities": [
            "T(x)=floor(x^(3/2)) for odd x",
            "T^2(x)=floor(floor(x^(3/2))^(3/2)) when T(x) is odd",
            "the successor is odd",
        ],
        "domains": [DOMAIN_OE, DOMAIN_OO],
        "not_investigated": "k>2",
        "candidate1_is_definitional": False,
        "candidate2_is_definitional": False,
        "candidate2_uses_second_step_parity": True,
        "candidate3_is_definitional": False,
        "global_termination_claimed": False,
        "global_divergence_claimed": False,
        "scope": "LOCAL_BRANCH_LAW",
        "reason": (
            "T^2(n)>n on D_OO, n>=3 uses the second-step odd parity to select the "
            "expanding formula, then the comparison (n+1)^2 <= n^3. It is not "
            "T=floor(n^(3/2)) written twice. T(n)>n for odd n>=3 holds on D_OE as "
            "well, but T^2>n does not: the even second step contracts."
        ),
        "growth_survived": None if growth is None else growth.survived,
    }


def phase10_payload(
    samples: tuple[OddOddSample, ...],
    oe_count: int,
    *,
    lean_proved: bool,
) -> dict[str, Any]:
    outcomes = tuple(evaluate_candidate(item, samples) for item in ranked_candidates())
    classification, reason = classify(outcomes)
    if lean_proved and classification is OddOddClass.JUGGLER_ODD_ODD_GREEN_LOOT:
        lean_status = "PROVED"
        mathematical_status = "NEW_STRUCTURAL_LEMMA"
        green = "JUGGLER_ODD_ODD_GREEN_LOOT"
    elif classification is OddOddClass.JUGGLER_ODD_ODD_GREEN_LOOT:
        lean_status = "FORMALIZATION_READY"
        mathematical_status = "NEW_STRUCTURAL_LEMMA"
        green = "NO_NEW_LOOT"
        classification = OddOddClass.JUGGLER_ODD_ODD_PROMISING
        reason = "thresholded growth survived with an exact derivation but is not Lean-proved"
    else:
        lean_status = "NOT_YET_FORMALIZATION_READY"
        mathematical_status = "none"
        green = "NO_NEW_LOOT"
    dossier = updated_proposals(classification)
    survivors = [item.as_dict() for item in outcomes if item.survived]
    counterexamples = [
        {
            "name": item.name,
            "rank": item.rank,
            "failure_class": item.failure_class,
            "counterexample": None if item.counterexample is None else item.counterexample.as_dict(),
        }
        for item in outcomes
        if not item.survived and item.counterexample is not None
    ]
    payload: dict[str, Any] = {
        "engine_control_version": ENGINE_CONTROL_VERSION,
        "source_engine": "v2.3",
        "experimental_status": "PHASE_10_JUGGLER_ODD_ODD_COMPOSITION_FALSIFIER",
        "experiment_name": EXPERIMENT_NAME,
        "target": TARGET,
        "attack": ATTACK,
        "composition_depth": DEPTH,
        "gated": True,
        "domains": {
            "D_OE": DOMAIN_OE,
            "D_OO": DOMAIN_OO,
            "positive_control": LEAN_ODD_EVEN,
            "odd_even_unchanged": True,
        },
        "candidates": [item.as_dict() for item in outcomes],
        "candidate_statements": [item.exact_statement for item in outcomes],
        "existing_samples": [item.as_dict() for item in samples],
        "existing_sample_count": len(samples),
        "odd_even_control_count": oe_count,
        "required_probe": {"source": 3, "mid": 5, "image": 11},
        "survivors": survivors,
        "first_counterexamples": counterexamples,
        "failure_mechanisms": [
            {"name": item.name, "class": item.failure_class, "text": item.failure_mechanism}
            for item in outcomes
            if not item.survived
        ],
        "anti_tautology_checks": anti_tautology_check(outcomes),
        "lean_status": lean_status,
        "lean_module": LEAN_MODULE,
        "lean_odd_even": f"{LEAN_MODULE}.{LEAN_ODD_EVEN}",
        "lean_odd_odd": f"{LEAN_MODULE}.{LEAN_ODD_ODD}",
        "mathematical_status": mathematical_status,
        "global_consequence": "LOCAL_BRANCH_LAW",
        "not_global_termination": True,
        "top3_update": dossier.as_dict(),
        "classification": classification.value,
        "decision": classification.value,
        "decision_reason": reason,
        "green_loot": green,
        "laboratory_decision": (
            "PROMOTE" if classification is OddOddClass.JUGGLER_ODD_ODD_GREEN_LOOT else "PARK"
        ),
    }
    return payload


def render_phase10_markdown(payload: Mapping[str, Any]) -> str:
    lines = [
        "# Juggler odd-odd composition Phase-10 falsifier",
        "",
        "Status: **PHASE_10_JUGGLER_ODD_ODD_COMPOSITION_FALSIFIER**",
        "",
        "This is not a termination attack, not a ranking synthesizer, and not a",
        "generalization of `odd_even_two_step_decrease`. Depth is frozen at `k=2`.",
        "It asks what exact two-step law, if any, replaces descent on the odd→odd",
        "floor-power cylinder.",
        "",
        "## Branch budget",
        "",
        "```text",
        "Mathematical target     On D_OO, does T^2 satisfy a simple exact k=2 law",
        "                        that is not definitional floor-power restatement?",
        "Novelty hypothesis      The complementary cylinder has a dual growth law",
        "                        to the proved odd-even descent.",
        "Falsifier               An exact two-step sample violating each frozen",
        "                        candidate, or a definitional restatement billed as loot.",
        "Existing machinery      FloorPowerSpec, WINDOW+orbit 13, FloorPower.lean.",
        "Maximum Phase-10 scope  Three pre-ranked k=2 candidates on frozen D_OO.",
        "Promotion criterion     Exact non-definitional branch law with Lean path.",
        "Stop criterion          k>2, ranking, census growth, generic engine,",
        "                        termination/divergence claim.",
        "```",
        "",
        "## Metadata",
        "",
        f"- engine_control_version: `{payload['engine_control_version']}`",
        f"- source_engine: `{payload['source_engine']}`",
        f"- experimental_status: `{payload['experimental_status']}`",
        f"- target: `{payload['target']}`",
        f"- attack: `{payload['attack']}`",
        f"- composition depth: `{payload['composition_depth']}`",
        f"- classification: **{payload['classification']}**",
        f"- lean: `{payload['lean_status']}`",
        f"- green loot: `{payload['green_loot']}`",
        f"- global consequence: `{payload['global_consequence']}`",
        f"- decision reason: {payload['decision_reason']}",
        "",
        "Candidate list frozen at three. `odd_even_two_step_decrease` is unchanged.",
        "`DEFAULT_ATTACK_ORDER` is unchanged. No production odd-odd attack.",
        "",
        "## Domains",
        "",
        f"- `{payload['domains']['D_OE']}`",
        f"- `{payload['domains']['D_OO']}`",
        f"- Positive control: `{payload['domains']['positive_control']}`",
        f"- Odd-even theorem unchanged: `{payload['domains']['odd_even_unchanged']}`",
        "",
        "## Anti-tautology",
        "",
        f"- Rejected identities: {payload['anti_tautology_checks']['rejected_identities']}",
        f"- Scope: `{payload['anti_tautology_checks']['scope']}`",
        f"- Not investigated: `{payload['anti_tautology_checks']['not_investigated']}`",
        f"- {payload['anti_tautology_checks']['reason']}",
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
                f"- Expected yield: {item['expected_yield']}",
                f"- Cheapest falsifier: {item['cheapest_falsifier']}",
                f"- Arithmetic class: `{item['arithmetic_class']}`",
                f"- Checked: {item['checked']}",
                "",
            ]
        )
        if item["survived"]:
            lines.append(f"- Assessed: `{item['assessed_arithmetic']}`")
            lines.append("")
        else:
            cex = item.get("counterexample") or {}
            lines.append(
                f"- Counterexample: `{cex.get('source')} -> {cex.get('mid')} -> {cex.get('image')}`"
            )
            lines.append(f"- Failure class: `{item['failure_class']}`")
            lines.append(f"- Mechanism: {item['failure_mechanism']}")
            lines.append("")
    samples = payload.get("existing_samples") or []
    lines.extend(["## Existing samples", ""])
    lines.append(
        f"- Frozen D_OO two-step samples: {payload.get('existing_sample_count', len(samples))}"
    )
    lines.append(f"- Frozen D_OE control samples: {payload.get('odd_even_control_count', '—')}")
    probe = payload.get("required_probe") or {}
    lines.append(
        f"- Required probe: `{probe.get('source')} -> {probe.get('mid')} -> {probe.get('image')}`"
    )
    for item in samples:
        lines.append(
            f"- `{item['source']} -> {item['mid']} -> {item['image']}` "
            f"(T^2 odd={item.get('image_odd')})"
        )
    lines.extend(
        [
            "",
            "## Decision",
            "",
            f"**{payload['decision']}**",
            "",
            payload["decision_reason"] + ".",
            "",
            f"Green loot: `{payload['green_loot']}`. Lean: `{payload['lean_status']}`.",
            "Scope: `LOCAL_BRANCH_LAW`. Not `GLOBAL_TERMINATION`.",
            "Not a production attack. `odd_even_two_step_decrease` is unchanged.",
            "Top-3 #1 is `odd_odd_symbolic_composition` (proposed, not registered).",
            "`odd_odd_branch_composition` is not in `DEFAULT_ATTACK_ORDER`.",
            "",
            "## Best next question",
            "",
        ]
    )
    if payload["classification"] == OddOddClass.JUGGLER_ODD_ODD_GREEN_LOOT.value:
        lines.append(
            "The odd-odd cylinder is not T^2-invariant (5->11->36). Does that leakage "
            "feed the existing odd-even lemma without raising composition depth?"
        )
    else:
        lines.append(
            "Promote the Phase-9 backup: basin_preimage_grammar on 7x+1. "
            "Do not invent a fourth Juggler attack."
        )
    lines.append("")
    return "\n".join(lines)
