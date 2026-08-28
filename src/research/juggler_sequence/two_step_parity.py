"""Multi-step itinerary-parity census on odd Juggler starts.

Phase-0 falsifier for the two-step parity discrepancy branch. Exact
integer counting only: does the joint parity word of the first four
itinerary letters on odd starts converge to the product densities,
and with what empirical discrepancy exponent?

Not a Research Engine control-layer experiment. Not a frequency
theorem, not a predictive-state claim (theta bins and residue states
stay REFUTED/CLOSE), and not a termination theorem. The census gated
the depth-2 analytic lemma; that lemma is now proved, and the depth-4
extension (triple parity discrepancy, OOEE density N/16, certified
four-step descent class 13/16) is proved as well (ledger rows
J-nested-parity-linearization, J-nested-parity-discrepancy,
J-fourth-letter-linearization, J-triple-parity-discrepancy,
J-four-step-descent-density; proofs in
docs/research/juggler_two_step_parity_lemma.md). This module also
hosts the exact validators used by both review passes.
"""

from __future__ import annotations

import json
from math import isqrt, log
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
JSON_PATH = REPO_ROOT / "docs" / "research" / "juggler_two_step_parity.json"
DOC_PATH = REPO_ROOT / "docs" / "research" / "juggler_two_step_parity.md"

N_MAX = 10_000_000
DEPTH = 4
COARSE_GRID = (
    10_000,
    100_000,
    1_000_000,
    *(1 << k for k in range(14, 24)),
    N_MAX,
)
ENVELOPE_RATIO = 1.06

WORDS4 = tuple(
    "O" + "".join(w)
    for w in (
        (a, b, c)
        for a in "EO"
        for b in "EO"
        for c in "EO"
    )
)

# The only length-4 contracting continuation of an odd-to-odd start:
# 3^2 < 2^4 forces image^16 <= n^9, hence a four-step certificate.
CONTRACTING_TARGET = "OOEE"

ANTI_OVERCLAIM = {
    "global_termination": False,
    "parity_frequency_theorem": False,
    "predictive_state_claim": False,
    "reopen_landing_theta": False,
    "reopen_2adic_bridge": False,
    # Flipped by the Phase-2 review pass: Theorem C is EXACT — HUMAN
    # PROOF (ledger row J-nested-parity-discrepancy). Ambient counting
    # only; the flags above stay False.
    "depth2_analytic_lemma_proved": True,
    # Flipped by the Phase-3 review pass: Theorem E and Corollary F
    # are EXACT — HUMAN PROOF (rows J-triple-parity-discrepancy,
    # J-four-step-descent-density). Even-branch fourth letter only;
    # the OOO* classes remain open.
    "depth4_even_branch_proved": True,
    # Phase 4: the conditional implication (equidistribution at all
    # depths => density-one descent) is a theorem. No unconditional
    # density-one claim (depth >= 5 equidistribution is open).
    "tier2_analytic_lemma_proved": True,
    "density_one_claimed": False,
    # Phase 5: Proposition L closes the OE-branch third letter, so all
    # depth-3 word classes are proved.
    "depth3_words_proved": True,
    # Phases 8-9: the tier-2 kernel bound (Theorem R, formerly
    # Conjecture O) is EXACT — HUMAN PROOF after the Phase-9
    # adversarial review (row J-kernel-cancellation), and Theorem S
    # closes OOO*: depth-4 equidistribution is complete
    # (row J-depth4-complete).
    "kernel_bound_proved": True,
    # Phase 6: Theorem Q closes the OE** splits (growing layer on the
    # slow variable w).
    "depth4_slow_branch_proved": True,
    # Phase 8 draft, upgraded by the Phase-9 review.
    "kernel_double_differencing_draft": True,
    "depth4_complete_proved": True,
    # Phase 10: Theorem T / Corollary U close OOOEE and OOEOE;
    # certified descent density 7/8. OOOO* at depth 5 remains open.
    "depth5_contracting_proved": True,
    # Phase 11: the OOOO* fifth letter is the isolated level-3
    # floor-defect kernel K3 (Lemma V1). No bound, no density move.
    "depth5_kernel_isolated": True,
    "depth5_kernel_bound_proved": False,
    # Phase 12: copying Theorem R to K3 is REFUTED (no v-level
    # b-runs; forced inner linearization produces α = 45/16).
    "scale_invariant_R_extension_refuted": True,
    # Phase 13: OOEOOEE and OOOEOEE close under the engine + R at
    # alpha <= 9/8; certified descent density 57/64. OOOOEEE still
    # needs K3.
    "depth7_engine_contracting_proved": True,
    # Phase 14: differencing K3 first, then increment-linearizing
    # on X-cell b-runs, is REFUTED (no J-runs on those cells;
    # unfreezing J reintroduces α = 45/16).
    "increment_first_k3_refuted": True,
}


def juggler_step(x: int) -> int:
    if x % 2 == 1:
        return isqrt(x * x * x)
    return isqrt(x)


# --- Phase 1: exact validation of the linearization and gap structure ---

SCALE = 10**30


def _sqrt_scaled(x: int, scale: int = SCALE) -> int:
    """floor(sqrt(x) * scale) in exact integer arithmetic."""
    return isqrt(x * scale * scale)


def _quartic_scaled(x: int, scale: int = SCALE) -> int:
    """floor(x^{1/4} * scale) in exact integer arithmetic."""
    return isqrt(isqrt(x * scale**4))


def identity_error_scaled(n: int, scale: int = SCALE) -> tuple[int, int]:
    """(E(n)*scale, bound*scale) for the exact linearization at odd n.

    Lemma A: m^{3/2} = (3/2) m n^{3/4} - (1/2) n^{9/4} + E(n) with
    0 <= E(n) <= (3/8) (n^{3/2}-1)^{-1/2} <= (1/2) n^{-3/4}, where
    m = floor(n^{3/2}). Returned values carry integer-rounding slack of
    a few units times m, negligible at this scale.
    """
    if n < 3 or n % 2 == 0:
        raise ValueError("odd n >= 3 required")
    m = isqrt(n**3)
    m32 = _sqrt_scaled(m**3, scale)
    n94 = _quartic_scaled(n**9, scale)
    n34 = _quartic_scaled(n**3, scale)
    err = m32 + n94 // 2 - (3 * m * n34) // 2
    bound = (scale * scale) // (2 * n34)
    return err, bound


def identity_scan(samples: tuple[int, ...]) -> dict[str, Any]:
    """Check 0 <= E(n) <= (1/2) n^{-3/4} on the given odd samples."""
    slack_units = 8
    worst_ratio = 0.0
    for n in samples:
        err, bound = identity_error_scaled(n)
        m = isqrt(n**3)
        slack = slack_units * max(m, 1)
        if err < -slack or err > bound + slack:
            return {"holds": False, "witness": n}
        if bound > 0:
            worst_ratio = max(worst_ratio, err / bound)
    return {"holds": True, "count": len(samples), "worst_ratio": round(worst_ratio, 6)}


def smooth_cancellation_check(n: int, h: int) -> float:
    """|A1''(n)| * n^{7/4} / h^2 for the smooth difference part (j = 1).

    A1(n) = -(1/4)[(n+2h)^{9/4} - n^{9/4}]
            + (3/4) n^{3/2} [(n+2h)^{3/4} - n^{3/4}].
    The leading n^{5/4}-scale terms cancel, leaving A1'' = O(h^2 n^{-7/4});
    this returns the normalized ratio via an exact scaled second
    difference (step 2), which must stay O(1).
    """
    scale = SCALE

    def a1_scaled(x: int) -> int:
        q9 = _quartic_scaled(x**9, scale)
        q9h = _quartic_scaled((x + 2 * h) ** 9, scale)
        q34 = _quartic_scaled(x**3, scale)
        q34h = _quartic_scaled((x + 2 * h) ** 3, scale)
        s32 = _sqrt_scaled(x**3, scale)
        return -(q9h - q9) // 4 + (3 * s32 * (q34h - q34)) // (4 * scale)

    d2 = a1_scaled(n + 2) - 2 * a1_scaled(n) + a1_scaled(n - 2)
    n74 = _quartic_scaled(n**7, scale)
    # A1'' ~ d2 / (4 * scale); ratio = |A1''| n^{7/4} / h^2.
    return abs(d2) * n74 / (4 * scale * scale * h * h)


def _eighth_scaled(x: int, scale: int = SCALE) -> int:
    """floor(x^{1/8} * scale) in exact integer arithmetic."""
    return isqrt(isqrt(isqrt(x * scale**8)))


def fourth_letter_smoothing_check(n: int, scale: int = SCALE) -> tuple[int, int]:
    """(D(n)*scale, bound*scale) for the fourth-letter linearization.

    Lemma D: v^{1/2} = n^{9/8} + D(n) with
    -(3/4) n^{-3/8} - n^{-9/8} <= D(n) <= 0, where m = floor(n^{3/2}),
    v = floor(m^{3/2}). Composition of the exact linearizations of
    m^{3/4} and (m^{3/2} - theta_2)^{1/2}; all amplitudes decay.
    """
    if n < 3 or n % 2 == 0:
        raise ValueError("odd n >= 3 required")
    m = isqrt(n**3)
    v = isqrt(m**3)
    v12 = _sqrt_scaled(v, scale)
    n98 = _eighth_scaled(n**9, scale)
    diff = v12 - n98
    n38 = _eighth_scaled(n**3, scale)
    bound = (3 * scale * scale) // (4 * n38) + (scale * scale) // n98
    return diff, bound


def fourth_letter_scan(samples: tuple[int, ...]) -> dict[str, Any]:
    """Check -(3/4) n^{-3/8} - n^{-9/8} <= D(n) <= 0 on odd samples."""
    slack = 8
    worst_ratio = 0.0
    for n in samples:
        diff, bound = fourth_letter_smoothing_check(n)
        if diff > slack or diff < -bound - slack:
            return {"holds": False, "witness": n}
        if bound > 0:
            worst_ratio = max(worst_ratio, -diff / bound)
    return {"holds": True, "count": len(samples), "worst_ratio": round(worst_ratio, 6)}


def ooee_indicator_identity_check(n_max: int) -> dict[str, Any]:
    """Exact branch-consistency check of the OOEE sign algebra.

    itinerary_word(n, 4) == 'OOEE' iff ((-1)^m, (-1)^v, (-1)^isqrt(v))
    equals (-1, +1, +1) with m = isqrt(n^3), v = isqrt(m^3): the
    (1+psi_2) factor restricts to even v, exactly where J^3 takes the
    even branch, so psi_3 may be evaluated unconditionally.
    """
    for n in range(3, n_max + 1, 2):
        m = isqrt(n**3)
        v = isqrt(m**3)
        signs = (m % 2 == 1, v % 2 == 0, isqrt(v) % 2 == 0)
        if (itinerary_word(n, 4) == "OOEE") != all(signs):
            return {"holds": False, "witness": n}
    return {"holds": True, "n_max": n_max}


def deep_word_counts(n_max: int, depth: int) -> dict[str, int]:
    """Exact census of length-`depth` itinerary words on odd starts."""
    counts: dict[str, int] = {}
    for n in range(3, n_max + 1, 2):
        w = itinerary_word(n, depth)
        counts[w] = counts.get(w, 0) + 1
    return dict(sorted(counts.items()))


# --- Phase 6: the OEO* split (growing layer on the slow variable) ---


def lemma_a_prime_check(n: int, scale: int = SCALE) -> tuple[int, int]:
    """(E*scale, bound*scale) for the w-level linearization (Lemma A').

    With m = floor(n^{3/2}), U = m^{1/2}, w = floor(U), theta_w = U - w:
    w^{3/2} = -(1/2) m^{3/4} + (3/2) w m^{1/4} + E,
    0 <= E <= (3/8)(U-1)^{-1/2}. Since U m^{1/4} = m^{3/4} exactly, this
    rearranges to w^{3/2} = m^{3/4} - (3/2) m^{1/4} theta_w + E: the
    entire OEO* fourth-letter phase is one decaying-smooth term plus
    one growing sawtooth of amplitude (3/2) m^{1/4} ~ n^{3/8}.
    """
    if n < 5 or n % 2 == 0:
        raise ValueError("odd n >= 5 required")
    m = isqrt(n**3)
    w = isqrt(m)
    lhs = isqrt(w**3 * scale * scale)
    r34m = isqrt(isqrt(m**3 * scale**4))
    r14m = isqrt(isqrt(m * scale**4))
    poly = -r34m // 2 + 3 * w * r14m // 2
    bound = 3 * scale // (8 * isqrt(w - 1))
    return lhs - poly, bound


def lemma_a_prime_scan(samples: tuple[int, ...]) -> dict[str, Any]:
    for n in samples:
        diff, bound = lemma_a_prime_check(n)
        if not (-4 * n <= diff <= bound + 4 * n):
            return {"holds": False, "witness": n}
    return {"holds": True, "count": len(samples)}


def oeo_smoothing_check(n: int, scale: int = SCALE) -> tuple[int, int, int]:
    """(d2*scale, lo*scale, hi*scale) for the full OEO* smoothing.

    d2 = w^{3/2} - n^{9/8} + (3/2) m^{1/4} theta_w collects Lemma A'
    plus the m^{3/4} -> n^{9/8} substitution:
    -(3/4) n^{-3/8} - (3/32)(X-1)^{-5/4} <= d2 <= (3/8)(U-1)^{-1/2}.
    All error terms decay, so the phase (k/2) w^{3/2} equals
    (k/2) n^{9/8} - (3k/4) m^{1/4} theta_w + absorbable.
    """
    if n < 5 or n % 2 == 0:
        raise ValueError("odd n >= 5 required")
    m = isqrt(n**3)
    w = isqrt(m)
    t_w = isqrt(w**3 * scale * scale)
    r98 = _eighth_scaled(n**9, scale)
    r38 = _eighth_scaled(n**3, scale)
    r14m = isqrt(isqrt(m * scale**4))
    th_w = isqrt(m * scale * scale) - w * scale
    d2 = t_w - r98 + 3 * (r14m * th_w) // (2 * scale)
    lo = -(3 * scale * scale) // (4 * r38)
    hi = 3 * scale // (8 * isqrt(w - 1))
    return d2, lo, hi


def oeo_smoothing_scan(samples: tuple[int, ...]) -> dict[str, Any]:
    for n in samples:
        d2, lo, hi = oeo_smoothing_check(n)
        if not (lo - 4 * n <= d2 <= hi + 4 * n):
            return {"holds": False, "witness": n}
    return {"holds": True, "count": len(samples)}


def oeo_indicator_identity_check(n_max: int) -> dict[str, Any]:
    """Branch consistency for all four OE** depth-4 words.

    For odd n with m = floor(n^{3/2}) even and w = isqrt(m): the word
    is 'OE' + parity(w) + parity(isqrt(w^3) if w odd else isqrt(w)).
    The (1-(-1)^w)/2 factor vanishes exactly where J^3 would take the
    even branch, so psi(w^{3/2}) evaluates unconditionally.
    """
    checked = 0
    for n in range(3, n_max + 1, 2):
        m = isqrt(n**3)
        if m % 2 == 1:
            continue
        w = isqrt(m)
        if w % 2 == 1:
            fourth = isqrt(w**3)
        else:
            fourth = isqrt(w)
        expected = (
            "OE"
            + ("O" if w % 2 == 1 else "E")
            + ("O" if fourth % 2 == 1 else "E")
        )
        if itinerary_word(n, 4) != expected:
            return {"holds": False, "witness": n}
        checked += 1
    return {"holds": True, "checked": checked, "n_max": n_max}


def _sixteenth_scaled(x: int, scale: int = SCALE) -> int:
    """floor(x^{1/16} * scale) via four nested isqrts."""
    return isqrt(isqrt(isqrt(isqrt(x * scale**16))))


def oooee_smoothing_check(n: int, scale: int = SCALE) -> tuple[int, int]:
    """(d5*scale, bound*scale) for the OOOE* fifth-letter smoothing.

    z = floor(v^{3/2}), v = floor(m^{3/2}), m = floor(n^{3/2}):
    z^{1/2} = n^{27/16} - (9/8) n^{3/16} theta + D5, with D5 decaying
    (the theta_2 and theta_z amplitudes are O(n^{-9/16})). The only
    growing sawtooth has coefficient n^{3/16} < n — engine side.
    """
    if n < 5 or n % 2 == 0:
        raise ValueError("odd n >= 5 required")
    m = isqrt(n**3)
    v = isqrt(m**3)
    z = isqrt(v**3)
    z12 = isqrt(z * scale * scale)
    r27 = _sixteenth_scaled(n**27, scale)
    r3 = _sixteenth_scaled(n**3, scale)
    th = isqrt(n**3 * scale * scale) - m * scale
    d5 = z12 - r27 + 9 * (r3 * th) // (8 * scale)
    # Decaying envelope: (3/4) m^{-3/8} + (1/2) v^{-3/4} + (9/128) n^{-7/16}.
    r38m = isqrt(isqrt(isqrt(m**3 * scale**8)))
    r34v = isqrt(isqrt(v**3 * scale**4))
    r7 = _sixteenth_scaled(n**7, scale)
    bound = 3 * scale * scale // (4 * r38m) + scale * scale // (2 * r34v) + 9 * scale * scale // (128 * r7)
    return d5, bound


def oooee_smoothing_scan(samples: tuple[int, ...]) -> dict[str, Any]:
    for n in samples:
        d5, bound = oooee_smoothing_check(n)
        if not (-bound - 8 * n <= d5 <= bound + 8 * n):
            return {"holds": False, "witness": n, "d5": d5, "bound": bound}
    return {"holds": True, "count": len(samples)}


def ooeoe_smoothing_check(n: int, scale: int = SCALE) -> tuple[int, int]:
    """(d5*scale, bound*scale) for the OOEO* fifth-letter linearization.

    w = floor(v^{1/2}), v = floor(m^{3/2}): Lemma A' at the w-level
    plus the v^{3/4} -> n^{27/16} chain gives
    w^{3/2} = n^{27/16} - (9/8) n^{3/16} theta - (3/2) v^{1/4} theta_w + D,
    D decaying. Two engine sawtooths: coeff n^{3/16} (theta) and
    n^{9/16} (theta_w); both grow slower than n.
    """
    if n < 5 or n % 2 == 0:
        raise ValueError("odd n >= 5 required")
    m = isqrt(n**3)
    v = isqrt(m**3)
    w = isqrt(v)
    t_w = isqrt(w**3 * scale * scale)
    r27 = _sixteenth_scaled(n**27, scale)
    r3 = _sixteenth_scaled(n**3, scale)
    th = isqrt(n**3 * scale * scale) - m * scale
    r14v = isqrt(isqrt(v * scale**4))
    th_w = isqrt(v * scale * scale) - w * scale
    d5 = t_w - r27 + 9 * (r3 * th) // (8 * scale) + 3 * (r14v * th_w) // (2 * scale)
    r38m = isqrt(isqrt(isqrt(m**3 * scale**8)))
    bound = 3 * scale * scale // (4 * r38m) + 3 * scale // (8 * isqrt(max(w, 2) - 1))
    return d5, bound


def ooeoe_smoothing_scan(samples: tuple[int, ...]) -> dict[str, Any]:
    for n in samples:
        d5, bound = ooeoe_smoothing_check(n)
        if not (-bound - 8 * n <= d5 <= bound + 8 * n):
            return {"holds": False, "witness": n, "d5": d5, "bound": bound}
    return {"holds": True, "count": len(samples)}


def oooee_indicator_identity_check(n_max: int) -> dict[str, Any]:
    """Branch consistency: OOOE* fifth letter is parity of isqrt(z)."""
    checked = 0
    for n in range(3, n_max + 1, 2):
        word = itinerary_word(n, 5)
        if not word.startswith("OOOE"):
            continue
        m = isqrt(n**3)
        v = isqrt(m**3)
        z = isqrt(v**3)
        expected = "OOOE" + ("O" if isqrt(z) % 2 == 1 else "E")
        if word != expected:
            return {"holds": False, "witness": n}
        checked += 1
    return {"holds": True, "checked": checked, "n_max": n_max}


def ooeoe_indicator_identity_check(n_max: int) -> dict[str, Any]:
    """Branch consistency: OOEO* fifth letter is parity of isqrt(w^3)."""
    checked = 0
    for n in range(3, n_max + 1, 2):
        word = itinerary_word(n, 5)
        if not word.startswith("OOEO"):
            continue
        m = isqrt(n**3)
        v = isqrt(m**3)
        w = isqrt(v)
        expected = "OOEO" + ("O" if isqrt(w**3) % 2 == 1 else "E")
        if word != expected:
            return {"holds": False, "witness": n}
        checked += 1
    return {"holds": True, "checked": checked, "n_max": n_max}


def ooeoe_mode_probe(p_block: int) -> dict[str, Any]:
    """Float probe of sum e((1/2) w^{3/2}) on the OOEO cylinder, n ~ P."""
    from math import cos, pi, sin

    s = 10**12
    re = im = 0.0
    cnt = 0
    n = p_block + 1
    while n < 2 * p_block:
        m = isqrt(n**3)
        if m % 2 == 0:
            n += 2
            continue
        v = isqrt(m**3)
        if v % 2 == 1:
            n += 2
            continue
        w = isqrt(v)
        if w % 2 == 0:
            n += 2
            continue
        t_w = isqrt(w**3 * s * s)
        frac = (t_w % (2 * s)) / (2 * s)
        ph = 2 * pi * frac
        re += cos(ph)
        im += sin(ph)
        cnt += 1
        n += 2
    return {"count": cnt, "abs_sum": round((re * re + im * im) ** 0.5, 1)}


def oooee_mode_probe(p_block: int) -> dict[str, Any]:
    """Float probe of sum e((1/2) z^{1/2}) on the OOOE cylinder, n ~ P."""
    from math import cos, pi, sin

    s = 10**12
    re = im = 0.0
    cnt = 0
    n = p_block + 1
    while n < 2 * p_block:
        m = isqrt(n**3)
        if m % 2 == 0:
            n += 2
            continue
        v = isqrt(m**3)
        if v % 2 == 0:
            n += 2
            continue
        z = isqrt(v**3)
        if z % 2 == 1:
            n += 2
            continue
        t = isqrt(z * s * s)
        frac = (t % (2 * s)) / (2 * s)
        ph = 2 * pi * frac
        re += cos(ph)
        im += sin(ph)
        cnt += 1
        n += 2
    return {"count": cnt, "abs_sum": round((re * re + im * im) ** 0.5, 1)}


# --- Phase 11: OOOO* kernel isolation (level-3 floor defect) ---


def level3_reformulation_check(n: int, scale: int = 10**40) -> tuple[int, int]:
    """(diff*scale, bound*scale) for the level-3 kernel reformulation.

    With Z = v^{3/2}, z = floor(Z), theta_3 = Z - z:
    (1/2)(v^{9/4} - z^{3/2}) - (3/4) z^{1/2} theta_3 = R3 in
    [0, (3/16) z^{-1/2}] (Taylor of (z + theta_3)^{3/2} at z, one-signed
    remainder). Hence the central kernel phase c*theta_3 with
    c = (3k/4) z^{1/2} equals (k/2)(v^{9/4} - z^{3/2}) up to k R3:
    the OOOO* kernel is the exponential sum of the level-3 local
    floor defect. Lemma R1 with (m, v) replaced by (v, z).
    """
    if n < 5 or n % 2 == 0:
        raise ValueError("odd n >= 5 required")
    m = isqrt(n**3)
    v = isqrt(m**3)
    z = isqrt(v**3)
    v94 = isqrt(isqrt(v**9 * scale**4))
    z32 = isqrt(z**3 * scale * scale)
    z12 = isqrt(z * scale * scale)
    th3 = isqrt(v**3 * scale * scale) - z * scale
    diff = (v94 - z32) // 2 - (3 * z12 * th3) // (4 * scale)
    # Floor slack: z12 and th3 each carry O(1) scaled-unit error;
    # the cross product propagates them at z^{1/2} ~ n^{27/16} units.
    slack = isqrt(z) + 10**6
    bound = (3 * scale * scale) // (16 * z12) + slack
    return diff, bound


def level3_reformulation_scan(samples: tuple[int, ...]) -> dict[str, Any]:
    """Check 0 <= diff <= bound on odd samples (slack folded into bound)."""
    slack = 10**7
    for n in samples:
        diff, bound = level3_reformulation_check(n)
        if diff < -slack or diff > bound:
            return {"holds": False, "witness": n}
    return {"holds": True, "count": len(samples)}


def _level3_phase_scaled(n: int, coeff_num: int, coeff_den: int) -> float:
    """{c(n) theta_3(n)} with c = (num/den) z^{1/2}, exact scaled ints."""
    s = 10**12
    s30 = 10**30
    v = isqrt(isqrt(n**3) ** 3)
    z = isqrt(v**3)
    t3 = isqrt(v**3 * s * s)
    th3 = t3 - (t3 // s) * s
    z12 = isqrt(z * s30 * s30)
    prod = (coeff_num * z12 * th3) // coeff_den
    return (prod % (s30 * s)) / (s30 * s)


def level3_kernel_probe(
    p_block: int, coeff_num: int = 3, coeff_den: int = 4
) -> dict[str, Any]:
    """Float probe of the isolated level-3 kernel K3 = sum e(c {v^{3/2}}).

    c(n) = (coeff_num/coeff_den) z^{1/2}, the natural z^{1/2}-scale of
    the OOOO* reduction (z = floor(v^{3/2}) ~ n^{27/8}, so
    c ~ n^{27/16}). Exact scaled phase arithmetic; float only in the
    final exponential. Not a proof; supports or refutes Conjecture V.
    """
    from math import cos, pi, sin

    re = im = 0.0
    cnt = 0
    n = p_block + 1
    while n < 2 * p_block:
        frac = _level3_phase_scaled(n, coeff_num, coeff_den)
        ph = 2 * pi * frac
        re += cos(ph)
        im += sin(ph)
        cnt += 1
        n += 2
    return {"count": cnt, "abs_sum": round((re * re + im * im) ** 0.5, 1)}


def differenced_level3_kernel_probe(
    p_block: int,
    h1: int,
    h2: int = 0,
    h3: int = 0,
    coeff_num: int = 3,
    coeff_den: int = 4,
) -> dict[str, Any]:
    """Once-, twice- or thrice-differenced level-3 kernel sums.

    Same corner construction as differenced_kernel_probe; phase is
    c theta_3 with c = (coeff_num/coeff_den) z^{1/2}. Not a proof.
    """
    from math import cos, pi, sin

    corners = [(1, 2 * h1), (-1, 0)]
    for h in (h2, h3):
        if h > 0:
            corners = [(s, d + 2 * h) for s, d in corners] + [
                (-s, d) for s, d in corners
            ]
    re = im = 0.0
    cnt = 0
    n = p_block + 1
    while n < 2 * p_block:
        ph = 0.0
        for sgn, d in corners:
            ph += sgn * _level3_phase_scaled(n + d, coeff_num, coeff_den)
        theta = 2 * pi * ph
        re += cos(theta)
        im += sin(theta)
        cnt += 1
        n += 2
    return {
        "count": cnt,
        "abs_sum": round((re * re + im * im) ** 0.5, 1),
        "sqrt_count": round(cnt**0.5, 1),
    }


def level3_raw_gap_wildness(p_block: int, window: int = 80) -> dict[str, Any]:
    """Raw third/fourth differences of Z = v^{3/2} are not frozen.

    The smooth model G(n) = n^{27/8} has G''' ≍ P^{3/8} ≫ 1 and
    G^{(4)} ≍ P^{-5/8} ≪ 1, so three Weyl steps freeze the smooth
    content. The discrete Z inherits jumps from both inner floors
    (m and v), and |Δ⁴ Z| stays ≫ 1 — the Phase-8 raw-freeze
    falsifier one layer up. A freeze argument that ignores the
    nested carry lattice is dead on arrival.
    """
    s = 10**12
    step = 2

    def z_real(x: int) -> float:
        v = isqrt(isqrt(x**3) ** 3)
        return isqrt(v**3 * s * s) / s

    d3s: list[float] = []
    d4s: list[float] = []
    n = p_block + 1
    for _ in range(window):
        vals = [z_real(n + k * step) for k in range(5)]
        d3s.append(abs(vals[3] - 3 * vals[2] + 3 * vals[1] - vals[0]))
        d4s.append(
            abs(vals[4] - 4 * vals[3] + 6 * vals[2] - 4 * vals[1] + vals[0])
        )
        n += 2
    d3_mean = sum(d3s) / len(d3s)
    d4_mean = sum(d4s) / len(d4s)
    pred3 = (27 / 8) * (19 / 8) * (11 / 8) * p_block ** (3 / 8) * step**3
    return {
        "window": window,
        "d3_mean": round(d3_mean, 3),
        "d4_mean": round(d4_mean, 3),
        "smooth_d3_pred": round(pred3, 3),
        "raw_d4_wild": d4_mean > 1.0,
        "d3_above_smooth": d3_mean > 10 * pred3,
    }


def oooo_indicator_identity_check(n_max: int) -> dict[str, Any]:
    """Branch consistency: OOOO* fifth letter is parity of isqrt(z^3)."""
    checked = 0
    for n in range(3, n_max + 1, 2):
        word = itinerary_word(n, 5)
        if not word.startswith("OOOO"):
            continue
        m = isqrt(n**3)
        v = isqrt(m**3)
        z = isqrt(v**3)
        expected = "OOOO" + ("O" if isqrt(z**3) % 2 == 1 else "E")
        if word != expected:
            return {"holds": False, "witness": n}
        checked += 1
    return {"holds": True, "checked": checked, "n_max": n_max}


def level3_inner_linearization_check(
    n: int, scale: int = 10**40
) -> tuple[int, int]:
    """(E*scale, bound*scale) for the forced inner linearization (V2).

    v^{3/2} = m^{9/4} - (3/2) m^{3/4} theta_2 + E, with
    0 ≤ E ≤ (3/8) v^{-1/2} (Taylor of (Y - theta_2)^{3/2} at Y).
    The main term produces the W-family phase C theta_2 with
    C = (3c/2) m^{3/4} ≍ k n^{45/16} once the outer coefficient
    c ≍ k z^{1/2} is restored — past the engine line α = 9/4 of
    Theorem R's Step-3 θ-coefficients.
    """
    if n < 5 or n % 2 == 0:
        raise ValueError("odd n >= 5 required")
    m = isqrt(n**3)
    v = isqrt(m**3)
    v32 = isqrt(v**3 * scale * scale)
    m94 = isqrt(isqrt(m**9 * scale**4))
    m34 = isqrt(isqrt(m**3 * scale**4))
    th2 = isqrt(m**3 * scale * scale) - v * scale
    err = v32 - m94 + (3 * m34 * th2) // (2 * scale)
    v12 = isqrt(v * scale * scale)
    slack = isqrt(v) + 10**6
    bound = (3 * scale * scale) // (8 * v12) + slack
    return err, bound


def level3_inner_linearization_scan(samples: tuple[int, ...]) -> dict[str, Any]:
    slack = 10**7
    for n in samples:
        err, bound = level3_inner_linearization_check(n)
        if err < -slack or err > bound:
            return {"holds": False, "witness": n}
    return {"holds": True, "count": len(samples)}


def v_level_cell_scan(p_block: int, window: int = 400) -> dict[str, Any]:
    """Run lengths of floor(ΔY) and Δv at step 2.

    Theorem R needs b-runs of floor(ΔX) of length ≍ P^{1/2}/h.
    The v-level analogue — runs of floor(ΔY) or of Δv — has mean
    length 1 at every tested scale: Y' ≍ P^{5/4} so the first
    difference of Y changes by ≍ P^{1/4} ≫ 1 at every step.
    A copy of Lemma R3 at the v-level cannot even be stated.
    """
    s = 10**12

    def y_scaled(x: int) -> int:
        return isqrt(isqrt(x**3) ** 3 * s * s)

    def v_of(x: int) -> int:
        return isqrt(isqrt(x**3) ** 3)

    floor_runs: list[int] = []
    dv_runs: list[int] = []
    prev_f = prev_dv = None
    f_run = dv_run = 0
    n = p_block + 1
    for _ in range(window):
        floor_dy = (y_scaled(n + 2) - y_scaled(n)) // s
        dv = v_of(n + 2) - v_of(n)
        if prev_f is None or floor_dy != prev_f:
            if f_run:
                floor_runs.append(f_run)
            f_run = 1
            prev_f = floor_dy
        else:
            f_run += 1
        if prev_dv is None or dv != prev_dv:
            if dv_run:
                dv_runs.append(dv_run)
            dv_run = 1
            prev_dv = dv
        else:
            dv_run += 1
        n += 2
    if f_run:
        floor_runs.append(f_run)
    if dv_run:
        dv_runs.append(dv_run)
    return {
        "window": window,
        "floor_dY_mean_run": sum(floor_runs) / len(floor_runs),
        "floor_dY_max_run": max(floor_runs),
        "dv_mean_run": sum(dv_runs) / len(dv_runs),
        "dv_max_run": max(dv_runs),
        "no_v_level_cells": max(floor_runs) == 1 and max(dv_runs) == 1,
    }


def increment_linearization_check(
    n: int, scale: int = 10**24
) -> tuple[int, int]:
    """(E*scale, bound*scale) for the increment identity (Z1).

    F_J(y) = (y+J)^{3/2} - y^{3/2} at J = Δv (step 2). Taylor in the
    single variable θ₂ = {Y} at fixed J:

        F_J(v) = F_J(Y) - F_J'(Y) θ₂ + R_J,

    equivalently E = F_J(Y) - F_J(v) - F_J'(Y) θ₂ satisfies
    0 ≤ E ≤ (3/8) v^{-1/2} (F_J'' < 0, ξ ≥ v). Restoring
    c ≍ k z^{1/2} leaves a W-family C θ₂ with
    C = c F_J'(Y) ≍ k n^{29/16} at the identity-step gap, plus an
    engine-side remainder. An algebraic identity only: it does not
    produce runs on which J is frozen.
    """
    if n < 5 or n % 2 == 0:
        raise ValueError("odd n >= 5 required")
    d = 2
    m = isqrt(n**3)
    v = isqrt(m**3)
    J = isqrt(isqrt((n + d) ** 3) ** 3) - v
    if J <= 0:
        raise ValueError("positive increment J required")
    ys = isqrt(m**3 * scale * scale)
    fv = isqrt((v + J) ** 3 * scale * scale) - isqrt(v**3 * scale * scale)
    fy = isqrt((ys + J * scale) ** 3 // scale) - isqrt(ys**3 // scale)
    y12 = isqrt(ys * scale)
    yj12 = isqrt((ys + J * scale) * scale)
    fp = (3 * (yj12 - y12)) // 2
    th2 = ys - v * scale
    err = fy - fv - (fp * th2) // scale
    v12 = isqrt(v * scale * scale)
    slack = isqrt(max(v, 1)) + 10**6
    bound = (3 * scale * scale) // (8 * max(v12, 1)) + slack
    return err, bound


def increment_linearization_scan(samples: tuple[int, ...]) -> dict[str, Any]:
    slack = 10**7
    checked = 0
    for n in samples:
        try:
            err, bound = increment_linearization_check(n)
        except ValueError:
            continue
        if err < -slack or err > bound:
            return {"holds": False, "witness": n, "err": err, "bound": bound}
        checked += 1
    return {"holds": True, "count": checked}


def increment_j_derivative_check(n: int) -> dict[str, float]:
    """c (F_{J+1}(v) - F_J(v)) / n^{45/16} against the limit 9/8.

    ∂F_J/∂J = (3/2)(v+J)^{1/2}, so unfreezing J by 1 produces the
    Phase-12 leftover c · (3/2) v^{1/2} ≍ n^{45/16}. Scaled integers
    (float only in the final ratio).
    """
    if n < 5 or n % 2 == 0:
        raise ValueError("odd n >= 5 required")
    m = isqrt(n**3)
    v = isqrt(m**3)
    z = isqrt(v**3)
    J = isqrt(isqrt((n + 2) ** 3) ** 3) - v
    if J <= 0:
        raise ValueError("positive increment J required")
    s = 10**12
    df = isqrt((v + J + 1) ** 3 * s * s) - isqrt((v + J) ** 3 * s * s)
    c = (3 * isqrt(z * s * s)) // 4
    phase = c * df
    # n^{45/16} s^2 = n^2 n^{13/16} s^2
    n13s = isqrt(isqrt(isqrt(isqrt(n**13 * s**16))))
    target = (9 * (n**2) * n13s * s) // 8
    ratio = phase / target if target else 0.0
    return {
        "n": float(n),
        "J": float(J),
        "ratio": ratio,
        "limit": 1.0,
    }


def increment_j_derivative_scan(samples: tuple[int, ...]) -> dict[str, Any]:
    """The J-derivative ratio stays near 9/8 through the sample."""
    ratios = []
    for n in samples:
        try:
            row = increment_j_derivative_check(n)
        except ValueError:
            continue
        if not (0.99 <= row["ratio"] <= 1.02):
            return {"holds": False, "witness": n, "ratio": row["ratio"]}
        ratios.append(row["ratio"])
    return {"holds": True, "count": len(ratios), "ratios": ratios}


def x_cell_increment_scan(
    p_block: int, window: int = 400, h: int = 1
) -> dict[str, Any]:
    """Run lengths of floor(ΔY) and Δv *inside* X-cell b-runs.

    The increment-first attack needs frozen J = floor(ΔY) on
    b-runs of floor(Δ_h X) (length ≍ P^{1/2}/h). On those cells
    m advances by b ≍ h P^{1/2} per step, while the m-freeze
    length of floor((m+b)^{3/2}-m^{3/2}) is ≍ P^{1/4}/h, and
    P^{1/2} > P^{1/4}: J changes at every in-cell step. Measured
    mean and max run 1, with mean |Δ floor(ΔY)| ≍ P^{1/4}.
    """
    d = 2 * h
    s = 10**12

    def floor_dx(n: int) -> int:
        # Real gap floor(ΔX), not Δm = floor(ΔX)+κ (the carry flickers).
        return (
            isqrt((n + d) ** 3 * s * s) - isqrt(n**3 * s * s)
        ) // s

    def floor_dy(n: int) -> int:
        m = isqrt(n**3)
        m1 = isqrt((n + d) ** 3)
        return (isqrt(m1**3 * s * s) - isqrt(m**3 * s * s)) // s

    def dv_of(n: int) -> int:
        return isqrt(isqrt((n + d) ** 3) ** 3) - isqrt(isqrt(n**3) ** 3)

    def branch_floor(m: int, gap: int) -> int:
        return (isqrt((m + gap) ** 3 * s * s) - isqrt(m**3 * s * s)) // s

    floor_runs: list[int] = []
    dv_runs: list[int] = []
    b_runs: list[int] = []
    branch_runs: dict[int, list[int]] = {0: [], 1: []}
    dy_changes: list[int] = []
    current_b: int | None = None
    b_run = 0
    prev_f = prev_dv = None
    prev_br: dict[int, int | None] = {0: None, 1: None}
    br_run = {0: 0, 1: 0}
    f_run = dv_run = 0
    last_dy: int | None = None
    n = p_block + 1
    for _ in range(window):
        b = floor_dx(n)
        if current_b is None:
            current_b = b
            b_run = 1
        elif b != current_b:
            if f_run:
                floor_runs.append(f_run)
            if dv_run:
                dv_runs.append(dv_run)
            if b_run:
                b_runs.append(b_run)
            for kap in (0, 1):
                if br_run[kap]:
                    branch_runs[kap].append(br_run[kap])
                br_run[kap] = 0
                prev_br[kap] = None
            f_run = dv_run = 0
            prev_f = prev_dv = None
            last_dy = None
            current_b = b
            b_run = 1
        else:
            b_run += 1
        fdY = floor_dy(n)
        dvt = dv_of(n)
        m = isqrt(n**3)
        if last_dy is not None:
            dy_changes.append(abs(fdY - last_dy))
        last_dy = fdY
        if prev_f is None or fdY != prev_f:
            if f_run:
                floor_runs.append(f_run)
            f_run = 1
            prev_f = fdY
        else:
            f_run += 1
        if prev_dv is None or dvt != prev_dv:
            if dv_run:
                dv_runs.append(dv_run)
            dv_run = 1
            prev_dv = dvt
        else:
            dv_run += 1
        for kap in (0, 1):
            bf = branch_floor(m, b + kap)
            if prev_br[kap] is None or bf != prev_br[kap]:
                if br_run[kap]:
                    branch_runs[kap].append(br_run[kap])
                br_run[kap] = 1
                prev_br[kap] = bf
            else:
                br_run[kap] += 1
        n += 2
    if f_run:
        floor_runs.append(f_run)
    if dv_run:
        dv_runs.append(dv_run)
    if b_run:
        b_runs.append(b_run)
    for kap in (0, 1):
        if br_run[kap]:
            branch_runs[kap].append(br_run[kap])
    branch_max = max(
        (max(branch_runs[k]) for k in (0, 1) if branch_runs[k]),
        default=0,
    )
    return {
        "window": window,
        "n_b_runs": len(b_runs),
        "b_run_max": max(b_runs) if b_runs else 0,
        "b_run_mean": (sum(b_runs) / len(b_runs)) if b_runs else 0.0,
        "floor_dY_mean_run": (
            sum(floor_runs) / len(floor_runs) if floor_runs else 0.0
        ),
        "floor_dY_max_run": max(floor_runs) if floor_runs else 0,
        "dv_mean_run": sum(dv_runs) / len(dv_runs) if dv_runs else 0.0,
        "dv_max_run": max(dv_runs) if dv_runs else 0,
        "branch_j_max_run": branch_max,
        "mean_abs_d_floor_dY": (
            sum(dy_changes) / len(dy_changes) if dy_changes else 0.0
        ),
        "pred_P14": p_block**0.25,
        "no_j_runs_on_x_cells": (
            bool(floor_runs)
            and bool(dv_runs)
            and max(floor_runs) == 1
            and max(dv_runs) == 1
            and branch_max == 1
            and max(b_runs) >= 2
        ),
    }


# --- Phase 13: length-7 engine contractors (OOEOOEE, OOOEOEE) ---


def sixth_ooeoo_check(n: int, scale: int = SCALE) -> tuple[int, int]:
    """(E*scale, bound*scale) for the OOEOO* sixth-letter rearrangement.

    p = floor(w^{3/2}), w = floor(v^{1/2}):
    p^{3/2} = -(5/4) v^{9/8} + (9/4) w v^{5/8} - (3/2) w^{3/4} theta_p + E
    with 0 ≤ E ≤ (3/8) p^{-1/2} + (45/32) v^{1/8} (Taylor remainders
    of (W - theta_p)^{3/2} and (U - theta_w)^{9/4}). The naive
    theta_w coefficient n^{45/32} is absorbed into the integer w;
    no supercritical sawtooth remains.
    """
    if n < 5 or n % 2 == 0:
        raise ValueError("odd n >= 5 required")
    m = isqrt(n**3)
    v = isqrt(m**3)
    w = isqrt(v)
    p = isqrt(w**3)
    p32 = isqrt(p**3 * scale * scale)
    v98 = _eighth_scaled(v**9, scale)
    v58 = _eighth_scaled(v**5, scale)
    w34 = isqrt(isqrt(w**3 * scale**4))
    th_p = isqrt(w**3 * scale * scale) - p * scale
    err = p32 + (5 * v98) // 4 - (9 * w * v58) // 4 + (
        3 * w34 * th_p
    ) // (2 * scale)
    p12 = isqrt(p * scale * scale)
    v18 = _eighth_scaled(v, scale)
    bound = (
        3 * scale * scale // (8 * max(p12, 1))
        + (45 * v18) // 32
        + isqrt(max(v, 1))
        + 10**6
    )
    return err, bound


def sixth_ooeoo_scan(samples: tuple[int, ...]) -> dict[str, Any]:
    slack = 10**7
    for n in samples:
        err, bound = sixth_ooeoo_check(n)
        if err < -slack or err > bound:
            return {"holds": False, "witness": n, "err": err, "bound": bound}
    return {"holds": True, "count": len(samples)}


def sixth_oooeo_check(n: int, scale: int = SCALE) -> tuple[int, int]:
    """(E*scale, bound*scale) for the OOOEO* sixth-letter A' form.

    s = floor(z^{1/2}), z = floor(v^{3/2}):
    s^{3/2} = -(1/2) z^{3/4} + (3/2) s z^{1/4} + E,
    0 ≤ E ≤ (3/8)(U-1)^{-1/2}, U = z^{1/2}. Lemma A' at base z.
    """
    if n < 5 or n % 2 == 0:
        raise ValueError("odd n >= 5 required")
    m = isqrt(n**3)
    v = isqrt(m**3)
    z = isqrt(v**3)
    s = isqrt(z)
    t = isqrt(s**3 * scale * scale)
    z34 = isqrt(isqrt(z**3 * scale**4))
    z14 = isqrt(isqrt(z * scale**4))
    err = t + z34 // 2 - (3 * s * z14) // 2
    u = max(s, 2)
    # Floor slack: z14 error O(1) times (3/2)s ~ n^{27/16}.
    slack = 2 * s + 10**6
    bound = 3 * scale // (8 * isqrt(u - 1)) + slack
    return err, bound


def sixth_oooeo_scan(samples: tuple[int, ...]) -> dict[str, Any]:
    slack = 10**7
    for n in samples:
        err, bound = sixth_oooeo_check(n)
        if err < -slack or err > bound:
            return {"holds": False, "witness": n, "err": err, "bound": bound}
    return {"holds": True, "count": len(samples)}


def w_gap_freeze_scan(p_block: int, window: int = 400) -> dict[str, Any]:
    """floor(Δ v^{1/2}) freezes on the OOEO cylinder (long runs).

    Predicted run length ≍ P^{7/8}: (v^{1/2})'' ≍ P^{-7/8} < 1.
    The integer first gap of w is this frozen floor plus a 0/1 carry.
    """
    s = 10**12
    runs: list[int] = []
    prev = None
    run = 0
    n = p_block + 1
    got = 0
    while got < window and n < 20 * p_block:
        m = isqrt(n**3)
        if m % 2 == 0:
            n += 2
            continue
        v = isqrt(m**3)
        if v % 2 == 1:
            n += 2
            continue
        u0 = isqrt(v * s * s)
        n2 = n + 2
        v2 = isqrt(isqrt(n2**3) ** 3)
        u1 = isqrt(v2 * s * s)
        floor_du = (u1 - u0) // s
        if prev is None or floor_du != prev:
            if run:
                runs.append(run)
            run = 1
            prev = floor_du
        else:
            run += 1
        got += 1
        n += 2
    if run:
        runs.append(run)
    return {
        "got": got,
        "mean_run": sum(runs) / len(runs) if runs else 0.0,
        "max_run": max(runs) if runs else 0,
        "n_runs": len(runs),
        "frozen": bool(runs) and (sum(runs) / len(runs) >= 8),
    }


def ooeooee_indicator_identity_check(n_max: int) -> dict[str, Any]:
    """Branch consistency: OOEOOEE is OOEOO plus even p^{3/2} and even q^{1/2}."""
    checked = 0
    for n in range(3, n_max + 1, 2):
        word = itinerary_word(n, 7)
        if not word.startswith("OOEOO"):
            continue
        m = isqrt(n**3)
        v = isqrt(m**3)
        w = isqrt(v)
        p = isqrt(w**3)
        q = isqrt(p**3)
        expected = (
            "OOEOO"
            + ("O" if q % 2 == 1 else "E")
            + ("O" if isqrt(q) % 2 == 1 else "E")
        )
        if q % 2 == 0:
            expected = "OOEOO" + "E" + ("O" if isqrt(q) % 2 == 1 else "E")
        else:
            expected = "OOEOO" + "O" + ("O" if isqrt(q**3) % 2 == 1 else "E")
        if word != expected:
            return {"holds": False, "witness": n, "got": word, "expected": expected}
        checked += 1
    return {"holds": True, "checked": checked, "n_max": n_max}


def oooeoee_indicator_identity_check(n_max: int) -> dict[str, Any]:
    """Branch consistency: OOOEO* sixth letter is parity of isqrt(s^3)."""
    checked = 0
    for n in range(3, n_max + 1, 2):
        word = itinerary_word(n, 7)
        if not word.startswith("OOOEO"):
            continue
        m = isqrt(n**3)
        v = isqrt(m**3)
        z = isqrt(v**3)
        s = isqrt(z)
        q = isqrt(s**3)
        if q % 2 == 0:
            expected = "OOOEO" + "E" + ("O" if isqrt(q) % 2 == 1 else "E")
        else:
            expected = "OOOEO" + "O" + ("O" if isqrt(q**3) % 2 == 1 else "E")
        if word != expected:
            return {"holds": False, "witness": n, "got": word, "expected": expected}
        checked += 1
    return {"holds": True, "checked": checked, "n_max": n_max}


def oeo_mode_probe(p_block: int) -> dict[str, Any]:
    """Float probe of the OEO* mode sum sum e((1/2) w^{3/2}) on n ~ P.

    Exact scaled phase; float only in the exponential. Cancellation
    here is what Theorem Q proves.
    """
    from math import cos, pi, sin

    s = 10**12
    re = im = 0.0
    cnt = 0
    n = p_block + 1
    while n < 2 * p_block:
        w = isqrt(isqrt(n**3))
        t_w = isqrt(w**3 * s * s)
        frac = (t_w % (2 * s)) / (2 * s)
        ph = 2 * pi * frac
        re += cos(ph)
        im += sin(ph)
        cnt += 1
        n += 2
    return {"count": cnt, "abs_sum": round((re * re + im * im) ** 0.5, 1)}


# --- Phase 5: even-branch third letter, tier-2 bricks, kernel probe ---


def m12_smoothing_check(n: int, scale: int = SCALE) -> tuple[int, int]:
    """(D1(n)*scale, bound*scale) for the OE-branch third-letter smoothing.

    Proposition L brick: m^{1/2} = n^{3/4} + D1(n) with
    -(1/2) n^{-3/4} - n^{-9/4} <= D1 <= 0, where m = floor(n^{3/2}).
    Decaying amplitudes only; same pattern as Lemma D.
    """
    if n < 3 or n % 2 == 0:
        raise ValueError("odd n >= 3 required")
    m = isqrt(n**3)
    m12 = isqrt(m * scale * scale)
    n34 = isqrt(isqrt(n**3 * scale**4))
    diff = m12 - n34
    r94 = isqrt(isqrt(n**9 * scale**4))
    bound = scale * scale // (2 * n34) + scale * scale // r94
    return diff, bound


def m12_scan(samples: tuple[int, ...]) -> dict[str, Any]:
    slack = 8
    for n in samples:
        diff, bound = m12_smoothing_check(n)
        if diff > slack or diff < -bound - slack:
            return {"holds": False, "witness": n}
    return {"holds": True, "count": len(samples)}


def oe_indicator_identity_check(n_max: int) -> dict[str, Any]:
    """Branch consistency for the OE-branch third letter.

    itinerary_word(n, 3) == 'OEE' iff m even and isqrt(m) even: the
    (1+psi_1) factor restricts to even m, exactly where J^2 takes the
    even branch, so psi(m^{1/2}) evaluates unconditionally.
    """
    for n in range(3, n_max + 1, 2):
        m = isqrt(n**3)
        if (itinerary_word(n, 3) == "OEE") != (m % 2 == 0 and isqrt(m) % 2 == 0):
            return {"holds": False, "witness": n}
    return {"holds": True, "n_max": n_max}


def lemma_m_checks(n: int, big_g: int, scale: int = 10**60) -> dict[str, tuple[int, int]]:
    """Exact scaled validation of the Lemma M second-order forms.

    (i)  m^{3/2} = -(1/8) X^{3/2} + (3/4) m X^{1/2} + (3/8) m^2 X^{-1/2}
         + R5,  0 <= R5 <= (1/16)(X-1)^{-3/2};
    (ii) (m+G)^{3/2} = Z^{3/2} - (3/2) X Z^{1/2} + (3/8) X^2 Z^{-1/2}
         + m [ (3/2) Z^{1/2} - (3/4) X Z^{-1/2} ] + (3/8) m^2 Z^{-1/2}
         + R6,  0 <= R6 <= (1/16)(Z-1)^{-3/2},
    (both remainders are the positive third-order Taylor terms of
    t -> (X-t)^{3/2} resp. (Z-t)^{3/2}, since f''' > 0 and theta > 0)
    with X = n^{3/2}, Z = X + G. These carry the differenced tier-2
    phase; remainders are absorbable against the W ~ k n^{9/8} weight.
    """
    if n < 5 or n % 2 == 0:
        raise ValueError("odd n >= 5 required")
    s2 = scale * scale
    m = isqrt(n**3)
    xs = isqrt(n**3 * s2)                          # X * scale
    x12 = isqrt(isqrt(n**3 * scale**4))            # X^{1/2} * scale
    x32 = isqrt(isqrt(n**9 * scale**4))            # X^{3/2} * scale

    lhs_i = isqrt(m**3 * s2)
    poly_i = -x32 // 8 + 3 * m * x12 // 4 + 3 * m * m * s2 // (8 * x12)
    bound_i = s2 // (14 * x32) + 4 * n**3 + 1000

    zs = xs + big_g * scale                        # Z * scale
    z12 = isqrt(zs * scale)                        # Z^{1/2} * scale
    z32 = zs * z12 // scale                        # Z^{3/2} * scale
    lhs_ii = isqrt((m + big_g) ** 3 * s2)
    poly_ii = (
        z32
        - 3 * xs * z12 // (2 * scale)
        + 3 * n**3 * s2 // (8 * z12)
        + m * (3 * z12 // 2 - 3 * xs * scale // (4 * z12))
        + 3 * m * m * s2 // (8 * z12)
    )
    bound_ii = s2 // (14 * z32) + 4 * n**3 + 1000
    return {
        "m32": (poly_i - lhs_i, bound_i),
        "shifted": (poly_ii - lhs_ii, bound_ii),
    }


def lemma_m_scan(samples: tuple[int, ...], h: int = 1) -> dict[str, Any]:
    """Check both Lemma M identities on samples with realized gaps G."""
    for n in samples:
        big_g = isqrt((n + 2 * h) ** 3) - isqrt(n**3)
        res = lemma_m_checks(n, big_g)
        # poly - lhs = -R with R the positive Taylor remainder: window [-bound, slack].
        for which in ("m32", "shifted"):
            diff, bound = res[which]
            if not (-bound <= diff <= 4 * n**3 + 1000):
                return {"holds": False, "witness": n, "which": which}
    return {"holds": True, "count": len(samples)}


def level2_gap_check(start: int, count: int, h: int) -> dict[str, Any]:
    """Lemma N: g2 = floor(DY) + [theta2 >= 1 - {DY}] with DY = Y+ - Y.

    Exact check on realized orbit data; boundary-ambiguous samples
    (fractional parts within a guard band of 0/1) are skipped, as in
    gap_decomposition_check.
    """
    s = 10**24
    guard = 10**6
    matches = skipped = 0
    n = start if start % 2 == 1 else start + 1
    for _ in range(count):
        m0 = isqrt(n**3)
        m1 = isqrt((n + 2 * h) ** 3)
        v0, v1 = isqrt(m0**3), isqrt(m1**3)
        y0 = isqrt(m0**3 * s * s)
        y1 = isqrt(m1**3 * s * s)
        dys = y1 - y0
        fdy, frac_dy = divmod(dys, s)
        th2 = y0 - v0 * s
        if frac_dy < guard or frac_dy > s - guard or abs(th2 - (s - frac_dy)) < guard:
            skipped += 1
            n += 2
            continue
        kappa2 = 1 if th2 >= s - frac_dy else 0
        if v1 - v0 != fdy + kappa2:
            return {"holds": False, "witness": n}
        matches += 1
        n += 2
    return {"holds": True, "matches": matches, "skipped": skipped}


def kernel_probe(p_block: int, coeff_num: int = 3, coeff_den: int = 4) -> dict[str, Any]:
    """Float probe of the isolated tier-2 kernel K = sum e(c(n) {m^{3/2}}).

    c(n) = (coeff_num/coeff_den) n^{9/8}, the natural W-scale of the
    OOO* reduction. Exact scaled phase arithmetic; float only in the
    final exponential. Not a proof; supports or refutes Conjecture L.
    """
    from math import cos, pi, sin

    s = 10**12
    s30 = 10**30
    re = im = 0.0
    cnt = 0
    n = p_block + 1
    while n < 2 * p_block:
        m = isqrt(n**3)
        t2 = isqrt(m**3 * s * s)
        th2 = t2 - (t2 // s) * s                     # {m^{3/2}} * s
        r9 = _eighth_scaled(n**9, s30)               # n^{9/8} * s30
        prod = (coeff_num * r9 * th2) // coeff_den   # c*theta2 * s30*s
        frac = (prod % (s30 * s)) / (s30 * s)
        ph = 2 * pi * frac
        re += cos(ph)
        im += sin(ph)
        cnt += 1
        n += 2
    return {"count": cnt, "abs_sum": round((re * re + im * im) ** 0.5, 1)}


# --- Phase 8: the kernel — double-differencing validators and probes ---


def kernel_reformulation_check(n: int, scale: int = 10**40) -> tuple[int, int]:
    """(diff*scale, bound*scale) for the kernel reformulation (Lemma R1).

    With Y = m^{3/2}, v = floor(Y), theta_2 = Y - v:
    (1/2)(m^{9/4} - v^{3/2}) - (3/4) v^{1/2} theta_2 = R in
    [0, (3/16) v^{-1/2}] (Taylor of (v + theta_2)^{3/2} at v, one-signed
    remainder). Hence the central kernel phase c*theta_2 with
    c = (3k/4) v^{1/2} equals (k/2)(m^{9/4} - v^{3/2}) up to kR: the
    kernel is the exponential sum of the level-2 local floor defect.
    """
    if n < 5 or n % 2 == 0:
        raise ValueError("odd n >= 5 required")
    m = isqrt(n**3)
    v = isqrt(m**3)
    m94 = isqrt(isqrt(m**9 * scale**4))
    v32 = isqrt(v**3 * scale * scale)
    v12 = isqrt(v * scale * scale)
    th2 = isqrt(m**3 * scale * scale) - v * scale
    diff = (m94 - v32) // 2 - (3 * v12 * th2) // (4 * scale)
    # Floor slack: th2 and v12 each carry O(1) scaled-unit error, and
    # the cross products propagate them at v^{1/2} ~ n^{9/8} units.
    slack = isqrt(n**9) + 10**6
    bound = (3 * scale * scale) // (16 * v12) + slack
    return diff, bound


def kernel_reformulation_scan(samples: tuple[int, ...]) -> dict[str, Any]:
    """Check 0 <= diff <= bound on odd samples (slack folded into bound)."""
    slack = 10**7
    for n in samples:
        diff, bound = kernel_reformulation_check(n)
        if diff < -slack or diff > bound:
            return {"holds": False, "witness": n}
    return {"holds": True, "count": len(samples)}


def double_gap_identity_check(
    start: int, count: int, h1: int, h2: int
) -> dict[str, Any]:
    """Lemma R2: the second difference of the level-2 gap decomposes as

    D2 g2 = floor(D2 D1 Y) + kappa'' + D2 kappa_2,

    with W = D1 Y, kappa'' = [{W} >= 1 - {D2 W}] (gap identity on the
    sequence W) and kappa_2 = [theta_2 >= 1 - {W}] (Lemma N). Exact on
    orbit data; boundary-ambiguous samples are skipped (guard band),
    as in level2_gap_check. Lean: seq_floor_gap applied twice
    (seq_floor_gap_second in GapCells.lean).
    """
    s = 10**24
    guard = 10**6
    matches = skipped = 0
    n = start if start % 2 == 1 else start + 1
    d1, d2 = 2 * h1, 2 * h2

    def y_scaled(x: int) -> int:
        return isqrt(isqrt(x**3) ** 3 * s * s)

    def v_of(x: int) -> int:
        return isqrt(isqrt(x**3) ** 3)

    for _ in range(count):
        y00, y10 = y_scaled(n), y_scaled(n + d1)
        y01, y11 = y_scaled(n + d2), y_scaled(n + d1 + d2)
        v00, v10, v01, v11 = v_of(n), v_of(n + d1), v_of(n + d2), v_of(n + d1 + d2)
        w0 = y10 - y00                      # W(n) * s
        w1 = y11 - y01                      # W(n + d2) * s
        dw = w1 - w0                        # (D2 D1 Y) * s
        fdw, frac_dw = divmod(dw, s)
        frac_w0 = w0 % s
        frac_w1 = w1 % s
        th2_0 = y00 - v00 * s
        th2_1 = y01 - v01 * s
        fracs = (frac_dw, frac_w0, frac_w1, th2_0, th2_1)
        pairs = (
            (frac_w0, s - frac_dw),
            (th2_0, s - frac_w0),
            (th2_1, s - frac_w1),
        )
        if any(f < guard or f > s - guard for f in fracs) or any(
            abs(a - b) < guard for a, b in pairs
        ):
            skipped += 1
            n += 2
            continue
        kappa_dd = 1 if frac_w0 >= s - frac_dw else 0
        kappa2_0 = 1 if th2_0 >= s - frac_w0 else 0
        kappa2_1 = 1 if th2_1 >= s - frac_w1 else 0
        lhs = (v11 - v01) - (v10 - v00)     # D2 g2
        rhs = fdw + kappa_dd + (kappa2_1 - kappa2_0)
        if lhs != rhs:
            return {"holds": False, "witness": n}
        matches += 1
        n += 2
    return {"holds": True, "matches": matches, "skipped": skipped}


def branch_freeze_scan(
    p_block: int, h1: int, h2: int, window: int
) -> dict[str, Any]:
    """Lemma R3 support: the branch values of D2 D1 Y freeze.

    Raw floor(D2 D1 Y) is NOT frozen: the level-1 second gap
    j1 = D2 g1 flickers at every step and shifts D2 D1 Y by
    (3/2) j1 m^{1/2} ~ n^{3/4}. The proof's organization conditions on
    the cell gaps (G1, G2) and the bounded j1 = j; the branch function
    F_j(m) = (m+G1+G2+j)^{3/2} - (m+G1)^{3/2} - (m+G2)^{3/2} + m^{3/2}
    is smooth in m with n-drift ~ (9/8) j n^{-1/4} + O(h1 h2 n^{-3/4})
    < 1, so its floor is constant on long runs; the flicker lives in
    the indicator [j1 = j], never in the branch. This scan evaluates
    each branch j in {-1, 0, 1} at every n of a window inside a cell
    intersection and reports the distinct-floor counts against the
    drift prediction.
    """
    s = 10**24
    d1, d2 = 2 * h1, 2 * h2
    n0 = p_block + 1
    m0 = isqrt(n0**3)
    big_g1 = isqrt((n0 + d1) ** 3) - m0
    big_g2 = isqrt((n0 + d2) ** 3) - m0

    def branch_floor(m: int, j: int) -> int:
        val = (
            isqrt((m + big_g1 + big_g2 + j) ** 3 * s * s)
            - isqrt((m + big_g1) ** 3 * s * s)
            - isqrt((m + big_g2) ** 3 * s * s)
            + isqrt(m**3 * s * s)
        )
        return val // s

    out: dict[str, Any] = {"window": window}
    in_cell = 0
    values: dict[int, set[int]] = {-1: set(), 0: set(), 1: set()}
    n = n0
    for _ in range(window):
        m = isqrt(n**3)
        if (
            isqrt((n + d1) ** 3) - m != big_g1
            or isqrt((n + d2) ** 3) - m != big_g2
        ):
            break
        in_cell += 1
        for j in (-1, 0, 1):
            values[j].add(branch_floor(m, j))
        n += 2
    for j in (-1, 0, 1):
        drift = 1.125 * abs(j) / p_block**0.25 + h1 * h2 / p_block**0.75
        out[f"branch_{j}"] = {
            "distinct": len(values[j]),
            "predicted": round(1 + 2 * in_cell * drift, 1),
        }
    out["in_cell"] = in_cell
    return out


def _kernel_phase_scaled(n: int, coeff_num: int, coeff_den: int) -> float:
    """{c(n) theta_2(n)} with c = (num/den) n^{9/8}, exact scaled ints."""
    s = 10**12
    s30 = 10**30
    m = isqrt(n**3)
    t2 = isqrt(m**3 * s * s)
    th2 = t2 - (t2 // s) * s
    r9 = _eighth_scaled(n**9, s30)
    prod = (coeff_num * r9 * th2) // coeff_den
    return (prod % (s30 * s)) / (s30 * s)


def differenced_kernel_probe(
    p_block: int,
    h1: int,
    h2: int = 0,
    h3: int = 0,
    coeff_num: int = 3,
    coeff_den: int = 4,
) -> dict[str, Any]:
    """Float probe of the once-, twice- or thrice-differenced kernel sums.

    h2 = 0: T1 = sum e(phi(n+2h1) - phi(n)).
    h2 > 0: T2, the second Weyl difference over the (h1, h2) rectangle.
    h3 > 0: T3, the third difference (the targeted extra differencing of
    the review pass, applied to the kernel itself as a proxy for the
    mixed pieces). phi = c theta_2 with c = (coeff_num/coeff_den)
    n^{9/8}. Exact scaled phases, float only in the final exponential.
    Supports or refutes the differencing route; not a proof.
    """
    from math import cos, pi, sin

    # Build signed corner shifts for up to three nested differences.
    corners = [(1, 2 * h1), (-1, 0)]
    for h in (h2, h3):
        if h > 0:
            corners = [(s, d + 2 * h) for s, d in corners] + [
                (-s, d) for s, d in corners
            ]
    re = im = 0.0
    cnt = 0
    n = p_block + 1
    while n < 2 * p_block:
        ph = 0.0
        for sgn, d in corners:
            ph += sgn * _kernel_phase_scaled(n + d, coeff_num, coeff_den)
        theta = 2 * pi * ph
        re += cos(theta)
        im += sin(theta)
        cnt += 1
        n += 2
    return {
        "count": cnt,
        "abs_sum": round((re * re + im * im) ** 0.5, 1),
        "sqrt_count": round(cnt**0.5, 1),
    }


# --- Phase 4: second-order linearization bricks for the OOO* layer ---

SCALE2 = 10**60


def _eighth_scaled2(x: int, scale: int = SCALE2) -> int:
    return isqrt(isqrt(isqrt(x * scale**8)))


def second_order_checks(n: int, scale: int = SCALE2) -> dict[str, tuple[int, int]]:
    """Exact scaled validation of the three Lemma G / Proposition H identities.

    (a) m^{3/4} = (5/32) n^{9/8} + (15/16) m n^{-3/8} - (3/32) m^2 n^{-15/8} - R3,
        0 <= R3 <= (5/128)(n^{3/2}-1)^{-9/4};
    (b) m^{9/4} = (5/32) n^{27/8} - (9/16) m n^{15/8} + (45/32) m^2 n^{3/8} + R4,
        -(15/128)(n^{3/2}-1)^{-3/4} <= R4 <= 0;
    (c) v^{3/2} = -(5/64) n^{27/8} + (9/32) m n^{15/8} - (45/64) m^2 n^{3/8}
        + (15/64) v n^{9/8} + (45/32) v m n^{-3/8} - (9/64) v m^2 n^{-15/8} + err,
        |err| <= (3/4) n^{-9/8}.

    Returns {name: (diff_scaled, bound_scaled)} at SCALE2 (needed because the
    identities cancel to n^{-9/8} out of n^{27/8}-size terms).
    """
    if n < 5 or n % 2 == 0:
        raise ValueError("odd n >= 5 required")
    m = isqrt(n**3)
    v = isqrt(m**3)
    s2 = scale * scale
    r3 = _eighth_scaled2(n**3, scale)      # n^{3/8}  * scale
    r9 = _eighth_scaled2(n**9, scale)      # n^{9/8}  * scale
    r15 = _eighth_scaled2(n**15, scale)    # n^{15/8} * scale
    r27 = _eighth_scaled2(n**27, scale)    # n^{27/8} * scale

    # Negative powers are computed as direct divisions by the scaled
    # roots (never as products with a scaled inverse): the floor error
    # is then relative ~1/(n^a * scale) instead of absolute, keeping
    # every term's rounding at O(n^3) scaled units.
    m34 = isqrt(isqrt(m**3 * scale**4))
    poly_a = 5 * r9 // 32 + 15 * m * s2 // (16 * r3) - 3 * m * m * s2 // (32 * r15)
    bound_a = 5 * s2 // (128 * r27) + n + 100

    m94 = isqrt(isqrt(m**9 * scale**4))
    poly_b = 5 * r27 // 32 - 9 * m * r15 // 16 + 45 * m * m * r3 // 32
    bound_b = 15 * s2 // (128 * r9) + n + 100

    v32 = isqrt(v**3 * scale * scale)
    poly_c = (
        -(5 * r27) // 64
        + 9 * m * r15 // 32
        - 45 * m * m * r3 // 64
        + 15 * v * r9 // 64
        + 45 * v * m * s2 // (32 * r3)
        - 9 * v * m * m * s2 // (64 * r15)
    )
    bound_c = 3 * s2 // (4 * r9) + n + 100

    return {
        "m34": (poly_a - m34, bound_a),
        "m94": (m94 - poly_b, bound_b),
        "v32": (v32 - poly_c, bound_c),
    }


def second_order_scan(samples: tuple[int, ...]) -> dict[str, Any]:
    """Check R3 in [0, bound], R4 in [-bound, 0], |err| <= bound on samples.

    Slack covers integer-division rounding: each term contributes up to
    ~(45/32) m^2 = O(n^3) scaled units of floor error, so 4 n^3 covers
    the sum; that is <= 10^{-23} in value for n <= 10^{12}, far below
    the n^{-9/8}-scale remainder bounds.
    """
    for n in samples:
        slack = 4 * n**3 + 1000
        res = second_order_checks(n)
        da, ba = res["m34"]
        if not (-slack <= da <= ba + slack):
            return {"holds": False, "witness": n, "which": "m34"}
        db, bb = res["m94"]
        if not (-bb - slack <= db <= slack):
            return {"holds": False, "witness": n, "which": "m94"}
        dc, bc = res["v32"]
        if abs(dc) > bc + slack:
            return {"holds": False, "witness": n, "which": "v32"}
    return {"holds": True, "count": len(samples)}


def ooo_indicator_identity_check(n_max: int) -> dict[str, Any]:
    """Branch consistency of the OOO* sign algebra.

    itinerary_word(n, 4) == 'OOOE' iff m odd, v odd, isqrt(v^3) even:
    the (1-psi_2) factor restricts to odd v, exactly where J^3 takes
    the odd branch, so psi_4 = psi(v^{3/2}) evaluates unconditionally.
    """
    for n in range(3, n_max + 1, 2):
        m = isqrt(n**3)
        v = isqrt(m**3)
        signs = (m % 2 == 1, v % 2 == 1, isqrt(v**3) % 2 == 0)
        if (itinerary_word(n, 4) == "OOOE") != all(signs):
            return {"holds": False, "witness": n}
    return {"holds": True, "n_max": n_max}


def second_gap_collision_check(start: int, count: int, h: int) -> dict[str, Any]:
    """Quantify the composed-cell obstruction.

    On maximal runs (cells) where g1 = m(n+2h) - m(n) is constant, count
    the distinct values of g2 = v(n+2h) - v(n). Ratio near 1 means g2
    changes at almost every point of the cell: there is no usable
    second-level cell structure, so the naive composition of Lemma B
    across two growing layers fails.
    """
    cells: list[tuple[int, int]] = []  # (cell length, distinct g2 count)
    prev_g1 = None
    g2_set: set[int] = set()
    length = 0
    n = start if start % 2 == 1 else start + 1
    for _ in range(count):
        m0, m1 = isqrt(n**3), isqrt((n + 2 * h) ** 3)
        g1 = m1 - m0
        g2 = isqrt(m1**3) - isqrt(m0**3)
        if g1 != prev_g1 and prev_g1 is not None:
            cells.append((length, len(g2_set)))
            g2_set, length = set(), 0
        prev_g1 = g1
        g2_set.add(g2)
        length += 1
        n += 2
    interior = cells[1:] if len(cells) > 2 else cells
    total_len = sum(c[0] for c in interior)
    total_distinct = sum(c[1] for c in interior)
    return {
        "cells": len(interior),
        "mean_cell_length": round(total_len / max(1, len(interior)), 2),
        "distinct_ratio": round(total_distinct / max(1, total_len), 4),
    }


def gap_decomposition_check(start: int, count: int, h: int) -> dict[str, Any]:
    """Verify g(n) = floor(delta) + kappa on `count` consecutive odd n.

    g(n) = m(n+2h) - m(n), delta(n) = (n+2h)^{3/2} - n^{3/2}, and
    kappa = [ {n^{3/2}} >= 1 - {delta(n)} ]. Exact scaled integers;
    samples within a tiny window of a cell boundary are skipped and
    counted separately.
    """
    scale = SCALE
    tol = 10
    matches = skipped = 0
    for i in range(count):
        n = start + 2 * i
        m0 = isqrt(n**3)
        m1 = isqrt((n + 2 * h) ** 3)
        g = m1 - m0
        s0 = _sqrt_scaled(n**3, scale)
        s1 = _sqrt_scaled((n + 2 * h) ** 3, scale)
        delta_scaled = s1 - s0
        floor_delta = delta_scaled // scale
        frac_delta = delta_scaled % scale
        frac_n = s0 - m0 * scale
        threshold = scale - frac_delta
        if abs(frac_n - threshold) <= tol:
            skipped += 1
            continue
        kappa = 1 if frac_n >= threshold else 0
        if g != floor_delta + kappa:
            return {"holds": False, "witness": n}
        matches += 1
    return {"holds": True, "matches": matches, "skipped": skipped}


def itinerary_word(n: int, depth: int = DEPTH) -> str:
    """Parity letters of n, J(n), ..., J^{depth-1}(n). Exact isqrt only."""
    letters = []
    x = n
    for _ in range(depth):
        letters.append("O" if x % 2 == 1 else "E")
        x = juggler_step(x)
    return "".join(letters)


def word_counts(n_max: int, depth: int = DEPTH) -> dict[str, int]:
    """Exact counts of depth-letter itinerary words over odd n in [3, n_max]."""
    counts = {w: 0 for w in WORDS4} if depth == 4 else {}
    for n in range(3, n_max + 1, 2):
        w = itinerary_word(n, depth)
        counts[w] = counts.get(w, 0) + 1
    return counts


def _prefix_counts(counts4: dict[str, int], depth: int) -> dict[str, int]:
    out: dict[str, int] = {}
    for w, c in counts4.items():
        key = w[:depth]
        out[key] = out.get(key, 0) + c
    return out


def _discrepancies(counts4: dict[str, int], odds: int) -> dict[str, float]:
    """D_w = count_w - odds * 2^{-(|w|-1)} for every word of length 2..4."""
    out: dict[str, float] = {}
    for depth in (2, 3, 4):
        expected = odds / (1 << (depth - 1))
        for w, c in _prefix_counts(counts4, depth).items():
            out[w] = c - expected
    return out


def _fit_exponent(points: list[tuple[int, float]]) -> float | None:
    """Least-squares slope of log max|D| vs log N on the top half of points."""
    usable = [(n, v) for n, v in points if v > 0]
    if len(usable) < 8:
        return None
    tail = usable[len(usable) // 2:]
    xs = [log(n) for n, _ in tail]
    ys = [log(v) for _, v in tail]
    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)
    den = sum((x - mx) ** 2 for x in xs)
    if den == 0:
        return None
    return round(sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / den, 4)


def scan(n_max: int = N_MAX) -> dict[str, Any]:
    """One exact pass over odd starts with a geometric discrepancy envelope."""
    counts4 = {w: 0 for w in WORDS4}
    odds = 0
    ooee_descent_violations = 0
    max_abs: dict[int, float] = {2: 0.0, 3: 0.0, 4: 0.0}
    envelope: dict[int, list[tuple[int, float]]] = {2: [], 3: [], 4: []}
    rows: list[dict[str, Any]] = []
    coarse = {n for n in COARSE_GRID if n <= n_max} | {n_max}
    next_sample = 1024

    for n in range(3, n_max + 1, 2):
        letters = []
        x = n
        for _ in range(DEPTH):
            letters.append("O" if x % 2 == 1 else "E")
            x = juggler_step(x)
        w = "".join(letters)
        counts4[w] += 1
        odds += 1
        if w == CONTRACTING_TARGET and x >= n:
            ooee_descent_violations += 1
        boundary = n + 1
        if boundary >= next_sample or boundary >= n_max - 1:
            disc = _discrepancies(counts4, odds)
            for depth in (2, 3, 4):
                depth_max = max(abs(v) for k, v in disc.items() if len(k) == depth)
                if depth_max > max_abs[depth]:
                    max_abs[depth] = depth_max
                envelope[depth].append((boundary, max_abs[depth]))
            if boundary in coarse or boundary - 1 in coarse:
                rows.append(
                    {
                        "n": boundary,
                        "odds": odds,
                        "counts4": dict(counts4),
                        "D": {k: round(v, 4) for k, v in disc.items()},
                        "max_abs_D": {str(d): round(max_abs[d], 4) for d in (2, 3, 4)},
                        "max_over_n12": {
                            str(d): round(max_abs[d] / boundary**0.5, 6)
                            for d in (2, 3, 4)
                        },
                        "max_over_n13": {
                            str(d): round(max_abs[d] / boundary ** (1 / 3), 6)
                            for d in (2, 3, 4)
                        },
                    }
                )
            while next_sample <= boundary:
                next_sample = int(next_sample * ENVELOPE_RATIO) + 1

    final = rows[-1]
    fitted = {str(d): _fit_exponent(envelope[d]) for d in (2, 3, 4)}
    ooee_count = counts4[CONTRACTING_TARGET]
    return {
        "n_max": n_max,
        "depth": DEPTH,
        "checkpoints": rows,
        "final": final,
        "max_abs_D": {str(d): round(max_abs[d], 4) for d in (2, 3, 4)},
        "fitted_exponent": fitted,
        "ooee": {
            "count": ooee_count,
            "fraction_of_odds": round(ooee_count / final["odds"], 6),
            "expected_fraction": 0.125,
            "descent_violations": ooee_descent_violations,
        },
        "anti_overclaim": dict(ANTI_OVERCLAIM),
    }


def write_json(row: dict[str, Any], path: Path = JSON_PATH) -> None:
    path.write_text(json.dumps(row, indent=2) + "\n", encoding="utf-8")


def write_docs(row: dict[str, Any], path: Path = DOC_PATH) -> None:
    final = row["final"]
    fit = row["fitted_exponent"]
    ooee = row["ooee"]
    lines = [
        "# Juggler multi-step itinerary-parity census",
        "",
        "Status: **COMPUTATIONALLY VERIFIED** counts; every depth-4 word",
        "class is **EXACT — HUMAN PROOF**",
        "(`J-nested-parity-discrepancy`, `J-triple-parity-discrepancy`,",
        "`J-even-branch-third-letter`, `J-four-step-descent-density`,",
        "`J-depth4-slow-branch`, `J-kernel-cancellation`,",
        "`J-depth4-complete`, `J-depth5-contracting`,",
        "`J-five-step-descent-density`, `J-depth7-engine-contracting`,",
        "`J-seven-step-descent-density`; proofs in",
        "`juggler_two_step_parity_lemma.md`). Certified descent",
        "density 57/64. OOOO* kernel isolated (Lemma V1); the",
        "scale-invariant copy of Theorem R and the increment-first",
        "K3 attack are **REFUTED**.",
        "",
        "Exact census of the joint parity word of the first four itinerary",
        "letters on odd starts. Phase-0 falsifier for iterating the one-step",
        "discrepancy bound (Theorem 5.1 in the finite-dynamics note) to",
        "depth two and beyond. Not a frequency theorem, not a predictive",
        "state, not a termination claim.",
        "",
        f"Window: odd `n <= {row['n_max']}`. Expected class fraction of a",
        "depth-`d` word within odd starts is `2^{-(d-1)}`.",
        "",
        "| depth | max|D_w| on window | max|D|/N^{1/2} | max|D|/N^{1/3} | fitted exponent |",
        "| --- | --- | --- | --- | --- |",
    ]
    for d in ("2", "3", "4"):
        lines.append(
            f"| {d} | {row['max_abs_D'][d]} | "
            f"{final['max_over_n12'][d]} | {final['max_over_n13'][d]} | "
            f"{fit[d]} |"
        )
    lines += [
        "",
        f"Depth-4 counts at `N = {final['n']}` (odds = {final['odds']}):",
        "",
        "| word | count | D_w |",
        "| --- | --- | --- |",
    ]
    for w in sorted(final["counts4"]):
        lines.append(f"| {w} | {final['counts4'][w]} | {final['D'][w]} |")
    lines += [
        "",
        "## OOEE class",
        "",
        f"`OOEE` count {ooee['count']} = {ooee['fraction_of_odds']} of odd",
        f"starts (product density {ooee['expected_fraction']}). Every census",
        "OOEE start satisfied the four-step descent `T^4(n) < n`",
        f"(violations: {ooee['descent_violations']}); this instantiates the",
        "contraction `3^2 < 2^4` and is a guard, not a new theorem.",
        "",
        "## Reading",
        "",
        "The fitted exponents are envelope slopes on a geometric sample,",
        "label **OBSERVATION**. The analytic statements they probe are",
        "now theorems at every depth <= 4, and the two length-5",
        "contracting splits OOOEE/OOEOE lift certified descent to 7/8;",
        "the two length-7 engine contractors OOEOOEE/OOOEOEE lift",
        "certified descent to 57/64; the OOOO* kernel K3 is isolated",
        "and both the scale-invariant copy of Theorem R and the",
        "increment-first K3 attack are REFUTED.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    row = scan()
    write_json(row)
    write_docs(row)
    print(
        "fitted exponents",
        row["fitted_exponent"],
        "ooee fraction",
        row["ooee"]["fraction_of_odds"],
    )


if __name__ == "__main__":
    main()
