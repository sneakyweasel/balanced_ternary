"""Research-control layer for frozen Research Engine v2.4.

Not an attack engine. Discovers a frontier, classifies why execution
stopped, preserves the v2.3 baseline, and proposes three next attacks
without executing them.
"""

from research_engine.control.archive import archive_with_control, overlay_from_experiments
from research_engine.control.baseline import (
    BASELINE_IDENTIFIER,
    BaselineImmutableError,
    FrozenBaseline,
    load_v2_3_baseline,
    verify_manifest,
)
from research_engine.control.close import validate_pair, validate_record
from research_engine.control.migrate import V2_3_INFERENCE, infer_classification
from research_engine.control.proposals import (
    REGISTERED_ATTACKS,
    assert_not_executable,
    evidence_from_experiment,
    is_registered_attack,
    propose_attacks,
)
from research_engine.control.replay import (
    assert_blind_excludes_historical,
    assert_replay_isolated,
    compare_replay,
    recover_historical,
    replay_campaign_id,
    run_replay,
)
from research_engine.control.retrospective import build_retrospective
from research_engine.control.store import ControlStore
from research_engine.control.types import (
    ENGINE_CONTROL_VERSION,
    AttackProposal,
    AttackProposalDossier,
    CampaignControlRecord,
    CampaignType,
    CloseTag,
    ExecutionStatus,
    FieldProvenance,
    MathematicalStatus,
    ReplayComparison,
    ReplayMetadata,
    V2_3_CAMPAIGN_ORDER,
)


def v2_3_control_records(baseline: FrozenBaseline | None = None) -> tuple[CampaignControlRecord, ...]:
    snap = baseline if baseline is not None else load_v2_3_baseline()
    experiments = tuple(snap.experiment(name) for name in V2_3_CAMPAIGN_ORDER)
    return overlay_from_experiments(experiments)


__all__ = [
    "BASELINE_IDENTIFIER",
    "BaselineImmutableError",
    "CampaignControlRecord",
    "CampaignType",
    "CloseTag",
    "ControlStore",
    "ENGINE_CONTROL_VERSION",
    "ExecutionStatus",
    "FieldProvenance",
    "FrozenBaseline",
    "MathematicalStatus",
    "REGISTERED_ATTACKS",
    "ReplayComparison",
    "ReplayMetadata",
    "V2_3_CAMPAIGN_ORDER",
    "V2_3_INFERENCE",
    "AttackProposal",
    "AttackProposalDossier",
    "archive_with_control",
    "assert_blind_excludes_historical",
    "assert_not_executable",
    "assert_replay_isolated",
    "build_retrospective",
    "compare_replay",
    "evidence_from_experiment",
    "infer_classification",
    "is_registered_attack",
    "load_v2_3_baseline",
    "overlay_from_experiments",
    "propose_attacks",
    "recover_historical",
    "replay_campaign_id",
    "run_replay",
    "v2_3_control_records",
    "validate_pair",
    "validate_record",
    "verify_manifest",
]
