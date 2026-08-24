"""Exact Phase-0 objects for Erdős distinct subset sums.

Three predicates are kept distinct:

* subset sums distinct  iff  R(A) = {0^n}  iff  C_A(0) = 1
* all signed sums distinct  iff  C_A(x) <= 1 for every x
* modular signed relation  is labelled MODULAR ONLY until |s| < 3^k
  forces s = 0

Canonical encode(s) is a complete invariant of the integer s. Digit
length, leading trit, and v_3 are functions of s, not extra constraints
on A. No CLI, visualization, or generic additive-combinatorics package.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from itertools import product
from math import comb
from typing import Iterable, Sequence

from bt.metrics import v3
from bt.normalization import add_with_trace
from bt.representation import encode

TRITS = (-1, 0, 1)
FAST_N = 7
MAX_N = 12
CARRY_N = 7

# Conway–Guy a_n for n <= 12. OEIS A005318; a_0 = 0.
CONWAY_GUY_A: tuple[int, ...] = (
    0,
    1,
    2,
    4,
    7,
    13,
    24,
    44,
    84,
    161,
    309,
    594,
    1164,
)

# Lunnon: f(n) equals Conway–Guy max for n <= 8. Grossman: n = 9.
A276661_PREFIX: tuple[int, ...] = (0, 1, 2, 4, 7, 13, 24, 44, 84, 161)


def _as_tuple(A: Sequence[int] | Iterable[int]) -> tuple[int, ...]:
    values = tuple(A)
    if any(isinstance(a, bool) or not isinstance(a, int) for a in values):
        raise TypeError("A must be a sequence of ints")
    return values


def _require_n(n: int, name: str = "n") -> int:
    if isinstance(n, bool) or not isinstance(n, int) or n < 1:
        raise ValueError(f"{name} must be a positive int")
    return n


def _require_k(k: int) -> int:
    if isinstance(k, bool) or not isinstance(k, int) or k < 1:
        raise ValueError("k must be a positive int")
    return k


def signed_sum(A: Sequence[int], eps: Sequence[int]) -> int:
    """Integer value of sum ε_i a_i."""

    if len(eps) != len(A):
        raise ValueError("eps and A must have the same length")
    total = 0
    for coeff, value in zip(eps, A):
        if coeff not in TRITS:
            raise ValueError(f"coefficient {coeff!r} is not a balanced trit")
        total += coeff * value
    return total


def signed_sum_histogram(A: Sequence[int]) -> Counter[int]:
    """C_A: multiplicity of each signed sum. Built by DP, not subset sums."""

    values = _as_tuple(A)
    counts: Counter[int] = Counter({0: 1})
    for a in values:
        nxt: Counter[int] = Counter()
        for partial, multiplicity in counts.items():
            for trit in TRITS:
                nxt[partial + trit * a] += multiplicity
        counts = nxt
    return counts


def concentration_at_zero(A: Sequence[int]) -> int:
    """C_A(0)."""

    return signed_sum_histogram(A)[0]


def is_sum_distinct(A: Sequence[int]) -> bool:
    """Subset sums distinct iff no nontrivial balanced-sign relation."""

    return concentration_at_zero(A) == 1


def all_signed_sums_distinct(A: Sequence[int]) -> bool:
    """Strictly stronger than sum-distinctness: C_A(x) <= 1 for every x."""

    hist = signed_sum_histogram(A)
    return all(count == 1 for count in hist.values())


def signed_relations(A: Sequence[int]) -> tuple[tuple[int, ...], ...]:
    """The kernel R(A), including the zero vector."""

    values = _as_tuple(A)
    n = len(values)
    kernel = []
    for eps in product(TRITS, repeat=n):
        if signed_sum(values, eps) == 0:
            kernel.append(eps)
    return tuple(kernel)


def relation_witness(A: Sequence[int]) -> tuple[int, ...] | None:
    """One nontrivial exact relation, or None if A is sum-distinct."""

    for eps in signed_relations(A):
        if any(coeff != 0 for coeff in eps):
            return eps
    return None


def powers_of_two(n: int) -> tuple[int, ...]:
    n = _require_n(n)
    return tuple(2**i for i in range(n))


def powers_of_three(n: int) -> tuple[int, ...]:
    n = _require_n(n)
    return tuple(3**i for i in range(n))


def nearest_int(x: float) -> int:
    """Nearest integer; halves round away from zero (matches A005318)."""

    if x >= 0:
        return int(x + 0.5)
    return int(x - 0.5)


def conway_guy_a(n: int) -> int:
    """Conway–Guy sequence a_n, n >= 0. Recurrence against A005318."""

    if isinstance(n, bool) or not isinstance(n, int) or n < 0:
        raise ValueError("n must be a nonnegative int")
    seq = [0, 1]
    if n <= 1:
        return seq[n]
    for m in range(1, n):
        radius = nearest_int((2 * m) ** 0.5)
        seq.append(2 * seq[m] - seq[m - radius])
    return seq[n]


def conway_guy_set(n: int) -> tuple[int, ...]:
    """The n-element Conway–Guy set {a_n - a_{n-1}, ..., a_n - a_0}."""

    n = _require_n(n)
    top = conway_guy_a(n)
    return tuple(sorted(top - conway_guy_a(i) for i in range(n)))


def a276661_extremal(n: int) -> tuple[int, ...]:
    """Published small extremal: Conway–Guy, optimal for n <= 8 (Lunnon)."""

    n = _require_n(n)
    if n > 9:
        raise ValueError("A276661 exact extremals are recorded only through n=9")
    return conway_guy_set(n)


def word_stats(s: int) -> dict[str, int | str | None]:
    """Canonical BT data of an integer. A complete invariant of s."""

    word = encode(s)
    return {
        "value": s,
        "word": word.word(),
        "length": len(word),
        "leading_trit": 0 if s == 0 else word.digits_msd[0],
        "v3": v3(s),
    }


def bt_length(s: int) -> int:
    return len(encode(s))


def magnitude_length_bound(s: int) -> int:
    """Smallest L with |s| <= (3^L - 1)/2. Equals the canonical length."""

    if s == 0:
        return 1
    magnitude = abs(s)
    length = 1
    while (3**length - 1) // 2 < magnitude:
        length += 1
    return length


@dataclass(frozen=True)
class RelationNode:
    """One merged state of the signed-relation tree at a fixed depth."""

    depth: int
    partial_sum: int
    word: str
    length: int
    leading_trit: int
    v3: int | None


def balanced_relation_tree(A: Sequence[int]) -> dict[str, object]:
    """Trie over {-1,0,+1} with nodes merged by partial integer sum.

    R_j(A) is the number of distinct partial sums after j coefficients.
    For a sum-distinct set this need not equal 3^n at the final depth.
    """

    values = _as_tuple(A)
    states = {0}
    r_counts = [1]
    nodes: list[RelationNode] = [RelationNode(0, 0, "0", 1, 0, None)]
    for depth, a in enumerate(values, start=1):
        nxt: set[int] = set()
        for partial in states:
            for trit in TRITS:
                nxt.add(partial + trit * a)
        states = nxt
        r_counts.append(len(states))
        if depth == len(values):
            for partial in sorted(states):
                stats = word_stats(partial)
                nodes.append(
                    RelationNode(
                        depth=depth,
                        partial_sum=partial,
                        word=str(stats["word"]),
                        length=int(stats["length"]),
                        leading_trit=int(stats["leading_trit"]),
                        v3=stats["v3"] if isinstance(stats["v3"], int) else None,
                    )
                )
    return {
        "n": len(values),
        "R_j": tuple(r_counts),
        "final_distinct_sums": r_counts[-1],
        "signed_space": 3 ** len(values),
        "all_signed_sums_distinct": r_counts[-1] == 3 ** len(values),
        "final_nodes": tuple(nodes[1:]) if values else (nodes[0],),
    }


def valuation_histogram(A: Sequence[int]) -> dict[str, int]:
    """v_3 of nonzero signed sums. Zero is recorded separately as exact_zero."""

    hist = signed_sum_histogram(A)
    out: Counter[str] = Counter()
    out["exact_zero"] = hist[0]
    for value, multiplicity in hist.items():
        if value == 0:
            continue
        val = v3(value)
        key = str(val if val is not None else "none")
        out[key] += multiplicity
    return dict(out)


def mod_3k_relation_profile(A: Sequence[int], k: int) -> dict[str, object]:
    """φ_k : {-1,0,+1}^n → Z/3^k Z. Every nonzero hit is MODULAR ONLY."""

    values = _as_tuple(A)
    k = _require_k(k)
    modulus = 3**k
    residue_counts: Counter[int] = Counter()
    modular_kernel = 0
    exact_zero = 0
    for eps in product(TRITS, repeat=len(values)):
        s = signed_sum(values, eps)
        residue = s % modulus
        residue_counts[residue] += 1
        if residue == 0:
            if s == 0:
                exact_zero += 1
            else:
                modular_kernel += 1
    occupied = len(residue_counts)
    max_mult = max(residue_counts.values()) if residue_counts else 0
    return {
        "k": k,
        "modulus": modulus,
        "codomain": modulus,
        "occupied_residues": occupied,
        "max_multiplicity": max_mult,
        "exact_zero": exact_zero,
        "modular_only_kernel": modular_kernel,
        "label": "MODULAR ONLY",
        "injective": occupied == 3 ** len(values),
    }


def magnitude_valuation_bridge(
    A: Sequence[int], k: int
) -> dict[str, object]:
    """Vectors with v_3(s) >= k and |s| < 3^k.

    The only integer satisfying both is s = 0, so the hit list is R(A).
    """

    values = _as_tuple(A)
    k = _require_k(k)
    bound = 3**k
    hits: list[tuple[int, ...]] = []
    for eps in product(TRITS, repeat=len(values)):
        s = signed_sum(values, eps)
        if abs(s) >= bound:
            continue
        if s == 0:
            hits.append(eps)
            continue
        val = v3(s)
        if val is not None and val >= k:
            hits.append(eps)
    return {
        "k": k,
        "bound": bound,
        "hits": tuple(hits),
        "hit_count": len(hits),
        "equals_kernel": tuple(hits) == signed_relations(values),
        "nonzero_forced_zero": all(signed_sum(values, eps) == 0 for eps in hits),
    }


def carry_profile(A: Sequence[int]) -> dict[str, object]:
    """Carry counts along coefficient paths. Path data, still integer addition."""

    values = _as_tuple(A)
    n = len(values)
    if n > CARRY_N:
        return {"computed": False, "n": n, "reason": "carry census only for n<=7"}
    nonzero_carries = 0
    steps = 0
    max_carries = 0
    for eps in product(TRITS, repeat=n):
        partial = 0
        path_carries = 0
        for coeff, a in zip(eps, values):
            term = coeff * a
            if term == 0:
                continue
            trace = add_with_trace(encode(partial), encode(term))
            step_carries = sum(1 for step in trace.steps if step.carry_out != 0)
            path_carries += step_carries
            nonzero_carries += step_carries
            steps += 1
            partial += term
        if path_carries > max_carries:
            max_carries = path_carries
    return {
        "computed": True,
        "n": n,
        "paths": 3**n,
        "addition_steps": steps,
        "nonzero_carry_steps": nonzero_carries,
        "max_path_carries": max_carries,
    }


def trit_statistics(A: Sequence[int]) -> dict[str, object]:
    """Length / leading-trit census of all signed sums."""

    hist = signed_sum_histogram(A)
    lengths: Counter[int] = Counter()
    leading: Counter[int] = Counter()
    for value, multiplicity in hist.items():
        stats = word_stats(value)
        lengths[int(stats["length"])] += multiplicity
        leading[int(stats["leading_trit"])] += multiplicity
    length_vs_magnitude = all(
        bt_length(value) == magnitude_length_bound(value) for value in hist
    )
    return {
        "lengths": dict(sorted(lengths.items())),
        "leading_trits": dict(sorted(leading.items())),
        "length_equals_magnitude_bound": length_vs_magnitude,
        "distinct_sums": len(hist),
        "signed_space": 3 ** len(_as_tuple(A)),
    }


def _signed_enumeration(A: Sequence[int], k: int) -> dict[str, object]:
    """One pass for the kernel, φ_k profile, and magnitude+valuation hits."""

    values = _as_tuple(A)
    k = _require_k(k)
    modulus = 3**k
    kernel: list[tuple[int, ...]] = []
    residue_counts: Counter[int] = Counter()
    modular_only = 0
    bridge_hits: list[tuple[int, ...]] = []
    for eps in product(TRITS, repeat=len(values)):
        s = signed_sum(values, eps)
        residue = s % modulus
        residue_counts[residue] += 1
        if s == 0:
            kernel.append(eps)
            bridge_hits.append(eps)
        elif residue == 0:
            modular_only += 1
        if s != 0 and abs(s) < modulus:
            val = v3(s)
            if val is not None and val >= k:
                bridge_hits.append(eps)
    occupied = len(residue_counts)
    return {
        "kernel": tuple(kernel),
        "witness": next((eps for eps in kernel if any(eps)), None),
        "mod_3k": {
            "k": k,
            "modulus": modulus,
            "codomain": modulus,
            "occupied_residues": occupied,
            "max_multiplicity": max(residue_counts.values()) if residue_counts else 0,
            "exact_zero": len(kernel),
            "modular_only_kernel": modular_only,
            "label": "MODULAR ONLY",
            "injective": occupied == 3 ** len(values),
        },
        "bridge": {
            "k": k,
            "bound": modulus,
            "hits": tuple(bridge_hits),
            "hit_count": len(bridge_hits),
            "equals_kernel": tuple(bridge_hits) == tuple(kernel),
            "nonzero_forced_zero": all(signed_sum(values, eps) == 0 for eps in bridge_hits),
        },
    }


def construction_row(name: str, A: Sequence[int], *, k: int = 2) -> dict[str, object]:
    """One construction in the Phase-0 table."""

    values = _as_tuple(A)
    n = len(values)
    hist = signed_sum_histogram(values)
    tree = balanced_relation_tree(values)
    enumerated = _signed_enumeration(values, k)
    return {
        "name": name,
        "n": n,
        "A": values,
        "max": max(values) if values else 0,
        "sum_distinct": hist[0] == 1,
        "all_signed_sums_distinct": all(c == 1 for c in hist.values()),
        "C_A_0": hist[0],
        "nonzero_relations": hist[0] - 1,
        "relation_witness": enumerated["witness"],
        "R_j": tree["R_j"],
        "valuation": valuation_histogram(values),
        "mod_3k": enumerated["mod_3k"],
        "trit": trit_statistics(values),
        "bridge": enumerated["bridge"],
        "dfx_binomial": comb(n, n // 2) if n else 0,
    }


def _high_valuation_without_relation(A: Sequence[int], k: int) -> bool:
    """Sum-distinct set with a nonzero signed sum divisible by 3^k."""

    if not is_sum_distinct(A):
        return False
    hist = signed_sum_histogram(A)
    bound_val = k
    for value, multiplicity in hist.items():
        if value == 0:
            continue
        val = v3(value)
        if val is not None and val >= bound_val and multiplicity:
            return True
    return False


def invariant_audit(max_n: int = FAST_N) -> dict[str, object]:
    """Break the four Phase-0 invariant candidates."""

    max_n = _require_n(max_n, "max_n")
    if max_n > MAX_N:
        raise ValueError(f"max_n must be <= {MAX_N}")

    p2 = powers_of_two(max_n)
    cg = conway_guy_set(max_n)
    p3 = powers_of_three(max_n)
    colliding = (1, 2, 3)

    # 1. High v_3 density is not an exact-relation forcing law.
    high_v3_sum_distinct = _high_valuation_without_relation(p2, 1) and (
        _high_valuation_without_relation(cg, 1)
    )
    bridge_p2 = magnitude_valuation_bridge(p2, 2)
    bridge_rel = magnitude_valuation_bridge(colliding, 2)

    # 2. Leading-trit / length patterns occur on both extremal families.
    trit_p2 = trit_statistics(p2)
    trit_cg = trit_statistics(cg)
    shared_leadings = set(trit_p2["leading_trits"]) & set(trit_cg["leading_trits"])
    shared_lengths = set(trit_p2["lengths"]) & set(trit_cg["lengths"])

    # 3. Digit length is the magnitude bound.
    length_is_magnitude = trit_p2["length_equals_magnitude_bound"] and trit_cg[
        "length_equals_magnitude_bound"
    ]

    # Construction negative: powers of 3 lose to powers of 2.
    p3_worse = max(p3) > max(p2)

    # All signed sums distinct is strictly stronger.
    binary = powers_of_two(3)
    stronger_gap = is_sum_distinct(binary) and not all_signed_sums_distinct(binary)

    return {
        "high_v3_without_relation": high_v3_sum_distinct,
        "bridge_equals_kernel_on_powers2": bridge_p2["equals_kernel"],
        "bridge_equals_kernel_on_123": bridge_rel["equals_kernel"],
        "shared_leading_trits": sorted(shared_leadings),
        "shared_lengths": sorted(shared_lengths),
        "length_is_magnitude_bound": length_is_magnitude,
        "powers3_worse_than_powers2": p3_worse,
        "all_signed_sums_strictly_stronger": stronger_gap,
        "powers3_all_signed_sums_distinct": all_signed_sums_distinct(p3),
        "cannot_reproduce_dfx": True,
        "dfx_reason": (
            "The DFX gap is Harper isoperimetry / Berry–Esseen on the cube. "
            "encode(s) and v_3(s) are functions of the integer signed sum and "
            "do not produce the middle-binomial or Gaussian comparison."
        ),
    }


def triage_report(max_n: int = FAST_N, *, k: int = 2) -> dict[str, object]:
    """Bounded Phase-0 census on known constructions."""

    max_n = _require_n(max_n, "max_n")
    if max_n > MAX_N:
        raise ValueError(f"max_n must be <= {MAX_N}")
    rows = []
    for n in range(1, max_n + 1):
        rows.append(construction_row(f"powers2_n{n}", powers_of_two(n), k=k))
        rows.append(construction_row(f"conway_guy_n{n}", conway_guy_set(n), k=k))
        rows.append(construction_row(f"powers3_n{n}", powers_of_three(n), k=k))
    rows.append(construction_row("relation_123", (1, 2, 3), k=k))
    rows.append(construction_row("binary_124", (1, 2, 4), k=k))
    a276661_same = all(a276661_extremal(n) == conway_guy_set(n) for n in range(1, min(max_n, 9) + 1))
    return {
        "max_n": max_n,
        "k": k,
        "rows": rows,
        "a276661_equals_conway_guy": a276661_same,
        "audit": invariant_audit(max_n),
        "conway_guy_a": tuple(conway_guy_a(i) for i in range(max_n + 1)),
        "carry_sample": {
            "powers2": carry_profile(powers_of_two(min(max_n, CARRY_N))),
            "conway_guy": carry_profile(conway_guy_set(min(max_n, CARRY_N))),
            "relation_123": carry_profile((1, 2, 3)),
        },
    }
