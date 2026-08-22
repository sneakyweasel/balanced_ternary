"""select3 and piecewise arithmetic."""

from __future__ import annotations

from bt.calculus.order import cmp3
from bt.calculus.select import abs_z, clamp_z, max_z, median_z, min_z, select3, sign_z
from bt.calculus.trit import Trit


def test_select3_branches():
    assert select3(Trit.MINUS, 10, 20, 30) == 10
    assert select3(0, 10, 20, 30) == 20
    assert select3(1, 10, 20, 30) == 30


def test_piecewise_functions():
    for x in range(-40, 41):
        assert abs_z(x) == abs(x)
        assert sign_z(x) == (0 if x == 0 else (1 if x > 0 else -1))
        for y in range(-40, 41):
            assert max_z(x, y) == max(x, y)
            assert min_z(x, y) == min(x, y)
            assert select3(cmp3(x, y), -1, 0, 1) == int(cmp3(x, y))
            for z in range(-20, 21):
                assert median_z(x, y, z) == sorted((x, y, z))[1]
        assert clamp_z(x, -3, 5) == min(max(x, -3), 5)
