"""Hidden branching systems for frozen-engine diagnostics. Not an attack."""

from __future__ import annotations

from research.linear_constraint_loops.spec import RelationLoopSpec, _require_int


def two_affine_images(x: int) -> tuple[int, ...]:
    x = _require_int(x, "x")
    return (2 * x + 1, x - 2)


def stay_or_decrement_images(x: int) -> tuple[int, ...]:
    x = _require_int(x, "x")
    if x < 1:
        return ()
    return (x, x - 1)


def dual_decrement_images(x: int) -> tuple[int, ...]:
    x = _require_int(x, "x")
    if x < 1:
        return ()
    if x == 1:
        return (0,)
    return (x - 1, x - 2)


def decrement_or_double_images(x: int) -> tuple[int, ...]:
    x = _require_int(x, "x")
    if x < 1:
        return ()
    return (x - 1, 2 * x)


def two_affine_spec(*, start: int = 3) -> RelationLoopSpec:
    return RelationLoopSpec(name="hidden_nondet_two_affine", start=start, images=two_affine_images)


def stay_or_decrement_spec(*, start: int = 4) -> RelationLoopSpec:
    return RelationLoopSpec(
        name="hidden_nondet_stay_or_decrement",
        start=start,
        images=stay_or_decrement_images,
    )


def dual_decrement_spec(*, start: int = 6) -> RelationLoopSpec:
    return RelationLoopSpec(
        name="hidden_nondet_dual_decrement",
        start=start,
        images=dual_decrement_images,
    )


def decrement_or_double_spec(*, start: int = 3) -> RelationLoopSpec:
    return RelationLoopSpec(
        name="hidden_nondet_decrement_or_double",
        start=start,
        images=decrement_or_double_images,
    )
