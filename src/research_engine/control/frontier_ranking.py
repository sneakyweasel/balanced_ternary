"""Phase-9 mathematical frontier re-ranking. Not an attack.

Ranks existing (target, attack-family) pairs from frozen v2.3/v2.4
evidence. Does not execute a winner, thaw DEFAULT_ATTACK_ORDER, open a
board, or reopen reverse-and-add.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from research_engine.control.proposals import assert_not_executable
from research_engine.control.types import (
    ENGINE_CONTROL_VERSION,
    AttackProposal,
    AttackProposalDossier,
    CloseTag,
    Confidence,
    ImplementationScope,
    MathematicalStatus,
    NoveltyRisk,
    REPLAY_V22_TARGETS,
    V2_3_CAMPAIGN_ORDER,
)

EXPERIMENT_NAME = "phase9_frontier_ranking"
EXPERIMENTAL_STATUS = "PHASE_9_FRONTIER_RERANKING"
SOURCE_ENGINE = "v2.3"
REVERSE_ADD_TARGET = "reverse_and_add_base3"

FORBIDDEN_ATTACKS: frozenset[str] = frozenset(
    {
        "ranking_function_synthesis",
        "symbolic_nonlinear_composition",
        "concat_word_composition",
        "digit_structure_ranking",
        "odd_even_two_step_decrease",
        "odd_even_symbolic_composition",
        "restricted_symbolic_composition",
    }
)

MACHINERY_GRAVITY_ATTACKS: frozenset[str] = frozenset(
    {
        "ranking_function_synthesis",
        "symbolic_nonlinear_composition",
        "concat_word_composition",
        "digit_structure_ranking",
    }
)

REQUIRED_CANDIDATE_FIELDS: tuple[str, ...] = (
    "target_id",
    "attack_family",
    "mathematical_frontier",
    "observed_trigger",
    "supporting_campaigns",
    "why_current_machinery_is_already_close",
    "expected_mathematical_yield",
    "strongest_existing_counterexample",
    "cheapest_falsifier",
    "lean_path",
    "novelty_risk",
    "implementation_scope",
    "target_reuse_value",
    "proposal_confidence",
)

_RISK_WEIGHT = {
    NoveltyRisk.LOW: 1,
    NoveltyRisk.MEDIUM: 2,
    NoveltyRisk.HIGH: 3,
}
_SCOPE_WEIGHT = {
    ImplementationScope.SMALL: 1,
    ImplementationScope.MEDIUM: 2,
    ImplementationScope.LARGE: 3,
}
_PROXIMITY_WEIGHT = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}
_FRONTIER_WEIGHT = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}
_LEAN_WEIGHT = {"CLEAR": 3, "PLAUSIBLE": 2, "BLOCKED": 1, "UNKNOWN": 1}
_LOOT_WEIGHT = {"BLUE_POSSIBLE": 4, "GREEN": 3, "GREY": 1}


class ExpectedLoot(str, Enum):
    GREY = "GREY"
    GREEN = "GREEN"
    BLUE_POSSIBLE = "BLUE_POSSIBLE"


class LeanPath(str, Enum):
    CLEAR = "CLEAR"
    PLAUSIBLE = "PLAUSIBLE"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"


class FrontierDecision(str, Enum):
    SELECTED_FRONTIER = "SELECTED_FRONTIER"


def qualitative_score_milli(
    *,
    expected_loot: ExpectedLoot,
    frontier_strength: str,
    lean_path: LeanPath,
    implementation_scope: ImplementationScope,
    novelty_risk: NoveltyRisk,
) -> int:
    """Prioritization aid. Not a calibrated probability.

    S = P(new math) * frontier strength * formalization / (cost * novelty).
    """

    numerator = (
        _LOOT_WEIGHT[expected_loot.value]
        * _FRONTIER_WEIGHT[frontier_strength]
        * _LEAN_WEIGHT[lean_path.value]
    )
    denominator = _SCOPE_WEIGHT[implementation_scope] * _RISK_WEIGHT[novelty_risk]
    return (1000 * numerator) // denominator


@dataclass(frozen=True)
class FrontierCandidate:
    target_id: str
    attack_name: str
    attack_family: str
    mathematical_frontier: str
    observed_trigger: str
    supporting_campaigns: tuple[str, ...]
    why_current_machinery_is_already_close: str
    expected_mathematical_yield: str
    strongest_existing_counterexample: str
    cheapest_falsifier: str
    lean_path: LeanPath
    novelty_risk: NoveltyRisk
    implementation_scope: ImplementationScope
    target_reuse_value: str
    proposal_confidence: Confidence
    expected_loot: ExpectedLoot
    frontier_strength: str
    machinery_proximity: str
    why_now: str
    recommendation: str
    close_tag: str
    mathematical_status: str
    replay: bool = False
    replay_attractive: bool = False
    excluded: bool = False
    exclusion_reason: str = ""

    @property
    def pair_id(self) -> str:
        return f"{self.target_id}::{self.attack_name}"

    @property
    def score_milli(self) -> int:
        if self.excluded:
            return 0
        return qualitative_score_milli(
            expected_loot=self.expected_loot,
            frontier_strength=self.frontier_strength,
            lean_path=self.lean_path,
            implementation_scope=self.implementation_scope,
            novelty_risk=self.novelty_risk,
        )

    def sort_key(self) -> tuple[int, int, int, int, str, str]:
        return (
            self.score_milli,
            -_RISK_WEIGHT[self.novelty_risk],
            -_SCOPE_WEIGHT[self.implementation_scope],
            _PROXIMITY_WEIGHT[self.machinery_proximity],
            self.target_id,
            self.attack_name,
        )

    def as_proposal(self, rank: int) -> AttackProposal:
        assert_not_executable(self.attack_name)
        return AttackProposal(
            rank=rank,
            attack_name=self.attack_name,
            trigger=self.observed_trigger,
            mathematical_target=self.mathematical_frontier,
            mechanism=self.why_current_machinery_is_already_close,
            required_capability=self.attack_family,
            expected_yield=self.expected_mathematical_yield,
            falsifier=self.cheapest_falsifier,
            novelty_risk=self.novelty_risk,
            implementation_scope=self.implementation_scope,
            confidence=self.proposal_confidence,
            novelty_risk_reason=self.why_now,
        )

    def as_dict(self, *, rank: int | None = None) -> dict[str, Any]:
        payload = {
            "target_id": self.target_id,
            "attack_name": self.attack_name,
            "attack_family": self.attack_family,
            "mathematical_frontier": self.mathematical_frontier,
            "observed_trigger": self.observed_trigger,
            "supporting_campaigns": list(self.supporting_campaigns),
            "why_current_machinery_is_already_close": self.why_current_machinery_is_already_close,
            "expected_mathematical_yield": self.expected_mathematical_yield,
            "strongest_existing_counterexample": self.strongest_existing_counterexample,
            "cheapest_falsifier": self.cheapest_falsifier,
            "lean_path": self.lean_path.value,
            "novelty_risk": self.novelty_risk.value,
            "implementation_scope": self.implementation_scope.value,
            "target_reuse_value": self.target_reuse_value,
            "proposal_confidence": self.proposal_confidence.value,
            "expected_loot": self.expected_loot.value,
            "frontier_strength": self.frontier_strength,
            "machinery_proximity": self.machinery_proximity,
            "why_now": self.why_now,
            "recommendation": self.recommendation,
            "close_tag": self.close_tag,
            "mathematical_status": self.mathematical_status,
            "replay": self.replay,
            "replay_attractive": self.replay_attractive,
            "excluded": self.excluded,
            "exclusion_reason": self.exclusion_reason,
            "score_milli": self.score_milli,
            "pair_id": self.pair_id,
        }
        if rank is not None:
            payload["rank"] = rank
            payload["proposal"] = self.as_proposal(rank).as_dict()
        return payload


def _candidate(**kwargs: Any) -> FrontierCandidate:
    return FrontierCandidate(**kwargs)


def frozen_exclusions() -> tuple[dict[str, str], ...]:
    return (
        {
            "target_id": REVERSE_ADD_TARGET,
            "reason": (
                "Phase-8 CLOSED the reverse-add branch: involution summaries "
                "are generic arithmetic or counterexample-killed. Reopening "
                "would be machinery gravity."
            ),
        },
        {
            "target_id": "weak_collatz_floor_5x4_rplus",
            "reason": (
                "CLOSE_REPARAMETERIZATION of the 4/3 SLC language; a new "
                "restricted-composition pass would upgrade a known representation."
            ),
        },
        {
            "target_id": "skolem_order2_known_zero",
            "reason": (
                "v2.2 calibration replay of a known zero; historical reproduction "
                "without a new attack hypothesis."
            ),
        },
        {
            "target_id": "cyclic_tag_bit",
            "reason": (
                "CLOSE_SPEC_MISMATCH and RANKING_IMPLAUSIBLE; length nondecrease "
                "is the production, and a native word engine is machinery gravity."
            ),
        },
        {
            "target_id": "juggler_sequence",
            "attack_name": "odd_even_two_step_decrease",
            "reason": (
                "Already converted to a gated attack and Lean-proved as "
                "floorPower_odd_even_two_step_lt. Do not rerun the exhausted lemma."
            ),
        },
        {
            "target_id": "home_prime_49",
            "attack_name": "concat_word_composition",
            "reason": (
                "Dossier forbids a concatenation attack; a general digit-language "
                "engine is machinery gravity. Phase-2 two-step length already failed."
            ),
        },
        {
            "target_id": "*",
            "attack_name": "ranking_function_synthesis",
            "reason": "Unrestricted ranking synthesizer is machinery gravity.",
        },
        {
            "target_id": "*",
            "attack_name": "symbolic_nonlinear_composition",
            "reason": "Generic symbolic algebra engine is machinery gravity.",
        },
    )


def frozen_candidates() -> tuple[FrontierCandidate, ...]:
    """Evidence-backed pool. Frozen before ranking. No fourth family invented."""

    return (
        _candidate(
            target_id="juggler_sequence",
            attack_name="odd_odd_branch_composition",
            attack_family="restricted_symbolic_composition",
            mathematical_frontier=(
                "Unexplained nonlinear branch interaction on the complementary "
                "odd-to-odd floor-power cylinder: odd-even T^2(n)<n is proved, "
                "but odd-to-odd steps such as 3->5 remain outside the lemma and "
                "are not a halt theorem."
            ),
            observed_trigger=(
                "Phase-1/2 next_proposal odd_odd_branch_composition; 9 frozen "
                "odd-to-odd transitions; Phase-0 growth at 3->5."
            ),
            supporting_campaigns=(
                "juggler_sequence",
                "ranking_phase0",
                "ranking_phase1",
                "symbolic_composition_phase2",
                "symbolic_composition_phase3",
            ),
            why_current_machinery_is_already_close=(
                "The Juggler trajectory already produced NEW_STRUCTURAL_LEMMA "
                "by bounded survivor -> exact two-step inequality -> Lean. "
                "FloorPower.lean exists. The complementary cylinder is named "
                "and sampled; the next statement does not require a new engine."
            ),
            expected_mathematical_yield=(
                "NEW_STRUCTURAL_LEMMA on the odd-odd cylinder, or a closed "
                "k=2 obstruction. Not a halt theorem on positive integers."
            ),
            strongest_existing_counterexample="3 -> 5 (odd floor-power growth)",
            cheapest_falsifier=(
                "On the frozen odd-to-odd pairs, test any k=2 size law "
                "T^2(n)<n (fails at 3->5->11) or a single exact parity-cylinder "
                "predicate; do not enlarge depth to hide 3->5."
            ),
            lean_path=LeanPath.PLAUSIBLE,
            novelty_risk=NoveltyRisk.MEDIUM,
            implementation_scope=ImplementationScope.MEDIUM,
            target_reuse_value=(
                "Reuse FloorPowerSpec, gated restricted-composition matching, "
                "and existing Lean sqrt identities. Do not generalize "
                "odd_even_two_step_decrease automatically."
            ),
            proposal_confidence=Confidence.HIGH,
            expected_loot=ExpectedLoot.GREEN,
            frontier_strength="HIGH",
            machinery_proximity="HIGH",
            why_now=(
                "v2.4's only green-loot trajectory left an explicit complementary "
                "branch unimplemented. Reverse-add showed the same idea does not "
                "transfer; the remaining Juggler cylinder is still local, exact, "
                "and Lean-adjacent."
            ),
            recommendation=(
                "Run a k=2 odd-odd composition falsifier on the existing frozen "
                "odd-to-odd transitions; do not claim termination and do not "
                "generalize the gated odd-even primitive."
            ),
            close_tag=CloseTag.CLOSE_FINITE_CENSUS.value,
            mathematical_status=MathematicalStatus.FRONTIER.value,
        ),
        _candidate(
            target_id="mx_plus_r_7x1_class_obstruction",
            attack_name="basin_preimage_grammar",
            attack_family="basin_preimage_reasoning",
            mathematical_frontier=(
                "Local image-class invariant without a basin consequence: after "
                "one step, odd images lie in <2> inside (Z/7Z)*, but complementary "
                "classes still reach 1. Which odd positives reach 1 remains open."
            ),
            observed_trigger=(
                "CLOSE_FALSE_OBSTRUCTION: T(73)=1 and T(299593)=1 kill "
                "class-as-basin; recurring engine limitation image class != basin."
            ),
            supporting_campaigns=(
                "mx_plus_r_7x1_class_obstruction",
                "v2_3_top3",
                "engine_retrospective",
            ),
            why_current_machinery_is_already_close=(
                "Forward image recovery and Lean counterexamples already exist "
                "in MxPlusR.lean. The missing step is a finite predecessor "
                "quotient tested against those known hits, not another image census."
            ),
            expected_mathematical_yield=(
                "Regular-preimage lemma or a splitting pair for reachability of 1. "
                "Not a solution of 7x+1."
            ),
            strongest_existing_counterexample="T(73)=1 and T(299593)=1",
            cheapest_falsifier=(
                "Propose one finite residue/valuation quotient of predecessors of "
                "1 and exhibit two states in the same class with different "
                "reachability of 1 on the stored window."
            ),
            lean_path=LeanPath.PLAUSIBLE,
            novelty_risk=NoveltyRisk.MEDIUM,
            implementation_scope=ImplementationScope.MEDIUM,
            target_reuse_value=(
                "Reuse MxPlusRSpec, recovered image class, and existing "
                "counterexample identities. Different family from the refuted "
                "class-obstruction lead."
            ),
            proposal_confidence=Confidence.MEDIUM,
            expected_loot=ExpectedLoot.GREY,
            frontier_strength="MEDIUM",
            machinery_proximity="HIGH",
            why_now=(
                "The v2.3 retrospective named image-as-basin as a recurring "
                "failure. This target already has Lean-certified counterexamples, "
                "so a basin/preimage falsifier can run without a new map engine."
            ),
            recommendation=(
                "Test one predecessor quotient against the known hits 73 and "
                "299593 versus a stored non-hit such as seed 3; do not rerun "
                "the false class obstruction."
            ),
            close_tag=CloseTag.CLOSE_FALSE_OBSTRUCTION.value,
            mathematical_status=MathematicalStatus.STRONG_NEGATIVE.value,
        ),
        _candidate(
            target_id="matthews_prize_mod3_avoider",
            attack_name="basin_preimage_grammar",
            attack_family="basin_preimage_reasoning",
            mathematical_frontier=(
                "Whether every integer orbit that stays in {1,2} mod 3 for all "
                "time enters -1 or {-2,-4}. Finite-window preimages and the "
                "fact that packet seeds are not avoiders do not decide that."
            ),
            observed_trigger=(
                "CLOSE_FALSE_OBSTRUCTION: {1,2} mod 3 is not a basin; packet "
                "seeds are not avoiders; -28 and -10 are strict preimages of "
                "the 2-cycle."
            ),
            supporting_campaigns=(
                "matthews_prize_mod3_avoider",
                "v2_3_top3",
                "engine_retrospective",
            ),
            why_current_machinery_is_already_close=(
                "Three affine branches, cycles, and expanding 0 mod 3 are already "
                "Lean-certified in MatthewsMod3.lean. The missing object is a "
                "predecessor grammar for genuine avoiders, not another window census."
            ),
            expected_mathematical_yield=(
                "A sound finite preimage quotient for the named cycles, or a "
                "splitting pair. Not a Matthews-prize solution."
            ),
            strongest_existing_counterexample=(
                "packet seeds are not avoiders; -28 and -10 are strict preimages "
                "of {-2,-4}"
            ),
            cheapest_falsifier=(
                "Propose one residue quotient of bounded preimages of {-1} union "
                "{-2,-4} and split two states with identical class but different "
                "avoider behavior."
            ),
            lean_path=LeanPath.PLAUSIBLE,
            novelty_risk=NoveltyRisk.MEDIUM,
            implementation_scope=ImplementationScope.MEDIUM,
            target_reuse_value=(
                "Reuse the three-branch spec and existing cycle identities. "
                "Different family from the refuted avoider-as-basin lead."
            ),
            proposal_confidence=Confidence.MEDIUM,
            expected_loot=ExpectedLoot.GREY,
            frontier_strength="MEDIUM",
            machinery_proximity="MEDIUM",
            why_now=(
                "Same recurring image/basin limitation as 7x+1, with a second "
                "Lean module and named cycles already in hand. Cheaper than a "
                "Skolem vanishing procedure."
            ),
            recommendation=(
                "Test one bounded preimage quotient for the known cycles; do not "
                "claim the Matthews prize and do not rerun the false avoider obstruction."
            ),
            close_tag=CloseTag.CLOSE_FALSE_OBSTRUCTION.value,
            mathematical_status=MathematicalStatus.STRONG_NEGATIVE.value,
        ),
        _candidate(
            target_id="juggler_sequence",
            attack_name="basin_preimage_grammar",
            attack_family="basin_preimage_reasoning",
            mathematical_frontier=(
                "The basin of 1 under the floor-power map is unresolved. Seed-13 "
                "closure and the odd-even two-step lemma do not imply that every "
                "positive integer reaches 1."
            ),
            observed_trigger=(
                "CLOSE_FINITE_CENSUS: four-step orbit of 13 is not a map theorem; "
                "StrategyPlanner selected unimplemented global_inductive."
            ),
            supporting_campaigns=("juggler_sequence", "symbolic_composition_phase3"),
            why_current_machinery_is_already_close=(
                "Predecessors of 1 can be probed on the frozen window, but the "
                "open claim is global reachability. Restricted composition already "
                "covers a local cylinder; basin reasoning here is the halt conjecture."
            ),
            expected_mathematical_yield="Regular-preimage lemma for 1, or a splitting pair. Not Juggler totality.",
            strongest_existing_counterexample="Every positive n decreases is REFUTED at n=3",
            cheapest_falsifier=(
                "A proposed predecessor quotient of 1 that identifies 3 with a "
                "state that reaches 1 on the frozen window."
            ),
            lean_path=LeanPath.PLAUSIBLE,
            novelty_risk=NoveltyRisk.HIGH,
            implementation_scope=ImplementationScope.MEDIUM,
            target_reuse_value="Reuse FloorPowerSpec; do not upgrade seed-13 to a halt theorem.",
            proposal_confidence=Confidence.LOW,
            expected_loot=ExpectedLoot.GREY,
            frontier_strength="HIGH",
            machinery_proximity="LOW",
            why_now=(
                "The halt question remains, but it is strictly more ambitious than "
                "the named odd-odd cylinder and has no cheap exact statement yet."
            ),
            recommendation=(
                "Do not select the Juggler basin as the next experiment while the "
                "odd-odd cylinder is still unfalsified."
            ),
            close_tag=CloseTag.CLOSE_FINITE_CENSUS.value,
            mathematical_status=MathematicalStatus.FRONTIER.value,
        ),
        _candidate(
            target_id="companion_shift_order6_zero_class",
            attack_name="global_vanishing_congruence",
            attack_family="symbolic_matrix_word_congruence",
            mathematical_frontier=(
                "Unimplemented global-inductive / matrix-word mechanism: whether "
                "the first coordinate vanishes on Z. A length-65 zero-free prefix "
                "and skipped 25^6 census are not a vanishing congruence."
            ),
            observed_trigger=(
                "CLOSE_SKIP_BOUNDARY: vector_affine / matrix_word_invariant skipped "
                "by adapter cell budget; every small modulus hits a 0 residue."
            ),
            supporting_campaigns=(
                "companion_shift_order6_zero_class",
                "v2_3_top3",
            ),
            why_current_machinery_is_already_close=(
                "Companion window and prefix identities are Lean-certified. A "
                "symbolic gcd/resultant congruence that does not enumerate 25^6 "
                "is the named Top-3 gap. Unbounded matrix-word search is excluded."
            ),
            expected_mathematical_yield=(
                "Exact vanishing congruence independent of the skipped census, "
                "or a proof that the skipped attack cannot supply one."
            ),
            strongest_existing_counterexample=(
                "every modulus in 2..32 hits a 0 residue on the prefix; a prefix "
                "gap is not modular exclusion"
            ),
            cheapest_falsifier=(
                "One candidate lattice/gcd constraint on vanishing indices, "
                "killed by a prefix that hits 0 in every class of that constraint."
            ),
            lean_path=LeanPath.UNKNOWN,
            novelty_risk=NoveltyRisk.HIGH,
            implementation_scope=ImplementationScope.LARGE,
            target_reuse_value=(
                "Reuse CompanionShift identities. Do not un-skip matrix-word or "
                "start a Skolem decision procedure."
            ),
            proposal_confidence=Confidence.MEDIUM,
            expected_loot=ExpectedLoot.GREY,
            frontier_strength="HIGH",
            machinery_proximity="LOW",
            why_now=(
                "Genuine FRONTIER at the skip boundary, but the falsifier is "
                "expensive relative to Juggler odd-odd and 7x+1 preimage."
            ),
            recommendation=(
                "Keep as a later backup: one symbolic congruence, not a 25^6 census."
            ),
            close_tag=CloseTag.CLOSE_SKIP_BOUNDARY.value,
            mathematical_status=MathematicalStatus.FRONTIER.value,
        ),
        _candidate(
            target_id="skolem_order5_unconditional",
            attack_name="global_vanishing_congruence",
            attack_family="symbolic_matrix_word_congruence",
            mathematical_frontier=(
                "Unconditional order-5 vanishing remains open. Same skip pair as "
                "dimension 6; a finite prefix is not a Skolem theorem."
            ),
            observed_trigger="CLOSE_SKIP_BOUNDARY: same skip pair as companion order 6",
            supporting_campaigns=("skolem_order5_unconditional", "companion_shift_order6_zero_class"),
            why_current_machinery_is_already_close=(
                "Less recovered structure than the order-6 companion window. "
                "The missing capability is the same symbolic congruence, not a "
                "new census."
            ),
            expected_mathematical_yield="Exact vanishing congruence or a closed skip-boundary lemma.",
            strongest_existing_counterexample="skipped matrix-word / cell-budget census",
            cheapest_falsifier=(
                "One candidate congruence class on the stored order-5 prefix that "
                "is already hit by a zero residue."
            ),
            lean_path=LeanPath.UNKNOWN,
            novelty_risk=NoveltyRisk.HIGH,
            implementation_scope=ImplementationScope.LARGE,
            target_reuse_value="Do not start a Skolem procedure. Rank below the order-6 companion.",
            proposal_confidence=Confidence.LOW,
            expected_loot=ExpectedLoot.GREY,
            frontier_strength="HIGH",
            machinery_proximity="LOW",
            why_now="Same skip-boundary FRONTIER as companion, with weaker local identities.",
            recommendation="Do not select order-5 vanishing before the cheaper Juggler/7x+1 falsifiers.",
            close_tag=CloseTag.CLOSE_SKIP_BOUNDARY.value,
            mathematical_status=MathematicalStatus.FRONTIER.value,
        ),
        _candidate(
            target_id="switching_affine_z2_origin",
            attack_name="proof_guided_invariant_refinement",
            attack_family="proof_guided_hypothesis_refinement",
            mathematical_frontier=(
                "Local invariant without a global basin consequence: N0^2 origin "
                "reachability is classified, while termination on Z^2 remains open."
            ),
            observed_trigger=(
                "v2.2 recovered two affine pieces and two_path_nonneg_never_origin; "
                "v2.4 replay added close-tag metadata, not a new theorem."
            ),
            supporting_campaigns=("switching_affine_z2_origin", "replay_v22_switching_affine_z2_origin"),
            why_current_machinery_is_already_close=(
                "TwoPathZ2.lean already certifies the nonnegative orthant. A "
                "refined signed-seed invariant would reuse those identities, but "
                "the replay did not expose a new attack hypothesis."
            ),
            expected_mathematical_yield="Sharpened signed-seed invariant or a counterexample on Z^2.",
            strongest_existing_counterexample=(
                "signed seeds can reach the origin in one step; (3,2) grows on the window"
            ),
            cheapest_falsifier=(
                "One candidate inductive predicate on Z^2 that holds on N0^2 but "
                "fails at a stored signed seed."
            ),
            lean_path=LeanPath.PLAUSIBLE,
            novelty_risk=NoveltyRisk.MEDIUM,
            implementation_scope=ImplementationScope.MEDIUM,
            target_reuse_value="Replay is eligible, but historically unattractive: reproduction plus taxonomy.",
            proposal_confidence=Confidence.LOW,
            expected_loot=ExpectedLoot.GREY,
            frontier_strength="LOW",
            machinery_proximity="MEDIUM",
            why_now=(
                "v2.2 already exposed the structure; v2.3/v2.4 merely reproduced it. "
                "Do not select a replay to increase campaign count."
            ),
            recommendation="Do not replay switching-affine merely to relabel the orthant theorem.",
            close_tag=CloseTag.CLOSE_KNOWN.value,
            mathematical_status=MathematicalStatus.UNRESOLVED.value,
            replay=True,
            replay_attractive=False,
        ),
        _candidate(
            target_id="home_prime_49",
            attack_name="basin_preimage_grammar",
            attack_family="basin_preimage_reasoning",
            mathematical_frontier=(
                "Exact finite prefix of seed 49 without an infinite primality "
                "statement. Ranking and two-step concatenation composition failed."
            ),
            observed_trigger=(
                "CLOSE_FINITE_CENSUS; Phase-1 piecewise ranking failed at 4->22; "
                "Phase-2 composition failed to yield a length law."
            ),
            supporting_campaigns=(
                "home_prime_49",
                "ranking_phase0",
                "ranking_phase1",
                "symbolic_composition_phase2",
            ),
            why_current_machinery_is_already_close=(
                "Predecessors of primes under factor-concatenation would be a "
                "basin question, but current machinery has no cheap exact "
                "statement after concat composition failed. A digit-language "
                "engine is excluded."
            ),
            expected_mathematical_yield="Splitting pair for prime-preimages, not primality of seed 49.",
            strongest_existing_counterexample="4 -> 22 concat length growth; 10 -> 25 factor_count nondecrease",
            cheapest_falsifier=(
                "One proposed prime-preimage quotient that identifies 4->22 with "
                "a stored prime halt."
            ),
            lean_path=LeanPath.BLOCKED,
            novelty_risk=NoveltyRisk.HIGH,
            implementation_scope=ImplementationScope.LARGE,
            target_reuse_value="FactorConcat.lean identities exist; concatenation attacks are forbidden.",
            proposal_confidence=Confidence.LOW,
            expected_loot=ExpectedLoot.GREY,
            frontier_strength="MEDIUM",
            machinery_proximity="LOW",
            why_now=(
                "Eligible as basin/preimage, but expected yield is weak after "
                "two composition/ranking failures and the concatenation ban."
            ),
            recommendation="Do not open a home-prime digit engine; keep this pair below the Top-3.",
            close_tag=CloseTag.CLOSE_FINITE_CENSUS.value,
            mathematical_status=MathematicalStatus.FRONTIER.value,
        ),
    )


def eligible_candidates(
    items: tuple[FrontierCandidate, ...] | None = None,
) -> tuple[FrontierCandidate, ...]:
    pool = items if items is not None else frozen_candidates()
    return tuple(
        item
        for item in pool
        if not item.excluded
        and item.target_id != REVERSE_ADD_TARGET
        and item.attack_name not in FORBIDDEN_ATTACKS
    )


def rank_candidates(
    items: tuple[FrontierCandidate, ...] | None = None,
) -> tuple[FrontierCandidate, ...]:
    return tuple(sorted(eligible_candidates(items), key=lambda item: item.sort_key(), reverse=True))


def top3(items: tuple[FrontierCandidate, ...] | None = None) -> tuple[FrontierCandidate, ...]:
    ranked = rank_candidates(items)
    if len(ranked) < 3:
        raise ValueError("Phase-9 ranking requires at least three eligible candidates")
    return ranked[:3]


def selected_frontier(items: tuple[FrontierCandidate, ...] | None = None) -> FrontierCandidate:
    return top3(items)[0]


def as_proposal_dossier(items: tuple[FrontierCandidate, ...] | None = None) -> AttackProposalDossier:
    chosen = top3(items)
    proposals = tuple(item.as_proposal(rank) for rank, item in enumerate(chosen, start=1))
    for proposal in proposals:
        assert_not_executable(proposal.attack_name)
    return AttackProposalDossier(
        campaign_id=EXPERIMENT_NAME,
        proposals=proposals,
        notes=(
            "Phase-9 selection only; not executed",
            "unit is (target, attack), so attack_name may repeat across targets",
            f"targets: {', '.join(item.target_id for item in chosen)}",
            "reverse_and_add_base3 excluded",
            "DEFAULT_ATTACK_ORDER unchanged",
        ),
    )


def grey_loot_records(items: tuple[FrontierCandidate, ...] | None = None) -> tuple[dict[str, Any], ...]:
    chosen = top3(items)
    winner = chosen[0]
    return (
        {
            "id": "phase9:loot:ranking",
            "kind": "Potential research question",
            "statement": (
                f"Selected frontier is ({winner.target_id}, {winner.attack_name}) "
                "by expected new mathematics per unit of attack effort."
            ),
            "experiment_id": EXPERIMENT_NAME,
            "target": winner.target_id,
            "reusable_lesson": (
                "Rank (target, attack) pairs from accumulated evidence; do not "
                "keep inventing scalar attacks on a CLOSED branch."
            ),
            "possible_transfer_targets": [item.target_id for item in chosen],
            "status": "ACTIVE",
            "payload": {
                "why_ranked": [item.why_now for item in chosen],
                "supporting_campaigns": [list(item.supporting_campaigns) for item in chosen],
                "prior_art": (
                    "Juggler odd-even lemma is NEW_STRUCTURAL_LEMMA; reverse-add "
                    "scalars are generic arithmetic or refuted; 7x+1 and Matthews "
                    "image-as-basin obstructions are KNOWN false leads."
                ),
                "reverse_add_excluded": True,
                "repeated_missing_capability": (
                    "restricted symbolic composition on a complementary branch; "
                    "symbolic predecessor construction for image-vs-basin"
                ),
                "cheapest_falsifier": winner.cheapest_falsifier,
            },
        },
        {
            "id": "phase9:loot:reverse_add_closed",
            "kind": "Useful negative result",
            "statement": (
                "Reverse-and-add is excluded from Phase-9: Phase-8 closed the "
                "compressed involution falsifier; further refinement is machinery gravity."
            ),
            "experiment_id": EXPERIMENT_NAME,
            "target": REVERSE_ADD_TARGET,
            "reusable_lesson": "A CLOSED branch with many stored observations is not a reason to reopen it.",
            "possible_transfer_targets": (),
            "status": "SATURATED",
            "payload": {"reason": frozen_exclusions()[0]["reason"]},
        },
    )


def phase9_payload(items: tuple[FrontierCandidate, ...] | None = None) -> dict[str, Any]:
    pool = frozen_candidates() if items is None else items
    ranked = rank_candidates(pool)
    chosen = ranked[:3]
    winner = chosen[0]
    dossier = as_proposal_dossier(pool)
    payload: dict[str, Any] = {
        "engine_control_version": ENGINE_CONTROL_VERSION,
        "source_engine": SOURCE_ENGINE,
        "experimental_status": EXPERIMENTAL_STATUS,
        "experiment_name": EXPERIMENT_NAME,
        "gated": True,
        "executed": False,
        "candidate_pool": [item.as_dict() for item in pool],
        "excluded_targets": list(frozen_exclusions()),
        "scoring_basis": {
            "formula": (
                "S = P(new mathematics) * frontier_strength * formalization_value "
                "/ (implementation_cost * novelty_risk)"
            ),
            "not_calibrated": True,
            "weights": {
                "expected_loot": dict(_LOOT_WEIGHT),
                "frontier_strength": dict(_FRONTIER_WEIGHT),
                "lean_path": dict(_LEAN_WEIGHT),
                "implementation_scope": {
                    "SMALL": _SCOPE_WEIGHT[ImplementationScope.SMALL],
                    "MEDIUM": _SCOPE_WEIGHT[ImplementationScope.MEDIUM],
                    "LARGE": _SCOPE_WEIGHT[ImplementationScope.LARGE],
                },
                "novelty_risk": {
                    "LOW": _RISK_WEIGHT[NoveltyRisk.LOW],
                    "MEDIUM": _RISK_WEIGHT[NoveltyRisk.MEDIUM],
                    "HIGH": _RISK_WEIGHT[NoveltyRisk.HIGH],
                },
            },
            "tie_break": (
                "score desc, novelty risk asc, scope asc, machinery proximity desc, "
                "target_id asc, attack_name asc"
            ),
            "objective": "new mathematics per unit of attack effort",
        },
        "ranked_candidates": [item.as_dict(rank=index) for index, item in enumerate(ranked, start=1)],
        "selected_frontier": {
            "label": "SELECTED_FRONTIER",
            **winner.as_dict(rank=1),
        },
        "backup_frontier_1": {
            "label": "BACKUP_FRONTIER_1",
            **chosen[1].as_dict(rank=2),
        },
        "backup_frontier_2": {
            "label": "BACKUP_FRONTIER_2",
            **chosen[2].as_dict(rank=3),
        },
        "supporting_evidence": {
            "v2_3_campaign_order": list(V2_3_CAMPAIGN_ORDER),
            "replay_v22_targets": list(REPLAY_V22_TARGETS),
            "green_loot_model": "bounded survivor -> symbolic explanation -> Lean theorem",
            "green_loot_example": "floorPower_odd_even_two_step_lt",
            "reverse_add_status": "CLOSED after Phase 8",
            "recurring_missing_capabilities": (
                "restricted symbolic composition on complementary branches",
                "symbolic predecessor construction",
                "proof-guided hypothesis refinement",
            ),
            "grey_loot": list(grey_loot_records(pool)),
        },
        "cheapest_falsifier": winner.cheapest_falsifier,
        "top3_attack_update": dossier.as_dict(),
        "decision": FrontierDecision.SELECTED_FRONTIER.value,
        "decision_reason": (
            f"{winner.target_id} x {winner.attack_name}: mathematically interesting, "
            "cheap to falsify, exact, Lean-adjacent, and not exhausted."
        ),
        "laboratory_decision": "PROMOTE",
        "green_loot": "NO_NEW_LOOT",
        "global_consequence": "NONE",
        "default_attack_order_unchanged": True,
        "no_new_board": True,
        "no_new_attack_registration": True,
        "reverse_add_reopened": False,
    }
    for field in (
        "candidate_pool",
        "excluded_targets",
        "scoring_basis",
        "ranked_candidates",
        "selected_frontier",
        "supporting_evidence",
        "cheapest_falsifier",
        "decision",
    ):
        if field not in payload:
            raise ValueError(f"missing required Phase-9 field {field}")
    return payload


def render_phase9_markdown(payload: Mapping[str, Any]) -> str:
    selected = payload["selected_frontier"]
    backup1 = payload["backup_frontier_1"]
    backup2 = payload["backup_frontier_2"]
    ranked = (selected, backup1, backup2)

    def _row(item: Mapping[str, Any]) -> str:
        frontier = str(item["mathematical_frontier"]).split(":")[0]
        return (
            f"| {item['rank']} | `{item['target_id']}` | `{item['attack_name']}` | "
            f"{frontier} | {item['cheapest_falsifier']} | {item['expected_loot']} | "
            f"{item['implementation_scope']} | {item['lean_path']} |"
        )

    def _block(title: str, item: Mapping[str, Any]) -> list[str]:
        return [
            f"## {title}",
            "",
            f"- Rank: `{item['rank']}`",
            f"- Target: `{item['target_id']}`",
            f"- Attack: `{item['attack_name']}`",
            f"- Mathematical frontier: {item['mathematical_frontier']}",
            f"- Why now: {item['why_now']}",
            f"- Cheapest falsifier: {item['cheapest_falsifier']}",
            f"- Expected loot: `{item['expected_loot']}`",
            f"- Novelty risk: `{item['novelty_risk']}`",
            f"- Implementation scope: `{item['implementation_scope']}`",
            f"- Lean path: `{item['lean_path']}`",
            f"- Recommendation: {item['recommendation']}",
            "",
        ]

    lines = [
        "# Phase-9 mathematical frontier re-ranking",
        "",
        "Status: **PHASE_9_FRONTIER_RERANKING**",
        "",
        "This is a target × attack selection experiment. It does not implement a",
        "new attack, does not modify `DEFAULT_ATTACK_ORDER`, does not open a new",
        "board, and does not reopen reverse-and-add.",
        "",
        "## Branch budget",
        "",
        "```text",
        "Mathematical target     Among remaining frontiers, which (target, attack)",
        "                        pair has the highest expected new mathematics per",
        "                        unit of attack effort?",
        "Novelty hypothesis      Accumulated v2.4 evidence can rank existing pairs",
        "                        without inventing a new attack family.",
        "Falsifier               Reverse-add reopened; flood order thawed; a new",
        "                        target created; the winner executed in this phase.",
        "Existing machinery      ResearchMemory, GreyLoot, Top-3 dossiers, Phase 0-8",
        "                        records, v2.2 replays, CLOSE/math-status taxonomy.",
        "Maximum Phase-9 scope   Frozen candidate pool, qualitative score, Top-3,",
        "                        artifacts, tests. No execution.",
        "Promotion criterion     A selected frontier with a cheap falsifier and",
        "                        visible evidence, not a new campaign.",
        "Stop criterion          New attack family; reverse-add reopening; ranking",
        "                        synthesizer; digit-language engine.",
        "```",
        "",
        "## Metadata",
        "",
        f"- engine_control_version: `{payload['engine_control_version']}`",
        f"- source_engine: `{payload['source_engine']}`",
        f"- experimental_status: `{payload['experimental_status']}`",
        f"- decision: **{payload['decision']}**",
        f"- executed: `{payload['executed']}`",
        f"- green loot: `{payload['green_loot']}`",
        "",
        "Reverse-and-add is excluded. `DEFAULT_ATTACK_ORDER` is unchanged.",
        "No production attack is registered.",
        "",
        "## Scoring basis",
        "",
        payload["scoring_basis"]["formula"],
        "",
        "The score is a prioritization aid, not a calibrated probability.",
        "Objective: new mathematics per unit of attack effort.",
        "",
        "## Comparison table",
        "",
        "| Rank | Target | Attack | Frontier | Cheapest falsifier | Expected loot | Scope | Lean |",
        "| ---- | ------ | ------ | -------- | ------------------ | ------------- | ----- | ---- |",
        _row(selected),
        _row(backup1),
        _row(backup2),
        "",
    ]
    for title, item in (
        ("Rank 1 — SELECTED_FRONTIER", selected),
        ("Rank 2 — BACKUP_FRONTIER_1", backup1),
        ("Rank 3 — BACKUP_FRONTIER_2", backup2),
    ):
        lines.extend(_block(title, item))
    lines.extend(
        [
            "## Exclusions",
            "",
        ]
    )
    for item in payload["excluded_targets"]:
        attack = item.get("attack_name")
        label = item["target_id"] if not attack else f"{item['target_id']} × {attack}"
        lines.append(f"- `{label}`: {item['reason']}")
    lines.extend(
        [
            "",
            "## Decision",
            "",
            "**SELECTED_FRONTIER**",
            "",
            payload["decision_reason"],
            "",
            "Do not execute the winner in this phase.",
            "",
            "## Best next question",
            "",
            ranked[0]["recommendation"],
            "",
        ]
    )
    return "\n".join(lines)
