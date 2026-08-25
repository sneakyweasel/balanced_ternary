"""Bounded probes for ``T(n)=W(n)``. Not planner hints."""

from __future__ import annotations

from bt.metrics import bt_weight
from research.balanced_ternary_weight_dynamics.spec import (
    BOX_BOUND,
    DEFAULT_START,
    digit_square_sum,
    weight_dynamics_spec,
)
from research_engine.attacks.envelope import (
    compare_envelope_to_reachable,
    envelope_from_interval,
    reachable_from_ints,
)
from research_engine.attacks.separation import separate_states
from research_engine.behavior.profile import ComplexityProfile, closure_status_label
from research_engine.core.semantics import CertificateKind

PROBE_LIMIT = 80
WINDOW = 20

# OEIS A005812 prefix, n = 0, 1, 2, ...
A005812_PREFIX: tuple[int, ...] = (
    0, 1, 2, 1, 2, 3, 2, 3, 2, 1, 2, 3, 2, 3, 4, 3, 4, 3, 2, 3, 4, 3, 4, 3,
    2, 3, 2, 1, 2, 3, 2, 3, 4, 3, 4, 3, 2, 3, 4, 3, 4, 5, 4, 5, 4, 3, 4, 5,
)


def matches_certified_weight(limit: int = PROBE_LIMIT) -> bool:
    if isinstance(limit, bool) or not isinstance(limit, int) or limit < 0:
        raise ValueError(f"limit must be a nonnegative int, got {limit!r}")
    for n in range(-limit, limit + 1):
        if digit_square_sum(n) != bt_weight(n):
            return False
    return True


def matches_oeis_prefix() -> bool:
    return all(digit_square_sum(n) == A005812_PREFIX[n] for n in range(len(A005812_PREFIX)))


def orbit_of(n: int, *, max_steps: int = 16) -> tuple[int, ...]:
    if isinstance(max_steps, bool) or not isinstance(max_steps, int) or max_steps < 1:
        raise ValueError(f"max_steps must be a positive int, got {max_steps!r}")
    seen: list[int] = []
    current = n
    for _ in range(max_steps):
        if current in seen:
            break
        seen.append(current)
        current = digit_square_sum(current)
    return tuple(seen)


def magnitude_drop_counterexample(limit: int = PROBE_LIMIT, *, min_abs: int = 2) -> int | None:
    if isinstance(limit, bool) or not isinstance(limit, int) or limit < 0:
        raise ValueError(f"limit must be a nonnegative int, got {limit!r}")
    if isinstance(min_abs, bool) or not isinstance(min_abs, int) or min_abs < 0:
        raise ValueError(f"min_abs must be a nonnegative int, got {min_abs!r}")
    best: int | None = None
    for n in range(-limit, limit + 1):
        if abs(n) < min_abs:
            continue
        if abs(digit_square_sum(n)) >= abs(n):
            if best is None or abs(n) < abs(best) or (abs(n) == abs(best) and n < best):
                best = n
    return best


def idempotent_counterexample(limit: int = PROBE_LIMIT) -> int | None:
    if isinstance(limit, bool) or not isinstance(limit, int) or limit < 0:
        raise ValueError(f"limit must be a nonnegative int, got {limit!r}")
    for n in range(-limit, limit + 1):
        image = digit_square_sum(n)
        if digit_square_sum(image) != image:
            return n
    return None


def even_map_counterexample(limit: int = PROBE_LIMIT) -> int | None:
    if isinstance(limit, bool) or not isinstance(limit, int) or limit < 0:
        raise ValueError(f"limit must be a nonnegative int, got {limit!r}")
    for n in range(-limit, limit + 1):
        if digit_square_sum(-n) != digit_square_sum(n):
            return n
    return None


def odd_map_counterexample(limit: int = PROBE_LIMIT) -> int | None:
    if isinstance(limit, bool) or not isinstance(limit, int) or limit < 0:
        raise ValueError(f"limit must be a nonnegative int, got {limit!r}")
    for n in range(-limit, limit + 1):
        if digit_square_sum(-n) != -digit_square_sum(n):
            return n
    return None


def lyapunov_n_witness() -> int:
    """Least-absolute ``n`` where ``V(n)=n`` does not strictly decrease."""
    for bound in range(0, 13):
        candidates = (0,) if bound == 0 else (bound, -bound)
        for n in candidates:
            if digit_square_sum(n) >= n:
                return n
    raise AssertionError("no Lyapunov witness in the probe window")


def interval_leak_witness(bound: int = BOX_BOUND) -> tuple[int, int] | None:
    if isinstance(bound, bool) or not isinstance(bound, int) or bound < 0:
        raise ValueError(f"bound must be a nonnegative int, got {bound!r}")
    for n in range(-bound, bound + 1):
        image = digit_square_sum(n)
        if abs(image) > bound:
            return n, image
    return None


def distinct_orbits_witness() -> tuple[int, int]:
    return 4, 5


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
    spec = weight_dynamics_spec(start=start)
    orbit = orbit_of(start)
    envelope_size = 2 * BOX_BOUND + 1
    nxt = digit_square_sum(start)
    sep = separate_states(spec, (start,), (nxt,))
    depth = sep.witness_length if sep.separated else 0
    return ComplexityProfile(
        control_count=1,
        invariant_state_count=envelope_size,
        reachable_state_count=len(orbit),
        behavioral_state_count=len(orbit),
        minimal_machine_count=len(orbit),
        graph_diameter=max(0, len(orbit) - 1),
        max_separation_depth=depth,
        closure_status=closure_status_label(certificate_kind=CertificateKind.EXACT_CLOSURE),
    )
