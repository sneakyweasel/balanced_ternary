"""Phase-0: named word fragments of WORD_REWRITE_RULES, excluding Add.

The production table stays unchanged. This file records:

* the full table is not locally confluent (peak N∘W∘W);
* two-way N∘D ↔ D∘N is a reduction cycle;
* the simplifying-only fragment WORD_SIMP_RULES is terminating and
  every string-rewriting critical pair joins;
* the W/K3 stock is the interesting kernel of that fragment.

This is not the OpFrag tree TRS and not coefficient-word
``BTCalculus/Confluence.lean``.
"""

from __future__ import annotations

from itertools import product

from bt.calculus.rewrite import (
    WORD_REWRITE_RULES,
    WORD_SIMP_RULES,
    WordRewriteRule,
    rewrite_word,
)

RuleTriple = tuple[tuple[str, ...], tuple[str, ...], str]


def _triples(rules: tuple[WordRewriteRule, ...]) -> list[RuleTriple]:
    return [(rule.src, rule.dst, rule.reason) for rule in rules]


def _word_steps(word: tuple[str, ...], rules: list[RuleTriple]) -> list[tuple[str, ...]]:
    out: list[tuple[str, ...]] = []
    letters = list(word)
    for src, dst, _name in rules:
        k = len(src)
        if k == 0:
            continue
        for i in range(len(letters) - k + 1):
            if tuple(letters[i : i + k]) == src:
                out.append(tuple(letters[:i] + list(dst) + letters[i + k :]))
    return out


def _word_nfs(
    word: tuple[str, ...],
    rules: list[RuleTriple],
    *,
    limit: int = 800,
) -> set[tuple[str, ...]]:
    seen = {word}
    stack = [word]
    while stack and len(seen) < limit:
        current = stack.pop()
        for nxt in _word_steps(current, rules):
            if nxt not in seen:
                seen.add(nxt)
                stack.append(nxt)
    return {t for t in seen if not _word_steps(t, rules)}


def _word_critical_pairs(
    rules: list[RuleTriple],
) -> list[tuple[str, tuple[str, ...], tuple[str, ...], tuple[str, ...]]]:
    pairs: list[tuple[str, tuple[str, ...], tuple[str, ...], tuple[str, ...]]] = []
    for l1, r1, n1 in rules:
        for l2, r2, n2 in rules:
            for k in range(1, min(len(l1), len(l2)) + 1):
                if l1[-k:] != l2[:k]:
                    continue
                if k == len(l1) == len(l2) and (l1, r1) == (l2, r2):
                    continue
                peak = l1 + l2[k:]
                pairs.append((f"{n1} overlap {n2} k={k}", peak, r1 + l2[k:], l1[:-k] + r2))
            if len(l2) < len(l1):
                for i in range(len(l1) - len(l2) + 1):
                    if l1[i : i + len(l2)] == l2:
                        pairs.append(
                            (
                                f"{n2} in {n1} @{i}",
                                l1,
                                r1,
                                l1[:i] + r2 + l1[i + len(l2) :],
                            )
                        )
    return pairs


def _nonjoining(
    rules: list[RuleTriple],
) -> list[tuple[str, tuple[str, ...], set[tuple[str, ...]], set[tuple[str, ...]]]]:
    out = []
    for name, _peak, left, right in _word_critical_pairs(rules):
        left_nf = _word_nfs(left, rules)
        right_nf = _word_nfs(right, rules)
        if left_nf != right_nf:
            out.append((name, _peak, left_nf, right_nf))
    return out


FULL = _triples(WORD_REWRITE_RULES)
SIMP = _triples(WORD_SIMP_RULES)
WK3_REASONS = {
    "K3 is a projection",
    "W∘W = K3 (strip factors of 3)",
    "W∘S = W  (appending zeros does not change W)",
    "K3∘S = K3",
    "K3∘W = W  (W(n) is never divisible by 3 unless 0)",
    "W∘K3 = W",
}
WK3 = [row for row in SIMP if row[2] in WK3_REASONS]


# ---------------------------------------------------------------------------
# Inventory
# ---------------------------------------------------------------------------


def test_word_simp_is_exactly_the_simplifying_rows():
    assert len(WORD_REWRITE_RULES) == 32
    assert len(WORD_SIMP_RULES) == 16
    assert WORD_SIMP_RULES == tuple(r for r in WORD_REWRITE_RULES if r.simplifying)
    assert all(not rule.simplifying for rule in WORD_REWRITE_RULES if rule not in WORD_SIMP_RULES)


def test_production_table_has_two_way_nd_and_nw_but_no_nk3():
    reasons = {rule.reason for rule in WORD_REWRITE_RULES}
    assert "N∘D = D∘N" in reasons
    assert "D∘N = N∘D" in reasons
    assert "N∘W = W∘N" in reasons
    assert "W∘N = N∘W" in reasons
    srcs = {rule.src for rule in WORD_REWRITE_RULES}
    assert ("N", "K3") not in srcs
    assert ("K3", "N") not in srcs


# ---------------------------------------------------------------------------
# Full table: named obstructions
# ---------------------------------------------------------------------------


def test_full_table_nd_is_a_two_cycle():
    """Two-way N∘D ↔ D∘N is a reduction cycle (KNOWN TRS fact)."""
    assert _word_steps(("N", "D"), FULL) == [("D", "N")]
    assert _word_steps(("D", "N"), FULL) == [("N", "D")]


def test_full_table_nww_does_not_join():
    """Peak N∘W∘W: N∘K3 and K3∘N are distinct production irreducibles."""
    peak = ("N", "W", "W")
    steps = _word_steps(peak, FULL)
    assert ("N", "K3") in steps
    assert ("W", "N", "W") in steps
    assert _word_nfs(("N", "K3"), FULL) == {("N", "K3")}
    assert _word_nfs(("K3", "N"), FULL) == {("K3", "N")}
    assert _word_nfs(peak, FULL) == {("N", "K3"), ("K3", "N")}


def test_full_table_critical_pairs_fail_exactly_at_ww_nw():
    """The only non-joining production CPs are the W∘W / N∘W overlaps."""
    failures = _nonjoining(FULL)
    peaks = {peak for _name, peak, _l, _r in failures}
    assert peaks == {("N", "W", "W"), ("W", "W", "N")}
    irreducibles = {nf for _name, _peak, left, right in failures for nf in left | right}
    assert irreducibles == {("N", "K3"), ("K3", "N")}


# ---------------------------------------------------------------------------
# WORD_SIMP_RULES: termination + local confluence
# ---------------------------------------------------------------------------


def test_simp_every_rule_drops_the_termination_rank():
    """Rank (I0-count, length): I0→S drops the first; others drop length."""
    for rule in WORD_SIMP_RULES:
        src_i0 = rule.src.count("I0")
        dst_i0 = rule.dst.count("I0")
        if rule.src == ("I0",):
            assert rule.dst == ("S",)
            assert dst_i0 < src_i0
            assert len(rule.dst) == len(rule.src)
        else:
            assert len(rule.src) == 2
            assert len(rule.dst) <= 1
            assert dst_i0 <= src_i0


def test_simp_critical_pairs_join():
    assert _nonjoining(SIMP) == []


def test_simp_named_peaks_join():
    """The documented W/K3 and I0 overlaps reach the stated joins."""
    expected = {
        ("N", "N", "N"): {("N",)},
        ("D", "I0"): {()},
        ("W", "W", "W"): {("W",)},
        ("W", "W", "S"): {("K3",)},
        ("W", "W", "K3"): {("K3",)},
        ("K3", "W", "W"): {("K3",)},
        ("W", "K3", "W"): {("K3",)},
        ("K3", "K3", "K3"): {("K3",)},
    }
    for peak, nfs in expected.items():
        assert _word_nfs(peak, SIMP) == nfs


def test_wk3_stock_critical_pairs_join():
    """The six-rule W/K3 kernel is itself locally confluent."""
    assert len(WK3) == 6
    assert _nonjoining(WK3) == []


def test_wk3_unique_nf_on_words_of_length_at_most_6():
    alphabet = ("W", "K3", "S")
    conflicts: list[tuple[str, ...]] = []
    for n in range(7):
        for word in product(alphabet, repeat=n):
            if len(_word_nfs(word, WK3)) != 1:
                conflicts.append(word)
                if len(conflicts) >= 4:
                    break
        if conflicts:
            break
    assert conflicts == []


def test_simp_unique_nf_on_mixed_words_of_length_at_most_4():
    """Bounded census on the letters that actually interact in SIMP."""
    alphabet = ("W", "K3", "S", "D", "I0", "N")
    conflicts: list[tuple[str, ...]] = []
    for n in range(5):
        for word in product(alphabet, repeat=n):
            if len(_word_nfs(word, SIMP)) != 1:
                conflicts.append(word)
                if len(conflicts) >= 4:
                    break
        if conflicts:
            break
    assert conflicts == []


def test_rewrite_word_simplifying_only_is_the_named_fragment():
    word, used = rewrite_word(("N", "W", "W"), simplifying_only=True)
    assert word == ("N", "K3")
    assert "W∘W = K3 (strip factors of 3)" in used
    assert all("N∘W" not in reason for reason in used)
    full, _ = rewrite_word(("N", "W", "W"))
    # Left-to-right engine happens to emit one of the two irreducibles;
    # confluence of the full table is still false.
    assert full in {("N", "K3"), ("K3", "N")}
