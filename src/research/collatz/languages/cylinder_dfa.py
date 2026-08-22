"""Balanced-ternary DFA and entropy of a valuation cylinder.

Words are **all** length-``L`` strings over ``{-,0,+}`` (leading zeros
allowed). That is the regular language of the residue DFA
``ModularAutomaton(2^P)`` with accept states equal to the cylinder
residues. Canonical (no leading ``0``) counts are a separate column.

``H_L(ks) = (1/L) log_3 (# accepted length-L words)``. Finite-``L`` values
are **VERIFIED COMPUTATIONALLY**. A spectral growth rate is not claimed.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from automata.modular import ALPHABET, ModularAutomaton
from balanced_ternary.representation import WordLike, decode, msd_digits
from research.collatz.cylinders import ValuationCylinder, parse_ks, valuation_cylinder
from research.collatz.languages.dfa_minimize import MinimizedDFA, minimize_dfa
from research.collatz.valuation import v2


DIGIT_CHARS = ("-", "0", "+")


class ResidueLanguageDFA:
    """MSD acceptor for ``decode(w) ≡ r (mod q)`` for ``r`` in ``accepts``."""

    def __init__(self, modulus: int, accept_residues: tuple[int, ...]):
        if isinstance(modulus, bool) or not isinstance(modulus, int) or modulus < 2:
            raise ValueError(f"modulus must be an integer >= 2, got {modulus!r}")
        self.modulus = modulus
        self._auto = ModularAutomaton(modulus)
        acc = tuple(sorted({r % modulus for r in accept_residues}))
        self.accept_residues = acc
        self._accept_set = frozenset(acc)

    def residue(self, word: WordLike) -> int:
        return self._auto.residue(word)

    def accepts(self, word: WordLike) -> bool:
        return self.residue(word) in self._accept_set

    def minimized(self) -> MinimizedDFA:
        return minimize_dfa(
            start=0,
            alphabet=ALPHABET,
            delta=self._auto.transition,
            accepts=self._accept_set,
        )

    def count_words(self, length: int) -> int:
        """Number of length-``L`` strings (leading zeros allowed)."""
        if isinstance(length, bool) or not isinstance(length, int) or length < 0:
            raise ValueError(f"length must be an integer >= 0, got {length!r}")
        if length == 0:
            return 1 if 0 in self._accept_set else 0
        cur = [0] * self.modulus
        cur[0] = 1
        for _ in range(length):
            nxt = [0] * self.modulus
            for s, c in enumerate(cur):
                if c == 0:
                    continue
                for a in ALPHABET:
                    nxt[(3 * s + a) % self.modulus] += c
            cur = nxt
        return sum(cur[r] for r in self.accept_residues)

    def count_canonical_words(self, length: int) -> int:
        """Length-``L`` words whose first digit is not ``0`` (or ``0`` if L=1)."""
        if isinstance(length, bool) or not isinstance(length, int) or length < 1:
            raise ValueError(f"length must be an integer >= 1, got {length!r}")
        if length == 1:
            count = 0
            for a in ALPHABET:
                if a % self.modulus in self._accept_set:
                    count += 1
            return count
        # First digit in {-, +}, then L-1 free digits.
        cur = [0] * self.modulus
        for a in (-1, 1):
            cur[a % self.modulus] += 1
        for _ in range(length - 1):
            nxt = [0] * self.modulus
            for s, c in enumerate(cur):
                if c == 0:
                    continue
                for a in ALPHABET:
                    nxt[(3 * s + a) % self.modulus] += c
            cur = nxt
        return sum(cur[r] for r in self.accept_residues)


class CylinderDFA(ResidueLanguageDFA):
    """Residue DFA of a valuation cylinder."""

    def __init__(
        self,
        ks: tuple[int, ...] | str | list[int] = (),
        leftover_q: int = 1,
    ):
        self.cylinder = valuation_cylinder(ks, leftover_q=leftover_q)
        super().__init__(1 << self.cylinder.precision, self.cylinder.residues)
        self.ks = self.cylinder.ks


def valuation_class_minimized_size(k: int) -> int:
    """``A_k``: minimized DFA size of ``L_k = {w : v2(decode(w)) = k}``."""
    from research.collatz.transducers.valuation_languages import ValuationClassDFA

    return ValuationClassDFA(k).minimized_state_count()


@dataclass(frozen=True)
class EntropyReport:
    ks: tuple[int, ...]
    length: int
    word_count: int
    canonical_count: int
    minimized_states: int
    h_base3: float | None
    h_bits: float | None
    empty_h_base3: float | None
    status: str

    def as_dict(self) -> dict[str, object]:
        return {
            "ks": list(self.ks),
            "length": self.length,
            "word_count": self.word_count,
            "canonical_count": self.canonical_count,
            "minimized_states": self.minimized_states,
            "H_L_base3": self.h_base3,
            "H_L_bits": self.h_bits,
            "H_L_empty_base3": self.empty_h_base3,
            "status": self.status,
        }

    def format(self) -> str:
        h = "undefined" if self.h_base3 is None else f"{self.h_base3:.6f}"
        he = "undefined" if self.empty_h_base3 is None else f"{self.empty_h_base3:.6f}"
        return (
            f"Entropy L={self.length}  ks={self.ks}\n"
            f"padded word count: {self.word_count}  "
            f"canonical (no leading 0): {self.canonical_count}\n"
            f"minimized DFA states: {self.minimized_states}\n"
            f"H_L (base 3): {h}  bits/symbol: "
            f"{'undefined' if self.h_bits is None else f'{self.h_bits:.6f}'}\n"
            f"H_L(empty cylinder, odds, base 3): {he}\n"
            f"status: {self.status}\n"
        )


def _entropy_from_count(count: int, length: int) -> tuple[float | None, float | None]:
    if length <= 0 or count <= 0:
        return None, None
    h3 = math.log(count, 3) / length
    h2 = math.log2(count) / length
    return h3, h2


def entropy_report(
    ks: tuple[int, ...] | str | list[int],
    length: int,
    leftover_q: int = 1,
) -> EntropyReport:
    if isinstance(length, bool) or not isinstance(length, int) or length < 1:
        raise ValueError(f"length must be an integer >= 1, got {length!r}")
    ks = parse_ks(ks)
    dfa = CylinderDFA(ks, leftover_q=leftover_q)
    count = dfa.count_words(length)
    canon = dfa.count_canonical_words(length)
    minimized = dfa.minimized().state_count
    h3, h2 = _entropy_from_count(count, length)
    empty = CylinderDFA((), leftover_q=leftover_q)
    ecount = empty.count_words(length)
    eh3, _ = _entropy_from_count(ecount, length)
    return EntropyReport(
        ks=ks,
        length=length,
        word_count=count,
        canonical_count=canon,
        minimized_states=minimized,
        h_base3=h3,
        h_bits=h2,
        empty_h_base3=eh3,
        status="VERIFIED COMPUTATIONALLY",
    )


def decode_in_cylinder(word: WordLike, cylinder: ValuationCylinder) -> bool:
    """``decode(w)`` lies in the residue class of the cylinder (any sign)."""
    n = decode(word)
    return cylinder.contains_residue(n)


def padded_word_from_digits(digits: tuple[int, ...]) -> str:
    table = {-1: "-", 0: "0", 1: "+"}
    if not digits:
        return "0"
    return "".join(table[d] for d in digits)


def v2_of_decoded(word: WordLike) -> int | None:
    return v2(decode(word))


def msd_first_digit(word: WordLike) -> int:
    return msd_digits(word)[0]
