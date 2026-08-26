"""Identifier-aware literature-leak matching. Package ids are not leaks."""

from __future__ import annotations

import re

DEFAULT_ALLOWLIST: tuple[str, ...] = (
    "skolem_lrs",
    "aliquot_dynamics",
    "linear_constraint_loops",
    "bb5_map",
    "engine_campaign",
    "engine_memory",
    "target_board",
    "companion_shift",
    "CompanionShift",
    "vector_affine",
    "matrix_word_invariant",
    "switching_affine_z2_origin",
    "two_path_z2",
    "skolem_order2_known_zero",
    "companion_shift_order2",
    "research_strategy",
    "StrategyPlanner",
    "ResearchHypothesis",
    "global_inductive",
    "InvariantCertificate",
    "RankingCertificate",
)


def leak_hits(
    source: str,
    forbidden: tuple[str, ...],
    *,
    allowlist: tuple[str, ...] = DEFAULT_ALLOWLIST,
) -> tuple[str, ...]:
    """Return forbidden tokens that occur outside allowlisted identifiers.

    ``skolem_lrs`` as a problem id does not count as a ``skolem`` leak.
    A bare ``Skolem`` in adapter/spec source still does.
    """

    masked = source
    for token in sorted(allowlist, key=len, reverse=True):
        if not token:
            continue
        masked = masked.replace(token, " " * len(token))
    hits: list[str] = []
    for token in forbidden:
        if not token:
            continue
        if token in masked:
            hits.append(token)
            continue
        if re.search(rf"(?<![A-Za-z0-9_]){re.escape(token)}(?![A-Za-z0-9_])", masked):
            hits.append(token)
    return tuple(hits)


def adapter_is_blind(
    source: str,
    forbidden: tuple[str, ...],
    *,
    allowlist: tuple[str, ...] = DEFAULT_ALLOWLIST,
    scout_module: str = "",
) -> bool:
    if scout_module:
        for line in source.splitlines():
            stripped = line.strip()
            if scout_module in stripped and not stripped.startswith("#"):
                return False
    return leak_hits(source, forbidden, allowlist=allowlist) == ()
