"""Printed Step 5b interpolant-error chain, not the sums."""

from __future__ import annotations

from research.juggler_sequence.step5b_p0 import (
    ANTI,
    first_p0s,
    intro_example_holds,
    leftover_219_vs_01_holds,
    printed_chain_gap,
    printed_chain_holds,
    three_term_error,
    v_covers_error_holds,
    vs_le_c7_half_holds,
)


def test_anti_overclaim():
    assert ANTI["sums_evaluated"] is False
    assert ANTI["paper_b_modified"] is False
    assert ANTI["kernel_retagged"] is False
    assert ANTI["k3_reopened"] is False


def test_printed_chain_never_holds():
    for p in (10**6, 10**8, 10**12, 10**18):
        assert printed_chain_holds(p) is False
        assert printed_chain_gap(p) > 0.0
        # The 0.11 term already exceeds the 0.1 right-hand side.
        assert three_term_error(p) > 0.1 * float(p) ** (-5.0 / 6.0)
    assert first_p0s()["printed_chain"] is None


def test_intro_example_threshold():
    assert intro_example_holds(10**12) is False
    assert intro_example_holds(10**14) is True
    p0 = first_p0s()["intro_54_vs_01"]
    assert p0 is not None
    assert 10**13 < p0 < 10**14


def test_leftover_219_is_larger():
    p0 = first_p0s()["leftover_219_vs_01"]
    intro = first_p0s()["intro_54_vs_01"]
    assert p0 is not None and intro is not None
    assert p0 > intro
    assert leftover_219_vs_01_holds(p0) is True
    assert leftover_219_vs_01_holds(p0 - 1) is False


def test_v_and_vs_fail_at_laboratory_p():
    assert v_covers_error_holds(10**8) is False
    assert vs_le_c7_half_holds(10**8) is False
