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
    statuses["latent_piecewise_affine_control"] = CoverageStatus.NOT_TESTED.value
    statuses["parameter_domain_certification"] = CoverageStatus.NOT_TESTED.value
    statuses["control_word_composition"] = CoverageStatus.NOT_TESTED.value
    statuses["control_obstruction_calculus"] = CoverageStatus.NOT_TESTED.value
    statuses["symbolic_multi_step_obstruction"] = CoverageStatus.NOT_TESTED.value
    statuses["recursive_remainder_invariant"] = CoverageStatus.NOT_TESTED.value
    statuses["latent_vector_affine_control"] = CoverageStatus.NOT_TESTED.value

    if _ran(results, "piecewise_affine"):
        statuses["latent_piecewise_affine_control"] = CoverageStatus.EXERCISED.value
    elif _inapplicable(skipped, "piecewise_affine"):
        statuses["latent_piecewise_affine_control"] = CoverageStatus.INAPPLICABLE.value

    if _ran(results, "parameter_domain"):
        statuses["parameter_domain_certification"] = CoverageStatus.EXERCISED.value
        domains = results["parameter_domain"].evidence.get("domains") or ()
        maximal = False
        for item in domains:
            if not isinstance(item, dict):
                continue
            kind = (item.get("domain") or {}).get("kind")
            parts = (item.get("domain") or {}).get("parts") or ()
            if kind == "maximal_divisibility" or any(
                isinstance(part, dict) and part.get("kind") == "maximal_divisibility"
                for part in parts
            ):
                if item.get("direction") == "EXACT":
                    maximal = True
                    break
        census_kind = results.get("piecewise_affine")
        parameterized = (
            census_kind is not None
            and census_kind.evidence.get("census_kind") == "PARAMETERIZED_CENSUS"
        )
        if parameterized and maximal:
            statuses["valuation_dynamics"] = CoverageStatus.EXERCISED.value
    elif _inapplicable(skipped, "parameter_domain"):
        statuses["parameter_domain_certification"] = CoverageStatus.INAPPLICABLE.value

    if _ran(results, "control_word"):
        statuses["control_word_composition"] = CoverageStatus.EXERCISED.value
        constraints = results["control_word"].evidence.get("constraints") or ()
        if any(
            isinstance(item, dict) and item.get("kind") == "CYCLE_CONSTRAINT"
            for item in constraints
        ):
            statuses["cycle_obstruction"] = CoverageStatus.EXERCISED.value
    elif _inapplicable(skipped, "control_word"):
        statuses["control_word_composition"] = CoverageStatus.INAPPLICABLE.value

    if _ran(results, "control_obstruction"):
        statuses["control_obstruction_calculus"] = CoverageStatus.EXERCISED.value
        certs = results["control_obstruction"].evidence.get("certificates") or ()
        if any(
            isinstance(item, dict)
            and item.get("kind") in {
                "divisibility",
                "gcd",
                "modular",
                "bound",
                "valuation",
                "invariant",
            }
            and item.get("status") in {"PROVED", "LEAN_CERTIFIED", "SYMBOLICALLY_PROVED"}
            for item in certs
        ):
            statuses["cycle_obstruction"] = CoverageStatus.EXERCISED.value
        if any(
            isinstance(item, dict)
            and item.get("scope") == "SYMBOLIC_CLASS"
            and item.get("status") in {"PROVED", "LEAN_CERTIFIED", "SYMBOLICALLY_PROVED"}
            for item in certs
        ):
            statuses["symbolic_multi_step_obstruction"] = CoverageStatus.EXERCISED.value
        if any(
            isinstance(item, dict)
            and item.get("scope") == "RECURSIVE_INVARIANT"
            and item.get("status") in {"PROVED", "LEAN_CERTIFIED", "SYMBOLICALLY_PROVED"}
            for item in certs
        ):
            statuses["recursive_remainder_invariant"] = CoverageStatus.EXERCISED.value
    elif _inapplicable(skipped, "control_obstruction"):
        statuses["control_obstruction_calculus"] = CoverageStatus.INAPPLICABLE.value
        statuses["symbolic_multi_step_obstruction"] = CoverageStatus.INAPPLICABLE.value
        statuses["recursive_remainder_invariant"] = CoverageStatus.INAPPLICABLE.value

    if _ran(results, "vector_affine"):
        statuses["latent_vector_affine_control"] = CoverageStatus.EXERCISED.value
        vector = results["vector_affine"]
        domains = vector.evidence.get("domains") or ()
        if any(isinstance(item, dict) and item.get("direction") in {"EXACT", "SUFFICIENT_ONLY", "NECESSARY_ONLY"} for item in domains):
            statuses["parameter_domain_certification"] = CoverageStatus.EXERCISED.value
        if vector.evidence.get("relations"):
            statuses["control_word_composition"] = CoverageStatus.EXERCISED.value
            statuses["cycle_obstruction"] = CoverageStatus.EXERCISED.value
        certs = vector.evidence.get("certificates") or ()
        if any(
            isinstance(item, dict)
            and item.get("status") in {"PROVED", "LEAN_CERTIFIED", "SYMBOLICALLY_PROVED"}
            for item in certs
        ):
            statuses["control_obstruction_calculus"] = CoverageStatus.EXERCISED.value
        if any(
            isinstance(item, dict)
            and (item.get("domain") or {}).get("kind") == "valuation"
            for item in domains
        ):
            statuses["valuation_dynamics"] = CoverageStatus.EXERCISED.value
    elif _inapplicable(skipped, "vector_affine"):
        statuses["latent_vector_affine_control"] = CoverageStatus.INAPPLICABLE.value

    if (
        fingerprint.control_structure == "SINGLETON"
        and fingerprint.numerical_contraction == "MIXED_MAGNITUDE"
        and fingerprint.eventual_region == "UNBOUNDED_SAMPLE"
        and statuses["valuation_dynamics"] != CoverageStatus.EXERCISED.value
    ):
        statuses["valuation_dynamics"] = CoverageStatus.NOT_TESTED.value

    return CapabilityCoverage(statuses=statuses)
