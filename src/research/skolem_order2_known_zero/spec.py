"""Hint-free order-2 companion window. Scout material is not imported."""

from research.skolem_lrs.spec import CompanionShiftSpec

LAST_ROW = (-2, 3)
WINDOW = (-7, -6)


def map_spec() -> CompanionShiftSpec:
    return CompanionShiftSpec(
        name="companion_shift_order2",
        last_row=LAST_ROW,
        window=WINDOW,
    )
