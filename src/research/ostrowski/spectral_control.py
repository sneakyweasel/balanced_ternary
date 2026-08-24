"""Origin residual as a bounded-control convolution of an expanding linear system.

From the origin, ``T_w(s) = A s − e₃ w`` unfolds to

    s_k = −∑_{j<k} A^{k−1−j} e₃ w_j = −∑_{r<k} h_r w_{k−1−r}

with impulse ``h_r = A^r e₃ = (3 q_{r−1}, 3 q_{r−2}+q_{r−1}, q_r)``.
This is KNOWN variation of constants / place-value dictionary, not an
``L_0`` bound. Energy of the same particular is ``energy_telescope`` /
``consumed_sum``.

The companion embedding ``z = s₁ + s₂ λ + s₃ λ²`` in
``Z[λ]/(λ³−2λ²−λ−3)`` satisfies ``z(T_w s) = λ z(s) − λ² w``.
All three embeddings have ``|λ_j|>1`` (non-Pisot). Normalized
``|λ|^{-k}|z|`` bounded is not residual boundedness. Large ``|s|``
does not force unique Ext: Ext is the energy slab, not a residual bound.
"""

from __future__ import annotations

from collections import deque

from research.ostrowski.control_language import matrix_power
from research.ostrowski.energy_trajectory import apply_word, consumed_sum
from research.ostrowski.ext_feasibility import live_ext
from research.ostrowski.live_growth import legal_w, residual_is_live
from research.ostrowski.live_layers import ORIGIN, energy_canonical, forward_layers, linf
from research.ostrowski.spectral import cubic_roots
from research.ostrowski.spectral_residual import apply_matrix, residual_matrix, transition_affine
from research.ostrowski.system import characteristic_poly_coeffs, nonpisot_order3

State3 = tuple[int, int, int]
StatePos = tuple[State3, int]
Triple = tuple[int, int, int]
E3: State3 = (0, 0, 1)

GROWTH_NOT_INFINITUDE = "finite_depth_is_not_infinitude"
NORMALIZED_NOT_RESIDUAL = "normalized_mode_bound_is_not_residual_bound"
KNOWN_PACKAGING = "convolution_is_variation_of_constants"
THREE_EXPANDING = "three_expanding_modes_versus_one_slab"
IMPULSE_IS_PLACE = "impulse_is_place_value"
EXT_NOT_UNIQUE = "large_s_does_not_force_unique_ext"
SCALAR_FORCING = "scalar_recurrence_has_local_forcing"

# N=12 remaining-0 maximizer. Finite depth, not a family.
N12_MAXIMIZER_WORD: tuple[int, ...] = (2, -4, -4, 0, 0, -4, 1, 1, -4, 1, 1, -2)
N12_MAXIMIZER_STATE: State3 = (-27, -6, 0)


def _sys():
    return nonpisot_order3()


def _sub(s: State3, t: State3) -> State3:
    return (s[0] - t[0], s[1] - t[1], s[2] - t[2])


def _smul(k: int, s: State3) -> State3:
    return (k * s[0], k * s[1], k * s[2])


def q_shift(index: int) -> int:
    """``q_i`` with value ``0`` for ``i<0``."""
    return _sys().place_value(index)


def place_impulse(r: int) -> State3:
    """``h_r = (3 q_{r−1}, 3 q_{r−2}+q_{r−1}, q_r)``. Underflow is 0."""
    if r < 0:
        raise ValueError("impulse index must be nonnegative")
    q1 = q_shift(r - 1)
    q2 = q_shift(r - 2)
    return (3 * q1, 3 * q2 + q1, q_shift(r))


def matrix_impulse(r: int) -> State3:
    """``h_r = A^r e₃`` by integer matrix power."""
    sys = _sys()
    return apply_matrix(matrix_power(residual_matrix(sys), r), E3)


def iterate_a(state: State3, r: int) -> State3:
    """Homogeneous ``A^r s`` as ``r`` steps of ``T_0``."""
    sys = _sys()
    out = state
    for _ in range(r):
        out = transition_affine(sys, out, 0)
    return out


def impulse_matches_place(r: int) -> bool:
    return matrix_impulse(r) == place_impulse(r) == iterate_a(E3, r)


def control_convolution(word: tuple[int, ...]) -> State3:
    """``s_k = −∑_{j<k} A^{k−1−j} e₃ w_j``. MSD: ``word[0]`` is applied first."""
    acc: State3 = ORIGIN
    k = len(word)
    for j, w in enumerate(word):
        acc = _sub(acc, _smul(w, matrix_impulse(k - 1 - j)))
    return acc


def control_convolution_reindexed(word: tuple[int, ...]) -> State3:
    """``s_k = −∑_{r<k} h_r w_{k−1−r}`` with ``h_r`` the place impulse."""
    acc: State3 = ORIGIN
    k = len(word)
    for r in range(k):
        acc = _sub(acc, _smul(word[k - 1 - r], place_impulse(r)))
    return acc


def convolution_matches_apply_word(word: tuple[int, ...]) -> bool:
    sys = _sys()
    from_apply = apply_word(sys, ORIGIN, word)
    return (
        control_convolution(word) == from_apply
        and control_convolution_reindexed(word) == from_apply
    )


def energy_of_particular_holds(start_remaining: int, word: tuple[int, ...]) -> bool:
    """From the origin, ``E_{N−k}(s_k) = −consumed_sum``."""
    if len(word) > start_remaining:
        return False
    sys = _sys()
    state = control_convolution(word)
    left = energy_canonical(sys, state, start_remaining - len(word))
    right = -consumed_sum(sys, start_remaining, word)
    return left == right


def ostrowski_s3(word: tuple[int, ...]) -> int:
    """``s_k^{(3)} = −∑_{r<k} q_r w_{k−1−r}``."""
    k = len(word)
    return -sum(q_shift(r) * word[k - 1 - r] for r in range(k))


def ostrowski_s1(word: tuple[int, ...]) -> int:
    """``s_k^{(1)} = −3 ∑_{r<k} q_{r−1} w_{k−1−r}``."""
    k = len(word)
    return -3 * sum(q_shift(r - 1) * word[k - 1 - r] for r in range(k))


def scalar_forcing(w_k: int, w_k1: int, w_k2: int) -> State3:
    """Local Cayley–Hamilton forcing ``F = (−3 w_{k+1}, −3 w_k − w_{k+1}, −w_{k+2})``."""
    return (-3 * w_k1, -3 * w_k - w_k1, -w_k2)


def scalar_forcing_holds(word: tuple[int, ...]) -> bool:
    """Cayley–Hamilton forcing along ``apply_word`` from the origin."""
    if len(word) < 3:
        return True
    sys = _sys()
    states: list[State3] = [ORIGIN]
    acc = ORIGIN
    for w in word:
        acc = transition_affine(sys, acc, w)
        states.append(acc)
    for k in range(len(word) - 2):
        s0, s1, s2, s3 = states[k], states[k + 1], states[k + 2], states[k + 3]
        w_k = word[k]
        w_k1 = word[k + 1]
        w_k2 = word[k + 2]
        force = scalar_forcing(w_k, w_k1, w_k2)
        predicted = (
            2 * s2[0] + s1[0] + 3 * s0[0] + force[0],
            2 * s2[1] + s1[1] + 3 * s0[1] + force[1],
            2 * s2[2] + s1[2] + 3 * s0[2] + force[2],
        )
        if predicted != s3:
            return False
    return True


def impulse_recurrence_holds(r: int) -> bool:
    """Each coordinate of ``h_r`` obeys the place-value recurrence."""
    h0 = place_impulse(r)
    h1 = place_impulse(r + 1)
    h2 = place_impulse(r + 2)
    h3 = place_impulse(r + 3)
    predicted = (
        2 * h2[0] + h1[0] + 3 * h0[0],
        2 * h2[1] + h1[1] + 3 * h0[1],
        2 * h2[2] + h1[2] + 3 * h0[2],
    )
    return predicted == h3


def large_s_ext_not_unique() -> dict[str, object]:
    """Ext depends on the energy slab. Large ``|s|`` is not unique control."""
    sys = _sys()
    word = N12_MAXIMIZER_WORD
    start = 12
    witnesses: list[dict[str, object]] = []
    acc = ORIGIN
    remaining = start
    if live_ext(acc, remaining) and len(live_ext(acc, remaining)) > 1:
        witnesses.append(
            {
                "remaining": remaining,
                "state": acc,
                "linf": linf(acc),
                "ext": live_ext(acc, remaining),
            }
        )
    for w in word:
        acc = transition_affine(sys, acc, w)
        remaining -= 1
        if remaining < 1:
            break
        ext = live_ext(acc, remaining)
        if linf(acc) >= 8 and len(ext) > 1:
            witnesses.append(
                {
                    "remaining": remaining,
                    "state": acc,
                    "linf": linf(acc),
                    "ext": ext,
                }
            )
    return {
        "word": word,
        "final": acc,
        "witnesses": witnesses,
        "refuted": len(witnesses) > 0,
        EXT_NOT_UNIQUE: True,
    }


def mul_lambda(z: Triple) -> Triple:
    """Multiply by ``λ`` in ``Z[λ]/(λ³ = 2λ² + λ + 3)``."""
    a, b, c = z
    return (3 * c, a + c, b + 2 * c)


def z_of_state(state: State3) -> Triple:
    """Companion embedding ``s₁ + s₂ λ + s₃ λ²``."""
    return state


def z_after_step(z: Triple, w: int) -> Triple:
    """``λ z − λ² w``."""
    return _sub(mul_lambda(z), (0, 0, w))


def z_step_holds(state: State3, w: int) -> bool:
    sys = _sys()
    nxt = transition_affine(sys, state, w)
    return z_of_state(nxt) == z_after_step(z_of_state(state), w)


def z_from_word(word: tuple[int, ...]) -> Triple:
    """``z_k = −λ² ∑_{j<k} λ^{k−1−j} w_j`` by iterating the recurrence."""
    z: Triple = ORIGIN
    for w in word:
        z = z_after_step(z, w)
    return z


def embedding_eval(z: Triple, lam: complex) -> complex:
    """Float diagnostic: evaluate ``a + b λ + c λ²``. Not a theorem."""
    return z[0] + z[1] * lam + z[2] * lam * lam


def field_coeff_norm(z: Triple) -> int:
    """Sup-norm of coefficients. Exact. Equals ``linf`` of the state."""
    return max(abs(z[0]), abs(z[1]), abs(z[2]))


def all_embeddings_expanding() -> dict[str, object]:
    """Non-Pisot: every ``|λ_j|>1``. Classification floats only."""
    coeffs = characteristic_poly_coeffs(_sys())
    assert coeffs is not None
    roots = cubic_roots(coeffs)
    moduli = tuple(abs(z) for z in roots)
    return {
        "moduli": moduli,
        "all_gt_one": all(m > 1 + 1e-9 for m in moduli),
        THREE_EXPANDING: True,
        NORMALIZED_NOT_RESIDUAL: True,
    }


def _prefix(
    parent: dict[StatePos, tuple[StatePos, int]], key: StatePos
) -> tuple[int, ...]:
    word: list[int] = []
    cur = key
    while cur in parent:
        prev, w = parent[cur]
        word.append(w)
        cur = prev
    word.reverse()
    return tuple(word)


def remaining_zero_live(start_remaining: int) -> dict[str, object]:
    """Origin-reachable remaining-0 live states with prefixes. Not infinitude."""
    sys = _sys()
    start: StatePos = (ORIGIN, start_remaining)
    seen: set[StatePos] = {start}
    queue: deque[StatePos] = deque([start])
    parent: dict[StatePos, tuple[StatePos, int]] = {}
    by_rem: dict[int, set[State3]] = {start_remaining: {ORIGIN}}
    while queue:
        state, remaining = queue.popleft()
        if remaining == 0:
            continue
        for w in legal_w(sys, remaining - 1):
            nxt = transition_affine(sys, state, w)
            nxt_rem = remaining - 1
            if not residual_is_live(sys, nxt, nxt_rem):
                continue
            key = (nxt, nxt_rem)
            if key in seen:
                continue
            seen.add(key)
            parent[key] = ((state, remaining), w)
            by_rem.setdefault(nxt_rem, set()).add(nxt)
            queue.append(key)
    l0 = set(by_rem.get(0, ()))
    if not l0:
        return {
            "N": start_remaining,
            "L0": 0,
            "max_linf": 0,
            "max_coeff_norm": 0,
            "maximizers": [],
        }
    max_l = max(linf(s) for s in l0)
    ranked = sorted(l0, key=lambda s: (linf(s), s[0], s[1], s[2]), reverse=True)
    maximizers = []
    for state in ranked:
        if linf(state) < max_l and len(maximizers) >= 4:
            break
        if linf(state) == max_l or len(maximizers) < 4:
            word = _prefix(parent, (state, 0))
            maximizers.append(
                {
                    "state": state,
                    "word": word,
                    "linf": linf(state),
                    "convolution_ok": control_convolution(word) == state,
                }
            )
        if len(maximizers) >= 4:
            break
    coeffs = characteristic_poly_coeffs(sys)
    assert coeffs is not None
    roots = cubic_roots(coeffs)
    max_embed = []
    for lam in roots:
        m = max(abs(embedding_eval(z_of_state(s), lam)) for s in l0)
        max_embed.append(m)
    k = start_remaining
    normalized = tuple(
        (max_embed[i] / (abs(roots[i]) ** k) if abs(roots[i]) else None)
        for i in range(3)
    )
    return {
        "N": start_remaining,
        "L0": len(l0),
        "max_linf": max_l,
        "max_coeff_norm": max_l,
        "max_embed_abs": tuple(max_embed),
        "normalized_embed_abs": normalized,
        "maximizers": maximizers,
        GROWTH_NOT_INFINITUDE: True,
        NORMALIZED_NOT_RESIDUAL: True,
        KNOWN_PACKAGING: True,
        THREE_EXPANDING: True,
    }


def compare_remaining_zero(n_small: int = 12, n_large: int = 16) -> dict[str, object]:
    small = remaining_zero_live(n_small)
    large = remaining_zero_live(n_large)
    z_grows = large["max_embed_abs"][0] > small["max_embed_abs"][0]
    coeff_grows = large["max_coeff_norm"] > small["max_coeff_norm"]
    words = [row["word"] for row in large["maximizers"]]
    periodic_looking = []
    for word in words:
        flag = False
        if len(word) >= 2 and len(set(word)) == 1:
            flag = True
        periodic_looking.append(flag)
    return {
        "small": {
            "N": small["N"],
            "L0": small["L0"],
            "max_linf": small["max_linf"],
            "max_embed_abs": small["max_embed_abs"],
            "normalized_embed_abs": small["normalized_embed_abs"],
            "maximizers": small["maximizers"],
        },
        "large": {
            "N": large["N"],
            "L0": large["L0"],
            "max_linf": large["max_linf"],
            "max_embed_abs": large["max_embed_abs"],
            "normalized_embed_abs": large["normalized_embed_abs"],
            "maximizers": large["maximizers"],
        },
        "unnormalized_z_grows": z_grows,
        "coeff_norm_grows": coeff_grows,
        "uniform_cancellation_refuted": z_grows or coeff_grows,
        "maximizer_all_constant": all(periodic_looking) if periodic_looking else False,
        "symbolic_family": False,
        GROWTH_NOT_INFINITUDE: True,
        NORMALIZED_NOT_RESIDUAL: True,
        KNOWN_PACKAGING: True,
        THREE_EXPANDING: True,
    }


def phase0_spectral_control() -> dict[str, object]:
    samples = (
        (),
        (0,),
        (-4, 2),
        (1, -3, 0, 2),
        (-4, -4, -4, 1, 1),
        N12_MAXIMIZER_WORD,
    )
    conv_ok = all(convolution_matches_apply_word(w) for w in samples)
    coords_ok = all(
        control_convolution(w)[0] == ostrowski_s1(w)
        and control_convolution(w)[2] == ostrowski_s3(w)
        for w in samples
    )
    impulse_ok = all(impulse_matches_place(r) for r in range(12))
    rec_ok = all(impulse_recurrence_holds(r) for r in range(8))
    force_ok = all(scalar_forcing_holds(w) for w in samples)
    z_ok = all(
        z_step_holds(s, w)
        for s, w in (
            (ORIGIN, 0),
            ((-3, -1, 0), -4),
            ((6, 5, 1), 2),
            ((15, 2, -2), -1),
        )
    )
    z_word_ok = all(z_from_word(w) == control_convolution(w) for w in samples)
    energy_ok = all(
        energy_of_particular_holds(16, w) for w in samples if len(w) <= 16
    )
    embeddings = all_embeddings_expanding()
    ext_report = large_s_ext_not_unique()
    layers_ok = True
    sys = _sys()
    fwd = forward_layers(sys, 12, live_only=True)
    s_max = fwd["layers"][0]["s_max"]
    prefix = fwd["layers"][0]["prefix"]
    if s_max is not None and prefix is not None:
        layers_ok = control_convolution(prefix) == s_max
    return {
        "convolution_on_samples": conv_ok,
        "ostrowski_coordinates": coords_ok,
        "impulse_is_place": impulse_ok,
        "impulse_recurrence": rec_ok,
        "scalar_forcing": force_ok,
        "z_step_on_samples": z_ok,
        "z_word_equals_convolution": z_word_ok,
        "energy_particular": energy_ok,
        "embeddings": embeddings,
        "ext_not_unique": ext_report,
        "layer_prefix_matches_convolution": layers_ok,
        KNOWN_PACKAGING: True,
        IMPULSE_IS_PLACE: True,
        SCALAR_FORCING: True,
        EXT_NOT_UNIQUE: True,
        NORMALIZED_NOT_RESIDUAL: True,
        GROWTH_NOT_INFINITUDE: True,
        THREE_EXPANDING: True,
    }
