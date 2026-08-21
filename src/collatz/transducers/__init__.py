"""LSD-first sequential transducers for doubling and 2-adic odd-part.

Reading direction is least-significant digit first. This is dual to the
MSD Horner automaton in ``automata.modular``.

Claim status is recorded in ``docs/collatz_mathematics.md``.
"""

from collatz.transducers.divide_by_two import (
    DivideByTwoTransducer,
    LeftoverCarryError,
    apply_even,
)
from collatz.transducers.divide_by_two_power import (
    DivideByTwoPowerTransducer,
    apply_divisible,
)
from collatz.transducers.doubling import DoublingTransducer, apply_double
from collatz.transducers.odd_part import odd_part_word
from collatz.transducers.valuation_languages import ValuationClassDFA

__all__ = [
    "DivideByTwoPowerTransducer",
    "DivideByTwoTransducer",
    "DoublingTransducer",
    "LeftoverCarryError",
    "ValuationClassDFA",
    "apply_divisible",
    "apply_double",
    "apply_even",
    "odd_part_word",
]
