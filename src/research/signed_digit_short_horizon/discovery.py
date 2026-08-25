"""Finite-horizon control versus 3-adic residual separation.

Semantics: two product states at the same control state are equivalent
when their maps on maximal legal words agree, including termination.
Illegal letters are not used as observations; termination is the empty
continuation. Horizon 0 is deadlock and is not counted as a genuine
residual merge.

Reuses ``signed_step``, ``ControlAutomaton``, and ``mealy_partition``.
Does not reopen the phase law or the any-word unrestricted theorem.
"""

from __future__ import annotations

from collections.abc import Sequence
from itertools import product

from research.signed_digit_constrained_controls.discovery import (
    ControlAutomaton,
    constrained_report,
    residual_merge_same_control,
)
from research.signed_digit_residual.discovery import alphabet_m, signed_step
from research.signed_digit_residual_minimality.discovery import val3
from research_engine.behavior.profile import ComplexityProfile

PAIRS: tuple[tuple[int, int], ...] = ((0, 3), (0, 9), (0, 27))
SPEC_HORIZON = 2


def critical_len(left: int, right: int) -> int:
    if left == right:
        return 0
    return val3(left - right) + 1


def truncated_congruent(left: int, right: int, horizon: int) -> bool:
    modulus = 3 ** int(horizon)
    return (int(left) - int(right)) % modulus == 0


def horizon_automaton(horizon: int, alphabet: Sequence[int]) -> ControlAutomaton:
    letters = tuple(int(letter) for letter in alphabet)
    depth = int(horizon)

    def legal(control: object) -> tuple[int, ...]:
        return letters if int(control) > 0 else ()

    return ControlAutomaton(
        f"S1_horizon_{depth}",
        depth,
        legal,
        lambda q, _u: max(int(q) - 1, 0),
        letters,
    )


def branching_horizon_automaton(horizon: int, alphabet: Sequence[int]) -> ControlAutomaton:
    """Model S2: several letters at each remaining depth, hard stop at 0."""
    auto = horizon_automaton(horizon, alphabet)
    auto.name = f"S2_branching_{int(horizon)}"
    return auto


def asymmetric_automaton(alphabet: Sequence[int] = (-1, 0, 1)) -> ControlAutomaton:
    """Model S3: first letter chooses remaining depth 1 or 2."""
    letters = tuple(int(letter) for letter in alphabet)

    def legal(control: object) -> tuple[int, ...]:
        if control == "S":
            return letters
        return letters if int(control) > 0 else ()

    def delta(control: object, letter: int) -> object:
        if control == "S":
            return 2 if int(letter) > 0 else 1
        return max(int(control) - 1, 0)

    return ControlAutomaton("S3_asymmetric", "S", legal, delta, letters)


def signed_trace(state: int, word: Sequence[int], gain: int = 1) -> tuple[int, ...]:
    residual = int(state)
    bits: list[int] = []
    for letter in word:
        residual, bit = signed_step(residual, int(letter), gain)
        bits.append(bit)
    return tuple(bits)


def legal_output_map(
    residual: int,
    automaton: ControlAutomaton,
    control: object,
    gain: int = 1,
) -> dict[tuple[int, ...], tuple[tuple[int, ...], bool]]:
    """Maximal legal words to (output, terminated). Exact finite-language map."""
    results: dict[tuple[int, ...], tuple[tuple[int, ...], bool]] = {}

    def rec(state: int, node: object, word: tuple[int, ...], outs: tuple[int, ...]) -> None:
        letters = automaton.legal(node)
        if not letters:
            results[word] = (outs, True)
            return
        for letter in letters:
            nxt, bit = signed_step(state, int(letter), gain)
            rec(nxt, automaton.delta(node, letter), word + (int(letter),), outs + (bit,))

    rec(int(residual), control, (), ())
    return results


def maps_equal(
    left: int,
    right: int,
    automaton: ControlAutomaton,
    control: object,
    gain: int = 1,
) -> bool:
    return legal_output_map(left, automaton, control, gain) == legal_output_map(
        right, automaton, control, gain
    )


def first_separating_word(
    left: int,
    right: int,
    horizon: int,
    alphabet: Sequence[int],
    gain: int = 1,
) -> tuple[int, ...] | None:
    letters = tuple(int(x) for x in alphabet)
    for length in range(1, int(horizon) + 1):
        for word in product(letters, repeat=length):
            if signed_trace(left, word, gain) != signed_trace(right, word, gain):
                return word
    return None


def pair_report(
    left: int,
    right: int,
    horizon: int,
    alphabet: Sequence[int] = (-1, 0, 1),
    gain: int = 1,
) -> dict[str, object]:
    auto = horizon_automaton(horizon, alphabet)
    agree = maps_equal(left, right, auto, auto.start, gain)
    predicted = truncated_congruent(left, right, horizon)
    depth = critical_len(left, right)
    deadlock = int(horizon) == 0
    genuine = bool(agree and left != right and not deadlock)
    return {
        "left": left,
        "right": right,
        "gain": gain,
        "horizon": int(horizon),
        "alphabet": tuple(int(x) for x in alphabet),
        "val3": val3(left - right) if left != right else None,
        "critical_len": depth,
        "agree": agree,
        "predicted_mod": predicted,
        "deadlock": deadlock,
        "genuine_merge": genuine,
        "separator": None if agree else first_separating_word(left, right, horizon, alphabet, gain),
    }


def coprime_sweep(gain: int = 1, alphabet: Sequence[int] = (-1, 0, 1)) -> tuple[dict[str, object], ...]:
    rows: list[dict[str, object]] = []
    for left, right in PAIRS:
        depth = critical_len(left, right)
        for horizon in range(0, depth + 2):
            rows.append(pair_report(left, right, horizon, alphabet, gain))
    return tuple(rows)


def truncated_congruence_holds(gain: int = 1) -> bool:
    for row in coprime_sweep(gain):
        if bool(row["agree"]) != bool(row["predicted_mod"]):
            return False
    return True


def smallest_genuine_merge() -> tuple[int, int, int]:
    """Smallest coprime-gain genuine merge: residuals, horizon."""
    return (0, 3, 1)


def genuine_merge_exists() -> bool:
    left, right, horizon = smallest_genuine_merge()
    return bool(pair_report(left, right, horizon)["genuine_merge"])


def shorter_always_separates() -> bool:
    """H2: some legal word shorter than k always separates. False."""
    return not genuine_merge_exists()


def only_deadlock_merges() -> bool:
    """H3: the only merges are horizon-0 termination. False."""
    return not genuine_merge_exists()


def horizon_u2_product_size(gain: int = 1) -> int:
    report = constrained_report(horizon_automaton(SPEC_HORIZON, alphabet_m(2)), gain)
    return int(report["product_count"])


def origin_reachable_positive_horizon_residual_merge(gain: int = 1) -> bool:
    """U_2 origin product merges distinct residuals only at remaining 0."""
    auto = horizon_automaton(SPEC_HORIZON, alphabet_m(2))
    report = constrained_report(auto, gain)
    found = residual_merge_same_control(report["reachable_product"], auto, gain)
    return any(control != 0 for _s, _t, control in found)


def asymmetric_obeys_local_truncation(gain: int = 1) -> bool:
    auto = asymmetric_automaton()
    at_one = maps_equal(0, 3, auto, 1, gain)
    at_two = maps_equal(0, 3, auto, 2, gain)
    return at_one is True and at_two is False


def lambda3_positive_horizon_is_translation() -> bool:
    """L≥1 merges exactly the known s≡t (mod 3) classes, not a new quotient."""
    alphabet = alphabet_m(1)
    probes = ((0, 1), (0, 3), (0, 9), (1, 4), (2, 5), (0, 6))
    for left, right in probes:
        for horizon in range(1, 4):
            row = pair_report(left, right, horizon, alphabet, 3)
            known = truncated_congruent(left, right, 1)
            if bool(row["agree"]) != known:
                return False
    return True


def lambda3_deadlock_merges_everything() -> bool:
    return bool(pair_report(0, 1, 0, alphabet_m(1), 3)["agree"])


def ray_automaton(word: Sequence[int]) -> ControlAutomaton:
    """One predetermined legal word. A proper subset of the complete tree."""
    path = tuple(int(letter) for letter in word)
    depth = len(path)

    def legal(control: object) -> tuple[int, ...]:
        index = int(control)
        if index < 0 or index >= depth:
            return ()
        return (path[index],)

    return ControlAutomaton(
        f"ray_{path}",
        0,
        legal,
        lambda q, _u: int(q) + 1,
        path if path else (0,),
    )


def drop_last_automaton(
    horizon: int,
    alphabet: Sequence[int],
    banned: int,
) -> ControlAutomaton:
    """Complete depth-L tree minus one last-step letter. Length-L words remain."""
    letters = tuple(int(letter) for letter in alphabet)
    depth = int(horizon)
    forbidden = int(banned)

    def legal(control: object) -> tuple[int, ...]:
        remaining = int(control)
        if remaining <= 0:
            return ()
        if remaining == 1:
            return tuple(letter for letter in letters if letter != forbidden)
        return letters

    return ControlAutomaton(
        f"drop_last_{depth}_{forbidden}",
        depth,
        legal,
        lambda q, _u: max(int(q) - 1, 0),
        letters,
    )


def language_max_len(automaton: ControlAutomaton, control: object | None = None) -> int:
    start = automaton.start if control is None else control
    longest = 0

    def rec(node: object, depth: int) -> None:
        nonlocal longest
        letters = automaton.legal(node)
        if not letters:
            longest = max(longest, depth)
            return
        for letter in letters:
            rec(automaton.delta(node, letter), depth + 1)

    rec(start, 0)
    return longest


def subset_pair_report(
    left: int,
    right: int,
    automaton: ControlAutomaton,
    gain: int = 1,
) -> dict[str, object]:
    agree = maps_equal(left, right, automaton, automaton.start, gain)
    max_len = language_max_len(automaton)
    depth = critical_len(left, right)
    predicted = max_len < depth
    return {
        "left": left,
        "right": right,
        "gain": gain,
        "name": automaton.name,
        "max_len": max_len,
        "critical_len": depth,
        "agree": agree,
        "predicted_max_len": predicted,
        "genuine_merge": bool(agree and left != right and max_len >= 1),
    }


def proper_subset_creates_extra_merge() -> bool:
    """False: a proper subset with a word of length ≥k still separates."""
    alphabet = alphabet_m(1)
    probes = (
        ray_automaton((0, 0)),
        ray_automaton((1, -1)),
        drop_last_automaton(2, alphabet, -1),
        drop_last_automaton(2, alphabet, 0),
    )
    for auto in probes:
        row = subset_pair_report(0, 3, auto, 1)
        if row["agree"] is True:
            return True
        if row["predicted_max_len"] is True:
            return True
    short_ray = subset_pair_report(0, 3, ray_automaton((0,)), 1)
    return short_ray["agree"] is not True


def max_len_criterion_holds() -> bool:
    alphabet = alphabet_m(1)
    autos = (
        horizon_automaton(0, alphabet),
        horizon_automaton(1, alphabet),
        horizon_automaton(2, alphabet),
        ray_automaton((0,)),
        ray_automaton((0, 0)),
        ray_automaton((0, 0, 0)),
        drop_last_automaton(2, alphabet, 1),
        drop_last_automaton(3, alphabet, -1),
        asymmetric_automaton(alphabet),
    )
    pairs = ((0, 3), (0, 9), (0, 1), (0, 27))
    for auto in autos:
        for left, right in pairs:
            row = subset_pair_report(left, right, auto, 1)
            if bool(row["agree"]) != bool(row["predicted_max_len"]):
                return False
    return True


def horizon_complexity_profile(gain: int = 1) -> ComplexityProfile:
    report = constrained_report(horizon_automaton(SPEC_HORIZON, alphabet_m(2)), gain)
    return ComplexityProfile(
        control_count=len(alphabet_m(2)),
        raw_contribution_count=len(alphabet_m(2)),
        reachable_state_count=int(report["product_count"]),
        behavioral_state_count=int(report["mealy"]),
        minimal_machine_count=int(report["mealy"]),
        max_separation_depth=1,
        closure_status="EXACT_CLOSURE",
    )
