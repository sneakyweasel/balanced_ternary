"""3-adic rigidity of ``F_{λ,U}`` under a finite control automaton.

Reuses ``signed_step`` and ``mealy_partition``. Does not reopen the
finite/infinite phase law. A constant distinguishing word is not assumed.
"""

from __future__ import annotations

from collections import deque
from collections.abc import Callable, Sequence
from typing import Hashable

from bt.transducers.mealy import mealy_partition
from research.signed_digit_residual.discovery import (
    alphabet_m,
    reachable_from,
    signed_step,
)
from research.signed_digit_residual_minimality.discovery import val3

Control = Hashable
SINK = ("SINK",)
ILLEGAL_OUT = 99

LegalFn = Callable[[Control], tuple[int, ...]]
DeltaFn = Callable[[Control, int], Control]


def any_word_separates(left: int, right: int, word: Sequence[int], gain: int = 1) -> bool:
    if left == right or len(word) != val3(left - right) + 1:
        return False
    out_l: list[int] = []
    out_r: list[int] = []
    state_l, state_r = left, right
    for letter in word:
        state_l, bit_l = signed_step(state_l, int(letter), gain)
        state_r, bit_r = signed_step(state_r, int(letter), gain)
        out_l.append(bit_l)
        out_r.append(bit_r)
    return tuple(out_l) != tuple(out_r)


class ControlAutomaton:
    """Finite legality/next-state map. Not a new research engine."""

    def __init__(
        self,
        name: str,
        start: Control,
        legal: LegalFn,
        delta: DeltaFn,
        alphabet: Sequence[int],
    ) -> None:
        self.name = name
        self.start = start
        self._legal = legal
        self._delta = delta
        self.alphabet = tuple(int(letter) for letter in alphabet)

    def legal(self, control: Control) -> tuple[int, ...]:
        return self._legal(control)

    def delta(self, control: Control, letter: int) -> Control:
        return self._delta(control, letter)


def periodic_automaton(letter: int) -> ControlAutomaton:
    return ControlAutomaton(
        "A_periodic",
        0,
        lambda _q: (letter,),
        lambda q, _u: q,
        (letter,),
    )


def alternating_automaton(first: int, second: int) -> ControlAutomaton:
    return ControlAutomaton(
        "B_alternating",
        0,
        lambda q: (first,) if q == 0 else (second,),
        lambda q, _u: 1 - int(q),
        (first, second) if first != second else (first,),
    )


def norepeat_automaton(alphabet: Sequence[int], start: Control = None) -> ControlAutomaton:
    letters = tuple(int(x) for x in alphabet)

    def legal(control: Control) -> tuple[int, ...]:
        if control is start:
            return letters
        return tuple(letter for letter in letters if letter != control)

    return ControlAutomaton(
        "C_norepeat",
        start,
        legal,
        lambda _q, letter: letter,
        letters,
    )


def parity_automaton(even: Sequence[int], odd: Sequence[int]) -> ControlAutomaton:
    even_t = tuple(int(x) for x in even)
    odd_t = tuple(int(x) for x in odd)
    alphabet = tuple(dict.fromkeys(even_t + odd_t))
    return ControlAutomaton(
        "D_parity",
        0,
        lambda q: even_t if q == 0 else odd_t,
        lambda q, _u: 1 - int(q),
        alphabet,
    )


def product_reachable(
    automaton: ControlAutomaton,
    gain: int = 1,
    cap: int = 256,
) -> frozenset[tuple[int, Control]] | None:
    start = (0, automaton.start)
    seen: set[tuple[int, Control]] = {start}
    queue = deque([start])
    while queue:
        residual, control = queue.popleft()
        for letter in automaton.legal(control):
            nxt, _out = signed_step(residual, letter, gain)
            state = (nxt, automaton.delta(control, letter))
            if state not in seen:
                seen.add(state)
                queue.append(state)
                if len(seen) > cap:
                    return None
    return frozenset(seen)


def _complete_step(
    automaton: ControlAutomaton,
    gain: int,
    state: object,
    letter: int,
) -> tuple[object, int]:
    if state is SINK:
        return SINK, ILLEGAL_OUT
    residual, control = state  # type: ignore[misc]
    if letter not in automaton.legal(control):
        return SINK, ILLEGAL_OUT
    nxt, out = signed_step(int(residual), letter, gain)
    return (nxt, automaton.delta(control, letter)), out


def product_mealy_count(
    states: Sequence[tuple[int, Control]],
    automaton: ControlAutomaton,
    gain: int = 1,
) -> int:
    completed = list(states) + [SINK]

    def step(state: object, letter: int) -> tuple[object, int]:
        return _complete_step(automaton, gain, state, letter)

    parts = mealy_partition(completed, automaton.alphabet, step)
    return len(tuple(part for part in parts if SINK not in part))


def product_merged_classes(
    states: Sequence[tuple[int, Control]],
    automaton: ControlAutomaton,
    gain: int = 1,
) -> tuple[tuple[object, ...], ...]:
    completed = list(states) + [SINK]

    def step(state: object, letter: int) -> tuple[object, int]:
        return _complete_step(automaton, gain, state, letter)

    parts = mealy_partition(completed, automaton.alphabet, step)
    live = tuple(part for part in parts if SINK not in part)
    return tuple(tuple(sorted(part, key=str)) for part in live if len(part) > 1)


def residual_merge_same_control(
    states: Sequence[tuple[int, Control]],
    automaton: ControlAutomaton,
    gain: int = 1,
) -> tuple[tuple[int, int, Control], ...]:
    """Distinct residuals at one control state in the same Mealy class."""
    merged = product_merged_classes(states, automaton, gain)
    found: list[tuple[int, int, Control]] = []
    for block in merged:
        by_control: dict[Control, list[int]] = {}
        for item in block:
            residual, control = item  # type: ignore[misc]
            by_control.setdefault(control, []).append(int(residual))
        for control, residuals in by_control.items():
            uniq = sorted(set(residuals))
            if len(uniq) > 1:
                found.append((uniq[0], uniq[1], control))
    return tuple(found)


def constrained_report(automaton: ControlAutomaton, gain: int = 1) -> dict[str, object]:
    reached = product_reachable(automaton, gain)
    assert reached is not None
    states = tuple(sorted(reached, key=str))
    residuals = frozenset(residual for residual, _control in states)
    controls = frozenset(control for _residual, control in states)
    unconstrained = reachable_from(0, automaton.alphabet, gain)
    assert unconstrained is not None
    mealy = product_mealy_count(states, automaton, gain)
    merged = product_merged_classes(states, automaton, gain)
    residual_merges = residual_merge_same_control(states, automaton, gain)
    return {
        "name": automaton.name,
        "gain": gain,
        "alphabet": automaton.alphabet,
        "reachable_product": states,
        "product_count": len(states),
        "residual_count": len(residuals),
        "control_count": len(controls),
        "unconstrained_count": len(unconstrained),
        "mealy": mealy,
        "minimal_product": mealy == len(states),
        "merged": merged,
        "residual_merges": residual_merges,
    }


def model_family(gain: int = 1) -> tuple[dict[str, object], ...]:
    u2 = alphabet_m(2)
    return (
        constrained_report(periodic_automaton(2), gain),
        constrained_report(alternating_automaton(0, 2), gain),
        constrained_report(norepeat_automaton(u2), gain),
        constrained_report(parity_automaton((0, 2), (1,)), gain),
        constrained_report(parity_automaton(u2, u2), gain),
    )


def norepeat_u2_product_size(gain: int = 1) -> int:
    report = constrained_report(norepeat_automaton(alphabet_m(2)), gain)
    return int(report["product_count"])


def constant_word_is_required() -> bool:
    """False: no-repeat forbids constants but remains product-minimal."""
    report = constrained_report(norepeat_automaton(alphabet_m(2)), 1)
    return not report["minimal_product"]


def residual_merge_exists() -> bool:
    for gain in (1, 2):
        for report in model_family(gain):
            if report["residual_merges"]:
                return True
    return False


def bisimilar_parity_collapses_controls() -> bool:
    report = constrained_report(parity_automaton(alphabet_m(2), alphabet_m(2)), 1)
    return (
        report["mealy"] == report["residual_count"]
        and report["mealy"] < report["product_count"]
        and not report["residual_merges"]
    )
