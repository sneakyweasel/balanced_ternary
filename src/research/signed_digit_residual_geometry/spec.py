"""Geometry session reuses ``SignedDigitResidualSpec``. No geometry engine."""

from research.signed_digit_residual.spec import (
    SignedDigitResidualSpec,
    minimized_state_count,
    raw_state_count,
    signed_digit_spec,
)

INPUT_LENGTH = 8


def geometry_spec(start_remaining: int = INPUT_LENGTH) -> SignedDigitResidualSpec:
    return SignedDigitResidualSpec(
        bound=2,
        gain=1,
        start_remaining=start_remaining,
        name="signed_digit_residual_geometry",
    )


__all__ = [
    "SignedDigitResidualSpec",
    "geometry_spec",
    "minimized_state_count",
    "raw_state_count",
    "signed_digit_spec",
]
