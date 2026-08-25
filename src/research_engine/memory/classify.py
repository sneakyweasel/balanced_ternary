"""Heuristic failure classification from already-computed evidence."""

from __future__ import annotations

from dataclasses import dataclass

from research_engine.memory.types import (
    ENGINE_MEMORY_VERSION,
    FailureClass,
    FailureRecord,
    FailureStatus,
    ImportanceLevel,
)


@dataclass(frozen=True)
class FailureSignals:
    """Post-run signals. Never inferred from a target name."""

    target: str
    experiment_id: str
    decision: str
    census_kind: str = ""
    affine_control_type: str = ""
    piecewise_affine_structure: str = ""
    latent_control: str = ""
    numerical_contraction: str = ""
    eventual_region: str = ""
    control_structure: str = ""
    computation_exhausted: bool = False
    overlapping_branches: bool = False
    recovered_language: bool = False
    infinite_reachability_unresolved: bool = False
    transition_unresolved: bool = False
    hygiene_issue: bool = False
    sign_first_truncation: bool = False
    dimension: int = 1
    skipped_control_stack: bool = False
    engine_version: str = ENGINE_MEMORY_VERSION
    prior_art_status: str = ""


def classify_signals(signals: FailureSignals) -> tuple[FailureRecord, ...]:
    """Return zero or more failure records. A success may still yield a lesson."""

    records: list[FailureRecord] = []
    base = {
        "target": signals.target,
        "experiment_id": signals.experiment_id,
        "engine_version": signals.engine_version,
        "prior_art_status": signals.prior_art_status,
    }

    if signals.hygiene_issue:
        records.append(
            _record(
                **base,
                suffix="hygiene",
                phase="benchmark",
                attack="literature_leak",
                failure_class=FailureClass.EXPERIMENT_HYGIENE,
                representation_status="N_A",
                bottleneck="identifier_token_false_positive",
                evidence="technical identifier matched a literature token",
                lesson="Package ids and theorem names must not trigger literature-leak failures.",
                action="RESOLVED",
                value=ImportanceLevel.LOW,
                status=FailureStatus.RESOLVED,
                family="hygiene",
            )
        )

    if signals.overlapping_branches:
        records.append(
            _record(
                **base,
                suffix="quantifier",
                phase="control",
                attack="control_word",
                failure_class=FailureClass.QUANTIFIER,
                representation_status="NONDETERMINISTIC_BRANCHING",
                bottleneck="overlapping_existential_branches",
                evidence="branching is diagnosable but deterministic control cannot consume it",
                lesson="Nondeterminism is a quantifier mismatch, not a missing affine census.",
                family="deterministic_control",
                value=ImportanceLevel.MEDIUM,
            )
        )

    if signals.sign_first_truncation:
        records.append(
            _record(
                **base,
                suffix="domain",
                phase="census",
                attack="piecewise_affine",
                failure_class=FailureClass.DOMAIN_INFERENCE,
                representation_status="SIGN_TRUNCATED_AFFINE",
                bottleneck="sign_first_region_inference",
                evidence="sign-first partition truncates a globally valid affine law",
                lesson="Do not implement a census fix from a single involution failure.",
                action="DO_NOT_IMPLEMENT",
                family="piecewise_affine",
                value=ImportanceLevel.MEDIUM,
            )
        )

    recovered = signals.recovered_language or signals.piecewise_affine_structure in {
        "FINITE",
        "PARAMETERIZED",
    }
    affine_type = signals.affine_control_type
    vectorish = affine_type in {"VECTOR", "MATRIX_PARAMETERIZED"} or recovered

    if signals.transition_unresolved or (
        signals.decision == "ENGINE_LIMITATION"
        and not recovered
        and signals.census_kind in {"", "UNRESOLVED", "UNCERTAIN"}
        and not signals.computation_exhausted
    ):
        records.append(
            _record(
                **base,
                suffix="representation",
                phase="census",
                attack="piecewise_affine",
                failure_class=FailureClass.REPRESENTATION,
                representation_status="NON_AFFINE",
                bottleneck="outside_affine_valuation_control",
                evidence="singleton mixed-magnitude dynamics with no recovered affine language",
                lesson="A representation mismatch is not a missing attack to implement immediately.",
                family="latent_affine",
                value=ImportanceLevel.HIGH,
            )
        )

    if signals.computation_exhausted:
        records.append(
            _record(
                **base,
                suffix="computational",
                phase="census",
                attack="vector_affine",
                failure_class=FailureClass.COMPUTATIONAL,
                representation_status="VECTOR_AFFINE_ADEQUATE" if vectorish or signals.dimension >= 2 else "UNKNOWN",
                bottleneck="finite_budget_exhausted",
                evidence="exact reasoning conceptually available; computational budget exhausted",
                lesson="Computational blockage is not mathematical impossibility.",
                family="vector_census",
                value=ImportanceLevel.MEDIUM,
            )
        )

    if signals.infinite_reachability_unresolved and (
        recovered or vectorish or signals.dimension >= 2
    ):
        records.append(
            _record(
                **base,
                suffix="global",
                phase="reachability",
                attack="closure",
                failure_class=FailureClass.GLOBAL_REASONING,
                representation_status="LANGUAGE_ADEQUATE",
                bottleneck="finite_to_infinite_certificate",
                evidence="state language reconstructed; infinite-time reachability unresolved",
                lesson="Representation fit is not an infinite-time theorem.",
                family="global_reachability",
                value=ImportanceLevel.HIGH,
            )
        )

    if signals.decision in {"CLOSE", "FAMILY_SATURATED"} and signals.numerical_contraction == "FINITE_CONTRACTING":
        if not any(item.failure_class is FailureClass.REPRESENTATION for item in records):
            records.append(
                _record(
                    **base,
                    suffix="novelty",
                    phase="diagnosis",
                    attack="reconnaissance",
                    failure_class=FailureClass.NOVELTY,
                    representation_status="SCALAR_DIGIT_FOLD",
                    bottleneck="saturated_finite_contracting_regime",
                    evidence="core fingerprint matches a saturated finite-contracting family",
                    lesson="Further scalar digit-fold variants have low expected research value.",
                    family="scalar_fold",
                    value=ImportanceLevel.LOW,
                    status=FailureStatus.RECORDED,
                )
            )

    return tuple(records)


def _record(
    *,
    target: str,
    experiment_id: str,
    engine_version: str,
    prior_art_status: str,
    suffix: str,
    phase: str,
    attack: str,
    failure_class: FailureClass,
    representation_status: str,
    bottleneck: str,
    evidence: str,
    lesson: str,
    family: str,
    action: str = "PARK",
    value: ImportanceLevel = ImportanceLevel.MEDIUM,
    status: FailureStatus = FailureStatus.PARKED,
) -> FailureRecord:
    return FailureRecord(
        id=f"{experiment_id}:{suffix}",
        target=target,
        experiment_id=experiment_id,
        engine_version=engine_version,
        phase=phase,
        attack=attack,
        failure_class=failure_class,
        representation_status=representation_status,
        mathematical_bottleneck=bottleneck,
        evidence=evidence,
        reusable_lesson=lesson,
        prior_art_status=prior_art_status,
        engineering_action=action,
        research_value=value,
        status=status,
        affected_attack_family=family,
    )
