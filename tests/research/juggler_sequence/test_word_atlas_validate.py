"""Three-way atlas validation gate."""

from __future__ import annotations

from research.juggler_sequence.atlas.validate import (
    check_floor_power_fixtures,
    check_lean_word_fixtures,
    check_metadata_recompute,
    validate_suite,
)
from research.juggler_sequence.atlas.schema import CLAIM_CPU, CLAIM_LEAN


def test_cpu_equals_lean_fixtures():
    assert check_floor_power_fixtures() == []
    assert check_lean_word_fixtures() == []


def test_stored_metadata_recompute_identity():
    assert check_metadata_recompute(8) == []


def test_validate_suite_claims():
    report = validate_suite()
    assert report["ok"]
    assert CLAIM_LEAN in report["claims"]
    assert CLAIM_CPU in report["claims"]
