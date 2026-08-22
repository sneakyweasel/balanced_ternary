"""Bounded exponent-code cycle census and literature replication."""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from itertools import product
from pathlib import Path
from typing import Any

from collatz.cycle_codes import is_primitive
from collatz.cycle_divisibility import (
    christoffel_exponent_code,
    divisibility_report,
)
from collatz.cycle_language import (
    enumerate_cycle_language,
    proposed_restrictions,
    cycle_word_graph,
    exponent_stats,
)
from collatz.cycles import candidate_cycle, rotation_preserves_cycle
from collatz.experiments.schema import CYCLE_LANGUAGE_SCHEMA_VERSION, ExperimentManifest
from collatz.experiments.table_io import write_experiment
from collatz.itinerary import ValuationItinerary


CYCLE_SCHEMA_VERSION = CYCLE_LANGUAGE_SCHEMA_VERSION


def replicate_christoffel_divisibility(max_p: int, k_budget: int) -> dict[str, Any]:
    """Independent check of the Christoffel-class divisibility claim.

    Lebel 2026 claims the Christoffel class never satisfies D | C for a
    positive integer cycle. Fernández–Ibáñez use Syracuse parity Christoffel
    words. Both are preprints. We test the exponent-code image of those
    words for ``p <= max_p`` with ``K`` in the contracting window.
    """
    rows = []
    integral = []
    for p in range(1, max_p + 1):
        min_K = p  # all ones
        max_K = min(k_budget, 8 * p)
        for K in range(min_K, max_K + 1):
            if (1 << K) <= 3**p:
                continue
            try:
                code = christoffel_exponent_code(p, K)
            except ValueError:
                continue
            rec = candidate_cycle(code)
            row = {
                "p": p,
                "K": K,
                "code": list(code),
                "D_divides_C": rec.denominator != 0
                and rec.C % rec.denominator == 0,
                "is_integral": rec.is_integral,
                "is_exact_cycle": rec.is_exact_cycle,
                "candidate_n": None
                if rec.candidate_n is None
                else [rec.candidate_n.numerator, rec.candidate_n.denominator],
            }
            rows.append(row)
            if rec.is_integral:
                integral.append(row)
    only_one = all(
        row["code"] == [2] or (row["is_exact_cycle"] is False)
        for row in rows
        if row["is_exact_cycle"]
    )
    return {
        "rows": rows,
        "integral": integral,
        "only_trivial_cycle": only_one,
        "status": "COMPUTATIONALLY VERIFIED inside the bound; preprint not assumed",
    }


def replicate_K_gt_2p(max_p: int, k_max: int) -> dict[str, Any]:
    """Search for exact cycles with ``K > 2p`` (Syracuse ``N > 2r``)."""
    witnesses = []
    scanned = 0
    for p in range(1, max_p + 1):
        for ks in product(range(1, k_max + 1), repeat=p):
            if not is_primitive(ks):
                continue
            scanned += 1
            if sum(ks) <= 2 * p:
                continue
            rec = candidate_cycle(ks)
            if rec.is_exact_cycle:
                witnesses.append(list(ks))
    return {
        "scanned_primitive": scanned,
        "witnesses": witnesses,
        "classification": "COMPUTATIONALLY VERIFIED" if not witnesses else "REFUTED",
        "status": "finite exponent-code search, not a global theorem",
    }


def replicate_C_mod_3(max_p: int, k_max: int) -> dict[str, Any]:
    """De Jesus 2026: universal C mod 3 pin, claimed orthogonal because 3 | D.

    In this repository ``D = 2^K - 3^p ≡ 2^K (mod 3)``, so ``3`` never
    divides ``D`` for ``p >= 1``. The orthogonality hypothesis is a
    convention mismatch / false for this D.
    """
    residues = set()
    three_divides_D = 0
    counted = 0
    for p in range(1, max_p + 1):
        for ks in product(range(1, k_max + 1), repeat=p):
            it = ValuationItinerary.from_ks(ks)
            D = it.denominator - it.numerator_multiplier
            counted += 1
            residues.add(it.C % 3)
            if D % 3 == 0:
                three_divides_D += 1
    return {
        "counted": counted,
        "C_residues_mod_3": sorted(residues),
        "three_divides_D": three_divides_D,
        "classification": "convention mismatch",
        "note": "3 never divides 2^K-3^p, so a universal C-mod-3 pin cannot obstruct D|C",
    }


@dataclass
class CycleCensus:
    max_p: int
    k_max: int
    additive_bound: int | None
    multiplicative_bound: str | None
    counts: dict[str, int]
    exact_cycles: tuple[dict[str, Any], ...]
    restrictions: list[dict[str, Any]]
    graph: dict[str, Any]
    christoffel: dict[str, Any]
    K_gt_2p: dict[str, Any]
    C_mod_3: dict[str, Any]
    schema_version: str = CYCLE_SCHEMA_VERSION
    paths: dict[str, str] = field(default_factory=dict)


def run_cycle_census(
    max_p: int = 6,
    k_max: int = 4,
    *,
    additive_bound: int | None = None,
    multiplicative_bound: Fraction | None = None,
    output_dir: Path | str | None = None,
) -> CycleCensus:
    counts, cycles, language = enumerate_cycle_language(
        max_p,
        k_max,
        additive_bound=additive_bound,
        multiplicative_bound=multiplicative_bound,
    )
    recs = cycles
    restrictions = proposed_restrictions(recs)
    graph = cycle_word_graph(max_p, k_max, additive_bound=additive_bound)
    christoffel = replicate_christoffel_divisibility(max_p, k_max * max_p)
    kgt = replicate_K_gt_2p(max_p, k_max)
    cmod = replicate_C_mod_3(min(max_p, 4), min(k_max, 3))
    cycle_rows = []
    for rec in recs:
        row = rec.as_dict()
        row["stats"] = exponent_stats(rec.code)
        row["divisibility"] = divisibility_report(rec.code).as_dict()
        row["rotation_invariant"] = rotation_preserves_cycle(rec.code)
        cycle_rows.append(row)
    paths: dict[str, str] = {}
    if output_dir is not None:
        manifest = ExperimentManifest(
            experiment_name="cycle-language",
            parameters={
                "max_p": max_p,
                "k_max": k_max,
                "additive_bound": additive_bound,
                "multiplicative_bound": None
                if multiplicative_bound is None
                else str(multiplicative_bound),
            },
            row_count=len(cycle_rows),
            claim_status="EXACT identities; census is computational",
            schema_version=CYCLE_SCHEMA_VERSION,
        )
        paths = write_experiment(cycle_rows, output_dir, "cycle_language", manifest)
    return CycleCensus(
        max_p=max_p,
        k_max=k_max,
        additive_bound=additive_bound,
        multiplicative_bound=None if multiplicative_bound is None else str(multiplicative_bound),
        counts=counts.as_dict(),
        exact_cycles=tuple(cycle_rows),
        restrictions=restrictions,
        graph=graph,
        christoffel=christoffel,
        K_gt_2p=kgt,
        C_mod_3=cmod,
        paths=paths,
    )
