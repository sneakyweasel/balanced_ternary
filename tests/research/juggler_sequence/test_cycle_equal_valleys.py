"""Equal valleys versus leftover finance. Not a halt test."""

from __future__ import annotations

from pathlib import Path

from research.conjectures import get_conjecture
from research.literature import get_reference
from research.juggler_sequence.cycle_equal_valleys import (
    CLASS_CLOSED,
    CLASS_GREEN,
    CLASS_INCOMPLETE,
    EXISTING_LEAN,
    FOCUS_LENGTH,
    FOCUS_M,
    FORBIDDEN_LEAN_FILES,
    FORBIDDEN_NEW_API,
    FORBIDDEN_THEOREMS,
    LEAN_CONST,
    LEAN_FLOOR,
    classify,
    height_split_rhs,
    lean_api_present,
    probe_payload,
    render_markdown,
    smallest_killing_n2,
    split_valley_rhs,
    theta_of,
)
from research.juggler_sequence.cycle_finance import EPS_CONST
from research.juggler_sequence.cycle_gap_baker import o_min
from research.juggler_sequence.cycle_m_finance import first_odd_image, steiner_rhs

REPO = Path(__file__).resolve().parents[3]


def test_prefix_return_uniqueness_is_the_equal_valley_obstruction():
    assert FOCUS_LENGTH == 84
    assert o_min(84) == 53
    assert LEAN_FLOOR == 261
    payload = probe_payload()
    scan = payload["scan"]
    assert scan["unique_visit"] is True
    assert scan["all_equal_only_if_m1_or_shorter_cycle"] is True
    assert scan["second_valley_at_least_n_plus_two"] is True


def test_n_plus_two_does_not_kill_length_eighty_four_m3():
    odd = o_min(FOCUS_LENGTH)
    theta = theta_of(FOCUS_LENGTH, odd)
    n = LEAN_FLOOR
    n2 = n + 2
    split = split_valley_rhs(n, FOCUS_LENGTH, odd, FOCUS_M, n2, const=LEAN_CONST)
    joint = steiner_rhs(n, FOCUS_LENGTH, odd, FOCUS_M, const=LEAN_CONST)
    height_split = height_split_rhs(
        n, FOCUS_LENGTH, odd, FOCUS_M, n2, const=LEAN_CONST
    )
    assert n2 == 263
    assert split < joint
    assert joint - split < 0.00002
    assert split > theta
    assert height_split > theta
    assert smallest_killing_n2(
        n, FOCUS_LENGTH, odd, FOCUS_M, theta, const=LEAN_CONST
    ) is None
    assert (
        smallest_killing_n2(
            n,
            FOCUS_LENGTH,
            odd,
            FOCUS_M,
            theta,
            const=LEAN_CONST,
            rhs=height_split_rhs,
        )
        == 281
    )
    t = first_odd_image(n)
    assert t == 4216


def test_six_fifths_is_strictly_worse():
    odd = o_min(FOCUS_LENGTH)
    lean = split_valley_rhs(
        LEAN_FLOOR, FOCUS_LENGTH, odd, FOCUS_M, LEAN_FLOOR + 2, const=LEAN_CONST
    )
    six = split_valley_rhs(
        LEAN_FLOOR, FOCUS_LENGTH, odd, FOCUS_M, LEAN_FLOOR + 2, const=EPS_CONST
    )
    assert six > lean


def test_probe_closes_and_adds_no_lean():
    payload = probe_payload()
    decision = classify(payload["scan"], payload["lean"])
    assert decision["classification"] == CLASS_CLOSED
    assert payload["scan"]["slogan_false"] is True
    assert payload["anti_overclaim"]["halt_theorem"] is False
    assert payload["anti_overclaim"]["new_lean"] is False
    assert payload["lean"]["sorry_free"] is True
    assert payload["lean"]["no_equal_valleys_lean"] is True
    assert payload["lean"]["not_in_paper_barrel"] is True
    for name in EXISTING_LEAN:
        assert payload["lean"][name] is True
    for name in FORBIDDEN_THEOREMS:
        assert payload["lean"][f"has_{name}"] is False
    for name in FORBIDDEN_NEW_API:
        assert payload["lean"][f"has_api_{name}"] is False
    for path in FORBIDDEN_LEAN_FILES:
        assert not path.is_file()
    markdown = render_markdown(payload)
    assert CLASS_CLOSED in markdown
    assert decision["classification"] != CLASS_GREEN
    assert decision["classification"] != CLASS_INCOMPLETE


def test_dossier_and_registry():
    dossier = (
        REPO / "docs" / "problems" / "juggler_cycle_equal_valleys.md"
    ).read_text(encoding="utf-8")
    paper = (REPO / "formal" / "Problems" / "JugglerPaper.lean").read_text(
        encoding="utf-8"
    )
    assert "## Branch budget" in dossier
    assert "## Decision" in dossier
    assert "## Publication assessment" in dossier
    assert "**CLOSE**" in dossier
    assert "juggler_cycle_finance_note.md" in dossier
    assert "CycleEqualValleys" not in paper
    assert "UniqueValley" not in paper
    get_reference("simons-de-weger-2005-collatz-m-cycles")
    equal = get_conjecture("juggler_cycle_all_valleys_equal")
    killer = get_conjecture("juggler_equal_valleys_leftover_killer")
    assert equal["status"] == "REFUTED"
    assert killer["status"] == "REFUTED"
    assert equal["counterexamples"]
    assert killer["counterexamples"]
    lean = lean_api_present()
    assert lean["cycle_finance_present"] is True
