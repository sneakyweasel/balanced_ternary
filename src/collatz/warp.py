"""Domain-aware composition of balanced-ternary reversal with accelerated T.

``T`` is defined only on positive odd integers. ``W`` (A134028) is defined
on every integer and need not stay positive or odd. The commutator

    Comm_WT(n) = W(T(n)) - T(W(n))

is therefore defined only when ``n`` is positive odd and ``W(n)`` is
positive odd. Otherwise ``T(W(n))`` is recorded as undefined.

No signed extension of ``T`` is introduced.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from itertools import product
from typing import Callable

from balanced_ternary.oeis_maps import (
    bt_alternating_digit_sum,
    bt_digit_sum,
    bt_is_palindrome,
    bt_length,
    bt_reverse,
    bt_reverse_tail,
)
from balanced_ternary.representation import encode
from collatz.core import collatz_step, collatz_valuation
from collatz.cylinders import parse_ks
from collatz.dual_code import CollatzDualCode, canonical_realizer_formula
from collatz.trajectory import collatz_trajectory


OPERATORS: tuple[str, ...] = ("T", "W", "Wt")


def is_positive_odd(n: object) -> bool:
    return isinstance(n, int) and not isinstance(n, bool) and n > 0 and n % 2 == 1


def _require_int(n: int, name: str = "n") -> int:
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"{name} must be int, got {type(n).__name__}")
    return n


@dataclass(frozen=True)
class WarpState:
    """Exact word/Collatz snapshot at one integer."""

    n: int
    bt_n: str
    W_n: int
    bt_W: str
    T_n: int | None
    W_T: int | None
    T_W: int | None
    Comm_WT: int | None
    s3_n: int
    s3_T: int | None
    s3_alt_n: int
    s3_alt_T: int | None
    L3_n: int
    L3_T: int | None
    palindrome_n: bool
    palindrome_T: bool | None
    delta_s: int | None
    delta_alt: int | None
    delta_L: int | None
    t_defined: bool
    t_of_W_defined: bool

    def as_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["BT(n)"] = self.bt_n
        payload["W(n)"] = self.W_n
        payload["BT(W(n))"] = self.bt_W
        payload["T(n)"] = self.T_n
        payload["W(T(n))"] = self.W_T
        payload["T(W(n))"] = self.T_W
        payload["s3(n)"] = self.s3_n
        payload["s3(T(n))"] = self.s3_T
        payload["s3_alt(n)"] = self.s3_alt_n
        payload["L3(n)"] = self.L3_n
        payload["L3(T(n))"] = self.L3_T
        payload["palindrome(n)"] = self.palindrome_n
        payload["palindrome(T(n))"] = self.palindrome_T
        return payload

    def experiment_row(self) -> dict[str, object]:
        """Stable JSONL fields for the collatz-bt-warp/v1 schema."""
        return {
            "n": self.n,
            "BT(n)": self.bt_n,
            "W(n)": self.W_n,
            "BT(W(n))": self.bt_W,
            "T(n)": self.T_n,
            "W(T(n))": self.W_T,
            "T(W(n))": self.T_W,
            "Comm_WT": self.Comm_WT,
            "s3(n)": self.s3_n,
            "s3(T(n))": self.s3_T,
            "s3_alt(n)": self.s3_alt_n,
            "L3(n)": self.L3_n,
            "L3(T(n))": self.L3_T,
            "palindrome(n)": self.palindrome_n,
            "palindrome(T(n))": self.palindrome_T,
            "delta_s": self.delta_s,
            "delta_alt": self.delta_alt,
            "delta_L": self.delta_L,
            "t_defined": self.t_defined,
            "t_of_W_defined": self.t_of_W_defined,
        }


def warp_state(n: int) -> WarpState:
    n = _require_int(n)
    w_n = bt_reverse(n)
    t_defined = is_positive_odd(n)
    t_n = collatz_step(n) if t_defined else None
    w_t = bt_reverse(t_n) if t_n is not None else None
    t_of_w_defined = is_positive_odd(w_n)
    t_w = collatz_step(w_n) if t_of_w_defined else None
    comm = None
    if w_t is not None and t_w is not None:
        comm = w_t - t_w
    s3_t = bt_digit_sum(t_n) if t_n is not None else None
    s3_alt_t = bt_alternating_digit_sum(t_n) if t_n is not None else None
    l3_t = bt_length(t_n) if t_n is not None else None
    pal_t = bt_is_palindrome(t_n) if t_n is not None else None
    s3_n = bt_digit_sum(n)
    s3_alt_n = bt_alternating_digit_sum(n)
    l3_n = bt_length(n)
    return WarpState(
        n=n,
        bt_n=encode(n).word(),
        W_n=w_n,
        bt_W=encode(w_n).word(),
        T_n=t_n,
        W_T=w_t,
        T_W=t_w,
        Comm_WT=comm,
        s3_n=s3_n,
        s3_T=s3_t,
        s3_alt_n=s3_alt_n,
        s3_alt_T=s3_alt_t,
        L3_n=l3_n,
        L3_T=l3_t,
        palindrome_n=bt_is_palindrome(n),
        palindrome_T=pal_t,
        delta_s=None if s3_t is None else s3_t - s3_n - 1,
        delta_alt=None if s3_alt_t is None else s3_alt_t - s3_alt_n,
        delta_L=None if l3_t is None else l3_t - l3_n,
        t_defined=t_defined,
        t_of_W_defined=t_of_w_defined,
    )


@dataclass(frozen=True)
class WarpedTrajectory:
    start: int
    W_start: int
    values: tuple[int, ...]
    t_started: bool
    truncated: bool
    max_steps: int

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


def warped_trajectory(n: int, max_steps: int) -> WarpedTrajectory:
    """Path ``n -> W(n) -> T(W(n)) -> ...`` while ``T`` stays defined."""
    n = _require_int(n)
    if isinstance(max_steps, bool) or not isinstance(max_steps, int) or max_steps < 0:
        raise ValueError(f"max_steps must be an integer >= 0, got {max_steps!r}")
    w = bt_reverse(n)
    values = [n, w]
    t_started = is_positive_odd(w)
    if not t_started or max_steps == 0:
        return WarpedTrajectory(
            start=n,
            W_start=w,
            values=tuple(values),
            t_started=t_started,
            truncated=False,
            max_steps=max_steps,
        )
    current = w
    steps = 0
    while steps < max_steps and current != 1:
        current = collatz_step(current)
        values.append(current)
        steps += 1
        if current == 1:
            break
    truncated = current != 1 and steps >= max_steps
    return WarpedTrajectory(
        start=n,
        W_start=w,
        values=tuple(values),
        t_started=True,
        truncated=truncated,
        max_steps=max_steps,
    )


def palindrome_along_trajectory(n: int, max_steps: int) -> tuple[dict[str, object], ...]:
    """Palindrome flags on an ordinary accelerated trajectory."""
    traj = collatz_trajectory(n, max_steps)
    rows = []
    for value in traj.values:
        rows.append(
            {
                "n": value,
                "BT(n)": encode(value).word(),
                "palindrome": bt_is_palindrome(value),
                "W(n)": bt_reverse(value),
            }
        )
    return tuple(rows)


def apply_operator(op: str, n: int) -> int | None:
    """Apply one labelled generator. ``T`` returns None off its domain."""
    if op == "W":
        return bt_reverse(_require_int(n))
    if op == "Wt":
        return bt_reverse_tail(_require_int(n))
    if op == "T":
        if not is_positive_odd(n):
            return None
        return collatz_step(n)
    raise ValueError(f"unknown operator {op!r}; expected one of {OPERATORS}")


def apply_word(ops: tuple[str, ...] | list[str] | str, n: int) -> int | None:
    """Compose generators left-to-right. None means some ``T`` was undefined."""
    if isinstance(ops, str):
        tokens = tuple(ops.split()) if " " in ops else tuple(ops.split(","))
        if tokens == ("",):
            tokens = ()
    else:
        tokens = tuple(ops)
    value: int | None = _require_int(n)
    for op in tokens:
        if value is None:
            return None
        value = apply_operator(op, value)
    return value


def _word_key(ops: tuple[str, ...]) -> str:
    return "id" if not ops else " ".join(ops)


def enumerate_operator_words(max_length: int) -> tuple[tuple[str, ...], ...]:
    if (
        isinstance(max_length, bool)
        or not isinstance(max_length, int)
        or max_length < 0
    ):
        raise ValueError("max_length must be an integer >= 0")
    words: list[tuple[str, ...]] = [()]
    for length in range(1, max_length + 1):
        words.extend(product(OPERATORS, repeat=length))
    return tuple(words)


NAIVE_IDENTITIES: tuple[tuple[str, tuple[str, ...], tuple[str, ...]], ...] = (
    ("W W = id", ("W", "W"), ()),
    ("Wt Wt = id", ("Wt", "Wt"), ()),
    ("W T = T W", ("W", "T"), ("T", "W")),
    ("Wt T = T Wt", ("Wt", "T"), ("T", "Wt")),
    ("W T = T", ("W", "T"), ("T",)),
    ("T W = T", ("T", "W"), ("T",)),
)


def smallest_disagreement(
    left: tuple[str, ...],
    right: tuple[str, ...],
    limit: int,
    *,
    odd_only: bool = True,
) -> int | None:
    """Smallest n in the scan where both sides are defined and differ."""
    if limit < 0:
        raise ValueError("limit must be >= 0")
    values = range(1, limit + 1, 2) if odd_only else range(-limit, limit + 1)
    for n in values:
        if n == 0:
            continue
        left_val = apply_word(left, n)
        right_val = apply_word(right, n)
        if left_val is None or right_val is None:
            continue
        if left_val != right_val:
            return n
    return None


def identity_table(limit: int, max_length: int = 6) -> dict[str, object]:
    """Naive identities versus smallest counterexamples on a finite domain."""
    records = []
    for name, left, right in NAIVE_IDENTITIES:
        witness = smallest_disagreement(left, right, limit)
        records.append(
            {
                "name": name,
                "left": _word_key(left),
                "right": _word_key(right),
                "smallest_counterexample": witness,
                "holds_on_bound": witness is None,
                "status": (
                    "VERIFIED COMPUTATIONALLY on the bound"
                    if witness is None
                    else "REFUTED; smallest counterexample recorded"
                ),
            }
        )
    words = enumerate_operator_words(max_length)
    return {
        "limit": limit,
        "max_length": max_length,
        "word_count": len(words),
        "naive_identities": records,
    }


Predicate = Callable[[WarpState], bool]


SPECIAL_CLASS_PREDICATES: dict[str, Predicate] = {
    "palindrome": lambda state: state.palindrome_n,
    "length_1": lambda state: state.L3_n == 1,
    "length_2": lambda state: state.L3_n == 2,
    "length_3": lambda state: state.L3_n == 3,
    "sparse_weight_1": lambda state: encode(state.n).word().count("0")
    == len(encode(state.n)) - 1
    and state.n != 0,
    "tail_fixed": lambda state: bt_reverse_tail(state.n) == state.n,
    "trailing_plus": lambda state: state.bt_n.endswith("+"),
    "trailing_minus": lambda state: state.bt_n.endswith("-"),
    "trailing_zero": lambda state: state.bt_n.endswith("0"),
}


def _iter_odds(limit: int):
    if isinstance(limit, bool) or not isinstance(limit, int) or limit < 1:
        raise ValueError("limit must be an integer >= 1")
    return range(1, limit + 1, 2)


def commutator_census(limit: int) -> dict[str, object]:
    """Exact commutator census on positive odd integers up to ``limit``."""
    defined = 0
    zero = 0
    nonzero: list[tuple[int, int]] = []
    residue_mod_9: dict[int, int] = {}
    residue_mod_4: dict[int, int] = {}
    delta_s_values: dict[int, int] = {}
    delta_l_values: dict[int, int] = {}
    palindrome_comm_zero = 0
    palindrome_defined = 0
    smallest_defined = None
    smallest_zero = None
    smallest_nonzero = None
    for n in _iter_odds(limit):
        state = warp_state(n)
        if state.delta_s is not None:
            delta_s_values[state.delta_s] = delta_s_values.get(state.delta_s, 0) + 1
        if state.delta_L is not None:
            delta_l_values[state.delta_L] = delta_l_values.get(state.delta_L, 0) + 1
        if not state.t_of_W_defined:
            continue
        defined += 1
        if smallest_defined is None:
            smallest_defined = n
        comm = state.Comm_WT
        assert comm is not None
        if comm == 0:
            zero += 1
            if smallest_zero is None:
                smallest_zero = n
            residue_mod_9[n % 9] = residue_mod_9.get(n % 9, 0) + 1
            residue_mod_4[n % 4] = residue_mod_4.get(n % 4, 0) + 1
            if state.palindrome_n:
                palindrome_comm_zero += 1
        else:
            nonzero.append((n, comm))
            if smallest_nonzero is None:
                smallest_nonzero = {"n": n, "Comm_WT": comm, "W(n)": state.W_n}
        if state.palindrome_n:
            palindrome_defined += 1
    nonzero.sort(key=lambda item: (abs(item[1]), item[0]))
    odd_count = (limit + 1) // 2
    return {
        "limit": limit,
        "odd_count": odd_count,
        "commutator_defined": defined,
        "commutator_zero": zero,
        "commutator_nonzero": defined - zero,
        "defined_density_among_odds": defined / odd_count if odd_count else 0.0,
        "zero_density_among_defined": zero / defined if defined else 0.0,
        "smallest_defined": smallest_defined,
        "smallest_zero": smallest_zero,
        "smallest_nonzero": smallest_nonzero,
        "smallest_nonzero_commutators": [
            {"n": n, "Comm_WT": comm} for n, comm in nonzero[:12]
        ],
        "zero_set_mod_9": residue_mod_9,
        "zero_set_mod_4": residue_mod_4,
        "delta_s_histogram": delta_s_values,
        "delta_L_histogram": delta_l_values,
        "delta_L_min": min(delta_l_values) if delta_l_values else None,
        "delta_L_max": max(delta_l_values) if delta_l_values else None,
        "palindrome_defined": palindrome_defined,
        "palindrome_commutator_zero": palindrome_comm_zero,
        "status": "VERIFIED COMPUTATIONALLY on the stated odd bound",
    }


def special_class_report(limit: int) -> dict[str, dict[str, object]]:
    """Commutator behaviour on named BT classes, with smallest witnesses."""
    reports: dict[str, dict[str, object]] = {}
    for name, predicate in SPECIAL_CLASS_PREDICATES.items():
        defined = 0
        zero = 0
        smallest_true = None
        smallest_defined = None
        smallest_zero = None
        smallest_nonzero = None
        for n in _iter_odds(limit):
            state = warp_state(n)
            if not predicate(state):
                continue
            if smallest_true is None:
                smallest_true = n
            if not state.t_of_W_defined:
                continue
            defined += 1
            if smallest_defined is None:
                smallest_defined = n
            if state.Comm_WT == 0:
                zero += 1
                if smallest_zero is None:
                    smallest_zero = n
            elif smallest_nonzero is None:
                smallest_nonzero = {
                    "n": n,
                    "Comm_WT": state.Comm_WT,
                    "W(n)": state.W_n,
                }
        reports[name] = {
            "smallest_member": smallest_true,
            "commutator_defined": defined,
            "commutator_zero": zero,
            "smallest_defined": smallest_defined,
            "smallest_zero": smallest_zero,
            "smallest_nonzero": smallest_nonzero,
            "universal_commutation_on_bound": defined > 0 and smallest_nonzero is None,
            "status": "VERIFIED COMPUTATIONALLY on the stated odd bound",
        }
    return reports


def reverse_valuations(ks: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(reversed(ks))


def reverse_tail_valuations(ks: tuple[int, ...]) -> tuple[int, ...]:
    if len(ks) <= 1:
        return ks
    return (ks[0],) + tuple(reversed(ks[1:]))


def realizer_warp_row(valuations: tuple[int, ...] | str | list[int]) -> dict[str, object]:
    ks = parse_ks(valuations)
    dual = CollatzDualCode.from_valuations(ks)
    state = warp_state(dual.R)
    w_r = state.W_n
    rev = reverse_valuations(ks)
    tail = reverse_tail_valuations(ks)
    r_rev = canonical_realizer_formula(rev)
    r_tail = canonical_realizer_formula(tail)
    next_k = ks[0] if ks else None
    lift = dual.lift_digits[0] if dual.lift_digits else None
    row = state.experiment_row()
    row.update(
        {
            "itinerary": list(ks),
            "R": dual.R,
            "BT(R)": dual.balanced_ternary_R,
            "W(R)": w_r,
            "next_k": next_k,
            "lift_digit": lift,
            "reverse_itinerary": list(rev),
            "R_reverse_itinerary": r_rev,
            "W_R_equals_R_reverse": w_r == r_rev,
            "tail_itinerary": list(tail),
            "R_tail_itinerary": r_tail,
            "W_R_equals_R_tail": w_r == r_tail,
            "W_R_equals_R": w_r == dual.R,
            "K": dual.K,
            "v2_3R_plus_one": collatz_valuation(dual.R),
        }
    )
    return row


def realizer_warp_census(max_length: int, max_k: int) -> dict[str, object]:
    if (
        isinstance(max_length, bool)
        or not isinstance(max_length, int)
        or max_length < 1
    ):
        raise ValueError("max_length must be an integer >= 1")
    if isinstance(max_k, bool) or not isinstance(max_k, int) or max_k < 1:
        raise ValueError("max_k must be an integer >= 1")
    rows = []
    smallest_reverse_fail = None
    smallest_tail_fail = None
    reverse_hits = 0
    tail_hits = 0
    for length in range(1, max_length + 1):
        for ks in product(range(1, max_k + 1), repeat=length):
            row = realizer_warp_row(ks)
            rows.append(row)
            if row["W_R_equals_R_reverse"]:
                reverse_hits += 1
            elif smallest_reverse_fail is None:
                smallest_reverse_fail = row
            if row["W_R_equals_R_tail"]:
                tail_hits += 1
            elif smallest_tail_fail is None:
                smallest_tail_fail = row
    return {
        "max_length": max_length,
        "max_k": max_k,
        "row_count": len(rows),
        "reverse_itinerary_hits": reverse_hits,
        "tail_itinerary_hits": tail_hits,
        "smallest_reverse_counterexample": smallest_reverse_fail,
        "smallest_tail_counterexample": smallest_tail_fail,
        "rows": rows,
        "status": "VERIFIED COMPUTATIONALLY on the bounded exponent-code sample",
    }


def preserved_counterexamples() -> dict[str, dict[str, object]]:
    """Exact small witnesses for the naive identities that fail."""
    return {
        "W_W_equals_id": {
            "claim": "W(W(n)) = n for all n",
            "counterexample": 3,
            "W(3)": bt_reverse(3),
            "W(W(3))": bt_reverse(bt_reverse(3)),
            "criterion": "fails iff n != 0 and 3 divides n",
            "status": "REFUTED EXACTLY",
        },
        "W_3n_equals_3_W_n": {
            "claim": "W(3n) = 3 W(n)",
            "counterexample": 1,
            "W(3)": bt_reverse(3),
            "3_W(1)": 3 * bt_reverse(1),
            "status": "REFUTED EXACTLY",
        },
        "W_T_equals_T_W": {
            "claim": "W(T(n)) = T(W(n)) whenever both are defined",
            "counterexample": smallest_disagreement(("W", "T"), ("T", "W"), 10_000),
            "status": "search for smallest defined disagreement",
        },
    }
