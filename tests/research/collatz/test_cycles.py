"""Periodic exponent codes, amplitude, primitivity, and cycle languages."""

from __future__ import annotations

from fractions import Fraction

from research.collatz.amplitude import (
    additive_amplitude_is_even,
    cycle_amplitude,
    exponent_code_from_syracuse,
    fernandez_slope,
    syracuse_parity_word,
)
from research.collatz.cycle_codes import (
    exponent_root,
    is_primitive,
    lex_min_rotation,
    rotations,
)
from research.collatz.cycle_divisibility import (
    christoffel_exponent_code,
    divisibility_report,
    finite_field_walk_sum,
)
from research.collatz.cycle_language import enumerate_cycle_language, proposed_restrictions
from research.collatz.cycles import candidate_cycle, rotated_affine_constant, rotation_preserves_cycle
from research.collatz.experiments.cycle_census import run_cycle_census
from research.collatz.itinerary import affine_constant


def test_primitive_root_not_string_naive():
    assert exponent_root((2, 2, 2)) == (2,)
    assert exponent_root((1, 2, 1, 2)) == (1, 2)
    assert exponent_root((1, 2, 3)) == (1, 2, 3)
    assert is_primitive((2,))
    assert not is_primitive((2, 2))
    assert not is_primitive(())


def test_lex_min_rotation():
    assert lex_min_rotation((2, 1, 3)) == (1, 3, 2)
    assert set(rotations((1, 2))) == {(1, 2), (2, 1)}


def test_trivial_cycle_is_exact():
    rec = candidate_cycle((2,))
    assert rec.is_primitive
    assert rec.is_integral
    assert rec.is_exact_cycle
    assert rec.candidate_n == 1
    assert rec.candidate_states == (1,)
    assert rec.amplitude.additive == 0
    assert rec.amplitude.multiplicative == 1
    assert rec.lift_digits == (0,)
    assert rotation_preserves_cycle((2,))


def test_repeated_twos_is_period_not_primitive_cycle():
    rec = candidate_cycle((2, 2))
    assert rec.is_integral
    assert rec.is_exact_period
    assert not rec.is_primitive
    assert not rec.is_exact_cycle
    assert rec.primitive_period == (2,)


def test_affine_not_enough_without_valuations():
    rec = candidate_cycle((1,))
    assert rec.candidate_n is None
    assert rec.denominator < 0
    assert not rec.is_exact_cycle


def test_rotation_constant_on_trivial_cycle():
    C = affine_constant((2,))
    D = 4 - 3
    assert rotated_affine_constant(C, D, 2) == C


def test_syracuse_dictionary_round_trip():
    code = (1, 4, 2)
    bits = syracuse_parity_word(code)
    assert exponent_code_from_syracuse(bits) == code
    assert fernandez_slope(code) == Fraction(7, 3)


def test_additive_amplitude_even():
    rec = candidate_cycle((2,))
    assert additive_amplitude_is_even(rec.candidate_states)
    assert cycle_amplitude((7, 11, 17)).additive % 2 == 0


def test_walk_agrees_with_divisibility_for_ones():
    code = (1, 1)
    report = divisibility_report(code)
    assert report.D < 0
    rec = candidate_cycle(code)
    assert rec.candidate_n is None
    assert not rec.is_exact_cycle


def test_christoffel_of_one_two_is_the_trivial_code():
    code = christoffel_exponent_code(1, 2)
    assert code == (2,)
    rec = candidate_cycle(code)
    assert rec.is_exact_cycle


def test_language_A0_is_the_one_cycle():
    counts, cycles, language = enumerate_cycle_language(3, 3, additive_bound=0)
    assert counts.exact_cycle == 1
    assert [rec.code for rec in language] == [(2,)]
    assert counts.enumerated == 3 + 9 + 27
    restrictions = proposed_restrictions(cycles)
    names = {row["name"]: row["classification"] for row in restrictions}
    assert names["exact_cycle_implies_contracting"] == "PROVED"
    assert names["additive_amplitude_even"] == "PROVED"


def test_census_small(tmp_path):
    result = run_cycle_census(3, 3, additive_bound=0, output_dir=tmp_path)
    assert result.counts["exact_cycle"] == 1
    assert result.K_gt_2p["witnesses"] == []
    assert result.C_mod_3["three_divides_D"] == 0
    assert result.paths["jsonl"]
    assert result.schema_version == "collatz-cycle-language/v1"


def test_finite_field_walk_on_twos():
    # D = 1, n = 1, D | C. The only prime factor of D=1 is none.
    rec = candidate_cycle((2,))
    assert rec.C % rec.denominator == 0
    assert finite_field_walk_sum((2,), 5) == 1  # λ_0 = 1, p=1
