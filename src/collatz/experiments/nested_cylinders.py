"""Nested-cylinder traces along explicit infinite-prefix families."""

from __future__ import annotations

from collatz.compatibility import nested_cylinder_report
from collatz.zero_lift import lift_digit


def all_ones_prefix(m: int) -> tuple[int, ...]:
    if isinstance(m, bool) or not isinstance(m, int) or m < 0:
        raise ValueError(f"m must be an integer >= 0, got {m!r}")
    return (1,) * m


def run_nested_trace(ks: tuple[int, ...]) -> dict[str, object]:
    report = nested_cylinder_report(ks)
    lifts = []
    for i in range(len(ks)):
        parent = ks[:i]
        j = ks[i]
        lifts.append(
            {"i": i, "j": j, "lift_digit": lift_digit(parent, j), "status": "EXACT"}
        )
    return {
        "report": report.format(),
        "R_m": list(report.realizers),
        "lifts": lifts,
        "monotone": report.monotone,
        "status": report.status,
    }
