"""Prefix family ``P_m = (2)·(-4)^m`` plus a uniformly bounded tail.

Phase-0 asks whether a tail of length at most ``T`` completes the
prefix to an origin-legal remaining-0 live word whose landing is
not the two-step ray, not the hub, and not a ``(B*)^k``-padded hub.

The prefix dies for ``m>=3``: after ``(2,-4,-4)`` the next ``-4``
lands on ``(6,2,2)``, which is not live. Live completions at this
bound exist only for ``m=0,1,2`` and do not share a closed-form
tail. A finite ``m``-range is not ``|L_0|=∞``. This is not a
generic engine attack.
"""

from __future__ import annotations

from research.ostrowski.energy_trajectory import apply_word
from research.ostrowski.live_growth import legal_w, residual_is_live
from research.ostrowski.live_layers import ORIGIN
from research.ostrowski.nonpisot_search import HUB
from research.ostrowski.recurrence_zero import (
    HUB_WORD,
    RECURRENCE_WORD_MSD,
    fully_live,
    reset_pow_then_hub_word,
)
from research.ostrowski.spectral_control import N12_MAXIMIZER_WORD
from research.ostrowski.spectral_residual import transition_affine
from research.ostrowski.system import nonpisot_order3
from research.ostrowski.zero_value_kernel import on_legal_two_step_ray
from research_engine.attacks.result import AttackStatus
from research_engine.core.semantics import ClaimKind, SearchScope

State3 = tuple[int, int, int]

PREFIX_HEAD = 2
PREFIX_REPEAT = -4
DEFAULT_MAX_M = 12
DEFAULT_MAX_TAIL = 6
_TAIL_SET_CAP = 64

GROWTH_NOT_INFINITUDE = "finite_depth_is_not_infinitude"
PREFIX_NOT_UNBOUNDED_FAMILY = "bounded_tail_prefix_is_not_unbounded_L0"
EXCLUDED_NOT_THIS_FAMILY = "ray_hub_bstar_are_not_this_family"
CLASS_HUB = "hub"
CLASS_RAY = "two_step_ray"
CLASS_BSTAR = "bstar_padded_hub"
CLASS_OTHER = "other"
EXCLUDED_CLASSES = frozenset({CLASS_HUB, CLASS_RAY, CLASS_BSTAR})


def _sys():
    return nonpisot_order3()


def prefix(m: int) -> tuple[int, ...]:
    """``P_m = (2) · (-4)^m``."""
    if m < 0:
        raise ValueError("m must be nonnegative")
    return (PREFIX_HEAD,) + (PREFIX_REPEAT,) * m


def is_hub(state: State3) -> bool:
    return state == HUB


def is_bstar_padded_hub_word(word: tuple[int, ...]) -> bool:
    """``w = (B*)^k · (1,-2)`` for some ``k >= 0``."""
    n_hub = len(HUB_WORD)
    if len(word) < n_hub or word[-n_hub:] != HUB_WORD:
        return False
    body = word[:-n_hub]
    block = RECURRENCE_WORD_MSD
    if len(body) % len(block) != 0:
        return False
    k = len(body) // len(block)
    return body == block * k


def classify_landing(state: State3) -> str:
    """Ray / hub from the particular. Hub sits on the two-step ray."""
    if is_hub(state):
        return CLASS_HUB
    if on_legal_two_step_ray(state):
        return CLASS_RAY
    return CLASS_OTHER


def classify_completion(word: tuple[int, ...], landing: State3) -> str:
    """Excluded families first. ``U_k`` is a B*-padded hub, not this prefix."""
    if is_bstar_padded_hub_word(word) and landing == HUB:
        return CLASS_BSTAR
    return classify_landing(landing)


def is_excluded(label: str) -> bool:
    return label in EXCLUDED_CLASSES


def walk_live(
    word: tuple[int, ...],
    start_remaining: int | None = None,
    start_state: State3 = ORIGIN,
) -> State3 | None:
    """Apply ``word`` if every letter is legal and every residual is live."""
    sys = _sys()
    remaining = len(word) if start_remaining is None else start_remaining
    if remaining < len(word):
        return None
    state = start_state
    if not residual_is_live(sys, state, remaining):
        return None
    for w in word:
        place = remaining - 1
        if place < 0 or w not in legal_w(sys, place):
            return None
        state = transition_affine(sys, state, w)
        remaining -= 1
        if not residual_is_live(sys, state, remaining):
            return None
    return state


def _dfs_tails(
    sys,
    state: State3,
    remaining: int,
    acc: list[int],
    found: list[tuple[tuple[int, ...], State3]],
    tail_cap: int,
) -> None:
    if remaining == 0:
        found.append((tuple(acc), state))
        return
    if tail_cap >= 0 and len(found) >= tail_cap:
        return
    place = remaining - 1
    nxt_rem = remaining - 1
    for w in legal_w(sys, place):
        nxt = transition_affine(sys, state, w)
        if not residual_is_live(sys, nxt, nxt_rem):
            continue
        acc.append(w)
        _dfs_tails(sys, nxt, nxt_rem, acc, found, tail_cap)
        acc.pop()
        if tail_cap >= 0 and len(found) >= tail_cap:
            return


def complete_prefix(
    m: int,
    max_tail: int = DEFAULT_MAX_TAIL,
) -> dict[str, object]:
    """Live remaining-0 completions of ``P_m`` with tail length ``0..max_tail``."""
    if max_tail < 0:
        raise ValueError("max_tail must be nonnegative")
    head = prefix(m)
    sys = _sys()
    landings: dict[State3, tuple[int, ...]] = {}
    other_tails: set[tuple[int, ...]] = set()
    n_live = 0
    n_other = 0
    n_excluded = 0
    prefix_live_any = False
    classes: dict[str, int] = {}
    for t in range(max_tail + 1):
        start = len(head) + t
        after = walk_live(head, start)
        if after is None:
            continue
        prefix_live_any = True
        found: list[tuple[tuple[int, ...], State3]] = []
        _dfs_tails(sys, after, t, [], found, -1)
        for tail, landing in found:
            n_live += 1
            word = head + tail
            label = classify_completion(word, landing)
            classes[label] = classes.get(label, 0) + 1
            landings.setdefault(landing, word)
            if is_excluded(label):
                n_excluded += 1
            else:
                n_other += 1
                if len(other_tails) < _TAIL_SET_CAP:
                    other_tails.add(tail)
    return {
        "m": m,
        "prefix": head,
        "prefix_live_any_tail": prefix_live_any,
        "n_live_completions": n_live,
        "n_other": n_other,
        "n_excluded": n_excluded,
        "landings": tuple(sorted(landings)),
        "n_distinct_landings": len(landings),
        "classes": classes,
        "other_tails": tuple(sorted(other_tails)),
        "other_tails_capped": n_other > len(other_tails),
        "prefix_dies": n_live == 0,
        "sample_word": next(iter(landings.values()), None),
    }


def _closed_form_tail(rows: list[dict[str, object]]) -> tuple[int, ...] | None:
    """A single tail that yields an other-class landing for every ``m``."""
    other_sets: list[set[tuple[int, ...]]] = []
    for row in rows:
        if row["other_tails_capped"] or row["n_other"] == 0:
            return None
        other_sets.append(set(row["other_tails"]))
    if not other_sets:
        return None
    common = other_sets[0]
    for extra in other_sets[1:]:
        common &= extra
        if not common:
            return None
    return min(common)


def _tail_scheme(rows: list[dict[str, object]]) -> dict[str, object]:
    live = [r for r in rows if r["n_live_completions"] > 0]
    other = [r for r in rows if r["n_other"] > 0]
    constant = _closed_form_tail(rows) if other and len(other) == len(rows) else None
    lengths = [
        {len(t) for t in r["other_tails"]}
        for r in other
        if r["other_tails"]
    ]
    length_grows = False
    if len(lengths) >= 2:
        mins = [min(s) for s in lengths]
        length_grows = mins[-1] > mins[0] and all(
            mins[i] <= mins[i + 1] for i in range(len(mins) - 1)
        )
    unstructured = constant is None and (
        any(r["other_tails_capped"] for r in rows) or len(other) < len(rows)
    )
    return {
        "constant_tail": constant,
        "empty_tail": constant == (),
        "length_grows_with_m": length_grows,
        "unstructured": unstructured,
        "n_m_live": len(live),
        "n_m_other": len(other),
        "n_m_dead": sum(1 for r in rows if r["prefix_dies"]),
    }


def search_prefix_family(
    max_m: int = DEFAULT_MAX_M,
    max_tail: int = DEFAULT_MAX_TAIL,
) -> dict[str, object]:
    """Bounded ``m`` and tail length. Not an infinitude claim."""
    if max_m < 0:
        raise ValueError("max_m must be nonnegative")
    rows = [complete_prefix(m, max_tail) for m in range(max_m + 1)]
    scheme = _tail_scheme(rows)
    closed = scheme["constant_tail"] is not None
    other_landings: set[State3] = set()
    excluded_landings: set[State3] = set()
    for row in rows:
        for state in row["landings"]:
            if classify_landing(state) in EXCLUDED_CLASSES:
                excluded_landings.add(state)
            else:
                other_landings.add(state)
    first_dead = next((r["m"] for r in rows if r["prefix_dies"]), None)
    return {
        "max_m": max_m,
        "max_tail": max_tail,
        "rows": rows,
        "scheme": scheme,
        "closed_form_tail": scheme["constant_tail"],
        "symbolic_family": closed,
        "first_dead_m": first_dead,
        "other_landings": tuple(sorted(other_landings)),
        "excluded_landings": tuple(sorted(excluded_landings)),
        "n_other_landings": len(other_landings),
        "prefix_dies_some_m": any(r["prefix_dies"] for r in rows),
        "all_live_are_excluded": (
            all(r["n_other"] == 0 for r in rows)
            and any(r["n_live_completions"] > 0 for r in rows)
        ),
        GROWTH_NOT_INFINITUDE: True,
        PREFIX_NOT_UNBOUNDED_FAMILY: True,
    }


def phase0_prefix_family(
    max_m: int = DEFAULT_MAX_M,
    max_tail: int = DEFAULT_MAX_TAIL,
) -> dict[str, object]:
    """Observation at a finite bound. Kind is never ``LIVE``."""
    search = search_prefix_family(max_m, max_tail)
    closed = bool(search["symbolic_family"])
    return {
        **search,
        "status": AttackStatus.OBSERVATION.value,
        "scope": SearchScope.BOUNDED.value,
        "kind": ClaimKind.LIVE_SLICE.value,
        "infinitude_claimed": False,
        "l0_promoted": False,
        GROWTH_NOT_INFINITUDE: True,
        PREFIX_NOT_UNBOUNDED_FAMILY: True,
        EXCLUDED_NOT_THIS_FAMILY: True,
        "closed_form_found": closed,
        "symbolic_family": closed,
        "maximizer_prefix": prefix(2),
        "maximizer_word": N12_MAXIMIZER_WORD,
    }


def maximizer_starts_with_prefix() -> bool:
    return N12_MAXIMIZER_WORD[:3] == prefix(2)


def maximizer_is_origin_live() -> bool:
    word = N12_MAXIMIZER_WORD
    return fully_live(word, len(word)) and walk_live(word) is not None


def uk_is_excluded(k: int) -> bool:
    word = reset_pow_then_hub_word(k)
    landing = apply_word(_sys(), ORIGIN, word)
    return is_excluded(classify_completion(word, landing))
