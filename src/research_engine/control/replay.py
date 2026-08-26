"""v2.2 replay protocol. Historical results are evaluation metadata, not blind inputs."""

from __future__ import annotations

from collections.abc import Callable

from research_engine.control.archive import archive_with_control
from research_engine.control.baseline import FrozenBaseline
from research_engine.control.close import validate_record
from research_engine.control.store import ControlStore
from research_engine.control.types import (
    COMPARISON_DIMENSIONS,
    CampaignControlRecord,
    CampaignType,
    CloseTag,
    ComparisonCell,
    ControlSchemaError,
    EXECUTION_ENGINE,
    ExecutionStatus,
    MathematicalStatus,
    ReplayComparison,
    ReplayMetadata,
    ReplayObservationClass,
)
from research_engine.memory.types import BlindPacket, MemoryExperiment, TargetBoard

ReplayRunner = Callable[[str], MemoryExperiment]


def replay_campaign_id(source_target_id: str) -> str:
    return f"replay_v22_{source_target_id}"


def recover_historical(baseline: FrozenBaseline, source_target_id: str) -> MemoryExperiment:
    return baseline.find_experiment(source_target_id)


def recover_target(board: TargetBoard, source_target_id: str):
    return board.by_name()[source_target_id]


def assert_already_run_unchanged(board: TargetBoard, source_target_id: str) -> None:
    target = recover_target(board, source_target_id)
    if not target.already_run:
        raise ControlSchemaError(f"historical already_run was reset for {source_target_id}")


def historical_tokens(experiment: MemoryExperiment) -> tuple[str, ...]:
    tokens: list[str] = []
    yield_report = experiment.mathematical_yield
    tokens.extend(yield_report.new_exact_results)
    tokens.extend(yield_report.new_counterexamples)
    tokens.extend(yield_report.new_obstructions)
    tokens.extend(yield_report.new_conjectures)
    tokens.extend(item.statement for item in experiment.grey_loot)
    if experiment.diagnosis.strongest_exact:
        tokens.append(experiment.diagnosis.strongest_exact)
    if experiment.diagnosis.strongest_falsification:
        tokens.append(experiment.diagnosis.strongest_falsification)
    return tuple(item for item in tokens if item and len(item) >= 8)


def assert_blind_excludes_historical(packet: BlindPacket, historical: MemoryExperiment) -> None:
    """Historical yield/loot must not enter the blind attack payload."""

    payload = packet.attack_payload()
    blob = " ".join(str(value) for value in payload.values())
    for token in historical_tokens(historical):
        if token and token in blob:
            raise ControlSchemaError(
                "historical result leaked into BlindPacket.attack_payload: "
                f"{token[:80]!r}"
            )


def assert_replay_isolated(
    historical: MemoryExperiment,
    replay: MemoryExperiment,
    board: TargetBoard,
    source_target_id: str,
) -> None:
    if replay.experiment_id == historical.experiment_id:
        raise ControlSchemaError("replay must use a distinct campaign/experiment id")
    if not replay.experiment_id.startswith("replay_"):
        raise ControlSchemaError("replay experiment_id must be a replay_* identifier")
    assert_already_run_unchanged(board, source_target_id)
    if replay.blind_packet is not None:
        assert_blind_excludes_historical(replay.blind_packet, historical)


def _cell(historical: str, current: str, classification: ReplayObservationClass) -> ComparisonCell:
    return ComparisonCell(historical=historical, current=current, classification=classification)


def _classify_text(historical: str, current: str) -> ReplayObservationClass:
    if not current or current == historical:
        return ReplayObservationClass.HISTORICAL_REPRODUCTION
    if historical and historical in current:
        return ReplayObservationClass.HISTORICAL_REFINEMENT
    return ReplayObservationClass.NEW_FORMULATION


def compare_replay(
    historical: MemoryExperiment,
    current: MemoryExperiment,
    current_record: CampaignControlRecord,
    *,
    historical_close: CloseTag | None = None,
    historical_math: MathematicalStatus | None = None,
) -> ReplayComparison:
    hist_fp = historical.diagnosis.fingerprint.populated()
    cur_fp = current.diagnosis.fingerprint.populated()
    hist_yield = "; ".join(historical.mathematical_yield.new_exact_results) or historical.diagnosis.strongest_exact
    cur_yield = "; ".join(current.mathematical_yield.new_exact_results) or current.diagnosis.strongest_exact
    hist_false = historical.diagnosis.strongest_falsification
    cur_false = current.diagnosis.strongest_falsification
    hist_lean = historical.diagnosis.lean_certificate or "; ".join(
        historical.run_artifact.lean_theorems if historical.run_artifact else ()
    )
    cur_lean = current.diagnosis.lean_certificate or "; ".join(
        current.run_artifact.lean_theorems if current.run_artifact else ()
    )
    mapping_h = historical.diagnosis.reusable_machinery or historical.diagnosis.semantic_class
    mapping_c = current.diagnosis.reusable_machinery or current.diagnosis.semantic_class
    dimensions = {
        "mapping_recovered": _cell(mapping_h, mapping_c, _classify_text(mapping_h, mapping_c)),
        "structural_observations": _cell(str(hist_fp), str(cur_fp), _classify_text(str(hist_fp), str(cur_fp))),
        "candidate_hypotheses": _cell(
            historical.diagnosis.decision_reason,
            current.diagnosis.decision_reason,
            _classify_text(historical.diagnosis.decision_reason, current.diagnosis.decision_reason),
        ),
        "falsifiers": _cell(hist_false, cur_false, _classify_text(hist_false, cur_false)),
        "scout_blind_behavior": _cell(
            "scout isolated; blind packet present" if historical.blind_packet else "no blind packet",
            "scout isolated; blind packet present" if current.blind_packet else "no blind packet",
            ReplayObservationClass.HISTORICAL_REPRODUCTION,
        ),
        "mathematical_yield": _cell(hist_yield, cur_yield, _classify_text(hist_yield, cur_yield)),
        "lean_certification": _cell(hist_lean, cur_lean, _classify_text(hist_lean, cur_lean)),
        "close_tag": _cell(
            historical_close.value if historical_close is not None else "(absent in v2.2 record)",
            current_record.close_tag.value if current_record.close_tag is not None else "",
            ReplayObservationClass.NEW_FORMULATION
            if current_record.close_tag is not None
            else ReplayObservationClass.HISTORICAL_REPRODUCTION,
        ),
        "mathematical_status": _cell(
            historical_math.value if historical_math is not None else "(absent in v2.2 record)",
            current_record.mathematical_status.value,
            ReplayObservationClass.NEW_FORMULATION,
        ),
    }
    missing = [name for name in COMPARISON_DIMENSIONS if name not in dimensions]
    if missing:
        raise ControlSchemaError(f"comparison missing dimensions {missing}")

    added: list[str] = []
    if current_record.close_tag is not None:
        added.append(f"close_tag={current_record.close_tag.value}")
    added.append(f"mathematical_status={current_record.mathematical_status.value}")
    names = tuple(item.attack_name for item in current_record.proposals.proposals)
    added.append("attack_proposals=" + ",".join(names))
    if current.diagnosis.strongest_falsification and current.diagnosis.strongest_falsification != hist_false:
        added.append("falsifier=" + current.diagnosis.strongest_falsification)

    regressions: list[str] = []
    if hist_lean and not cur_lean:
        regressions.append("lean certificate missing on replay")
    if hist_yield and not cur_yield:
        regressions.append("exact yield missing on replay")

    return ReplayComparison(
        source_target_id=historical.experiment_id,
        replay_campaign_id=current_record.campaign_id,
        dimensions=dimensions,
        v2_4_added_information=tuple(added),
        v2_4_regression=tuple(regressions),
    )


def run_replay(
    baseline: FrozenBaseline,
    source_target_id: str,
    runner: ReplayRunner,
    *,
    store: ControlStore | None = None,
    execution_status: ExecutionStatus = ExecutionStatus.CLOSE,
) -> CampaignControlRecord:
    """Run a supplied blind runner and archive a REPLAY control record.

    ``runner`` must not ingest historical GreyLoot or yield into the blind track.
    """

    historical = recover_historical(baseline, source_target_id)
    assert_already_run_unchanged(baseline.board, source_target_id)
    live = runner(source_target_id)
    cid = replay_campaign_id(source_target_id)
    if live.experiment_id != cid:
        raise ControlSchemaError(
            f"runner must assign experiment_id {cid!r}, got {live.experiment_id!r}"
        )
    assert_replay_isolated(historical, live, baseline.board, source_target_id)
    metadata = ReplayMetadata(
        campaign_type=CampaignType.REPLAY,
        source_engine="v2.2",
        execution_engine=EXECUTION_ENGINE,
        source_target_id=source_target_id,
        source_campaign_id=historical.experiment_id,
    )
    record = archive_with_control(
        live,
        campaign_id=cid,
        execution_status=execution_status,
        campaign_type=CampaignType.REPLAY,
        replay_metadata=metadata,
        store=store,
        notes=("v2.2 replay; historical results used only for comparison",),
    )
    comparison = compare_replay(historical, live, record)
    record = CampaignControlRecord(
        campaign_id=record.campaign_id,
        experiment_id=record.experiment_id,
        target=record.target,
        execution_status=record.execution_status,
        mathematical_status=record.mathematical_status,
        proposals=record.proposals,
        close_tag=record.close_tag,
        provenance=record.provenance,
        campaign_type=record.campaign_type,
        replay_metadata=record.replay_metadata,
        comparison=comparison,
        engine_control_version=record.engine_control_version,
        source_engine_version=record.source_engine_version,
        notes=record.notes,
    )
    validate_record(record)
    if store is not None:
        store.add(record)
    return record
