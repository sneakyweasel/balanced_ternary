"""Integer polynomials attached to canonical balanced-ternary words.

``P_n(x) = sum_i a_i x^i`` with ``a_i in {-1,0,+1}`` and ``P_n(3) = n``.
Factorization is in ``Z[x]`` and is not a factorization of the integer
``P_n(3)``.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from bt.metrics import signed_digit_sum, weight
from bt.sequences import bt_alternating_digit_sum, bt_is_palindrome
from bt.representation import digits, encode


def _require_int(n: int, name: str = "n") -> int:
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"{name} must be int, got {type(n).__name__}")
    return n


def _strip(coeffs: tuple[int, ...]) -> tuple[int, ...]:
    i = len(coeffs)
    while i > 1 and coeffs[i - 1] == 0:
        i -= 1
    return coeffs[:i] if i else (0,)


def _add(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    n = max(len(a), len(b))
    out = [0] * n
    for i, c in enumerate(a):
        out[i] += c
    for i, c in enumerate(b):
        out[i] += c
    return _strip(tuple(out))


def _sub(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    return _add(a, tuple(-c for c in b))


def _mul(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    if a == (0,) or b == (0,):
        return (0,)
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x == 0:
            continue
        for j, y in enumerate(b):
            out[i + j] += x * y
    return _strip(tuple(out))


def _divmod_poly(
    num: tuple[int, ...], den: tuple[int, ...]
) -> tuple[tuple[int, ...], tuple[int, ...]] | None:
    """Polynomial division over ``Q``, returning ``Z`` quotient/remainder if exact over ``Q``
    and the quotient happens to lie in ``Z[x]`` with remainder in ``Z[x]``.
    """
    den = _strip(den)
    num_f = [Fraction(c) for c in _strip(num)]
    den_f = [Fraction(c) for c in den]
    if den_f == [Fraction(0)]:
        raise ZeroDivisionError("polynomial division by zero")
    quot_f = [Fraction(0)] * max(1, len(num_f) - len(den_f) + 1)
    while len(num_f) >= len(den_f) and any(num_f):
        lead = num_f[-1] / den_f[-1]
        deg = len(num_f) - len(den_f)
        if deg >= len(quot_f):
            quot_f.extend([Fraction(0)] * (deg + 1 - len(quot_f)))
        quot_f[deg] += lead
        for i, c in enumerate(den_f):
            num_f[deg + i] -= lead * c
        while len(num_f) > 1 and num_f[-1] == 0:
            num_f.pop()
        if num_f == [Fraction(0)]:
            break
    def to_int(cs: list[Fraction]) -> tuple[int, ...] | None:
        out = []
        for c in cs:
            if c.denominator != 1:
                return None
            out.append(int(c.numerator))
        return _strip(tuple(out))

    q = to_int(quot_f)
    r = to_int(num_f)
    if q is None or r is None:
        return None
    return q, r


def _cyclotomic(n: int) -> tuple[int, ...]:
    """``Φ_n`` for ``1 <= n <= 12`` as LSD-first integer coefficients."""
    table = {
        1: (-1, 1),
        2: (1, 1),
        3: (1, 1, 1),
        4: (1, 0, 1),
        5: (1, 1, 1, 1, 1),
        6: (1, -1, 1),
        7: (1, 1, 1, 1, 1, 1, 1),
        8: (1, 0, 0, 0, 1),
        9: (1, 0, 0, 1, 0, 0, 1),
        10: (1, -1, 1, -1, 1),
        12: (1, 0, -1, 0, 1),
    }
    if n not in table:
        raise ValueError(f"cyclotomic Φ_{n} is not in the small table")
    return table[n]


@dataclass(frozen=True)
class BTPolynomial:
    """LSD-first coefficients ``(a_0, a_1, ..., a_d)``."""

    coeffs: tuple[int, ...]

    def __post_init__(self) -> None:
        stripped = _strip(self.coeffs)
        object.__setattr__(self, "coeffs", stripped)
        for c in stripped:
            if c not in (-1, 0, 1):
                raise ValueError(f"coefficient {c} is not a balanced trit")

    @property
    def degree(self) -> int:
        if self.coeffs == (0,):
            return -1
        return len(self.coeffs) - 1

    def evaluate(self, x: int) -> int:
        acc = 0
        pow_x = 1
        for a in self.coeffs:
            acc += a * pow_x
            pow_x *= x
        return acc

    def support(self) -> tuple[int, ...]:
        return tuple(i for i, a in enumerate(self.coeffs) if a != 0)

    def coefficient_weight(self) -> int:
        return sum(abs(a) for a in self.coeffs)

    def reverse_polynomial(self) -> "BTPolynomial":
        """Coefficient reverse without padding: ``(a_d, ..., a_0)`` as LSD-first of the reverse word."""
        return BTPolynomial(tuple(reversed(self.coeffs)))

    def reciprocal_polynomial(self) -> "BTPolynomial":
        """``x^d P(1/x)``, LSD-first. Zero polynomial stays zero."""
        if self.degree < 0:
            return self
        return BTPolynomial(tuple(reversed(self.coeffs)))

    def is_palindromic(self) -> bool:
        return self.coeffs == tuple(reversed(self.coeffs))

    def is_reciprocal(self) -> bool:
        return self.coeffs == tuple(reversed(self.coeffs))

    def divides_value(self, x: int) -> bool:
        return self.evaluate(x) == 0

def polynomial(n: int) -> BTPolynomial:
    return BTPolynomial(digits(encode(_require_int(n))))


def evaluate(poly: BTPolynomial, x: int) -> int:
    return poly.evaluate(x)


def reverse_polynomial(poly: BTPolynomial) -> BTPolynomial:
    return poly.reverse_polynomial()


def reciprocal_polynomial(poly: BTPolynomial) -> BTPolynomial:
    return poly.reciprocal_polynomial()


def support(poly: BTPolynomial) -> tuple[int, ...]:
    return poly.support()


def degree(poly: BTPolynomial) -> int:
    return poly.degree


def coefficient_weight(poly: BTPolynomial) -> int:
    return poly.coefficient_weight()


def is_palindromic(poly: BTPolynomial) -> bool:
    return poly.is_palindromic()


def factor_small(poly: BTPolynomial) -> tuple[str, ...]:
    """Trial division by ``x-1``, ``x+1``, and small cyclotomics.

    Factors are reported as strings. Coefficients of a factor in ``Z[x]``
    need not lie in ``{-1,0,+1}``; those cases are named, not reconstructed
    as ``BTPolynomial``.
    """
    factors: list[str] = []
    if poly.coeffs == (0,):
        return ("0",)
    if poly.evaluate(1) == 0:
        factors.append("x-1")
    if poly.evaluate(-1) == 0:
        factors.append("x+1")
    for n, name in (
        (3, "Phi_3=x^2+x+1"),
        (4, "Phi_4=x^2+1"),
        (6, "Phi_6=x^2-x+1"),
        (5, "Phi_5"),
        (8, "Phi_8=x^4+1"),
        (10, "Phi_10"),
        (12, "Phi_12=x^4-x^2+1"),
    ):
        phi = _cyclotomic(n)
        raw = _divmod_poly(poly.coeffs, phi)
        if raw is not None and raw[1] == (0,):
            factors.append(name)
    return tuple(factors)


def evaluation_identities(n: int) -> dict[str, int | bool]:
    n = _require_int(n)
    p = polynomial(n)
    return {
        "P(3)": p.evaluate(3),
        "n": n,
        "P(1)": p.evaluate(1),
        "signed_digit_sum": signed_digit_sum(encode(n)),
        "P(-1)": p.evaluate(-1),
        "alternating_digit_sum": bt_alternating_digit_sum(n),
        "weight": weight(encode(n)),
        "coefficient_weight": p.coefficient_weight(),
        "bt_palindrome": bt_is_palindrome(n),
        "poly_palindrome": p.is_palindromic(),
        "degree": p.degree,
    }

