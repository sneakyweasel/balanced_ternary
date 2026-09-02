"""N350 descent-floor extension with a 5-minute heartbeat.

Not a halt proof. Resume-safe; do not run a DP pool alongside this.
"""

from __future__ import annotations

import json
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

from research.juggler_sequence.cycle_finance import PROGRESS_CHUNK, PROGRESS_PATH
from research.juggler_sequence.cycle_floor_sensitivity import (
    VERIFY_DIR,
    verify_floor_certified,
)

N0 = 350_000_000
N_FROM = 162_849_449
WORKERS = 4
BIT_CAP = 1_000_000_000
HEARTBEAT_S = 300


def expected_chunks(n_from: int, n_top: int) -> int:
    walk_from = max(3, n_from if n_from % 2 == 1 else n_from + 1)
    return (n_top - walk_from) // PROGRESS_CHUNK + 1


def _write_heartbeat(
    out_dir: Path,
    chunks_total: int,
    last_done: int,
    started: float,
) -> int:
    chunks_dir = out_dir / "chunks"
    done = len(list(chunks_dir.glob("*.json"))) if chunks_dir.is_dir() else 0
    progress: dict = {}
    if PROGRESS_PATH.is_file():
        try:
            progress = json.loads(PROGRESS_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            progress = {}
    elapsed = time.perf_counter() - started
    remaining = max(0, chunks_total - done)
    rate = done / elapsed if elapsed > 0 and done > 0 else 0.0
    eta_s = remaining / rate if rate > 0 else 0.0
    row = {
        "iso": datetime.now(timezone.utc).isoformat(),
        "chunks_done": done,
        "chunks_total": chunks_total,
        "extension_pct": 100.0 * done / chunks_total if chunks_total else 100.0,
        "max_bits": progress.get("max_bits"),
        "hardest_seed": progress.get("hardest_seed"),
        "failure_count": progress.get("failure_count"),
        "workers": progress.get("workers", WORKERS),
        "elapsed": progress.get("elapsed"),
        "eta": progress.get("eta"),
        "heartbeat_eta_s": eta_s,
        "stalled": last_done >= 0 and done == last_done,
    }
    log_path = out_dir / "heartbeat.jsonl"
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, separators=(",", ":")) + "\n")
    print(
        f"heartbeat {row['extension_pct']:.1f}%  "
        f"chunks={done}/{chunks_total}  "
        f"bits={row['max_bits']}  fail={row['failure_count']}  "
        f"stalled={row['stalled']}",
        flush=True,
    )
    return done


def heartbeat_loop(
    stop: threading.Event,
    out_dir: Path,
    chunks_total: int,
    started: float,
) -> None:
    last_done = _write_heartbeat(out_dir, chunks_total, -1, started)
    while not stop.wait(HEARTBEAT_S):
        last_done = _write_heartbeat(out_dir, chunks_total, last_done, started)


def main() -> None:
    out_dir = VERIFY_DIR / f"N{N0}"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "chunks").mkdir(parents=True, exist_ok=True)
    chunks_total = expected_chunks(N_FROM, N0)
    started = time.perf_counter()
    stop = threading.Event()
    thread = threading.Thread(
        target=heartbeat_loop,
        args=(stop, out_dir, chunks_total, started),
        daemon=True,
        name="n350-heartbeat",
    )
    thread.start()
    try:
        cert = verify_floor_certified(
            N0,
            n_from=N_FROM,
            workers=WORKERS,
            bit_cap=BIT_CAP,
            resume=True,
            out_dir=out_dir,
        )
    finally:
        stop.set()
        _write_heartbeat(out_dir, chunks_total, -1, started)
    keys = (
        "N0",
        "n_from",
        "verified",
        "odds_walked",
        "chunk_count",
        "max_stopping_time",
        "hardest_seed",
        "max_bits",
        "max_bits_seed",
        "sha256_chunks",
        "step_failures",
        "bit_failures",
        "other_failures",
    )
    print(json.dumps({k: cert[k] for k in keys}, indent=1), flush=True)


if __name__ == "__main__":
    main()
