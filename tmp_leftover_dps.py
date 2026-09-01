"""Certified walk-charge kills for the parity leftovers at floor 162849448.

Runs one DP per leftover length in parallel; writes one JSON per
length so partial progress survives interruption.
"""

import json
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

OUT = Path("data/research/juggler/cycle_walk_charge/new_floor_kills")
N0 = 162_849_448
LENGTHS = [
    202_032, 226_759, 252_540, 277_267, 303_048, 327_775,
    352_502, 353_556, 378_283, 403_010, 404_064, 428_791,
    453_518, 454_572,
]


def run_one(length: int) -> dict:
    from research.juggler_sequence.cycle_walk_charge import certified_report

    report = certified_report(length, N0)
    path = OUT / f"L{length}.json"
    path.write_text(json.dumps(report, indent=1), encoding="utf-8")
    return report


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    todo = [
        length for length in LENGTHS
        if not (OUT / f"L{length}.json").exists()
    ]
    print(f"leftover DPs to run: {len(todo)}", flush=True)
    with ProcessPoolExecutor(max_workers=14) as pool:
        futures = {pool.submit(run_one, length): length for length in todo}
        for future in as_completed(futures):
            report = future.result()
            print(
                f"L={report['length']} margin={report['kill_margin']:.3f} "
                f"excludes={report['certified_excludes']} "
                f"({report['elapsed_s']:.0f}s)",
                flush=True,
            )


if __name__ == "__main__":
    main()
