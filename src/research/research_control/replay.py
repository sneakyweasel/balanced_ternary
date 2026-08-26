"""Blind v2.2 replay runners. Historical yield is not an input."""

from __future__ import annotations

from research.skolem_order2_known_zero.planner import plan_map_session as plan_skolem_order2
from research.skolem_order2_known_zero.spec import map_spec as spec_skolem_order2
from research.switching_affine_z2_origin.planner import plan_map_session as plan_switching
from research.switching_affine_z2_origin.spec import map_spec as spec_switching
from research_engine.control.replay import replay_campaign_id
from research_engine.control.types import REPLAY_V22_TARGETS
from research_engine.memory.ingest import experiment_from_session
from research_engine.memory.types import MemoryExperiment

_RUNNERS = {
    "skolem_order2_known_zero": (spec_skolem_order2, plan_skolem_order2, "companion_shift"),
    "switching_affine_z2_origin": (spec_switching, plan_switching, "switching_affine"),
}


def run_blind_replay(source_target_id: str) -> MemoryExperiment:
    """Execute frozen v2.3 attacks with empty memory. No historical loot."""

    if source_target_id not in _RUNNERS:
        raise KeyError(f"no replay runner for {source_target_id}; Phase-0 set is {REPLAY_V22_TARGETS}")
    spec_fn, plan_fn, family = _RUNNERS[source_target_id]
    spec = spec_fn()
    session = plan_fn(spec, record=True, memory=None)
    return experiment_from_session(
        session,
        spec,
        spec.attack_context(),
        experiment_id=replay_campaign_id(source_target_id),
        target_family=family,
        engine_version="0.2.7",
        experiment_date="2026-08-26",
    )
