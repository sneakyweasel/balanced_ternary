"""PS-inversion probe: the fixed harmonic of the floor-Hardy axis in the m-variable.

Phase-0 of docs/problems/juggler_ps_inversion_barrier.md.

Exact identity (no approximation): with v(n) = floor(n^{3/2}) and

    r(m) = #{n : v(n) = m} = ceil((m+1)^{2/3}) - ceil(m^{2/3}) in {0, 1},

the fixed-harmonic Weyl sum of the rate-free tower target satisfies

    S_c(N) := sum_{n<=N} e(c v(n)^{9/4}) = sum_{m<=v(N)} r(m) e(c m^{9/4}).

Splitting r(m) = w(m) + [psi(-(m+1)^{2/3}) - psi(-m^{2/3})] with
w(m) = (m+1)^{2/3} - m^{2/3} and psi(t) = {t} - 1/2:

* the smooth main term W(M) = sum_{m<=M} w(m) e(c m^{9/4}) has unconditional
  power savings O_c(M^{13/24}) = O_c(N^{13/16}) (van der Corput third-derivative
  test on dyadic blocks against the decreasing weight);
* after Vaaler truncation at J = M^{2/5} the whole door is the family of clean
  two-monomial sums T_j(M) = sum_{m<=M} e(c m^{9/4} - j m^{2/3}), which must be
  o(M^{2/3}) -- BELOW the Piatetski-Shapiro density.  Exponent pairs give
  M^{(5/4)p+q}; the density barrier needs (5/4)p + q < 2/3 = 0.666...,
  while van der Corput derivative tests give 7/8 and the known hull bottoms
  out at 95/112 ~ 0.848 (Bourgain's pair (13/84, 55/84)).  The exponent-pair
  conjecture point (0, 1/2) would prove the axis with power savings.

The probe seals the identity exactly, measures |S_c(N)|/sqrt(N), measures
W(M) against the proved M^{13/24} envelope, and scans T_j against sqrt(M)
and the density scale M^{2/3}.  All m^{9/4} fractional parts are exact
big-integer fourth roots (floor(m^{9/4} 2^s) = isqrt(isqrt(m^9 << 4s)));
no floating-point phase at amplitude ~10^15 is ever used.
"""

from __future__ import annotations

import json
import math
import sys
from math import cos, isqrt, sin
from pathlib import Path

SBITS = 64
SCALE = 1 << SBITS
TWO_SCALE = SCALE << 1
SHIFT4 = 4 * SBITS
TWO_PI = 2.0 * math.pi

DATA_DIR = Path("data/research/juggler/ps_inversion_barrier")

# Barrier constants (exponents of M).
DENSITY_EXPONENT = 2.0 / 3.0
MAIN_TERM_EXPONENT = 13.0 / 24.0
VDC_EXPONENT = 7.0 / 8.0
BOURGAIN_PAIR = (13.0 / 84.0, 55.0 / 84.0)
EPC_PAIR = (0.0, 0.5)


def pair_functional(pair: tuple[float, float]) -> float:
    """(5/4)p + q: the block exponent of T_j under the exponent pair (p, q)."""
    p, q = pair
    return 1.25 * p + q


def floor_m94_scaled(m: int, sbits: int = SBITS) -> int:
    """Exact floor(m^{9/4} * 2^sbits) via two integer square roots."""
    return isqrt(isqrt((m**9) << (4 * sbits)))


def frac_half_m94(m: int) -> float:
    """{m^{9/4} / 2} from the exact scaled floor (harmonic c = 1/2)."""
    t = floor_m94_scaled(m)
    return (t % TWO_SCALE) / TWO_SCALE


def frac_one_m94(m: int) -> float:
    """{m^{9/4}} from the exact scaled floor (harmonic c = 1)."""
    t = floor_m94_scaled(m)
    return (t % SCALE) / SCALE


def icbrt(y: int) -> int:
    """floor(y^{1/3}) for y >= 0, Newton seeded by float, exact adjust."""
    if y < 0:
        raise ValueError("icbrt needs y >= 0")
    if y == 0:
        return 0
    x = int(round(float(y) ** (1.0 / 3.0))) if y.bit_length() < 900 else 1 << (
        (y.bit_length() + 2) // 3
    )
    if x <= 0:
        x = 1
    for _ in range(80):
        x_next = (2 * x + y // (x * x)) // 3
        if x_next >= x:
            break
        x = x_next
    while x * x * x > y:
        x -= 1
    while (x + 1) ** 3 <= y:
        x += 1
    return x


def ceil_cbrt(y: int) -> int:
    """Smallest integer n with n^3 >= y."""
    n = icbrt(y)
    return n if n**3 >= y else n + 1


def r_of_m(m: int) -> int:
    """r(m) = #{n : floor(n^{3/2}) = m} = ceil((m+1)^{2/3}) - ceil(m^{2/3})."""
    return ceil_cbrt((m + 1) ** 2) - ceil_cbrt(m**2)


def v_of_n(n: int) -> int:
    """v(n) = floor(n^{3/2})."""
    return isqrt(n**3)


def seal_identity(n_max: int) -> dict:
    """Exact seal: n-sum equals the r(m)-weighted m-sum, c = 1/2."""
    re_n = im_n = 0.0
    for n in range(1, n_max + 1):
        phase = TWO_PI * frac_half_m94(v_of_n(n))
        re_n += cos(phase)
        im_n += sin(phase)
    m_max = v_of_n(n_max)
    re_m = im_m = 0.0
    r_total = 0
    r_bad = 0
    for m in range(1, m_max + 1):
        r = r_of_m(m)
        if r not in (0, 1):
            r_bad += 1
        r_total += r
        if r:
            phase = TWO_PI * frac_half_m94(m)
            re_m += cos(phase)
            im_m += sin(phase)
    return {
        "n_max": n_max,
        "m_max": m_max,
        "abs_gap": math.hypot(re_n - re_m, im_n - im_m),
        "r_sum_equals_N": r_total == n_max,
        "r_outside_01": r_bad,
    }


def weyl_sums_n(n_max: int) -> list[dict]:
    """|S_c(N)| checkpoints (all n and odd n; c = 1/2 and c = 1)."""
    acc = {key: [0.0, 0.0] for key in ("all_half", "all_one", "odd_half", "odd_one")}
    checkpoints: list[dict] = []
    next_cp = 1024
    for n in range(1, n_max + 1):
        t = floor_m94_scaled(v_of_n(n))
        ph_half = TWO_PI * ((t % TWO_SCALE) / TWO_SCALE)
        ph_one = TWO_PI * ((t % SCALE) / SCALE)
        ch, sh = cos(ph_half), sin(ph_half)
        co, so = cos(ph_one), sin(ph_one)
        acc["all_half"][0] += ch
        acc["all_half"][1] += sh
        acc["all_one"][0] += co
        acc["all_one"][1] += so
        if n & 1:
            acc["odd_half"][0] += ch
            acc["odd_half"][1] += sh
            acc["odd_one"][0] += co
            acc["odd_one"][1] += so
        if n == next_cp or n == n_max:
            root = math.sqrt(n)
            checkpoints.append(
                {
                    "N": n,
                    **{
                        key: {
                            "abs": math.hypot(*acc[key]),
                            "over_sqrt": math.hypot(*acc[key]) / root,
                        }
                        for key in acc
                    },
                }
            )
            next_cp <<= 1
    return checkpoints


def m_scan(m_max: int, js: tuple[int, ...] = (1, 2, 5)) -> list[dict]:
    """Main term W(M) and fluctuation sums T_j(M), c = 1/2, checkpoints."""
    w_re = w_im = 0.0
    t_acc = {j: [0.0, 0.0] for j in js}
    checkpoints: list[dict] = []
    next_cp = 1024
    two_thirds = 2.0 / 3.0
    for m in range(1, m_max + 1):
        f94h = frac_half_m94(m)
        f23 = math.fmod(float(m) ** two_thirds, 1.0)
        w = (m + 1.0) ** two_thirds - float(m) ** two_thirds
        ph = TWO_PI * f94h
        w_re += w * cos(ph)
        w_im += w * sin(ph)
        for j in js:
            phj = TWO_PI * (f94h - j * f23)
            t_acc[j][0] += cos(phj)
            t_acc[j][1] += sin(phj)
        if m == next_cp or m == m_max:
            envelope = float(m) ** MAIN_TERM_EXPONENT
            density = float(m) ** DENSITY_EXPONENT
            root = math.sqrt(m)
            checkpoints.append(
                {
                    "M": m,
                    "absW": math.hypot(w_re, w_im),
                    "W_over_M1324": math.hypot(w_re, w_im) / envelope,
                    "T": {
                        str(j): {
                            "abs": math.hypot(*t_acc[j]),
                            "over_sqrt": math.hypot(*t_acc[j]) / root,
                            "over_density": math.hypot(*t_acc[j]) / density,
                        }
                        for j in js
                    },
                }
            )
            next_cp <<= 1
    return checkpoints


def run_probe(
    seal_n: int = 10_000,
    weyl_n_max: int = 1 << 21,
    m_max: int = 1 << 23,
) -> dict:
    seal = seal_identity(seal_n)
    weyl = weyl_sums_n(weyl_n_max)
    scan = m_scan(m_max)
    barrier = {
        "density_exponent": DENSITY_EXPONENT,
        "main_term_exponent": MAIN_TERM_EXPONENT,
        "main_term_exponent_in_N": 1.5 * MAIN_TERM_EXPONENT,
        "vdc_exponent": VDC_EXPONENT,
        "bourgain_functional": pair_functional(BOURGAIN_PAIR),
        "epc_functional": pair_functional(EPC_PAIR),
        "needed": "(5/4)p + q < 2/3",
    }
    green = (
        seal["abs_gap"] < 1e-8
        and seal["r_sum_equals_N"]
        and seal["r_outside_01"] == 0
        and pair_functional(BOURGAIN_PAIR) > DENSITY_EXPONENT
    )
    summary = {
        "id": "juggler_ps_inversion_barrier",
        "verdict": "PS_INVERSION_BARRIER_GREEN" if green else "PS_INVERSION_BARRIER_RED",
        "seal": seal,
        "weyl_n_checkpoints": weyl,
        "m_scan_checkpoints": scan,
        "barrier": barrier,
    }
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    out = DATA_DIR / "summary.json"
    out.write_text(json.dumps(summary, indent=1), encoding="utf-8")
    return summary


def main(argv: list[str]) -> None:
    kwargs = {}
    if len(argv) > 1:
        kwargs["weyl_n_max"] = int(argv[1])
    if len(argv) > 2:
        kwargs["m_max"] = int(argv[2])
    summary = run_probe(**kwargs)
    seal = summary["seal"]
    print(f"seal: |S_n - S_m| = {seal['abs_gap']:.3e} at N = {seal['n_max']}")
    last_w = summary["weyl_n_checkpoints"][-1]
    print(
        f"S(N): N = {last_w['N']}, |S_half(all)|/sqrt(N) = "
        f"{last_w['all_half']['over_sqrt']:.3f}, odd = {last_w['odd_half']['over_sqrt']:.3f}"
    )
    last_m = summary["m_scan_checkpoints"][-1]
    print(
        f"W(M): M = {last_m['M']}, |W|/M^(13/24) = {last_m['W_over_M1324']:.4f}"
    )
    for j, row in last_m["T"].items():
        print(
            f"T_{j}(M): |T|/sqrt(M) = {row['over_sqrt']:.3f}, "
            f"|T|/M^(2/3) = {row['over_density']:.4f}"
        )
    print(f"barrier: bourgain {summary['barrier']['bourgain_functional']:.4f} "
          f"vs needed < {summary['barrier']['density_exponent']:.4f}")
    print(summary["verdict"])


if __name__ == "__main__":
    main(sys.argv)
