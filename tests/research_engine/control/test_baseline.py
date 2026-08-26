"""Historical integrity of the frozen v2.3 baseline."""

from __future__ import annotations

import json

import pytest

from research_engine.control.baseline import (
    BASELINE_IDENTIFIER,
    BaselineImmutableError,
    FrozenResearchMemory,
    load_v2_3_baseline,
    verify_manifest,
)
from research_engine.control.types import V2_3_CAMPAIGN_ORDER
from research_engine.memory.store import BOARD_PATH, SEED_PATH
from research_engine.memory.types import MemoryExperiment, TargetBoard
from research_engine.planner.orchestrator import DEFAULT_ATTACK_ORDER


V2_2_ALREADY_RUN = (
    "skolem_order2_known_zero",
    "switching_affine_z2_origin",
    "slc_decrement",
    "euclidean_remainder",
    "aliquot_seed_12",
)


def test_baseline_identifier_and_hashes():
    baseline = load_v2_3_baseline()
    assert baseline.identifier == BASELINE_IDENTIFIER
    assert baseline.attack_order[-1] == "symmetry"
    assert baseline.attack_order == DEFAULT_ATTACK_ORDER
    verify_manifest(baseline.manifest)


def test_v2_3_campaigns_load_unchanged():
    raw = json.loads(SEED_PATH.read_text(encoding="utf-8"))
    by_id = {item["experiment_id"]: item for item in raw["experiments"]}
    for name in V2_3_CAMPAIGN_ORDER:
        original = by_id[name]
        loaded = MemoryExperiment.from_dict(original)
        assert loaded.experiment_id == name
        assert loaded.diagnosis.decision.value == original["diagnosis"]["decision"]
        assert "close_tag" not in original
        assert "mathematical_status" not in original
        assert "execution_status" not in original


def test_already_run_is_not_reset():
    board = TargetBoard.from_dict(json.loads(BOARD_PATH.read_text(encoding="utf-8")))
    names = board.by_name()
    for name in V2_3_CAMPAIGN_ORDER + V2_2_ALREADY_RUN:
        assert names[name].already_run is True


def test_target_ids_remain_stable():
    board = TargetBoard.from_dict(json.loads(BOARD_PATH.read_text(encoding="utf-8")))
    assert {item.name for item in board.targets} >= set(V2_3_CAMPAIGN_ORDER)
    assert len(board.targets) == 17


def test_baseline_memory_is_immutable():
    baseline = load_v2_3_baseline()
    experiment = baseline.experiment("mx_plus_r_7x1_class_obstruction")
    with pytest.raises(BaselineImmutableError):
        baseline.memory.add(experiment)
    with pytest.raises(BaselineImmutableError):
        baseline.memory.to_json(SEED_PATH)
    assert isinstance(baseline.memory, FrozenResearchMemory)


def test_frozen_memory_loads_historical_count():
    baseline = load_v2_3_baseline()
    assert len(baseline.memory.experiments) == 29
