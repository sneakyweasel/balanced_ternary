"""Specialized order-3 transition and unread-tail extremals.

Fixed Γ = ([0; 2̄], [0; 1̄], [0; 1̄]). Digits from Baranwal §5.3:

* a_0 ∈ {0,1}, so LSD w ∈ {-2,…,1};
* a_i ∈ {0,1,2} for i≥1, so interior w ∈ {-4,…,2}.

The specialized map is

    (s1, s2, s3) ↦ (s3, s1+s3, s2+2 s3 − w).
"""

from __future__ import annotations

from functools import lru_cache

from research.ostrowski.residual import CarryState, residual_integer
from research.ostrowski.system import OstrowskiSystem, phase0_order3

INTERIOR_W = tuple(range(-4, 3))  # place i ≥ 1
LSD_W = tuple(range(-2, 2))  # place i = 0
State3 = tuple[int, int, int]


def legal_w(place: int) -> tuple[int, ...]:
    """Difference alphabet at place ``place`` (0 = LSD)."""
    if place < 0:
        raise ValueError("place must be nonnegative")
    return LSD_W if place == 0 else INTERIOR_W


def order3_transition(state: State3, w: int) -> State3:
    """Exact map for this Γ; independent of remaining length."""
    s1, s2, s3 = state
    return (s3, s1 + s3, s2 + 2 * s3 - w)


def is_sign_flip_symmetry() -> bool:
    """The digit-difference alphabet is asymmetric, so s ↦ −s is not a symmetry."""
    return INTERIOR_W == tuple(-w for w in reversed(INTERIOR_W))


@lru_cache(maxsize=None)
def _system() -> OstrowskiSystem:
    return phase0_order3()


def place_sum(i: int) -> int:
    """``sum_{j=0}^{i} q_j``."""
    if i < 0:
        return 0
    qs = _system().place_values(i + 1)
    return sum(qs)


def unread_tail_bounds(remaining: int) -> tuple[int, int]:
    """Min and max of ``sum_{j<remaining} w_j q_j`` over legal difference words.

    LSD uses ``LSD_W``; every higher place uses ``INTERIOR_W``.
    For ``remaining = 0`` the unread tail is empty, so both bounds are 0.
    """
    if remaining < 0:
        raise ValueError("remaining must be nonnegative")
    if remaining == 0:
        return (0, 0)
    sys = _system()
    qs = sys.place_values(remaining)
    lo = LSD_W[0] * qs[0]
    hi = LSD_W[-1] * qs[0]
    for j in range(1, remaining):
        lo += INTERIOR_W[0] * qs[j]
        hi += INTERIOR_W[-1] * qs[j]
    return (lo, hi)


def residual_is_live(state: CarryState, remaining: int) -> bool:
    """Whether ``E_remaining(state)`` can still be realized by a legal unread tail."""
    lo, hi = unread_tail_bounds(remaining)
    value = residual_integer(_system(), state, remaining)
    return lo <= value <= hi


def extremal_next_coords(state: State3, place: int) -> dict[str, object]:
    """Min/max of each next coordinate over legal ``w`` at ``place``."""
    ws = legal_w(place)
    images = [order3_transition(state, w) for w in ws]
    return {
        "state": state,
        "place": place,
        "w": ws,
        "images": tuple(images),
        "min": tuple(min(im[k] for im in images) for k in range(3)),
        "max": tuple(max(im[k] for im in images) for k in range(3)),
    }
