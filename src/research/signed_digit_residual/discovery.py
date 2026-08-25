"""Exact residual dynamics of ``F(s,u)=λ·D(s+u)``.

This is discovery, not a new engine. ``D`` is the existing balanced
quotient. Finite-horizon growth is never treated as infinitude.
"""

from __future__ import annotations

from collections.abc import Sequence

from bt.calculus.derivative import D
from bt.operators import lsd_digit
from bt.transducers.mealy import minimize_mealy_count

TRITS: tuple[int, int, int] = (-1, 0, 1)
DISTINGUISHING_PAIRS: tuple[tuple[int, int], ...] = (
    (1, 1),
    (1, 2),
    (1, 3),
    (2, 1),
    (2, 2),
    (3, 1),
)
INFINITE_COMPANION: tuple[int, int] = (3, 2)
DEFAULT_CAP = 256


def alphabet_m(m: int) -> tuple[int, ...]:
    if m < 0:
        raise ValueError("alphabet bound must be nonnegative")
    return tuple(range(-m, m + 1))


def signed_step(state: int, control: int, gain: int = 1) -> tuple[int, int]:
    """One residual step. Output is ``lsd(s+u)``; next state is ``λ·D(s+u)``."""
    total = state + control
    return gain * D(total), lsd_digit(total)


def reachable_from(
    start: int,
    alphabet: Sequence[int],
    gain: int = 1,
    cap: int = DEFAULT_CAP,
) -> frozenset[int] | None:
    """BFS from ``start``. ``None`` means the cap was hit, not infinitude."""
    seen: set[int] = {start}
    queue = [start]
    while queue:
        if len(seen) > cap:
            return None
        state = queue.pop()
        for control in alphabet:
            nxt, _out = signed_step(state, control, gain)
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
                if len(seen) > cap:
                    return None
    return frozenset(seen)


def box_leak(
    radius: int,
    alphabet: Sequence[int],
    gain: int = 1,
) -> tuple[int, int] | None:
    """Smallest ``(s,u)`` with ``s`` in the box and ``F(s,u)`` outside it."""
    letters = tuple(alphabet)
    for state in range(-radius, radius + 1):
        for control in letters:
            nxt, _out = signed_step(state, control, gain)
            if abs(nxt) > radius:
                return state, control
    return None


def smallest_invariant_radius(
    alphabet: Sequence[int],
    gain: int = 1,
    max_radius: int = 64,
) -> int | None:
    for radius in range(0, max_radius + 1):
        if box_leak(radius, alphabet, gain) is None:
            return radius
    return None


def lyapunov_leak(
    alphabet: Sequence[int],
    gain: int = 1,
    *,
    min_abs: int,
    search_radius: int,
) -> tuple[int, int] | None:
    """Smallest ``(s,u)`` with ``|s|≥min_abs`` and ``|F(s,u)|≥|s|``."""
    letters = tuple(alphabet)
    for abs_s in range(min_abs, search_radius + 1):
        for state in (abs_s, -abs_s):
            for control in letters:
                nxt, _out = signed_step(state, control, gain)
                if abs(nxt) >= abs_s:
                    return state, control
    return None


def mealy_count(
    states: Sequence[int],
    alphabet: Sequence[int],
    gain: int = 1,
) -> int:
    letters = tuple(alphabet)

    def mealy(state: int, control: int) -> tuple[int, int]:
        return signed_step(state, control, gain)

    return minimize_mealy_count(states, letters, mealy)


def constant_orbit(
    control: int,
    gain: int,
    steps: int,
    start: int = 0,
) -> tuple[int, ...]:
    state = start
    orbit = [state]
    for _ in range(steps):
        state, _out = signed_step(state, control, gain)
        orbit.append(state)
    return tuple(orbit)


def is_constant_unbounded_family(
    control: int,
    gain: int,
    steps: int = 8,
) -> bool:
    """Exact family ``s_n=3n`` for gain 3 and control 2; otherwise not a certificate."""
    orbit = constant_orbit(control, gain, steps)
    if gain == 3 and control == 2:
        expected = tuple(3 * n for n in range(steps + 1))
        return orbit == expected
    if gain == 3 and control == -2:
        expected = tuple(-3 * n for n in range(steps + 1))
        return orbit == expected
    return False


def max_abs(alphabet: Sequence[int]) -> int:
    return max((abs(int(letter)) for letter in alphabet), default=0)


def finite_from_origin_alphabet(gain: int, alphabet: Sequence[int]) -> bool:
    """Exact Level-B law: finite iff ``λ≤2`` or every ``|u|≤1``."""
    if gain <= 0:
        raise ValueError("gain must be positive")
    return gain <= 2 or max_abs(alphabet) <= 1


def constant_control_unbounded(gain: int, control: int) -> bool:
    """Exact escape: ``λ≥3`` and ``|u|≥2``, not BFS growth."""
    return gain >= 3 and abs(control) >= 2


def gain3_identity_holds(state: int, control: int) -> bool:
    nxt, out = signed_step(state, control, 3)
    return nxt == state + control - out


def lambda2_reachable_radius(m: int) -> int:
    """Sharp ``λ=2`` invariant/reachable radius ``2(m-1)_+``."""
    if m < 0:
        raise ValueError("alphabet bound must be nonnegative")
    return 2 * max(m - 1, 0)


def lambda2_residual_complexity(m: int) -> int:
    """Origin-reachable count for ``F_{2,U_m}``: one even lattice point per step of the radius."""
    if m <= 1:
        return 1
    return 2 * m - 1


def lambda1_reachable_radius(m: int) -> int:
    return m // 2


def lambda1_invariant_radius_loose(m: int) -> int:
    """Loose candidate ``⌈(m+1)/2⌉`` from ``3|DZ n|≤|n|+1``. Not assumed sharp."""
    return (m + 2) // 2


def origin_reachable_report(
    m: int,
    gain: int = 1,
    cap: int = DEFAULT_CAP,
) -> dict[str, object]:
    alphabet = alphabet_m(m)
    reachable = reachable_from(0, alphabet, gain, cap=cap)
    box = smallest_invariant_radius(alphabet, gain)
    if reachable is None:
        classification = "OBSERVATION"
        states: tuple[int, ...] | None = None
        mealy: int | None = None
    else:
        states = tuple(sorted(reachable))
        mealy = mealy_count(states, alphabet, gain)
        classification = "EXACT FINITE"
    infinite = False
    if not finite_from_origin(gain, m):
        witness = 2 if m >= 2 else 0
        infinite = constant_control_unbounded(gain, witness)
        if infinite:
            classification = "EXACT INFINITE"
    return {
        "gain": gain,
        "m": m,
        "alphabet": alphabet,
        "reachable": states,
        "reachable_count": None if states is None else len(states),
        "invariant_radius": box,
        "mealy": mealy,
        "classification": classification,
        "unbounded_witness": infinite,
    }


def distinguishing_fingerprint() -> dict[tuple[int, int], dict[str, object]]:
    out: dict[tuple[int, int], dict[str, object]] = {}
    for gain, bound in DISTINGUISHING_PAIRS:
        out[(gain, bound)] = origin_reachable_report(bound, gain)
    out[INFINITE_COMPANION] = origin_reachable_report(INFINITE_COMPANION[1], INFINITE_COMPANION[0])
    return out


def trit_sum_values(arity: int) -> frozenset[int]:
    if arity < 0:
        raise ValueError("arity must be nonnegative")
    values = {0}
    for _ in range(arity):
        values = {total + digit for total in values for digit in TRITS}
    return frozenset(values)


def r_way_step(state: int, digits: Sequence[int]) -> tuple[int, int]:
    return signed_step(state, sum(digits), 1)


def r_way_reachable(arity: int, cap: int = DEFAULT_CAP) -> frozenset[int] | None:
    return reachable_from(0, alphabet_m(arity), gain=1, cap=cap)


def r_way_mealy(arity: int) -> int:
    reachable = r_way_reachable(arity)
    if reachable is None:
        raise RuntimeError("r-way reachable set exceeded the cap")
    return mealy_count(tuple(sorted(reachable)), alphabet_m(arity), gain=1)


def residual_complexity(arity: int) -> int:
    """``M(r)=2⌊r/2⌋+1`` for origin-reachable r-way trit addition."""
    return 2 * (arity // 2) + 1


def finite_from_origin(gain: int, bound: int) -> bool:
    """Exact condition on ``F_{λ,U_m}`` for every integer ``λ≥1``."""
    if gain <= 0 or bound < 0:
        raise ValueError("gain must be positive and bound nonnegative")
    return gain <= 2 or bound <= 1


def asymmetric_perturbation() -> dict[str, object]:
    """One controlled perturbation: ``U={0,1,2}`` at gain 1, after ``C(λ,U)``."""
    alphabet = (0, 1, 2)
    reachable = reachable_from(0, alphabet, gain=1)
    assert reachable is not None
    return {
        "alphabet": alphabet,
        "reachable": tuple(sorted(reachable)),
        "invariant_radius": smallest_invariant_radius(alphabet, gain=1),
        "mealy": mealy_count(tuple(sorted(reachable)), alphabet, gain=1),
        "classification": "EXACT FINITE",
        "note": "symmetry of U_m is not required for finiteness at λ=1",
    }


def _alphabet_report(alphabet: Sequence[int], gain: int) -> dict[str, object]:
    letters = tuple(int(letter) for letter in alphabet)
    reachable = reachable_from(0, letters, gain)
    finite = finite_from_origin_alphabet(gain, letters)
    if finite:
        assert reachable is not None
        states = tuple(sorted(reachable))
        return {
            "alphabet": letters,
            "gain": gain,
            "max_abs": max_abs(letters),
            "reachable": states,
            "reachable_count": len(states),
            "invariant_radius": smallest_invariant_radius(letters, gain),
            "mealy": mealy_count(states, letters, gain),
            "classification": "EXACT FINITE",
            "unbounded_witness": False,
        }
    witness = next((letter for letter in letters if abs(letter) >= 2), None)
    return {
        "alphabet": letters,
        "gain": gain,
        "max_abs": max_abs(letters),
        "reachable": None,
        "reachable_count": None,
        "invariant_radius": smallest_invariant_radius(letters, gain),
        "mealy": None,
        "classification": "EXACT INFINITE",
        "unbounded_witness": witness is not None
        and constant_control_unbounded(gain, witness),
    }


def geometry_perturbation() -> dict[str, dict[str, object]]:
    """Sparse and asymmetric alphabets: phase follows max|u|, closure follows geometry."""
    return {
        "sparse_2_g1": _alphabet_report((-2, 0, 2), 1),
        "sparse_2_g2": _alphabet_report((-2, 0, 2), 2),
        "sparse_2_g3": _alphabet_report((-2, 0, 2), 3),
        "asymmetric_012_g1": _alphabet_report((0, 1, 2), 1),
        "asymmetric_012_g2": _alphabet_report((0, 1, 2), 2),
        "asymmetric_012_g3": _alphabet_report((0, 1, 2), 3),
        "singleton_2_g2": _alphabet_report((2,), 2),
    }
