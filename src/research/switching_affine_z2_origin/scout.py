"""Scout dossier. Never imported by spec or adapter."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ScoutEntry:
    target: str
    problem_definition: str
    known_theorems: str
    known_barriers: str
    open_questions: str
    literature: tuple[str, ...]
    classifications: tuple[tuple[str, str], ...]


BASELINE = (
    (
        "Termination of purely affine (single-update) integer loops is decidable.",
        "THEOREM",
    ),
    (
        "General multi-path integer linear-constraint loops remain open.",
        "UNKNOWN",
    ),
    (
        "The stored representative is the two-path loop on Z^2 with the declared guards.",
        "COMPUTATIONAL",
    ),
)


MAP = ScoutEntry(
    target="two_path_z2",
    problem_definition=(
        "On the deterministic two-path integer map "
        "if y >= 1 then (x,y):=(x+y, y-1) else if x >= 1 then (x,y):=(x-1, x+y) "
        "else halt, is (0,0) reachable from (3,2), and does the loop terminate "
        "from every nonnegative seed?"
    ),
    known_theorems=(
        "Affine SLC termination over Z is decidable (Hosseini–Ouaknine–Worrell). "
        "Single-path affine loops are in that fragment."
    ),
    known_barriers=(
        "Two-path updates leave the decidable affine-SLC fragment. No ranking "
        "function or origin certificate is supplied to the adapter."
    ),
    open_questions="Origin reachability from (3,2); universal termination on N^2.",
    literature=(
        "ben-amram-genaim-ouaknine-worrell-2025-termination-survey",
        "hosseini-ouaknine-worrell-2019-termination-linear-loops",
    ),
    classifications=(
        ("Affine integer-loop termination is decidable.", "THEOREM"),
        ("Multi-path integer-loop termination is open in general.", "UNKNOWN"),
        ("This explicit two-path instance is the board's locked representative.", "COMPUTATIONAL"),
    ),
)


def scout_for(name: str) -> ScoutEntry:
    del name
    return MAP
