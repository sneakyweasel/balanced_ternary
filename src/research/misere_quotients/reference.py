"""Published misere-quotient data used as the Phase-0 oracle.

All statements here are ``KNOWN``. Finite experiments that agree with
this data are ``COMPUTATIONALLY VERIFIED`` reproductions, not theorems.
"""

from __future__ import annotations

# Plambeck 2005, Theorem 1 and Figures 3--4.
# Twenty elements in the printed order, 0-indexed against the 1-indexed table.
Q123_ELEMENTS: tuple[str, ...] = (
    "e",
    "x",
    "z",
    "a",
    "b",
    "xz",
    "xa",
    "xb",
    "z2",
    "za",
    "zb",
    "b2",
    "xz2",
    "xza",
    "xzb",
    "xb2",
    "z3",
    "zb2",
    "xz3",
    "xzb2",
)

Q123_P: frozenset[str] = frozenset({"x", "xa", "b2", "z2", "zb"})

# Action of the four generators, taken from Figure 4 (1-based images).
_X = (2, 1, 6, 7, 8, 3, 4, 5, 13, 14, 15, 16, 9, 10, 11, 12, 19, 20, 17, 18)
_Z = (3, 6, 9, 10, 11, 13, 14, 15, 17, 17, 5, 18, 19, 19, 8, 20, 9, 12, 13, 16)
_A = (4, 7, 10, 1, 11, 14, 2, 15, 17, 3, 5, 18, 19, 6, 8, 20, 9, 12, 13, 16)
_B = (5, 8, 11, 11, 12, 15, 15, 16, 5, 5, 18, 16, 8, 8, 20, 12, 11, 20, 15, 18)

Q123_GEN_ACTION: dict[str, tuple[int, ...]] = {
    "x": tuple(value - 1 for value in _X),
    "z": tuple(value - 1 for value in _Z),
    "a": tuple(value - 1 for value in _A),
    "b": tuple(value - 1 for value in _B),
}

Q123_INDEX: dict[str, int] = {name: index for index, name in enumerate(Q123_ELEMENTS)}

# Figure 3: heaps 1..5, then the 5+ row repeats.
_Q123_HEAP_PREFIX: tuple[str, ...] = ("x", "e", "z", "z", "x")
_Q123_HEAP_PERIOD: tuple[str, ...] = ("b2", "e", "a", "b", "x")

# Plambeck–Siegel 2008 / Nowakowski: published |Q_n(0.07)| checkpoints.
# These are true partial-quotient orders, not finite-context class counts.
DAWSON_Q_CHECKPOINTS: tuple[tuple[int, int], ...] = (
    (24, 24),
    (26, 144),
    (29, 176),
    (30, 360),
    (31, 520),
    (32, 552),
    (33, 638),
)

DAWSON_Q33_P_SIZE = 109

# miseregames.org Q33(0.07) pretending function, heaps 0..33.
# Words are not reduced here; P-membership is used only for the
# singleton/listed words in DAWSON_Q33_P_WORDS.
DAWSON_Q33_PHI: tuple[str, ...] = (
    "1",
    "1",
    "a",
    "a",
    "b",
    "1",
    "ab",
    "a",
    "a",
    "1",
    "c2g",
    "ab",
    "c",
    "b",
    "d",
    "1",
    "ad",
    "ac2g",
    "b",
    "ac",
    "ab",
    "e",
    "f",
    "ae",
    "g",
    "h",
    "c",
    "i",
    "j",
    "c2",
    "k",
    "l",
    "m",
    "n",
)

# Words from the published P-portion that occur as raw Phi labels.
DAWSON_Q33_P_WORDS: frozenset[str] = frozenset(
    {
        "a",
        "b2",
        "b4",
        "c",
        "ac2",
        "ad",
        "cd",
        "ac2d",
        "ad2",
        "cd2",
        "ac2d2",
        "e",
        "d2e",
        "f",
        "df",
        "d2f",
        "aef",
        "ad2ef",
        "af2",
        "ag",
        "cg",
        "ac2g",
        "adg",
        "ad2g",
        "fg",
        "dfg",
        "d2fg",
        "k",
        "l",
    }
)


def q123_heap_phi(n: int) -> str:
    """Published pretending function of 0.123 at a single heap."""

    if isinstance(n, bool) or not isinstance(n, int) or n < 0:
        raise ValueError("heap size must be a nonnegative int")
    if n == 0:
        return "e"
    if n <= 5:
        return _Q123_HEAP_PREFIX[n - 1]
    return _Q123_HEAP_PERIOD[(n - 6) % 5]


def q123_multiply(left: str, right: str) -> str:
    """Product in the published 20-element monoid, via generator action."""

    if left not in Q123_INDEX or right not in Q123_INDEX:
        raise KeyError(f"unknown 0.123 class {left!r} or {right!r}")
    index = Q123_INDEX[left]
    for generator in _factor_word(right):
        index = Q123_GEN_ACTION[generator][index]
    return Q123_ELEMENTS[index]


def q123_position_phi(heaps: tuple[int, ...]) -> str:
    """Published monoid image of a heap tuple."""

    value = "e"
    for heap in heaps:
        value = q123_multiply(value, q123_heap_phi(heap))
    return value


def q123_is_P(element: str) -> bool:
    if element not in Q123_INDEX:
        raise KeyError(f"unknown 0.123 class {element!r}")
    return element in Q123_P


def dawson_phi_predicts_P(heap: int) -> bool | None:
    """Published Q33 P-membership of Phi(heap), or None if the word is unlisted."""

    if isinstance(heap, bool) or not isinstance(heap, int) or heap < 0:
        raise ValueError("heap size must be a nonnegative int")
    if heap >= len(DAWSON_Q33_PHI):
        return None
    word = DAWSON_Q33_PHI[heap]
    if word == "1":
        return False
    if word in DAWSON_Q33_P_WORDS:
        return True
    return False


def _factor_word(element: str) -> tuple[str, ...]:
    if element == "e":
        return ()
    factors: list[str] = []
    rest = element
    while rest:
        if rest[0] not in Q123_GEN_ACTION:
            raise ValueError(f"unparsed 0.123 word {element!r}")
        generator = rest[0]
        rest = rest[1:]
        count = 1
        if rest and rest[0].isdigit():
            count = int(rest[0])
            rest = rest[1:]
        factors.extend([generator] * count)
    return tuple(factors)
