"""Campaign facade. Scout material is not imported here."""

from research.matthews_prize_mod3_avoider.planner import (
    plan_map,
    plan_map_session,
    plan_strategy,
)
from research.matthews_prize_mod3_avoider.runner import CampaignReport, run_campaign
from research.matthews_prize_mod3_avoider.spec import map_spec

__all__ = [
    "CampaignReport",
    "map_spec",
    "plan_map",
    "plan_map_session",
    "plan_strategy",
    "run_campaign",
]
