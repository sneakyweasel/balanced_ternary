"""Hint-free order-6 companion window. Scout material is not imported."""

from research.skolem_lrs.spec import CompanionShiftSpec

LAST_ROW = (-4225, 8970, -5267, 532, -19, 10)
WINDOW = (12, 49, 374, 6003, 21520, 150773)


def map_spec() -> CompanionShiftSpec:
    return CompanionShiftSpec(
        name="companion_shift_order6",
        last_row=LAST_ROW,
        window=WINDOW,
    )
