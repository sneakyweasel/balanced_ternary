"""Which generic capabilities an experiment actually exercised."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from research_engine.attacks.result import AttackResult
from research_engine.diagnosis.types import (
    CAPABILITIES,
    UNOBSERVED,
    CapabilityCoverage,
    CoverageStatus,
    RegimeFingerprint,
)
from research_engine.planner.orchestrator import PlannerReport, SkipRecord


def _skip_map(report: PlannerReport) -> dict[str, SkipRecord]:
    return {item.attack: item for item in report.skipped}


def _result_map(report: PlannerReport) -> dict[str, AttackResult]:
    return {item.name: item for item in report.results}


def _ran(results: Mapping[str, AttackResult], name: str) -> bool:
    return name in results


def _inapplicable(skipped: Mapping[str, SkipRecord], name: str) -> bool:
    record = skipped.get(name)
    if record is None:
        return False
    return "inapplicable" in record.reason.lower() or "needs" in record.reason.lower()


def capability_coverage(
    fingerprint: RegimeFingerprint,
    report: PlannerReport,
    probes: Mapping[str, Any] | None = None,
) -> CapabilityCoverage:
    results = _result_map(report)
    skipped = _skip_map(report)
    probes = probes or {}
    magnitude = probes.get("magnitude") if isinstance(probes, dict) else None
    statuses: dict[str, str] = {name: CoverageStatus.NOT_TESTED.value for name in CAPABILITIES}

    if fingerprint.eventual_region == "FINITE_SEED_CLOSURE":
        statuses["finite_closure"] = CoverageStatus.EXERCISED.value
    elif fingerprint.eventual_region == "UNBOUNDED_SAMPLE":
        statuses["finite_closure"] = CoverageStatus.EXERCISED.value
        statuses["infinite_reachable_trajectories"] = CoverageStatus.EXERCISED.value

    if fingerprint.numerical_contraction not in {UNOBSERVED}:
        statuses["numerical_contraction"] = CoverageStatus.EXERCISED.value
    if fingerprint.numerical_contraction in {"EXPANDING", "MIXED_MAGNITUDE", "UNIVERSAL_DESCENT_REFUTED"}:
        statuses["growth"] = CoverageStatus.EXERCISED.value
    elif isinstance(magnitude, dict) and magnitude.get("growths", 0) > 0:
        statuses["growth"] = CoverageStatus.EXERCISED.value

    if fingerprint.structural_compression in {"COARSE_OBSERVATION", "NONTRIVIAL_QUOTIENT"}:
        statuses["non_numerical_compression"] = CoverageStatus.EXERCISED.value

    if fingerprint.control_structure == "BRANCHING":
        statuses["branching_controls"] = CoverageStatus.EXERCISED.value
        statuses["nontrivial_control_alphabet"] = CoverageStatus.EXERCISED.value
    elif fingerprint.control_structure == "SINGLETON":
        statuses["branching_controls"] = CoverageStatus.INAPPLICABLE.value
        statuses["nontrivial_control_alphabet"] = CoverageStatus.INAPPLICABLE.value

    if _ran(results, "modular"):
        statuses["modular_restrictions"] = CoverageStatus.EXERCISED.value
    elif fingerprint.modular_structure == "SAMPLED_RESTRICTION":
        statuses["modular_restrictions"] = CoverageStatus.EXERCISED.value
    elif _inapplicable(skipped, "modular"):
        statuses["modular_restrictions"] = CoverageStatus.INAPPLICABLE.value

    if _ran(results, "quotient"):
        statuses["behavioral_quotient"] = CoverageStatus.EXERCISED.value
    elif _inapplicable(skipped, "quotient"):
        statuses["behavioral_quotient"] = CoverageStatus.INAPPLICABLE.value

    if _ran(results, "separation"):
        statuses["separation"] = CoverageStatus.EXERCISED.value
    elif _inapplicable(skipped, "separation"):
        statuses["separation"] = CoverageStatus.INAPPLICABLE.value

    if _ran(results, "symmetry"):
        statuses["symmetry"] = CoverageStatus.EXERCISED.value
    elif _inapplicable(skipped, "symmetry"):
        statuses["symmetry"] = CoverageStatus.INAPPLICABLE.value

    if _ran(results, "block"):
        statuses["block_dynamics"] = CoverageStatus.EXERCISED.value
    elif _inapplicable(skipped, "block"):
        statuses["block_dynamics"] = CoverageStatus.INAPPLICABLE.value

    if _ran(results, "reverse"):
        statuses["reverse_preimage_structure"] = CoverageStatus.EXERCISED.value
    elif _inapplicable(skipped, "reverse"):
        statuses["reverse_preimage_structure"] = CoverageStatus.INAPPLICABLE.value

    statuses["symbolic_control"] = CoverageStatus.NOT_TESTED.value
    statuses["cycle_obstruction"] = CoverageStatus.NOT_TESTED.value
    statuses["valuation_dynamics"] = CoverageStatus.NOT_TESTED.value
    statuses["recursive_semantics"] = CoverageStatus.NOT_TESTED.value

    if (
        fingerprint.control_structure == "SINGLETON"
        and fingerprint.numerical_contraction == "MIXED_MAGNITUDE"
        and fingerprint.eventual_region == "UNBOUNDED_SAMPLE"
    ):
        statuses["valuation_dynamics"] = CoverageStatus.NOT_TESTED.value

    return CapabilityCoverage(statuses=statuses)
