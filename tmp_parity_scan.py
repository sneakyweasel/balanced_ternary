"""Parity leftovers at the prospective floor 162849448 for L in (2e5, 6e5]."""

import json

from research.juggler_sequence.cycle_finance import (
    EPS_CONST,
    parity_excludes,
    parity_rhs_upper,
)
from research.juggler_sequence.cycle_floor_sensitivity import iter_o_min

N0 = 162_849_448
L_MAX = 600_000

rows = []
for length, odd_count, theta in iter_o_min(L_MAX):
    if length <= 176_250:
        continue
    if parity_excludes(length, odd_count, theta, N0):
        continue
    rhs = parity_rhs_upper(N0 + 1, length, odd_count, const=EPS_CONST)
    rows.append({
        "L": length,
        "o": odd_count,
        "theta": theta,
        "parity_rhs": rhs,
        "required_improvement": rhs / theta if theta > 0 else None,
    })

print(json.dumps({"floor": N0, "l_max": L_MAX, "leftovers": rows}, indent=1))
