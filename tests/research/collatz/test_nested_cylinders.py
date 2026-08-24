"""Nested cylinders and the R_m -> inf implication."""

from __future__ import annotations

from research.collatz.compatibility import (
    RealizabilityClass,
    nested_cylinder_report,
    positive_integer_would_bound_R,
)
from research.collatz.experiments.nested_cylinders import all_ones_prefix, run_nested_trace
from research.collatz.lower_bounds import certificate_attempts, log2_R_upper_bound_exponent
from research.collatz.zero_lift import lift_digit
from research.collatz.min_realizer import min_realizer


def test_all_ones_closed_form():
    """R((1,)*m) = 2^{m+1}-1. PROVED; this is a check of the formula."""
    for m in range(0, 16):
        assert min_realizer((1,) * m) == (1 << (m + 1)) - 1
    ks = all_ones_prefix(8)
    report = nested_cylinder_report(ks)
    assert report.monotone
    assert report.realizers[-1] == (1 << 9) - 1


def test_no_smaller_child():
    parent = (1, 2, 1)
    r_p = min_realizer(parent)
    for j in range(1, 6):
        r_c = min_realizer(parent + (j,))
        assert r_c >= r_p
        t = lift_digit(parent, j)
        assert t >= 0


def test_unbounded_excludes_integer_logic():
    rs = (1, 3, 7, 15, 31)
    assert not positive_integer_would_bound_R(7, rs)
    assert positive_integer_would_bound_R(31, rs)


def test_certificate_labels():
    names = {c.name: c.status for c in certificate_attempts()}
    assert names["trivial_upper_bound"] == "PROVED"
    assert names["all_ones_R_unbounded"] == "PROVED"
    assert names["expansionary_forces_R_to_infinity"] == "CONJECTURE"
    assert log2_R_upper_bound_exponent((1, 2)) == 4
    assert RealizabilityClass.FINITELY_TWO_ADICALLY_REALIZABLE.value.startswith("FINITELY")


def test_nested_trace_lifts():
    payload = run_nested_trace((1, 1, 2))
    assert payload["monotone"]
    assert len(payload["lifts"]) == 3
