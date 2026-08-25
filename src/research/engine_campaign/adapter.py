"""Campaign facade: corpus seed and sequential ResearchLoop runner."""

from research.engine_campaign.candidates import score_pool, spec_for_selection
from research.engine_campaign.corpus import seed_baseline_corpus
from research.engine_campaign.runner import CampaignReport, run_campaign

__all__ = [
    "CampaignReport",
    "run_campaign",
    "score_pool",
    "seed_baseline_corpus",
    "spec_for_selection",
]
