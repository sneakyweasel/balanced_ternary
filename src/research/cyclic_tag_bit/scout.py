"""Scout dossier. Never imported by spec, adapter, or planner."""

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
        "Packet seed 101 never reaches the empty word under the stored rewrite.",
        "COMPUTATIONAL",
    ),
    (
        "The encoded map is not residue-affine; the state is a word, not a linear residue.",
        "KNOWN",
    ),
    (
        "Word rewriting sits outside the integer ProblemSpec sweet spot by design.",
        "KNOWN",
    ),
)


MAP = ScoutEntry(
    target="cyclic_tag_bit",
    problem_definition=(
        "On the stored 0|->0, 1|->11 rewrite with halt on empty, does frozen v2.3 "
        "diagnose a representation mismatch for an integer encoding of words, "
        "without a new rewrite attack and without a universality claim?"
    ),
    known_theorems=(
        "Empty is the unique word with no successor. All-zero words are fixed. "
        "Length never decreases. Seed 101 maps to 0111 and grows. The successor "
        "is not an integer affine map on the encoding."
    ),
    known_barriers=(
        "A finite seed prefix is not a halt theorem on all words. Integer encoding "
        "is not the word rewrite. Do not add a tag-system attack. Do not claim "
        "universality."
    ),
    open_questions="Whether the declared seed word reaches empty; answered negatively for this production on nonempty words.",
    literature=("baader-nipkow-1998-term-rewriting",),
    classifications=(
        ("Empty has no successor.", "KNOWN"),
        ("Length is nondecreasing.", "KNOWN"),
        ("No residue-affine cover is expected.", "KNOWN"),
        ("Integer encoding is a representation mismatch.", "KNOWN"),
    ),
)


def scout_for(name: str) -> ScoutEntry:
    del name
    return MAP
