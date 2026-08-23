"""Finite-state classification of coefficient normalization by alphabet.

Already-trit words: identity / strip high zeros.
Fixed ``[-B, B]``: LSD sequential, carry in a finite set.
Unbounded ``ℤ``: not one finite-state transduction.

Do not lift a finite-``B`` machine to unbounded coefficients.
"""

from __future__ import annotations

from dataclasses import dataclass

from bt.normtheory.coeffword import CoeffWord
from bt.normtheory.rewrite import balanced_divmod
from bt.representation import BalancedTernary, from_digits_lsd


def carry_bound(B: int) -> int:
    """Safe carry alphabet bound ``C = B`` for inputs in ``[-B, B]``.

    If the incoming carry is in ``[-B, B]`` then
    ``|q| <= floor((2B + 1) / 3) <= B`` for ``B >= 1``.
    Algebraic bound used in Lean: ``|q| <= (B + 1) // 3`` on a single
    coefficient with no incoming carry.
    """
    if B < 0:
        raise ValueError("B must be >= 0")
    return B


def single_coeff_carry_bound(B: int) -> int:
    """``|q| <= floor((B + 1) / 3)`` when rewriting one coefficient in ``[-B, B]``."""
    if B < 0:
        raise ValueError("B must be >= 0")
    return (B + 1) // 3


@dataclass(frozen=True)
class LocalityClass:
    alphabet: str
    finite_state: bool
    transducer_type: str
    carry_set: str
    notes: str

    def as_dict(self) -> dict[str, object]:
        return {
            "alphabet": self.alphabet,
            "finite_state": self.finite_state,
            "transducer_type": self.transducer_type,
            "carry_set": self.carry_set,
            "notes": self.notes,
        }


def classify_alphabet(bound: int | None) -> LocalityClass:
    if bound is None:
        return LocalityClass(
            alphabet="Z",
            finite_state=False,
            transducer_type="not one finite-state transduction",
            carry_set="unbounded",
            notes="A coefficient 3^k produces carry scale 3^{k-1}. Unbounded input alphabet.",
        )
    if bound <= 1:
        return LocalityClass(
            alphabet="{-1,0,+1}",
            finite_state=True,
            transducer_type="identity / strip high zeros",
            carry_set="{0}",
            notes="Already canonical up to trailing high zeros.",
        )
    C = carry_bound(bound)
    return LocalityClass(
        alphabet=f"[-{bound},{bound}]",
        finite_state=True,
        transducer_type="LSD sequential Mealy",
        carry_set=f"[-{C},{C}]",
        notes=f"Incoming carry stays in [-{C},{C}]. |q| on one coeff <= {single_coeff_carry_bound(bound)}.",
    )


class BoundedNormalizeTransducer:
    """LSD Mealy machine for coefficient words over a fixed ``[-B, B]``."""

    def __init__(self, bound: int) -> None:
        if bound < 1:
            raise ValueError("bound must be >= 1")
        self.bound = bound
        self.carry_limit = carry_bound(bound)

    def step(self, carry: int, digit: int) -> tuple[int, int]:
        if abs(digit) > self.bound:
            raise ValueError(f"digit {digit} outside [-{self.bound},{self.bound}]")
        if abs(carry) > self.carry_limit:
            raise ValueError(f"carry {carry} outside [-{self.carry_limit},{self.carry_limit}]")
        r, q = balanced_divmod(digit + carry)
        if abs(q) > self.carry_limit:
            raise RuntimeError(f"carry escaped bound: q={q}")
        return q, r

    def apply(self, word: CoeffWord) -> BalancedTernary:
        carry = 0
        out: list[int] = []
        for c in word.coeffs:
            carry, d = self.step(carry, c)
            out.append(d)
        while carry:
            r, carry = balanced_divmod(carry)
            out.append(r)
        return from_digits_lsd(out)


def all_classes() -> list[LocalityClass]:
    return [
        classify_alphabet(1),
        classify_alphabet(3),
        classify_alphabet(5),
        classify_alphabet(None),
    ]
