"""EXISTS_PATH ≠ ALL_PATHS. A window certificate is not a Z-theorem."""

from __future__ import annotations

from research_engine.core.semantics import ClaimKind
from research_engine.planner.hypothesis import Hypothesis, HypothesisStatus
from research_engine.quantifiers.types import PathStatus, QuantifierReport


def no_path_found_is_not_nonexistence(report: QuantifierReport) -> bool:
    claim = report.claim("existential_cycle")
    if claim is None or claim.status is not PathStatus.NO_PATH_FOUND:
        return True
    blob = f"{claim.statement} {claim.status.value}".upper()
    if claim.status is PathStatus.REFUTED:
        return False
    if "NOT A NONEXISTENCE" in blob:
        return True
    return "NO LEGAL PATH EXISTS" not in blob


def existential_cycle_is_not_all_paths_cycle(report: QuantifierReport) -> bool:
    exists = report.claim("existential_cycle")
    all_paths = report.claim("all_paths_cycle")
    if exists is None or exists.status is not PathStatus.EXISTENTIAL_WITNESS:
        return True
    if all_paths is None:
        return False
    if all_paths.status is PathStatus.CERTIFIED_ON_WINDOW:
        return False
    if all_paths.status is PathStatus.EXISTENTIAL_WITNESS:
        return False
    return all_paths.status is PathStatus.UNKNOWN


def certified_on_window_is_not_z_theorem(report: QuantifierReport) -> bool:
    for claim in report.claims:
        if claim.status is PathStatus.CERTIFIED_ON_WINDOW:
            blob = claim.statement.upper().replace("NOT A Z-THEOREM", "")
            if "UNIVERSAL_THEOREM" in blob:
                return False
    return True


def truncation_is_unknown_not_refuted(report: QuantifierReport) -> bool:
    for claim in report.claims:
        blob = claim.statement.lower()
        if "truncat" in blob or "search bound" in blob:
            if claim.status is PathStatus.REFUTED:
                return False
            if claim.status is not PathStatus.UNKNOWN:
                return False
    return True


def live_hypothesis_unpromoted(hyp: Hypothesis) -> bool:
    return hyp.kind is ClaimKind.LIVE and hyp.status is HypothesisStatus.OPEN
