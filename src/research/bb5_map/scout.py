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
    known_generalized_collatz: str
    known_reductions: str
    known_invariants: str
    known_computational: str
    known_conjectures: str
    literature: tuple[str, ...]
    saturation: str
    open_questions: str
    classifications: tuple[tuple[str, str], ...]


BASELINE = (
    (
        "The Marxen–Buntrock 5-state machine simulates a partial residue-selected "
        "affine map B on nonnegative integers (Michel).",
        "THEOREM",
    ),
    (
        "Blank-tape halting of that machine is equivalent to the finite orbit of B "
        "from 0 reaching the undefined residue. This is settled: BB(5)=47,176,870 "
        "(bbchallenge 2024/2025).",
        "THEOREM",
    ),
    (
        "Totality of the machine on all inputs is a different statement from blank-tape "
        "halting, and is equivalent to convergence of B on all nonnegative seeds "
        "(Michel). Yolcu–Aaronson–Heule (2021/2023) did not prove termination of the "
        "corresponding mixed {3,5}-ary rewriting system.",
        "KNOWN",
    ),
    (
        "Map convergence, BB-5 totality, and a generalized-Collatz theorem are not "
        "the same claim.",
        "THEOREM",
    ),
)


MAP = ScoutEntry(
    target="partial_five_three",
    problem_definition=(
        "B(n)=(5n+18)/3 if n≡0 (mod 3); (5n+22)/3 if n≡1 (mod 3); undefined "
        "if n≡2 (mod 3). Michel's generalized-Collatz map for the BB-5 candidate."
    ),
    state_space="nonnegative integers",
    transition_relation="the unique y with 3y in {5n+18, 5n+22}, when it exists",
    domain="n >= 0",
    known_termination=(
        "The orbit from 0 is finite and hits n≡2 (mod 3) at 12284. This is the "
        "blank-tape run of the Marxen–Buntrock machine, used in the BB(5) value. "
        "Universal convergence of B on all n>=0 was not proved by the 2021/2023 "
        "rewriting approach."
    ),
    known_nontermination="No proved infinite self-avoiding trajectory on n>=0.",
    known_cycles=(
        "On Z, 3x=5x+18 gives x=-9 and 3x=5x+22 gives x=-11, both outside n>=0. "
        "No cycle is reported in the nonnegative window used here."
    ),
    known_generalized_collatz=(
        "B is a partial consistent Collatz-like map with scale 5/3 and modulus 3. "
        "It is not the Syracuse map and not an (mx+r)/2^k odd-only acceleration."
    ),
    known_reductions=(
        "Michel: the 5-state champion simulates B. Yolcu–Aaronson–Heule: mixed "
        "{3,5}-ary SRS whose termination would imply convergence of B; no proof found. "
        "bbchallenge: S(5)=47176870 via a Coq/Rocq enumeration, not via a termination "
        "proof of B on all seeds."
    ),
    known_invariants="On the defined locus, 3y = 5n+18 or 5n+22. Expanding whenever defined on n>=0.",
    known_computational=(
        "0 -> 6 -> 16 -> 34 -> 64 -> 114 -> 196 -> 334 -> 564 -> 946 -> 1584 -> "
        "2646 -> 4416 -> 7366 -> 12284 -> bot. Small nonnegative seeds empirically halt."
    ),
    known_conjectures=(
        "Whether every n>=0 eventually hits n≡2 (mod 3) under B. Distinct from BB(5) "
        "and from the classical Collatz conjecture."
    ),
    literature=(
        "michel-1993-busy-beaver-collatz",
        "michel-2015-busy-beaver-number-theory",
        "yolcu-aaronson-heule-2023-automated-collatz",
        "bbchallenge-2025-fifth-busy-beaver",
        "aaronson-2020-busy-beaver-frontier",
    ),
    saturation=(
        "The integer graph of B is elementary. Blank-tape / seed-0 halt is settled. "
        "Universal convergence on N remains a Collatz-like question and must not be claimed."
    ),
    open_questions="Does every nonnegative orbit of B eventually become undefined?",
    classifications=(
        ("Integer restriction of B is a partial function.", "THEOREM"),
        ("3y=5n+18 on n≡0 (mod 3) and 3y=5n+22 on n≡1 (mod 3).", "THEOREM"),
        ("Seed 0 reaches the undefined class.", "THEOREM"),
        ("BB(5)=47176870.", "THEOREM"),
        ("Universal convergence of B on N was not proved by the 2021 rewriting method.", "KNOWN"),
    ),
)


SCOUTS = {MAP.target: MAP}


def scout_for(name: str) -> ScoutEntry:
    return SCOUTS[name]
