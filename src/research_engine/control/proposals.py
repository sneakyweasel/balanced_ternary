"""Non-executing Top-3 attack proposal generator. Never registers attacks."""

from __future__ import annotations

from dataclasses import dataclass

from research_engine.control.types import (
    AttackProposal,
    AttackProposalDossier,
    Confidence,
    ControlSchemaError,
    FORBIDDEN_PROPOSAL_NAMES,
    ImplementationScope,
    NoveltyRisk,
    ProposalEvidence,
)
from research_engine.memory.types import MemoryExperiment
from research_engine.planner.orchestrator import DEFAULT_ATTACK_ORDER, DEFERRED_ATTACKS
from research_engine.strategy.capabilities import GLOBAL_INDUCTIVE_CHAIN

REGISTERED_ATTACKS: frozenset[str] = frozenset(DEFAULT_ATTACK_ORDER) | frozenset(DEFERRED_ATTACKS)

_SCOPE_WEIGHT = {
    ImplementationScope.SMALL: 1,
    ImplementationScope.MEDIUM: 2,
    ImplementationScope.LARGE: 3,
}
_NOVELTY_WEIGHT = {
    NoveltyRisk.LOW: 1,
    NoveltyRisk.MEDIUM: 2,
    NoveltyRisk.HIGH: 3,
}


@dataclass(frozen=True)
class _Candidate:
    attack_name: str
    trigger: str
    mathematical_target: str
    mechanism: str
    required_capability: str
    expected_yield: str
    falsifier: str
    novelty_risk: NoveltyRisk
    implementation_scope: ImplementationScope
    confidence: Confidence
    novelty_risk_reason: str
    yield_rank: int


def is_registered_attack(name: str) -> bool:
    return name in REGISTERED_ATTACKS


def assert_not_executable(name: str) -> None:
    if is_registered_attack(name):
        raise ControlSchemaError(f"proposal {name!r} is an executable registry attack")
    if name.lower().strip() in FORBIDDEN_PROPOSAL_NAMES:
        raise ControlSchemaError(f"proposal name {name!r} is generic, not a mechanism")


def evidence_from_experiment(experiment: MemoryExperiment, *, strategy_chain: str = "") -> ProposalEvidence:
    fp = experiment.diagnosis.fingerprint
    artifact = experiment.run_artifact
    yield_report = experiment.mathematical_yield
    skipped = tuple(artifact.skipped) if artifact is not None else ()
    statuses = dict(artifact.attack_statuses) if artifact is not None else {}
    exhausted = any(value == "COMPUTATION_EXHAUSTED" for value in statuses.values())
    return ProposalEvidence(
        experiment_id=experiment.experiment_id,
        target=experiment.target,
        fingerprint=fp.as_dict(),
        failure_classes=tuple(item.failure_class.value for item in experiment.failures),
        skipped_attacks=skipped,
        skip_reasons=tuple((name, statuses.get(name, "SKIPPED")) for name in skipped),
        attack_statuses=statuses,
        strategy_chain=strategy_chain,
        unresolved_questions=tuple(yield_report.unresolved_questions),
        new_counterexamples=tuple(yield_report.new_counterexamples),
        new_obstructions=tuple(yield_report.new_obstructions),
        new_exact_results=tuple(yield_report.new_exact_results),
        known_rediscoveries=tuple(yield_report.known_rediscoveries),
        strongest_falsification=experiment.diagnosis.strongest_falsification,
        census_kind=(artifact.census_kind if artifact is not None else "") or "",
        piecewise_affine_structure=fp.piecewise_affine_structure,
        affine_control_type=fp.affine_control_type,
        eventual_region=fp.eventual_region,
        numerical_contraction=fp.numerical_contraction,
        decision_reason=experiment.diagnosis.decision_reason,
        novelty_status=experiment.novelty_status.value,
        lean_certificate=experiment.diagnosis.lean_certificate,
        computation_exhausted=exhausted,
        infinite_reachability_unresolved="reach" in " ".join(yield_report.unresolved_questions).lower()
        or fp.eventual_region in {"UNBOUNDED_SAMPLE", "UNBOUNDED"},
    )


def _blob(evidence: ProposalEvidence) -> str:
    return " ".join(
        [
            evidence.experiment_id,
            evidence.target,
            evidence.decision_reason,
            evidence.census_kind,
            evidence.piecewise_affine_structure,
            evidence.eventual_region,
            evidence.strategy_chain,
            " ".join(evidence.failure_classes),
            " ".join(evidence.unresolved_questions),
            " ".join(evidence.new_obstructions),
            " ".join(evidence.new_counterexamples),
            " ".join(evidence.new_exact_results),
            " ".join(evidence.known_rediscoveries),
            evidence.strongest_falsification,
            " ".join(evidence.skipped_attacks),
        ]
    ).lower()


def _candidates(evidence: ProposalEvidence) -> list[_Candidate]:
    text = _blob(evidence)
    items: list[_Candidate] = []

    skipped_matrix = "matrix_word_invariant" in evidence.skipped_attacks or evidence.attack_statuses.get(
        "matrix_word_invariant"
    ) in {"COMPUTATION_EXHAUSTED", "SKIPPED"}
    skipped_vector = "vector_affine" in evidence.skipped_attacks or evidence.attack_statuses.get(
        "vector_affine"
    ) in {"COMPUTATION_EXHAUSTED", "SKIPPED"}
    affine_failed = evidence.piecewise_affine_structure in {"UNOBSERVED", "UNCERTAIN"} or evidence.census_kind in {
        "",
        "INCONCLUSIVE",
    }
    has_image = "image" in text or "residue" in text or "mod " in text
    has_basin = "basin" in text or "reach" in text or "avoider" in text
    has_counter = bool(evidence.new_counterexamples) or bool(evidence.strongest_falsification)
    global_gap = (
        "GLOBAL_REASONING" in evidence.failure_classes
        or evidence.infinite_reachability_unresolved
        or evidence.strategy_chain == "global_inductive"
        or bool(evidence.unresolved_questions)
    )
    standing_ranking_gap = not GLOBAL_INDUCTIVE_CHAIN.attacks
    rewrite = "tag" in text or "length" in text or "rewrite" in text or "digit" in text
    nonlinear = affine_failed and (
        "floor" in text or "power" in text or "factor" in text or "concat" in text or "reverse" in text
    )

    if has_image and (has_basin or has_counter):
        items.append(
            _Candidate(
                attack_name="basin_preimage_grammar",
                trigger=(
                    evidence.new_obstructions[0]
                    if evidence.new_obstructions
                    else evidence.strongest_falsification
                    or "image or residue class does not exclude the investigated basin"
                ),
                mathematical_target=(
                    "Characterize a finite quotient of predecessor states that preserves "
                    "reachability of the declared target, or prove that no class of the "
                    "recovered image is a basin obstruction."
                ),
                mechanism=(
                    "From the recovered forward image class C, construct the predecessor "
                    "relation T^{-1} restricted to residue or valuation slices and ask "
                    "whether membership in C is necessary for reaching the target."
                ),
                required_capability="symbolic predecessor construction",
                expected_yield="quotient theorem or counterexample family for basin membership",
                falsifier=(
                    "Produce two predecessor states indistinguishable by the proposed "
                    "quotient but with different reachability behavior."
                ),
                novelty_risk=NoveltyRisk.MEDIUM,
                implementation_scope=ImplementationScope.MEDIUM,
                confidence=Confidence.HIGH if has_counter else Confidence.MEDIUM,
                novelty_risk_reason="forward image classes are classical; predecessor quotients may still be new as engine language",
                yield_rank=6,
            )
        )
    if has_image and ("valuation" in text or "v_2" in text or "odd" in text or "mod" in text):
        items.append(
            _Candidate(
                attack_name="residue_valuation_coupling",
                trigger=evidence.new_exact_results[0] if evidence.new_exact_results else "recovered residue image class",
                mathematical_target=(
                    "Couple the residue image with a valuation (or length) coordinate "
                    "and extract a necessary condition for target-hitting orbits."
                ),
                mechanism=(
                    "Write the transition on pairs (residue, valuation) and search for "
                    "an invariant or a one-way implication residue ∈ C ⇒ valuation constraint."
                ),
                required_capability="residue × valuation class algebra",
                expected_yield="necessary condition relating residue class and valuation",
                falsifier="Find a transition that stays in the residue class while violating every candidate valuation bound.",
                novelty_risk=NoveltyRisk.MEDIUM,
                implementation_scope=ImplementationScope.MEDIUM,
                confidence=Confidence.MEDIUM,
                novelty_risk_reason="residue–valuation dictionaries are standard in mx+r maps",
                yield_rank=4,
            )
        )
    if standing_ranking_gap or global_gap:
        items.append(
            _Candidate(
                attack_name="ranking_function_synthesis",
                trigger=(
                    "global_inductive selected but has no ranking implementation"
                    if (evidence.strategy_chain == "global_inductive" or standing_ranking_gap)
                    else evidence.unresolved_questions[0]
                    if evidence.unresolved_questions
                    else "finite local evidence does not lift to an infinite-time theorem"
                ),
                mathematical_target=(
                    "Construct a well-founded ranking function outside a finite exceptional set, "
                    "or prove that every candidate ranking from the existing catalog fails."
                ),
                mechanism=(
                    "Search a catalog of linear / norm / lexicographic measures V with "
                    "V(T(x)) < V(x) on the complement of a finite set, using existing "
                    "envelope leaks only as oracles, not as theorems."
                ),
                required_capability="ranking-function synthesis",
                expected_yield="ranking certificate or a closed branch on which every catalog measure fails",
                falsifier="Generate a closed branch on which every candidate ranking measure fails.",
                novelty_risk=NoveltyRisk.HIGH,
                implementation_scope=ImplementationScope.LARGE,
                confidence=Confidence.MEDIUM if global_gap else Confidence.LOW,
                novelty_risk_reason="ranking catalogs often rediscover Lyapunov folklore; still the missing v2.3 boundary",
                yield_rank=5 if global_gap else 3,
            )
        )
    if skipped_matrix or skipped_vector:
        items.append(
            _Candidate(
                attack_name="global_vanishing_congruence",
                trigger=(
                    "vector_affine / matrix_word_invariant skipped by adapter cell budget"
                    if skipped_matrix or skipped_vector
                    else "companion window recovered without a vanishing congruence"
                ),
                mathematical_target=(
                    "Produce a lattice or modular constraint on vanishing indices that is "
                    "independent of the skipped 25^d census, or prove no such constraint exists "
                    "in the current matrix-word language."
                ),
                mechanism=(
                    "Work with the companion recurrence symbolically: gcd of values, "
                    "resultant of truncated generating functions, or an ideal membership "
                    "test that does not enumerate the 25^d cube."
                ),
                required_capability="symbolic matrix-word / lattice congruence outside the cell budget",
                expected_yield="exact vanishing congruence or a proof that the skipped attack cannot supply one",
                falsifier="Exhibit a prefix or modulus that hits 0 in every candidate congruence class.",
                novelty_risk=NoveltyRisk.HIGH,
                implementation_scope=ImplementationScope.LARGE,
                confidence=Confidence.MEDIUM,
                novelty_risk_reason="Skolem-type congruences are heavily studied; the engine-specific gap is the skip boundary",
                yield_rank=5,
            )
        )
    if nonlinear or affine_failed:
        items.append(
            _Candidate(
                attack_name="symbolic_nonlinear_composition",
                trigger=(
                    "piecewise-affine census INCONCLUSIVE; successor is not residue-affine"
                    if affine_failed
                    else "nonlinear branch recovered only as exact I/O"
                ),
                mathematical_target=(
                    "Compose the exact nonlinear successor symbolically for several steps "
                    "and extract an invariant, a growth law, or a finite attractor grammar."
                ),
                mechanism=(
                    "Treat T as a piecewise nonlinear word (floor-power, digit reverse, "
                    "factor concatenation, or rewrite) and compute a closed-form iterate "
                    "or a generating-function identity on a cylinder."
                ),
                required_capability="symbolic nonlinear branch composition",
                expected_yield="exact iterate identity, growth invariant, or attractor grammar",
                falsifier="Find a cylinder on which the composed expression disagrees with exact I/O.",
                novelty_risk=NoveltyRisk.HIGH,
                implementation_scope=ImplementationScope.LARGE,
                confidence=Confidence.MEDIUM if nonlinear else Confidence.LOW,
                novelty_risk_reason="nonlinear composition is the declared missing language, with high rediscovery risk per map",
                yield_rank=5,
            )
        )
    if rewrite:
        items.append(
            _Candidate(
                attack_name="digit_structure_ranking",
                trigger="length is nondecreasing under the rewrite rules"
                if "length" in text
                else "digit or word structure dominates the integer encoding",
                mathematical_target=(
                    "Lift a digit- or length-ranking on the native word representation, "
                    "not on the integer encoding, and decide termination or expansion."
                ),
                mechanism=(
                    "Interpret T on words, take a lexicographic or length measure, and "
                    "compare V(w) and V(T(w)) independently of the integer embedding."
                ),
                required_capability="digit-structure ranking on the native representation",
                expected_yield="ranking certificate on words, or a spec-mismatch lemma",
                falsifier="Produce a word whose successor decreases the proposed ranking.",
                novelty_risk=NoveltyRisk.LOW,
                implementation_scope=ImplementationScope.SMALL,
                confidence=Confidence.HIGH if "length" in text else Confidence.MEDIUM,
                novelty_risk_reason="length-nondecrease is often the production itself",
                yield_rank=3,
            )
        )
    if evidence.lean_certificate or evidence.unresolved_questions:
        items.append(
            _Candidate(
                attack_name="proof_guided_invariant_refinement",
                trigger=(
                    f"Lean module {evidence.lean_certificate} certifies identities while the map theorem stays open"
                    if evidence.lean_certificate
                    else evidence.unresolved_questions[0]
                ),
                mathematical_target=(
                    "Turn the surviving Lean identities and unresolved question into a "
                    "sharpened invariant hypothesis with an explicit finite exceptional set."
                ),
                mechanism=(
                    "Read the certified identities as constraints, propose the weakest "
                    "inductive predicate that implies the open claim, and search for a "
                    "counterexample on the complement."
                ),
                required_capability="proof-guided hypothesis refinement",
                expected_yield="proof-ready conjecture or a finite exceptional-set counterexample",
                falsifier="Find a state satisfying the certified identities but violating the refined invariant.",
                novelty_risk=NoveltyRisk.MEDIUM,
                implementation_scope=ImplementationScope.MEDIUM,
                confidence=Confidence.MEDIUM if evidence.lean_certificate else Confidence.LOW,
                novelty_risk_reason="refinement of known identities can collapse to restatement",
                yield_rank=4,
            )
        )
    items.append(
        _Candidate(
            attack_name="predecessor_reachability_quotient",
            trigger=evidence.unresolved_questions[0]
            if evidence.unresolved_questions
            else "forward image restriction fails to characterize the basin",
            mathematical_target=(
                "Build a finite automaton or residue quotient of predecessor states "
                "that is sound for reachability of the declared target."
            ),
            mechanism=(
                "Iterate a bounded preimage operator, merge states with identical "
                "one-step images, and ask whether the accepting component is regular."
            ),
            required_capability="basin / preimage reasoning",
            expected_yield="regular-preimage lemma or a pair of states that split reachability",
            falsifier="Produce two predecessor states indistinguishable by the proposed quotient but with different reachability behavior.",
            novelty_risk=NoveltyRisk.MEDIUM,
            implementation_scope=ImplementationScope.MEDIUM,
            confidence=Confidence.LOW,
            novelty_risk_reason="preimage automata are classical; value is coupling to the recovered engine language",
            yield_rank=4,
        )
    )
    items.append(
        _Candidate(
            attack_name="local_invariant_asymptotic_coupling",
            trigger=evidence.known_rediscoveries[0]
            if evidence.known_rediscoveries
            else "local exact identities exist without an asymptotic theorem",
            mathematical_target=(
                "Couple a local invariant recovered on a window with an asymptotic "
                "growth or contraction law on the complement."
            ),
            mechanism=(
                "Split state space into a finite core and a tail; prove the local "
                "relation on the core and a monotonicity law on the tail."
            ),
            required_capability="local invariant × asymptotic growth",
            expected_yield="exact lemma on the core plus a tail ranking, or a leak in the tail",
            falsifier="Find a tail transition escaping every candidate member of the proposed class.",
            novelty_risk=NoveltyRisk.MEDIUM,
            implementation_scope=ImplementationScope.MEDIUM,
            confidence=Confidence.LOW,
            novelty_risk_reason="core/tail splits often restatement of known contraction",
            yield_rank=3,
        )
    )
    # Deduplicate by attack_name, first trigger wins.
    unique: dict[str, _Candidate] = {}
    for item in items:
        if item.attack_name not in unique:
            unique[item.attack_name] = item
    return list(unique.values())


def _score(item: _Candidate) -> tuple[int, int, int]:
    """Conceptual yield / (novelty). Deep proposals outrank census extensions."""

    return (-item.yield_rank, _NOVELTY_WEIGHT[item.novelty_risk], _SCOPE_WEIGHT[item.implementation_scope])


def _thin_confidence(evidence: ProposalEvidence) -> bool:
    return (
        not evidence.new_exact_results
        and not evidence.new_counterexamples
        and not evidence.unresolved_questions
        and not evidence.skipped_attacks
    )


def propose_attacks(evidence: ProposalEvidence, *, campaign_id: str = "") -> AttackProposalDossier:
    """Emit exactly three ranked non-executable proposals."""

    ranked = sorted(_candidates(evidence), key=_score)
    thin = _thin_confidence(evidence)
    chosen = ranked[:3]
    fillers = (
        "proof_guided_invariant_refinement",
        "finite_exception_ranking",
        "local_invariant_asymptotic_coupling",
    )
    used = {item.attack_name for item in chosen}
    for name in fillers:
        if len(chosen) >= 3:
            break
        if name in used:
            continue
        chosen.append(
            _Candidate(
                attack_name=name,
                trigger="insufficient campaign structure; default refinement proposal",
                mathematical_target="Sharpen any surviving exact identity into a falsifiable invariant.",
                mechanism="Treat certified identities as constraints and search a counterexample on the complement.",
                required_capability="proof-guided hypothesis refinement",
                expected_yield="proof-ready conjecture",
                falsifier="Find a state satisfying the identities but violating the refined invariant.",
                novelty_risk=NoveltyRisk.HIGH,
                implementation_scope=ImplementationScope.MEDIUM,
                confidence=Confidence.LOW,
                novelty_risk_reason="filler proposal under thin evidence",
                yield_rank=2,
            )
        )
        used.add(name)
    if len(chosen) < 3:
        raise ControlSchemaError("could not produce three attack proposals")
    proposals: list[AttackProposal] = []
    for index, item in enumerate(chosen[:3], start=1):
        assert_not_executable(item.attack_name)
        confidence = Confidence.LOW if thin else item.confidence
        proposals.append(
            AttackProposal(
                rank=index,
                attack_name=item.attack_name,
                trigger=item.trigger,
                mathematical_target=item.mathematical_target,
                mechanism=item.mechanism,
                required_capability=item.required_capability,
                expected_yield=item.expected_yield,
                falsifier=item.falsifier,
                novelty_risk=item.novelty_risk,
                implementation_scope=item.implementation_scope,
                confidence=confidence,
                novelty_risk_reason=item.novelty_risk_reason,
            )
        )
    notes = ()
    if thin:
        notes = ("evidence was thin; all three proposals marked LOW confidence",)
    return AttackProposalDossier(
        proposals=tuple(proposals),
        campaign_id=campaign_id or evidence.experiment_id,
        notes=notes,
    )
