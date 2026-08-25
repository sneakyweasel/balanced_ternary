"""Build a ``RegimeFingerprint`` from a spec, planner report, and probes."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from research_engine.attacks.result import AttackContext, AttackResult, AttackStatus
from research_engine.core.contribution import has_raw_contribution
from research_engine.core.observation import has_output, observe
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import CertificateKind, SearchScope
from research_engine.diagnosis.probes import is_integer_state, run_integer_probes
from research_engine.diagnosis.types import UNOBSERVED, RegimeFingerprint
from research_engine.planner.orchestrator import PlannerReport, SkipRecord


def _by_name(report: PlannerReport) -> dict[str, AttackResult]:
    return {item.name: item for item in report.results}


def _skipped(report: PlannerReport) -> dict[str, SkipRecord]:
    return {item.attack: item for item in report.skipped}


def _control_structure(spec: ProblemSpec, context: AttackContext) -> str:
    del context
    phase = spec.initial_phase()
    start = spec.canonicalize(spec.initial_state)
    try:
        controls = spec.legal_controls(start, phase)
    except (TypeError, ValueError):
        return UNOBSERVED
    count = len(controls)
    if count == 0:
        return "EMPTY"
    if count == 1:
        return "SINGLETON"
    return "BRANCHING"


def _transition_architecture(control: str) -> str:
    if control == "SINGLETON":
        return "DETERMINISTIC"
    if control == "BRANCHING":
        return "BRANCHING"
    if control == "EMPTY":
        return "EMPTY"
    return UNOBSERVED


def _state_space_type(spec: ProblemSpec) -> str:
    start = spec.canonicalize(spec.initial_state)
    if spec.dimension == 1 and is_integer_state(start):
        return "INTEGER_1D"
    if is_integer_state(start):
        return "INTEGER_VECTOR"
    return "OTHER"


def _observation_kind(spec: ProblemSpec) -> str:
    if not has_output(spec):
        return "NONE"
    start = spec.canonicalize(spec.initial_state)
    phase = spec.initial_phase()
    controls = spec.legal_controls(start, phase)
    if not controls:
        return "PRESENT"
    try:
        out = observe(spec, start, controls[0], phase)
    except (TypeError, ValueError):
        return "PRESENT"
    if is_integer_state(start) and out == start[0]:
        return "IDENTITY"
    return "COARSE"


def _attack_field(
    results: Mapping[str, AttackResult],
    skipped: Mapping[str, SkipRecord],
    name: str,
    *,
    supported: str,
    observation: str,
    refuted: str,
    inconclusive: str,
    inapplicable: str = "INAPPLICABLE",
) -> str:
    if name in skipped:
        reason = skipped[name].reason
        if "inapplicable" in reason.lower() or "needs" in reason.lower():
            return inapplicable
        return UNOBSERVED
    result = results.get(name)
    if result is None:
        return UNOBSERVED
    if result.status is AttackStatus.INAPPLICABLE:
        return inapplicable
    if result.status is AttackStatus.SUPPORTED:
        return supported
    if result.status is AttackStatus.OBSERVATION:
        return observation
    if result.status is AttackStatus.REFUTED:
        return refuted
    if result.status is AttackStatus.INCONCLUSIVE:
        return inconclusive
    return UNOBSERVED


def fingerprint_from_report(
    spec: ProblemSpec,
    report: PlannerReport,
    context: AttackContext | None = None,
    probes: Mapping[str, Any] | None = None,
) -> RegimeFingerprint:
    """Classify discovered structure. Does not read ``spec.name``."""
    ctx = context if context is not None else AttackContext()
    results = _by_name(report)
    skipped = _skipped(report)
    if probes is None:
        probes = run_integer_probes(spec, ctx)

    control = _control_structure(spec, ctx)
    state_type = _state_space_type(spec)
    observation = _observation_kind(spec)

    closure = results.get("closure")
    if closure is None:
        eventual = UNOBSERVED
        orbit = UNOBSERVED
        recurrence = UNOBSERVED
        cert = UNOBSERVED
        union_size = None
        complete = None
    else:
        complete = bool(closure.evidence.get("complete"))
        union_size = closure.evidence.get("union_size")
        if complete and closure.certificate_kind is CertificateKind.EXACT_CLOSURE:
            eventual = "FINITE_SEED_CLOSURE"
            orbit = "FINITE"
            recurrence = "CLOSED_COMPONENT"
            cert = CertificateKind.EXACT_CLOSURE.value
        elif closure.status is AttackStatus.INCONCLUSIVE or complete is False:
            eventual = "UNBOUNDED_SAMPLE"
            orbit = "INCOMPLETE"
            recurrence = UNOBSERVED
            cert = SearchScope.BOUNDED.value
        else:
            eventual = UNOBSERVED
            orbit = UNOBSERVED
            recurrence = UNOBSERVED
            cert = UNOBSERVED

    magnitude = probes.get("magnitude") if probes else None
    mag_regime = magnitude.get("regime") if isinstance(magnitude, dict) else UNOBSERVED
    functional = results.get("functional")
    if eventual == "FINITE_SEED_CLOSURE":
        contraction = "FINITE_CONTRACTING"
    elif mag_regime == "MIXED_MAGNITUDE":
        contraction = "MIXED_MAGNITUDE"
    elif mag_regime == "WINDOW_EXPANDING":
        contraction = "EXPANDING"
    elif mag_regime == "WINDOW_CONTRACTING":
        contraction = "WINDOW_CONTRACTING"
    elif functional is not None and functional.status is AttackStatus.REFUTED:
        contraction = "UNIVERSAL_DESCENT_REFUTED"
    else:
        contraction = UNOBSERVED

    if observation == "IDENTITY":
        compression = "IDENTITY_OBSERVATION"
    elif observation == "COARSE":
        compression = "COARSE_OBSERVATION"
    else:
        compression = "NONE"

    quotient = results.get("quotient")
    if "quotient" in skipped:
        quotient_field = "INAPPLICABLE" if "inapplicable" in skipped["quotient"].reason.lower() else UNOBSERVED
    elif quotient is None:
        quotient_field = UNOBSERVED
    else:
        qcount = quotient.evidence.get("quotient_count")
        rcount = quotient.evidence.get("reachable_state_count") or union_size
        if qcount is not None and rcount is not None and qcount < rcount:
            quotient_field = "NONTRIVIAL"
            compression = "NONTRIVIAL_QUOTIENT"
        elif qcount is not None and rcount is not None:
            quotient_field = "IDENTITY"
        elif quotient.status is AttackStatus.INAPPLICABLE:
            quotient_field = "INAPPLICABLE"
        else:
            quotient_field = "OBSERVED"

    separation = _attack_field(
        results,
        skipped,
        "separation",
        supported="SEPARATED",
        observation="BOUNDED",
        refuted="EQUIVALENT",
        inconclusive="BOUNDED",
    )
    if "separation" in results:
        sep = results["separation"]
        if sep.evidence.get("separated") is True:
            separation = "SEPARATED"
        elif sep.evidence.get("separated") is False and sep.scope is SearchScope.EXACT:
            separation = "EQUIVALENT"

    symmetry = _attack_field(
        results,
        skipped,
        "symmetry",
        supported="PRESENT",
        observation="OBSERVED",
        refuted="REFUTED",
        inconclusive="INCONCLUSIVE",
    )
    block = _attack_field(
        results,
        skipped,
        "block",
        supported="CLASSIFIED",
        observation="OBSERVED",
        refuted="REFUTED",
        inconclusive="INCONCLUSIVE",
    )
    reverse = _attack_field(
        results,
        skipped,
        "reverse",
        supported="EXACT",
        observation="BOUNDED",
        refuted="REFUTED",
        inconclusive="BOUNDED",
    )
    modular = _attack_field(
        results,
        skipped,
        "modular",
        supported="FORCING",
        observation="NONE",
        refuted="REFUTED",
        inconclusive="INCONCLUSIVE",
    )
    spectral = _attack_field(
        results,
        skipped,
        "spectral",
        supported="CLASSIFIED",
        observation="OBSERVED",
        refuted="REFUTED",
        inconclusive="INCONCLUSIVE",
    )
    factorization = _attack_field(
        results,
        skipped,
        "factorization",
        supported="VERIFIED",
        observation="OBSERVED",
        refuted="REFUTED",
        inconclusive="INCONCLUSIVE",
    )
    if not has_raw_contribution(spec) and factorization == UNOBSERVED:
        factorization = "INAPPLICABLE"

    residue = probes.get("residue") if probes else None
    if (
        modular == "INAPPLICABLE"
        and isinstance(residue, dict)
        and residue.get("restriction_count", 0) > 0
    ):
        modular = "SAMPLED_RESTRICTION"

    piecewise_structure = UNOBSERVED
    latent = UNOBSERVED
    if "piecewise_affine" in skipped:
        piecewise_structure = UNOBSERVED
        latent = UNOBSERVED
    else:
        piecewise = results.get("piecewise_affine")
        if piecewise is None:
            piecewise_structure = UNOBSERVED
            latent = UNOBSERVED
        else:
            kind = piecewise.evidence.get("census_kind")
            if kind == "PARAMETERIZED_CENSUS":
                piecewise_structure = "PARAMETERIZED"
                latent = "PARAMETERIZED"
            elif kind == "FINITE_CENSUS":
                piecewise_structure = "FINITE"
                latent = "FINITE"
            elif kind == "UNRESOLVED":
                piecewise_structure = "UNCERTAIN"
                latent = "UNCERTAIN"
            else:
                piecewise_structure = "NONE"
                latent = "NONE"

    domain_field = UNOBSERVED
    if "parameter_domain" in skipped:
        domain_field = UNOBSERVED
    else:
        domain = results.get("parameter_domain")
        if domain is None:
            domain_field = UNOBSERVED
        else:
            domains = domain.evidence.get("domains") or ()
            lean = domain.evidence.get("lean") or ""
            directions = {item.get("direction") for item in domains if isinstance(item, dict)}
            evidences = {item.get("evidence") for item in domains if isinstance(item, dict)}
            if lean or "LEAN_CERTIFIED" in evidences or "EXACT_PROVED" in evidences:
                domain_field = "EXACT"
            elif "EXACT" in directions:
                domain_field = "SAMPLE_SUPPORTED"
            elif directions:
                domain_field = "SAMPLE_SUPPORTED"
            else:
                domain_field = "UNCERTAIN"

    algebra_field = UNOBSERVED
    if "control_word" in skipped:
        algebra_field = UNOBSERVED
    else:
        composed = results.get("control_word")
        if composed is None:
            algebra_field = UNOBSERVED
        else:
            relations = composed.evidence.get("relations") or ()
            impossible = composed.evidence.get("impossible_words") or ()
            quotient = composed.evidence.get("quotient") or ()
            constraints = composed.evidence.get("constraints") or ()
            realizability = composed.evidence.get("realizability") or ()
            nontrivial_cycle = any(
                isinstance(item, dict)
                and item.get("kind") == "CYCLE_CONSTRAINT"
                and item.get("left") not in {0, None}
                for item in constraints
            )
            cycle_impossible = any(
                isinstance(item, dict) and item.get("cycle_status") == "IMPOSSIBLE"
                for item in realizability
            )
            if not relations:
                algebra_field = "UNCERTAIN"
            elif impossible or quotient or nontrivial_cycle or cycle_impossible:
                algebra_field = "EXPLOITABLE"
            else:
                algebra_field = "FORMALLY_COMPOSED"

    obstruction_field = UNOBSERVED
    if "control_obstruction" in skipped:
        obstruction_field = UNOBSERVED
    else:
        obstructed = results.get("control_obstruction")
        if obstructed is None:
            obstruction_field = UNOBSERVED
        else:
            certs = obstructed.evidence.get("certificates") or ()
            statuses = {item.get("status") for item in certs if isinstance(item, dict)}
            proved_statuses = {"PROVED", "LEAN_CERTIFIED", "SYMBOLICALLY_PROVED"}

            def _proved(scope: str) -> bool:
                return any(
                    isinstance(item, dict)
                    and item.get("scope") == scope
                    and item.get("status") in proved_statuses
                    for item in certs
                )

            if _proved("RECURSIVE_INVARIANT"):
                obstruction_field = "RECURSIVE_INVARIANT"
            elif _proved("SYMBOLIC_CLASS"):
                obstruction_field = "SYMBOLIC_CLASS"
            elif _proved("CLASS"):
                obstruction_field = "CLASS"
            elif _proved("WORD"):
                obstruction_field = "WORD"
            elif statuses:
                obstruction_field = "NONE"
            else:
                obstruction_field = "NONE"

    affine_control_type = UNOBSERVED
    if piecewise_structure in {"FINITE", "PARAMETERIZED"}:
        affine_control_type = "SCALAR"

    vector = results.get("vector_affine")
    if vector is not None and piecewise_structure in {UNOBSERVED, "NONE", "UNCERTAIN"}:
        kind = vector.evidence.get("census_kind")
        if kind == "PARAMETERIZED_CENSUS":
            piecewise_structure = "PARAMETERIZED"
            latent = "PARAMETERIZED"
            affine_control_type = "MATRIX_PARAMETERIZED"
        elif kind == "FINITE_CENSUS":
            piecewise_structure = "FINITE"
            latent = "FINITE"
            affine_control_type = "VECTOR"
        elif kind == "UNRESOLVED":
            piecewise_structure = "UNCERTAIN"
            latent = "UNCERTAIN"
        if domain_field == UNOBSERVED:
            domains = vector.evidence.get("domains") or ()
            directions = {item.get("direction") for item in domains if isinstance(item, dict)}
            evidences = {item.get("evidence") for item in domains if isinstance(item, dict)}
            if "LEAN_CERTIFIED" in evidences or "EXACT_PROVED" in evidences:
                domain_field = "EXACT"
            elif "EXACT" in directions and "COUNTEREXAMPLE_SURVIVED" in evidences:
                # Vector domains certified by falsify-window survival are exact
                # relative to the reconstructed family, not Lean theorems.
                domain_field = "EXACT"
            elif "EXACT" in directions or directions:
                domain_field = "SAMPLE_SUPPORTED"
        if algebra_field == UNOBSERVED:
            relations = vector.evidence.get("relations") or ()
            certs = vector.evidence.get("certificates") or ()
            if relations and certs:
                algebra_field = "EXPLOITABLE"
            elif relations:
                algebra_field = "FORMALLY_COMPOSED"
        if obstruction_field == UNOBSERVED:
            certs = vector.evidence.get("certificates") or ()
            proved_statuses = {"PROVED", "LEAN_CERTIFIED", "SYMBOLICALLY_PROVED"}

            def _vector_proved(scope: str) -> bool:
                return any(
                    isinstance(item, dict)
                    and item.get("scope") == scope
                    and item.get("status") in proved_statuses
                    for item in certs
                )

            if _vector_proved("SYMBOLIC_CLASS"):
                obstruction_field = "SYMBOLIC_CLASS"
            elif _vector_proved("CLASS"):
                obstruction_field = "CLASS"
            elif _vector_proved("WORD"):
                obstruction_field = "WORD"
            elif certs:
                obstruction_field = "NONE"

    return RegimeFingerprint(
        transition_architecture=_transition_architecture(control),
        state_space_type=state_type,
        control_structure=control,
        numerical_contraction=contraction,
        structural_compression=compression,
        eventual_region=eventual,
        orbit_behavior=orbit,
        recurrence=recurrence,
        quotient=quotient_field,
        separation=separation,
        symmetry=symmetry,
        block_structure=block,
        reverse_structure=reverse,
        modular_structure=modular,
        spectral_structure=spectral,
        factorization_structure=factorization,
        piecewise_affine_structure=piecewise_structure,
        latent_control=latent,
        parameter_domain=domain_field,
        latent_control_algebra=algebra_field,
        latent_control_obstruction=obstruction_field,
        affine_control_type=affine_control_type,
        certificate_strength=cert,
    )


def semantic_class(fingerprint: RegimeFingerprint) -> str:
    """Structural class label from populated fields, not the problem name."""
    parts = [
        fingerprint.state_space_type,
        fingerprint.control_structure,
        fingerprint.numerical_contraction,
        fingerprint.eventual_region,
    ]
    return "|".join(part for part in parts if part != UNOBSERVED) or "UNCLASSIFIED"
