"""Exact Phase-0 tests for balanced-Monna endpoint pairs and jump depths.

The balanced Monna map reads a 3-adic expansion sum a_i 3^i as the real
series sum a_i 3^{-i-1}. Endpoint pairs are the two expansions of one
real value: a common finite prefix, one boundary digit, and opposite
infinite tails. They are not Collatz 3-adic endpoints and not
``bt_reverse``.

All real and 3-adic values are ``fractions.Fraction``. No floating
point is used.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from itertools import product

from bt.calculus.residual import TRITS
from bt.calculus.section import IntPoly, parse_poly
from bt.metrics import v3

MAX_N = 5
INF = None

X = parse_poly("x")
NEG_X = parse_poly("-x")
X3 = parse_poly("x^3")
TWICE_PLUS = parse_poly("2x+1")
PLUS_ONE = parse_poly("x+1")


def _require_n(n: int) -> int:
    if isinstance(n, bool) or not isinstance(n, int) or n < 0:
        raise ValueError("n must be a nonnegative int")
    return n


def pack_word(word: tuple[int, ...]) -> int:
    acc = 0
    pow3 = 1
    for a in word:
        if a not in TRITS:
            raise ValueError(f"prefix digit must be a trit, got {a}")
        acc += a * pow3
        pow3 *= 3
    return acc


def monna_prefix(word: tuple[int, ...]) -> Fraction:
    total = Fraction(0)
    pow3 = Fraction(1, 3)
    for a in word:
        total += a * pow3
        pow3 /= 3
    return total


def balanced_residue_frac(x: Fraction) -> int:
    """Balanced residue of a 3-adic integer represented as a rational."""

    den = x.denominator
    if den % 3 == 0:
        raise ValueError(f"{x} is not a 3-adic integer")
    inv = pow(den % 3, -1, 3)
    r = (x.numerator * inv) % 3
    return -1 if r == 2 else r


def v3_frac(x: Fraction) -> int | None:
    if x == 0:
        return None
    n = abs(x.numerator)
    d = abs(x.denominator)
    vn = 0
    while n % 3 == 0:
        n //= 3
        vn += 1
    vd = 0
    while d % 3 == 0:
        d //= 3
        vd += 1
    return vn - vd


def monna_value(x: Fraction, max_digits: int = 96) -> Fraction:
    """Exact balanced Monna value of a 3-adic rational integer."""

    total = Fraction(0)
    weight = Fraction(1, 3)
    seen: dict[tuple[int, int], tuple[int, Fraction, Fraction]] = {}
    for i in range(max_digits):
        key = (x.numerator, x.denominator)
        if key in seen:
            start, start_total, start_weight = seen[key]
            period = i - start
            period_sum = total - start_total
            ratio = Fraction(1) - Fraction(1, 3**period)
            return start_total + period_sum / ratio
        seen[key] = (i, total, weight)
        if x == 0:
            return total
        a = balanced_residue_frac(x)
        total += a * weight
        x = (x - a) / 3
        weight /= 3
    raise RuntimeError("Monna expansion did not cycle or terminate")


@dataclass(frozen=True)
class EndpointPair:
    """One balanced-Monna fibre over a triadic real.

    ``kind='plus'``: prefix, then (+, ---...) versus (0, +++...).
    ``kind='minus'``: prefix, then (0, ---...) versus (-, +++...).
    """

    n: int
    prefix: tuple[int, ...]
    kind: str

    def __post_init__(self) -> None:
        if self.n != len(self.prefix):
            raise ValueError("prefix length must equal n")
        if self.kind not in ("plus", "minus"):
            raise ValueError(f"unknown endpoint kind {self.kind!r}")

    @property
    def pack(self) -> int:
        return pack_word(self.prefix)

    def values(self) -> tuple[Fraction, Fraction]:
        half = Fraction(3 ** (self.n + 1), 2)
        pack = Fraction(self.pack)
        if self.kind == "plus":
            u = pack + Fraction(3**self.n) + half
            v = pack - half
        else:
            u = pack + half
            v = pack - Fraction(3**self.n) - half
        return u, v

    def midpoint(self) -> Fraction:
        u, v = self.values()
        return (u + v) / 2

    def monna(self) -> Fraction:
        return monna_value(self.values()[0])


def iterate_pairs(n: int) -> list[EndpointPair]:
    n = _require_n(n)
    prefixes = [()] if n == 0 else list(product(TRITS, repeat=n))
    return [EndpointPair(n, prefix, kind) for prefix in prefixes for kind in ("plus", "minus")]


def difference_is_four_pow(pair: EndpointPair) -> bool:
    u, v = pair.values()
    return u - v == 4 * 3**pair.n


def cubic_difference_formula(pair: EndpointPair) -> Fraction:
    zeta = pair.midpoint()
    return 4 * 3**pair.n * (3 * zeta * zeta + 4 * 3 ** (2 * pair.n))


def predicted_divergence_depth(pair: EndpointPair) -> int:
    """t = n + min(1 + 2 v_3(zeta), 2n), or 3n when zeta = 0."""

    n = pair.n
    zeta = pair.midpoint()
    s = v3_frac(zeta)
    if s is None:
        return 3 * n
    return n + min(1 + 2 * s, 2 * n)


def eval_poly(f: IntPoly, x: Fraction) -> Fraction:
    acc = Fraction(0)
    pow_x = Fraction(1)
    for c in f.coeffs:
        acc += c * pow_x
        pow_x *= x
    return acc


def padic_divergence_depth(f: IntPoly, pair: EndpointPair) -> int | None:
    u, v = pair.values()
    return v3_frac(eval_poly(f, u) - eval_poly(f, v))


def euclidean_jump(f: IntPoly, pair: EndpointPair) -> Fraction:
    u, v = pair.values()
    return abs(monna_value(eval_poly(f, u)) - monna_value(eval_poly(f, v)))


def preserves_pair(f: IntPoly, pair: EndpointPair) -> bool:
    return euclidean_jump(f, pair) == 0


def endpoint_normal_form(x: Fraction, y: Fraction) -> bool:
    """True if {x, y} is equal or is some constructed endpoint pair."""

    if x == y:
        return True
    diff = abs(x - y)
    if diff.denominator != 1:
        return False
    d = diff.numerator
    # 4 * 3^k
    if d % 4 != 0:
        return False
    rest = d // 4
    k = 0
    while rest % 3 == 0:
        rest //= 3
        k += 1
    if rest != 1:
        return False
    mid = (x + y) / 2
    # Reconstruct both kinds at this k and see if the unordered pair matches.
    # Prefix is not needed: values are determined by midpoint and kind.
    # mid = pack ± 3^k / 2, pack in the balanced window.
    for sign in (1, -1):
        pack = mid - sign * Fraction(3**k, 2)
        if pack.denominator != 1:
            continue
        p = pack.numerator
        window = (3**k - 1) // 2 if k else 0
        if k == 0:
            if p != 0:
                continue
        elif abs(p) > window:
            continue
        # Rebuild the pair of that kind.
        kind = "plus" if sign == 1 else "minus"
        # Recover any prefix with this packed value.
        prefix = _prefix_from_pack(p, k)
        cand = EndpointPair(k, prefix, kind)
        a, b = cand.values()
        if {a, b} == {x, y}:
            return True
    return False


def _prefix_from_pack(p: int, n: int) -> tuple[int, ...]:
    if n == 0:
        return ()
    digits: list[int] = []
    cur = p
    for _ in range(n):
        from bt.normtheory.rewrite import balanced_divmod

        r, cur = balanced_divmod(cur)
        digits.append(r)
    return tuple(digits)


def affine_controls() -> dict[str, IntPoly]:
    return {
        "x": X,
        "-x": NEG_X,
        "0": parse_poly("0"),
        "1": parse_poly("1"),
        "x+1": PLUS_ONE,
        "2x+1": TWICE_PLUS,
    }


@lru_cache(maxsize=None)
def control_preservation(max_n: int = MAX_N) -> dict[str, dict[str, object]]:
    max_n = _require_n(max_n)
    out: dict[str, dict[str, object]] = {}
    for name, f in affine_controls().items():
        preserved = 0
        total = 0
        jumps: list[str] = []
        for n in range(max_n + 1):
            for pair in iterate_pairs(n):
                total += 1
                if preserves_pair(f, pair):
                    preserved += 1
                elif len(jumps) < 4:
                    jumps.append(f"n={n},{pair.kind},{pair.prefix}")
        out[name] = {
            "preserved": preserved,
            "total": total,
            "all_preserved": preserved == total,
            "jump_samples": jumps,
        }
    return out


def cubic_census(max_n: int = MAX_N) -> dict[str, object]:
    max_n = _require_n(max_n)
    rows: list[dict[str, object]] = []
    mismatches = 0
    preservations = 0
    formula_fails = 0
    depths: dict[int, int] = {}
    for n in range(max_n + 1):
        for pair in iterate_pairs(n):
            u, v = pair.values()
            left = eval_poly(X3, u) - eval_poly(X3, v)
            formula = cubic_difference_formula(pair)
            if left != formula:
                formula_fails += 1
            pred = predicted_divergence_depth(pair)
            actual = padic_divergence_depth(X3, pair)
            if actual != pred:
                mismatches += 1
            jump = euclidean_jump(X3, pair)
            preserved = jump == 0
            if preserved:
                preservations += 1
            images_endpoint = endpoint_normal_form(eval_poly(X3, u), eval_poly(X3, v))
            depths[pred] = depths.get(pred, 0) + 1
            rows.append(
                {
                    "n": n,
                    "kind": pair.kind,
                    "prefix": list(pair.prefix),
                    "predicted": pred,
                    "actual": actual,
                    "jump_zero": preserved,
                    "images_endpoint": images_endpoint,
                }
            )
    image_endpoint_count = sum(1 for row in rows if row["images_endpoint"])
    return {
        "max_n": max_n,
        "pair_count": len(rows),
        "formula_fails": formula_fails,
        "depth_mismatches": mismatches,
        "preservations": preservations,
        "depth_histogram": {str(k): v for k, v in sorted(depths.items())},
        "image_endpoint_count": image_endpoint_count,
    }


def spectrum_counts(n: int) -> dict[int, int]:
    """Exact predicted multiplicity of each depth at a fixed n."""

    n = _require_n(n)
    counts: dict[int, int] = {}
    for pair in iterate_pairs(n):
        t = predicted_divergence_depth(pair)
        counts[t] = counts.get(t, 0) + 1
    return counts


def predicted_spectrum_closed_form(n: int) -> dict[int, int]:
    """Closed count of depths at level n, both boundary kinds.

    For a nonzero prefix of valuation s < n the depth is n+1+2s.
    There are 2 * 2 * 3^{n-s-1} such prefixes of exact valuation s
    (two signs of the first nonzero trit, two kinds, free higher digits),
    plus two all-zero prefixes (the empty higher digits) giving depth 3n
    when n>=1, one for each kind. At n=0 the unique empty prefix has
    midpoint ±1/2 of valuation 0, so depth min(1,0)+0 wait: zeta=±1/2,
    v3=0, depth = 0 + min(1, 0) = 0? 

    n=0, zeta = ± 3^0 / 2 = ±1/2, v3(1/2)=0, t = 0 + min(1, 0) = 0.

    But u^3-v^3 at n=0: 4*(3ζ²+4). ζ=±1/2, 3/4+4 = 19/4, times 4 = 19,
    v3(19)=0. Yes depth 0.

    The all-zero prefix at n>=1 has zeta = ± 3^n / 2, v3=n, t=n+min(1+2n,2n)=3n.
    Two kinds, so 2 pairs of depth 3n.

    Prefixes with exact val s < n: first nonzero at position s, 2 choices
    for that trit, 3^{n-s-1} free digits after? Positions s+1..n-1 are
    free (n-s-1 positions), position s nonzero (2 choices). Times 2 kinds.
    Count: 2 * 2 * 3^{n-s-1} = 4 * 3^{n-s-1}.
    """

    n = _require_n(n)
    if n == 0:
        return {0: 2}
    out: dict[int, int] = {3 * n: 2}
    for s in range(n):
        depth = n + 1 + 2 * s
        out[depth] = out.get(depth, 0) + 4 * 3 ** (n - s - 1)
    return out


def triage_report(max_n: int = MAX_N) -> dict[str, object]:
    max_n = _require_n(max_n)
    identity_ok = True
    for n in range(max_n + 1):
        if spectrum_counts(n) != predicted_spectrum_closed_form(n):
            identity_ok = False
            break
    cubic = cubic_census(max_n)
    controls = control_preservation(max_n)
    return {
        "max_n": max_n,
        "difference_four": all(
            difference_is_four_pow(pair) for n in range(max_n + 1) for pair in iterate_pairs(n)
        ),
        "monna_collision": all(
            monna_value(pair.values()[0]) == monna_value(pair.values()[1])
            for n in range(min(3, max_n) + 1)
            for pair in iterate_pairs(n)
        ),
        "spectrum_formula_matches_enumeration": identity_ok,
        "cubic": cubic,
        "controls": controls,
        "x_preserves": controls["x"]["all_preserved"],
        "neg_x_preserves": controls["-x"]["all_preserved"],
        "constants_preserve": controls["0"]["all_preserved"] and controls["1"]["all_preserved"],
        "twice_plus_preserves": controls["2x+1"]["all_preserved"],
        "x3_preserves_any": cubic["preservations"] > 0,
    }
