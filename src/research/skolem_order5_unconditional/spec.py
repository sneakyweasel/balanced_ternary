"""Hint-free order-5 companion window. Scout material is not imported."""

from research.skolem_lrs.spec import CompanionShiftSpec

LAST_ROW = (4225, -4745, 522, -10, 9)
WINDOW = (-30, -27, 0, 469, 1762)


def map_spec() -> CompanionShiftSpec:
    return CompanionShiftSpec(
        name="companion_shift_order5",
        last_row=LAST_ROW,
        window=WINDOW,
    )
