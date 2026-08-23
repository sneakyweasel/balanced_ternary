"""Newton-class image of the cubic residual machine of ``x^3``.

Along an LSD-first trit word ``w`` of length ``m`` with packed prefix
``p = p(w)``,

    f_w(x) = 3^{2m} x^3 + 3^{m+1} p x^2 + 3 p^2 x + D^m(p^3)
           = D^m( (p + 3^m x)^3 ).

The finite-horizon class is the Newton residue ``Φ_k(f_w)``. Then

    M_k(x^3) = |{ Φ_k(f_w) : |w| < k }| = |Im F_k|

where ``F_k(m, p)`` is the explicit 4-tuple below. Distinct words give
distinct ordinary polynomials, so ``R_k(x^3) = (3^k-1)/2``.
"""

from __future__ import annotations

from collections import defaultdict
from itertools import product

from bt.calculus.poly_congruence import newton_coeffs, pad_phi, phi_k
from bt.calculus.quadratic import iter_dz, pack_word
from bt.calculus.residual import TRITS
from bt.calculus.section import IntPoly
from bt.metrics import v3


def _require_nat(n: int, name: str) -> int:
    if isinstance(n, bool) or not isinstance(n, int) or n < 0:
        raise ValueError(f"{name} must be a natural number")
    return n


def balanced_bound(m: int) -> int:
    """Half-width of ``P_m``: ``(3^m-1)/2``."""
    m = _require_nat(m, "m")
    return (3**m - 1) // 2


def is_balanced_width(m: int, p: int) -> bool:
    """``p`` is a packed prefix of some length-``m`` trit word."""
    return abs(p) <= balanced_bound(m)


def prefixes_at(m: int) -> range:
    """Integers ``P_m`` as a contiguous symmetric interval."""
    w = balanced_bound(m)
    return range(-w, w + 1)


def cubic_coeffs(m: int, p: int) -> tuple[int, int, int, int]:
    """Monomial ``(A, B, C, D)`` of the residual of ``x^3`` at depth ``m``."""
    m = _require_nat(m, "m")
    return (3 ** (2 * m), 3 ** (m + 1) * p, 3 * p * p, iter_dz(p ** 3, m))


def cubic_residual_formula(word: tuple[int, ...]) -> IntPoly:
    """Closed form of the residual of ``x^3`` along ``word``."""
    m = len(word)
    p = pack_word(word)
    A, B, C, D = cubic_coeffs(m, p)
    return IntPoly((D, C, B, A))


def newton_from_monomial(A: int, B: int, C: int, D: int) -> tuple[int, int, int, int]:
    """``(N0, N1, N2, N3) = (Δ^j q(0))_{j=0..3}`` of ``A x^3 + B x^2 + C x + D``."""
    return (D, A + B + C, 6 * A + 2 * B, 6 * A)


def newton_of_residual(m: int, p: int) -> tuple[int, int, int, int]:
    """Newton coordinates of the residual of ``x^3`` with packed prefix ``p``."""
    A, B, C, D = cubic_coeffs(m, p)
    return newton_from_monomial(A, B, C, D)


def F_k(m: int, p: int, k: int) -> tuple[int, int, int, int]:
    """Arithmetic image map: Newton residues of the ``(m, p)`` residual."""
    k = _require_nat(k, "k")
    mod = 3**k if k else 1
    return tuple(n % mod for n in newton_of_residual(m, p))


def section_monomial_step(A: int, B: int, C: int, D: int, a: int) -> tuple[int, int, int, int]:
    """Coefficient step of ``𝔇_a`` on ``A x^3 + B x^2 + C x + D``.

    The linear coefficient of ``f(a+3x)`` is ``9A a^2 + 6B a + 3C``, so
    the residual linear term is ``3A a^2 + 2B a + C`` with no extra
    divisibility hypothesis.
    """
    val = A * a ** 3 + B * a ** 2 + C * a + D
    from bt.normtheory.rewrite import balanced_divmod

    _rho, q = balanced_divmod(val)
    return (9 * A, 9 * A * a + 3 * B, 3 * A * a * a + 2 * B * a + C, q)


def newton_section_step(N: tuple[int, int, int, int], a: int) -> tuple[int, int, int, int]:
    """Newton-coordinate section step, via the monomial recurrence."""
    N0, N1, N2, N3 = N
    if N3 % 6 != 0 or (N2 - N3) % 2 != 0:
        raise ValueError("Newton tuple is not the image of a Z[x] cubic")
    A = N3 // 6
    B = (N2 - N3) // 2
    C = N1 - A - B
    D = N0
    A2, B2, C2, D2 = section_monomial_step(A, B, C, D, a)
    return newton_from_monomial(A2, B2, C2, D2)


def newton_section_step_closed(m: int, p: int, a: int) -> tuple[int, int, int, int]:
    """Exact Newton image of ``𝔇_a`` on the ``(m, p)`` residual of ``x^3``."""
    return newton_of_residual(m + 1, p + 3**m * a)


def prefixes(k: int):
    """All ``(word, m, p)`` with ``|w| < k``."""
    k = _require_nat(k, "k")
    for m in range(k):
        words = product(TRITS, repeat=m) if m else ((),)
        for word in words:
            yield word, m, pack_word(word)


def raw_count_x3(k: int) -> int:
    """``R_k(x^3) = (3^k-1)/2`` for ``k≥1``; empty domain at ``k=0``."""
    k = _require_nat(k, "k")
    if k == 0:
        return 0
    return (3**k - 1) // 2


def newton_image(k: int) -> dict[tuple[int, int, int, int], list[tuple[tuple[int, ...], int, int]]]:
    """Map ``Φ_k(f_w) →`` list of ``(word, m, p)`` realizing it, ``|w| < k``."""
    k = _require_nat(k, "k")
    buckets: dict[tuple[int, int, int, int], list[tuple[tuple[int, ...], int, int]]] = defaultdict(list)
    for word, m, p in prefixes(k):
        buckets[F_k(m, p, k)].append((word, m, p))
    return buckets


def M_k_x3(k: int) -> int:
    """``M_k(x^3)`` as the cardinality of the Newton image."""
    return len(newton_image(k))


def shallow_lower_bound(k: int) -> int:
    """Number of residuals with ``2m+1 < k``; these are ``≡_k``-separated.

    For those depths ``N3 = 2·3^{2m+1}`` is a distinct nonzero residue, and
    ``N2`` recovers ``p`` completely.
    """
    k = _require_nat(k, "k")
    if k <= 1:
        return 1
    r = (k - 2) // 2
    return (3 ** (r + 1) - 1) // 2


def same_depth_collide(m: int, p: int, q: int, k: int) -> bool:
    """Exact same-depth collision criterion for residuals of ``x^3``."""
    k = _require_nat(k, "k")
    m = _require_nat(m, "m")
    if k == 0:
        return True
    return F_k(m, p, k) == F_k(m, q, k)


def collision_classes(k: int) -> list[list[tuple[tuple[int, ...], int, int]]]:
    """Newton classes with at least two residual words."""
    return [members for members in newton_image(k).values() if len(members) > 1]


def newton_class_table(f: IntPoly, k: int) -> list[dict[str, object]]:
    """CLI rows: word, polynomial, Newton coordinates, class id."""
    k = _require_nat(k, "k")
    from bt.calculus.residual import residual_along

    rows: list[dict[str, object]] = []
    class_id: dict[tuple[int, ...], int] = {}
    for word, m, p in prefixes(k):
        poly = residual_along(f, word)
        newt = newton_coeffs(poly)
        ph = pad_phi(phi_k(poly, k), max(4, len(newton_coeffs(poly))))
        if ph not in class_id:
            class_id[ph] = len(class_id)
        rows.append(
            {
                "word": list(word),
                "m": m,
                "p": p,
                "poly": poly.render(),
                "newton": list(newt),
                "phi": list(ph),
                "class_id": class_id[ph],
            }
        )
    return rows


def collision_table(f: IntPoly, k: int) -> list[dict[str, object]]:
    """Collision classes of ``f`` at horizon ``k``."""
    groups: dict[tuple[int, ...], list[dict[str, object]]] = defaultdict(list)
    for row in newton_class_table(f, k):
        groups[tuple(row["phi"])].append(row)
    out = []
    for phi, members in groups.items():
        if len(members) < 2:
            continue
        out.append(
            {
                "phi": list(phi),
                "size": len(members),
                "members": members,
            }
        )
    return out


def tau_sign_pair(m: int, p: int) -> int | None:
    """``τ`` of the odd pair ``(m, p)`` vs ``(m, -p)``, or ``None`` if ``p = 0``."""
    if p == 0:
        return None
    n0, n1, n2, n3 = newton_of_residual(m, p)
    n0b, n1b, n2b, n3b = newton_of_residual(m, -p)
    diffs = (n0 - n0b, n1 - n1b, n2 - n2b, n3 - n3b)
    vals = [v3(d) for d in diffs if d != 0]
    if not vals:
        return None
    return min(vals) + 1


def image_profile(k: int) -> dict[str, object]:
    """Summary row for one horizon."""
    k = _require_nat(k, "k")
    R = raw_count_x3(k)
    M = M_k_x3(k)
    return {
        "k": k,
        "R": R,
        "M": M,
        "collisions": R - M,
        "ratio": (M / R) if R else None,
        "shallow_lower": shallow_lower_bound(k),
        "n_collision_classes": len(collision_classes(k)),
    }
