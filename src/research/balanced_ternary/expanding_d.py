"""Expanding map ``T(n) = 3n - λ lsd(n)`` on existing BT operators.

This is not laboratory ``D``. Lab ``D`` remains ``(n - lsd(n))/3``.
Canonical ``λ = 1`` is the section ``I_{-lsd(n)}(n)``.
"""

from __future__ import annotations

from collections import defaultdict

from bt.calculus.derivative import D
from bt.calculus.integral import I
from bt.operators import lsd_digit

TRITS: tuple[int, int, int] = (-1, 0, 1)


def _require_int(n: int, name: str = "n") -> int:
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"{name} must be int, got {type(n).__name__}")
    return n


def expanding_d(n: int, gain: int = 1) -> int:
    """``T_λ(n) = 3n - λ lsd(n)``. Uses existing ``lsd_digit``."""
    n = _require_int(n)
    gain = _require_int(gain, "gain")
    return 3 * n - gain * lsd_digit(n)


def as_section(n: int) -> int:
    """Canonical ``λ = 1`` is the existing section ``I_{-lsd(n)}(n)``."""
    n = _require_int(n)
    return I(-lsd_digit(n), n)


def residue_step(residue: int, gain: int = 1) -> int:
    """Exact next LSD: ``lsd(T_λ(n)) = lsd(-λ r)`` because ``3n ≡ 0 (mod 3)``."""
    residue = _require_int(residue, "residue")
    gain = _require_int(gain, "gain")
    if residue not in TRITS:
        raise ValueError(f"residue must be a trit, got {residue}")
    return lsd_digit(-gain * residue)


def quotient_form(n: int) -> tuple[int, int]:
    """``n = 3q + r`` with ``r = lsd(n)`` and ``q = D(n)``."""
    n = _require_int(n)
    return D(n), lsd_digit(n)


def expanding_d_from_quotient(n: int) -> int:
    """``T(n) = 9q + 2r`` for canonical ``λ = 1``."""
    q, r = quotient_form(n)
    return 9 * q + 2 * r


def lsd_orbit(n: int, length: int, gain: int = 1) -> tuple[int, ...]:
    """Observable ``r_k = lsd(T_λ^k(n))`` including ``k = 0``."""
    n = _require_int(n)
    length = _require_int(length, "length")
    if length < 0:
        raise ValueError("length must be nonnegative")
    out: list[int] = []
    current = n
    for _ in range(length):
        out.append(lsd_digit(current))
        current = expanding_d(current, gain)
    return tuple(out)


def predicted_lsd_orbit(n: int, length: int, gain: int = 1) -> tuple[int, ...]:
    """LSD stream predicted from ``lsd(n)`` alone."""
    n = _require_int(n)
    length = _require_int(length, "length")
    if length < 0:
        raise ValueError("length must be nonnegative")
    residue = lsd_digit(n)
    out: list[int] = []
    for _ in range(length):
        out.append(residue)
        residue = residue_step(residue, gain)
    return tuple(out)


def integer_orbit(n: int, steps: int, gain: int = 1) -> tuple[int, ...]:
    n = _require_int(n)
    steps = _require_int(steps, "steps")
    if steps < 0:
        raise ValueError("steps must be nonnegative")
    orbit = [n]
    current = n
    for _ in range(steps):
        current = expanding_d(current, gain)
        orbit.append(current)
    return tuple(orbit)


def observational_classes(
    values: tuple[int, ...],
    length: int,
    gain: int = 1,
) -> dict[tuple[int, ...], tuple[int, ...]]:
    buckets: dict[tuple[int, ...], list[int]] = defaultdict(list)
    for n in values:
        buckets[lsd_orbit(n, length, gain)].append(n)
    return {sig: tuple(group) for sig, group in buckets.items()}


def sample_range(limit: int) -> tuple[int, ...]:
    limit = _require_int(limit, "limit")
    if limit < 0:
        raise ValueError("limit must be nonnegative")
    return tuple(range(-limit, limit + 1))


def window_refines_observation(
    values: tuple[int, ...],
    window: int,
    length: int,
    gain: int = 1,
) -> tuple[bool, tuple[int, int] | None]:
    """Whether ``n ≡ m (mod 3^window)`` implies equal LSD streams of ``length``.

    A ``True`` answer on a finite sample is an OBSERVATION, not a theorem.
    """
    window = _require_int(window, "window")
    if window < 1:
        raise ValueError("window must be a positive int")
    modulus = 3**window
    by_residue: dict[int, list[int]] = defaultdict(list)
    for n in values:
        by_residue[n % modulus].append(n)
    for group in by_residue.values():
        signatures = {lsd_orbit(n, length, gain) for n in group}
        if len(signatures) > 1:
            first = group[0]
            first_sig = lsd_orbit(first, length, gain)
            second = next(m for m in group if lsd_orbit(m, length, gain) != first_sig)
            return False, (first, second)
    return True, None


def observation_implies_same_lsd(
    values: tuple[int, ...],
    length: int,
    gain: int = 1,
) -> tuple[bool, tuple[int, int] | None]:
    """Whether equal LSD streams of ``length`` imply equal ``lsd``."""
    classes = observational_classes(values, length, gain)
    for group in classes.values():
        residues = {lsd_digit(n) for n in group}
        if len(residues) > 1:
            first = group[0]
            second = next(m for m in group if lsd_digit(m) != lsd_digit(first))
            return False, (first, second)
    return True, None


def separating_pair(
    left: int,
    right: int,
    length: int,
    gain: int = 1,
) -> tuple[tuple[int, ...], tuple[int, ...]] | None:
    """Return the LSD streams if they differ, else ``None``."""
    left_sig = lsd_orbit(left, length, gain)
    right_sig = lsd_orbit(right, length, gain)
    if left_sig != right_sig:
        return left_sig, right_sig
    return None


def magnitude_contracts(n: int, gain: int = 1) -> bool:
    return abs(expanding_d(n, gain)) < abs(n)


def discovery_report(
    limit: int = 40,
    length: int = 12,
    max_window: int = 3,
    gain: int = 1,
) -> dict[str, object]:
    """Bounded residual reconnaissance. Not an exact Myhill–Nerode theorem."""
    values = sample_range(limit)
    classes = observational_classes(values, length, gain)
    windows: dict[int, bool] = {}
    witnesses: dict[str, object] = {}
    for window in range(1, max_window + 1):
        ok, witness = window_refines_observation(values, window, length, gain)
        windows[window] = ok
        if not ok:
            witnesses[f"window_{window}"] = witness
    same_lsd, lsd_witness = observation_implies_same_lsd(values, length, gain)
    if lsd_witness is not None:
        witnesses["lsd"] = lsd_witness
    predicted_ok = all(
        lsd_orbit(n, length, gain) == predicted_lsd_orbit(n, length, gain) for n in values
    )
    return {
        "scope": "BOUNDED",
        "status": "OBSERVATION",
        "sample_limit": limit,
        "orbit_length": length,
        "class_count": len(classes),
        "lsd_class_count": len({lsd_digit(n) for n in values}),
        "windows_sufficient": windows,
        "observation_implies_lsd": same_lsd,
        "predicted_matches_sample": predicted_ok,
        "mod9_not_necessary": separating_pair(1, 4, length, gain) is None,
        "lsd_separates_1_2": separating_pair(1, 2, length, gain) is not None,
        "magnitude_contracts_on_1": magnitude_contracts(1, gain),
        "witnesses": witnesses,
    }
