"""v^{9/4} rate-free door: placement, literature, integer-dilation witness."""

from __future__ import annotations

from math import floor
from pathlib import Path

from research.juggler_sequence.horizontal_weyl import (
    C_LEADING,
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


def test_integer_dilation_is_not_smooth_monomial():
    """{Δ v^{9/4}} = {Δv · {α}} and is not {2 · (27/8) n^{19/8}}.

    Reuses the keep-v first-difference sample. Not a Weyl census.
    """

    diff = first_difference_check(WITNESS_BLOCKS)
    assert diff["mvt_holds"]
    assert diff["carry_holds"]

    from research.juggler_sequence.horizontal_weyl import _axis_data

    start, stop = WITNESS_BLOCKS[0]
    prev = None
    gaps: list[float] = []
    n = start if start % 2 == 1 else start + 1
    while n <= stop:
        d = _axis_data(n, digits=24)
        if prev is not None:
            dv = d["v"] - prev["v"]
            if dv <= 0:
                prev = d
                n += 2
                continue
            dphi = (d["r_v94"] - prev["r_v94"]) / d["scale"]
            alpha = dphi / dv
            # {k α} = {k {α}} for integer k
            left = _frac(dphi)
            right = _frac(dv * _frac(alpha))
            err = min(abs(left - right), 1.0 - abs(left - right))
            assert err < 1e-9
            # smooth monomial { (27/8) * 2 * n^{19/8} }
            # n^{19/8} = n^2 * n^{3/8}
            n38 = scaled_eighth(n**3, 24) / 10**24
            smooth = C_LEADING * (3.0 / 2.0) * 2.0 * (n**2) * n38
            # (27/8) * h with h=2 is (27/4) n^{19/8}
            # C_LEADING * (3/2) * h = (9/4)*(3/2)*2 = 27/4 yes
            gap = min(
                abs(left - _frac(smooth)),
                1.0 - abs(left - _frac(smooth)),
            )
            gaps.append(gap)
        prev = d
        n += 2
    assert gaps
    # the sequences are not the same torus point: median gap stays
    # away from machine noise
    gaps.sort()
    assert gaps[len(gaps) // 2] > 1e-4


def test_conjecture_stays_active():
    text = CONJECTURE.read_text(encoding="utf-8")
    assert '"status": "ACTIVE"' in text or '"status":"ACTIVE"' in text
    assert "juggler_v94_rate_free" in text or "Hardy-of-floor" in text
