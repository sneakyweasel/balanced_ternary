"""Scout dossier. Never imported by spec or adapter."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ScoutEntry:
    target: str
    problem_definition: str
    state_space: str
    transition_relation: str
    domain: str
    known_termination: str
    known_nontermination: str
    known_cycles: str
    known_computational: str
    known_conjectures: str
    literature: tuple[str, ...]
    saturation: str
    open_questions: str
    classifications: tuple[tuple[str, str], ...]


BASELINE = (
    (
        "A(n) = sigma(n) - n is the sum of proper divisors.",
        "THEOREM",
    ),
    (
        "Catalan–Dickson: every aliquot sequence terminates or becomes periodic.",
        "CONJECTURE",
    ),
    (
        "Guy–Selfridge: many (even) aliquot sequences diverge.",
        "CONJECTURE",
    ),
    (
        "276 is the smallest start whose fate is unknown (Lehmer five: "
        "276, 552, 564, 660, 966).",
        "COMPUTATIONAL",
    ),
    (
        "OEIS A008892 records 276 through 2145 terms; term 2145 has 214 digits; "
        "whether it reaches 0 remains open.",
        "COMPUTATIONAL",
    ),
)


MAP = ScoutEntry(
    target="sigma_minus_n_276",
    problem_definition="Iterate A(n)=sigma(n)-n from n0=276.",
    state_space="positive integers, with 0 as a terminal empty menu",
    transition_relation="A(n)=sigma(n)-n when n is completely factored inside budget",
    domain="n >= 1",
    known_termination=(
        "Primes map to 1 then 0. Powers of 2 decrease. Deficient numbers often "
        "descend. Every start < 138 is settled (Lehmer). 138 terminates after a "
        "large peak."
    ),
    known_nontermination=(
        "No sequence is proved unbounded. Guy–Selfridge heuristics and drivers "
        "suggest divergence is possible."
    ),
    known_cycles=(
        "Length 1: perfect numbers (6, 28, 496, ...). Length 2: amicable pairs "
        "(220, 284). Longer sociable cycles (Poulet: 12496 period 5; 14316 period 28)."
    ),
    known_computational=(
        "276: 276, 396, 696, 1104, 1872, 3770, ... still open after 2000+ terms. "
        "552, 564, 660, 966 likewise open. Factorization of large terms is the "
        "practical barrier (FactorDB / Zimmermann / Creyaufmueller)."
    ),
    known_conjectures=(
        "Catalan–Dickson (bounded / terminate-or-cycle). Guy–Selfridge counter-"
        "conjecture (many diverge). Neither is settled."
    ),
    literature=(
        "guy-selfridge-1975-aliquot-drivers",
        "erdos-1976-aliquot",
        "oeis-A008892",
        "te-riele-1999-advances-aliquot",
        "oeis-A003416",
    ),
    saturation=(
        "Small-n classification and named cycles are classical. 276 remains open. "
        "Do not claim termination, divergence, or periodicity of 276."
    ),
    open_questions="Does the orbit of 276 terminate, become periodic, or diverge?",
    classifications=(
        ("A(n)=sigma(n)-n.", "THEOREM"),
        ("A(p)=1 for prime p; A(1)=0.", "THEOREM"),
        ("A(6)=6.", "THEOREM"),
        ("A(220)=284 and A(284)=220.", "THEOREM"),
        ("Catalan–Dickson conjecture.", "CONJECTURE"),
        ("Guy–Selfridge divergence heuristic.", "CONJECTURE"),
        ("276 is unresolved after 2145 computed terms.", "COMPUTATIONAL"),
        ("Erdős: geometric mean of A(n)/n for abundant n, etc.", "THEOREM"),
    ),
)


SCOUTS = {MAP.target: MAP}


def scout_for(name: str) -> ScoutEntry:
    return SCOUTS.get(name, MAP)
