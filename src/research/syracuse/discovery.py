"""Bounded probes for the accelerated odd-only map. Not planner hints."""

from __future__ import annotations

from research.syracuse.spec import DEFAULT_START, syracuse_spec, syracuse_step
from research_engine.attacks.separation import separate_states
from research_engine.behavior.profile import ComplexityProfile, closure_status_label
from research_engine.core.semantics import CertificateKind


PROBE_LIMIT = 40
ODD_WINDOW = tuple(n for n in range(1, 41) if n % 2 == 1)


def orbit_of(n: int, *, max_steps: int = 32) -> tuple[int, ...]:
    if isinstance(max_steps, bool) or not isinstance(max_steps, int) or max_steps < 1:
        raise ValueError(f"max_steps must be a positive int, got {max_steps!r}")
    seen: list[int] = []
    current = n
    for _ in range(max_steps):
        if current in seen:
            break
        seen.append(current)
        current = syracuse_step(current)
    return tuple(seen)


def lyapunov_n_witness() -> int:
    """Smallest positive odd ``n`` where ``V(n)=n`` does not strictly decrease."""
    for n in ODD_WINDOW:
        if syracuse_step(n) >= n:
            return n
    raise AssertionError("no Lyapunov witness in the probe window")


def interval_leak_witness(bound: int = 15) -> tuple[int, int] | None:
    """A one-step image that leaves the odd integers in ``[1, bound]``."""
    region = {n for n in range(1, bound + 1) if n % 2 == 1}
    for n in region:
        image = syracuse_step(n)
        if image not in region:
            return (n, image)
    return None


def magnitude_drop_counterexample(min_n: int = 3) -> int | None:
    """Smallest odd ``n >= min_n`` with ``S(n) >= n``."""
    for n in ODD_WINDOW:
        if n < min_n:
            continue
        if syracuse_step(n) >= n:
            return n
    return None


def idempotent_counterexample() -> int | None:
    for n in ODD_WINDOW:
        if syracuse_step(syracuse_step(n)) != syracuse_step(n):
            return n
    return None


def distinct_orbits_prefix(left: int = 3, right: int = 5, steps: int = 8) -> tuple[int, int]:
    a = set(orbit_of(left, max_steps=steps))
    b = set(orbit_of(right, max_steps=steps))
    if a.isdisjoint(b):
        return left, right
    return 7, 15


def seed_complexity_profile(start: int = DEFAULT_START) -> ComplexityProfile:
    spec = syracuse_spec(start=start)
    prefix = orbit_of(start, max_steps=spec.state_cap)
    nxt = syracuse_step(start)
    sep = separate_states(spec, (start,), (nxt,))
    depth = sep.witness_length if sep.separated else 0
    complete = len(prefix) < spec.state_cap and prefix[-1] in prefix[:-1]
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
