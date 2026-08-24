"""Phase-0 tests for {S,N,D,W} recorded-identity completeness."""

from __future__ import annotations

from research.operator_dynamics.algebra import Composition
from research.operator_dynamics.problem import PROBLEM
from research.operator_dynamics.triage import (
    MAX_LEN,
    RECORDED_SNDW_RULES,
    apply_word,
    critical_pairs_join,
    first_disagreement,
    generator_words,
    known_separations,
    reduce_recorded,
    rewrite_sound_on_probes,
    semantic_collisions,
    triage_report,
)


def test_closed_problem_is_registered():
    from research.open_problems import get_problem

    assert PROBLEM.status == "ARCHIVED"
    assert get_problem("operator_dynamics") is PROBLEM
    assert "docs/problems/operator_dynamics.md" in PROBLEM.docs


def test_recorded_rules_stay_off_the_production_table():
    from bt.calculus.rewrite import WORD_REWRITE_RULES

    production_srcs = {rule.src for rule in WORD_REWRITE_RULES}
    assert ("N", "K3") not in production_srcs
    assert any(src == ("N", "K3") for src, _dst, _reason in RECORDED_SNDW_RULES)


def test_recorded_reductions_of_known_identities():
    assert reduce_recorded(("N", "N")) == ()
    assert reduce_recorded(("D", "S")) == ()
    assert reduce_recorded(("W", "S")) == ("W",)
    assert reduce_recorded(("W", "W")) == ("K3",)
    assert reduce_recorded(("W", "W", "W")) == ("W",)
    assert reduce_recorded(("W", "W", "S")) == ("K3",)
    assert reduce_recorded(("S", "D", "S", "D")) == ("S", "D")
    assert reduce_recorded(("W", "D", "S", "W")) == ("K3",)
    assert reduce_recorded(("N", "W", "S")) == ("W", "N")
    assert reduce_recorded(("N", "W", "W")) == ("K3", "N")
    assert reduce_recorded(("K3", "N")) == ("K3", "N")


def test_refuted_identities_stay_distinct():
    assert reduce_recorded(("W", "W")) != reduce_recorded(())
    assert apply_word(("W", "W"), 3) != apply_word((), 3)
    assert apply_word(("W",), 3) != 3 * apply_word(("W",), 1)
    assert apply_word(("S", "D"), 1) != 1
    assert apply_word(("D", "W"), 10) != apply_word(("W", "D"), 10)
    assert apply_word(("S", "W"), 1) != apply_word(("W",), 1)
    assert first_disagreement(("D", "W"), ("W", "D")) is not None
    assert first_disagreement(("S", "W"), ("W",)) is not None


def test_n_w_w_peak_joins_under_recorded_orientation():
    assert reduce_recorded(("N", "W", "W")) == reduce_recorded(("K3", "N"))
    assert reduce_recorded(("N", "W", "W")) == reduce_recorded(("N", "K3"))
    sep = known_separations()
    assert sep["N_W_W_joins"] is True
    assert sep["W_W_vs_id"]["witness"] is not None
    assert sep["S_D_vs_id"]["witness"] is not None
    assert sep["D_W_vs_W_D"]["witness"] is not None


def test_recorded_rules_are_sound_and_locally_confluent():
    assert critical_pairs_join()
    assert rewrite_sound_on_probes(max_len=3)


def test_recorded_rules_agree_with_integer_maps():
    for n in range(-80, 81):
        assert apply_word(("N", "N"), n) == n
        assert apply_word(("D", "S"), n) == n
        assert apply_word(("W", "S"), n) == apply_word(("W",), n)
        assert apply_word(("W", "W", "W"), n) == apply_word(("W",), n)
        assert apply_word(("N", "W"), n) == apply_word(("W", "N"), n)
        assert apply_word(("N", "D"), n) == apply_word(("D", "N"), n)
        assert apply_word(("N", "S"), n) == apply_word(("S", "N"), n)


def test_composition_is_reused_for_evaluation():
    assert apply_word(("W", "D", "N", "S"), 5) == Composition(("W", "D", "N", "S")).apply(5)


def test_length_four_has_no_new_identity():
    assert MAX_LEN == 4
    assert len(generator_words(MAX_LEN)) == 341
    collisions = semantic_collisions(MAX_LEN)
    assert collisions == ()
    report = triage_report(MAX_LEN)
    assert report["enumerated"] == 341
    assert report["normal_forms"] == 77
    assert report["rewrite_sound_on_probes"] is True
    assert report["critical_pairs_join"] is True
    assert report["new_identities"] == ()
    assert report["probe_collisions"] == 0
    assert "recorded consequence" in report["verdict"]
