"""Host PE certification. GPU Kernel A never writes PE_CERTIFIED."""

from __future__ import annotations

from typing import Any

from research.juggler_sequence.atlas.packed import pack_word, word_id
from research.juggler_sequence.atlas.schema import (
    LANG_PE_CERTIFIED,
    LANG_PE_RUN,
    LANG_PERSISTENT,
    PE_CERTIFIED,
    PE_PROXY,
)
from research.juggler_sequence.expansion_slack import walk_pe_run
from research.juggler_sequence.residual_chain import residual_excursion
from research.juggler_sequence.two_block_residual import (
    classify_step,
    odd_odd_starts,
)


def classify_persistent_odd(x: int) -> dict[str, Any] | None:
    raw = residual_excursion(x)
    if raw is None:
        return None
    row = classify_step(x, raw)
    if not row["persistent"]:
        return None
    return row


def classify_persistent_expanding(x: int) -> dict[str, Any] | None:
    row = classify_persistent_odd(x)
    if row is None or not row["expanding"]:
        return None
    return row


def pe_certified_records(
    *,
    n_max: int,
    search_id: str,
    pe_definition: str = PE_CERTIFIED,
) -> dict[str, list[dict[str, Any]]]:
    """Scan odd-odd starts with the repository PE predicate.

    ``PE_PROXY`` is rejected. Milestone 1 writes only ``PE_CERTIFIED``.
    """

    if pe_definition == PE_PROXY:
        raise ValueError("PE_PROXY must not be written in Milestone 1")
    if pe_definition != PE_CERTIFIED:
        raise ValueError(f"unknown pe_definition {pe_definition!r}")

    certified: list[dict[str, Any]] = []
    persistent: list[dict[str, Any]] = []
    runs: list[dict[str, Any]] = []
    seen_pe: set[int] = set()
    seen_run: set[str] = set()
    for x in odd_odd_starts(n_max):
        raw = residual_excursion(x)
        if raw is None:
            continue
        row = classify_step(x, raw)
        length, packed = pack_word(row["word"])
        wid = word_id(length, packed)
        if row["persistent"]:
            persistent.append(
                {
                    "language_id": LANG_PERSISTENT,
                    "word_id": wid,
                    "word": row["word"],
                    "min_n": x,
                    "end_state": row["y"],
                    "a": row["a"],
                    "b": row["b"],
                    "pe_definition": PE_CERTIFIED,
                    "search_id": search_id,
                }
            )
        if row["persistent"] and row["expanding"] and x not in seen_pe:
            seen_pe.add(x)
            certified.append(
                {
                    "language_id": LANG_PE_CERTIFIED,
                    "word_id": wid,
                    "word": row["word"],
                    "min_n": x,
                    "end_state": row["y"],
                    "a": row["a"],
                    "b": row["b"],
                    "scan_limit": n_max,
                    "pe_definition": PE_CERTIFIED,
                    "search_id": search_id,
                }
            )
        run = walk_pe_run(x)
        if not run:
            continue
        run_word = "".join(block["word"] for block in run)
        if run_word in seen_run:
            continue
        seen_run.add(run_word)
        rlen, rpacked = pack_word(run_word)
        runs.append(
            {
                "language_id": LANG_PE_RUN,
                "word_id": word_id(rlen, rpacked),
                "word": run_word,
                "min_n": x,
                "end_state": run[-1]["y"],
                "scan_limit": n_max,
                "pe_definition": PE_CERTIFIED,
                "search_id": search_id,
                "block_count": len(run),
            }
        )
    return {
        "pe_certified": certified,
        "persistent": persistent,
        "pe_run": runs,
    }
