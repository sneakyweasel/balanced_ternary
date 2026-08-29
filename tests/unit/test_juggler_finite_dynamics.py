"""Finite-dynamics companion instantiates the note; it does not halt."""

from visualization.juggler_finite_dynamics import (
    LEFTOVER_CUTOFF,
    NOTE_ORBIT_3,
    NOTE_PEAK_37,
    WORD_MAX,
    classify_word,
    compose_view,
    descent_view,
    descent_window,
    envelope_view,
    even_cell_view,
    four_block_replay,
    leftover_table,
    leftover_words,
    length_eight_open_words,
    next_square_view,
    odd_cell_view,
    parse_word,
    walk_orbit,
)


def test_orbit_of_three_matches_the_note():
    view = walk_orbit(3, 20)
    assert view.states == NOTE_ORBIT_3
    assert view.word == "OOOEEE"
    assert view.reached_one
    assert not view.too_large


def test_orbit_of_thirty_seven_records_the_note_peak():
    view = walk_orbit(37, 80)
    assert NOTE_PEAK_37 in view.states
    assert view.reached_one
    assert not view.bit_capped


def test_envelope_identity_on_one_odd_letter():
    view = envelope_view(3, "O")
    assert view.follows
    assert view.image == 5
    assert view.slack == 2
    assert view.delta == 2
    assert view.regime == "expanding"
    assert view.vanishing == "monochrome but a local remainder is positive"


def test_mixed_word_is_strictly_positive():
    view = envelope_view(5, "OOE")
    assert view.follows
    assert view.image == 6
    assert not view.monochrome
    assert view.vanishing == "mixed word, Δ > 0"
    if view.slack is not None:
        assert view.slack > 0


def test_compose_matches_when_budget_allows():
    view = compose_view(3, "O", "O")
    assert view.follows
    assert view.mid == 5
    assert view.end == 11
    if not view.too_large and view.composed is not None:
        assert view.composed == view.delta_uv


def test_leftover_tables_have_no_returns():
    for word, cutoff in LEFTOVER_CUTOFF.items():
        table = leftover_table(word)
        assert table.n_hi == cutoff
        assert table.checked == cutoff - 2
        assert table.hits == ()
        assert not any(row["returned"] for row in table.rows)


def test_leftover_words_are_the_note_four():
    assert leftover_words() == ("OOOEOE", "OOOOEE", "OOOOEOE", "OOOOOEE")


def test_classify_leftovers_and_open_length_eight():
    assert classify_word("OOOEOE").kind == "leftover"
    assert classify_word("OOOOEE").kind == "leftover"
    assert classify_word("OOOOEOE").kind == "leftover"
    assert classify_word("OOOOOEE").kind == "leftover"
    assert classify_word("OOOOOE").kind == "odd-run"
    assert classify_word("OOE").kind == "threshold"
    open_word = length_eight_open_words()[0]
    info = classify_word(open_word)
    assert info.kind == "open"
    assert "open" in info.reason


def test_length_eight_open_list_is_expanding_and_even_terminating():
    words = length_eight_open_words()
    assert words
    assert all(len(word) == 8 and word.endswith("E") for word in words)
    assert all(2 ** 8 < 3 ** word.count("O") for word in words)


def test_descent_buckets_of_note_starts():
    even = descent_view(2)
    assert even.bucket == "EVEN_PROGRESS"
    assert even.certificate == "E"
    odd_odd = descent_view(3)
    assert odd_odd.bucket == "ODD_ODD"
    oe = descent_view(7)
    assert oe.bucket == "OE_PROGRESS"
    assert oe.certificate == "OE"


def test_descent_window_is_a_count_not_a_density():
    counts = descent_window(80)
    assert counts["n_max"] == 80
    assert counts["EVEN_PROGRESS"] + counts["OE_PROGRESS"] + counts["ODD_ODD"] == 79
    assert counts["EVEN_PROGRESS"] > 0
    assert counts["ODD_ODD"] > 0


def test_four_block_chain_replays_the_note():
    chain = four_block_replay()
    assert [step.start for step in chain] == [1999, 5169, 50093, 193753]
    assert [step.word for step in chain] == ["OOE", "OOOOEE", "OOE", "OOE"]
    assert [step.image for step in chain] == [5169, 50093, 193753, 887471]
    assert all(step.matches for step in chain)


def test_next_square_on_three_and_five():
    at_three = next_square_view(3, "OO")
    assert at_three.follows
    assert at_three.image == 11
    assert at_three.met is False
    at_five = next_square_view(5, "OO")
    assert at_five.follows
    assert at_five.met is True


def test_cells_match_floor_geometry():
    even = even_cell_view(6)
    assert even.lo == 36
    assert even.hi == 49
    assert 36 in even.evens
    assert 48 in even.evens
    odd = odd_cell_view(11)
    assert odd.integers == (5,)


def test_parse_word_rejects_overlong_and_junk():
    assert parse_word("ooe") == "OOE"
    assert parse_word("O O E") == "OOE"
    assert parse_word("") == ""
    assert parse_word("OX") is None
    assert parse_word("O" * (WORD_MAX + 1)) is None


def test_bit_cap_refuses_a_huge_start():
    huge = 1 << 300
    view = walk_orbit(huge, 4)
    assert view.too_large
    slack = envelope_view(10**12 + 1, "O")
    assert slack.follows
    assert slack.slack_too_large
