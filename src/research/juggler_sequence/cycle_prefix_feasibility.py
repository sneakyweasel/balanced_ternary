"""Prefix-expansion feasibility on E_run leftovers.

Not a halt theorem, not a leftover-word census, and not a claim
that a symbolic path is an integer cycle. The question is whether
a finance-surviving (L, o_min) admits any O/E lattice path whose
every prefix stays expanding (3^{o_k} >= 2^k), together with the
already-proved first-run constraints a0 >= 2 and R(2) = 0.

Dossier: docs/problems/juggler_cycle_prefix_feasibility.md.
"""

from __future__ import annotations

import json
import math
from typing import Any

from research.juggler_sequence.cycle_finance import (
    DATA_DIR,
    PUBLISHED_FLOOR,
    o_min_and_theta,
    sha256_int_list,
)
from research.juggler_sequence.cycle_run_extremum import survivor_lengths

SPOTLIGHT = (25781, 55293)
LOG2 = math.log(2.0)
LOG3 = math.log(3.0)
PREFIX_CHARS = 32


def r_of(k: int) -> int:
    """Lower envelope r(k) = min{r : 3^r >= 2^k}."""

    if k < 0:
        raise ValueError("k must be nonnegative")
    if k == 0:
        return 0
    odd_count = 0
    pow3 = 1
    pow2 = 1 << k
    while pow3 < pow2:
        pow3 *= 3
        odd_count += 1
    return odd_count


def isolated_oe_allowed(a0: int, isolated_r: int) -> bool:
    """First-OO comparison 2^{a+2r+1} <= 3^{a+r}."""

    if isolated_r < 0:
        return False
    if a0 < 1:
        return isolated_r == 0
    return (1 << (a0 + 2 * isolated_r + 1)) <= 3 ** (a0 + isolated_r)


def isolated_oe_r_max(a0: int) -> int:
    """Largest r with 2^{a+2r+1} <= 3^{a+r}. R(2)=0, R(3)=1, R(4)=3."""

    isolated_r = 0
    while isolated_oe_allowed(a0, isolated_r + 1):
        isolated_r += 1
    return isolated_r


def extremal_word(length: int) -> str:
    """Unique path o_k = r(k) from (0, 0) to (L, r(L))."""

    if length < 1:
        raise ValueError("length must be positive")
    letters: list[str] = []
    pow2 = 1
    pow3 = 1
    for _ in range(length):
        pow2 *= 2
        if pow3 < pow2:
            pow3 *= 3
            letters.append("O")
        else:
            letters.append("E")
    return "".join(letters)


def ceiling_christoffel_word(length: int, odd: int) -> str:
    """Ceiling Christoffel of slope odd/length, integer ceil.

    Same sequence as cycle_christoffel.christoffel_bits when the
    float formula is exact, which it is for every E_run leftover.
    """

    if length < 1:
        raise ValueError("length must be positive")
    if odd < 0 or odd > length:
        raise ValueError("odd count must lie in [0, length]")

    def ceil_mul(index: int) -> int:
        if index <= 0:
            return 0
        return (index * odd + length - 1) // length

    return "".join(
        "O" if ceil_mul(index) - ceil_mul(index - 1) else "E"
        for index in range(1, length + 1)
    )


def prefix_report(word: str) -> dict[str, Any]:
    """Exact integer walk: every prefix satisfies 3^{o_k} >= 2^k."""

    pow2 = 1
    pow3 = 1
    odd_count = 0
    min_surplus = float("inf")
    min_k = 0
    all_ok = True
    for step, letter in enumerate(word, start=1):
        pow2 *= 2
        if letter == "O":
            pow3 *= 3
            odd_count += 1
        elif letter != "E":
            raise ValueError(f"letter must be O or E, got {letter!r}")
        if pow3 < pow2:
            all_ok = False
            break
        surplus = odd_count * LOG3 - step * LOG2
        if surplus < min_surplus:
            min_surplus = surplus
            min_k = step
    return {
        "all_prefixes_ok": all_ok,
        "o": odd_count,
        "min_log_surplus": min_surplus if all_ok else None,
        "min_surplus_k": min_k if all_ok else None,
    }


def prefix_admissible(word: str) -> bool:
    return bool(prefix_report(word)["all_prefixes_ok"])


def first_odd_run(word: str) -> int:
    run = 0
    for letter in word:
        if letter != "O":
            break
        run += 1
    return run


def first_isolated_oe_count(word: str) -> int:
    """r in the opening block O^{a0} E (OE)^r."""

    a0 = first_odd_run(word)
    if a0 >= len(word) or word[a0] != "E":
        return 0
    isolated_r = 0
    index = a0 + 1
    while index + 1 < len(word) and word[index] == "O" and word[index + 1] == "E":
        isolated_r += 1
        index += 2
    return isolated_r


def starts_oo(word: str) -> bool:
    return len(word) >= 2 and word[:2] == "OO"


def first_oo_ok(word: str) -> bool:
    """a0 >= 2 and the first isolated-OE block obeys r <= R(a0)."""

    if not starts_oo(word):
        return False
    a0 = first_odd_run(word)
    return isolated_oe_allowed(a0, first_isolated_oe_count(word))


def feasibility_row(length: int) -> dict[str, Any]:
    odd_count, theta = o_min_and_theta(length)
    word = extremal_word(length)
    report = prefix_report(word)
    a0 = first_odd_run(word)
    isolated_r = first_isolated_oe_count(word)
    christoffel = ceiling_christoffel_word(length, odd_count)
    christoffel_report = prefix_report(christoffel)
    ends_at_o_min = report["o"] == odd_count
    admissible = bool(report["all_prefixes_ok"] and ends_at_o_min)
    first_ok = first_oo_ok(word)
    christoffel_ok = bool(
        christoffel_report["all_prefixes_ok"]
        and christoffel_report["o"] == odd_count
        and first_oo_ok(christoffel)
    )
    return {
        "L": length,
        "o": odd_count,
        "e": length - odd_count,
        "theta": theta,
        "r_L": r_of(length),
        "ends_at_o_min": ends_at_o_min,
        "all_prefixes_ok": report["all_prefixes_ok"],
        "starts_oo": starts_oo(word),
        "a0": a0,
        "first_isolated_oe_r": isolated_r,
        "first_oo_ok": first_ok,
        "prefix": word[:PREFIX_CHARS],
        "min_log_surplus": report["min_log_surplus"],
        "min_surplus_k": report["min_surplus_k"],
        "christoffel_admissible": christoffel_ok,
        "christoffel_prefix": christoffel[:PREFIX_CHARS],
        "A_nonempty": admissible and first_ok,
    }


def feasibility_scan(*, floor: int = PUBLISHED_FLOOR) -> dict[str, Any]:
    rows = [feasibility_row(length) for length in survivor_lengths(floor=floor)]
    empty = [row["L"] for row in rows if not row["A_nonempty"]]
    christoffel_fail = [
        row["L"] for row in rows if not row["christoffel_admissible"]
    ]
    not_o_min = [row["L"] for row in rows if not row["ends_at_o_min"]]
    first_oo_fail = [row["L"] for row in rows if not row["first_oo_ok"]]
    spotlights = {
        str(length): next(row for row in rows if row["L"] == length)
        for length in SPOTLIGHT
        if any(row["L"] == length for row in rows)
    }
    return {
        "bound": "prefix_feasibility",
        "floor": floor,
        "survivor_count": len(rows),
        "sha256_survivors": sha256_int_list([row["L"] for row in rows]),
        "R2": isolated_oe_r_max(2),
        "R3": isolated_oe_r_max(3),
        "R4": isolated_oe_r_max(4),
        "small_r": [r_of(k) for k in range(0, 6)],
        "small_extremal": extremal_word(6),
        "A_empty": empty,
        "A_nonempty_count": len(rows) - len(empty),
        "ends_at_o_min_failures": not_o_min,
        "first_oo_failures": first_oo_fail,
        "christoffel_failures": christoffel_fail,
        "all_A_nonempty": not empty,
        "all_christoffel_admissible": not christoffel_fail,
        "spotlights": spotlights,
        "rows": rows,
        "halt_theorem": False,
        "no_cycle_all_lengths": False,
    }


def write_prefix_feasibility_artifacts(
    payload: dict[str, Any] | None = None,
    *,
    floor: int = PUBLISHED_FLOOR,
) -> dict[str, Any]:
    data = payload if payload is not None else feasibility_scan(floor=floor)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    path = DATA_DIR / "prefix_feasibility.json"
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return data


if __name__ == "__main__":
    report = write_prefix_feasibility_artifacts()
    print(
        json.dumps(
            {
                "survivors": report["survivor_count"],
                "all_A_nonempty": report["all_A_nonempty"],
                "A_empty": report["A_empty"],
                "christoffel_failures": report["christoffel_failures"],
                "first_oo_failures": report["first_oo_failures"],
                "R2": report["R2"],
                "spotlight_25781": report["spotlights"]["25781"]["prefix"],
                "spotlight_55293": report["spotlights"]["55293"]["prefix"],
            },
            indent=2,
        )
    )
