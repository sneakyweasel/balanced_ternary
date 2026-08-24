"""Phase-0 tests for k-abelian residual signatures."""

from __future__ import annotations

from research.kabelian_complexity.problem import PROBLEM
from research.kabelian_complexity.triage import (
    CANTOR_START,
    PERIOD_DOUBLING_START,
    THUE_MORSE_START,
    cantor_prefix,
    class_key,
    extend_signature,
    extension_conflicts,
    factors_of_length,
    family_complexity_sequence,
    k_abelian_classes,
    occurrence_count,
    period_doubling_prefix,
    signature,
    thue_morse_prefix,
    triage_report,
)


def test_problem_is_registered():
    from research.conjectures import get_conjecture
    from research.literature import get_reference
    from research.open_problems import get_problem

    assert get_problem("kabelian_complexity") is PROBLEM
    assert PROBLEM.status == "ARCHIVED"
    assert PROBLEM.docs == ("docs/problems/kabelian_complexity.md",)
    assert get_reference("karhumaki-saarela-zamboni-2013-k-abelian")["year"] == 2013
    assert get_reference("parreau-rigo-rowland-vandomme-2015-2-regular")["year"] == 2015
    assert get_reference("greinecker-2015-tm-2-abelian")["year"] == 2015
    assert get_reference("chen-lu-wu-2017-cantor-k-abelian")["year"] == 2017
    assert get_reference("shallit-2020-abelian-synchronization")["year"] == 2020
    assert get_reference("couvreur-et-al-2025-pisot-k-abelian")["year"] == 2025
    assert get_reference("allouche-shallit-2003-automatic-sequences")["year"] == 2003
    conj = get_conjecture("kabelian_regularity_automatic")
    assert conj["status"] == "ACTIVE"
    assert PROBLEM.conjectures == ("kabelian_regularity_automatic",)


def test_published_prefixes():
    assert thue_morse_prefix(8) == THUE_MORSE_START
    assert period_doubling_prefix(8) == PERIOD_DOUBLING_START
    assert cantor_prefix(9) == CANTOR_START


def test_overlapping_counts_and_local_update():
    word = (0, 1, 1, 0, 1)
    assert occurrence_count(word, (1, 1)) == 1
    assert occurrence_count((1, 1, 1), (1, 1)) == 2
    alphabet = (0, 1)
    for k in (1, 2, 3):
        updated = extend_signature(word, 0, k, alphabet)
        recomputed = signature(word + (0,), k, alphabet)
        assert updated == recomputed


def test_k1_is_abelian_and_short_words_are_equality():
    alphabet = (0, 1)
    u = (0, 1, 0)
    v = (0, 0, 1)
    # Same letters, different order: 1-abelian equivalent, not 2-abelian.
    assert class_key(u, 1, alphabet) == class_key(v, 1, alphabet)
    assert class_key(u, 2, alphabet) != class_key(v, 2, alphabet)
    # Length < k: k-abelian is ordinary equality.
    assert class_key((0, 1), 3, alphabet) != class_key((1, 0), 3, alphabet)


def test_thue_morse_small_complexity_is_exact():
    prefix = thue_morse_prefix(256)
    alphabet = (0, 1)
    # Length 1: two letters.
    assert k_abelian_classes(factors_of_length(prefix, 1), 1, alphabet) == 2
    # Length 2 abelian: 00, 01/10, 11 — three Parikh vectors.
    assert k_abelian_classes(factors_of_length(prefix, 2), 1, alphabet) == 3
    # For n < k, ρ_k = factor complexity.
    p3 = len(factors_of_length(prefix, 3))
    assert k_abelian_classes(factors_of_length(prefix, 3), 4, alphabet) == p3


def test_extension_is_deterministic_on_ksz_classes():
    prefix = thue_morse_prefix(512)
    for k, n in ((1, 8), (2, 8), (2, 16)):
        assert extension_conflicts(prefix, n, k, (0, 1)) == 0
    cantor = cantor_prefix(729)
    assert extension_conflicts(cantor, 12, 2, (0, 1)) == 0


def test_raw_signature_grows_with_length():
    prefix = thue_morse_prefix(256)
    alphabet = (0, 1)
    short = max(signature(u, 2, alphabet) for u in factors_of_length(prefix, 4))
    long = max(signature(u, 2, alphabet) for u in factors_of_length(prefix, 16))
    assert long > short


def test_triage_report_recovers_benchmarks_and_ksz_compression():
    report = triage_report(n_max=16)
    assert report["prefixes"]["thue_morse"][:8] == THUE_MORSE_START
    assert report["prefixes"]["period_doubling"][:8] == PERIOD_DOUBLING_START
    assert report["prefixes"]["cantor"][:9] == CANTOR_START

    tm2 = report["complexity"]["thue_morse"][2]
    pd2 = report["complexity"]["period_doubling"][2]
    cantor1 = report["complexity"]["cantor"][1]
    assert len(tm2) == 16
    assert tm2[0] == 2
    assert pd2[0] == 2
    assert cantor1[0] == 2
    # Unbounded 2-abelian complexity on Thue–Morse in this window.
    assert max(tm2) > tm2[0]

    for row in report["rows"]:
        assert row["class_equals_signature"]
        assert row["extension_conflicts"] == 0
        assert row["k_abelian_class_count"] == row["compressed_state_count"]
        assert row["k_abelian_class_count"] == row["relative_state_count"]
        if row["n"] >= 8:
            assert row["stable"]
            assert row["sliding_conflicts"] > 0
            assert row["max_raw_coordinate"] > 1
            if row["k"] >= 2:
                assert row["naive_dfao_suffix_count"] < row["k_abelian_class_count"]

    growth = report["relative_union_growth"]["thue_morse"][2]
    assert growth[-1] > growth[0]
    assert report["kernels"]["thue_morse"][2] >= 1
    assert report["kernels"]["cantor"][1] >= 1
