"""GPU walk-charge DP agrees with the CPU DP and brute force.

Skipped when cupy or a CUDA device is unavailable; the committed
certificates are the CPU records, the GPU is an accelerator.
"""

import math

import pytest

cp = pytest.importorskip("cupy")

try:
    _HAS_GPU = cp.cuda.runtime.getDeviceCount() > 0
except Exception:  # pragma: no cover - driver missing
    _HAS_GPU = False

pytestmark = pytest.mark.skipif(not _HAS_GPU, reason="no CUDA device")


def test_gpu_matches_cpu_and_brute_force_on_tiny_lengths():
    from research.juggler_sequence.cycle_walk_charge import (
        brute_force_budget,
        walk_budget,
    )
    from research.juggler_sequence.cycle_walk_charge_gpu import (
        gpu_walk_budget,
    )

    for length, odd_count in ((10, 7), (12, 8), (14, 9)):
        brute = brute_force_budget(length, odd_count, 500)
        cpu = walk_budget(length, odd_count, 500)["walk_sum"]
        gpu = gpu_walk_budget(length, odd_count, 500)["walk_sum"]
        assert math.isclose(gpu, cpu, rel_tol=1e-12)
        assert math.isclose(gpu, brute, rel_tol=1e-12)


def test_gpu_matches_cpu_at_reduced_base():
    from research.juggler_sequence.cycle_finance import o_min_and_theta
    from research.juggler_sequence.cycle_walk_charge import (
        deficit_D,
        walk_budget,
    )
    from research.juggler_sequence.cycle_walk_charge_gpu import (
        gpu_walk_budget,
    )

    length = 1054
    n = 162_849_449
    odd_count, _ = o_min_and_theta(length)
    log_n_prime = math.log(n) - deficit_D(length, odd_count, n)
    cpu = walk_budget(length, odd_count, n, log_n=log_n_prime)["walk_sum"]
    gpu = gpu_walk_budget(length, odd_count, n, log_n=log_n_prime)["walk_sum"]
    assert math.isclose(gpu, cpu, rel_tol=1e-12)
