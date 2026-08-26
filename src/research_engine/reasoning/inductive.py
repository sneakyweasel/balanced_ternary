"""True T(S) ⊆ S over legal_controls. Does not filter on is_terminal."""

from __future__ import annotations

from research_engine.attacks.result import AttackContext
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import State
from research_engine.reasoning.regions import contains, probe_states
from research_engine.reasoning.types import EvidenceState, InvariantCertificate, Region, RegionForm


def _working_phase(spec: ProblemSpec, context: AttackContext):
    phases = context.phases
    if phases:
        return phases[0]
    return spec.initial_phase()


def images_of(spec: ProblemSpec, state: State, context: AttackContext) -> tuple[State, ...]:
    phase = _working_phase(spec, context)
    src = spec.canonicalize(state)
    found: list[State] = []
    try:
        controls = spec.legal_controls(src, phase)
    except (TypeError, ValueError):
        return ()
    for control in controls:
        try:
            nxt = spec.canonicalize(spec.transition(src, control, phase))
        except (TypeError, ValueError):
            continue
        found.append(nxt)
    return tuple(found)


def seeds_included(region: Region, seeds: tuple[State, ...]) -> bool:
    return all(contains(region, seed) for seed in seeds)


def transition_leaks(
    spec: ProblemSpec,
    region: Region,
    context: AttackContext,
    extra: tuple[State, ...] = (),
) -> tuple[tuple[State, State], ...]:
    leaks: list[tuple[State, State]] = []
    for state in probe_states(region, extra):
        for nxt in images_of(spec, state, context):
            if not contains(region, nxt):
                leaks.append((state, nxt))
    return tuple(leaks)


def certify_invariant(
    spec: ProblemSpec,
    region: Region,
    context: AttackContext,
    *,
    observed: tuple[State, ...] = (),
    closure_complete: bool = False,
) -> InvariantCertificate:
    seed = spec.canonicalize(spec.initial_state)
    seeds = (seed,)
    included = seeds_included(region, seeds)
    leaks = transition_leaks(spec, region, context, extra=observed + seeds)
    closed = not leaks
    probe = probe_states(region, observed + seeds)
    target = str(getattr(spec, "name", "") or "")
    statement = f"T(S) ⊆ S for {region.form.value}"
    if not included:
        evidence = EvidenceState.UNKNOWN
        statement = "S0 is not contained in S"
    elif leaks:
        evidence = EvidenceState.INDUCTIVE_CANDIDATE
        statement = "T(S) leaks a probed image"
    elif region.form is RegionForm.FINITE_SET:
        members = tuple(region.parameters.get("states", ()))
        if closure_complete and closed:
            evidence = EvidenceState.FINITE_EXACT
            statement = f"complete finite closure of size {len(members)}; not a universal theorem"
        elif closed and len(members) <= 48:
            evidence = EvidenceState.INDUCTIVE_CERTIFIED
            statement = f"enumerated finite set of size {len(members)} is one-step closed"
        else:
            evidence = EvidenceState.INDUCTIVE_CANDIDATE
    elif region.form is RegionForm.INTERVAL:
        lo, hi = int(region.parameters["lo"]), int(region.parameters["hi"])
        if closed and (hi - lo) <= 256:
            evidence = EvidenceState.INDUCTIVE_CERTIFIED
            statement = f"enumerated interval [{lo},{hi}] is one-step closed"
        elif closed:
            evidence = EvidenceState.INDUCTIVE_CANDIDATE
        else:
            evidence = EvidenceState.INDUCTIVE_CANDIDATE
    elif region.form is RegionForm.SIGN_ORTHANT and closed:
        evidence = EvidenceState.INDUCTIVE_CERTIFIED
        statement = "sign orthant has no probed one-step leak; not a Z-theorem"
    elif region.form is RegionForm.MODULAR_CLASS and closed:
        evidence = EvidenceState.INDUCTIVE_CANDIDATE
        statement = "modular class has no probed leak; class is not exhausted"
    else:
        evidence = EvidenceState.UNKNOWN
    return InvariantCertificate(
        region=region,
        seeds=seeds,
        seeds_included=included,
        transition_closed=closed,
        evidence=evidence,
        counterexamples=tuple(f"{src}->{dst}" for src, dst in leaks[:8]),
        source_target=target,
        probe_size=len(probe),
        statement=statement,
    )
