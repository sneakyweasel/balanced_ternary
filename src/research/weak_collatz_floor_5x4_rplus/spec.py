"""Hint-free packet bounds for the 5x-4 strip. Scout material is not imported."""

from research.linear_constraint_loops.spec import OneVariableLoopSpec, integer_images

DEFAULT_START = 5
INPUT_LENGTH = 16
INTEGER_STATE_CAP = 32


def strip_images(x: int) -> tuple[int, ...]:
    if isinstance(x, bool) or not isinstance(x, int):
        raise TypeError(f"x must be int, got {type(x).__name__}")
    if x < 2:
        return ()
    return integer_images(5 * x - 4, 5 * x - 1, 4)


def map_spec(
    *,
    start: int = DEFAULT_START,
    start_remaining: int = INPUT_LENGTH,
    state_cap: int = INTEGER_STATE_CAP,
) -> OneVariableLoopSpec:
    """Existing OneVariableLoopSpec with the stored blind-packet seed and budget."""

    return OneVariableLoopSpec(
        name="floor_5x4_strip",
        start=start,
        images=strip_images,
        start_remaining=start_remaining,
        state_cap=state_cap,
    )
