"""Hint-free packet bounds for the three-branch map. Scout material is not imported."""

from research.linear_constraint_loops.spec import OneVariableLoopSpec

DEFAULT_START = 1
SECOND_START = 5
INPUT_LENGTH = 16
INTEGER_STATE_CAP = 32


def map_images(x: int) -> tuple[int, ...]:
    if isinstance(x, bool) or not isinstance(x, int):
        raise TypeError(f"x must be int, got {type(x).__name__}")
    residue = x % 3
    if residue == 0:
        return (2 * x,)
    if residue == 1:
        return ((7 * x + 2) // 3,)
    return ((x - 2) // 3,)


def map_spec(
    *,
    start: int = DEFAULT_START,
    start_remaining: int = INPUT_LENGTH,
    state_cap: int = INTEGER_STATE_CAP,
) -> OneVariableLoopSpec:
    """Existing OneVariableLoopSpec with the stored blind-packet seed and budget."""

    return OneVariableLoopSpec(
        name="mod3_three_branch",
        start=start,
        images=map_images,
        start_remaining=start_remaining,
        state_cap=state_cap,
    )
