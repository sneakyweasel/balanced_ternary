"""Bounded counterexample-guided region refinement. Not a general CEGIS solver."""

from __future__ import annotations

from research_engine.attacks.envelope import compute_exact_reachable
from research_engine.attacks.result import AttackContext
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import State
from research_engine.reasoning.inductive import certify_invariant, images_of, transition_leaks
from research_engine.reasoning.regions import (
    FINITE_SET_CAP,
    candidates_from_sample,
    enlarge_finite,
)
from research_engine.reasoning.types import EvidenceState, InvariantCertificate, RegionForm

CEGIS_ROUNDS = 4


def observe_states(spec: ProblemSpec, context: AttackContext) -> tuple[tuple[State, ...], bool]:
    if context.candidate_region:
        return tuple(sorted(context.candidate_region)), False
    closure = compute_exact_reachable(spec, context)
    reached = tuple(sorted(closure.reachable)) if closure.reachable else ()
    if reached:
        return reached, bool(closure.complete)
    seed = spec.canonicalize(spec.initial_state)
    orbit = [seed]
    seen = {seed}
    state = seed
    steps = context.max_steps if context.max_steps is not None else 16
    for _ in range(max(0, steps)):
        images = images_of(spec, state, context)
        if not images:
            break
        nxt = images[0]
        if nxt in seen:
            orbit.append(nxt)
            break
        seen.add(nxt)
        orbit.append(nxt)
        state = nxt
    return tuple(orbit), False


def _is_universe(region) -> bool:
    if region.form is RegionForm.INTERVAL:
        lo, hi = int(region.parameters["lo"]), int(region.parameters["hi"])
        return hi - lo > 10_000
    return False


def synthesize_invariant(spec: ProblemSpec, context: AttackContext) -> tuple[InvariantCertificate | None, tuple[State, ...], bool]:
    observed, complete = observe_states(spec, context)
    dim = int(getattr(spec, "dimension", 1) or 1)
    if observed and dim < len(observed[0]):
        dim = len(observed[0])
    best: InvariantCertificate | None = None
    for region in candidates_from_sample(observed, dimension=dim, complete=complete):
        if _is_universe(region):
            continue
        current = region
        cert = None
        for _ in range(CEGIS_ROUNDS):
            cert = certify_invariant(
                spec,
                current,
                context,
                observed=observed,
                closure_complete=complete,
            )
            if cert.transition_closed and cert.seeds_included:
                break
            leaks = transition_leaks(spec, current, context, extra=observed)
            if not leaks:
                break
            if current.form is RegionForm.FINITE_SET:
                extras = [dst for _, dst in leaks]
                enlarged = enlarge_finite(current, extras)
                if len(enlarged.parameters.get("states", ())) > FINITE_SET_CAP:
                    cert = InvariantCertificate(
                        region=current,
                        seeds=cert.seeds,
                        seeds_included=cert.seeds_included,
                        transition_closed=False,
                        evidence=EvidenceState.UNKNOWN,
                        counterexamples=cert.counterexamples,
                        source_target=cert.source_target,
                        probe_size=cert.probe_size,
                        statement="finite-set refinement exceeded cap",
                    )
                    break
                current = enlarged
                continue
            break
        if cert is None:
            continue
        if _preference(cert) > _preference(best):
            best = cert
    return best, observed, complete


def _preference(certificate: InvariantCertificate | None) -> int:
    if certificate is None:
        return -1
    evidence = {
        EvidenceState.INDUCTIVE_CERTIFIED: 30,
        EvidenceState.FINITE_EXACT: 20,
        EvidenceState.INDUCTIVE_CANDIDATE: 10,
    }.get(certificate.evidence, 0)
    form = {
        RegionForm.SIGN_ORTHANT: 3,
        RegionForm.INTERVAL: 2,
        RegionForm.MODULAR_CLASS: 1,
        RegionForm.FINITE_SET: 0,
    }.get(certificate.region.form, 0)
    return evidence + form
