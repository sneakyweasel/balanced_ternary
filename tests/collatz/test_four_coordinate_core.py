"""Core tests for four-coordinate Collatz compatibility."""

from __future__ import annotations

from dataclasses import replace
from itertools import product
from math import log, log1p

import pytest

from collatz.compatibility import (
    CompatibilityState,
    ExponentCodeDiagnostic,
    build_compatibility_graph,
)
from collatz.dual_code import CollatzDualCode
from collatz.endpoint_3adic import (
    KramerEndpoint,
    endpoint_residue_rate,
    endpoint_congruence_holds,
    kramer_endpoint_residue,
    least_positive_residue,
    real_drift,
    start_residue_rate,
)
from collatz.rational_base import (
    RationalBaseThreeHalves,
    append_odd_step,
    decode_base_3_2,
    encode_base_3_2,
    is_admissible_base_3_2,
)


def test_kramer_endpoint_convention_and_empty_prefix():
    assert least_positive_residue(0, 9) == 9
    assert least_positive_residue(10, 9) == 1
    assert kramer_endpoint_residue(()) == 1
    assert KramerEndpoint.from_valuations(()).as_dict()["modulus"] == 1

    assert kramer_endpoint_residue((1,)) == 2
    assert kramer_endpoint_residue((4,)) == 1
    assert endpoint_congruence_holds(5, (1,))
    assert endpoint_congruence_holds(1, (4,))


def test_kramer_formula_and_endpoint_congruence_exhaustive_small():
    for length in range(5):
        words = ((),) if length == 0 else product(range(1, 5), repeat=length)
        for word in words:
            ks = tuple(word)
            dual = CollatzDualCode.from_valuations(ks)
            endpoint = KramerEndpoint.from_valuations(ks)
            assert endpoint.validates()
            assert endpoint.modulus == 3**length
            assert endpoint.contains(dual.endpoints[-1])
            if ks:
                expected = dual.C * pow(1 << dual.K, -1, 3**length) % (3**length)
                assert endpoint.M % endpoint.modulus == expected


def test_diagnostic_exact_bridge_and_natural_log_rates():
    diagnostic = ExponentCodeDiagnostic.from_valuations((1, 4, 2))
    dual = CollatzDualCode.from_valuations((1, 4, 2))

    assert diagnostic.R == dual.R
    assert diagnostic.r == dual.R % (1 << dual.K)
    assert diagnostic.C == dual.C
    assert diagnostic.exact_drift == (3**dual.m, 1 << dual.K)
    assert diagnostic.rho_r == pytest.approx(log1p(diagnostic.r) / diagnostic.m)
    expected_rho_M = log(
        1 + diagnostic.M / ((3 / 2) ** diagnostic.m)
    ) / diagnostic.m
    assert diagnostic.rho_M == pytest.approx(expected_rho_M)
    assert diagnostic.d == pytest.approx(
        abs(diagnostic.K / diagnostic.m - log(3) / log(2))
    )
    assert diagnostic.validates()
    assert ExponentCodeDiagnostic.from_dual_code(dual) == diagnostic
    assert CompatibilityState.from_dual_code(dual).validates()
    assert real_drift(diagnostic.K, diagnostic.m) == diagnostic.d
    assert start_residue_rate(diagnostic.r, diagnostic.m) == diagnostic.rho_r
    assert endpoint_residue_rate(diagnostic.M, diagnostic.m) == diagnostic.rho_M
    assert not replace(diagnostic, rho_r=diagnostic.rho_r + 0.1).validates()

    empty = ExponentCodeDiagnostic.from_valuations(())
    assert empty.r == 0
    assert empty.M == 1
    assert (empty.d, empty.rho_r, empty.rho_M) == (0.0, 0.0, 0.0)

    with pytest.raises(ValueError):
        real_drift(1, 0)
    with pytest.raises(ValueError):
        start_residue_rate(1, 0)
    with pytest.raises(ValueError):
        endpoint_residue_rate(2, 0)


def test_compatibility_state_extensions_and_validation():
    state = CompatibilityState.from_valuations((1, 2))
    assert state.validates()
    assert state.canonical_endpoint % state.three_power == state.M % state.three_power
    assert state.three_power * state.R + state.C == (
        state.two_power * state.canonical_endpoint
    )

    children = state.extensions(4)
    assert tuple(child.valuations[-1] for child in children) == (1, 2, 3, 4)
    for k, child in enumerate(children, start=1):
        exact = CollatzDualCode.from_valuations(state.valuations + (k,))
        assert child.R == exact.R
        assert child.lift_digits == exact.lift_digits
        assert child.validates()

    assert not replace(state, M=state.M + 1).validates()
    with pytest.raises(ValueError):
        state.extend(0)
    with pytest.raises(ValueError):
        state.extensions(True)


def test_bounded_compatibility_graph_is_exact_prefix_tree():
    graph = build_compatibility_graph(max_depth=2, k_max=3)
    assert len(graph.nodes) == 1 + 3 + 9
    assert len(graph.edges) == 3 + 9
    assert graph.validates()
    assert graph.root.valuations == ()
    assert {node.valuations for node in graph.nodes if node.m == 2} == set(
        product(range(1, 4), repeat=2)
    )

    rooted = build_compatibility_graph(1, 2, root=(4,))
    assert rooted.root.valuations == (4,)
    assert {node.valuations for node in rooted.nodes} == {(4,), (4, 1), (4, 2)}


@pytest.mark.parametrize(
    ("n", "word"),
    [(0, ""), (1, "2"), (2, "21"), (3, "210"), (4, "212"), (5, "2101")],
)
def test_rational_base_published_recurrence_examples(n: int, word: str):
    assert encode_base_3_2(n) == word
    assert decode_base_3_2(word) == n
    assert RationalBaseThreeHalves.from_int(n).word == word


def test_rational_base_round_trip_and_odd_append_identity():
    for n in range(1000):
        word = encode_base_3_2(n)
        assert decode_base_3_2(word) == n
        assert is_admissible_base_3_2(word)
        if n % 2:
            appended = append_odd_step(word)
            assert appended == word + "1"
            assert decode_base_3_2(appended) == (3 * n + 1) // 2
            assert RationalBaseThreeHalves.from_int(n).odd_step().value == (
                3 * n + 1
            ) // 2


def test_rational_base_decoder_rejects_nonintegral_and_noncanonical_words():
    assert decode_base_3_2("") == 0
    for word in ("1", "20", "211", "3", "2x"):
        assert not is_admissible_base_3_2(word)
        with pytest.raises((TypeError, ValueError)):
            decode_base_3_2(word)

    with pytest.raises(ValueError):
        decode_base_3_2("02")
    assert decode_base_3_2("02", canonical=False) == 1
    with pytest.raises(ValueError):
        append_odd_step("21")
    with pytest.raises(ValueError):
        encode_base_3_2(-1)
    with pytest.raises(ValueError):
        encode_base_3_2(True)
