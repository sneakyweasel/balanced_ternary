"""Research loop: diagnose structure, then run the existing attack planner."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from research_engine.attacks.result import AttackContext, AttackStatus
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import SearchScope
from research_engine.diagnosis.corpus import ResearchCorpus
from research_engine.diagnosis.coverage import capability_coverage
from research_engine.diagnosis.decision import decide_research
from research_engine.diagnosis.family import family_id_of, family_status_for
from research_engine.diagnosis.fingerprint import fingerprint_from_report, semantic_class
from research_engine.diagnosis.probes import run_integer_probes
from research_engine.diagnosis.types import (
    CapabilityCoverage,
    ExperimentRecord,
    FamilyStatus,
    RegimeFingerprint,
    ResearchDecision,
    StructuralDelta,
)
from research_engine.planner.hypothesis import HypothesisStatus
from research_engine.planner.ledger import ResearchLedger
from research_engine.planner.orchestrator import AttackPlanner, PlannerReport


@dataclass(frozen=True)
class DiagnosisReport:
    fingerprint: RegimeFingerprint
    coverage: CapabilityCoverage
    semantic_class: str
    family_status: FamilyStatus
    family_id: str
    nearest_target: str
    delta: StructuralDelta | None
    probes: Mapping[str, Any]


@dataclass(frozen=True)
class ResearchSession:
    diagnosis: DiagnosisReport
    attack_report: PlannerReport
    decision: ResearchDecision
    decision_reason: str
    record: ExperimentRecord


def diagnose(
    spec: ProblemSpec,
    report: PlannerReport,
    context: AttackContext | None = None,
    corpus: ResearchCorpus | None = None,
    probes: Mapping[str, Any] | None = None,
) -> DiagnosisReport:
    ctx = context if context is not None else AttackContext()
    memory = corpus if corpus is not None else ResearchCorpus()
    probe_data = probes if probes is not None else run_integer_probes(spec, ctx)
    fingerprint = fingerprint_from_report(spec, report, ctx, probe_data)
    coverage = capability_coverage(fingerprint, report, probe_data)
    nearest, delta = memory.nearest(fingerprint, exclude=getattr(spec, "name", ""))
    status = family_status_for(fingerprint, memory.records)
    return DiagnosisReport(
        fingerprint=fingerprint,
        coverage=coverage,
        semantic_class=semantic_class(fingerprint),
        family_status=status,
        family_id=family_id_of(fingerprint),
        nearest_target="" if nearest is None else nearest.target,
        delta=delta,
        probes=probe_data,
    )


def _strongest_exact(report: PlannerReport) -> str:
    for item in report.results:
        if item.status is AttackStatus.SUPPORTED and item.scope is SearchScope.EXACT:
            return item.claim
    return ""


def _strongest_falsification(report: PlannerReport) -> str:
    for item in report.results:
        if item.status is AttackStatus.REFUTED:
            return item.claim
    for hyp in report.hypotheses:
        if hyp.status is HypothesisStatus.REFUTED:
            return hyp.statement
    return ""


def record_from_session(
    spec: ProblemSpec,
    diagnosis: DiagnosisReport,
    report: PlannerReport,
    decision: ResearchDecision,
    reason: str,
    *,
    lean_certificate: str = "",
    prior_art_status: str = "",
    reusable_machinery: str = "",
) -> ExperimentRecord:
    return ExperimentRecord(
        target=spec.name,
        semantic_class=diagnosis.semantic_class,
        fingerprint=diagnosis.fingerprint,
        family_status=diagnosis.family_status,
        family_id=diagnosis.family_id,
        nearest_target=diagnosis.nearest_target,
        structural_delta=diagnosis.delta,
        coverage=diagnosis.coverage,
        strongest_exact=_strongest_exact(report),
        strongest_falsification=_strongest_falsification(report),
        lean_certificate=lean_certificate,
        prior_art_status=prior_art_status,
        reusable_machinery=reusable_machinery,
        decision=decision,
        decision_reason=reason,
    )


class ResearchLoop:
    """Phase A classifies structure; Phase B is AttackPlanner including piecewise_affine, parameter_domain, control_word, and control_obstruction."""

    def __init__(self, ledger: ResearchLedger | None = None) -> None:
        self.ledger = ledger if ledger is not None else ResearchLedger()

    def run(
        self,
        spec: ProblemSpec,
        context: AttackContext,
        corpus: ResearchCorpus | None = None,
        *,
        lean_certificate: str = "",
        prior_art_status: str = "",
        reusable_machinery: str = "",
        record: bool = True,
    ) -> ResearchSession:
        memory = corpus if corpus is not None else ResearchCorpus()
        attack_report = AttackPlanner(self.ledger).run(spec, context)
        probes = run_integer_probes(spec, context)
        diagnosis = diagnose(spec, attack_report, context, memory, probes)
        decision, reason = decide_research(
            diagnosis.fingerprint,
            diagnosis.family_status,
            diagnosis.delta,
            attack_report,
        )
        experiment = record_from_session(
            spec,
            diagnosis,
            attack_report,
            decision,
            reason,
            lean_certificate=lean_certificate,
            prior_art_status=prior_art_status,
            reusable_machinery=reusable_machinery,
        )
        if record:
            memory.add(experiment)
        return ResearchSession(
            diagnosis=diagnosis,
            attack_report=attack_report,
            decision=decision,
            decision_reason=reason,
            record=experiment,
        )
