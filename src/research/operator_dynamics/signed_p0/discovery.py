"""Bounded probes for ``N ∘ I_0 ∘ D``. Not planner hints."""

from __future__ import annotations

from bt.calculus.derivative import D
from bt.calculus.integral import I, P_zero
from research.operator_dynamics.signed_p0.spec import (
    BOX_BOUND,
    DEFAULT_START,
    integer_sign,
    lsd_int,
    signed_p0,
    signed_p0_spec,
)
from research_engine.attacks.envelope import (
    compare_envelope_to_reachable,
    envelope_from_interval,
    reachable_from_ints,
)
from research_engine.attacks.separation import separate_states
from research_engine.behavior.profile import ComplexityProfile, closure_status_label
from research_engine.core.semantics import CertificateKind


PROBE_LIMIT = 40
WINDOW = 12


def fab_collapses(a: int, b: int, n: int) -> bool:
    """``I_a(D(I_b(n)))`` is exactly ``I_a(n)``."""
    return I(a, D(I(b, n))) == I(a, n)


def fab_is_section_on_probes(limit: int = PROBE_LIMIT) -> bool:
    if isinstance(limit, bool) or not isinstance(limit, int) or limit < 0:
        raise ValueError(f"limit must be a nonnegative int, got {limit!r}")
    for a in (-1, 0, 1):
        for b in (-1, 0, 1):
            for n in range(-limit, limit + 1):
                if not fab_collapses(a, b, n):
                    return False
    return True


def orbit_of(n: int, *, max_steps: int = 8) -> tuple[int, ...]:
    if isinstance(max_steps, bool) or not isinstance(max_steps, int) or max_steps < 1:
        raise ValueError(f"max_steps must be a positive int, got {max_steps!r}")
    seen: list[int] = []
    current = n
    for _ in range(max_steps):
        if current in seen:
            break
        seen.append(current)
        current = signed_p0(current)
    return tuple(seen)


def f2_equals_p0(n: int) -> bool:
    return signed_p0(signed_p0(n)) == P_zero(n)


def f2_p0_counterexample(limit: int = PROBE_LIMIT) -> int | None:
    if isinstance(limit, bool) or not isinstance(limit, int) or limit < 0:
        raise ValueError(f"limit must be a nonnegative int, got {limit!r}")
    for n in range(-limit, limit + 1):
        if not f2_equals_p0(n):
            return n
    return None


def lyapunov_n_witness() -> int:
    """Smallest ``n`` where ``V(n)=n`` does not strictly decrease."""
    for n in range(-12, 13):
        if signed_p0(n) >= n:
            return n
    raise AssertionError("no Lyapunov witness in the probe window")


def interval_leak_witness(bound: int = BOX_BOUND) -> tuple[int, int]:
    """A one-step image that leaves ``[-bound, bound]``."""
    if isinstance(bound, bool) or not isinstance(bound, int) or bound < 0:
        raise ValueError(f"bound must be a nonnegative int, got {bound!r}")
    for n in range(-bound, bound + 1):
        image = signed_p0(n)
        if abs(image) > bound:
            return n, image
    raise AssertionError(f"no interval leak inside [{-bound}, {bound}]")


def distinct_orbits_witness() -> tuple[int, int]:
    """Two seeds whose orbits are disjoint and unbounded as a family."""
    return 3, 6


def sign_stream(n: int, length: int = 6) -> tuple[int, ...]:
    if isinstance(length, bool) or not isinstance(length, int) or length < 0:
        raise ValueError(f"length must be a nonnegative int, got {length!r}")
    current = n
    out: list[int] = []
    for _ in range(length):
        out.append(integer_sign(current))
        current = signed_p0(current)
    return tuple(out)


def envelope_versus_orbit(
    start: int = DEFAULT_START,
    bound: int = BOX_BOUND,
):
    orbit = orbit_of(start)
    envelope = envelope_from_interval(-bound, bound, as_states=True)
    reached = reachable_from_ints(orbit, seed=start, as_states=True)
    return compare_envelope_to_reachable(envelope, reached)


def window_orbits(limit: int = WINDOW) -> dict[int, tuple[int, ...]]:
    if isinstance(limit, bool) or not isinstance(limit, int) or limit < 0:
        raise ValueError(f"limit must be a nonnegative int, got {limit!r}")
    return {n: orbit_of(n) for n in range(-limit, limit + 1)}


def max_orbit_size(limit: int = WINDOW) -> int:
    return max(len(orbit) for orbit in window_orbits(limit).values())


def seed_complexity_profile(start: int = DEFAULT_START) -> ComplexityProfile:
    spec = signed_p0_spec(start=start)
    orbit = orbit_of(start)
    comparison = envelope_versus_orbit(start)
    sep = separate_states(spec, (start,), (signed_p0(start),))
    positives = [n for n in orbit if n > 0]
    merged = 0
    if len(positives) >= 2:
        merge = separate_states(spec, (positives[0],), (positives[1],))
        if merge.separated is False:
            merged = 1
    behavioral = len(orbit) - merged
    depth = sep.witness_length if sep.separated else None
    return ComplexityProfile(
        control_count=1,
        invariant_state_count=len(comparison.holes) + len(orbit)
        if comparison.envelope_equals_reachable
        else 2 * BOX_BOUND + 1,
        reachable_state_count=len(orbit),
        behavioral_state_count=behavioral,
        minimal_machine_count=behavioral,
        graph_diameter=max(0, len(orbit) - 1),
        max_separation_depth=depth,
        closure_status=closure_status_label(certificate_kind=CertificateKind.EXACT_CLOSURE),
    )


def lsd_after_one_step_is_zero(limit: int = PROBE_LIMIT) -> bool:
    for n in range(-limit, limit + 1):
        if lsd_int(signed_p0(n)) != 0:
            return False
    return True
