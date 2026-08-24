"""Minimum positive realizers of valuation cylinders.

Convention (Milestone 3, leftover ``Q = 1``): ``C_ks`` is the unique
residue class modulo ``2^{K+1}``. The smallest positive representative
``R(ks)`` is that residue, which lies in ``{1, 3, ..., 2^{K+1}-1}``.

**PROVED:** every ``n ≡ R(ks) (mod 2^{K+1})`` realises the prefix.
Along a nested prefix, ``R(child) ≡ R(parent) (mod 2^{K_parent+1})`` and
``0 < R(child) < 2^{K_child+1}``, hence

    R(child) = R(parent) + t * 2^{K_parent+1}   for some t >= 0,

so ``R`` is nondecreasing on nested prefixes. A child cannot have smaller
``R`` than its parent.

``count_cylinder_up_to(ks, X)`` counts positive realizers in ``[1, X]``.
"""

from __future__ import annotations

from dataclasses import dataclass

from bt.representation import encode
from research.collatz.cylinders import parse_ks, valuation_cylinder
from research.collatz.features import BalancedTernaryFeatures, extract_features
from research.collatz.itinerary import ValuationItinerary, positivity_threshold


def min_realizer(ks: tuple[int, ...] | str | list[int]) -> int:
    """Smallest positive odd integer realising ``ks``. Always finite."""
    ks = parse_ks(ks)
    cyl = valuation_cylinder(ks)
    if not cyl.residues:
        raise ArithmeticError(f"empty cylinder for ks={ks}, contradicting Milestone 3")
    return cyl.residues[0]


def count_cylinder_up_to(ks: tuple[int, ...] | str | list[int], x: int) -> int:
    """Number of positive realizers ``n`` with ``1 <= n <= X``."""
    if isinstance(x, bool) or not isinstance(x, int) or x < 1:
        raise ValueError(f"X must be an integer >= 1, got {x!r}")
    ks = parse_ks(ks)
    r = min_realizer(ks)
    modulus = 1 << (sum(ks) + 1)
    if x < r:
        return 0
    return (x - r) // modulus + 1


def expected_count_floor(ks: tuple[int, ...], x: int) -> int:
    """Asymptotic ``floor((X - r)/2^{K+1}) + 1`` is already exact for this cylinder."""
    return count_cylinder_up_to(ks, x)


@dataclass(frozen=True)
class ItinerarySignature:
    """Canonical exact signature of a finite valuation word."""

    ks: tuple[int, ...]
    m: int
    K: int
    C: int
    residue: int
    modulus: int
    R: int
    budget_kind: str
    two_power: int
    three_power: int
    positivity_threshold: int
    bt_word: str
    features: BalancedTernaryFeatures

    def as_dict(self) -> dict[str, object]:
        return {
            "ks": list(self.ks),
            "m": self.m,
            "K": self.K,
            "C": self.C,
            "residue": self.residue,
            "modulus": self.modulus,
            "R": self.R,
            "budget_kind": self.budget_kind,
            "two_power": self.two_power,
            "three_power": self.three_power,
            "positivity_threshold": self.positivity_threshold,
            "BT(R)": self.bt_word,
            "features": self.features.as_dict(),
            "status": "EXACT",
        }

    def format(self) -> str:
        bgt = self.budget_kind
        return (
            f"Itinerary signature  ks={self.ks}  [EXACT]\n"
            f"m={self.m}  K={self.K}  C={self.C}  R={self.R}  "
            f"r={self.residue} mod {self.modulus}\n"
            f"budget 2^K={self.two_power} vs 3^m={self.three_power}  {bgt}\n"
            f"positivity_threshold={self.positivity_threshold}\n"
            f"BT(R)={self.bt_word}\n"
            f"features length={self.features.length} weight={self.features.weight} "
            f"signed={self.features.signed_digit_sum} runs={self.features.number_of_runs}\n"
        )


def itinerary_signature(ks: tuple[int, ...] | str | list[int]) -> ItinerarySignature:
    ks = parse_ks(ks)
    it = ValuationItinerary.from_ks(ks)
    r = min_realizer(ks)
    bgt = it.budget()
    word = encode(r)
    return ItinerarySignature(
        ks=ks,
        m=it.m,
        K=it.K,
        C=it.C,
        residue=r,
        modulus=1 << (it.K + 1),
        R=r,
        budget_kind=bgt.kind,
        two_power=bgt.two_power,
        three_power=bgt.three_power,
        positivity_threshold=positivity_threshold(ks),
        bt_word=word.word(),
        features=extract_features(word),
    )


def nested_realizers(ks: tuple[int, ...]) -> tuple[int, ...]:
    """``(R(ks[:1]), ..., R(ks[:m]))``. Empty prefix has ``R=1``."""
    ks = parse_ks(ks)
    out = [min_realizer(())]
    for i in range(1, len(ks) + 1):
        out.append(min_realizer(ks[:i]))
    return tuple(out)
