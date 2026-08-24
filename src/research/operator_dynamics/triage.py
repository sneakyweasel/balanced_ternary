"""Phase-0: semantic identities in the {S,N,D,W} monoid.

Recorded exact identities from ``docs/operator_algebra.md`` are oriented
into a terminating rewrite list on the alphabet {S, N, D, W} with
auxiliary letter K3 = W∘W. This is not a production
``WORD_REWRITE_RULES`` change and not OpFrag ``discover_closed``.

Two words are a *consequence* of the recorded list when they share this
normal form. A *new* identity is semantic equality of two distinct
normal forms on ℤ.
"""

from __future__ import annotations

from collections import defaultdict
from itertools import product

from research.operator_dynamics.algebra import Composition

GENERATORS: tuple[str, ...] = ("S", "N", "D", "W")
MAX_LEN = 4

# Terminating orientation of the recorded {S,N,D,W} identities.
# K3 is W∘W, not a generator. Do not install these in WORD_REWRITE_RULES.
RECORDED_SNDW_RULES: tuple[tuple[tuple[str, ...], tuple[str, ...], str], ...] = (
    (("N", "N"), (), "N∘N = id"),
    (("D", "S"), (), "D∘S = id"),
    (("W", "S"), ("W",), "W∘S = W"),
    (("W", "W"), ("K3",), "W∘W = K3"),
    (("K3", "S"), ("K3",), "K3∘S = K3"),
    (("K3", "W"), ("W",), "K3∘W = W"),
    (("W", "K3"), ("W",), "W∘K3 = W"),
    (("K3", "K3"), ("K3",), "K3∘K3 = K3"),
    (("N", "S"), ("S", "N"), "N∘S = S∘N"),
    (("N", "D"), ("D", "N"), "N∘D = D∘N"),
    (("N", "W"), ("W", "N"), "N∘W = W∘N"),
    (("N", "K3"), ("K3", "N"), "N∘K3 = K3∘N"),
)


def reduce_recorded(factors: tuple[str, ...]) -> tuple[str, ...]:
    """Left-to-right recorded rewrite until stable."""
    word = list(factors)
    changed = True
    while changed:
        changed = False
        for src, dst, _reason in RECORDED_SNDW_RULES:
            k = len(src)
            if k == 0:
                continue
            i = 0
            while i + k <= len(word):
                if tuple(word[i : i + k]) == src:
                    word[i : i + k] = list(dst)
                    changed = True
                    i = max(0, i - k)
                else:
                    i += 1
    return tuple(word)


def generator_words(max_len: int = MAX_LEN) -> tuple[tuple[str, ...], ...]:
    if isinstance(max_len, bool) or not isinstance(max_len, int) or max_len < 0:
        raise ValueError(f"max_len must be a nonnegative int, got {max_len!r}")
    words: list[tuple[str, ...]] = [()]
    for depth in range(1, max_len + 1):
        words.extend(product(GENERATORS, repeat=depth))
    return tuple(words)


def probe_integers() -> tuple[int, ...]:
    """Short words plus long mixed probes that separate D/W shapes."""
    probes = set(range(-121, 122))
    for k in range(0, 12):
        probes.add(3**k)
        probes.add(-(3**k))
        probes.add(3**k + 1)
        probes.add(3**k - 1)
        probes.add(-(3**k) + 1)
        probes.add(1 + 3**k)
        if 2 * k <= 16:
            probes.add(1 + 3**k + 3 ** (2 * k))
    for k in range(2, 11):
        probes.add(1 + 3**k)
        probes.add(1 + 3 + 3**k)
        probes.add(2 + 3**k)
        probes.add(4 * (3**k) + 1)
    probes.update((364, 365, 1093, 2000, 6561, 10000, -10000, 10, 13, 28, 40))
    return tuple(sorted(probes))


def apply_word(factors: tuple[str, ...], n: int) -> int:
    return Composition(factors).apply(n)


def first_disagreement(
    left: tuple[str, ...],
    right: tuple[str, ...],
    probes: tuple[int, ...] | None = None,
) -> int | None:
    if probes is None:
        probes = probe_integers()
    for n in probes:
        if apply_word(left, n) != apply_word(right, n):
            return n
    return None


def hunt_witness(
    left: tuple[str, ...],
    right: tuple[str, ...],
    *,
    limit: int = 4000,
) -> int | None:
    """Wider integer search after a probe collision."""
    if isinstance(limit, bool) or not isinstance(limit, int) or limit < 0:
        raise ValueError(f"limit must be a nonnegative int, got {limit!r}")
    hit = first_disagreement(left, right)
    if hit is not None:
        return hit
    for n in range(-limit, limit + 1):
        if apply_word(left, n) != apply_word(right, n):
            return n
    extra = tuple(1 + 3**k + 3**m for k in range(1, 14) for m in range(k + 1, 15))
    return first_disagreement(left, right, extra)


def _critical_pairs() -> tuple[tuple[tuple[str, ...], tuple[str, ...]], ...]:
    """Prefix/suffix overlaps and inclusions of the recorded rules."""
    pairs: list[tuple[tuple[str, ...], tuple[str, ...]]] = []
    for src1, dst1, _r1 in RECORDED_SNDW_RULES:
        for src2, dst2, _r2 in RECORDED_SNDW_RULES:
            if not src1 or not src2:
                continue
            if src1 == src2 and dst1 == dst2:
                if len(src1) >= 2 and src1[1:] == src1[:-1]:
                    pairs.append((dst1 + src1[-1:], src1[:1] + dst1))
                continue
            for k in range(1, min(len(src1), len(src2))):
                if src1[-k:] == src2[:k]:
                    pairs.append((dst1 + src2[k:], src1[:-k] + dst2))
            for i in range(len(src1) - len(src2) + 1):
                if src1[i : i + len(src2)] == src2:
                    left = src1[:i] + dst2 + src1[i + len(src2) :]
                    pairs.append((dst1, left))
    return tuple(pairs)


def critical_pairs_join() -> bool:
    for left, right in _critical_pairs():
        if reduce_recorded(left) != reduce_recorded(right):
            return False
    return True


def fingerprint(factors: tuple[str, ...], probes: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(apply_word(factors, n) for n in probes)


def rewrite_sound_on_probes(
    max_len: int = MAX_LEN,
    probes: tuple[int, ...] | None = None,
) -> bool:
    if probes is None:
        probes = probe_integers()
    for word in generator_words(max_len):
        nf = reduce_recorded(word)
        if first_disagreement(word, nf, probes) is not None:
            return False
    return True


def semantic_collisions(
    max_len: int = MAX_LEN,
    probes: tuple[int, ...] | None = None,
) -> tuple[dict[str, object], ...]:
    """Distinct recorded-NFs that agree on the probe set."""
    if probes is None:
        probes = probe_integers()
    nfs: set[tuple[str, ...]] = set()
    for word in generator_words(max_len):
        nfs.add(reduce_recorded(word))
    by_print: dict[tuple[int, ...], list[tuple[str, ...]]] = defaultdict(list)
    for nf in sorted(nfs, key=lambda w: (len(w), w)):
        by_print[fingerprint(nf, probes)].append(nf)
    hits: list[dict[str, object]] = []
    for group in by_print.values():
        if len(group) < 2:
            continue
        for i, left in enumerate(group):
            for right in group[i + 1 :]:
                witness = hunt_witness(left, right)
                hits.append(
                    {
                        "left": left,
                        "right": right,
                        "witness": witness,
                        "new_identity": witness is None,
                    }
                )
    return tuple(hits)


def known_separations() -> dict[str, object]:
    """Already-recorded non-identities must stay distinct NFs."""
    return {
        "W_W_vs_id": {
            "left_nf": reduce_recorded(("W", "W")),
            "right_nf": reduce_recorded(()),
            "witness": first_disagreement(("W", "W"), ()),
        },
        "S_D_vs_id": {
            "left_nf": reduce_recorded(("S", "D")),
            "right_nf": reduce_recorded(()),
            "witness": first_disagreement(("S", "D"), ()),
        },
        "D_W_vs_W_D": {
            "left_nf": reduce_recorded(("D", "W")),
            "right_nf": reduce_recorded(("W", "D")),
            "witness": first_disagreement(("D", "W"), ("W", "D")),
        },
        "S_W_vs_W": {
            "left_nf": reduce_recorded(("S", "W")),
            "right_nf": reduce_recorded(("W",)),
            "witness": first_disagreement(("S", "W"), ("W",)),
        },
        "N_W_W_joins": reduce_recorded(("N", "W", "W")) == reduce_recorded(("K3", "N")),
    }


def triage_report(max_len: int = MAX_LEN) -> dict[str, object]:
    probes = probe_integers()
    words = generator_words(max_len)
    nfs = {reduce_recorded(word) for word in words}
    collisions = semantic_collisions(max_len, probes)
    new_identities = tuple(row for row in collisions if row["new_identity"])
    false_collisions = tuple(row for row in collisions if not row["new_identity"])
    if new_identities:
        verdict = "new exact identity among distinct recorded-NFs"
    else:
        verdict = (
            f"every identity of length ≤{max_len} is a recorded consequence "
            "(COMPUTATIONALLY VERIFIED on the probe set; distinct NFs disagree)"
        )
    return {
        "max_len": max_len,
        "enumerated": len(words),
        "normal_forms": len(nfs),
        "probes": len(probes),
        "rewrite_sound_on_probes": rewrite_sound_on_probes(max_len, probes),
        "critical_pairs_join": critical_pairs_join(),
        "known_separations": known_separations(),
        "probe_collisions": len(collisions),
        "false_probe_collisions": len(false_collisions),
        "new_identities": new_identities,
        "verdict": verdict,
    }
