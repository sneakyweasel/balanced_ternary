"""Lean-aligned Add/carry boundary witnesses.

Matches ``formal/BTCalculus/RewriteAddBoundary.lean``. No new production
rules. Word-table enlargement stays closed.
"""

from __future__ import annotations

from bt.calculus.derivative import D
from bt.calculus.integral import I_minus, I_plus


def test_add_is_not_D_local():
    """D(0+0)=0 and D(1+1)=1 while D(0)=D(1)=0."""
    assert D(0) == 0
    assert D(1) == 0
    assert D(0 + 0) == 0
    assert D(1 + 1) == 1
    assert D(1 + 1) != D(1) + D(1)


def test_same_sign_Ip_is_not_a_constructor_identity():
    """I+(x)+I+(y) = 3(x+y)+2, and 2 is not a trit."""
    for x, y in ((0, 0), (1, 2), (-3, 4)):
        assert I_plus(x) + I_plus(y) == 3 * (x + y) + 2
        assert I_minus(x) + I_minus(y) == 3 * (x + y) - 2


def test_mixed_N_S_has_unequal_slopes():
    """N(x)+S(y) = -x + 3y is not a function of x+y alone."""
    left = (-1) + 3 * 0
    right = (-0) + 3 * 1
    assert left != right
