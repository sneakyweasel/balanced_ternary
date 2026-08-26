"""Pipeline metadata for Lychrel / Reverse-and-Add. Not an attack."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from research.lychrel_dynamics.attack_families import (
    CANDIDATE_ATTACK_FAMILIES,
    CANDIDATE_ATTACK_FAMILY_IDS,
)

REQUIRED_SCHEMA_FIELDS: tuple[str, ...] = (
    "problem_id",
    "title",
    "domain",
    "status",
    "difficulty",
    "source",
    "source_url",
    "statement",
    "canonical_parameters",
    "known_instances",
    "novelty_risk",
    "recommended_attack_families",
    "research_notes",
)

LITERATURE_IDS: tuple[str, ...] = (
    "oeis-A023108",
    "oeis-A006960",
    "oeis-A056964",
    "oeis-A077408",
    "oeis-A060382",
    "prosper-veigneau-2001-palindromic-reversal",
    "weisstein-196-algorithm",
)

LEAN_PROSPECTIVE_OBJECTS: tuple[str, ...] = (
    "DigitBase",
    "Digits",
    "Reverse",
    "ReverseAdd",
    "Palindrome",
    "Trajectory",
    "ResidualState",
    "Transition",
    "Reachable",
    "PalReach",
)


@dataclass(frozen=True)
class KnownInstance:
    """One named seed. Computational evidence is not a proof."""

    instance_id: str
    base: int
    seed: int
    role: str
    evidence_kind: str
    mathematical_status: str
    conjectural_status: str
    source: str
    notes: str


@dataclass(frozen=True)
class NoveltyReviewItem:
    """A search that must finish before selection promotes to execution."""

    item_id: str
    status: str
    complete: bool
    notes: str


@dataclass(frozen=True)
class QualitativeScore:
    """Prioritization labels. Not a calibrated probability or milli-score."""

    new_math_probability: str
    frontier_strength: str
    lean_path: str
    cost: str
    novelty_risk: str
    intended_consequence: str


@dataclass(frozen=True)
class PipelineProblemRecord:
    """Machine-readable pipeline entry. Laboratory status stays on ProblemDefinition."""

    problem_id: str
    title: str
    domain: tuple[str, ...]
    status: str
    difficulty: str
    source: str
    source_url: str
    statement: str
    canonical_parameters: Mapping[str, Any]
    known_instances: tuple[KnownInstance, ...]
    novelty_risk: str
    recommended_attack_families: tuple[str, ...]
    research_notes: str
    attack_style: str
    primary_representation: str
    qualitative_score: QualitativeScore
    novelty_review_required: bool
    novelty_review_complete: bool
    novelty_review_checklist: tuple[NoveltyReviewItem, ...]
    lean_prospective_objects: tuple[str, ...]
    literature_ids: tuple[str, ...]
    attack_executed: bool
    distinct_from: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "problem_id": self.problem_id,
            "title": self.title,
            "domain": list(self.domain),
            "status": self.status,
            "difficulty": self.difficulty,
            "source": self.source,
            "source_url": self.source_url,
            "statement": self.statement,
            "canonical_parameters": dict(self.canonical_parameters),
            "known_instances": [
                {
                    "instance_id": item.instance_id,
                    "base": item.base,
                    "seed": item.seed,
                    "role": item.role,
                    "evidence_kind": item.evidence_kind,
                    "mathematical_status": item.mathematical_status,
                    "conjectural_status": item.conjectural_status,
                    "source": item.source,
                    "notes": item.notes,
                }
                for item in self.known_instances
            ],
            "novelty_risk": self.novelty_risk,
            "recommended_attack_families": list(self.recommended_attack_families),
            "research_notes": self.research_notes,
            "attack_style": self.attack_style,
            "primary_representation": self.primary_representation,
            "qualitative_score": {
                "new_math_probability": self.qualitative_score.new_math_probability,
                "frontier_strength": self.qualitative_score.frontier_strength,
                "lean_path": self.qualitative_score.lean_path,
                "cost": self.qualitative_score.cost,
                "novelty_risk": self.qualitative_score.novelty_risk,
                "intended_consequence": self.qualitative_score.intended_consequence,
            },
            "novelty_review_required": self.novelty_review_required,
            "novelty_review_complete": self.novelty_review_complete,
            "novelty_review_checklist": [
                {
                    "item_id": item.item_id,
                    "status": item.status,
                    "complete": item.complete,
                    "notes": item.notes,
                }
                for item in self.novelty_review_checklist
            ],
            "lean_prospective_objects": list(self.lean_prospective_objects),
            "literature_ids": list(self.literature_ids),
            "attack_executed": self.attack_executed,
            "distinct_from": self.distinct_from,
        }


RECORD = PipelineProblemRecord(
    problem_id="lychrel_dynamics",
    title="Lychrel / Reverse-and-Add dynamics",
    domain=("discrete_dynamics", "automata", "number_theory", "symbolic_dynamics"),
    status="open",
    difficulty="high",
    source="oeis-A023108",
    source_url="https://oeis.org/A023108",
    statement=(
        "Let b>=2 be an integer and rev_b the reversal of the ordinary "
        "unsigned base-b digits of a positive integer. Write "
        "R_b(n)=n+rev_b(n). For the canonical instance b=10, does there "
        "exist n>0 such that the trajectory n, R_b(n), R_b^2(n), ... never "
        "reaches a palindrome? Secondary instance b=3. Optional signed or "
        "balanced digits are an exploratory representation, not a transfer "
        "theorem. Results in one base do not transfer automatically to another."
    ),
    canonical_parameters={
        "base": "integer b >= 2",
        "digit_representation": (
            "unsigned_base_b",
            "optional_signed_balanced_exploratory",
        ),
        "map": "R_b(n) = n + rev_b(n)",
        "canonical_base": 10,
        "secondary_base": 3,
        "balanced_ternary_branch": "exploratory",
        "properties": (
            "trajectory",
            "finite_prefix_reachability",
            "palindrome_reachability",
            "candidate_non_termination",
            "residual_state_equivalence",
            "transducer_representation",
        ),
    },
    known_instances=(
        KnownInstance(
            instance_id="decimal_196",
            base=10,
            seed=196,
            role="smallest_documented_candidate",
            evidence_kind="known_computational_evidence",
            mathematical_status="not_a_proof",
            conjectural_status="literature_candidate",
            source="oeis-A023108",
            notes=(
                "OEIS A023108 lists 196 as a positive integer that apparently "
                "never results in a palindrome under A056964. The sequence "
                "conjectures 196 is the smallest such seed. This is not a "
                "theorem that 196 is Lychrel. Distinct from reverse_and_add_base3 "
                "seed 196, where W(196)=196 and n+W(n) reaches 0."
            ),
        ),
        KnownInstance(
            instance_id="base3_103",
            base=3,
            seed=103,
            role="historically_noted_base3_candidate",
            evidence_kind="known_computational_evidence",
            mathematical_status="not_a_proof",
            conjectural_status="literature_candidate",
            source="oeis-A077408",
            notes=(
                "OEIS A077408: 103 is conjectured to be the smallest number "
                "whose base-3 Reverse-and-Add trajectory does not lead to a "
                "palindrome. The same entry states that the palindrome-free "
                "method used for some base-2 and base-4 trajectories is not "
                "applicable here. Contextual metadata only."
            ),
        ),
    ),
    novelty_risk="very_high",
    recommended_attack_families=CANDIDATE_ATTACK_FAMILY_IDS,
    research_notes=(
        "Model Reverse-and-Add as digits -> reversal -> digitwise addition -> "
        "carry propagation -> new digits. Investigate whether the global map "
        "admits (finite control, finite/local residual) transitions compatible "
        "with residual equivalence, origin-live words, path separation, "
        "quantified future separation, closure, forbidden-word discovery, "
        "exact arithmetic invariants, and Lean-certified transition lemmas. "
        "known computational evidence != mathematical proof != conjectural "
        "status. Applies to 196, 103, and any future observation. Do not "
        "reopen reverse_and_add_base3. Do not execute attacks in this phase. "
        "Novelty review is mandatory before promotion from selection to "
        "execution. Qualitative score labels are not a numeric "
        "ExpectedResearchValue and do not auto-outrank lower-novelty-risk "
        "targets."
    ),
    attack_style="structural",
    primary_representation="digit_transducer",
    qualitative_score=QualitativeScore(
        new_math_probability="high",
        frontier_strength="high",
        lean_path="high",
        cost="medium_high",
        novelty_risk="very_high",
        intended_consequence=(
            "Serious research candidate, but must not automatically outrank "
            "targets with substantially lower novelty risk. Labels are not "
            "converted into fake numerical precision."
        ),
    ),
    novelty_review_required=True,
    novelty_review_complete=False,
    novelty_review_checklist=(
        NoveltyReviewItem(
            item_id="exact_proposed_invariant_or_transducer",
            status="required",
            complete=False,
            notes="Search before proposing any concrete invariant or transducer as new.",
        ),
        NoveltyReviewItem(
            item_id="prior_fst_automata_formulations",
            status="required",
            complete=False,
            notes="Search for prior finite-state / automata formulations of Reverse-and-Add.",
        ),
        NoveltyReviewItem(
            item_id="generalized_base_lychrel",
            status="partial",
            complete=False,
            notes=(
                "OEIS A060382 and A077408 recorded. Brockhaus base-2/base-4 "
                "palindrome-free method is cited as not applicable to 103. "
                "Further search still required before an attack."
            ),
        ),
        NoveltyReviewItem(
            item_id="ternary_and_balanced_digit_formulations",
            status="partial",
            complete=False,
            notes=(
                "Closed reverse_and_add_base3 is related (canonical BT reverse "
                "plus add) but is not unsigned base-3 Lychrel. Further search "
                "required."
            ),
        ),
        NoveltyReviewItem(
            item_id="prior_art_ids_on_metadata",
            status="required",
            complete=True,
            notes="Literature ids recorded on this record and in literature/.",
        ),
        NoveltyReviewItem(
            item_id="computational_patterns_are_not_new_math",
            status="standing_rule",
            complete=True,
            notes="Do not present rediscovery of a known computational pattern as new mathematics.",
        ),
    ),
    lean_prospective_objects=LEAN_PROSPECTIVE_OBJECTS,
    literature_ids=LITERATURE_IDS,
    attack_executed=False,
    distinct_from="reverse_and_add_base3",
)

PHASE_REPORT = {
    "problem_registered": True,
    "attack_executed": False,
    "default_attack_order_changed": False,
    "new_attack_family_registered": True,
    "novelty_review_required": True,
}

assert all(hasattr(RECORD, field) for field in REQUIRED_SCHEMA_FIELDS)
assert RECORD.recommended_attack_families == CANDIDATE_ATTACK_FAMILY_IDS
assert len(CANDIDATE_ATTACK_FAMILIES) == 5
assert RECORD.attack_executed is False
assert RECORD.novelty_review_required is True
assert RECORD.novelty_review_complete is False
