"""Compatibility shim. Canonical implementation: :mod:`bt.representation`."""

from bt.representation import *  # noqa: F403
from bt.representation import (
    BalancedTernary,
    CHAR_TO_DIGIT,
    DIGIT_TO_CHAR,
    WordLike,
    decode,
    digits,
    encode,
    from_digits_lsd,
    is_canonical,
    msd_digits,
    normalize,
    parse_digits_msd,
)
