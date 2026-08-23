"""Phase-0: named word fragments of WORD_REWRITE_RULES, excluding Add.

The production table stays unchanged. This file records:

* the full table is not locally confluent (peak N∘W∘W);
* two-way N∘D ↔ D∘N is a reduction cycle;
* the simplifying-only fragment WORD_SIMP_RULES is terminating and
  every string-rewriting critical pair joins;
* the W/K3 stock is the interesting kernel of that fragment;
* the opt-in fragment WORD_WN_RULES (SIMP + one-way N∘S, N∘W, N∘K3)
  is terminating and every critical pair joins;
* SIMP + one-way N∘D fails at N∘D∘I± even after N∘K3 is added;
* the opt-in fragment WORD_WND_RULES (WN + one-way N∘D and the
  exact word I± sign-flips) is terminating and every critical pair
  joins, including the old N∘D∘I± peaks.

This is not the OpFrag tree TRS and not coefficient-word
``BTCalculus/Confluence.lean``.
"""

from __future__ import annotations

from itertools import product

from bt.calculus.rewrite import (
    WORD_N_IM_RULE,
    WORD_N_IP_RULE,
    WORD_N_K3_RULE,
    WORD_REWRITE_RULES,
    WORD_SIMP_RULES,
    WORD_WND_RULES,
    WORD_WN_RULES,
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
WN = _triples(WORD_WN_RULES)
WND = _triples(WORD_WND_RULES)
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
    assert WORD_N_K3_RULE.src == ("N", "K3")
    assert WORD_N_K3_RULE not in WORD_REWRITE_RULES
    assert WORD_N_K3_RULE in WORD_WN_RULES
    assert WORD_N_IP_RULE not in WORD_REWRITE_RULES
    assert WORD_N_IM_RULE not in WORD_REWRITE_RULES
    assert WORD_N_IP_RULE in WORD_WND_RULES
    assert WORD_N_IM_RULE in WORD_WND_RULES


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


# ---------------------------------------------------------------------------
# WORD_WN_RULES: SIMP + one-way N∘S, N∘W, N∘K3
# ---------------------------------------------------------------------------

_PUSHABLE = frozenset({"S", "W", "K3"})


def _production(src: tuple[str, ...]) -> WordRewriteRule:
    for rule in WORD_REWRITE_RULES:
        if rule.src == src:
            return rule
    raise KeyError(src)


def _n_inversion(word: tuple[str, ...]) -> int:
    count = 0
    for i, letter in enumerate(word):
        if letter != "N":
            continue
        count += sum(1 for later in word[i + 1 :] if later in _PUSHABLE)
    return count


def _wn_rank(word: tuple[str, ...]) -> tuple[int, int, int]:
    return (word.count("I0"), _n_inversion(word), len(word))


def test_word_wn_is_simp_plus_one_way_ns_nw_nk3():
    assert len(WORD_WN_RULES) == 19
    assert WORD_WN_RULES[:16] == WORD_SIMP_RULES
    extras = WORD_WN_RULES[16:]
    assert [rule.src for rule in extras] == [("N", "S"), ("N", "W"), ("N", "K3")]
    assert extras[0] is _production(("N", "S"))
    assert extras[1] is _production(("N", "W"))
    assert extras[2] is WORD_N_K3_RULE
    assert ("D", "N") not in {rule.src for rule in WORD_WN_RULES}
    assert ("W", "N") not in {rule.src for rule in WORD_WN_RULES}
    assert ("K3", "N") not in {rule.src for rule in WORD_WN_RULES}


def test_nk3_is_exact_on_small_integers():
    from bt.operators import get_operator

    neg = get_operator("N")
    k3 = get_operator("K3")
    for n in range(-80, 81):
        assert neg.apply(k3.apply(n)) == k3.apply(neg.apply(n))


def test_wn_every_rule_drops_the_termination_rank():
    """Rank (I0-count, N-inversion, length); N moves inward past {S,W,K3}."""
    for rule in WORD_WN_RULES:
        assert _wn_rank(rule.dst) < _wn_rank(rule.src)


def test_wn_one_step_drops_rank_on_words_of_length_at_most_4():
    alphabet = ("W", "K3", "S", "N", "D", "I0")
    bad: list[tuple[tuple[str, ...], tuple[str, ...]]] = []
    for n in range(5):
        for word in product(alphabet, repeat=n):
            start = _wn_rank(word)
            for nxt in _word_steps(word, WN):
                if _wn_rank(nxt) >= start:
                    bad.append((word, nxt))
                    if len(bad) >= 4:
                        break
            if bad:
                break
        if bad:
            break
    assert bad == []


def test_wn_critical_pairs_join():
    assert _nonjoining(WN) == []


def test_wn_named_peaks_join():
    """N∘W∘W and the other new N-overlaps join after N∘K3 / N∘S."""
    expected = {
        ("N", "W", "W"): {("K3", "N")},
        ("N", "W", "S"): {("W", "N")},
        ("N", "W", "K3"): {("W", "N")},
        ("N", "K3", "K3"): {("K3", "N")},
        ("N", "K3", "S"): {("K3", "N")},
        ("N", "K3", "W"): {("W", "N")},
        ("N", "N", "S"): {("S",)},
        ("N", "N", "W"): {("W",)},
        ("N", "N", "K3"): {("K3",)},
        ("W", "W", "W"): {("W",)},
        ("D", "I0"): {()},
    }
    for peak, nfs in expected.items():
        assert _word_nfs(peak, WN) == nfs


def test_wn_unique_nf_on_mixed_words_of_length_at_most_4():
    alphabet = ("W", "K3", "S", "N", "D", "I0", "Ip", "Im")
    conflicts: list[tuple[str, ...]] = []
    for n in range(5):
        for word in product(alphabet, repeat=n):
            if len(_word_nfs(word, WN)) != 1:
                conflicts.append(word)
                if len(conflicts) >= 4:
                    break
        if conflicts:
            break
    assert conflicts == []


def test_rewrite_word_accepts_opt_in_wn_rules():
    word, used = rewrite_word(("N", "W", "W"), rules=WORD_WN_RULES)
    assert word == ("K3", "N")
    assert "N∘K3 = K3∘N" in used
    simp, _ = rewrite_word(("N", "W", "W"), simplifying_only=True)
    assert simp == ("N", "K3")


def test_two_way_nk3_is_a_cycle():
    """Reverse K3∘N ↔ N∘K3 is a reduction cycle; not installed."""
    two_way = WN + [(("K3", "N"), ("N", "K3"), "K3∘N = N∘K3")]
    assert _word_steps(("N", "K3"), two_way) == [("K3", "N")]
    assert _word_steps(("K3", "N"), two_way) == [("N", "K3")]


def test_opposite_k3n_orientation_fails_without_nk3():
    """K3∘N → N∘K3 without N∘K3 leaves W∘N∘K3 irreducible."""
    opposite = SIMP + [
        (_production(("N", "S")).src, _production(("N", "S")).dst, _production(("N", "S")).reason),
        (_production(("N", "W")).src, _production(("N", "W")).dst, _production(("N", "W")).reason),
        (("K3", "N"), ("N", "K3"), "K3∘N = N∘K3"),
    ]
    failures = _nonjoining(opposite)
    peaks = {peak for _name, peak, _l, _r in failures}
    assert ("N", "W", "K3") in peaks
    assert ("W", "K3", "N") in peaks


# ---------------------------------------------------------------------------
# SIMP + N∘D is not repaired by N∘K3
# ---------------------------------------------------------------------------


def test_simp_plus_nd_fails_at_nd_ip_even_with_nk3():
    """N∘D∘I±: D∘N∘I± and N are distinct irreducibles. No word I± sign-flip."""
    nd_fragment = WN + [
        (_production(("N", "D")).src, _production(("N", "D")).dst, _production(("N", "D")).reason),
    ]
    assert _word_nfs(("N", "D", "Ip"), nd_fragment) == {("N",), ("D", "N", "Ip")}
    assert _word_nfs(("N", "D", "Im"), nd_fragment) == {("N",), ("D", "N", "Im")}
    # I0 is rewritten to S, so N∘D∘I0 still joins.
    assert _word_nfs(("N", "D", "I0"), nd_fragment) == {("N",)}
    assert _word_nfs(("N", "D", "S"), nd_fragment) == {("N",)}
    failures = _nonjoining(nd_fragment)
    peaks = {peak for _name, peak, _l, _r in failures}
    assert peaks == {("N", "D", "Ip"), ("N", "D", "Im")}


# ---------------------------------------------------------------------------
# WORD_WND_RULES: WN + one-way N∘D + I± sign-flips
# ---------------------------------------------------------------------------

_WND_PUSHABLE = frozenset({"S", "W", "K3", "D", "Ip", "Im"})


def _wnd_inversion(word: tuple[str, ...]) -> int:
    count = 0
    for i, letter in enumerate(word):
        if letter != "N":
            continue
        count += sum(1 for later in word[i + 1 :] if later in _WND_PUSHABLE)
    return count


def _wnd_rank(word: tuple[str, ...]) -> tuple[int, int, int]:
    return (word.count("I0"), _wnd_inversion(word), len(word))


def test_word_wnd_is_wn_plus_one_way_nd_and_ipm_flips():
    assert len(WORD_WND_RULES) == 22
    assert WORD_WND_RULES[:19] == WORD_WN_RULES
    extras = WORD_WND_RULES[19:]
    assert [rule.src for rule in extras] == [("N", "D"), ("N", "Ip"), ("N", "Im")]
    assert extras[0] is _production(("N", "D"))
    assert extras[1] is WORD_N_IP_RULE
    assert extras[2] is WORD_N_IM_RULE
    assert extras[1].dst == ("Im", "N")
    assert extras[2].dst == ("Ip", "N")
    assert ("D", "N") not in {rule.src for rule in WORD_WND_RULES}
    assert ("Im", "N") not in {rule.src for rule in WORD_WND_RULES}
    assert ("Ip", "N") not in {rule.src for rule in WORD_WND_RULES}
    assert WORD_WND_RULES != WORD_REWRITE_RULES


def test_ipm_sign_flips_are_exact_on_small_integers():
    """N∘I+ = I-∘N and N∘I- = I+∘N because I_a(x)=a+3x."""
    from bt.operators import get_operator

    neg = get_operator("N")
    ip = get_operator("Ip")
    im = get_operator("Im")
    for n in range(-80, 81):
        assert neg.apply(ip.apply(n)) == im.apply(neg.apply(n))
        assert neg.apply(im.apply(n)) == ip.apply(neg.apply(n))


def test_wnd_every_rule_drops_the_termination_rank():
    """Rank (I0-count, N-inversion, length); N moves inward past {S,W,K3,D,I±}."""
    for rule in WORD_WND_RULES:
        assert _wnd_rank(rule.dst) < _wnd_rank(rule.src)


def test_wnd_one_step_drops_rank_on_words_of_length_at_most_4():
    alphabet = ("W", "K3", "S", "N", "D", "I0", "Ip", "Im")
    bad: list[tuple[tuple[str, ...], tuple[str, ...]]] = []
    for n in range(5):
        for word in product(alphabet, repeat=n):
            start = _wnd_rank(word)
            for nxt in _word_steps(word, WND):
                if _wnd_rank(nxt) >= start:
                    bad.append((word, nxt))
                    if len(bad) >= 4:
                        break
            if bad:
                break
        if bad:
            break
    assert bad == []


def test_wnd_critical_pairs_join():
    assert _nonjoining(WND) == []


def test_wnd_named_peaks_join():
    """N∘D∘I± joins after the sign-flips; WN peaks are unchanged."""
    expected = {
        ("N", "D", "Ip"): {("N",)},
        ("N", "D", "Im"): {("N",)},
        ("N", "D", "I0"): {("N",)},
        ("N", "D", "S"): {("N",)},
        ("N", "N", "Ip"): {("Ip",)},
        ("N", "N", "Im"): {("Im",)},
        ("N", "N", "D"): {("D",)},
        ("N", "W", "W"): {("K3", "N")},
        ("N", "W", "S"): {("W", "N")},
        ("N", "K3", "W"): {("W", "N")},
        ("D", "I0"): {()},
        ("W", "W", "W"): {("W",)},
    }
    for peak, nfs in expected.items():
        assert _word_nfs(peak, WND) == nfs


def test_wnd_unique_nf_on_mixed_words_of_length_at_most_4():
    alphabet = ("W", "K3", "S", "N", "D", "I0", "Ip", "Im")
    conflicts: list[tuple[str, ...]] = []
    for n in range(5):
        for word in product(alphabet, repeat=n):
            if len(_word_nfs(word, WND)) != 1:
                conflicts.append(word)
                if len(conflicts) >= 4:
                    break
        if conflicts:
            break
    assert conflicts == []


def test_rewrite_word_accepts_opt_in_wnd_rules():
    """The old irreducible D∘N∘I± joins to N only after the sign-flips."""
    word, used = rewrite_word(("D", "N", "Ip"), rules=WORD_WND_RULES)
    assert word == ("N",)
    assert "N∘Ip = Im∘N" in used
    assert "D∘Im = id" in used
    wn, _ = rewrite_word(("D", "N", "Ip"), rules=WORD_WN_RULES)
    assert wn == ("D", "N", "Ip")
    peak, _ = rewrite_word(("N", "D", "Ip"), rules=WORD_WND_RULES)
    assert peak == ("N",)


def test_two_way_nd_and_reverse_ipm_are_cycles():
    """Reverse N∘D and reverse I± flips are reduction cycles; not installed."""
    two_way = WND + [
        (("D", "N"), ("N", "D"), "D∘N = N∘D"),
        (("Im", "N"), ("N", "Ip"), "Im∘N = N∘Ip"),
        (("Ip", "N"), ("N", "Im"), "Ip∘N = N∘Im"),
    ]
    assert _word_steps(("N", "D"), two_way) == [("D", "N")]
    assert _word_steps(("D", "N"), two_way) == [("N", "D")]
    assert _word_steps(("N", "Ip"), two_way) == [("Im", "N")]
    assert _word_steps(("Im", "N"), two_way) == [("N", "Ip")]
    assert _word_steps(("N", "Im"), two_way) == [("Ip", "N")]
    assert _word_steps(("Ip", "N"), two_way) == [("N", "Im")]
