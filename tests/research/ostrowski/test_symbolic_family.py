"""Prefix family P_m = 2(-4)^m is not an |L_0| claim.

A bounded tail search is a BOUNDED LIVE_SLICE observation. It is
never ClaimKind.LIVE and never infinitude of origin-live terminals.
"""

from __future__ import annotations

from research.ostrowski.nonpisot_search import HUB
from research.ostrowski.recurrence_zero import reset_pow_then_hub_word
from research.ostrowski.spectral_control import N12_MAXIMIZER_STATE, N12_MAXIMIZER_WORD
from research.ostrowski.symbolic_family import (
    CLASS_BSTAR,
    CLASS_HUB,
    CLASS_OTHER,
    CLASS_RAY,
    EXCLUDED_NOT_THIS_FAMILY,
    GROWTH_NOT_INFINITUDE,
    PREFIX_NOT_UNBOUNDED_FAMILY,
    classify_completion,
    classify_landing,
    is_excluded,
    maximizer_is_origin_live,
    maximizer_starts_with_prefix,
    phase0_prefix_family,
    prefix,
    uk_is_excluded,
    walk_live,
)
from research.ostrowski.zero_value_kernel import LEGAL_TWO_STEP_K, on_legal_two_step_ray
from research_engine.core.semantics import ClaimKind, SearchScope
from research_engine.planner.orchestrator import DEFERRED_ATTACKS


def test_maximizer_is_live_and_starts_with_p2():
    assert prefix(2) == (2, -4, -4)
    assert maximizer_starts_with_prefix()
    assert N12_MAXIMIZER_WORD[:3] == prefix(2)
    assert maximizer_is_origin_live()
    landing = walk_live(N12_MAXIMIZER_WORD)
    assert landing == N12_MAXIMIZER_STATE
    assert classify_completion(N12_MAXIMIZER_WORD, landing) == CLASS_OTHER
    assert not is_excluded(CLASS_OTHER)


def test_uk_reset_then_hub_is_excluded():
    for k in range(4):
        word = reset_pow_then_hub_word(k)
        assert classify_completion(word, HUB) == CLASS_BSTAR
        assert uk_is_excluded(k)
        assert is_excluded(CLASS_BSTAR)
    assert prefix(0)[0] == 2
    assert reset_pow_then_hub_word(1)[0] == 1


def test_two_step_ray_landings_are_excluded():
    assert classify_landing(HUB) == CLASS_HUB
    assert is_excluded(CLASS_HUB)
    for k in LEGAL_TWO_STEP_K:
        state = (3 * k, k, 0)
        assert on_legal_two_step_ray(state)
        label = classify_landing(state)
        assert is_excluded(label)
        if k == -1:
            assert label == CLASS_HUB
        else:
            assert label == CLASS_RAY


def test_phase0_is_bounded_live_slice_not_live():
    report = phase0_prefix_family()
    assert report["kind"] == ClaimKind.LIVE_SLICE.value
    assert report["kind"] != ClaimKind.LIVE.value
    assert report["scope"] == SearchScope.BOUNDED.value
    assert report["status"] == "OBSERVATION"
    assert report["infinitude_claimed"] is False
    assert report["l0_promoted"] is False
    assert report[GROWTH_NOT_INFINITUDE] is True
    assert report[PREFIX_NOT_UNBOUNDED_FAMILY] is True
    assert report[EXCLUDED_NOT_THIS_FAMILY] is True
    assert "LIVE" not in (report["kind"], report["status"], report["scope"])
    assert report["symbolic_family"] is False
    assert report["closed_form_found"] is False
    assert report["closed_form_tail"] is None
    assert DEFERRED_ATTACKS == ("symbolic",)
    by_m = {row["m"]: row for row in report["rows"]}
    for m in (0, 1, 2):
        assert by_m[m]["n_other"] > 0
        assert by_m[m]["prefix_dies"] is False
    assert report["first_dead_m"] == 3
    for m in range(3, report["max_m"] + 1):
        assert by_m[m]["prefix_dies"] is True
        assert by_m[m]["n_live_completions"] == 0
        assert by_m[m]["prefix_live_any_tail"] is False
