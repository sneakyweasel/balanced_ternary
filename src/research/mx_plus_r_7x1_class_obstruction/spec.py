"""Hint-free packet bounds for accelerated 7x+1. Scout material is not imported."""

from research.mx_plus_r.spec import MxPlusRSpec

CONTROL = 0
DEFAULT_START = 3
INPUT_LENGTH = 16
INTEGER_STATE_CAP = 32


def map_spec(
    *,
    start: int = DEFAULT_START,
    start_remaining: int = INPUT_LENGTH,
    state_cap: int = INTEGER_STATE_CAP,
) -> MxPlusRSpec:
    """Existing MxPlusRSpec with the stored blind-packet seed and budget."""

    return MxPlusRSpec(
        m=7,
        r=1,
        start=start,
        start_remaining=start_remaining,
        state_cap=state_cap,
    )
