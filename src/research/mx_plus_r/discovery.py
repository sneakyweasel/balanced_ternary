"""Bounded probes for accelerated (mx+r). Not planner hints."""

from __future__ import annotations

from research.mx_plus_r.spec import DEFAULT_START, MxPlusRSpec, mx_plus_r_spec, mx_plus_r_step
from research_engine.attacks.separation import separate_states
from research_engine.behavior.profile import ComplexityProfile, closure_status_label
from research_engine.core.semantics import CertificateKind

PROBE_LIMIT = 80
ODD_WINDOW = tuple(n for n in range(1, PROBE_LIMIT + 1) if n % 2 == 1)


def orbit_of(n: int, m: int, r: int, *, max_steps: int = 32) -> tuple[int, ...]:
    if isinstance(max_steps, bool) or not isinstance(max_steps, int) or max_steps < 1:
        raise ValueError(f"max_steps must be a positive int, got {max_steps!r}")
    seen: list[int] = []
    current = n
    for _ in range(max_steps):
        if current in seen:
            break
        seen.append(current)
        current = mx_plus_r_step(current, m, r)
    return tuple(seen)


def magnitude_census(m: int, r: int, window: tuple[int, ...] = ODD_WINDOW) -> dict[str, int]:
    drops = 0
    growths = 0
    equals = 0
    for n in window:
        image = mx_plus_r_step(n, m, r)
        if image < n:
            drops += 1
        elif image > n:
            growths += 1
        else:
            equals += 1
    return {"drops": drops, "growths": growths, "equals": equals, "sampled": len(window)}


def recurrent_seeds(m: int, r: int, window: tuple[int, ...] = ODD_WINDOW, max_steps: int = 40) -> tuple[int, ...]:
    found: list[int] = []
    for n in window:
        orbit = orbit_of(n, m, r, max_steps=max_steps)
        if orbit and orbit[-1] in orbit[:-1]:
            found.append(n)
    return tuple(found)


def seed_complexity_profile(spec: MxPlusRSpec | None = None) -> ComplexityProfile:
    target = spec if spec is not None else mx_plus_r_spec(3, 1, start=DEFAULT_START)
    prefix = orbit_of(target.start, target.m, target.r, max_steps=target.state_cap)
    nxt = mx_plus_r_step(target.start, target.m, target.r)
    sep = separate_states(target, (target.start,), (nxt,))
    depth = sep.witness_length if sep.separated else 0
    complete = len(prefix) < target.state_cap and prefix[-1] in prefix[:-1]
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
