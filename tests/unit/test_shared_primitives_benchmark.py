"""Tiny timing smoke for shared primitives. Not an optimization pass."""

from __future__ import annotations

import time

from bt.arithmetic import add
from bt.representation import decode, encode, normalize
from bt.transducers.doubling import apply_double


def test_encode_decode_normalize_add_double_are_exact_and_finite():
    t0 = time.perf_counter()
    for n in range(-200, 201):
        word = encode(n)
        assert decode(word) == n
        assert decode(normalize(word.word())) == n
        assert decode(add(word, encode(1))) == n + 1
        assert decode(apply_double(word)) == 2 * n
    elapsed = time.perf_counter() - t0
    assert elapsed < 30
