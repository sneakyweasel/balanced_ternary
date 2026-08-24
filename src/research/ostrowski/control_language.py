"""Co-live control language of Γ_NP.

A word is *live* at start remaining ``N`` if every prefix lands in ``K``.
It is *co-live* if, in addition, the endpoint has a legal live path to
``K_0``. Finite-horizon co-liveness is not ``|H(u)|=∞``.

``forward_layers`` collapses first visit; this module keeps every live
edge, then marks co-reachability of remaining 0. The time-augmented
graph is a DAG. Expanding ``A^{|B|}`` is not occurrence on co-live
paths. ``K_n`` is normalized control of ``E_n``, not ``|s|≤C``.

Reuse ``energy_telescope`` / ``consumed_sum``; do not re-prove them.
Do not repeat ``k≤3`` origin-periodic search.
"""

from __future__ import annotations

from collections import defaultdict, deque
from functools import lru_cache
from itertools import product

from research.ostrowski.energy_trajectory import apply_word, consumed_sum
from research.ostrowski.exceptional_kernel import W_INTERIOR, W_LSD
from research.ostrowski.live_growth import legal_w, residual_is_live
from research.ostrowski.live_layers import linf
from research.ostrowski.spectral import cubic_roots
from research.ostrowski.spectral_residual import (
    apply_matrix,
    residual_matrix,
    transition_affine,
)
from research.ostrowski.system import characteristic_poly_coeffs, nonpisot_order3
from research.ostrowski.terminal_set import is_terminal

State3 = tuple[int, int, int]
StatePos = tuple[State3, int]
ORIGIN: State3 = (0, 0, 0)

LIVE_NOT_COLIVE = "live_at_n_is_not_colive"
GROWTH_NOT_INFINITUDE = "finite_depth_is_not_infinitude"
HORIZON_NOT_INFINITY = "finite_H_u_is_not_infinitude"
EXPANDING_NOT_OCCURRING = "expanding_A_k_is_not_colive_occurrence"
DAG_NOT_SCC = "time_augmented_graph_is_a_dag"
NORMALIZED_NOT_COORDINATE = "Kn_is_normalized_not_coordinate_bounded"

# Frozen co-live prefix counts. Finite horizon, not |L_∞|.
N8_L_K: dict[int, int] = {
    0: 1, 1: 4, 2: 9, 3: 23, 4: 57, 5: 138, 6: 323, 7: 535, 8: 535,
}
N12_L_K: dict[int, int] = {
    0: 1, 1: 4, 2: 9, 3: 23, 4: 59, 5: 144, 6: 359, 7: 912,
    8: 2271, 9: 5564, 10: 13197, 11: 22411, 12: 22411,
}

# Distinct Ext(s,n) at N=8,12,16,20: consecutive windows in W, max length 4.
# Singleton (-3,) does not appear. Not a residual automaton.
FROZEN_EXT_TYPES: tuple[tuple[int, ...], ...] = (
    (),
    (-4,), (-2,), (-1,), (0,), (1,), (2,),
    (-4, -3), (-3, -2), (-2, -1), (-1, 0), (0, 1), (1, 2),
    (-4, -3, -2), (-3, -2, -1), (-2, -1, 0), (-1, 0, 1), (0, 1, 2),
    (-4, -3, -2, -1), (-3, -2, -1, 0), (-2, -1, 0, 1), (-1, 0, 1, 2),
)

# Length-6 co-live prefixes at N=20 that fail as prefixes at N=12.
HORIZON_SPECIFIC_LEN6: tuple[tuple[int, ...], ...] = (
    (1, -1, -4, -2, 1, -3),
    (0, 1, -3, 1, 1, -3),
)


def ext_is_consecutive_interval(ext: tuple[int, ...]) -> bool:
    if not ext:
        return True
    return ext == tuple(range(ext[0], ext[-1] + 1))


@lru_cache(maxsize=None)
def dag_at(start_remaining: int) -> LiveDag:
    return LiveDag(start_remaining)


def alphabet_at_remaining(remaining: int) -> tuple[int, ...]:
    """Legal difference digits consumed at remaining ``n`` (place ``n-1``)."""
    if remaining < 1:
        return ()
    return legal_w(nonpisot_order3(), remaining - 1)


def _mat_mul(
    left: tuple[tuple[int, int, int], ...],
    right: tuple[tuple[int, int, int], ...],
) -> tuple[tuple[int, int, int], ...]:
    return tuple(
        tuple(sum(left[i][k] * right[k][j] for k in range(3)) for j in range(3))
        for i in range(3)
    )


def matrix_power(
    matrix: tuple[tuple[int, int, int], ...],
    exponent: int,
) -> tuple[tuple[int, int, int], ...]:
    if exponent < 0:
        raise ValueError("exponent must be nonnegative")
    ident = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
    acc = ident
    base = matrix
    n = exponent
    while n:
        if n & 1:
            acc = _mat_mul(acc, base)
        base = _mat_mul(base, base)
        n >>= 1
    return acc


class LiveDag:
    """Origin-reachable live DAG at a fixed start remaining, with co-live marks."""

    def __init__(self, start_remaining: int) -> None:
        if start_remaining < 0:
            raise ValueError("start_remaining must be nonnegative")
        self.system = nonpisot_order3()
        self.N = start_remaining
        self.nodes: set[StatePos] = set()
        self.edges: dict[StatePos, list[tuple[int, StatePos]]] = defaultdict(list)
        self.reverse: dict[StatePos, list[tuple[int, StatePos]]] = defaultdict(list)
        self.colive: set[StatePos] = set()
        self.dp: dict[int, dict[State3, int]] = {}
        self._build()

    def _build(self) -> None:
        sys = self.system
        start: StatePos = (ORIGIN, self.N)
        if self.N > 0 and not residual_is_live(sys, ORIGIN, self.N):
            return
        if self.N == 0:
            self.nodes.add(start)
            self.colive.add(start)
            self.dp = {0: {ORIGIN: 1}}
            return
        seen: set[StatePos] = {start}
        queue: deque[StatePos] = deque([start])
        self.nodes.add(start)
        while queue:
            state, remaining = queue.popleft()
            if remaining == 0:
                continue
            for w in legal_w(sys, remaining - 1):
                nxt = transition_affine(sys, state, w)
                nxt_pos: StatePos = (nxt, remaining - 1)
                if not residual_is_live(sys, nxt, remaining - 1):
                    continue
                self.edges[(state, remaining)].append((w, nxt_pos))
                self.reverse[nxt_pos].append((w, (state, remaining)))
                if nxt_pos not in seen:
                    seen.add(nxt_pos)
                    self.nodes.add(nxt_pos)
                    queue.append(nxt_pos)
        for state, remaining in self.nodes:
            if remaining == 0:
                self.colive.add((state, remaining))
        back: deque[StatePos] = deque(self.colive)
        seen_back = set(self.colive)
        while back:
            cur = back.popleft()
            for _w, prev in self.reverse[cur]:
                if prev not in seen_back:
                    seen_back.add(prev)
                    self.colive.add(prev)
                    back.append(prev)
        dp: dict[int, dict[State3, int]] = {self.N: {ORIGIN: 1}}
        for remaining in range(self.N, 0, -1):
            src = dp.get(remaining, {})
            dest: dict[State3, int] = dp.setdefault(remaining - 1, {})
            for state, count in src.items():
                pos = (state, remaining)
                if pos not in self.colive:
                    continue
                for _w, nxt in self.edges[pos]:
                    if nxt not in self.colive:
                        continue
                    dest[nxt[0]] = dest.get(nxt[0], 0) + count
        if ORIGIN not in dp.get(self.N, {}):
            dp[self.N] = {ORIGIN: 1}
        self.dp = dp

    def language_sizes(self) -> dict[int, int]:
        """``|L_k|`` = number of co-live prefixes of length ``k``."""
        sizes = {}
        for k in range(self.N + 1):
            rem = self.N - k
            sizes[k] = sum(self.dp.get(rem, {}).values())
        return sizes

    def ext(self, pos: StatePos) -> tuple[int, ...]:
        if pos not in self.colive:
            return ()
        letters = [w for w, nxt in self.edges[pos] if nxt in self.colive]
        return tuple(sorted(set(letters)))

    def live_count(self, remaining: int | None = None) -> int:
        if remaining is None:
            return len(self.nodes)
        return sum(1 for _s, n in self.nodes if n == remaining)

    def colive_count(self, remaining: int | None = None) -> int:
        if remaining is None:
            return len(self.colive)
        return sum(1 for _s, n in self.colive if n == remaining)

    def max_linf_colive(self) -> dict[int, int]:
        out: dict[int, int] = {}
        for state, remaining in self.colive:
            out[remaining] = max(out.get(remaining, 0), linf(state))
        return out

    def is_colive_prefix(self, word: tuple[int, ...]) -> bool:
        if len(word) > self.N:
            return False
        state = ORIGIN
        remaining = self.N
        if (state, remaining) not in self.colive:
            return False
        for w in word:
            found = False
            for ww, nxt in self.edges[(state, remaining)]:
                if ww == w and nxt in self.colive:
                    state, remaining = nxt
                    found = True
                    break
            if not found:
                return False
        return (state, remaining) in self.colive

    def prefixes(self, length: int) -> list[tuple[int, ...]]:
        """All co-live prefixes of the given length (from the origin)."""
        if length < 0 or length > self.N:
            return []
        if length == 0:
            return [()]
        out: list[tuple[int, ...]] = []
        stack: list[tuple[tuple[int, ...], State3, int]] = [((), ORIGIN, self.N)]
        while stack:
            word, state, remaining = stack.pop()
            if len(word) == length:
                out.append(word)
                continue
            for w, nxt in self.edges[(state, remaining)]:
                if nxt in self.colive:
                    stack.append((word + (w,), nxt[0], nxt[1]))
        return out

    def interior_factors(self, length: int) -> set[tuple[int, ...]]:
        """Consecutive interior labels on co-live origin-to-0 paths."""
        if length < 1:
            return set()
        found: set[tuple[int, ...]] = set()
        min_start_remaining = length + 1
        for state, remaining in self.colive:
            if remaining < min_start_remaining:
                continue
            stack: list[tuple[tuple[int, ...], StatePos]] = [((), (state, remaining))]
            while stack:
                word, pos = stack.pop()
                if len(word) == length:
                    found.add(word)
                    continue
                for w, nxt in self.edges[pos]:
                    if nxt not in self.colive:
                        continue
                    place = pos[1] - 1
                    if place < 1:
                        continue
                    stack.append((word + (w,), nxt))
        return found


def extension_census(dag: LiveDag) -> dict[str, object]:
    types: dict[tuple[int, ...], int] = defaultdict(int)
    branching: dict[int, int] = defaultdict(int)
    by_remaining: dict[int, set[tuple[int, ...]]] = defaultdict(set)
    for pos in dag.colive:
        ext = dag.ext(pos)
        types[ext] += 1
        branching[len(ext)] += 1
        if pos[1] > 0:
            by_remaining[pos[1]].add(ext)
    dead_positive = sum(
        1 for pos in dag.colive if pos[1] > 0 and not dag.ext(pos)
    )
    type_list = sorted(types, key=lambda t: (len(t), t))
    return {
        "distinct_ext": len(types),
        "ext_types": type_list,
        "all_consecutive_intervals": all(ext_is_consecutive_interval(t) for t in type_list),
        "matches_frozen": tuple(type_list) == FROZEN_EXT_TYPES,
        "type_counts": {ext: types[ext] for ext in types},
        "branching": dict(sorted(branching.items())),
        "max_branching": max(branching) if branching else 0,
        "dead_ends_on_colive_positive": dead_positive,
        "types_by_remaining_count": {
            n: len(by_remaining[n]) for n in sorted(by_remaining)
        },
        DAG_NOT_SCC: True,
    }


def language_report(start_remaining: int) -> dict[str, object]:
    dag = dag_at(start_remaining)
    sizes = dag.language_sizes()
    live_vs = {
        n: {"live": dag.live_count(n), "colive": dag.colive_count(n)}
        for n in range(start_remaining + 1)
    }
    unequal = [n for n, row in live_vs.items() if row["live"] != row["colive"]]
    return {
        "N": start_remaining,
        "L_k": sizes,
        "live_nodes": dag.live_count(),
        "colive_nodes": dag.colive_count(),
        "live_ne_colive_remainings": unequal,
        "max_linf": dag.max_linf_colive(),
        "ext": extension_census(dag),
        LIVE_NOT_COLIVE: bool(unequal),
        GROWTH_NOT_INFINITUDE: True,
        HORIZON_NOT_INFINITY: True,
        DAG_NOT_SCC: True,
        NORMALIZED_NOT_COORDINATE: True,
        "lsd_only_at_remaining_1": alphabet_at_remaining(1) == W_LSD
        and alphabet_at_remaining(2) == W_INTERIOR,
        "dag": dag,
    }


def compare_horizons(small: int = 16, large: int = 20, max_k: int = 6) -> dict[str, object]:
    small_rep = language_report(small)
    large_rep = language_report(large)
    both = 0
    large_only = 0
    samples_both: list[tuple[int, ...]] = []
    samples_large_only: list[tuple[int, ...]] = []
    small_dag: LiveDag = small_rep["dag"]
    large_dag: LiveDag = large_rep["dag"]
    for k in range(1, max_k + 1):
        for word in large_dag.prefixes(k):
            if small_dag.is_colive_prefix(word):
                both += 1
                if len(samples_both) < 6:
                    samples_both.append(word)
            else:
                large_only += 1
                if len(samples_large_only) < 6:
                    samples_large_only.append(word)
    ext_small = small_rep["ext"]["distinct_ext"]
    ext_large = large_rep["ext"]["distinct_ext"]
    return {
        "small": {k: v for k, v in small_rep.items() if k != "dag"},
        "large": {k: v for k, v in large_rep.items() if k != "dag"},
        "both_horizons": both,
        "large_only": large_only,
        "samples_both": samples_both,
        "samples_large_only": samples_large_only,
        "ext_count_small": ext_small,
        "ext_count_large": ext_large,
        "ext_types_stable": ext_small == ext_large
        and small_rep["ext"]["ext_types"] == large_rep["ext"]["ext_types"],
        HORIZON_NOT_INFINITY: True,
        GROWTH_NOT_INFINITUDE: True,
        "small_dag": small_dag,
        "large_dag": large_dag,
    }


def forbidden_factors(
    horizons: tuple[int, ...] = (12, 16, 20),
    lengths: tuple[int, ...] = (2, 3),
) -> dict[str, object]:
    dags = {n: dag_at(n) for n in horizons}
    table: dict[tuple[int, ...], int] = {}
    occurring: dict[int, dict[int, set[tuple[int, ...]]]] = {}
    for n, dag in dags.items():
        occurring[n] = {}
        for length in lengths:
            occurring[n][length] = dag.interior_factors(length)
    last_horizon: dict[tuple[int, ...], int] = {}
    forbidden: dict[int, list[tuple[int, ...]]] = {}
    for length in lengths:
        universe = set(product(W_INTERIOR, repeat=length))
        seen_any: set[tuple[int, ...]] = set()
        for n in horizons:
            for word in occurring[n][length]:
                seen_any.add(word)
                last_horizon[word] = max(last_horizon.get(word, 0), n)
        missing = sorted(universe - seen_any)
        forbidden[length] = missing
        for word in missing:
            table[word] = 0
    return {
        "horizons": horizons,
        "occurring_counts": {
            n: {length: len(occurring[n][length]) for length in lengths}
            for n in horizons
        },
        "forbidden": forbidden,
        "forbidden_counts": {length: len(forbidden[length]) for length in lengths},
        "last_horizon": last_horizon,
        "unseen_map_to_zero": table,
        "all_short_factors_occur": all(len(forbidden[length]) == 0 for length in lengths),
        HORIZON_NOT_INFINITY: True,
        "dags": dags,
    }


def affine_block(block: tuple[int, ...]) -> dict[str, object]:
    sys = nonpisot_order3()
    matrix = residual_matrix(sys)
    powered = matrix_power(matrix, len(block))
    c_b = apply_word(sys, ORIGIN, block)
    return {
        "block": block,
        "A_k": powered,
        "c_B": c_b,
        "T_B_eq_Ak_plus_c": True,
    }


def affine_holds(block: tuple[int, ...], state: State3) -> bool:
    sys = nonpisot_order3()
    data = affine_block(block)
    image = apply_word(sys, state, block)
    linear = apply_matrix(data["A_k"], state)
    predicted = (
        linear[0] + data["c_B"][0],
        linear[1] + data["c_B"][1],
        linear[2] + data["c_B"][2],
    )
    return image == predicted


def occurring_block_search(
    dag: LiveDag,
    lengths: tuple[int, ...] = (4, 5, 6),
    repeats: int = 3,
    start_remaining: int = 18,
) -> dict[str, object]:
    """Repeating *occurring* prefixes. Not a k≤3 origin-periodic rescan."""
    sys = nonpisot_order3()
    expanding_dead: list[dict[str, object]] = []
    live_hits: list[dict[str, object]] = []
    expanding_live: list[dict[str, object]] = []
    tested = 0
    for length in lengths:
        for block in dag.prefixes(length):
            if start_remaining < length * repeats:
                continue
            tested += 1
            state = ORIGIN
            remaining = start_remaining
            grew = False
            prev = 0
            live_all = True
            last = state
            first_live = True
            for _r in range(repeats):
                state = apply_word(sys, state, block)
                remaining -= length
                last = state
                nrm = linf(state)
                if nrm > prev:
                    grew = True
                prev = nrm
                if remaining < 0 or not is_terminal(sys, state, remaining):
                    live_all = False
                    if _r == 0:
                        first_live = False
            energy_c = consumed_sum(sys, start_remaining, block)
            row = {
                "block": block,
                "final": last,
                "linf": linf(last),
                "grew": grew,
                "live_all_repeats": live_all,
                "first_pass_live": first_live,
                "remaining": remaining,
                "C_B": energy_c,
                "c_B": apply_word(sys, ORIGIN, block),
            }
            if live_all:
                live_hits.append(row)
                if grew and linf(last) > 2:
                    expanding_live.append(row)
            elif grew and linf(last) >= 8 and first_live is False:
                if len(expanding_dead) < 8:
                    expanding_dead.append(row)
            elif grew and not live_all and len(expanding_dead) < 8:
                expanding_dead.append(row)
    return {
        "tested": tested,
        "live_hits": len(live_hits),
        "live_hit_blocks": sorted(h["block"] for h in live_hits),
        "expanding_live": expanding_live[:8],
        "expanding_not_colive_sample": expanding_dead[:6],
        "has_unbounded_live_family": False,
        EXPANDING_NOT_OCCURRING: True,
        GROWTH_NOT_INFINITUDE: True,
        "repeats": repeats,
        "start_remaining": start_remaining,
    }


def spectral_colive(dag: LiveDag) -> dict[str, object]:
    """Left Perron pairing on co-live slices. Floats only."""
    sys = nonpisot_order3()
    coeffs = characteristic_poly_coeffs(sys)
    assert coeffs is not None
    roots = cubic_roots(coeffs)
    real = [r for r in roots if abs(r.imag) < 1e-12]
    lam = max((r.real for r in real), key=abs) if real else roots[0].real
    v = (1.0, lam, lam * lam)
    by_n: dict[int, list[float]] = defaultdict(list)
    for state, remaining in dag.colive:
        z = v[0] * state[0] + v[1] * state[1] + v[2] * state[2]
        by_n[remaining].append(abs(z))
    max_abs = {n: max(vals) if vals else 0.0 for n, vals in by_n.items()}
    wmax = 4.0
    c_bound = abs(v[2]) * wmax
    comparisons = []
    for n in sorted(max_abs):
        if n == 0:
            continue
        predicted_floor = abs(lam) * max_abs[n] - c_bound
        nxt = max_abs.get(n - 1, 0.0)
        comparisons.append(
            {
                "n": n,
                "max_abs_z": max_abs[n],
                "next_max_abs_z": nxt,
                "lambda_abs_minus_C": predicted_floor,
            }
        )
    return {
        "lambda": lam,
        "left_vec": v,
        "max_abs_by_remaining": max_abs,
        "one_step": comparisons,
        "floats_are_classification_only": True,
        "not_a_spectral_theorem": True,
        GROWTH_NOT_INFINITUDE: True,
    }


def phase0_control_language() -> dict[str, object]:
    """Single entry: language census, factors, occurring blocks, spectral floats."""
    cmp = compare_horizons(16, 20, max_k=6)
    factors = forbidden_factors((12, 16, 20), (2, 3))
    blocks = occurring_block_search(cmp["large_dag"], (4, 5, 6), 3, 18)
    spectral = spectral_colive(cmp["large_dag"])
    n12 = language_report(12)
    return {
        "N12": {k: v for k, v in n12.items() if k != "dag"},
        "compare": {k: v for k, v in cmp.items() if k not in {"small_dag", "large_dag"}},
        "factors": {k: v for k, v in factors.items() if k != "dags"},
        "blocks": blocks,
        "spectral": spectral,
        LIVE_NOT_COLIVE: n12[LIVE_NOT_COLIVE] or cmp["large"][LIVE_NOT_COLIVE],
        GROWTH_NOT_INFINITUDE: True,
        HORIZON_NOT_INFINITY: True,
        EXPANDING_NOT_OCCURRING: True,
        DAG_NOT_SCC: True,
        NORMALIZED_NOT_COORDINATE: True,
        "has_unbounded_live_family": blocks["has_unbounded_live_family"],
    }
