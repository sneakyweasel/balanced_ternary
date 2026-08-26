"""Post-session control archival. Does not rewrite MemoryExperiment."""

from __future__ import annotations

from research_engine.control.close import validate_record
from research_engine.control.migrate import default_execution_status, infer_classification
from research_engine.control.proposals import evidence_from_experiment, propose_attacks
from research_engine.control.store import ControlStore
from research_engine.control.types import (
    ENGINE_CONTROL_VERSION,
    CampaignControlRecord,
    CampaignType,
    CloseTag,
    ExecutionStatus,
    FieldProvenance,
    MathematicalStatus,
    ReplayComparison,
    ReplayMetadata,
)
from research_engine.memory.types import MemoryExperiment


def archive_with_control(
    experiment: MemoryExperiment,
    *,
    campaign_id: str | None = None,
    execution_status: ExecutionStatus | None = None,
    close_tag: CloseTag | None = None,
    mathematical_status: MathematicalStatus | None = None,
    campaign_type: CampaignType = CampaignType.LIVE,
    replay_metadata: ReplayMetadata | None = None,
    comparison: ReplayComparison | None = None,
    strategy_chain: str = "",
    store: ControlStore | None = None,
    notes: tuple[str, ...] = (),
) -> CampaignControlRecord:
    """Classify, propose, and optionally persist a v2.4 overlay record."""

    cid = campaign_id or experiment.experiment_id
    inferred_tag, inferred_math, provenance_kind, reason = infer_classification(experiment)
    status = execution_status if execution_status is not None else default_execution_status(experiment)
    tag = close_tag if close_tag is not None else inferred_tag
    math_status = mathematical_status if mathematical_status is not None else inferred_math
    provenance = {
        "execution_status": FieldProvenance.EXPLICIT
        if execution_status is not None
        else FieldProvenance.INFERRED,
        "close_tag": FieldProvenance.EXPLICIT if close_tag is not None else provenance_kind,
        "mathematical_status": FieldProvenance.EXPLICIT
        if mathematical_status is not None
        else provenance_kind,
    }
    evidence = evidence_from_experiment(experiment, strategy_chain=strategy_chain)
    dossier = propose_attacks(evidence, campaign_id=cid)
    record = CampaignControlRecord(
        campaign_id=cid,
        experiment_id=experiment.experiment_id,
        target=experiment.target,
        execution_status=status,
        mathematical_status=math_status,
        proposals=dossier,
        close_tag=tag if status is ExecutionStatus.CLOSE else None,
        provenance=provenance,
        campaign_type=campaign_type,
        replay_metadata=replay_metadata,
        comparison=comparison,
        engine_control_version=ENGINE_CONTROL_VERSION,
        source_engine_version=experiment.engine_version,
        notes=notes + ((reason,) if reason else ()),
    )
    validate_record(record)
    if store is not None:
        store.add(record)
    return record


def overlay_from_experiments(
    experiments: tuple[MemoryExperiment, ...],
    *,
    campaign_type: CampaignType = CampaignType.HISTORICAL_V23,
    store: ControlStore | None = None,
) -> tuple[CampaignControlRecord, ...]:
    target = store if store is not None else ControlStore()
    records = []
    for experiment in experiments:
        records.append(
            archive_with_control(
                experiment,
                campaign_id=experiment.experiment_id,
                campaign_type=campaign_type,
                store=target,
            )
        )
    return tuple(records)
