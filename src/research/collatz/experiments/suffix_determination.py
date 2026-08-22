"""Bounded-suffix tests for lift digits and zero-lift successors.

Results are computational censuses except for the explicit full-``R``
counterexample `(1,)` versus `(1,4)`, which is exact.
"""

from __future__ import annotations

from itertools import product

from research.collatz.dual_code import CollatzDualCode, lift_digit_formula
from research.collatz.zero_lift import zero_lift_k


def _prefixes(max_length: int, k_max: int):
    yield ()
    for m in range(1, max_length + 1):
        yield from product(range(1, k_max + 1), repeat=m)


def suffix_determination_census(
    max_length: int,
    k_max: int,
    suffix_max: int,
    candidate_k_max: int | None = None,
) -> dict[str, object]:
    if max_length < 0 or k_max < 1 or suffix_max < 1:
        raise ValueError("invalid suffix census bounds")
    if candidate_k_max is None:
        candidate_k_max = k_max
    records = []
    for parent in _prefixes(max_length, k_max):
        parent = tuple(parent)
        dual = CollatzDualCode.from_valuations(parent)
        records.append(
            {
                "parent": parent,
                "R": dual.R,
                "BT(R)": dual.balanced_ternary_R,
                "zero_lift_value": zero_lift_k(parent),
                "candidate_lifts": tuple(
                    lift_digit_formula(parent, k)
                    for k in range(1, candidate_k_max + 1)
                ),
            }
        )
    rows = []
    for length in range(1, suffix_max + 1):
        next_buckets: dict[str, set[int]] = {}
        lift_buckets: dict[tuple[str, int], set[int]] = {}
        witnesses: dict[tuple[str, int], list[tuple[tuple[int, ...], int]]] = {}
        for record in records:
            suffix = str(record["BT(R)"])[-length:]
            next_buckets.setdefault(suffix, set()).add(int(record["zero_lift_value"]))
            for k, t in enumerate(record["candidate_lifts"], start=1):
                key = (suffix, k)
                lift_buckets.setdefault(key, set()).add(t)
                witnesses.setdefault(key, []).append((record["parent"], t))
        next_ambiguous = {
            suffix: sorted(values)
            for suffix, values in next_buckets.items()
            if len(values) > 1
        }
        lift_ambiguous = {
            f"{suffix}|k={k}": sorted(values)
            for (suffix, k), values in lift_buckets.items()
            if len(values) > 1
        }
        example = None
        for key, values in lift_buckets.items():
            if len(values) > 1:
                seen: dict[int, tuple[int, ...]] = {}
                for parent, t in witnesses[key]:
                    seen.setdefault(t, parent)
                first_two = list(seen.items())[:2]
                example = {
                    "suffix": key[0],
                    "candidate_k": key[1],
                    "a": {"parent": list(first_two[0][1]), "lift_digit": first_two[0][0]},
                    "b": {"parent": list(first_two[1][1]), "lift_digit": first_two[1][0]},
                }
                break
        rows.append(
            {
                "suffix_length": length,
                "next_value_determined": not next_ambiguous,
                "lift_digit_determined_given_k": not lift_ambiguous,
                "ambiguous_next_suffixes": len(next_ambiguous),
                "ambiguous_lift_states": len(lift_ambiguous),
                "sample_counterexample": example,
                "status": "VERIFIED COMPUTATIONALLY on stated finite bounds",
            }
        )
    exact_counterexample = {
        "prefix_a": [1],
        "prefix_b": [1, 4],
        "R": 3,
        "BT(R)": "+0",
        "zero_lift_a": 4,
        "zero_lift_b": 2,
        "candidate_k": 2,
        "lift_digit_a": 2,
        "lift_digit_b": 0,
        "status": "EXACT COUNTEREXAMPLE: full BT(R) is insufficient",
    }
    return {
        "max_length": max_length,
        "k_max": k_max,
        "candidate_k_max": candidate_k_max,
        "prefix_count": len(records),
        "rows": rows,
        "exact_full_R_counterexample": exact_counterexample,
        "status": "COMPUTATIONAL suffix census plus one exact counterexample",
    }
