"""Exact Phase-0 census for s_bal(P(n))=0 on nonlinear polynomials.

The integer level set and the finite-prefix family E^{(k)} are different
objects. Joint states are pairs (residual, partial output sum). Remaining-
horizon signatures are the finite-horizon proxy for an LSD-first recognizer
of the exact finite-word language; a fixed-horizon quotient is not a
depth-independent automaton.

No CLI, visualization, or generic transducer package.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from itertools import product

from bt.calculus.residual import TRITS, delta, output_along, residual_along, rho, section_value
from bt.calculus.section import IntPoly, parse_poly
from bt.sequences import bt_digit_sum

MAX_DEPTH = 10
FAST_DEPTH = 4
SIGNATURE_HORIZON = 3
POLY_SPECS: tuple[tuple[str, str], ...] = (
    ("x^2", "x^2"),
    ("x^3", "x^3"),
    ("x^3-x", "x^3-x"),
    ("x^4", "x^4"),
    ("x^2+x", "x^2+x"),
)


def _require_horizon(n: int, name: str = "horizon") -> int:
    if isinstance(n, bool) or not isinstance(n, int) or n < 0:
        raise ValueError(f"{name} must be a nonnegative int")
    return n


def ordinary_s3(n: int) -> int:
    """Ordinary base-3 digit sum, digits in {0,1,2}."""

    if isinstance(n, bool) or not isinstance(n, int) or n < 0:
        raise ValueError("ordinary_s3 expects a nonnegative int")
    if n == 0:
        return 0
    total = 0
    while n:
        total += n % 3
        n //= 3
    return total


def translation_s_bal(n: int) -> int:
    """Integer translation: s_bal(n)=s_3(2|n|)-s_3(|n|) with oddness."""

    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("n must be int")
    if n < 0:
        return -translation_s_bal(-n)
    return ordinary_s3(2 * n) - ordinary_s3(n)


def translation_holds(n: int) -> bool:
    return bt_digit_sum(n) == translation_s_bal(n)


@dataclass(frozen=True)
class SumStateRow:
    """One residual path; not persisted for the full 3^k tree."""

    poly_id: str
    depth: int
    packed: int
    residual: tuple[int, ...]
    last_output: int | None
    partial_sum: int
    terminal: int
    exact_sum: int


def make_row(poly_id: str, f: IntPoly, word: tuple[int, ...]) -> SumStateRow:
    outs = output_along(f, word)
    residual = residual_along(f, word)
    packed = section_value(word)
    terminal = bt_digit_sum(residual.eval(0))
    partial = sum(outs)
    return SumStateRow(
        poly_id=poly_id,
        depth=len(word),
        packed=packed,
        residual=residual.coeffs,
        last_output=outs[-1] if outs else None,
        partial_sum=partial,
        terminal=terminal,
        exact_sum=partial + terminal,
    )


def terminal_correction_holds(f: IntPoly, word: tuple[int, ...]) -> bool:
    row = make_row("", f, word)
    return row.exact_sum == bt_digit_sum(f.eval(row.packed))


@lru_cache(maxsize=None)
def accept_signature(coeffs: tuple[int, ...], s: int, r: int) -> object:
    """Remaining-horizon right language of exact integer zero.

    accept(g, s) iff s + s_bal(g(0)) = 0. Trit a sends
    (g, s) to (D_a g, s + rho_a(g)).
    """

    r = _require_horizon(r)
    g = IntPoly(coeffs)
    if r == 0:
        return s + bt_digit_sum(g.eval(0)) == 0
    parts = []
    for a in TRITS:
        parts.append(accept_signature(delta(g, a).coeffs, s + rho(g, a), r - 1))
    return tuple(parts)


def _step_layer(
    layer: dict[tuple[tuple[int, ...], int], int],
) -> tuple[dict[tuple[tuple[int, ...], int], int], int, int, int]:
    nxt: dict[tuple[tuple[int, ...], int], int] = {}
    stay = leave = enter = 0
    for (coeffs, s), mult in layer.items():
        g = IntPoly(coeffs)
        old_zero = s == 0
        for a in TRITS:
            ns = s + rho(g, a)
            key = (delta(g, a).coeffs, ns)
            nxt[key] = nxt.get(key, 0) + mult
            new_zero = ns == 0
            if old_zero and new_zero:
                stay += mult
            elif old_zero and not new_zero:
                leave += mult
            else:
                if new_zero:
                    enter += mult
    return nxt, stay, leave, enter


def _layer_row(
    poly_id: str,
    f: IntPoly,
    depth: int,
    layer: dict[tuple[tuple[int, ...], int], int],
    stay: int,
    leave: int,
    enter: int,
    sig_horizon: int,
) -> dict[str, object]:
    residuals = {coeffs for (coeffs, _s) in layer}
    sums = [s for (_c, s) in layer]
    prefix_zeros = sum(mult for (_c, s), mult in layer.items() if s == 0)
    exact_zeros = 0
    nonnegative_exact = 0
    nonnegative_ordinary_zero = 0
    nonnegative_count = 0
    for (coeffs, s), mult in layer.items():
        terminal = bt_digit_sum(IntPoly(coeffs).eval(0))
        if s + terminal == 0:
            exact_zeros += mult
    # Ordinary comparison is on values n = pack(w), which the layer does
    # not store. Reconstructing every word is unnecessary for the
    # translation identity; the nonnegative slice is computed only at
    # the packed-window enumeration for small extra depths in report.
    sigs: set[object] = set()
    if sig_horizon >= 0:
        for coeffs, s in layer:
            sigs.add(accept_signature(coeffs, s, sig_horizon))
    return {
        "poly": poly_id,
        "depth": depth,
        "raw_prefixes": 3**depth,
        "residual_states": len(residuals),
        "partial_sum_min": min(sums) if sums else 0,
        "partial_sum_max": max(sums) if sums else 0,
        "distinct_partial_sums": len(set(sums)),
        "joint_states": len(layer),
        "prefix_zeros": prefix_zeros,
        "exact_zeros": exact_zeros,
        "stay_zero": stay,
        "leave_zero": leave,
        "enter_zero": enter,
        "signature_horizon": sig_horizon,
        "predictive_states": len(sigs),
        "nonnegative_count": nonnegative_count,
        "nonnegative_exact": nonnegative_exact,
        "nonnegative_ordinary_zero": nonnegative_ordinary_zero,
    }


def census_poly(
    poly_id: str,
    f: IntPoly,
    max_depth: int,
    sig_horizon: int = SIGNATURE_HORIZON,
) -> list[dict[str, object]]:
    max_depth = _require_horizon(max_depth, "max_depth")
    sig_horizon = _require_horizon(sig_horizon, "sig_horizon")
    layer: dict[tuple[tuple[int, ...], int], int] = {(f.coeffs, 0): 1}
    rows = [_layer_row(poly_id, f, 0, layer, 0, 0, 0, sig_horizon)]
    for depth in range(max_depth):
        layer, stay, leave, enter = _step_layer(layer)
        rows.append(
            _layer_row(poly_id, f, depth + 1, layer, stay, leave, enter, sig_horizon)
        )
    return rows


def ordinary_window_comparison(f: IntPoly, depth: int) -> dict[str, int]:
    """Exact integer comparison on the balanced window P_depth, n >= 0."""

    depth = _require_horizon(depth, "depth")
    exact = ordinary = translation_zeros = 0
    count = 0
    for word in product(TRITS, repeat=depth):
        n = section_value(word)
        if n < 0:
            continue
        count += 1
        value = f.eval(n)
        if bt_digit_sum(value) == 0:
            exact += 1
        if value >= 0 and ordinary_s3(value) == 0:
            ordinary += 1
        if translation_s_bal(value) == 0:
            translation_zeros += 1
    return {
        "depth": depth,
        "nonnegative_count": count,
        "exact_zeros": exact,
        "ordinary_s3_zeros": ordinary,
        "translation_zeros": translation_zeros,
    }


def first_exact_zeros(f: IntPoly, depth: int, limit: int = 12) -> list[int]:
    depth = _require_horizon(depth, "depth")
    found: list[int] = []
    for word in product(TRITS, repeat=depth):
        n = section_value(word)
        if bt_digit_sum(f.eval(n)) == 0:
            found.append(n)
            if len(found) >= limit:
                break
    return found


def distinguish_exact(
    f: IntPoly,
    prefix_a: tuple[int, ...],
    prefix_b: tuple[int, ...],
    bound: int,
) -> tuple[int, ...] | None:
    """A continuation that is an exact zero after exactly one prefix."""

    bound = _require_horizon(bound, "bound")
    for length in range(bound + 1):
        for tail in product(TRITS, repeat=length):
            za = bt_digit_sum(f.eval(section_value(prefix_a + tail))) == 0
            zb = bt_digit_sum(f.eval(section_value(prefix_b + tail))) == 0
            if za != zb:
                return tail
    return None


def prefix_one_then_zeros(m: int) -> tuple[int, ...]:
    m = _require_horizon(m, "m")
    return (1,) + (0,) * m


def x2_zero_family_search(max_m: int = 4, word_bound: int = 4) -> dict[str, object]:
    """Search 10^m prefixes of x^2 for exact-zero Myhill–Nerode witnesses."""

    f = parse_poly("x^2")
    max_m = _require_horizon(max_m, "max_m")
    word_bound = _require_horizon(word_bound, "word_bound")
    pairs = []
    missing = 0
    for i in range(max_m + 1):
        for j in range(i + 1, max_m + 1):
            tail = distinguish_exact(
                f, prefix_one_then_zeros(i), prefix_one_then_zeros(j), word_bound
            )
            if tail is None:
                missing += 1
            else:
                pairs.append({"m": i, "n": j, "tail": list(tail)})
    return {
        "family": "10^m",
        "max_m": max_m,
        "word_bound": word_bound,
        "distinguished_pairs": pairs,
        "undistinguished_pairs": missing,
    }


def triage_report(
    max_depth: int = FAST_DEPTH,
    sig_horizon: int = SIGNATURE_HORIZON,
    compare_depth: int | None = None,
) -> dict[str, object]:
    max_depth = _require_horizon(max_depth, "max_depth")
    sig_horizon = _require_horizon(sig_horizon, "sig_horizon")
    if compare_depth is None:
        compare_depth = min(6, max_depth)
    else:
        compare_depth = _require_horizon(compare_depth, "compare_depth")
    translation_ok = all(translation_holds(n) for n in range(-80, 81))
    correction_ok = True
    x2 = parse_poly("x^2")
    for word in product(TRITS, repeat=3):
        if not terminal_correction_holds(x2, word):
            correction_ok = False
            break
    census = {}
    for poly_id, text in POLY_SPECS:
        census[poly_id] = census_poly(poly_id, parse_poly(text), max_depth, sig_horizon)
    comparisons = {
        poly_id: ordinary_window_comparison(parse_poly(text), compare_depth)
        for poly_id, text in POLY_SPECS
    }
    zeros = {
        poly_id: first_exact_zeros(parse_poly(text), min(5, max_depth))
        for poly_id, text in POLY_SPECS
    }
    family = x2_zero_family_search(
        max_m=min(3, max_depth), word_bound=min(3, max_depth)
    )
    x2_rows = census["x^2"]
    joint_grows = any(
        x2_rows[k]["joint_states"] > x2_rows[k - 1]["joint_states"]
        for k in range(1, len(x2_rows))
    )
    pred_grows = any(
        x2_rows[k]["predictive_states"] > x2_rows[0]["predictive_states"]
        for k in range(1, len(x2_rows))
    )
    return {
        "max_depth": max_depth,
        "signature_horizon": sig_horizon,
        "compare_depth": compare_depth,
        "translation_identity": translation_ok,
        "terminal_correction": correction_ok,
        "census": census,
        "ordinary_comparison": comparisons,
        "sample_exact_zeros": zeros,
        "x2_prefix_family": family,
        "x2_joint_grows": joint_grows,
        "x2_predictive_grows": pred_grows,
        "monna_opened": False,
    }
