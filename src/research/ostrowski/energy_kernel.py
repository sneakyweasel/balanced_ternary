"""Complementary coordinates in ker(E_n): neighboring energies.

Rows ``u_n, u_{n-1}, u_{n-2}`` invert ``s`` for remaining ``n≥2``:

    det M_n = 3^{n-2}

    (s1, s2, s3) = M_n^{-1} (E_n, E_{n-1}, E_{n-2})

This is KNOWN linear algebra, not an ``L_0`` bound. Homogeneous motion
``A^k`` is energy-neutral in the sliding index (``energy_step`` at
``w=0``). Kernel growth on a finite origin-live slice is not
infinitude.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product

from research.ostrowski.energy_geometry import adjoint_u, energy_canonical
from research.ostrowski.energy_trajectory import apply_word
from research.ostrowski.exceptional_kernel import W_INTERIOR
from research.ostrowski.live_growth import residual_is_live
from research.ostrowski.live_layers import forward_layers, linf
from research.ostrowski.spectral_residual import apply_matrix, residual_matrix, transition_affine
from research.ostrowski.system import OstrowskiSystem, nonpisot_order3
from research_engine.algebra.lattices import matrix_det, solve_over_q, vector_gcd

State3 = tuple[int, int, int]
Vec3 = tuple[int, int, int]
Rat3 = tuple[Fraction, Fraction, Fraction]
ORIGIN: State3 = (0, 0, 0)

NORMALIZED_NOT_COORDINATE = "Kn_is_normalized_not_coordinate_bounded"
GROWTH_NOT_INFINITUDE = "finite_depth_is_not_infinitude"
KNOWN_PACKAGING = "neighboring_energies_invert_s_not_L0"
HOMOGENEOUS_IS_STEP_ZERO = "homogeneous_neutrality_is_energy_step_at_w0"


def _sys() -> OstrowskiSystem:
    return nonpisot_order3()


def triple_det(u: Vec3, v: Vec3, w: Vec3) -> int:
    """Determinant of rows ``u, v, w``."""
    return matrix_det((u, v, w))


def adjoint_window(system: OstrowskiSystem, remaining: int) -> tuple[Vec3, Vec3, Vec3]:
    """Rows ``(u_n, u_{n-1}, u_{n-2})``."""
    return (
        adjoint_u(system, remaining),
        adjoint_u(system, remaining - 1),
        adjoint_u(system, remaining - 2),
    )


def adjoint_det(system: OstrowskiSystem, remaining: int) -> int:
    return triple_det(*adjoint_window(system, remaining))


def adjoint_det_closed_form(remaining: int) -> int:
    """``det M_n = 3^{n-2}`` for ``n≥2``."""
    if remaining < 2:
        raise ValueError("neighboring-energy window needs remaining >= 2")
    return 3 ** (remaining - 2)


def adjoint_det_table(max_n: int = 24) -> dict[str, object]:
    sys = _sys()
    rows = []
    all_match = True
    first_zero = None
    first_mismatch = None
    for n in range(2, max_n + 1):
        det = adjoint_det(sys, n)
        closed = adjoint_det_closed_form(n)
        match = det == closed
        all_match = all_match and match
        if det == 0 and first_zero is None:
            first_zero = n
        if not match and first_mismatch is None:
            first_mismatch = n
        rows.append({"n": n, "det": det, "closed": closed, "match": match})
    return {
        "rows": rows,
        "all_match_closed_form": all_match,
        "all_nonzero": first_zero is None,
        "first_zero_n": first_zero,
        "first_mismatch_n": first_mismatch,
        KNOWN_PACKAGING: True,
    }


def invert_from_energies(
    system: OstrowskiSystem,
    remaining: int,
    energies: tuple[int, int, int],
) -> Rat3:
    """``M_n^{-1} (E_n, E_{n-1}, E_{n-2})`` over ``Q``."""
    if remaining < 2:
        raise ValueError("inversion needs remaining >= 2")
    rows = adjoint_window(system, remaining)
    solved = solve_over_q(rows, energies)
    if solved is None:
        raise ZeroDivisionError("adjoint window is singular")
    return tuple(solved)


def neighboring_energies(system: OstrowskiSystem, state: State3, remaining: int) -> tuple[int, int, int]:
    return (
        energy_canonical(system, state, remaining),
        energy_canonical(system, state, remaining - 1),
        energy_canonical(system, state, remaining - 2),
    )


def inversion_recovers(system: OstrowskiSystem, state: State3, remaining: int) -> bool:
    if remaining < 2:
        return False
    recovered = invert_from_energies(
        system, remaining, neighboring_energies(system, state, remaining)
    )
    return recovered == tuple(Fraction(c) for c in state)


def orthogonal_perp(system: OstrowskiSystem, state: State3, remaining: int) -> Rat3:
    """Euclidean projection of ``s`` onto ``ker(u_n)``, exact over ``Q``."""
    u = adjoint_u(system, remaining)
    uu = u[0] * u[0] + u[1] * u[1] + u[2] * u[2]
    if uu == 0:
        raise ZeroDivisionError("zero adjoint covector")
    e = energy_canonical(system, state, remaining)
    return tuple(Fraction(state[i]) - Fraction(e * u[i], uu) for i in range(3))


def energy_parallel_and_perp(
    system: OstrowskiSystem, state: State3, remaining: int
) -> dict[str, object]:
    """Neighboring-energy split plus Euclidean ``ker(u_n)`` component.

    ``s_frame = M^{-1}(0, E_{n-1}, E_{n-2})`` is the complementary-coordinate
    component (ill-conditioned). ``s_orth`` is the geometric kernel part.
    """
    if remaining < 2:
        raise ValueError("kernel split needs remaining >= 2")
    e, v, z = neighboring_energies(system, state, remaining)
    s_e = invert_from_energies(system, remaining, (e, 0, 0))
    s_frame = invert_from_energies(system, remaining, (0, v, z))
    s_sum = tuple(s_e[i] + s_frame[i] for i in range(3))
    s_orth = orthogonal_perp(system, state, remaining)
    return {
        "E": e,
        "V": v,
        "Z": z,
        "s_E": s_e,
        "s_frame": s_frame,
        "s_orth": s_orth,
        "linf_frame": max(abs(c) for c in s_frame),
        "linf_orth": max(abs(c) for c in s_orth),
        "recovers": s_sum == tuple(Fraction(c) for c in state),
    }


def apply_A_power(system: OstrowskiSystem, state: State3, k: int) -> State3:
    matrix = residual_matrix(system)
    out = state
    for _ in range(k):
        out = apply_matrix(matrix, out)
    return out


def energy_homogeneous_holds(
    system: OstrowskiSystem, state: State3, n: int, k: int
) -> bool:
    """``E_n(A^k s) = E_{n+k}(s)``. Packaging of ``energy_step`` at ``w=0``."""
    image = apply_A_power(system, state, k)
    left = energy_canonical(system, image, n)
    right = energy_canonical(system, state, n + k)
    return left == right


def sliding_homogeneous_holds(
    system: OstrowskiSystem, state: State3, remaining: int, k: int
) -> bool:
    """``E_{n-k}(A^k s) = E_n(s)`` for ``k ≤ n``."""
    if k > remaining:
        return False
    image = apply_A_power(system, state, k)
    return energy_canonical(system, image, remaining - k) == energy_canonical(
        system, state, remaining
    )


def complementary_step(
    system: OstrowskiSystem, state: State3, w: int, remaining: int
) -> dict[str, int]:
    """Neighboring energies after ``T_w``. All three are ``energy_step``."""
    nxt = transition_affine(system, state, w)
    return {
        "E_n_image": energy_canonical(system, nxt, remaining),
        "E_nm1_image": energy_canonical(system, nxt, remaining - 1),
        "E_nm2_image": energy_canonical(system, nxt, remaining - 2),
        "E_np1_minus_wq": energy_canonical(system, state, remaining + 1)
        - w * system.place_value(remaining),
        "E_n_minus_wqm1": energy_canonical(system, state, remaining)
        - w * system.place_value(remaining - 1),
        "E_nm1_minus_wqm2": energy_canonical(system, state, remaining - 1)
        - w * system.place_value(remaining - 2),
    }


def complementary_step_holds(
    system: OstrowskiSystem, state: State3, w: int, remaining: int
) -> bool:
    row = complementary_step(system, state, w, remaining)
    return (
        row["E_n_image"] == row["E_np1_minus_wq"]
        and row["E_nm1_image"] == row["E_n_minus_wqm1"]
        and row["E_nm2_image"] == row["E_nm1_minus_wqm2"]
    )


def live_kernel_report(start_remaining: int) -> dict[str, object]:
    """Origin-reachable live slices: complementary ranges and ``|s_perp|``."""
    sys = _sys()
    fwd = forward_layers(sys, start_remaining, live_only=True)
    layers = fwd["layers"]
    by_remaining: dict[int, dict[str, object]] = {}
    global_max_perp = Fraction(0)
    global_max_V = 0
    global_max_Z = 0
    for n in range(2, start_remaining + 1):
        lset = set(layers[n].get("states_L", ()))
        if not lset:
            continue
        max_frame = Fraction(0)
        max_orth = Fraction(0)
        max_V = 0
        max_Z = 0
        max_linf_state = 0
        levels: dict[int, dict[str, int]] = {}
        argmax_orth = ORIGIN
        for state in lset:
            split = energy_parallel_and_perp(sys, state, n)
            orth = split["linf_orth"]
            if orth > max_orth:
                max_orth = orth
                argmax_orth = state
            max_frame = max(max_frame, split["linf_frame"])
            max_V = max(max_V, abs(split["V"]))
            max_Z = max(max_Z, abs(split["Z"]))
            max_linf_state = max(max_linf_state, linf(state))
            e = split["E"]
            bucket = levels.setdefault(
                e, {"count": 0, "max_linf": 0, "max_abs_s1": 0, "max_abs_s3": 0}
            )
            bucket["count"] += 1
            bucket["max_linf"] = max(bucket["max_linf"], linf(state))
            bucket["max_abs_s1"] = max(bucket["max_abs_s1"], abs(state[0]))
            bucket["max_abs_s3"] = max(bucket["max_abs_s3"], abs(state[2]))
        within_level_max = max(b["max_linf"] for b in levels.values())
        busiest = max(levels.values(), key=lambda b: (b["count"], b["max_linf"]))
        by_remaining[n] = {
            "L": len(lset),
            "energy_levels": len(levels),
            "max_linf": max_linf_state,
            "max_abs_V": max_V,
            "max_abs_Z": max_Z,
            "max_linf_frame": max_frame,
            "max_linf_orth": max_orth,
            "argmax_orth": argmax_orth,
            "max_linf_within_one_E": within_level_max,
            "busiest_level_count": busiest["count"],
            "busiest_level_max_linf": busiest["max_linf"],
        }
        global_max_perp = max(global_max_perp, max_orth)
        global_max_V = max(global_max_V, max_V)
        global_max_Z = max(global_max_Z, max_Z)
    remainings = sorted(by_remaining)
    perp_grows_as_remaining_drops = False
    if len(remainings) >= 2:
        first = by_remaining[remainings[-1]]["max_linf_orth"]
        last = by_remaining[remainings[0]]["max_linf_orth"]
        perp_grows_as_remaining_drops = last > first
    within_grows = False
    if len(remainings) >= 2:
        within_grows = (
            by_remaining[remainings[0]]["max_linf_within_one_E"]
            > by_remaining[remainings[-1]]["max_linf_within_one_E"]
        )
    return {
        "N": start_remaining,
        "by_remaining": by_remaining,
        "global_max_linf_orth": global_max_perp,
        "global_max_abs_V": global_max_V,
        "global_max_abs_Z": global_max_Z,
        "perp_grows_as_remaining_drops": perp_grows_as_remaining_drops,
        "within_level_linf_grows_as_remaining_drops": within_grows,
        NORMALIZED_NOT_COORDINATE: True,
        GROWTH_NOT_INFINITUDE: True,
        KNOWN_PACKAGING: True,
        HOMOGENEOUS_IS_STEP_ZERO: True,
    }


def compare_kernel_horizons(
    n_small: int = 12, n_large: int = 16, remaining: int = 4
) -> dict[str, object]:
    """Same remaining label, two origin-start horizons. Not infinitude."""
    small = live_kernel_report(n_small)
    large = live_kernel_report(n_large)
    s_row = small["by_remaining"].get(remaining)
    l_row = large["by_remaining"].get(remaining)
    perp_grows = False
    v_grows = False
    within_grows = False
    if s_row is not None and l_row is not None:
        perp_grows = l_row["max_linf_orth"] > s_row["max_linf_orth"]
        v_grows = l_row["max_abs_V"] > s_row["max_abs_V"]
        within_grows = l_row["max_linf_within_one_E"] > s_row["max_linf_within_one_E"]
    return {
        "remaining": remaining,
        "small_N": n_small,
        "large_N": n_large,
        "small": s_row,
        "large": l_row,
        "perp_grows_with_horizon": perp_grows,
        "V_grows_with_horizon": v_grows,
        "within_level_linf_grows_with_horizon": within_grows,
        "small_global_max_orth": small["global_max_linf_orth"],
        "large_global_max_orth": large["global_max_linf_orth"],
        "global_orth_grows": large["global_max_linf_orth"] > small["global_max_linf_orth"],
        GROWTH_NOT_INFINITUDE: True,
        NORMALIZED_NOT_COORDINATE: True,
    }


def kernel_targeted_blocks(
    start_remaining: int = 12,
    source_remaining: int = 8,
    max_len: int = 4,
) -> dict[str, object]:
    """Short interior words from a large-``|s_perp|`` origin-live state.

    Not a census. A 2-repeat that stays live at one horizon is not a
    symbolic family.
    """
    sys = _sys()
    report = live_kernel_report(start_remaining)
    row = report["by_remaining"].get(source_remaining)
    if row is None:
        return {"source_found": False, "symbolic_family": False}
    seed = row["argmax_orth"]
    expanding_live: list[dict[str, object]] = []
    two_repeat_live: list[tuple[int, ...]] = []
    left_k = 0
    checked = 0
    for length in range(1, max_len + 1):
        if source_remaining < length:
            break
        for block in product(W_INTERIOR, repeat=length):
            checked += 1
            state = seed
            rem = source_remaining
            live_path = True
            for w in block:
                state = transition_affine(sys, state, w)
                rem -= 1
                if not residual_is_live(sys, state, rem):
                    live_path = False
                    left_k += 1
                    break
            if not live_path:
                continue
            grew = linf(state) > linf(seed)
            if grew:
                expanding_live.append(
                    {
                        "block": block,
                        "end": state,
                        "end_remaining": rem,
                        "start_linf": linf(seed),
                        "end_linf": linf(state),
                    }
                )
            if 2 * length <= source_remaining:
                twice = apply_word(sys, seed, block + block)
                if residual_is_live(sys, twice, source_remaining - 2 * length):
                    two_repeat_live.append(block)
    return {
        "source_found": True,
        "N": start_remaining,
        "source_remaining": source_remaining,
        "seed": seed,
        "seed_linf": linf(seed),
        "seed_linf_orth": row["max_linf_orth"],
        "checked": checked,
        "left_K": left_k,
        "expanding_live_count": len(expanding_live),
        "expanding_live_sample": expanding_live[:6],
        "two_repeat_live_count": len(two_repeat_live),
        "two_repeat_live_sample": two_repeat_live[:6],
        "symbolic_family": False,
        GROWTH_NOT_INFINITUDE: True,
        HOMOGENEOUS_IS_STEP_ZERO: True,
    }


def gcd_adjoint(system: OstrowskiSystem, remaining: int) -> int:
    return vector_gcd(adjoint_u(system, remaining))


def phase0_energy_kernel() -> dict[str, object]:
    sys = _sys()
    dets = adjoint_det_table(16)
    samples = (
        (ORIGIN, 5),
        ((-3, -1, 0), 4),
        ((6, 5, 1), 6),
        ((2, -7, 3), 8),
    )
    invert_ok = all(inversion_recovers(sys, s, n) for s, n in samples)
    hom_ok = all(
        energy_homogeneous_holds(sys, s, n, k)
        for s, n, k in (
            (ORIGIN, 3, 2),
            ((-3, -1, 0), 4, 3),
            ((6, 5, 1), 2, 4),
        )
    )
    step_ok = all(
        complementary_step_holds(sys, s, w, n)
        for s, w, n in (
            (ORIGIN, 0, 5),
            ((-3, -1, 0), -4, 4),
            ((6, 5, 1), 2, 6),
        )
    )
    cmp = compare_kernel_horizons(12, 16, 4)
    blocks = kernel_targeted_blocks(12, 8, 4)
    gcd_one = all(gcd_adjoint(sys, n) == 1 for n in range(2, 17))
    return {
        "dets": {
            "all_match_closed_form": dets["all_match_closed_form"],
            "all_nonzero": dets["all_nonzero"],
            "n2": dets["rows"][0]["det"],
            "n3": dets["rows"][1]["det"],
        },
        "inversion_on_samples": invert_ok,
        "homogeneous_on_samples": hom_ok,
        "complementary_step_on_samples": step_ok,
        "gcd_u_n_is_one": gcd_one,
        "horizons": cmp,
        "blocks": {
            "seed": blocks.get("seed"),
            "expanding_live_count": blocks.get("expanding_live_count"),
            "two_repeat_live_count": blocks.get("two_repeat_live_count"),
            "symbolic_family": blocks.get("symbolic_family"),
        },
        KNOWN_PACKAGING: True,
        HOMOGENEOUS_IS_STEP_ZERO: True,
        NORMALIZED_NOT_COORDINATE: True,
        GROWTH_NOT_INFINITUDE: True,
    }
