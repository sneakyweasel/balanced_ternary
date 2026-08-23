"""Deepest-layer fibres of the residual machine of ``x^3``.

At depth ``m = k-1`` the Newton coordinates collapse to

    N3 ≡ 0,  N2 ≡ 0,  N1 ≡ 3 p^2,  N0 = D^{k-1}(p^3)   (mod 3^k),

for ``k ≥ 2``.  Two prefixes ``p, q ∈ P_{k-1}`` collide iff

    p^2 ≡ q^2  (mod 3^{k-1})
    and
    D^{k-1}(p^3) ≡ D^{k-1}(q^3)  (mod 3^k).

The image count ``C_{k,k-1}`` is the number of distinct pairs
``(N1, N0)``.  High-valuation strata have a closed cube-count; the
unit stratum is ``2 · 3^{k-2}`` minus an explicit sign-pair surplus.
"""

from __future__ import annotations

from collections import Counter, defaultdict

from bt.calculus.cubic import F_k
from bt.calculus.cubic_fibres import balanced_bound, prefixes_at, zero_fibre_exponent
from bt.calculus.quadratic import iter_dz
from bt.metrics import v3


def _require_nat(n: int, name: str) -> int:
    if isinstance(n, bool) or not isinstance(n, int) or n < 0:
        raise ValueError(f"{name} must be a natural number")
    return n


def deepest_n1(p: int, k: int) -> int:
    """``N1 ≡ 3 p^2 (mod 3^k)`` at depth ``k-1``."""
    k = _require_nat(k, "k")
    mod = 3**k if k else 1
    return (3 * p * p) % mod


def deepest_n0(p: int, k: int) -> int:
    """``N0 = D^{k-1}(p^3) (mod 3^k)``."""
    k = _require_nat(k, "k")
    if k == 0:
        return 0
    return iter_dz(p**3, k - 1) % (3**k)


def deepest_phi(p: int, k: int) -> tuple[int, int]:
    """Surviving deepest-layer invariant ``(N1, N0)``."""
    return (deepest_n1(p, k), deepest_n0(p, k))


def deepest_F_k(p: int, k: int) -> tuple[int, int, int, int]:
    """Full Newton residue ``F_k(k-1, p)``."""
    k = _require_nat(k, "k")
    return F_k(k - 1 if k else 0, p, k)


def balanced_residue(n: int, m: int) -> int:
    """Unique representative of ``n`` in ``P_m``."""
    m = _require_nat(m, "m")
    if m == 0:
        return 0
    return n - 3**m * iter_dz(n, m)


def deepest_n0_decomp(p: int, k: int) -> int:
    """``(p^3 - bal_{k-1}(p^3)) / 3^{k-1}``."""
    k = _require_nat(k, "k")
    if k == 0:
        return 0
    m = k - 1
    return (p**3 - balanced_residue(p**3, m)) // (3**m)


def square_congruence(p: int, q: int, k: int) -> bool:
    """``p^2 ≡ q^2 (mod 3^{k-1})``."""
    k = _require_nat(k, "k")
    if k == 0:
        return True
    return (p * p - q * q) % (3 ** (k - 1)) == 0


def cubic_quotient_congruence(p: int, q: int, k: int) -> bool:
    """``D^{k-1}(p^3) ≡ D^{k-1}(q^3) (mod 3^k)``."""
    return deepest_n0(p, k) == deepest_n0(q, k)


def deepest_equiv(p: int, q: int, k: int) -> bool:
    """Exact same-depth fibre criterion at ``m = k-1``."""
    return square_congruence(p, q, k) and cubic_quotient_congruence(p, q, k)


def square_split(p: int, q: int) -> tuple[int, int]:
    """``(v3(p-q), v3(p+q))``, using ``99`` for a zero argument."""
    a = 99 if p == q else v3(p - q)
    b = 99 if p == -q else v3(p + q)
    return (a, b)


def cube_root_bound(k: int) -> int:
    """Largest ``T`` with ``T^3 ≤ (3^{k-1}-1)/2``."""
    k = _require_nat(k, "k")
    if k == 0:
        return 0
    B = balanced_bound(k - 1)
    t = 0
    while (t + 1) ** 3 <= B:
        t += 1
    return t


def small_unit_sign_count(k: int) -> int:
    """Positive units ``p ≤ T_k`` (automatically ``D^{k-1}(p^3) = 0``)."""
    t = cube_root_bound(k)
    return t - t // 3


def large_unit_sign_prefixes(k: int) -> list[int]:
    """Positive units ``p > T_k`` with ``3^k | D^{k-1}(p^3)``."""
    k = _require_nat(k, "k")
    if k <= 1:
        return []
    m = k - 1
    B = balanced_bound(m)
    T = cube_root_bound(k)
    pow_hi = 3 ** (2 * k - 1)
    if pow_hi == 0:
        return []
    tmax = B**3 // pow_hi
    found: set[int] = set()
    for t in range(1, tmax + 1):
        target = t * pow_hi
        root = round(target ** (1 / 3))
        for cand in range(root - 2, root + 3):
            if T < cand <= B and cand % 3 and abs(cand**3 - target) <= B:
                if iter_dz(cand**3, m) % (3**k) == 0:
                    found.add(cand)
    return sorted(found)


def unit_sign_surplus(k: int) -> int:
    """``S_{k,0}``: number of positive unit sign-pairs."""
    return small_unit_sign_count(k) + len(large_unit_sign_prefixes(k))


def unit_stratum_count(k: int) -> int:
    """``I_{k,0} = 2 · 3^{k-2} - S_{k,0}`` for ``k ≥ 2``."""
    k = _require_nat(k, "k")
    if k < 2:
        return 1 if k == 1 else 0
    return 2 * 3 ** (k - 2) - unit_sign_surplus(k)


def high_s0(k: int) -> int:
    """``ceil((k-1)/2)``."""
    return k // 2


def unit_cubes_mod(nu: int) -> int:
    """Number of cubes in ``(Z/3^ν Z)*``."""
    if nu <= 0:
        return 1
    if nu == 1:
        return 2
    return 2 * 3 ** (nu - 2)


def high_stratum_count(k: int, s: int) -> int:
    """Closed ``I_{k,s}`` for ``ceil((k-1)/2) ≤ s < ceil((2k-1)/3)``."""
    k = _require_nat(k, "k")
    s = _require_nat(s, "s")
    nu = 2 * k - 1 - 3 * s
    mu = k - 1 - s
    if 2 * s == k - 1:
        return 2 * 3 ** (mu - 1) if mu >= 1 else 0
    return unit_cubes_mod(nu)


def deepest_class_count(k: int) -> int:
    """``C_{k,k-1}`` by hashing the deepest invariant (not the automaton)."""
    k = _require_nat(k, "k")
    if k == 0:
        return 0
    if k == 1:
        return 1
    return len({deepest_phi(p, k) for p in prefixes_at(k - 1)})


def deepest_image(k: int) -> dict[tuple[int, int], list[int]]:
    buckets: dict[tuple[int, int], list[int]] = defaultdict(list)
    for p in prefixes_at(k - 1):
        buckets[deepest_phi(p, k)].append(p)
    return buckets


def zero_fibre(k: int) -> list[int]:
    """Prefixes in the deepest fibre of ``0``."""
    k = _require_nat(k, "k")
    if k == 0:
        return [0]
    r = zero_fibre_exponent(k)
    return [p for p in prefixes_at(k - 1) if p % (3**r) == 0]


def zero_fibre_size(k: int) -> int:
    k = _require_nat(k, "k")
    if k == 0:
        return 1
    r = zero_fibre_exponent(k)
    return 3 ** (k - 1 - r)


def is_full_coset(ps: list[int], m: int) -> tuple[bool, int | None]:
    """Whether ``ps`` is a single full residue class ``α + 3^r P_{m-r}``."""
    if len(ps) <= 1:
        return True, 0
    diffs = [v3(a - b) for i, a in enumerate(ps) for b in ps[:i] if a != b]
    r = min(diffs) if diffs else 0
    if r <= 0:
        return False, r
    w = balanced_bound(m)
    residue = ps[0] % (3**r)
    expected = [p for p in range(-w, w + 1) if p % (3**r) == residue]
    return ps == expected, r


def fibre_kind(ps: list[int], m: int) -> str:
    """Coarse label: singleton, sign, zero-coset, translate-coset, twin, other."""
    xs = sorted(ps)
    if len(xs) == 1:
        return "singleton"
    if len(xs) == 2 and xs[0] == -xs[1]:
        return "sign"
    full, r = is_full_coset(xs, m)
    if full and r is not None and r > 0:
        if all(p % (3**r) == 0 for p in xs):
            return "zero-coset"
        return "translate-coset"
    if len(xs) == 2:
        mid = (xs[0] + xs[1]) // 2
        half = (xs[1] - xs[0]) // 2
        if mid != 0 and v3(abs(mid)) >= 1 and v3(half) >= 1:
            return "twin"
    return "other"


def deepest_fibres(k: int) -> list[list[int]]:
    return [sorted(ps) for ps in deepest_image(k).values() if len(ps) > 1]


def C_km_neighbors(k: int) -> dict[str, int]:
    """Diagnostic: ``C_{k,k-1}``, ``C_{k,k-2}``, ``C_{k,k-3}`` via ``F_k``."""
    from bt.calculus.cubic_fibres import C_km

    out = {"C_k_k-1": deepest_class_count(k)}
    if k >= 2:
        out["C_k_k-2"] = C_km(k, k - 2)
    if k >= 3:
        out["C_k_k-3"] = C_km(k, k - 3)
    return out


def deepest_report(k: int) -> dict[str, object]:
    """CLI payload for ``cubic-deepest``."""
    k = _require_nat(k, "k")
    image = deepest_image(k)
    C = len(image)
    raw = 3 ** (k - 1) if k else 1
    fibres = [sorted(ps) for ps in image.values() if len(ps) > 1]
    hist = dict(sorted(Counter(len(v) for v in image.values()).items()))
    kinds = Counter(fibre_kind(sorted(ps), k - 1) for ps in image.values())
    largest = max((len(ps) for ps in image.values()), default=1)
    z = zero_fibre(k)
    examples = []
    for ps in sorted(fibres, key=lambda xs: (len(xs), xs[0]))[:12]:
        examples.append(ps)
    return {
        "k": k,
        "raw": raw,
        "C": C,
        "n_fibres": len(fibres),
        "histogram": hist,
        "kinds": dict(kinds),
        "zero_fibre_size": len(z),
        "zero_formula": zero_fibre_size(k),
        "largest_fibre": largest,
        "unit_sign_surplus": unit_sign_surplus(k) if k >= 2 else 0,
        "small_unit_signs": small_unit_sign_count(k) if k >= 2 else 0,
        "large_unit_signs": large_unit_sign_prefixes(k) if k >= 2 else [],
        "examples": examples,
    }


def deepest_fibre_of(p: int, k: int) -> list[int]:
    """Deepest-layer fibre of a single prefix ``p ∈ P_{k-1}``."""
    k = _require_nat(k, "k")
    if not abs(p) <= balanced_bound(k - 1) if k else p == 0:
        raise ValueError(f"p={p} is not a packed prefix of width {k - 1}")
    target = deepest_phi(p, k)
    return [q for q in prefixes_at(k - 1) if deepest_phi(q, k) == target]
