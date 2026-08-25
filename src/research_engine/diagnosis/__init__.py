"""Generic diagnosis: fingerprints, families, coverage, and research decisions."""

from research_engine.diagnosis.compare import compare_fingerprints, core_match
from research_engine.diagnosis.corpus import ResearchCorpus
from research_engine.diagnosis.coverage import capability_coverage
from research_engine.diagnosis.decision import decide_research
from research_engine.diagnosis.family import family_id_of, family_status_for
from research_engine.diagnosis.fingerprint import fingerprint_from_report, semantic_class
from research_engine.diagnosis.loop import DiagnosisReport, ResearchLoop, ResearchSession, diagnose, record_from_session
from research_engine.diagnosis.probes import magnitude_census, residue_census, run_integer_probes
from research_engine.diagnosis.selection import score_candidate
from research_engine.diagnosis.types import (
    CAPABILITIES,
    CORE_DIMENSIONS,
    CandidateSketch,
    CapabilityCoverage,
    CoverageStatus,
    DeltaLevel,
    ExperimentRecord,
    FamilyStatus,
    RegimeFingerprint,
    RegimeSimilarity,
    ResearchDecision,
    SelectionReport,
    StructuralDelta,
)

__all__ = [
    "CAPABILITIES",
    "CORE_DIMENSIONS",
    "CandidateSketch",
    "CapabilityCoverage",
    "CoverageStatus",
    "DeltaLevel",
    "DiagnosisReport",
    "ExperimentRecord",
    "FamilyStatus",
    "RegimeFingerprint",
    "RegimeSimilarity",
    "ResearchCorpus",
    "ResearchDecision",
    "ResearchLoop",
    "ResearchSession",
    "SelectionReport",
    "StructuralDelta",
    "capability_coverage",
    "compare_fingerprints",
    "core_match",
    "decide_research",
    "diagnose",
    "family_id_of",
    "family_status_for",
    "fingerprint_from_report",
    "magnitude_census",
    "record_from_session",
    "record_from_session",
    "residue_census",
    "run_integer_probes",
    "score_candidate",
    "semantic_class",
]
