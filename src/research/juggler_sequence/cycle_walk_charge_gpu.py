"""GPU (CuPy) port of the certified reduced-base walk-charge DP.

Same recurrence as cycle_walk_charge.walk_budget on the eta = 0
certified path: values_k[a] = max(values_{k-1}[a], values_{k-1}[a-1])
+ charge on the feasible (step, odd-count) lattice, with charge
f(u) = exp(-w ln n' - ln(w ln n')), w = max(2^u, 1), u = STEP*a - k,
at the reduced base n' = n e^{-D} of the transport lemma. One fused
fp64 kernel per step, double-buffered; IEEE double precision
throughout, so results agree with the CPU DP to rounding
(observed <= ~1e-13 relative on the committed kill records, at
roughly 450x speed on an RTX 5090).

Optional accelerator only: the committed certificates remain the
CPU records of cycle_walk_charge. Requires cupy and a CUDA device.
Not a halt theorem, not a no-cycle-of-any-length claim.
"""

from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path
from typing import Any

import cupy as cp

from research.juggler_sequence.cycle_finance import (
    EPS_CONST,
    PARITY_REL_GUARD,
    o_min_and_theta,
)
from research.juggler_sequence.cycle_walk_charge import (
    DATA_DIR,
    STEP,
    U_TOL,
    deficit_D,
)

_KERNEL = cp.RawKernel(
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
    const double NEG = __longlong_as_double(0xfff0000000000000LL);
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


def gpu_walk_budget(
    length: int,
    odd_count: int,
    n: int,
    *,
    log_n: float | None = None,
) -> dict[str, Any]:
    """GPU twin of cycle_walk_charge.walk_budget (eta = 0)."""

    if log_n is None:
        log_n = math.log(n)
    started = time.perf_counter()
    width = odd_count + 1
    a_buf = cp.full(width, -math.inf, dtype=cp.float64)
    b_buf = cp.empty(width, dtype=cp.float64)
    a_buf[0] = math.exp(-log_n - math.log(log_n))
    threads = 256
    blocks = (width + threads - 1) // threads
    even_count = length - odd_count
    for k in range(1, length + 1):
        _KERNEL(
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


def gpu_certified_report(
    length: int,
    n0: int,
    *,
    const: float = EPS_CONST,
) -> dict[str, Any]:
    """GPU twin of cycle_walk_charge.certified_report."""

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
        "implementation": (
            "research.juggler_sequence.cycle_walk_charge_gpu"
            ".gpu_walk_budget (CuPy fp64 raw kernel)"
        ),
    }


def main() -> None:
    """CLI: python -m ... <length> <floor> [--write]."""

    length = int(sys.argv[1])
    n0 = int(sys.argv[2])
    report = gpu_certified_report(length, n0)
    print(json.dumps(report, indent=1), flush=True)
    if "--write" in sys.argv:
        out = DATA_DIR / "new_floor_kills" / f"L{length}.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, indent=1), encoding="utf-8")
        print(f"written {out}", flush=True)


if __name__ == "__main__":
    main()
