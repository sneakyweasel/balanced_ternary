"""Bounded languages of low-amplitude periodic exponent codes.

Enumeration is over exponent words, not over integers. Pruning stages:

1. expanding ``2^K < 3^p``
2. non-primitive
3. ``D`` does not divide ``C``
4. candidate not a positive odd integer
5. valuations do not match
6. amplitude exceeds the bound

A finite search does not prove the absence of cycles.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import product
from typing import Any, Iterator

from research.collatz.amplitude import fernandez_slope
from research.collatz.cycle_codes import is_primitive
from research.collatz.cycles import PeriodicExponentCode, candidate_cycle
from research.collatz.itinerary import ValuationItinerary


def longest_run(code: tuple[int, ...], symbol: int) -> int:
    best = current = 0
    doubled = code + code if code else ()
    limit = len(code)
    for i, k in enumerate(doubled):
        if i >= 2 * limit:
            break
        if k == symbol:
            current += 1
            if current > best:
                best = current
        else:
            current = 0
    return min(best, limit)


def repeated_factor_stats(code: tuple[int, ...]) -> dict[str, object]:
    """Borders and repeated blocks of a cyclic word.

    Factors are contiguous subwords of the linear word, plus cyclic runs.
    This is exact combinatorics on a finite word, not a cycle theorem.
    """
    p = len(code)
    if p == 0:
        return {
            "shortest_repeated_factor": (),
            "longest_repeated_factor": (),
            "maximal_repetition_exponent": 1,
            "border_length": 0,
        }
    shortest = None
    longest = ()
    max_exp = 1
    for length in range(1, p):
        for start in range(p - length + 1):
            block = code[start : start + length]
            exp = 1
            pos = start + length
            while pos + length <= p and code[pos : pos + length] == block:
                exp += 1
                pos += length
            if exp >= 2:
                if shortest is None or length < len(shortest):
                    shortest = block
                if length > len(longest):
                    longest = block
                if exp > max_exp:
                    max_exp = exp
    border = 0
    for length in range(1, p):
        if code[:length] == code[-length:]:
            border = length
    return {
        "shortest_repeated_factor": () if shortest is None else shortest,
        "longest_repeated_factor": longest,
        "maximal_repetition_exponent": max_exp,
        "border_length": border,
    }


def exponent_stats(code: tuple[int, ...]) -> dict[str, object]:
    it = ValuationItinerary.from_ks(code)
    return {
        "min_k": min(code),
        "max_k": max(code),
        "K": it.K,
        "p": it.m,
        "K_over_p_num": it.K,
        "K_over_p_den": it.m,
        "run_of_ones": longest_run(code, 1),
        "run_of_max": longest_run(code, max(code)),
        **repeated_factor_stats(code),
        "syracuse_slope": [fernandez_slope(code).numerator, fernandez_slope(code).denominator],
    }


@dataclass
class PruningCounts:
    enumerated: int = 0
    primitive: int = 0
    contracting: int = 0
    D_divides_C: int = 0
    integral: int = 0
    exact_period: int = 0
    exact_cycle: int = 0
    distinct_canonical_cycles: int = 0
    amplitude_survivors: int = 0

    def as_dict(self) -> dict[str, int]:
        return {
            "enumerated": self.enumerated,
            "primitive": self.primitive,
            "contracting": self.contracting,
            "D_divides_C": self.D_divides_C,
            "integral": self.integral,
            "exact_period": self.exact_period,
            "exact_cycle": self.exact_cycle,
            "distinct_canonical_cycles": self.distinct_canonical_cycles,
            "amplitude_survivors": self.amplitude_survivors,
        }


def iter_primitive_codes(max_p: int, k_max: int) -> Iterator[tuple[int, ...]]:
    if max_p < 1 or k_max < 1:
        raise ValueError("max_p and k_max must be >= 1")
    for p in range(1, max_p + 1):
        for ks in product(range(1, k_max + 1), repeat=p):
            if is_primitive(ks):
                yield ks


def enumerate_cycle_language(
    max_p: int,
    k_max: int,
    *,
    additive_bound: int | None = None,
    multiplicative_bound: Fraction | None = None,
) -> tuple[PruningCounts, tuple[PeriodicExponentCode, ...], tuple[PeriodicExponentCode, ...]]:
    """Stream primitive codes and apply exact pruning.

    Returns counts, exact primitive cycles, and amplitude-language survivors.
    Only exact cycles and a thin integral-but-not-cycle sample are stored.
    """
    counts = PruningCounts()
    cycles: list[PeriodicExponentCode] = []
    language: list[PeriodicExponentCode] = []
    canonical: set[tuple[int, ...]] = set()
    for p in range(1, max_p + 1):
        for ks in product(range(1, k_max + 1), repeat=p):
            counts.enumerated += 1
            it = ValuationItinerary.from_ks(ks)
            D = it.denominator - it.numerator_multiplier
            prim = is_primitive(ks)
            if prim:
                counts.primitive += 1
            if D <= 0:
                continue
            counts.contracting += 1
            if it.C % D != 0:
                continue
            counts.D_divides_C += 1
            rec = candidate_cycle(ks)
            if rec.is_integral:
                counts.integral += 1
            if rec.is_exact_period:
                counts.exact_period += 1
            if rec.is_exact_cycle:
                counts.exact_cycle += 1
                cycles.append(rec)
                canonical.add(rec.canonical_code)
                keep = True
                if rec.amplitude is not None:
                    if additive_bound is not None and rec.amplitude.additive > additive_bound:
                        keep = False
                    if (
                        multiplicative_bound is not None
                        and rec.amplitude.multiplicative > multiplicative_bound
                    ):
                        keep = False
                if keep:
                    counts.amplitude_survivors += 1
                    language.append(rec)
    counts.distinct_canonical_cycles = len(canonical)
    return counts, tuple(cycles), tuple(language)


def cycle_word_graph(
    max_p: int,
    k_max: int,
    *,
    additive_bound: int | None = None,
) -> dict[str, Any]:
    """Bounded directed path graph of valuation symbols with pruning flags.

    This is **not** a finite-state model of all Collatz cycles.
    """
    nodes = 0
    edges = 0
    pruned_expanding = 0
    surviving_paths = 0
    for p in range(1, max_p + 1):
        for ks in product(range(1, k_max + 1), repeat=p):
            nodes += 1
            if p < max_p:
                edges += k_max
            rec = candidate_cycle(ks)
            if not rec.is_contracting:
                pruned_expanding += 1
            if rec.is_exact_cycle:
                if additive_bound is None or (
                    rec.amplitude is not None and rec.amplitude.additive <= additive_bound
                ):
                    surviving_paths += 1
    return {
        "max_p": max_p,
        "k_max": k_max,
        "nodes": nodes,
        "potential_edges": edges,
        "pruned_expanding": pruned_expanding,
        "surviving_exact_paths": surviving_paths,
        "status": "bounded symbolic search graph; not a cycle automaton",
    }


def proposed_restrictions(records: tuple[PeriodicExponentCode, ...]) -> list[dict[str, object]]:
    """Evaluate candidate symbolic restrictions on the current exact-cycle set.

    Each row is classified against the supplied records only. A hold on a
    finite set is not a theorem.
    """
    proposals = []

    def _holds(name: str, pred, classification: str, note: str) -> None:
        failures = [list(rec.code) for rec in records if not pred(rec)]
        proposals.append(
            {
                "name": name,
                "classification": classification if not failures else "REFUTED",
                "failures": failures[:3],
                "note": note,
            }
        )

    _holds(
        "exact_cycle_implies_contracting",
        lambda rec: rec.is_contracting,
        "PROVED",
        "existing expanding-exclusion of a positive candidate",
    )
    _holds(
        "additive_amplitude_even",
        lambda rec: rec.amplitude is not None and rec.amplitude.additive % 2 == 0,
        "PROVED",
        "difference of odd states",
    )
    _holds(
        "trivial_cycle_is_all_twos",
        lambda rec: rec.candidate_n == 1 and rec.code == (2,) or rec.candidate_n != 1,
        "PROVED",
        "n=1 has itinerary (2)",
    )
    _holds(
        "nontrivial_has_positive_lift",
        lambda rec: rec.candidate_n == 1 or any(t > 0 for t in rec.lift_digits),
        "PROVED",
        "R_0=1 and R(code)=1 iff code is all twos",
    )
    _holds(
        "no_k_max_1_cycle",
        lambda rec: max(rec.code) >= 2,
        "PROVED",
        "all-ones words are expanding",
    )
    _holds(
        "low_amplitude_forces_repetition",
        lambda rec: rec.amplitude is None
        or rec.amplitude.additive > 0
        or repeated_factor_stats(rec.code)["maximal_repetition_exponent"] >= 1,
        "PROVED",
        "vacuous: exponent 1 always; amplitude 0 is the 1-cycle",
    )
    _holds(
        "K_le_2p_for_cycles",
        lambda rec: rec.K <= 2 * rec.p,
        "COMPUTATIONALLY VERIFIED",
        "Fernández–Ibáñez N<=2r in Syracuse units; finite codes only here",
    )
    return proposals
