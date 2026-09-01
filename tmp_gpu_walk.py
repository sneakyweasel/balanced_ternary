"""GPU (CuPy) port of the certified reduced-base walk-charge DP.

Same recurrence as cycle_walk_charge.walk_budget (eta = 0 certified
path): values_k[a] = max(values_{k-1}[a], values_{k-1}[a-1]) + charge
on the feasible lattice, charge f(u) = exp(-w ln n' - ln(w ln n')),
w = max(2^u, 1), u = STEP*a - k. One fused kernel per step,
double-buffered. Validation: brute force (tiny), CPU DP (small),
stored certified record L=176251 at floor 162849448.
"""

import json
import math
import sys
import time
from pathlib import Path

import cupy as cp

from research.juggler_sequence.cycle_finance import (
    EPS_CONST,
    PARITY_REL_GUARD,
    o_min_and_theta,
)
from research.juggler_sequence.cycle_walk_charge import (
    MU,
    STEP,
    U_TOL,
    deficit_D,
    walk_budget,
    brute_force_budget,
)

KERNEL = cp.RawKernel(
    r"""
extern "C" __global__
void walk_step(const double* prev, double* out,
               const long long width, const long long k,
               const long long length, const long long odd_count,
               const long long even_count,
               const double step, const double u_tol,
               const double log_n)
{
    long long a = (long long)blockIdx.x * blockDim.x + threadIdx.x;
    if (a >= width) return;
    const double NEG = -INFINITY;
    double m = prev[a];
    if (a > 0) {
        double up = prev[a - 1];
        if (up > m) m = up;
    }
    double u = step * (double)a - (double)k;
    long long amax = odd_count < k ? odd_count : k;
    bool feasible = (u >= -u_tol) && (a <= amax)
                    && ((k - a) <= even_count);
    if (!feasible) { out[a] = NEG; return; }
    if (k < length && m > NEG) {
        double uc = u > 0.0 ? u : 0.0;
        double w = exp2(uc);
        if (w < 1.0) w = 1.0;
        m += exp(-w * log_n - log(w * log_n));
    }
    out[a] = m;
}
""",
    "walk_step",
)


def gpu_walk_budget(length, odd_count, n, *, log_n=None):
    if log_n is None:
        log_n = math.log(n)
    started = time.perf_counter()
    width = odd_count + 1
    neg = -math.inf
    a_buf = cp.full(width, neg, dtype=cp.float64)
    b_buf = cp.empty(width, dtype=cp.float64)
    a_buf[0] = math.exp(-log_n - math.log(log_n))
    threads = 256
    blocks = (width + threads - 1) // threads
    even_count = length - odd_count
    for k in range(1, length + 1):
        KERNEL(
            (blocks,), (threads,),
            (a_buf, b_buf, width, k, length, odd_count, even_count,
             STEP, U_TOL, log_n),
        )
        a_buf, b_buf = b_buf, a_buf
    best = float(a_buf[odd_count])
    return {
        "length": length,
        "odd_count": odd_count,
        "even_count": even_count,
        "n": n,
        "walk_sum": best,
        "elapsed_s": time.perf_counter() - started,
    }


def gpu_certified_report(length, n0, *, const=EPS_CONST):
    odd_count, theta = o_min_and_theta(length)
    n = n0 + 1
    deficit = deficit_D(length, odd_count, n)
    log_n_prime = math.log(n) - deficit
    budget = gpu_walk_budget(length, odd_count, n, log_n=log_n_prime)
    rhs = const * budget["walk_sum"] * (1.0 + PARITY_REL_GUARD)
    return {
        "length": length,
        "odd_count": odd_count,
        "theta": theta,
        "floor": n0,
        "const": const,
        "deficit_D": deficit,
        "walk_rhs_certified": rhs,
        "kill_margin": theta / rhs if rhs > 0 else math.inf,
        "certified_excludes": theta * (1.0 - PARITY_REL_GUARD) > rhs,
        "elapsed_s": budget["elapsed_s"],
        "device": cp.cuda.runtime.getDeviceProperties(0)["name"].decode(),
        "implementation": "tmp_gpu_walk.gpu_walk_budget (CuPy fp64 raw kernel)",
    }


def validate():
    print("GPU:", cp.cuda.runtime.getDeviceProperties(0)["name"].decode(),
          flush=True)
    n = 162_849_449

    # 1. tiny lengths against brute force and CPU DP
    for length, odd_count in ((10, 7), (12, 8), (14, 9)):
        bf = brute_force_budget(length, odd_count, 500)
        cpu = walk_budget(length, odd_count, 500)["walk_sum"]
        gpu = gpu_walk_budget(length, odd_count, 500)["walk_sum"]
        rel_c = abs(gpu - cpu) / abs(cpu)
        rel_b = abs(gpu - bf) / abs(bf)
        print(f"L={length} o={odd_count}: brute={bf:.15e} cpu={cpu:.15e} "
              f"gpu={gpu:.15e} rel(gpu,cpu)={rel_c:.1e} "
              f"rel(gpu,brute)={rel_b:.1e}", flush=True)
        assert rel_c < 1e-12 and rel_b < 1e-12

    # 2. moderate length, CPU vs GPU at the reduced base
    length = 1054
    odd_count, _ = o_min_and_theta(length)
    d = deficit_D(length, odd_count, n)
    lnp = math.log(n) - d
    cpu = walk_budget(length, odd_count, n, log_n=lnp)["walk_sum"]
    gpu = gpu_walk_budget(length, odd_count, n, log_n=lnp)["walk_sum"]
    rel = abs(gpu - cpu) / abs(cpu)
    print(f"L=1054 reduced base: cpu={cpu:.15e} gpu={gpu:.15e} "
          f"rel={rel:.1e}", flush=True)
    assert rel < 1e-12

    # 3. stored certified record L=176251 at floor 162849448
    stored = json.loads(Path(
        "data/research/juggler/cycle_walk_charge/new_floor_kills/"
        "L176251.json").read_text())
    rep = gpu_certified_report(176251, 162_849_448)
    rel = abs(rep["walk_rhs_certified"] - stored["walk_rhs_certified"]) \
        / stored["walk_rhs_certified"]
    print(f"L=176251: stored rhs={stored['walk_rhs_certified']:.15e} "
          f"gpu rhs={rep['walk_rhs_certified']:.15e} rel={rel:.1e} "
          f"margin gpu={rep['kill_margin']:.6f} "
          f"stored={stored['kill_margin']:.6f} "
          f"({rep['elapsed_s']:.1f}s gpu vs {stored['elapsed_s']:.0f}s cpu)",
          flush=True)
    assert rel < 1e-9
    print("validation OK", flush=True)


def main():
    validate()
    if "--run-478245" in sys.argv:
        rep = gpu_certified_report(478245, 162_849_448)
        print(json.dumps(rep, indent=1), flush=True)
        out = Path("data/research/juggler/cycle_walk_charge/"
                   "new_floor_kills/L478245.json")
        out.write_text(json.dumps(rep, indent=1), encoding="utf-8")
        print(f"written {out}", flush=True)


if __name__ == "__main__":
    main()
