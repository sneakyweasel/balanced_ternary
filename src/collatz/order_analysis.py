"""Order-sensitive affine constants and permutation comparisons.

The homogeneous budget depends only on ``(m, K)``. The affine constant
``C`` depends on the order of the ``k_i``.

**PROVED adjacent-swap formula.** Write ``ks = (..., a, b, ...)`` with
``a`` in position ``t`` (0-based) and ``b`` in position ``t+1``. Let
``K_t = k_0+...+k_{t-1}``. After swapping ``a`` and ``b``,

    C_new - C_old = 3^{m-t-2} * 2^{K_t} * (2^b - 2^a).

Hence putting a larger valuation earlier strictly increases ``C``. For a
fixed multiset, the descending order maximises ``C`` and the ascending
order minimises it.

The same ordering need **not** extremize ``R``. That comparison is
computational and labelled as such.
"""

from __future__ import annotations

from itertools import permutations

from collatz.cylinders import parse_ks
from collatz.itinerary import affine_constant, partial_sums_K
from collatz.min_realizer import itinerary_signature, min_realizer


def adjacent_swap_delta_C(ks: tuple[int, ...], t: int) -> int:
    """Exact ``C_swapped - C_original`` for swapping indices ``t`` and ``t+1``."""
    ks = parse_ks(ks)
    if isinstance(t, bool) or not isinstance(t, int):
        raise TypeError("t must be int")
    if t < 0 or t + 1 >= len(ks):
        raise ValueError(f"swap index t={t} out of range for length {len(ks)}")
    a = ks[t]
    b = ks[t + 1]
    k_t = partial_sums_K(ks)[t]
    m = len(ks)
    return pow(3, m - t - 2) * (1 << k_t) * ((1 << b) - (1 << a))


def swap_adjacent(ks: tuple[int, ...], t: int) -> tuple[int, ...]:
    ks = parse_ks(ks)
    lst = list(ks)
    lst[t], lst[t + 1] = lst[t + 1], lst[t]
    return tuple(lst)


def verify_swap_formula(ks: tuple[int, ...], t: int) -> bool:
    ks = parse_ks(ks)
    nxt = swap_adjacent(ks, t)
    return affine_constant(nxt) - affine_constant(ks) == adjacent_swap_delta_C(ks, t)


def descending_ks(ks: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(sorted(parse_ks(ks), reverse=True))


def ascending_ks(ks: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(sorted(parse_ks(ks)))


def unique_permutations(ks: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    ks = parse_ks(ks)
    return tuple(sorted(set(permutations(ks))))


def permutation_table(ks: tuple[int, ...] | str | list[int]) -> tuple[dict[str, object], ...]:
    """Exact C, R, residue for every distinct permutation. Status: EXACT."""
    ks = parse_ks(ks)
    rows: list[dict[str, object]] = []
    for word in unique_permutations(ks):
        sig = itinerary_signature(word)
        rows.append(
            {
                "ks": list(word),
                "C": sig.C,
                "R": sig.R,
                "residue": sig.residue,
                "BT(R)": sig.bt_word,
                "budget_kind": sig.budget_kind,
                "status": "EXACT",
            }
        )
    return tuple(rows)


def extremal_orders(ks: tuple[int, ...] | str | list[int]) -> dict[str, object]:
    """Compare ascending / descending / observed min-max of C and R."""
    ks = parse_ks(ks)
    rows = permutation_table(ks)
    if not rows:
        empty = itinerary_signature(())
        return {"ks": [], "rows": [], "status": "EXACT", "C": empty.C, "R": empty.R}
    by_c = sorted(rows, key=lambda r: (r["C"], r["ks"]))
    by_r = sorted(rows, key=lambda r: (r["R"], r["ks"]))
    asc = list(ascending_ks(ks))
    desc = list(descending_ks(ks))
    c_asc = affine_constant(tuple(asc))
    c_desc = affine_constant(tuple(desc))
    r_asc = min_realizer(tuple(asc))
    r_desc = min_realizer(tuple(desc))
    same_order_extremizes_r = (
        by_r[0]["ks"] == asc and by_r[-1]["ks"] == desc
    ) or (by_r[0]["ks"] == desc and by_r[-1]["ks"] == asc)
    return {
        "multiset": list(ks),
        "C_min": by_c[0],
        "C_max": by_c[-1],
        "R_min": by_r[0],
        "R_max": by_r[-1],
        "ascending": {"ks": asc, "C": c_asc, "R": r_asc},
        "descending": {"ks": desc, "C": c_desc, "R": r_desc},
        "C_extremal_are_sorted": by_c[0]["ks"] == asc and by_c[-1]["ks"] == desc,
        "R_extremal_are_sorted": same_order_extremizes_r,
        "status": "EXACT for C theorem; COMPUTATIONAL for R on this multiset",
        "permutation_count": len(rows),
    }


def order_changes_R_for_same_K(ks: tuple[int, ...]) -> bool:
    """True if some permutation of ``ks`` has a different ``R``."""
    values = {row["R"] for row in permutation_table(ks)}
    return len(values) > 1
