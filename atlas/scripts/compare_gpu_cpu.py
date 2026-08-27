"""Compare native CUDA/CPU census tables to the Python exact reference."""

from __future__ import annotations

import sys
import time
from pathlib import Path

from research.juggler_sequence.atlas.cpu_census import census
from research.juggler_sequence.atlas.native import find_binary, parse_census_tsv, run_census
from research.juggler_sequence.atlas.packed import dense_index, pack_word
from research.juggler_sequence.atlas.validate import compare_dense_allow_overflow


def check(k_max: int, n_max: int, backend: str, out_dir: Path) -> int:
    binary = find_binary()
    if binary is None:
        print("juggler-atlas-census is not built")
        return 2
    dump = out_dir / f"{backend}_k{k_max}_n{n_max}.tsv"
    t0 = time.perf_counter()
    run_census(
        k_max=k_max,
        n_max=n_max,
        backend=backend,
        output=dump,
        binary=binary,
    )
    native_s = time.perf_counter() - t0
    parsed = parse_census_tsv(dump)
    t1 = time.perf_counter()
    py_min, _, _ = census(k_max=k_max, n_max=n_max)
    py_s = time.perf_counter() - t1
    errors = compare_dense_allow_overflow(
        py_min,
        parsed["min_n"],  # type: ignore[arg-type]
        overflow_count=int(parsed["overflow_count"]),
        label=backend,
    )
    idx = dense_index(*pack_word("OOE"))
    print(
        f"{backend} k={k_max} n={n_max} overflow={parsed['overflow_count']} "
        f"errors={len(errors)} ooe={parsed['min_n'][idx]}/{py_min[idx]} "
        f"native_s={native_s:.3f} py_s={py_s:.3f}"
    )
    for err in errors[:8]:
        print(" ", err)
    return 1 if errors else 0


def main(argv: list[str]) -> int:
    out_dir = Path(argv[1]) if len(argv) > 1 else Path("_atlas_gpu_check")
    out_dir.mkdir(parents=True, exist_ok=True)
    status = 0
    for k_max, n_max, backend in (
        (8, 10_000, "cuda"),
        (12, 100_000, "cuda"),
        (12, 1_000_000, "cuda"),
    ):
        status |= check(k_max, n_max, backend, out_dir)
    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv))
