"""Exact Phase-0 tests for k-abelian signatures of automatic sequences.

k-abelian equivalence is the Karhumäki–Saarela–Zamboni relation: overlapping
occurrence counts of every factor of length at most k. Raw signatures grow
with factor length. The compressed class key is the KSZ triple

    (prefix_{k-1}, suffix_{k-1}, length-k Parikh vector),

which is the k-block coding of the factor together with its borders. That
triple is a REPARAMETERIZATION of the 2015 block-coding construction, not a
new residual.

No Walnut run, no linear representation, no balanced-trit addressing, and
no claim that a finite table proves b-regularity.
"""

from __future__ import annotations

from itertools import product
from typing import Iterable, Sequence

from bt.automata.minimize import minimize_dfa

Word = tuple[int, ...]
Parikh = tuple[int, ...]
ClassKey = tuple[Word, Word, Parikh]

# Published prefixes. KNOWN.
THUE_MORSE_START: Word = (0, 1, 1, 0, 1, 0, 0, 1)
PERIOD_DOUBLING_START: Word = (0, 1, 0, 0, 0, 1, 0, 1)
CANTOR_START: Word = (1, 0, 1, 0, 0, 0, 1, 0, 1)

PREFIX_LEN = 4096
CANTOR_PREFIX_LEN = 6561  # 3^8
CENSUS_N = 24
KERNEL_TERMS = 4
SINK = "SINK"


def _require_positive(n: int, name: str) -> int:
    if isinstance(n, bool) or not isinstance(n, int) or n < 1:
        raise ValueError(f"{name} must be a positive int")
    return n


def _require_k(k: int) -> int:
    return _require_positive(k, "k")


def patterns_upto(alphabet: Sequence[int], k: int) -> tuple[Word, ...]:
    """All nonempty words of length at most k, short-lex then letter-lex."""

    k = _require_k(k)
    letters = tuple(alphabet)
    out: list[Word] = []
    for length in range(1, k + 1):
        out.extend(product(letters, repeat=length))
    return tuple(out)


def occurrence_count(word: Sequence[int], pattern: Sequence[int]) -> int:
    """Overlapping occurrences of ``pattern`` in ``word``."""

    w = tuple(word)
    p = tuple(pattern)
    m = len(p)
    if m == 0 or m > len(w):
        return 0
    return sum(1 for i in range(len(w) - m + 1) if w[i : i + m] == p)


def signature(word: Sequence[int], k: int, alphabet: Sequence[int]) -> Parikh:
    """Σ_k(u): occurrence counts of every factor of length 1..k."""

    pats = patterns_upto(alphabet, k)
    return tuple(occurrence_count(word, pat) for pat in pats)


def k_block_parikh(word: Sequence[int], k: int, alphabet: Sequence[int]) -> Parikh:
    """Occurrence counts of every length-k factor (overlapping)."""

    k = _require_k(k)
    blocks = tuple(product(tuple(alphabet), repeat=k))
    return tuple(occurrence_count(word, block) for block in blocks)


def class_key(word: Sequence[int], k: int, alphabet: Sequence[int]) -> ClassKey:
    """KSZ triple: prefix_{k-1}, suffix_{k-1}, length-k Parikh.

    For ``|u| < k`` the key is the word itself in the prefix slot, so
    distinct short words remain distinct.
    """

    k = _require_k(k)
    w = tuple(word)
    width = k - 1
    if len(w) < k:
        return (w, (), ())
    return (w[:width], w[len(w) - width :], k_block_parikh(w, k, alphabet))


def extend_signature(
    word: Sequence[int],
    letter: int,
    k: int,
    alphabet: Sequence[int],
) -> Parikh:
    """Local update: appending ``letter`` adds the suffixes of length 1..k."""

    k = _require_k(k)
    if letter not in tuple(alphabet):
        raise ValueError(f"letter {letter} is not in the alphabet")
    ua = tuple(word) + (letter,)
    added = {ua[len(ua) - ell :] for ell in range(1, min(k, len(ua)) + 1)}
    pats = patterns_upto(alphabet, k)
    base = signature(word, k, alphabet)
    return tuple(c + (1 if pat in added else 0) for c, pat in zip(base, pats))


def k_abelian_classes(factors: Iterable[Word], k: int, alphabet: Sequence[int]) -> int:
    keys = {class_key(u, k, alphabet) for u in factors}
    return len(keys)


def factors_of_length(prefix: Sequence[int], n: int) -> set[Word]:
    n = _require_positive(n, "n")
    w = tuple(prefix)
    if n > len(w):
        raise ValueError("prefix shorter than n")
    return {w[i : i + n] for i in range(len(w) - n + 1)}


def apply_morphism(seed: Word, rules: dict[int, Word], rounds: int) -> Word:
    word = seed
    for _ in range(rounds):
        out: list[int] = []
        for letter in word:
            out.extend(rules[letter])
        word = tuple(out)
    return word


def thue_morse_prefix(length: int) -> Word:
    """t(n) = popcount(n) mod 2, starting at n=0."""

    length = _require_positive(length, "length")
    return tuple(bin(n).count("1") % 2 for n in range(length))


def period_doubling_prefix(length: int) -> Word:
    """Fixed point of 0↦01, 1↦00 starting at 0."""

    length = _require_positive(length, "length")
    word = apply_morphism((0,), {0: (0, 1), 1: (0, 0)}, rounds=14)
    return word[:length]


def cantor_prefix(length: int) -> Word:
    """c(n)=1 iff the base-3 digits of n lie in {0,2}; c=σ^ω(1) for σ:0↦000,1↦101."""

    length = _require_positive(length, "length")

    def digit_ok(n: int) -> int:
        if n == 0:
            return 1
        while n:
            if n % 3 == 1:
                return 0
            n //= 3
        return 1

    return tuple(digit_ok(n) for n in range(length))


def thue_morse_state(index: int) -> int:
    return bin(index).count("1") % 2


def period_doubling_state(index: int) -> int:
    """v_2(index+1) mod 2; the 2-automatic value of the period-doubling word."""

    n = index + 1
    v = 0
    while n % 2 == 0:
        n //= 2
        v += 1
    return v % 2


def cantor_state(index: int) -> int:
    """DFAO state reading LSD base-3: 1 if a digit 1 has been seen."""

    n = index
    while n:
        if n % 3 == 1:
            return 1
        n //= 3
    return 0


FAMILIES: dict[str, dict] = {
    "thue_morse": {
        "base": 2,
        "alphabet": (0, 1),
        "prefix": thue_morse_prefix,
        "state": thue_morse_state,
        "start": THUE_MORSE_START,
        "prefix_len": PREFIX_LEN,
    },
    "period_doubling": {
        "base": 2,
        "alphabet": (0, 1),
        "prefix": period_doubling_prefix,
        "state": period_doubling_state,
        "start": PERIOD_DOUBLING_START,
        "prefix_len": PREFIX_LEN,
    },
    "cantor": {
        "base": 3,
        "alphabet": (0, 1),
        "prefix": cantor_prefix,
        "state": cantor_state,
        "start": CANTOR_START,
        "prefix_len": CANTOR_PREFIX_LEN,
    },
}


def factor_census_stable(prefix: Sequence[int], n: int) -> bool:
    """Whether the second half of the prefix adds no new length-n factors."""

    w = tuple(prefix)
    half = len(w) // 2
    if half < n:
        return False
    return factors_of_length(w[:half], n) == factors_of_length(w, n)


def relative_keys(
    factors: Iterable[Word],
    k: int,
    alphabet: Sequence[int],
) -> set[ClassKey]:
    items = list(factors)
    if not items:
        return set()
    raw = [class_key(u, k, alphabet) for u in items]
    parikhs = [key[2] for key in raw]
    if not parikhs[0]:
        return set(raw)
    mins = tuple(min(col) for col in zip(*parikhs))
    out: set[ClassKey] = set()
    for pref, suff, parikh in raw:
        rel = tuple(c - m for c, m in zip(parikh, mins))
        out.add((pref, suff, rel))
    return out


def naive_finite_keys(
    prefix: Sequence[int],
    n: int,
    k: int,
    state_fn,
) -> set[tuple[int, Word]]:
    """DFAO start-state plus suffix_{k-1}: finite, not a class invariant."""

    w = tuple(prefix)
    width = max(k - 1, 0)
    keys: set[tuple[int, Word]] = set()
    for i in range(len(w) - n + 1):
        factor = w[i : i + n]
        suff = factor[n - width :] if width else ()
        keys.add((state_fn(i), suff))
    return keys


def _record_transitions(
    prefix: Sequence[int],
    n: int,
    k: int,
    alphabet: Sequence[int],
    destination,
) -> tuple[dict[tuple[ClassKey, int], ClassKey], int]:
    """Map (class, letter) → destination class; count destination conflicts."""

    w = tuple(prefix)
    transitions: dict[tuple[ClassKey, int], ClassKey] = {}
    conflicts = 0
    for i in range(len(w) - n):
        src = class_key(w[i : i + n], k, alphabet)
        letter = w[i + n]
        dst = destination(w, i, n, k, alphabet)
        key = (src, letter)
        prior = transitions.get(key)
        if prior is None:
            transitions[key] = dst
        elif prior != dst:
            conflicts += 1
    return transitions, conflicts


def sliding_rauzy_from_prefix(
    prefix: Sequence[int],
    n: int,
    k: int,
    alphabet: Sequence[int],
) -> tuple[int, int, int]:
    """Fixed-length right shift: class count, minimized size, conflict count.

    A conflict means the KSZ class is not a sliding-window congruence.
    """

    w = tuple(prefix)
    letters = tuple(alphabet)
    factors = factors_of_length(w, n)
    classes = {class_key(u, k, alphabet) for u in factors}

    def dest(word, i, length, order, alph):
        return class_key(word[i + 1 : i + 1 + length], order, alph)

    transitions, conflicts = _record_transitions(w, n, k, alphabet, dest)
    if conflicts:
        return len(classes), len(classes), conflicts

    start = class_key(w[:n], k, alphabet)

    def delta(state, letter):
        if state == SINK:
            return SINK
        return transitions.get((state, letter), SINK)

    minimized = minimize_dfa(
        start=start,
        alphabet=letters,
        delta=delta,
        accepts=classes,
    )
    return len(classes), minimized.state_count, 0


def extension_conflicts(
    prefix: Sequence[int],
    n: int,
    k: int,
    alphabet: Sequence[int],
) -> int:
    """Growing-factor law: class of ``ua`` from class of ``u`` and letter ``a``.

    Zero conflicts means the KSZ triple plus the appended letter determines
    the next class — the local update the gate is testing.
    """

    def dest(word, i, length, order, alph):
        return class_key(word[i : i + length + 1], order, alph)

    _transitions, conflicts = _record_transitions(prefix, n, k, alphabet, dest)
    return conflicts


def empirical_kernel_count(
    values: Sequence[int],
    base: int,
    min_terms: int = KERNEL_TERMS,
) -> int:
    """Distinct length-``min_terms`` prefixes of b-kernel subsequences.

    This is an OBSERVATION on a finite table, not a proof of b-regularity.
    """

    if base < 2:
        raise ValueError("base must be at least 2")
    N = len(values)
    seen: set[tuple[int, ...]] = set()
    e = 0
    while True:
        step = base**e
        if step > N:
            break
        for r in range(step):
            seq: list[int] = []
            n = 0
            while True:
                idx = step * n + r
                if idx < 1:
                    n += 1
                    continue
                if idx > N:
                    break
                seq.append(values[idx - 1])
                n += 1
                if len(seq) >= min_terms:
                    break
            if len(seq) >= min_terms:
                seen.add(tuple(seq[:min_terms]))
        e += 1
    return len(seen)


def max_raw_coordinate(factors: Iterable[Word], k: int, alphabet: Sequence[int]) -> int:
    return max(
        (max(signature(u, k, alphabet), default=0) for u in factors),
        default=0,
    )


def family_row(
    name: str,
    k: int,
    n: int,
    prefix: Word,
    alphabet: Sequence[int],
    base: int,
    state_fn,
) -> dict:
    factors = factors_of_length(prefix, n)
    raw_factor_count = len(factors)
    sigs = {signature(u, k, alphabet) for u in factors}
    keys = {class_key(u, k, alphabet) for u in factors}
    rel = relative_keys(factors, k, alphabet)
    naive = naive_finite_keys(prefix, n, k, state_fn)
    raw_states, min_states, sliding_conflicts = sliding_rauzy_from_prefix(
        prefix, n, k, alphabet
    )
    return {
        "sequence": name,
        "base": base,
        "k": k,
        "n": n,
        "raw_factor_count": raw_factor_count,
        "k_abelian_class_count": len(keys),
        "raw_signature_count": len(sigs),
        "compressed_state_count": len(keys),
        "relative_state_count": len(rel),
        "naive_dfao_suffix_count": len(naive),
        "rauzy_raw": raw_states,
        "rauzy_min": min_states,
        "sliding_conflicts": sliding_conflicts,
        "extension_conflicts": extension_conflicts(prefix, n, k, alphabet),
        "max_raw_coordinate": max_raw_coordinate(factors, k, alphabet),
        "stable": factor_census_stable(prefix, n),
        "class_equals_signature": len(keys) == len(sigs),
    }


def family_complexity_sequence(
    name: str,
    k: int,
    n_max: int,
    prefix: Word,
    alphabet: Sequence[int],
) -> tuple[int, ...]:
    return tuple(
        k_abelian_classes(factors_of_length(prefix, n), k, alphabet)
        for n in range(1, n_max + 1)
    )


def union_relative_growth(
    prefix: Word,
    k: int,
    alphabet: Sequence[int],
    n_values: Sequence[int],
) -> list[int]:
    seen: set[ClassKey] = set()
    growth: list[int] = []
    for n in n_values:
        seen |= relative_keys(factors_of_length(prefix, n), k, alphabet)
        growth.append(len(seen))
    return growth


def triage_report(
    n_max: int = CENSUS_N,
    families: Sequence[str] = ("thue_morse", "period_doubling", "cantor"),
) -> dict:
    n_max = _require_positive(n_max, "n_max")
    rows: list[dict] = []
    complexity: dict[str, dict[int, tuple[int, ...]]] = {}
    kernels: dict[str, dict[int, int]] = {}
    growth: dict[str, dict[int, list[int]]] = {}
    prefixes: dict[str, Word] = {}

    for name in families:
        spec = FAMILIES[name]
        alphabet = spec["alphabet"]
        base = spec["base"]
        prefix = spec["prefix"](spec["prefix_len"])
        prefixes[name] = prefix
        ks = (1, 2) if name != "cantor" else (1, 2, 3)
        complexity[name] = {}
        kernels[name] = {}
        growth[name] = {}
        for k in ks:
            rho = family_complexity_sequence(name, k, n_max, prefix, alphabet)
            complexity[name][k] = rho
            kernels[name][k] = empirical_kernel_count(rho, base)
            sample_ns = tuple(n for n in (1, 2, 4, 8, 12, 16, 24) if n <= n_max)
            growth[name][k] = union_relative_growth(prefix, k, alphabet, sample_ns)
            for n in sample_ns:
                rows.append(
                    family_row(
                        name,
                        k,
                        n,
                        prefix,
                        alphabet,
                        base,
                        spec["state"],
                    )
                )

    return {
        "rows": rows,
        "complexity": complexity,
        "kernels": kernels,
        "relative_union_growth": growth,
        "prefixes": {name: prefixes[name][:16] for name in prefixes},
        "n_max": n_max,
        "prefix_len": {name: FAMILIES[name]["prefix_len"] for name in families},
    }
