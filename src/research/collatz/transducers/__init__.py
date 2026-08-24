"""Collatz-specific maps on balanced-ternary words.

Generic ``/2``, ``/2^k``, and doubling machines live in ``bt.transducers``.
The MSD residue automaton they dualize is ``bt.automata.modular``.
"""

from research.collatz.transducers.odd_part import odd_part_word
from research.collatz.transducers.valuation_languages import ValuationClassDFA

__all__ = [
    "ValuationClassDFA",
    "odd_part_word",
]
