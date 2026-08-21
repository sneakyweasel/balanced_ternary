"""Zero-lift coefficient ``J`` and infinite-itinerary compatibility.

Along a valuation word ``k_0, k_1, ...`` let ``R_m = R(k_0,...,k_{m-1})``
and ``K_m = k_0+...+k_{m-1}``. The **lift coefficient** is the integer

    J_m = (R_{m+1} - R_m) / 2^{K_m + 1}.

It is a nonnegative integer (**PROVED**, nested cylinders). ``J_m = 0``
iff ``R`` does not lift at that step.

**Dichotomy (PROVED).** For an infinite valuation itinerary the following
are equivalent:

1. some positive odd integer realises every finite prefix;
2. ``R_m`` is eventually constant;
3. ``J_m = 0`` for all sufficiently large ``m``.

The zero-lift continuation of a prefix is unique: it is the next
accelerated valuation of ``T^m(R)``. That path is the Collatz orbit of
``R``, so a complete characterisation of zero-lift paths repackages
Collatz. This module records the exact algebra of ``J``, not a Collatz
proof.

A Lean 4 target for the abstract sequence dichotomy lives in
``lean/ZeroLiftDichotomy.lean``.
"""

from __future__ import annotations

from dataclasses import dataclass

from collatz.compatibility import child_realizer_delta
from collatz.core import collatz_step, collatz_valuation
from collatz.cylinders import parse_ks
from collatz.itinerary import ValuationItinerary
from collatz.min_realizer import min_realizer, nested_realizers
from collatz.valuation import v2


def lift_J(parent: tuple[int, ...], j: int) -> int:
    """``J`` for the extension ``parent`` then ``j``. Exact nonnegative int."""
    return child_realizer_delta(parent, j)[2]


def J_along(ks: tuple[int, ...]) -> tuple[int, ...]:
    """``(J_0, ..., J_{m-1})`` along ``ks``, starting from the empty prefix."""
    ks = parse_ks(ks)
    return tuple(lift_J(ks[:i], ks[i]) for i in range(len(ks)))


def zero_lift_k(ks: tuple[int, ...] | str | list[int]) -> int:
    """The unique ``j >= 1`` with ``J(ks, j) = 0``.

    **PROVED:** ``R = R(ks)`` realises ``ks``, so ``x = T^m(R)`` is a
    positive odd integer and ``j = v2(3x+1)`` is the unique next
    valuation of that orbit. Then ``R`` realises ``ks+(j,)``, hence
    ``R_child <= R``. Nested monotonicity gives ``R_child = R``, so
    ``J = 0``. Any other ``j'`` is not the next valuation of ``R``, so
    ``R`` is not in the child cylinder and ``J >= 1``.
    """
    ks = parse_ks(ks)
    r = min_realizer(ks)
    x = ValuationItinerary.from_ks(ks).apply(r)
    return collatz_valuation(x)


def is_zero_lift_extension(ks: tuple[int, ...], j: int) -> bool:
    return j == zero_lift_k(ks)


@dataclass(frozen=True)
class ZeroLiftState:
    """Canonical state of the zero-lift successor map.

    ``R`` is constant along this map. ``x = T^m(R)``. The next symbol is
    ``v2(3x+1)``. This *is* the accelerated Collatz orbit of ``R``.
    """

    prefix: tuple[int, ...]
    R: int
    x: int
    m: int
    K: int

    @classmethod
    def from_prefix(cls, ks: tuple[int, ...] | str | list[int]) -> "ZeroLiftState":
        ks = parse_ks(ks)
        r = min_realizer(ks)
        x = ValuationItinerary.from_ks(ks).apply(r)
        return cls(prefix=ks, R=r, x=x, m=len(ks), K=sum(ks))

    @classmethod
    def empty(cls) -> "ZeroLiftState":
        return cls.from_prefix(())

    def successor_k(self) -> int:
        return collatz_valuation(self.x)

    def step(self) -> "ZeroLiftState":
        k = self.successor_k()
        return ZeroLiftState(
            prefix=self.prefix + (k,),
            R=self.R,
            x=collatz_step(self.x),
            m=self.m + 1,
            K=self.K + k,
        )

    def trace(self, steps: int) -> tuple["ZeroLiftState", ...]:
        if isinstance(steps, bool) or not isinstance(steps, int) or steps < 0:
            raise ValueError(f"steps must be an integer >= 0, got {steps!r}")
        out = [self]
        cur = self
        for _ in range(steps):
            cur = cur.step()
            out.append(cur)
        return tuple(out)

    def as_dict(self) -> dict[str, object]:
        return {
            "prefix": list(self.prefix),
            "R": self.R,
            "x": self.x,
            "m": self.m,
            "K": self.K,
            "next_k": self.successor_k(),
            "status": "EXACT",
        }


def zero_lift_trace(
    ks: tuple[int, ...] | str | list[int] = (),
    steps: int = 8,
) -> tuple[ZeroLiftState, ...]:
    return ZeroLiftState.from_prefix(ks).trace(steps)


@dataclass(frozen=True)
class DichotomyReport:
    ks: tuple[int, ...]
    R: tuple[int, ...]
    J: tuple[int, ...]
    trailing_zero_lifts: int
    all_J_zero: bool
    status: str

    def format(self) -> str:
        return (
            f"Zero-lift dichotomy on finite prefix  ks={self.ks}\n"
            f"R_m={self.R}\n"
            f"J_m={self.J}\n"
            f"all J=0: {str(self.all_J_zero).lower()}  "
            f"observed trailing zero-lifts={self.trailing_zero_lifts}\n"
            f"status: {self.status}\n"
            "Infinite itinerary has a positive integer realizer iff "
            "R_m eventually constant iff J_m=0 eventually. [PROVED]\n"
        )


def dichotomy_report(ks: tuple[int, ...] | str | list[int]) -> DichotomyReport:
    ks = parse_ks(ks)
    rs = nested_realizers(ks)
    js = J_along(ks)
    all_zero = all(j == 0 for j in js)
    trailing = 0
    for j in reversed(js):
        if j != 0:
            break
        trailing += 1
    return DichotomyReport(
        ks=ks,
        R=rs,
        J=js,
        trailing_zero_lifts=trailing,
        all_J_zero=all_zero,
        status=(
            "EXACT J and R on this finite prefix. "
            "The infinite dichotomy is PROVED; this sample does not prove Collatz."
        ),
    )


def all_zero_J_words_are_twos(ks: tuple[int, ...]) -> bool:
    """``J ≡ 0`` along a word starting from empty iff the word is ``(2,...,2)``.

    **PROVED:** unique zero-lift from ``()`` is ``k=2`` because ``R=1`` and
    ``T(1)=1`` with valuation 2. Inductively the unique zero-lift tail is
    the 1-cycle.
    """
    ks = parse_ks(ks)
    return all(j == 0 for j in J_along(ks)) == all(k == 2 for k in ks)


@dataclass(frozen=True)
class FiniteJCertificate:
    """A finite-state decision about one proposed extension.

    The state is ``x = T^m(R(parent)) mod 2^precision``. If
    ``v2(3x+1) < precision``, the next zero-lift valuation is known
    exactly. If the residue is zero, only ``v2(3x+1) >= precision`` is
    known; proposed ``j < precision`` can still be rejected exactly.
    """

    parent: tuple[int, ...]
    j: int
    precision: int
    state_residue: int
    valuation: int | None
    valuation_at_least: int | None
    result: str


def finite_J_certificate(
    parent: tuple[int, ...] | str | list[int],
    j: int,
    precision: int,
) -> FiniteJCertificate:
    """Certify ``J=0`` or ``J>0`` from finite canonical-state information.

    Results are ``CERTIFIED_ZERO``, ``CERTIFIED_POSITIVE``, or
    ``UNRESOLVED``. Every certificate is **PROVED** by arithmetic modulo
    ``2^precision``; ``UNRESOLVED`` makes no claim.
    """
    parent = parse_ks(parent)
    if isinstance(j, bool) or not isinstance(j, int) or j < 1:
        raise ValueError(f"j must be an integer >= 1, got {j!r}")
    if (
        isinstance(precision, bool)
        or not isinstance(precision, int)
        or precision < 1
    ):
        raise ValueError(
            f"precision must be an integer >= 1, got {precision!r}"
        )
    state = ZeroLiftState.from_prefix(parent)
    modulus = 1 << precision
    residue = state.x % modulus
    y_residue = (3 * residue + 1) % modulus
    if y_residue == 0:
        result = "CERTIFIED_POSITIVE" if j < precision else "UNRESOLVED"
        return FiniteJCertificate(
            parent=parent,
            j=j,
            precision=precision,
            state_residue=residue,
            valuation=None,
            valuation_at_least=precision,
            result=result,
        )
    valuation = v2(y_residue)
    if valuation is None or valuation >= precision:
        raise ArithmeticError("nonzero residue must have valuation below precision")
    return FiniteJCertificate(
        parent=parent,
        j=j,
        precision=precision,
        state_residue=residue,
        valuation=valuation,
        valuation_at_least=None,
        result="CERTIFIED_ZERO" if j == valuation else "CERTIFIED_POSITIVE",
    )


def expanding_word_has_positive_J(ks: tuple[int, ...]) -> bool:
    """Every expanding finite word (from empty) has some ``J_i > 0``. **PROVED.**

    The only all-zero-``J`` words are ``(2)^m``, which are contracting.
    """
    from collatz.automata.valuation_shift import growth_budget

    ks = parse_ks(ks)
    if not ks:
        return False
    if growth_budget(ks).kind != "expanding":
        return False
    return any(j > 0 for j in J_along(ks))
