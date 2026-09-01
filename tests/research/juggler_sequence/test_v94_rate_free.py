"""v^{9/4} rate-free door: placement, literature, integer-dilation witness."""

from __future__ import annotations

from math import floor
from pathlib import Path

from research.juggler_sequence.horizontal_weyl import (
    first_difference_check,
    scaled_eighth,
)
from research.literature import get_reference

DOSSIER = Path("docs/problems/juggler_v94_rate_free.md")
CONJECTURE = Path(
    "conjectures/active/juggler_tower_rate_free_equidistribution.json"
)

LIT_IDS = (
    "boshernitzan-1994-hardy-fields",
    "frantzikinakis-2009-sparse-nilmanifolds",
    "richter-2023-hardy-nilmanifolds",
)

# reuse the existing first-difference science blocks, but a short
# stretch is enough to witness the torus gap
WITNESS_BLOCKS = ((10**6 + 1, 10**6 + 1 + 80),)


def _frac(x: float) -> float:
    return x - floor(x)


def test_literature_ids_resolve():
    for ref_id in LIT_IDS:
        rec = get_reference(ref_id)
        assert rec["id"] == ref_id
        assert rec["project_relationship"] == "known"


def test_dossier_headings_and_close():
    dossier = DOSSIER.read_text(encoding="utf-8")
    for heading in (
        "## Problem",
        "## Exact statement",
        "## Current literature",
        "## Branch budget",
        "## Decision",
        "## Publication assessment",
    ):
        assert heading in dossier
    decision = dossier.split("## Decision", 1)[1].split("## ", 1)[0]
    assert "CLOSE" in decision
    assert "not claimed" in dossier.lower() or "Not an equidistribution" in dossier
    for ref_id in LIT_IDS:
        assert ref_id in dossier
    assert "integer dilation" in dossier.lower() or "Integer dilation" in dossier
    assert "J-nested-floor-without-W-family" in dossier
    assert "no new ledger row" in dossier.lower() or "No new ledger row" in dossier


def test_integer_dilation_identity_is_elementary():
    """{k α} = {k {α}} for k in Z. Algebra, not a large-n float check."""

    for k, alpha in ((3, 1.25), (17, 0.01), (1000, 2.0 / 3.0), (5, -0.4)):
        left = _frac(k * alpha)
        right = _frac(k * _frac(alpha))
        err = min(abs(left - right), 1.0 - abs(left - right))
        assert err < 1e-12


def test_keep_v_difference_is_not_smooth_monomial():
    """{Δ v^{9/4}} is not {(27/4) n^{19/8}} on the keep-v sample.

    Fractional parts from scaled integers (no float cancellation of
    the huge v^{9/4} values). Reuses horizontal_weyl first-difference
    blocks. Not a Weyl census.
    """

    diff = first_difference_check(WITNESS_BLOCKS)
    assert diff["mvt_holds"]
    assert diff["carry_holds"]

    from research.juggler_sequence.horizontal_weyl import _axis_data

    digits = 24
    scale = 10**digits
    start, stop = WITNESS_BLOCKS[0]
    prev = None
    gaps: list[float] = []
    n = start if start % 2 == 1 else start + 1
    while n <= stop:
        d = _axis_data(n, digits=digits)
        if prev is not None:
            f1 = (prev["r_v94"] % prev["scale"]) / prev["scale"]
            f2 = (d["r_v94"] % d["scale"]) / d["scale"]
            left = f2 - f1 if f2 >= f1 else f2 - f1 + 1.0
            # {(27/4) n^{19/8}} = {(27/4) n^2 n^{3/8}}
            r_n38 = scaled_eighth(n**3, digits)
            # (27 * n^2 * r_n38) / (4 * scale)  mod 1
            numer = 27 * (n * n) * r_n38
            denom = 4 * scale
            smooth = (numer % denom) / denom
            gap = min(abs(left - smooth), 1.0 - abs(left - smooth))
            gaps.append(gap)
        prev = d
        n += 2
    assert gaps
    gaps.sort()
    assert gaps[len(gaps) // 2] > 1e-4


def test_conjecture_stays_active():
    text = CONJECTURE.read_text(encoding="utf-8")
    assert '"status": "ACTIVE"' in text or '"status":"ACTIVE"' in text
    assert "juggler_v94_rate_free" in text or "Hardy-of-floor" in text
