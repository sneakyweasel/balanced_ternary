"""Exceptional kernel classes n ≡ 0 or 12 (mod 24) for Γ_NP.

Three relations, never mixed:

- Lean ``OriginReachable``: unrestricted ``w ∈ Z``. Already infinite;
  the existing theorem still excludes non-exceptional ``t_n``.
- ``R_W(0)``: interior alphabet ``W = {-4,…,2}`` (LSD ``{-2,…,1}``).
- ``L_0``: legal ``w`` and unread-tail liveness. Not proved finite or
  infinite here.

``C({0})`` is co-reachability of the origin, not ``R_W(0)``. Unbounded
``K`` does not imply unbounded ``L_0``. Finite reverse depth is not
unreachability. Finite modular graphs are not a live-set theorem.

Do not reparameterize the known ``s_1 ≡ 0 (mod 3)`` trap.
"""

from __future__ import annotations

from collections import deque
from itertools import product

from research.ostrowski.live_growth import residual_is_live
from research.ostrowski.nonpisot_search import HUB, l1
from research.ostrowski.origin_live import two_step_f_to_f
from research.ostrowski.reverse_map import integer_preimage
from research.ostrowski.spectral_residual import transition_affine
from research.ostrowski.system import nonpisot_order3
from research.ostrowski.terminal_set import is_terminal, kernel_family_state

State3 = tuple[int, int, int]
W_INTERIOR: tuple[int, ...] = tuple(range(-4, 3))
W_LSD: tuple[int, ...] = tuple(range(-2, 2))
DEFAULT_MODULI: tuple[int, ...] = (4, 8, 9, 13, 18, 24, 27)
CLASS_0 = 0
CLASS_12 = 12
ORIGIN: State3 = (0, 0, 0)
# C({0}) max ℓ₁ from exact_closure.BASIN_MAX_L1. Not imported: that module
# is the co-reachability basin, not R_W(0).
BASIN_MAX_L1 = 57

# Finite reverse BFS is pattern discovery, not a proof of unreachability.
REVERSE_NOT_A_PROOF = "finite_reverse_depth_is_not_unreachability"

GM_MODULI: tuple[int, ...] = (8, 9, 12, 18, 24, 27, 36, 48)
WINDOW_MODULI: tuple[int, ...] = (8, 9, 12, 18, 24)
AFFINE_AUG_MODULI: tuple[int, ...] = (8, 9, 12)
# Exact remaining window: t_48 needs a few extra prefix steps
# (max_length=49 made t_48 a horizon artifact miss; 52 hits).
WINDOW_MAX_LENGTH = 52

_Q_PERIOD_CACHE: dict[int, tuple[int, ...]] = {}
_REACH_CACHE: dict[tuple[int, tuple[int, ...]], frozenset[State3]] = {}
_GM_CACHE: dict[int, tuple[int, bytearray]] = {}


def _sys():
    return nonpisot_order3()


def _mod3(state: State3, modulus: int) -> State3:
    return (state[0] % modulus, state[1] % modulus, state[2] % modulus)


def step_mod(state: State3, w: int, modulus: int) -> State3:
    s1, s2, s3 = state
    return (
        (3 * s3) % modulus,
        (s1 + s3) % modulus,
        (s2 + 2 * s3 - w) % modulus,
    )


def exceptional_ns(remainder: int, count: int = 8) -> tuple[int, ...]:
    """``24k`` (remainder 0) or ``24k+12`` (remainder 12), positive."""
    if remainder not in (CLASS_0, CLASS_12):
        raise ValueError("remainder must be 0 or 12")
    if remainder == CLASS_0:
        return tuple(24 * k for k in range(1, count + 1))
    return tuple(24 * k + 12 for k in range(count))


def _q_mod_stream(modulus: int, length: int) -> list[int]:
    """``q_0,…,q_{length-1}`` modulo ``m`` by the linear recurrence."""
    if length < 1:
        return []
    seq = [1 % modulus]
    if length == 1:
        return seq
    seq.append(2 % modulus)
    if length == 2:
        return seq
    seq.append(5 % modulus)
    for _ in range(3, length):
        seq.append((2 * seq[-1] + seq[-2] + 3 * seq[-3]) % modulus)
    return seq


def _q_period(modulus: int) -> tuple[int, ...]:
    """Period of ``q_n mod m`` when the initial triple is on a cycle."""
    cached = _Q_PERIOD_CACHE.get(modulus)
    if cached is not None:
        return cached
    if modulus < 2:
        raise ValueError("modulus must be >= 2")
    cap = modulus**3 + 8
    mods = _q_mod_stream(modulus, cap)
    start = (mods[0], mods[1], mods[2])
    for n in range(3, cap):
        if (mods[n - 2], mods[n - 1], mods[n]) == start:
            cached = tuple(mods[: n - 2])
            _Q_PERIOD_CACHE[modulus] = cached
            return cached
    raise RuntimeError("place-value recurrence did not period modulo m")


def class_target_residues(modulus: int, remainder: int) -> frozenset[State3]:
    """All ``t_n mod m`` for one exceptional class, via the q-recurrence mod m."""
    seq = [1 % modulus, 2 % modulus, 5 % modulus]
    seen_pairs: set[tuple[int, int]] = set()
    residues: set[State3] = set()
    k = 0
    limit = modulus * modulus + 8
    while k <= limit:
        n = 24 * (k + 1) if remainder == CLASS_0 else 24 * k + remainder
        if n < 1:
            k += 1
            continue
        while len(seq) <= n:
            seq.append((2 * seq[-1] + seq[-2] + 3 * seq[-3]) % modulus)
        q1 = seq[n - 1]
        q2 = seq[n - 2]
        pair = (q1, q2)
        if pair in seen_pairs:
            break
        seen_pairs.add(pair)
        residues.add((q1, (-q2) % modulus, 0))
        k += 1
    return frozenset(residues)


def reachable_residues(modulus: int, alphabet: tuple[int, ...]) -> frozenset[State3]:
    """Forward residue BFS from the origin on ``(Z/mZ)^3``."""
    cache_key = (modulus, alphabet)
    cached = _REACH_CACHE.get(cache_key)
    if cached is not None:
        return cached
    start = ORIGIN
    seen = {start}
    layer = [start]
    while layer:
        nxt: list[State3] = []
        for state in layer:
            for w in alphabet:
                image = step_mod(state, w, modulus)
                if image not in seen:
                    seen.add(image)
                    nxt.append(image)
        layer = nxt
    frozen = frozenset(seen)
    _REACH_CACHE[cache_key] = frozen
    return frozen


def modular_row(modulus: int) -> dict[str, object]:
    """One modulus: W-restricted and alphabet-free reachable residues vs both classes."""
    w_reach = reachable_residues(modulus, W_INTERIOR)
    free_alphabet = tuple(range(modulus))
    free_reach = reachable_residues(modulus, free_alphabet)
    targets_0 = class_target_residues(modulus, CLASS_0)
    targets_12 = class_target_residues(modulus, CLASS_12)
    return {
        "m": modulus,
        "reachable_W": len(w_reach),
        "reachable_free": len(free_reach),
        "target_0": sorted(targets_0),
        "target_12": sorted(targets_12),
        "target_0_count": len(targets_0),
        "target_12_count": len(targets_12),
        "separates_0_W": targets_0.isdisjoint(w_reach),
        "separates_12_W": targets_12.isdisjoint(w_reach),
        "separates_0_free": targets_0.isdisjoint(free_reach),
        "separates_12_free": targets_12.isdisjoint(free_reach),
        "all_reachable_have_s1_mod3_zero": all(s[0] % 3 == 0 for s in w_reach)
        if modulus % 3 == 0
        else None,
    }


def modular_search(moduli: tuple[int, ...] = DEFAULT_MODULI) -> dict[str, object]:
    rows = [modular_row(m) for m in moduli]
    return {
        "rows": rows,
        "any_separates_0_free": any(r["separates_0_free"] for r in rows),
        "any_separates_12_free": any(r["separates_12_free"] for r in rows),
        "any_separates_0_W": any(r["separates_0_W"] for r in rows),
        "any_separates_12_W": any(r["separates_12_W"] for r in rows),
        "s1_mod3_is_not_a_new_invariant": True,
        "unbounded_K_does_not_imply_unbounded_L0": True,
    }


def affine_laws(modulus: int) -> list[tuple[int, int, int, int, int]]:
    """``ell(T_w s) ≡ λ ell(s) + μ w (mod m)`` for all s, w.

    Coefficient match: ``ell = a s1 + b s2 + c s3``.
    """
    laws: list[tuple[int, int, int, int, int]] = []
    for a, b, c, lam in product(range(modulus), repeat=4):
        if (b - lam * a) % modulus:
            continue
        if (c - lam * b) % modulus:
            continue
        if (3 * a + b + 2 * c - lam * c) % modulus:
            continue
        if a == 0 and b == 0 and c == 0:
            continue
        mu = (-c) % modulus
        laws.append((a, b, c, lam, mu))
    return laws


def _ell(coeff: tuple[int, int, int], state: State3, modulus: int) -> int:
    a, b, c = coeff
    return (a * state[0] + b * state[1] + c * state[2]) % modulus


def _is_s1_reparam(a: int, b: int, c: int, modulus: int) -> bool:
    """Pure first-coordinate forms, including the known ``s1`` trap."""
    return b % modulus == 0 and c % modulus == 0


def affine_search(moduli: tuple[int, ...] = (8, 9, 13)) -> dict[str, object]:
    """Linear forms that are not the ``s1 (mod 3)`` trap and that miss a class."""
    hits: list[dict[str, object]] = []
    for modulus in moduli:
        w_reach = reachable_residues(modulus, W_INTERIOR)
        free_reach = reachable_residues(modulus, tuple(range(modulus)))
        t0 = class_target_residues(modulus, CLASS_0)
        t12 = class_target_residues(modulus, CLASS_12)
        for a, b, c, lam, mu in affine_laws(modulus):
            if _is_s1_reparam(a, b, c, modulus):
                continue
            coeff = (a, b, c)
            reach_vals = {_ell(coeff, s, modulus) for s in w_reach}
            free_vals = {_ell(coeff, s, modulus) for s in free_reach}
            t0_vals = {_ell(coeff, s, modulus) for s in t0}
            t12_vals = {_ell(coeff, s, modulus) for s in t12}
            sep0 = t0_vals.isdisjoint(reach_vals)
            sep12 = t12_vals.isdisjoint(reach_vals)
            sep0_free = t0_vals.isdisjoint(free_vals)
            sep12_free = t12_vals.isdisjoint(free_vals)
            if sep0 or sep12 or sep0_free or sep12_free:
                hits.append(
                    {
                        "m": modulus,
                        "a": a,
                        "b": b,
                        "c": c,
                        "lambda": lam,
                        "mu": mu,
                        "separates_0_W": sep0,
                        "separates_12_W": sep12,
                        "separates_0_free": sep0_free,
                        "separates_12_free": sep12_free,
                    }
                )
    return {
        "separating_laws": hits,
        "count": len(hits),
        "discarded_s1_reparams": True,
    }


def length_residue_window(modulus: int, max_length: int) -> dict[str, object]:
    """Exact remaining length, residues of ``s``. LSD alphabet only at remaining 1."""
    seen: set[tuple[int, int, int, int]] = set()
    queue: deque[tuple[int, int, int, int]] = deque()
    for start in range(max_length + 1):
        key = (start, 0, 0, 0)
        seen.add(key)
        queue.append(key)
    while queue:
        remaining, s1, s2, s3 = queue.popleft()
        if remaining == 0:
            continue
        alphabet = W_LSD if remaining == 1 else W_INTERIOR
        for w in alphabet:
            nxt = (
                remaining - 1,
                (3 * s3) % modulus,
                (s1 + s3) % modulus,
                (s2 + 2 * s3 - w) % modulus,
            )
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    hits_0: list[int] = []
    hits_12: list[int] = []
    miss_0: list[int] = []
    miss_12: list[int] = []
    sys = _sys()
    for n in exceptional_ns(CLASS_0, count=4):
        if n >= max_length:
            continue
        t = _mod3(kernel_family_state(sys, n), modulus)
        ok = (n, t[0], t[1], t[2]) in seen
        (hits_0 if ok else miss_0).append(n)
    for n in exceptional_ns(CLASS_12, count=4):
        if n >= max_length:
            continue
        t = _mod3(kernel_family_state(sys, n), modulus)
        ok = (n, t[0], t[1], t[2]) in seen
        (hits_12 if ok else miss_12).append(n)
    return {
        "m": modulus,
        "max_length": max_length,
        "nodes": len(seen),
        "class_0_residue_hits": hits_0,
        "class_12_residue_hits": hits_12,
        "class_0_residue_misses": miss_0,
        "class_12_residue_misses": miss_12,
        "length_mod_is_not_OriginReachable": True,
    }


def length_mod_search(
    moduli: tuple[int, ...] = (8, 9),
    max_length: int = 16,
) -> dict[str, object]:
    rows = [length_residue_window(m, max_length) for m in moduli]
    return {"rows": rows, "window_is_not_a_global_obstruction": True}


def length_window_extended(
    moduli: tuple[int, ...] = WINDOW_MODULI,
    max_length: int = WINDOW_MAX_LENGTH,
) -> dict[str, object]:
    """Exact-remaining window covering t_24, t_36, t_48.

    Remaining is exact, so ``n`` near ``max_length`` has almost no prefix
    and a miss is inconclusive. ``G_m`` is the finite quotient. This
    window is not an obstruction.
    """
    rows = [length_residue_window(m, max_length) for m in moduli]
    return {
        "rows": rows,
        "window_is_not_a_global_obstruction": True,
        "finite_quotient_is_not_unreachability": True,
    }


def exceptional_phase_targets(
    modulus: int,
    remainder: int,
) -> frozenset[tuple[int, int, int, int]]:
    """Pairs ``(n mod m, t_n mod m)`` for one exceptional class."""
    seen_keys: set[tuple[int, int, int]] = set()
    out: set[tuple[int, int, int, int]] = set()
    seq = [1 % modulus, 2 % modulus, 5 % modulus]
    k = 0
    limit = modulus * modulus + 8
    while k <= limit:
        n = 24 * (k + 1) if remainder == CLASS_0 else 24 * k + remainder
        if n < 1:
            k += 1
            continue
        while len(seq) <= n:
            seq.append((2 * seq[-1] + seq[-2] + 3 * seq[-3]) % modulus)
        phase = n % modulus
        q1 = seq[n - 1]
        q2 = seq[n - 2]
        key = (phase, q1, q2)
        if key in seen_keys:
            break
        seen_keys.add(key)
        out.add((phase, q1, (-q2) % modulus, 0))
        k += 1
    return frozenset(out)


def _gm_index(r: int, s1: int, s2: int, s3: int, modulus: int) -> int:
    return ((r * modulus + s1) * modulus + s2) * modulus + s3


def _gm_seen(modulus: int) -> tuple[int, bytearray]:
    """Over-approx reachable bitmap of ``G_m``: interior ``W`` at every phase."""
    cached = _GM_CACHE.get(modulus)
    if cached is not None:
        return cached
    m = modulus
    nstates = m * m * m * m
    seen = bytearray(nstates)
    queue: deque[tuple[int, int, int, int]] = deque()
    for r in range(m):
        idx = _gm_index(r, 0, 0, 0, m)
        seen[idx] = 1
        queue.append((r, 0, 0, 0))
    reachable = m
    while queue:
        r, s1, s2, s3 = queue.popleft()
        nr = r - 1 if r else m - 1
        for w in W_INTERIOR:
            t1 = (3 * s3) % m
            t2 = (s1 + s3) % m
            t3 = (s2 + 2 * s3 - w) % m
            idx = _gm_index(nr, t1, t2, t3, m)
            if not seen[idx]:
                seen[idx] = 1
                reachable += 1
                queue.append((nr, t1, t2, t3))
    packed = (reachable, seen)
    _GM_CACHE[modulus] = packed
    return packed


def gm_reachable_list(modulus: int) -> list[tuple[int, int, int, int]]:
    """Materialize over-approx reachable states. For affine scans on small m."""
    _, seen = _gm_seen(modulus)
    m = modulus
    out: list[tuple[int, int, int, int]] = []
    m2 = m * m
    m3 = m2 * m
    for idx, flag in enumerate(seen):
        if not flag:
            continue
        r, rem = divmod(idx, m3)
        s1, rem = divmod(rem, m2)
        s2, s3 = divmod(rem, m)
        out.append((r, s1, s2, s3))
    return out


def time_augmented_row(modulus: int) -> dict[str, object]:
    """One finite quotient ``G_m``. A hit is not reachability; a miss is an obstruction candidate."""
    reachable_count, seen = _gm_seen(modulus)
    g_size = modulus**4
    t0 = exceptional_phase_targets(modulus, CLASS_0)
    t12 = exceptional_phase_targets(modulus, CLASS_12)
    miss_0 = [t for t in sorted(t0) if not seen[_gm_index(*t, modulus)]]
    miss_12 = [t for t in sorted(t12) if not seen[_gm_index(*t, modulus)]]
    hit_0 = len(t0) - len(miss_0)
    hit_12 = len(t12) - len(miss_12)
    return {
        "m": modulus,
        "g_size": g_size,
        "reachable": reachable_count,
        "target_0_count": len(t0),
        "target_12_count": len(t12),
        "target_exc_count": len(t0) + len(t12),
        "hits_0": hit_0,
        "hits_12": hit_12,
        "miss_0": miss_0,
        "miss_12": miss_12,
        "separates_0": bool(miss_0) and hit_0 == 0,
        "separates_12": bool(miss_12) and hit_12 == 0,
        "separates": (bool(miss_0) and hit_0 == 0) or (bool(miss_12) and hit_12 == 0),
        "over_approx_interior_W": True,
        "finite_quotient_hit_is_not_reachability": True,
    }


def time_augmented_search(
    moduli: tuple[int, ...] = GM_MODULI,
) -> dict[str, object]:
    rows = [time_augmented_row(m) for m in moduli]
    return {
        "rows": rows,
        "any_separates": any(r["separates"] for r in rows),
        "finite_quotient_is_not_unreachability": True,
        "over_approx_interior_W": True,
        "s1_mod3_is_not_a_new_invariant": True,
    }


def _ell_aug(
    coeff: tuple[int, int, int, int],
    state: tuple[int, int, int, int],
    modulus: int,
) -> int:
    a, b, c, d = coeff
    r, s1, s2, s3 = state
    return (a * r + b * s1 + c * s2 + d * s3) % modulus


def _is_s1_or_time_reparam(a: int, b: int, c: int, d: int, modulus: int) -> bool:
    """Spatial part is only ``s1`` (the known trap), with optional time."""
    return c % modulus == 0 and d % modulus == 0


def affine_augmented_search(
    moduli: tuple[int, ...] = AFFINE_AUG_MODULI,
) -> dict[str, object]:
    """Linear forms ``α r + β s1 + γ s2 + δ s3`` on ``G_m``.

    Discard ``s1``-reparams (including time-only and ``(r, s1)``). A
    finite-quotient miss is not an infinite obstruction.
    """
    hits: list[dict[str, object]] = []
    for modulus in moduli:
        reach = gm_reachable_list(modulus)
        t0 = list(exceptional_phase_targets(modulus, CLASS_0))
        t12 = list(exceptional_phase_targets(modulus, CLASS_12))
        for a, b, c, d in product(range(modulus), repeat=4):
            if a == 0 and b == 0 and c == 0 and d == 0:
                continue
            if _is_s1_or_time_reparam(a, b, c, d, modulus):
                continue
            coeff = (a, b, c, d)
            t0_vals = {_ell_aug(coeff, t, modulus) for t in t0}
            t12_vals = {_ell_aug(coeff, t, modulus) for t in t12}
            reach_vals: set[int] = set()
            sep0 = True
            sep12 = True
            for state in reach:
                val = _ell_aug(coeff, state, modulus)
                if val not in reach_vals:
                    reach_vals.add(val)
                    if val in t0_vals:
                        sep0 = False
                    if val in t12_vals:
                        sep12 = False
                    if not sep0 and not sep12:
                        break
                    if len(reach_vals) == modulus:
                        sep0 = False
                        sep12 = False
                        break
            if sep0:
                sep0 = t0_vals.isdisjoint(reach_vals)
            if sep12:
                sep12 = t12_vals.isdisjoint(reach_vals)
            if sep0 or sep12:
                hits.append(
                    {
                        "m": modulus,
                        "alpha": a,
                        "beta": b,
                        "gamma": c,
                        "delta": d,
                        "separates_0": sep0,
                        "separates_12": sep12,
                    }
                )
    return {
        "separating_laws": hits,
        "count": len(hits),
        "discarded_s1_and_time_reparams": True,
        "finite_quotient_is_not_unreachability": True,
    }


def reverse_cone(
    target: State3,
    max_depth: int,
    alphabet: tuple[int, ...] = W_INTERIOR,
    max_states: int = 20000,
    residue_moduli: tuple[int, ...] = (9, 24),
) -> dict[str, object]:
    """Instrumented reverse BFS. Finite depth is not unreachability."""
    seen: set[State3] = {target}
    layer: set[State3] = {target}
    hit_origin = target == ORIGIN
    layers: list[dict[str, object]] = [
        {
            "depth": 0,
            "cardinality": 1,
            "min_l1": l1(target),
            "max_l1": l1(target),
            "on_F": int(target[2] == 0),
        }
    ]
    first_rw_collision: dict[str, object] | None = None
    forward_res = {m: reachable_residues(m, alphabet) for m in residue_moduli}
    truncated = False
    depth = 0
    for depth in range(1, max_depth + 1):
        nxt: set[State3] = set()
        for t in layer:
            if t[0] % 3 != 0:
                continue
            for w in alphabet:
                pred = integer_preimage(t, w)
                if pred is None or pred in seen:
                    continue
                seen.add(pred)
                nxt.add(pred)
                if pred == ORIGIN:
                    hit_origin = True
                if first_rw_collision is None:
                    for m, rset in forward_res.items():
                        if _mod3(pred, m) in rset:
                            first_rw_collision = {
                                "depth": depth,
                                "state": pred,
                                "modulus": m,
                                "note": "residue collision is not a path to the origin",
                            }
                            break
                if len(seen) >= max_states:
                    truncated = True
                    break
            if truncated:
                break
        min_l1 = min((l1(s) for s in nxt), default=None)
        max_l1_v = max((l1(s) for s in nxt), default=None)
        layers.append(
            {
                "depth": depth,
                "cardinality": len(nxt),
                "min_l1": min_l1,
                "max_l1": max_l1_v,
                "on_F": sum(1 for s in nxt if s[2] == 0),
            }
        )
        if not nxt or hit_origin or truncated:
            break
        layer = nxt
    all_l1 = [l1(s) for s in seen]
    return {
        "target": target,
        "cardinality": len(seen),
        "depth": depth,
        "hit_origin": hit_origin,
        "min_l1": min(all_l1),
        "max_l1": max(all_l1),
        "layers": layers,
        "truncated": truncated,
        "basin_l1_cap": BASIN_MAX_L1,
        "hits_C_of_zero_possible": min(all_l1) <= BASIN_MAX_L1,
        "first_forward_residue_collision": first_rw_collision,
        REVERSE_NOT_A_PROOF: True,
        "C_of_zero_is_not_R_W": True,
    }


def reverse_cones_exceptional(
    ns: tuple[int, ...] = (12, 24, 36, 48),
    max_depth: int = 4,
) -> dict[str, object]:
    sys = _sys()
    rows = []
    for n in ns:
        t = kernel_family_state(sys, n)
        cone = reverse_cone(t, max_depth)
        cone["n"] = n
        cone["class"] = n % 24
        cone["l1_t"] = l1(t)
        rows.append(cone)
    return {
        "rows": rows,
        "class_0_ns": [r["n"] for r in rows if r["class"] == CLASS_0],
        "class_12_ns": [r["n"] for r in rows if r["class"] == CLASS_12],
        "any_hit_origin": any(r["hit_origin"] for r in rows),
        REVERSE_NOT_A_PROOF: True,
    }


def f_return_legal(a: int, b: int, w: int) -> State3 | None:
    """Two-step ``F→F`` with both controls in the interior alphabet."""
    alpha = b - w
    v = a + 2 * alpha
    if w not in W_INTERIOR or v not in W_INTERIOR:
        return None
    image = two_step_f_to_f(a, b, w, v)
    assert image == (3 * alpha, alpha, 0)
    return image


def f_return_report() -> dict[str, object]:
    """Legal two-step returns land on the ray ``(3k, k, 0)`` with bounded ``k``."""
    legal_k: set[int] = set()
    for k, w in product(range(-8, 9), W_INTERIOR):
        v = 5 * k - 2 * w
        if v in W_INTERIOR:
            legal_k.add(k)
    from_origin: list[dict[str, object]] = []
    for w in W_INTERIOR:
        image = f_return_legal(0, 0, w)
        if image is None:
            continue
        k = image[1]
        from_origin.append({"w": w, "image": image, "k": k, "is_hub": image == HUB})
    from_hub: list[State3] = []
    for w in W_INTERIOR:
        image = f_return_legal(HUB[0], HUB[1], w)
        if image is not None:
            from_hub.append(image)
    sys = _sys()
    ray_live: list[dict[str, object]] = []
    for k in sorted(legal_k):
        state = (3 * k, k, 0)
        live_ns = [n for n in range(0, 13) if is_terminal(sys, state, n)]
        ray_live.append({"k": k, "state": state, "live_at": live_ns, "is_hub": state == HUB})
    tn_on_ray = []
    for n in (12, 24, 36, 48):
        t = kernel_family_state(sys, n)
        on = t[2] == 0 and t[0] == 3 * t[1]
        tn_on_ray.append({"n": n, "on_ray": on})
    return {
        "identity": "T_v T_w (a,b,0) = (3 alpha, alpha, 0) with alpha = b-w, v = a+2 alpha",
        "legal_k": sorted(legal_k),
        "legal_k_bounded": max(abs(k) for k in legal_k) <= 2,
        "from_origin": from_origin,
        "from_hub": sorted(set(from_hub)),
        "hub_on_ray": HUB == (-3, -1, 0),
        "ray_live_sample": ray_live,
        "kernel_family_not_on_ray": all(not row["on_ray"] for row in tn_on_ray),
        "tn_on_ray": tn_on_ray,
        "bounded_ray_is_not_unbounded_L0": True,
    }


def _apply_block(state: State3, block: tuple[int, ...]) -> State3:
    sys = _sys()
    out = state
    for w in block:
        out = transition_affine(sys, out, w)
    return out


def periodic_blocks(
    max_block: int = 2,
    repeats: int = 6,
    check_ns: tuple[int, ...] = (12, 24, 36, 48),
) -> dict[str, object]:
    """Repeating interior blocks from the origin. A hit needs liveness separately."""
    sys = _sys()
    targets = {n: kernel_family_state(sys, n) for n in check_ns}
    tn_hits: list[dict[str, object]] = []
    f_hits: list[dict[str, object]] = []
    max_l1 = 0
    growing = False
    prev_max = 0
    for length in range(1, max_block + 1):
        for block in product(W_INTERIOR, repeat=length):
            state = ORIGIN
            orbit_l1 = [0]
            for r in range(1, repeats + 1):
                state = _apply_block(state, block)
                orbit_l1.append(l1(state))
                max_l1 = max(max_l1, l1(state))
                if state[2] == 0 and state != ORIGIN:
                    live_here = [
                        n
                        for n in range(0, 13)
                        if residual_is_live(sys, state, n)
                    ]
                    if live_here:
                        f_hits.append(
                            {
                                "block": block,
                                "repeats": r,
                                "state": state,
                                "live_at": live_here,
                            }
                        )
                for n, t in targets.items():
                    if state == t:
                        tn_hits.append({"n": n, "block": block, "repeats": r})
            if orbit_l1[-1] > prev_max:
                growing = True
            prev_max = max(prev_max, orbit_l1[-1])
            if len(f_hits) > 40:
                break
        if len(f_hits) > 40:
            break
    # Dedup F hits by state
    uniq_f = {}
    for row in f_hits:
        uniq_f[row["state"]] = row
    return {
        "tn_hits": tn_hits,
        "f_live_hits_sample": list(uniq_f.values())[:20],
        "f_live_distinct": len(uniq_f),
        "max_l1_seen": max_l1,
        "orbit_l1_grows_for_some_block": growing,
        "growth_is_not_infinitude_of_L0": True,
        "tn_hit_requires_acceptance_too": True,
    }


def phase0_report() -> dict[str, object]:
    """Deterministic Phase-0 bundle. Not a proof of |L0| or of unreachability."""
    modular = modular_search()
    affine = affine_search()
    length = length_mod_search()
    cones = reverse_cones_exceptional()
    fmap = f_return_report()
    blocks = periodic_blocks()
    return {
        "modular": modular,
        "affine": affine,
        "length": length,
        "reverse_cones": cones,
        "f_return": fmap,
        "periodic_blocks": blocks,
        "closed_alphabet_free_obstruction": bool(
            modular["any_separates_0_free"] or modular["any_separates_12_free"]
        ),
        "closed_W_obstruction": bool(
            modular["any_separates_0_W"] or modular["any_separates_12_W"]
        ),
        "affine_alphabet_free_obstruction": any(
            h["separates_0_free"] or h["separates_12_free"] for h in affine["separating_laws"]
        ),
        "bridge_tn_found": bool(blocks["tn_hits"]),
        "legal_two_step_ray_bounded": fmap["legal_k_bounded"],
        "any_cone_hit_origin": cones["any_hit_origin"],
        "outcome_d_no_theorem": True,
        "K_unbounded_does_not_imply_L0_unbounded": True,
        "tn_unreachability_does_not_imply_L0_finite": True,
        REVERSE_NOT_A_PROOF: True,
    }
