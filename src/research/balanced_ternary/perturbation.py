"""Carry-gain perturbations of doubled-trit dynamics.

``T_λ(c, d) = λ · DZ(c + 2d)``. Only ``λ = 1`` is value-preserving
normalization. ``λ = 2, 3`` are synthetic probes of the finite/infinite
boundary.
"""

from __future__ import annotations

from research.balanced_ternary.spec import DoubledTritSpec, doubled_trit_spec, emit
from research_engine.core.semantics import State


def gain_spec(gain: int, start_remaining: int = 8) -> DoubledTritSpec:
    return doubled_trit_spec(start_remaining=start_remaining, gain=gain)


def plus_one_orbit(gain: int, steps: int) -> tuple[State, ...]:
    """The all-``+1`` word. For ``λ = 3`` this is ``c_n = 3n``."""
    carry = 0
    orbit: list[State] = [(0,)]
    for _ in range(steps):
        carry, _out = emit(carry, 1, gain)
        orbit.append((carry,))
    return tuple(orbit)


def is_plus_one_unbounded_witness(gain: int = 3, steps: int = 8) -> bool:
    orbit = plus_one_orbit(gain, steps)
    values = [state[0] for state in orbit]
    if gain == 3:
        expected = [3 * n for n in range(steps + 1)]
        return values == expected
    return len(set(values)) == steps + 1 and abs(values[-1]) > abs(values[0])


def reachable_box(gain: int, cap: int = 64) -> frozenset[State] | None:
    """Tiny residual BFS. ``None`` means the cap was hit."""
    spec = gain_spec(gain)
    seen: set[State] = {spec.initial_state}
    queue = [spec.initial_state]
    phase = spec.initial_phase()
    while queue:
        if len(seen) > cap:
            return None
        state = queue.pop(0)
        for digit in spec.legal_controls(state, phase):
            nxt = spec.canonicalize(spec.transition(state, digit, phase))
            if nxt in seen:
                continue
            seen.add(nxt)
            queue.append(nxt)
    return frozenset(seen)


def family_fingerprint() -> dict[int, dict[str, object]]:
    """Exact finite closures for ``λ = 1, 2`` and the ``λ = 3`` witness."""
    out: dict[int, dict[str, object]] = {}
    for gain in (1, 2, 3):
        box = reachable_box(gain)
        out[gain] = {
            "gain": gain,
            "value_preserving": gain == 1,
            "finite": box is not None,
            "states": tuple(sorted(box)) if box is not None else None,
            "plus_one": plus_one_orbit(gain, 5),
            "unbounded_witness": is_plus_one_unbounded_witness(gain) if gain == 3 else False,
        }
    return out
