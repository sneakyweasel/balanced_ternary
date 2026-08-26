"""Generic inductive/ranking reasoning for Research Engine v2.3 Phase 2."""

from research_engine.reasoning.analyze import analyze, hypotheses_from_report
from research_engine.reasoning.cegis import observe_states, synthesize_invariant
from research_engine.reasoning.discipline import (
    clamp_universal,
    finite_exact_is_not_universal,
    from_closure,
    live_hypothesis_unpromoted,
)
from research_engine.reasoning.inductive import certify_invariant, images_of, transition_leaks
from research_engine.reasoning.ranking import synthesize_ranking
from research_engine.reasoning.types import (
    ENGINE_REASONING_VERSION,
    EvidenceState,
    InvariantCertificate,
    RankingCertificate,
    ReasoningReport,
    Region,
    RegionForm,
)

__all__ = [
    "ENGINE_REASONING_VERSION",
    "EvidenceState",
    "InvariantCertificate",
    "RankingCertificate",
    "ReasoningReport",
    "Region",
    "RegionForm",
    "analyze",
    "certify_invariant",
    "clamp_universal",
    "finite_exact_is_not_universal",
    "from_closure",
    "hypotheses_from_report",
    "images_of",
    "live_hypothesis_unpromoted",
    "observe_states",
    "synthesize_invariant",
    "synthesize_ranking",
    "transition_leaks",
]
