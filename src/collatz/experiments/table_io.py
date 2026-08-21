"""Helpers to write experiment tables as JSONL, plus Parquet when available."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence


def timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def write_rows(
    rows: Sequence[dict[str, Any]],
    output_dir: Path | str,
    stem: str,
) -> dict[str, str]:
    """Write JSONL always. Write Parquet if pyarrow is installed."""
    base = Path(output_dir)
    raw = base / "raw"
    raw.mkdir(parents=True, exist_ok=True)
    stamp = timestamp()
    jsonl_path = raw / f"{stem}_{stamp}.jsonl"
    with jsonl_path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, separators=(",", ":")) + "\n")
    paths = {"jsonl": str(jsonl_path)}
    try:
        import pyarrow as pa
        import pyarrow.parquet as pq

        table = pa.Table.from_pylist(list(rows))
        parquet_path = raw / f"{stem}_{stamp}.parquet"
        pq.write_table(table, parquet_path)
        paths["parquet"] = str(parquet_path)
    except ImportError:
        paths["parquet"] = ""
    return paths
