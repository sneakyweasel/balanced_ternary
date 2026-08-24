"""OEIS-style sequence dossiers for balanced-ternary operators.

A discovered prefix is not automatically new. Each dossier records the
definition, first terms, closest known sequence, and claim status.
"""

from __future__ import annotations

from dataclasses import dataclass

from bt.metrics import weight
from bt.operators import d_steps_to_zero, digit_derivative, lsd_digit, three_kernel
from bt.representation import encode
from bt.sequences import bt_length, bt_reverse


@dataclass(frozen=True)
class SequenceDossier:
    name: str
    definition: str
    offset: int
    terms: tuple[int, ...]
    closest_oeis: str
    claim_status: str
    notes: str

    def as_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "definition": self.definition,
            "offset": self.offset,
            "terms": list(self.terms),
            "closest_oeis": self.closest_oeis,
            "claim_status": self.claim_status,
            "notes": self.notes,
        }


def _prefix(fn, start: int, count: int) -> tuple[int, ...]:
    return tuple(fn(n) for n in range(start, start + count))


def dossier_d_stopping() -> SequenceDossier:
    terms = _prefix(d_steps_to_zero, 0, 40)
    length_terms = _prefix(bt_length, 0, 40)
    same = terms[1:] == length_terms[1:] and terms[0] == 0
    return SequenceDossier(
        name="D-stopping-time",
        definition="smallest j with D^j(n)=0; D^0(0)=0 gives 0",
        offset=0,
        terms=terms,
        closest_oeis="A134021 (canonical BT length L_3), except a(0)=1 there vs 0 here",
        claim_status="EXACT — HUMAN PROOF" if same else "OBSERVATION",
        notes=(
            "For n≠0 the D-orbit length equals L_3(n). A134021(0)=1 because "
            "the zero word has length 1. This is not a new sequence."
        ),
    )


def dossier_lsd() -> SequenceDossier:
    return SequenceDossier(
        name="balanced_lsd",
        definition="a_0(n) in {-1,0,+1}, the least-significant balanced digit",
        offset=0,
        terms=_prefix(lsd_digit, 0, 40),
        closest_oeis="n mod 3 lifted to {-1,0,+1}: 0,1,-1,0,1,-1,... (period 3)",
        claim_status="EXACT — HUMAN PROOF",
        notes="Equals n-3*round(n/3) in balanced remainder. Not submitted as new.",
    )


def dossier_w_ww() -> SequenceDossier:
    def ww(n: int) -> int:
        return bt_reverse(bt_reverse(n))

    terms = _prefix(ww, 0, 40)
    k3 = _prefix(three_kernel, 0, 40)
    return SequenceDossier(
        name="W_composed_with_W",
        definition="W(W(n))",
        offset=0,
        terms=terms,
        closest_oeis="n / 3^{v_3(n)} (3-free kernel), A007949 is v_3 itself",
        claim_status="EXACT — HUMAN PROOF" if terms == k3 else "OBSERVATION",
        notes="W∘W = K3. Restates the involution criterion for W.",
    )


def dossier_weight_of_double() -> SequenceDossier:
    terms = tuple(weight(encode(2 * n)) for n in range(0, 40))
    return SequenceDossier(
        name="weight_of_2n",
        definition="w(2n), Hamming weight after doubling",
        offset=0,
        terms=terms,
        closest_oeis="not identified; related to carry_defect(n,n)=2w(n)-w(2n)",
        claim_status="OBSERVATION",
        notes="Finite prefix only. Not a theorem and not claimed new in OEIS.",
    )


def dossier_d_parity() -> SequenceDossier:
    terms = tuple(digit_derivative(n) % 2 for n in range(0, 40))
    return SequenceDossier(
        name="parity_of_D",
        definition="D(n) mod 2",
        offset=0,
        terms=terms,
        closest_oeis="equals n-a_0(n) mod 2, hence determined by n and a_0",
        claim_status="EXACT — HUMAN PROOF",
        notes="Immediate from n = a0 + 3 D(n) and 3 odd.",
    )


def all_dossiers() -> tuple[SequenceDossier, ...]:
    return (
        dossier_d_stopping(),
        dossier_lsd(),
        dossier_w_ww(),
        dossier_weight_of_double(),
        dossier_d_parity(),
    )
