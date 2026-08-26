"""Path quantifiers over legal_controls as a relation. Research Engine v2.3 Phase 4."""

from research_engine.quantifiers.analyze import analyze, hypotheses_from_report
from research_engine.quantifiers.discipline import (
    certified_on_window_is_not_z_theorem,
    existential_cycle_is_not_all_paths_cycle,
    live_hypothesis_unpromoted,
    no_path_found_is_not_nonexistence,
    truncation_is_unknown_not_refuted,
)
from research_engine.quantifiers.probes import existential_cycle_witness, universal_termination_on_seeds
from research_engine.quantifiers.relation import relation_edges
from research_engine.quantifiers.types import (
    ENGINE_QUANTIFIER_VERSION,
    PathClaim,
    PathQuantifier,
    PathStatus,
    QuantifierReport,
    RelationEdge,
)

__all__ = [
    "ENGINE_QUANTIFIER_VERSION",
    "PathClaim",
    "PathQuantifier",
    "PathStatus",
    "QuantifierReport",
    "RelationEdge",
    "analyze",
    "certified_on_window_is_not_z_theorem",
    "existential_cycle_is_not_all_paths_cycle",
    "existential_cycle_witness",
    "hypotheses_from_report",
    "live_hypothesis_unpromoted",
    "no_path_found_is_not_nonexistence",
    "relation_edges",
    "truncation_is_unknown_not_refuted",
    "universal_termination_on_seeds",
]
