"""Scout dossiers. Never imported by spec or adapter."""

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


CARELLI_BASELINE = (
    (
        "General termination of linear-constraint loops over Z, Q, and R remains open.",
        "THEOREM",
    ),
    (
        "One-variable integer loops are tightly connected to generalized Collatz sequences.",
        "THEOREM",
    ),
    (
        "Termination of these loops is tied to a longstanding generalized-Collatz conjecture "
        "(Reachability Conjecture / Uniform Distribution).",
        "CONJECTURE",
    ),
    (
        "If a one-variable loop has a cyclic trace, then a cyclic trace of length at most two exists.",
        "THEOREM",
    ),
)


DECREMENT = ScoutEntry(
    target="slc_decrement",
    problem_definition="while x >= 1 do x := x - 1",
    state_space="Z",
    transition_relation="x' = x - 1 subject to the guard",
    domain="x >= 1",
    known_termination="Terminates from every integer: ranking function x on x >= 1, and x < 1 is already exited.",
    known_nontermination="None.",
    known_cycles="No cycles.",
    known_generalized_collatz="None. Affine single-path loop, not a residue-class map.",
    known_reductions="Affine SLC termination over Z is decidable (Hosseini–Ouaknine–Worrell 2019).",
    known_invariants="x decreases by 1 at each step.",
    known_computational="Trivial exhaustive check on any finite interval.",
    known_conjectures="None.",
    literature=(
        "carelli-2026-loop-termination",
        "hosseini-ouaknine-worrell-2019-termination-linear-loops",
        "tiwari-2004-termination-linear-programs",
        "braverman-2006-termination-integer-linear",
    ),
    saturation="Fully settled elementary ranking-function example.",
    open_questions="None for this instance.",
    classifications=(
        ("Terminates from every integer.", "THEOREM"),
        ("Affine SLC termination over Z is decidable in general.", "THEOREM"),
        ("No cycle.", "THEOREM"),
    ),
)


NEGATION = ScoutEntry(
    target="slc_negation",
    problem_definition="x' := -x with no guard",
    state_space="Z",
    transition_relation="x' = -x",
    domain="all of Z",
    known_termination="Does not terminate: every integer lies on a cycle.",
    known_nontermination="Infinite traces exist (in fact every trace is infinite).",
    known_cycles="Length 1 at 0; length 2 at every nonzero pair {x, -x}.",
    known_generalized_collatz="None required. Affine involution.",
    known_reductions="Carelli Theorem 3.20: a cycle implies a cycle of length at most two. Here both lengths occur.",
    known_invariants="|x| is constant. Parity of the step index selects the sign.",
    known_computational="Immediate.",
    known_conjectures="None.",
    literature=("carelli-2026-loop-termination",),
    saturation="Fully settled.",
    open_questions="None for this instance.",
    classifications=(
        ("Every integer is periodic of period 1 or 2.", "THEOREM"),
        ("Carelli length-(<=2) cyclic-trace theorem applies.", "THEOREM"),
    ),
)


RPLUS = ScoutEntry(
    target="slc_rplus",
    problem_definition=(
        "R+ = {(x, x') in R^2 | 4x-2 <= 3 x' <= 4x-1 and x >= 3}, "
        "Carelli Example 4.26 / Figure 2."
    ),
    state_space="Z, with integer transitions the integer points of R+",
    transition_relation="the strip 4x-2 <= 3 x' <= 4x-1 with x >= 3",
    domain="x >= 3",
    known_termination="Open in general. Equivalent to every orbit of floor(4x/3) hitting a multiple of 3.",
    known_nontermination="No proved infinite self-avoiding trace. Expanding on x >= 3 whenever a successor exists.",
    known_cycles="No cycle inside x >= 3, because x' > x whenever a successor exists. Length-1 solutions of the unrestricted strip sit at x=1 and x=2, outside the guard.",
    known_generalized_collatz=(
        "Weak Collatz mapping T(x) = (4x - i)/3 when 4x ≡ i (mod 3), equivalently T(x) = floor(4x/3). "
        "R+ is the SLC that follows this map while avoiding the residue that makes 3 | T^k(n)."
    ),
    known_reductions="Proposition 4.25: a weak Collatz mapping with m > d yields two SLCs R+ and R- whose infinite traces are exactly the avoiding orbits.",
    known_invariants="On integer points, at most one successor. Recessive direction of the strip is (3,4).",
    known_computational="Small n >= 3 empirically hit a multiple of 3 after a finite expanding prefix.",
    known_conjectures=(
        "Reachability Conjecture for this mapping: for every n >= 3 there exists k with 3 | T^k(n). "
        "Carelli records this instance as open."
    ),
    literature=(
        "carelli-2026-loop-termination",
        "matthews-watts-1984-generalization-hasse",
        "moller-1978-hasse-syracuse",
        "ben-amram-genaim-ouaknine-worrell-2025-termination-survey",
    ),
    saturation=(
        "The arithmetic of the integer graph is known. Universal termination is an open "
        "Reachability-Conjecture instance and must not be claimed."
    ),
    open_questions="Does every integer orbit starting at n >= 3 eventually lose its successor (hit a multiple of 3)?",
    classifications=(
        ("Integer restriction of R+ is a partial function.", "THEOREM"),
        ("T(x) = floor(4x/3) on the defined locus.", "THEOREM"),
        ("Reachability for this mapping remains open.", "CONJECTURE"),
        ("No cycle for x >= 3.", "THEOREM"),
    ),
)


INCREMENT = ScoutEntry(
    target="slc_increment",
    problem_definition="x' = x + 1 (Carelli Example 2.11)",
    state_space="Z",
    transition_relation="x' = x + 1",
    domain="all of Z",
    known_termination="Does not terminate.",
    known_nontermination="Infinite self-avoiding trace from every seed.",
    known_cycles="No cycles.",
    known_generalized_collatz="None.",
    known_reductions="Standard example that nontermination need not come from a cycle.",
    known_invariants="x increases by 1.",
    known_computational="Immediate.",
    known_conjectures="None.",
    literature=("carelli-2026-loop-termination",),
    saturation="Fully settled.",
    open_questions="None for this instance.",
    classifications=(
        ("No cycle, infinite self-avoiding traces.", "THEOREM"),
    ),
)


SCOUTS = {
    DECREMENT.target: DECREMENT,
    NEGATION.target: NEGATION,
    RPLUS.target: RPLUS,
    INCREMENT.target: INCREMENT,
}


def scout_for(name: str) -> ScoutEntry:
    return SCOUTS[name]
