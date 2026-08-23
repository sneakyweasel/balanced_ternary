"""Ordinary ``Z[x]`` section derivative ``𝔇_a``.

This is **not** ``BTPolynomial`` (trit coefficients, ``P(3)=n``) and not
``CoeffWord`` (digit expansion of an integer). Those remain separate.

Definition, for any ``a ∈ ℤ`` (digit sections use ``a ∈ {-1,0,+1}``):

    ρ_a(f) = [f(a)]_3
    𝔇_a f(x) = (f(a + 3x) - ρ_a(f)) / 3   in Z[x]

Degree is **not** lowered: for ``deg f = d ≥ 1``,
``LC(𝔇_a f) = 3^{d-1} LC(f)`` and ``deg(𝔇_a f) = d``.
"""

from __future__ import annotations

from dataclasses import dataclass

from bt.normtheory.rewrite import balanced_divmod


def _require_int(n: int, name: str = "n") -> int:
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"{name} must be int, got {type(n).__name__}")
    return n


def _strip(coeffs: tuple[int, ...]) -> tuple[int, ...]:
    i = len(coeffs)
    while i > 1 and coeffs[i - 1] == 0:
        i -= 1
    return coeffs[:i] if i else (0,)


def rho_int(n: int) -> int:
    """Canonical balanced residue ``[n]_3 ∈ {-1,0,+1}``."""
    r, _q = balanced_divmod(_require_int(n))
    return r


@dataclass(frozen=True)
class IntPoly:
    """Ordinary integer polynomial, LSD-first ``Σ c_i x^i`` with ``c_i ∈ ℤ``."""

    coeffs: tuple[int, ...]

    def __post_init__(self) -> None:
        raw = tuple(_require_int(c, "coefficient") for c in self.coeffs)
        object.__setattr__(self, "coeffs", _strip(raw))

    @classmethod
    def C(cls, n: int) -> "IntPoly":
        return cls((_require_int(n),))

    @classmethod
    def X(cls) -> "IntPoly":
        return cls((0, 1))

    @classmethod
    def from_dict(cls, terms: dict[int, int]) -> "IntPoly":
        if not terms:
            return cls((0,))
        deg = max(terms)
        cs = [0] * (deg + 1)
        for i, c in terms.items():
            if i < 0:
                raise ValueError("negative degree")
            cs[i] += c
        return cls(tuple(cs))

    @property
    def degree(self) -> int:
        if self.coeffs == (0,):
            return -1
        return len(self.coeffs) - 1

    def lc(self) -> int:
        return self.coeffs[-1]

    def coefficient(self, i: int) -> int:
        if i < 0:
            raise ValueError("i must be >= 0")
        if i >= len(self.coeffs):
            return 0
        return self.coeffs[i]

    def eval(self, x: int) -> int:
        acc = 0
        pow_x = 1
        for c in self.coeffs:
            acc += c * pow_x
            pow_x *= x
        return acc

    def add(self, other: "IntPoly") -> "IntPoly":
        n = max(len(self.coeffs), len(other.coeffs))
        return IntPoly(tuple(self.coefficient(i) + other.coefficient(i) for i in range(n)))

    def neg(self) -> "IntPoly":
        return IntPoly(tuple(-c for c in self.coeffs))

    def sub(self, other: "IntPoly") -> "IntPoly":
        return self.add(other.neg())

    def scale(self, k: int) -> "IntPoly":
        return IntPoly(tuple(k * c for c in self.coeffs))

    def mul(self, other: "IntPoly") -> "IntPoly":
        if self.coeffs == (0,) or other.coeffs == (0,):
            return IntPoly((0,))
        out = [0] * (self.degree + other.degree + 1)
        for i, a in enumerate(self.coeffs):
            if a == 0:
                continue
            for j, b in enumerate(other.coeffs):
                out[i + j] += a * b
        return IntPoly(tuple(out))

    def pow(self, n: int) -> "IntPoly":
        n = _require_int(n)
        if n < 0:
            raise ValueError("n must be >= 0")
        acc = IntPoly((1,))
        base = self
        while n:
            if n & 1:
                acc = acc.mul(base)
            base = base.mul(base)
            n >>= 1
        return acc

    def compose(self, inner: "IntPoly") -> "IntPoly":
        acc = IntPoly((0,))
        pow_g = IntPoly((1,))
        for c in self.coeffs:
            if c:
                acc = acc.add(pow_g.scale(c))
            pow_g = pow_g.mul(inner)
        return acc

    def rho(self, a: int) -> int:
        return rho_int(self.eval(_require_int(a, "a")))

    def section_deriv(self, a: int) -> "IntPoly":
        """``𝔇_a f ∈ Z[x]`` by binomial shift, no pointwise division."""
        a = _require_int(a, "a")
        shift = IntPoly((a, 3))  # a + 3x
        composed = self.compose(shift)
        r = self.rho(a)
        diff = composed.sub(IntPoly((r,)))
        if any(c % 3 != 0 for c in diff.coeffs):
            raise RuntimeError(f"section derivative not in Z[x]: {diff.coeffs}")
        return IntPoly(tuple(c // 3 for c in diff.coeffs))

    def render(self) -> str:
        if self.coeffs == (0,):
            return "0"
        parts: list[str] = []
        for i, c in enumerate(self.coeffs):
            if c == 0:
                continue
            if i == 0:
                parts.append(str(c))
                continue
            sign = "+" if c > 0 else "-"
            mag = abs(c)
            if i == 1:
                mon = "x" if mag == 1 else f"{mag}x"
            else:
                mon = f"x^{i}" if mag == 1 else f"{mag}x^{i}"
            if not parts:
                parts.append(mon if c > 0 else f"-{mon}")
            else:
                parts.append(f"{sign} {mon}")
        return " ".join(parts)


def parse_poly(text: str) -> IntPoly:
    """Parse ``x^2+x``, ``2x-1``, ``x^3``, ``-3``, ``x``."""
    s = text.replace(" ", "").replace("**", "^")
    if not s:
        raise ValueError("empty polynomial")
    s = s.replace("-", "+-")
    if s.startswith("+"):
        s = s[1:]
    terms = s.split("+")
    acc: dict[int, int] = {}
    for term in terms:
        if term == "":
            continue
        coeff, deg = _parse_term(term)
        acc[deg] = acc.get(deg, 0) + coeff
    return IntPoly.from_dict(acc) if acc else IntPoly((0,))


def _parse_term(term: str) -> tuple[int, int]:
    if "x" not in term:
        return int(term), 0
    left, _, right = term.partition("x")
    if left in ("", "+"):
        coeff = 1
    elif left == "-":
        coeff = -1
    else:
        coeff = int(left)
    if right == "":
        deg = 1
    elif right.startswith("^"):
        deg = int(right[1:])
    else:
        raise ValueError(f"bad term {term!r}")
    return coeff, deg


def section_reconstruction(f: IntPoly, a: int, x: int) -> bool:
    """``f(a+3x) = ρ_a(f) + 3 𝔇_a f(x)`` as integers."""
    return f.eval(a + 3 * x) == f.rho(a) + 3 * f.section_deriv(a).eval(x)


def twisted_leibniz(f: IntPoly, g: IntPoly, a: int) -> bool:
    left = f.mul(g).section_deriv(a)
    rf, rg = f.rho(a), g.rho(a)
    df, dg = f.section_deriv(a), g.section_deriv(a)
    right = dg.scale(rf).add(df.scale(rg)).add(df.mul(dg).scale(3))
    return left.coeffs == right.coeffs


def composition_law(f: IntPoly, g: IntPoly, a: int) -> bool:
    left = f.compose(g).section_deriv(a)
    right = f.section_deriv(g.rho(a)).compose(g.section_deriv(a))
    return left.coeffs == right.coeffs


def classical_leibniz(f: IntPoly, g: IntPoly, a: int) -> bool:
    left = f.mul(g).section_deriv(a)
    right = f.section_deriv(a).mul(g).add(f.mul(g.section_deriv(a)))
    return left.coeffs == right.coeffs


def classical_chain(f: IntPoly, g: IntPoly, a: int) -> bool:
    """Ordinary chain rule ``(𝔇 f)(g) · 𝔇_a g`` — not the section law."""
    left = f.compose(g).section_deriv(a)
    # There is no unique ``𝔇 f`` independent of section; use 𝔇_0 as a straw man.
    right = f.section_deriv(0).compose(g).mul(g.section_deriv(a))
    return left.coeffs == right.coeffs


def degree_drops(f: IntPoly, a: int) -> bool:
    d = f.degree
    if d <= 0:
        return True
    return f.section_deriv(a).degree == d - 1
