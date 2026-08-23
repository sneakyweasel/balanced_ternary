"""Exact Phase-0 tests for a regular-output preimage of x^2.

The output constraint is the two-state safety automaton forbidding the
trit -1. Combined with the residual Mealy machine of F, a constrained
state is a pair (g, q) with q in {live, dead}. The preimage language is
the set of input words that keep q live.

Finite-horizon right languages are memoized remaining-horizon
acceptance signatures, not sample signatures and not clocked DFAs.
Stabilization through a finite depth is computational evidence only.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from itertools import product

from bt.calculus.lifting import is_lift_node
from bt.calculus.residual import TRITS, delta, output_along, rho
from bt.calculus.section import IntPoly, parse_poly

LIVE = 1
DEAD = 0
MAX_DEPTH = 7
FORBIDDEN = -1
SAFE = (0, 1)

X = parse_poly("x")
X2 = parse_poly("x^2")


def _require_horizon(n: int, name: str = "horizon") -> int:
    if isinstance(n, bool) or not isinstance(n, int) or n < 0:
        raise ValueError(f"{name} must be a nonnegative int")
    return n


def step_safety(q: int, trit: int) -> int:
    """Two-state safety step: live until the first forbidden output."""

    if q not in (LIVE, DEAD):
        raise ValueError(f"unknown safety state {q!r}")
    if trit not in TRITS:
        raise ValueError(f"output must be a trit, got {trit}")
    if q == DEAD or trit == FORBIDDEN:
        return DEAD
    return LIVE


def is_safe_word(outputs: tuple[int, ...]) -> bool:
    return all(t in SAFE for t in outputs)


@lru_cache(maxsize=None)
def accept_signature(coeffs: tuple[int, ...], q: int, r: int) -> object:
    """Exact remaining-horizon right-language signature of (g, q).

    Dead states share one signature. Live signatures record, for each
    input trit, whether that letter is immediately fatal and otherwise
    the child live signature at horizon r-1. Outputs themselves are not
    stored: the observable is the preimage language, not the full Mealy
    word.
    """

    r = _require_horizon(r)
    if q == DEAD:
        return ("D",)
    if r == 0:
        return ("L",)
    g = IntPoly(coeffs)
    parts = []
    for a in TRITS:
        out = rho(g, a)
        nxt = step_safety(LIVE, out)
        if nxt == DEAD:
            parts.append("D")
        else:
            parts.append(accept_signature(delta(g, a).coeffs, LIVE, r - 1))
    return tuple(parts)


def signature_of(g: IntPoly, q: int, r: int) -> object:
    return accept_signature(g.coeffs, q, r)


def reachable_live(f: IntPoly, depth: int) -> list[IntPoly]:
    """Live residuals after a live input path of exact length ``depth``."""

    depth = _require_horizon(depth, "depth")
    layer = [f]
    for _ in range(depth):
        seen: set[tuple[int, ...]] = set()
        nxt: list[IntPoly] = []
        for g in layer:
            for a in TRITS:
                if step_safety(LIVE, rho(g, a)) == DEAD:
                    continue
                child = delta(g, a)
                if child.coeffs not in seen:
                    seen.add(child.coeffs)
                    nxt.append(child)
        layer = nxt
    return layer


def census_count(f: IntPoly, m: int, r: int) -> int:
    """Number of ≡_r right-language types among live states at depth m."""

    states = reachable_live(f, _require_horizon(m, "m"))
    return len({signature_of(g, LIVE, _require_horizon(r)) for g in states})


def census_table(f: IntPoly, max_depth: int = MAX_DEPTH) -> tuple[tuple[int, ...], ...]:
    """Rows are depths m=0..max_depth; columns are horizons r=0..max_depth."""

    max_depth = _require_horizon(max_depth, "max_depth")
    rows = []
    for m in range(max_depth + 1):
        rows.append(tuple(census_count(f, m, r) for r in range(max_depth + 1)))
    return tuple(rows)


def zero_output_is_proper_subset(f: IntPoly, max_len: int = 4) -> dict[str, object]:
    """Lifting language {output = 0*} is strictly inside the safety language."""

    max_len = _require_horizon(max_len, "max_len")
    safety = 0
    lifts = 0
    witness: tuple[int, ...] | None = None
    for length in range(max_len + 1):
        for word in product(TRITS, repeat=length) if length else ((),):
            outputs = output_along(f, word)
            if is_safe_word(outputs):
                safety += 1
                if is_lift_node(f, word):
                    lifts += 1
                elif witness is None and word:
                    witness = word
    return {
        "safety_count": safety,
        "lift_count": lifts,
        "proper_subset": lifts < safety,
        "safe_non_lift": list(witness) if witness is not None else None,
    }


def distinguish_accept(
    f: IntPoly,
    g: IntPoly,
    max_len: int,
) -> tuple[int, ...] | None:
    """Shortest word accepted by exactly one of the two live residuals."""

    max_len = _require_horizon(max_len, "max_len")
    for length in range(1, max_len + 1):
        for word in product(TRITS, repeat=length):
            acc_f = is_safe_word(output_along(f, word))
            acc_g = is_safe_word(output_along(g, word))
            if acc_f != acc_g:
                return word
    return None


def family_x2_plus_two(m: int) -> IntPoly:
    """Residual of x^2 along (1,) followed by m zeros: 3^{m+1} x^2 + 2x."""

    m = _require_horizon(m, "m")
    return IntPoly((0, 2, 3 ** (m + 1)))


def prefix_one_then_zeros(m: int) -> tuple[int, ...]:
    """The live prefix whose residual is ``family_x2_plus_two(m)``."""

    return (1,) + (0,) * _require_horizon(m, "m")


def distinguishing_word(m: int) -> tuple[int, ...]:
    """``(-1)^{m+1}`` followed by ``0``. Accepts ``g_m``, rejects every ``g_n`` with ``n>m``."""

    m = _require_horizon(m, "m")
    return (-1,) * (m + 1) + (0,)


def pack_all_minus(k: int) -> int:
    """``pack((-1)^k) = -(3^k-1)/2``."""

    k = _require_horizon(k, "k")
    return -(3**k - 1) // 2


def first_k_digits_of_one_minus_3k(k: int) -> tuple[int, ...]:
    """The first ``k`` balanced digits of ``1-3^k`` are ``(+ , 0^{k-1})``."""

    k = _require_horizon(k, "k")
    if k == 0:
        return ()
    return (1,) + (0,) * (k - 1)


def family_accepts(m: int, word: tuple[int, ...]) -> bool:
    return is_safe_word(output_along(family_x2_plus_two(m), word))


def distinction_holds(m: int, n: int) -> bool:
    """``w_m`` is a Myhill–Nerode witness between prefixes ``10^m`` and ``10^n``."""

    if n <= m:
        raise ValueError("need n > m")
    word = distinguishing_word(m)
    return family_accepts(m, word) and not family_accepts(n, word)


def distinguishing_family_search(max_m: int = 5, word_bound: int = 5) -> dict[str, object]:
    """Search the family 3^{m+1}x^2+2x for pairwise safety distinction."""

    max_m = _require_horizon(max_m, "max_m")
    word_bound = _require_horizon(word_bound, "word_bound")
    polys = [family_x2_plus_two(m) for m in range(max_m + 1)]
    pairs: list[dict[str, object]] = []
    for i, f in enumerate(polys):
        for j in range(i + 1, len(polys)):
            word = distinguish_accept(f, polys[j], word_bound)
            if word is not None:
                pairs.append(
                    {
                        "m": i,
                        "n": j,
                        "word": list(word),
                    }
                )
    return {
        "family": "3^{m+1} x^2 + 2x",
        "max_m": max_m,
        "word_bound": word_bound,
        "distinguished_pairs": pairs,
        "all_identified": len(pairs) == 0,
    }


def linear_live_count(max_depth: int = MAX_DEPTH) -> dict[str, object]:
    """The identity map has one live residual: itself."""

    table = census_table(X, max_depth)
    types = {count for row in table for count in row}
    return {
        "table": table,
        "unique_counts": sorted(types),
        "single_live_type": types == {1},
    }


@dataclass(frozen=True)
class QuotientProbe:
    """Observed live types at a large horizon, among depths 0..max_depth."""

    horizon: int
    max_depth: int
    type_count: int
    types_by_depth: tuple[int, ...]
    bounded: bool


def quotient_probe(f: IntPoly, max_depth: int = MAX_DEPTH, horizon: int | None = None) -> QuotientProbe:
    horizon = max_depth if horizon is None else _require_horizon(horizon)
    max_depth = _require_horizon(max_depth, "max_depth")
    seen: set[object] = set()
    per_depth = []
    for m in range(max_depth + 1):
        layer = {signature_of(g, LIVE, horizon) for g in reachable_live(f, m)}
        per_depth.append(len(layer))
        seen.update(layer)
    return QuotientProbe(
        horizon=horizon,
        max_depth=max_depth,
        type_count=len(seen),
        types_by_depth=tuple(per_depth),
        bounded=len(seen) <= max(per_depth),
    )


def first_outputs_of_x2() -> tuple[int, int, int]:
    return (rho(X2, -1), rho(X2, 0), rho(X2, 1))


def triage_report(max_depth: int = MAX_DEPTH) -> dict[str, object]:
    max_depth = _require_horizon(max_depth, "max_depth")
    linear = linear_live_count(max_depth)
    table = census_table(X2, max_depth)
    probe = quotient_probe(X2, max_depth)
    family = distinguishing_family_search(max_m=min(5, max_depth), word_bound=min(5, max_depth))
    subset = zero_output_is_proper_subset(X2, max_len=min(4, max_depth))
    root_rho = first_outputs_of_x2()
    growing = any(table[m][r] > table[0][r] for m in range(1, max_depth + 1) for r in range(max_depth + 1))
    return {
        "polynomial": "x^2",
        "constraint": "{0,+}^omega",
        "max_depth": max_depth,
        "root_rho": list(root_rho),
        "root_never_minus": FORBIDDEN not in root_rho,
        "linear": linear,
        "x2_census": table,
        "x2_probe": {
            "horizon": probe.horizon,
            "type_count": probe.type_count,
            "types_by_depth": list(probe.types_by_depth),
        },
        "distinguishing_family": family,
        "zero_output": subset,
        "census_grows_in_depth": growing,
        "ahmed_savchuk_unrestricted_infinite": True,
        "nonregular_witnesses": [
            {
                "m": m,
                "n": n,
                "word": list(distinguishing_word(m)),
                "holds": distinction_holds(m, n),
            }
            for m in range(min(5, max_depth))
            for n in range(m + 1, min(6, max_depth + 1))
        ],
    }
