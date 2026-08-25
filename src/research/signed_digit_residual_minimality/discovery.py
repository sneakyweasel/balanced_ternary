"""Exact Mealy quotient of ``F_{λ,U}`` versus origin-reachable geometry.

Reuses ``signed_step`` and ``mealy_partition``. Does not reopen the
finite/infinite phase law or the ``U_m`` fill theorems.
"""

from __future__ import annotations

from collections import deque
from collections.abc import Sequence

from bt.transducers.mealy import mealy_partition
from research.signed_digit_residual.discovery import (
    alphabet_m,
    reachable_from,
    signed_step,
)

SEARCH_ALPHABETS: tuple[tuple[int, ...], ...] = (
    (0, 1),
    (-1, 0),
    (1, 2),
    (-2, 0),
    (-2, 2),
    (-1, 1),
    (0, 2),
    (-2, 0, 2),
    (-2, -1, 2),
    (-2, 1, 2),
)


def val3(n: int) -> int:
    """3-adic valuation of a nonzero integer; ``val3(0)=0`` by convention."""
    value = abs(int(n))
    if value == 0:
        return 0
    depth = 0
    while value % 3 == 0:
        value //= 3
        depth += 1
    return depth


def predicted_sep_len(left: int, right: int) -> int:
    if left == right:
        return 0
    return val3(left - right) + 1


def val3_gap_plus_one_predictor(left: object, right: object) -> tuple[str, int]:
    """Research-layer predictor. The engine does not know 3-adic valuation."""
    src = int(left[0]) if isinstance(left, tuple) else int(left)
    tgt = int(right[0]) if isinstance(right, tuple) else int(right)
    return ("v_3_gap_plus_one", predicted_sep_len(src, tgt))


def output_signature(
    state: int,
    alphabet: Sequence[int],
    gain: int = 1,
) -> tuple[int, ...]:
    return tuple(signed_step(state, int(letter), gain)[1] for letter in alphabet)


def shortest_separating_word(
    left: int,
    right: int,
    alphabet: Sequence[int],
    gain: int = 1,
) -> tuple[int, ...] | None:
    """Shortest word with distinct output streams, or ``None`` if equivalent."""
    if left == right:
        return None
    letters = tuple(int(letter) for letter in alphabet)
    queue: deque[tuple[int, int, tuple[int, ...]]] = deque([(left, right, ())])
    seen = {(left, right)}
    while queue:
        state_l, state_r, word = queue.popleft()
        for letter in letters:
            next_l, out_l = signed_step(state_l, letter, gain)
            next_r, out_r = signed_step(state_r, letter, gain)
            nxt_word = word + (letter,)
            if out_l != out_r:
                return nxt_word
            pair = (next_l, next_r)
            if pair not in seen:
                seen.add(pair)
                queue.append((next_l, next_r, nxt_word))
    return None


def pair_report(
    left: int,
    right: int,
    alphabet: Sequence[int],
    gain: int = 1,
) -> dict[str, object]:
    word = shortest_separating_word(left, right, alphabet, gain)
    predicted = predicted_sep_len(left, right)
    return {
        "left": left,
        "right": right,
        "word": word,
        "sep_len": None if word is None else len(word),
        "predicted_sep_len": predicted,
        "matches_val3": word is not None and len(word) == predicted,
        "same_immediate_signature": output_signature(left, alphabet, gain)
        == output_signature(right, alphabet, gain),
    }


def minimality_report(
    alphabet: Sequence[int],
    gain: int = 1,
) -> dict[str, object]:
    letters = tuple(int(letter) for letter in alphabet)
    reached = reachable_from(0, letters, gain)
    assert reached is not None
    states = tuple(sorted(reached))

    def mealy(state: int, control: int) -> tuple[int, int]:
        return signed_step(state, control, gain)

    parts = mealy_partition(states, letters, mealy)
    merged = tuple(tuple(sorted(block)) for block in parts if len(block) > 1)
    pairs: list[dict[str, object]] = []
    max_len = 0
    for i, left in enumerate(states):
        for right in states[i + 1 :]:
            item = pair_report(left, right, letters, gain)
            pairs.append(item)
            sep_len = item["sep_len"]
            if isinstance(sep_len, int):
                max_len = max(max_len, sep_len)
    return {
        "alphabet": letters,
        "gain": gain,
        "reachable": states,
        "reachable_count": len(states),
        "mealy": len(parts),
        "classes": tuple(tuple(sorted(block)) for block in parts),
        "merged": merged,
        "minimal": not merged,
        "L_max": max_len,
        "pairs": tuple(pairs),
    }


def search_reports(gain: int = 1) -> tuple[dict[str, object], ...]:
    return tuple(minimality_report(alphabet, gain) for alphabet in SEARCH_ALPHABETS)


def first_merge(
    reports: Sequence[dict[str, object]] | None = None,
) -> dict[str, object] | None:
    items = reports if reports is not None else search_reports(1) + search_reports(2)
    for report in items:
        merged = report["merged"]
        if merged:
            return report
    return None


def search_is_minimal() -> bool:
    return first_merge() is None


def lambda1_zero_three_witness() -> dict[str, object]:
    """Same 1-letter signatures, separated at length 2: not a merge."""
    return pair_report(0, 3, (0,), 1)


def lambda3_translate_witness() -> dict[str, object]:
    """Global λ=3 translation symmetry: ``0 ~ 3`` under any nonempty U."""
    return pair_report(0, 3, (0,), 3)


def mod3_does_not_merge() -> bool:
    witness = lambda1_zero_three_witness()
    return witness["word"] == (0, 0) and witness["same_immediate_signature"] is True


def symmetric_family_minimal(bound: int = 8) -> bool:
    for gain in (1, 2):
        for size in range(bound + 1):
            report = minimality_report(alphabet_m(size), gain)
            if not report["minimal"]:
                return False
            if report["mealy"] != report["reachable_count"]:
                return False
            for pair in report["pairs"]:
                if pair["sep_len"] is not None and not pair["matches_val3"]:
                    return False
    return True
