"""Live v2.2 replays through frozen v2.3 attacks and the v2.4 control layer."""

from __future__ import annotations

from research.open_problems import get_problem
from research.research_control.problem import PROBLEM
from research.research_control.replay import run_blind_replay
from research_engine.control.baseline import load_v2_3_baseline
from research_engine.control.replay import replay_campaign_id, run_replay
from research_engine.control.store import ControlStore
from research_engine.control.types import CampaignType, REPLAY_V22_TARGETS
from research_engine.planner.orchestrator import DEFAULT_ATTACK_ORDER
from research_engine.strategy import freeze_attack_order


def test_problem_descriptor():
    assert get_problem("research_engine_v24") is PROBLEM
    assert PROBLEM.docs == ("docs/problems/research_engine_v24.md",)
    assert PROBLEM.status == "EXPLORATORY"


def test_attack_architecture_remains_frozen():
    assert DEFAULT_ATTACK_ORDER[-1] == "symmetry"
    assert freeze_attack_order() == DEFAULT_ATTACK_ORDER


def test_live_replays_are_isolated_and_distinct():
    baseline = load_v2_3_baseline()
    store = ControlStore()
    historical_ids = {item.experiment_id for item in baseline.memory.experiments}
    for name in REPLAY_V22_TARGETS:
        record = run_replay(baseline, name, run_blind_replay, store=store)
        assert record.campaign_id == replay_campaign_id(name)
        assert record.campaign_id not in historical_ids
        assert record.campaign_type is CampaignType.REPLAY
        assert record.experiment_id not in historical_ids
        assert baseline.board.by_name()[name].already_run is True
        assert baseline.memory.get(name).experiment_id == name
        assert len(record.proposals.proposals) == 3
        assert record.comparison is not None
        assert record.comparison.v2_4_added_information
        payload = record.as_dict()
        assert "grey_loot" not in str(payload.get("replay_metadata"))
