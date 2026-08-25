"""Convert a live ResearchSession into a memory experiment. Post-run only."""

from __future__ import annotations

from typing import Any

from research_engine.attacks.result import AttackContext
from research_engine.core.problem_spec import ProblemSpec
from research_engine.diagnosis.loop import ResearchSession
from research_engine.memory.classify import FailureSignals, classify_signals
from research_engine.memory.loot import extract_grey_loot
from research_engine.memory.types import (
    ENGINE_MEMORY_VERSION,
    BlindPacket,
    DecisionReason,
    MathematicalYield,
    MemoryExperiment,
    NoveltyLevel,
    NoveltyStatus,
    PriorArtMemory,
    RunArtifact,
    ScoutDossier,
)


def _attack_table(session: ResearchSession) -> dict[str, str]:
    table: dict[str, str] = {}
    for item in session.attack_report.skipped:
        table[item.attack] = "INAPPLICABLE" if "inapplicable" in item.reason.lower() else "SKIPPED"
    for item in session.attack_report.results:
        evidence = dict(item.evidence)
        if evidence.get("status") == "COMPUTATION_EXHAUSTED":
            table[item.name] = "COMPUTATION_EXHAUSTED"
        else:
            table[item.name] = item.status.value
    return table


def _census_kind(session: ResearchSession) -> str:
    for item in session.attack_report.results:
        if item.name in {"piecewise_affine", "vector_affine"}:
            kind = item.evidence.get("census_kind")
            if kind:
                return str(kind)
    return ""


def _recovered(session: ResearchSession) -> bool:
    fp = session.diagnosis.fingerprint
    return fp.piecewise_affine_structure in {"FINITE", "PARAMETERIZED"} or fp.affine_control_type in {
        "SCALAR",
        "VECTOR",
        "MATRIX_PARAMETERIZED",
    }


def signals_from_session(
    session: ResearchSession,
    spec: ProblemSpec,
    *,
    experiment_id: str,
    extra: dict[str, Any] | None = None,
) -> FailureSignals:
    payload = extra or {}
    table = _attack_table(session)
    fp = session.diagnosis.fingerprint
    exhausted = any(value == "COMPUTATION_EXHAUSTED" for value in table.values())
    unresolved_reach = (
        session.decision.value == "ENGINE_LIMITATION"
        or fp.eventual_region == "UNBOUNDED_SAMPLE"
        or table.get("closure") in {"INCONCLUSIVE", "COMPUTATION_EXHAUSTED"}
    )
    return FailureSignals(
        target=spec.name,
        experiment_id=experiment_id,
        decision=session.decision.value,
        census_kind=_census_kind(session),
        affine_control_type=fp.affine_control_type,
        piecewise_affine_structure=fp.piecewise_affine_structure,
        latent_control=fp.latent_control,
        numerical_contraction=fp.numerical_contraction,
        eventual_region=fp.eventual_region,
        control_structure=fp.control_structure,
        computation_exhausted=exhausted or bool(payload.get("computation_exhausted")),
        overlapping_branches=bool(payload.get("overlapping_branches")),
        recovered_language=_recovered(session),
        infinite_reachability_unresolved=bool(payload.get("infinite_reachability_unresolved", unresolved_reach and _recovered(session))),
        transition_unresolved=bool(payload.get("transition_unresolved")),
        hygiene_issue=bool(payload.get("hygiene_issue")),
        sign_first_truncation=bool(payload.get("sign_first_truncation")),
        dimension=int(getattr(spec, "dimension", 1) or 1),
        skipped_control_stack="control_word" in {item.attack for item in session.attack_report.skipped},
        prior_art_status=session.record.prior_art_status,
    )


def reason_from_session(session: ResearchSession, extra: dict[str, Any] | None = None) -> DecisionReason:
    payload = extra or {}
    if payload.get("hygiene_issue"):
        return DecisionReason.EXPERIMENT_HYGIENE
    if session.decision.value == "FAMILY_SATURATED":
        return DecisionReason.FAMILY_SATURATED
    prior = (session.record.prior_art_status or "").upper()
    if prior in {"KNOWN", "REPARAMETERIZATION"} and _recovered(session):
        return DecisionReason.KNOWN_REDISCOVERY
    if payload.get("overlapping_branches"):
        return DecisionReason.QUANTIFIER_MISMATCH
    if payload.get("transition_unresolved"):
        return DecisionReason.REPRESENTATION_MISMATCH
    if payload.get("computation_exhausted"):
        return DecisionReason.COMPUTATIONAL_BUDGET
    if session.decision.value == "ENGINE_LIMITATION":
        if _recovered(session):
            return DecisionReason.GLOBAL_REACHABILITY_GAP
        return DecisionReason.REPRESENTATION_MISMATCH
    return DecisionReason.NONE


def novelty_from_session(
    session: ResearchSession,
    extra: dict[str, Any] | None = None,
) -> tuple[NoveltyLevel, NoveltyLevel, NoveltyStatus]:
    payload = extra or {}
    if "representation_novelty" in payload:
        rep = NoveltyLevel(payload["representation_novelty"])
        math_n = NoveltyLevel(payload.get("mathematical_novelty") or NoveltyLevel.NONE.value)
        status = NoveltyStatus(payload.get("novelty_status") or NoveltyStatus.UNKNOWN.value)
        return rep, math_n, status
    recovered = _recovered(session)
    prior = (session.record.prior_art_status or "").upper()
    if recovered and prior in {"KNOWN", "REPARAMETERIZATION"}:
        return NoveltyLevel.HIGH, NoveltyLevel.NONE, NoveltyStatus.KNOWN_REDISCOVERY
    if session.decision.value == "FAMILY_SATURATED":
        return NoveltyLevel.NONE, NoveltyLevel.NONE, NoveltyStatus.KNOWN_REDISCOVERY
    if recovered:
        return NoveltyLevel.MEDIUM, NoveltyLevel.LOW, NoveltyStatus.PROJECT_SPECIFIC
    return NoveltyLevel.NONE, NoveltyLevel.NONE, NoveltyStatus.UNKNOWN


def yield_from_session(session: ResearchSession, extra: dict[str, Any] | None = None) -> MathematicalYield:
    payload = extra or {}
    raw = payload.get("mathematical_yield")
    if isinstance(raw, MathematicalYield):
        return raw
    if isinstance(raw, dict):
        return MathematicalYield.from_dict(raw)
    known = ()
    if (session.record.prior_art_status or "").upper() in {"KNOWN", "REPARAMETERIZATION"}:
        known = (session.record.strongest_exact or session.decision_reason,)
    return MathematicalYield(
        known_rediscoveries=known,
        new_exact_results=(session.record.strongest_exact,) if session.record.strongest_exact else (),
        new_counterexamples=(session.record.strongest_falsification,) if session.record.strongest_falsification else (),
        unresolved_questions=tuple(str(item) for item in (payload.get("unresolved_questions") or ())),
        engineering_changes=int(payload.get("engineering_changes") or 0),
    )


def blind_packet_from_spec(spec: ProblemSpec, context: AttackContext) -> BlindPacket:
    return BlindPacket(
        spec_name=spec.name,
        dimension=int(getattr(spec, "dimension", 1) or 1),
        skip_attacks=tuple(str(item) for item in context.skip_attacks),
        max_states=context.max_states,
        max_steps=context.max_steps,
    )


def experiment_from_session(
    session: ResearchSession,
    spec: ProblemSpec,
    context: AttackContext,
    *,
    experiment_id: str | None = None,
    target_family: str = "",
    adapter_version: str = "0.2.1",
    engine_version: str = ENGINE_MEMORY_VERSION,
    experiment_date: str = "",
    scout: ScoutDossier | None = None,
    prior_art: PriorArtMemory | None = None,
    extra: dict[str, Any] | None = None,
) -> MemoryExperiment:
    exp_id = experiment_id or spec.name
    payload = extra or {}
    loot = extract_grey_loot(session.attack_report, experiment_id=exp_id, target=spec.name)
    signals = signals_from_session(session, spec, experiment_id=exp_id, extra=payload)
    failures = classify_signals(signals)
    if payload.get("failures"):
        from research_engine.memory.types import FailureRecord

        failures = tuple(FailureRecord.from_dict(item) if isinstance(item, dict) else item for item in payload["failures"])
    if payload.get("grey_loot"):
        from research_engine.memory.types import GreyLoot

        loot = tuple(GreyLoot.from_dict(item) if isinstance(item, dict) else item for item in payload["grey_loot"])
    rep, math_n, status = novelty_from_session(session, payload)
    table = _attack_table(session)
    lean = session.record.lean_certificate
    run = RunArtifact(
        attack_statuses=table,
        skipped=tuple(item.attack for item in session.attack_report.skipped),
        strongest_exact=session.record.strongest_exact,
        strongest_falsification=session.record.strongest_falsification,
        census_kind=_census_kind(session),
        lean_theorems=tuple(part for part in (lean,) if part),
    )
    return MemoryExperiment(
        experiment_id=exp_id,
        target=spec.name,
        target_family=target_family,
        adapter_version=adapter_version,
        engine_version=engine_version,
        experiment_date=experiment_date,
        diagnosis=session.record,
        decision_reason_code=reason_from_session(session, payload),
        representation_novelty=rep,
        mathematical_novelty=math_n,
        novelty_status=status,
        mathematical_yield=yield_from_session(session, payload),
        failures=failures,
        grey_loot=loot,
        prior_art=prior_art,
        scout=scout,
        blind_packet=blind_packet_from_spec(spec, context),
        run_artifact=run,
        finalized=False,
    )
