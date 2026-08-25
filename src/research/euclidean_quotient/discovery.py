"""Bounded probes for Euclidean remainder dynamics. Not planner hints."""

from __future__ import annotations

from research.euclidean_quotient.spec import EuclideanSpec, euclidean_spec, euclidean_step
from research_engine.attacks.separation import separate_states
from research_engine.behavior.profile import ComplexityProfile, closure_status_label
from research_engine.core.semantics import CertificateKind, State


def orbit_of(start: State, *, max_steps: int = 32) -> tuple[State, ...]:
    if isinstance(max_steps, bool) or not isinstance(max_steps, int) or max_steps < 1:
        raise ValueError(f"max_steps must be a positive int, got {max_steps!r}")
    seen: list[State] = []
    current = (int(start[0]), int(start[1]))
    for _ in range(max_steps):
        if current in seen:
            break
        seen.append(current)
        current = euclidean_step(current)
    return tuple(seen)


def terminates(start: State, *, max_steps: int = 64) -> bool:
    orbit = orbit_of(start, max_steps=max_steps)
    return bool(orbit) and orbit[-1][1] == 0


def seed_complexity_profile(spec: EuclideanSpec | None = None) -> ComplexityProfile:
    target = spec if spec is not None else euclidean_spec()
    prefix = orbit_of(target.initial_state, max_steps=target.state_cap)
    nxt = euclidean_step(target.initial_state)
    sep = separate_states(target, target.initial_state, nxt)
    depth = sep.witness_length if sep.separated else 0
    complete = bool(prefix) and prefix[-1][1] == 0
    return ComplexityProfile(
        control_count=1,
        reachable_state_count=len(prefix) if complete else None,
        behavioral_state_count=len(prefix) if complete else None,
        max_separation_depth=depth,
        closure_status=closure_status_label(
            complete=complete,
            certificate_kind=CertificateKind.EXACT_CLOSURE if complete else None,
        ),
    )
