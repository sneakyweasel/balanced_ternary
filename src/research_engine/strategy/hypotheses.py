"""Generate ranked hypotheses from memory and live artifacts. Never fill a quota."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from research_engine.attacks.result import AttackResult, AttackStatus
from research_engine.core.semantics import ClaimKind, SearchScope
from research_engine.memory.types import (
    GreyLoot,
    GreyLootKind,
    LootEvidence,
    MemoryExperiment,
    NoveltyStatus,
)
from research_engine.planner.orchestrator import DEFAULT_ATTACK_ORDER
from research_engine.strategy.capabilities import CENSUS_OBSTRUCTION_CHAIN, VECTOR_MATRIX_CHAIN
from research_engine.strategy.types import (
    ObligationKind,
    ProofObligation,
    ResearchHypothesis,
    ResearchHypothesisStatus,
)

if TYPE_CHECKING:
    from research_engine.memory.store import ResearchMemory

_LOOT_OBLIGATION: dict[GreyLootKind, ObligationKind] = {
    GreyLootKind.CANDIDATE_INVARIANT: ObligationKind.INDUCTIVE_INCLUSION,
    GreyLootKind.FAILED_INVARIANT: ObligationKind.INDUCTIVE_INCLUSION,
    GreyLootKind.OBSTRUCTION_PATTERN: ObligationKind.CLASS_OBSTRUCTION,
    GreyLootKind.LATENT_CONTROL_PATTERN: ObligationKind.CONTROL_COMPOSITION,
    GreyLootKind.FAILED_DOMAIN_PREDICATE: ObligationKind.DOMAIN_CERTIFICATION,
}

_LOOT_CONFIDENCE: dict[LootEvidence, float] = {
    LootEvidence.PROVED: 0.9,
    LootEvidence.KNOWN: 0.85,
    LootEvidence.SUPPORTED: 0.7,
    LootEvidence.FINITE_RANGE: 0.45,
    LootEvidence.OBSERVED: 0.4,
    LootEvidence.CONJECTURAL: 0.3,
    LootEvidence.REFUTED: 0.95,
}

_GENERATIVE_LOOT = frozenset(
    {
        GreyLootKind.CANDIDATE_INVARIANT,
        GreyLootKind.FAILED_INVARIANT,
        GreyLootKind.OBSTRUCTION_PATTERN,
        GreyLootKind.LATENT_CONTROL_PATTERN,
        GreyLootKind.FAILED_DOMAIN_PREDICATE,
        GreyLootKind.POTENTIAL_RESEARCH_QUESTION,
        GreyLootKind.USEFUL_NEGATIVE_RESULT,
    }
)

_ATTACK_ALIASES: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("piecewise_affine", ("piecewise_affine", "piecewiseaffinecensus", "piecewise-affine")),
    ("parameter_domain", ("parameter_domain", "parameterdomain")),
    ("control_word", ("control_word", "controlword")),
    ("control_obstruction", ("control_obstruction", "controlobstruction")),
    ("vector_affine", ("vector_affine", "vectoraffine")),
    ("matrix_word_invariant", ("matrix_word_invariant", "matrixwordinvariant", "matrix-word")),
)


def _compact(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", text.lower())


def chain_from_machinery(text: str, *, dimension: int = 1) -> tuple[str, ...]:
    compact = _compact(text)
    found: list[str] = []
    for name, aliases in _ATTACK_ALIASES:
        if any(_compact(alias) in compact for alias in aliases) or name in text.lower():
            if name not in found:
                found.append(name)
    if found:
        order = {name: index for index, name in enumerate(DEFAULT_ATTACK_ORDER)}
        return tuple(sorted(found, key=lambda name: order.get(name, 99)))
    if dimension > 1:
        return VECTOR_MATRIX_CHAIN.attacks
    return CENSUS_OBSTRUCTION_CHAIN.attacks


def _status_from_loot(evidence: LootEvidence) -> ResearchHypothesisStatus:
    if evidence is LootEvidence.REFUTED:
        return ResearchHypothesisStatus.REFUTED
    if evidence is LootEvidence.PROVED:
        return ResearchHypothesisStatus.PROVED
    if evidence in {LootEvidence.SUPPORTED, LootEvidence.KNOWN}:
        return ResearchHypothesisStatus.SEARCH_SUPPORTED
    return ResearchHypothesisStatus.CANDIDATE


def _novelty_for(experiment: MemoryExperiment) -> NoveltyStatus:
    if experiment.novelty_status is not NoveltyStatus.UNKNOWN:
        return experiment.novelty_status
    if experiment.mathematical_novelty.value == "NONE" and experiment.prior_art is not None:
        return NoveltyStatus.KNOWN_REDISCOVERY
    return NoveltyStatus.UNKNOWN


def _closest_known(experiment: MemoryExperiment) -> tuple[str, tuple[str, ...]]:
    rediscoveries = experiment.mathematical_yield.known_rediscoveries
    closest = rediscoveries[0] if rediscoveries else ""
    matches: list[str] = list(rediscoveries)
    prior = experiment.prior_art
    if prior is not None:
        matches.extend(prior.literature_ids)
        if prior.known_theorem_status and not closest:
            closest = prior.known_theorem_status
        for item in prior.semantic_equivalents:
            if item.engine_form:
                matches.append(item.engine_form)
            if item.literature_id:
                matches.append(item.literature_id)
    if experiment.diagnosis.prior_art_status:
        matches.append(experiment.diagnosis.prior_art_status)
    unique = tuple(dict.fromkeys(item for item in matches if item))
    return closest, unique


def _obligation_for(kind: GreyLootKind, statement: str) -> tuple[ProofObligation, ...]:
    obligation_kind = _LOOT_OBLIGATION.get(kind)
    if obligation_kind is None:
        return ()
    templates = {
        ObligationKind.INDUCTIVE_INCLUSION: "Need: T(S) ⊆ S",
        ObligationKind.CLASS_OBSTRUCTION: "Need: class obstruction / D(k) ∤ C(k)",
        ObligationKind.CONTROL_COMPOSITION: "Need: certified control-word composition",
        ObligationKind.DOMAIN_CERTIFICATION: "Need: exact domain D_u",
        ObligationKind.MATRIX_INVARIANT: "Need: M(C) ⊆ C",
        ObligationKind.RANKING_DESCENT: "Need: V(T(x)) < V(x)",
        ObligationKind.DIVISIBILITY: "Need: D(k) ∤ C(k)",
    }
    return (
        ProofObligation(
            kind=obligation_kind,
            statement=templates.get(obligation_kind, statement),
        ),
    )


def _from_loot(experiment: MemoryExperiment, loot: GreyLoot) -> ResearchHypothesis | None:
    if loot.kind not in _GENERATIVE_LOOT or not loot.statement:
        return None
    closest, matches = _closest_known(experiment)
    novelty = _novelty_for(experiment)
    status = _status_from_loot(loot.evidence)
    if loot.kind is GreyLootKind.FAILED_INVARIANT:
        status = ResearchHypothesisStatus.REFUTED
    dim = 1
    if experiment.blind_packet is not None and experiment.blind_packet.dimension:
        dim = int(experiment.blind_packet.dimension)
    chain = chain_from_machinery(experiment.diagnosis.reusable_machinery, dimension=dim)
    return ResearchHypothesis(
        id=f"hyp:{loot.id}",
        statement=loot.statement,
        target=loot.target or experiment.target,
        source_target=loot.target or experiment.target,
        evidence=loot.evidence.value,
        supporting_artifacts=(loot.id, experiment.experiment_id),
        counterexamples=() if not loot.counterexample else (loot.counterexample,),
        confidence=_LOOT_CONFIDENCE.get(loot.evidence, 0.4),
        current_status=status,
        closest_known_result=closest,
        prior_art_matches=matches,
        proof_obligations=_obligation_for(loot.kind, loot.statement),
        candidate_attack_chain=chain,
        novelty_status=novelty,
        cluster_id=loot.bottleneck,
        kind=ClaimKind.REACHABLE,
    )


def _from_exact(experiment: MemoryExperiment, seen: set[str]) -> ResearchHypothesis | None:
    statement = experiment.diagnosis.strongest_exact.strip()
    if not statement:
        return None
    key = f"{experiment.target}|{statement}"
    if key in seen:
        return None
    closest, matches = _closest_known(experiment)
    dim = 1
    if experiment.blind_packet is not None and experiment.blind_packet.dimension:
        dim = int(experiment.blind_packet.dimension)
    lean = experiment.diagnosis.lean_certificate
    status = (
        ResearchHypothesisStatus.LEAN_CERTIFIED
        if lean
        else ResearchHypothesisStatus.SEARCH_SUPPORTED
    )
    return ResearchHypothesis(
        id=f"hyp:{experiment.experiment_id}:exact",
        statement=statement,
        target=experiment.target,
        source_target=experiment.target,
        evidence=experiment.diagnosis.decision_reason,
        supporting_artifacts=(experiment.experiment_id, "strongest_exact"),
        confidence=0.8 if lean else 0.65,
        current_status=status,
        closest_known_result=closest,
        prior_art_matches=matches,
        proof_obligations=(
            ProofObligation(
                kind=ObligationKind.CLASS_OBSTRUCTION
                if "obstruction" in statement.lower()
                else ObligationKind.CONTROL_COMPOSITION,
                statement=statement,
                status="OPEN" if not lean else "LEAN_CERTIFIED",
            ),
        ),
        candidate_attack_chain=chain_from_machinery(
            experiment.diagnosis.reusable_machinery, dimension=dim
        ),
        novelty_status=_novelty_for(experiment),
    )


def _from_cluster_questions(memory: ResearchMemory, seen: set[str]) -> list[ResearchHypothesis]:
    items: list[ResearchHypothesis] = []
    try:
        clusters = memory.named_clusters()
    except Exception:
        return items
    for cluster in clusters:
        for index, question in enumerate(cluster.research_questions):
            text = str(question).strip()
            if not text:
                continue
            key = f"{cluster.id}|{text}"
            if key in seen:
                continue
            seen.add(key)
            items.append(
                ResearchHypothesis(
                    id=f"hyp:cluster:{cluster.id}:{index}",
                    statement=text,
                    target=cluster.id,
                    source_target=cluster.id,
                    evidence=f"named failure cluster {cluster.id}",
                    supporting_artifacts=(cluster.id,),
                    confidence=0.35,
                    current_status=ResearchHypothesisStatus.CANDIDATE,
                    closest_known_result="",
                    prior_art_matches=(),
                    proof_obligations=(),
                    candidate_attack_chain=(),
                    novelty_status=NoveltyStatus.UNKNOWN,
                    cluster_id=cluster.id,
                )
            )
    return items


def generate_from_memory(memory: ResearchMemory) -> tuple[ResearchHypothesis, ...]:
    """Offline generation from v2.2 records. Does not fabricate filler hypotheses."""

    found: list[ResearchHypothesis] = []
    seen: set[str] = set()
    for experiment in memory.experiments:
        for loot in experiment.grey_loot:
            hyp = _from_loot(experiment, loot)
            if hyp is None:
                continue
            key = f"{hyp.target}|{hyp.statement}"
            if key in seen:
                continue
            seen.add(key)
            found.append(hyp)
        exact = _from_exact(experiment, seen)
        if exact is not None:
            seen.add(f"{exact.target}|{exact.statement}")
            found.append(exact)
        for failure in experiment.failures:
            if failure.failure_class.value != "GLOBAL_REASONING":
                continue
            statement = failure.evidence.strip() or failure.reusable_lesson
            if not statement:
                continue
            key = f"{experiment.target}|{statement}"
            if key in seen:
                continue
            seen.add(key)
            closest, matches = _closest_known(experiment)
            found.append(
                ResearchHypothesis(
                    id=f"hyp:{failure.id}",
                    statement=statement,
                    target=experiment.target,
                    source_target=experiment.target,
                    evidence=failure.mathematical_bottleneck,
                    supporting_artifacts=(failure.id,),
                    confidence=0.5,
                    current_status=ResearchHypothesisStatus.CANDIDATE,
                    closest_known_result=closest,
                    prior_art_matches=matches,
                    proof_obligations=(
                        ProofObligation(
                            kind=ObligationKind.INDUCTIVE_INCLUSION,
                            statement="Need: T(S) ⊆ S or a ranking V(T(x)) < V(x)",
                        ),
                    ),
                    candidate_attack_chain=chain_from_machinery(
                        experiment.diagnosis.reusable_machinery
                    ),
                    novelty_status=_novelty_for(experiment),
                    cluster_id="global_reachability",
                )
            )
    found.extend(_from_cluster_questions(memory, seen))
    from research_engine.strategy.rank import rank_hypotheses

    return rank_hypotheses(tuple(found), memory)


def extract_from_results(
    spec_name: str,
    results: tuple[AttackResult, ...] | list[AttackResult],
    *,
    chain: tuple[str, ...] = (),
    memory: ResearchMemory | None = None,
) -> tuple[ResearchHypothesis, ...]:
    """Live extraction from one strategy run. Same-target artifacts only."""

    found: list[ResearchHypothesis] = []
    for result in results:
        if result.status not in {AttackStatus.SUPPORTED, AttackStatus.OBSERVATION}:
            continue
        if not result.claim:
            continue
        status = (
            ResearchHypothesisStatus.SEARCH_SUPPORTED
            if result.status is AttackStatus.SUPPORTED
            else ResearchHypothesisStatus.CANDIDATE
        )
        if result.status is AttackStatus.SUPPORTED and result.scope is SearchScope.EXACT:
            status = ResearchHypothesisStatus.PROOF_READY
        obligation_kind = ObligationKind.CLASS_OBSTRUCTION
        if result.name in {"piecewise_affine", "parameter_domain"}:
            obligation_kind = ObligationKind.DOMAIN_CERTIFICATION
        elif result.name == "control_word":
            obligation_kind = ObligationKind.CONTROL_COMPOSITION
        elif result.name in {"affine", "closure"}:
            obligation_kind = ObligationKind.INDUCTIVE_INCLUSION
        found.append(
            ResearchHypothesis(
                id=f"hyp:{spec_name}:{result.name}",
                statement=result.claim,
                target=spec_name,
                source_target=spec_name,
                evidence=result.status.value,
                supporting_artifacts=(result.name,),
                counterexamples=tuple(str(item) for item in result.counterexamples[:8]),
                confidence=0.7 if result.status is AttackStatus.SUPPORTED else 0.45,
                current_status=status,
                proof_obligations=(
                    ProofObligation(kind=obligation_kind, statement=result.claim),
                ),
                candidate_attack_chain=chain or (result.name,),
                novelty_status=NoveltyStatus.UNKNOWN,
            )
        )
    ranked = found
    if memory is not None:
        from research_engine.strategy.rank import rank_hypotheses

        ranked = list(rank_hypotheses(tuple(found), memory))
    return tuple(ranked)


def remember_hypotheses(memory: ResearchMemory, hypotheses: tuple[ResearchHypothesis, ...] | list[ResearchHypothesis]) -> None:
    for item in hypotheses:
        memory.add_hypothesis(item)
