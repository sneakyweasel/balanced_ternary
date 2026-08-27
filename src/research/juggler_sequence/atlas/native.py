"""Optional native census binary. Python remains the exact reference."""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
BIN_NAMES = ("juggler-atlas-census.exe", "juggler-atlas-census")


def find_binary() -> Path | None:
    env = os.environ.get("JUGGLER_ATLAS_BIN")
    if env:
        path = Path(env)
        return path if path.is_file() else None
    for name in BIN_NAMES:
        found = shutil.which(name)
        if found:
            return Path(found)
    build = REPO_ROOT / "atlas" / "build"
    for name in BIN_NAMES:
        candidate = build / name
        if candidate.is_file():
            return candidate
        for nested in build.rglob(name):
            if nested.is_file():
                return nested
    return None


def run_census(
    *,
    k_max: int,
    n_max: int,
    n_begin: int = 1,
    backend: str = "cpu",
    output: Path,
    binary: Path | None = None,
) -> dict[str, str | int]:
    exe = binary or find_binary()
    if exe is None:
        raise FileNotFoundError("juggler-atlas-census is not built")
    output.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        str(exe),
        "--k-max",
        str(k_max),
        "--n-max",
        str(n_max),
        "--n-begin",
        str(n_begin),
        "--backend",
        backend,
        "--output",
        str(output),
    ]
    proc = subprocess.run(cmd, check=True, capture_output=True, text=True)
    return {
        "binary": str(exe),
        "backend": backend,
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


def parse_census_tsv(path: Path) -> dict[str, object]:
    """Parse the native TSV dump into dense Python tables."""

    from research.juggler_sequence.atlas.packed import dense_index, dense_size

    k_max = 0
    n_max = 0
    n_begin = 1
    backend = "cpu"
    overflow = 0
    rows: list[tuple[int, int, int | None, int | None]] = []
    with path.open(encoding="utf-8") as fh:
        for raw in fh:
            line = raw.rstrip("\n\r")
            if not line.strip():
                continue
            if line.startswith("#"):
                body = line[1:].strip()
                if "=" in body:
                    key, val = body.split("=", 1)
                    if key == "k_max":
                        k_max = int(val)
                    elif key == "n_max":
                        n_max = int(val)
                    elif key == "n_begin":
                        n_begin = int(val)
                    elif key == "backend":
                        backend = val
                    elif key == "overflow_count":
                        overflow = int(val)
                continue
            if line.startswith("length"):
                continue
            parts = line.rstrip("\n\r").split("\t")
            if len(parts) < 2:
                continue
            length = int(parts[0])
            packed = int(parts[1])
            min_n = int(parts[2]) if len(parts) > 2 and parts[2] else None
            min_exp = int(parts[3]) if len(parts) > 3 and parts[3] else None
            rows.append((length, packed, min_n, min_exp))
    size = dense_size(k_max)
    min_n_tbl: list[int | None] = [None] * size
    min_exp_tbl: list[int | None] = [None] * size
    for length, packed, min_n, min_exp in rows:
        idx = dense_index(length, packed)
        min_n_tbl[idx] = min_n
        min_exp_tbl[idx] = min_exp
    return {
        "k_max": k_max,
        "n_max": n_max,
        "n_begin": n_begin,
        "backend": backend,
        "overflow_count": overflow,
        "min_n": min_n_tbl,
        "min_exp": min_exp_tbl,
    }
