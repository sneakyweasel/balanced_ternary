"""Abstract local normalization rewrite on coefficient vectors.

The unique balanced residue of ``c`` is

    r = ((c + 1) mod 3) - 1 ∈ {-1,0,+1},    q = (c - r) / 3.

A legal step at index ``i`` exists iff ``c_i`` is not a trit. The relation
``P -> P'`` is one such step and does not depend on sweep order.

Ranking for termination: the finite-support sequence ``(|c_0|, |c_1|, ...)``
strictly decreases in lexicographic order, because a step at ``i`` leaves
positions ``< i`` unchanged and replaces ``|c_i| >= 2`` by ``|r| <= 1``.
"""

from __future__ import annotations

from bt.normtheory.coeffword import CoeffWord
from bt.normalization import rewrite_sum


def _require_int(n: int, name: str = "n") -> int:
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"{name} must be int, got {type(n).__name__}")
    return n


def balanced_divmod(c: int) -> tuple[int, int]:
    """Unique ``(r, q)`` with ``c = 3q + r`` and ``r in {-1,0,+1}``."""
    c = _require_int(c, "c")
    r = ((c + 1) % 3) - 1
    q = (c - r) // 3
    return r, q


def agrees_with_rewrite_sum_on_small() -> bool:
    """``balanced_divmod`` coincides with ``rewrite_sum`` on ``[-3, 3]``."""
    for s in range(-3, 4):
        if balanced_divmod(s) != rewrite_sum(s):
            return False
    return True


def is_legal_site(word: CoeffWord, i: int) -> bool:
    i = _require_int(i, "i")
    if i < 0:
        return False
    return word.coefficient(i) not in (-1, 0, 1)


def legal_sites(word: CoeffWord) -> tuple[int, ...]:
    extra = ()
    # A high implicit zero is never a site.
    return tuple(i for i in range(word.width()) if is_legal_site(word, i)) + extra


def normalize_step(word: CoeffWord, i: int) -> CoeffWord:
    """One legal carry/borrow at index ``i``. Raises if the site is illegal."""
    i = _require_int(i, "i")
    if not is_legal_site(word, i):
        raise ValueError(f"no legal rewrite at index {i} for {word.coeffs}")
    coeffs = list(word.coeffs)
    while len(coeffs) <= i + 1:
        coeffs.append(0)
    r, q = balanced_divmod(coeffs[i])
    coeffs[i] = r
    coeffs[i + 1] += q
    return CoeffWord(tuple(coeffs))


def successors(word: CoeffWord) -> tuple[tuple[int, CoeffWord], ...]:
    """All one-step ``P -> P'`` rewrites, as ``(index, result)``."""
    return tuple((i, normalize_step(word, i)) for i in legal_sites(word))


def irreducible(word: CoeffWord) -> bool:
    return word.is_canonical()


def lex_abs_key(word: CoeffWord) -> tuple[int, ...]:
    """Lexicographic rank ``(|c_0|, |c_1|, ...)``. Steps strictly decrease this."""
    return word.abs_tuple()


def lex_decreases(before: CoeffWord, after: CoeffWord) -> bool:
    a = before.abs_tuple()
    b = after.abs_tuple()
    n = max(len(a), len(b))
    a = a + (0,) * (n - len(a))
    b = b + (0,) * (n - len(b))
    return b < a


def weighted_l1(word: CoeffWord, alpha_num: int, alpha_den: int) -> tuple[int, int]:
    """``Σ |c_i| (alpha_num/alpha_den)^i`` as a rational ``(num, den)``."""
    num = 0
    den = 1
    pow_n = 1
    pow_d = 1
    for c in word.coeffs:
        num = num * pow_d + abs(c) * pow_n * den
        den = den * pow_d
        pow_n *= alpha_num
        pow_d *= alpha_den
        g = _gcd(num, den)
        num //= g
        den //= g
    return num, den


def _gcd(a: int, b: int) -> int:
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a or 1


def joinable(left: CoeffWord, right: CoeffWord, limit: int = 64) -> bool:
    """True if ``left`` and ``right`` have a common ``->*`` descendant within ``limit``."""
    from collections import deque

    def closure(start: CoeffWord) -> set[tuple[int, ...]]:
        seen = {start.coeffs}
        queue = deque([start])
        while queue and len(seen) < limit:
            current = queue.popleft()
            for _i, nxt in successors(current):
                if nxt.coeffs not in seen:
                    seen.add(nxt.coeffs)
                    queue.append(nxt)
        return seen

    a = closure(left)
    b = closure(right)
    return bool(a & b)


def locally_confluent(word: CoeffWord) -> bool:
    """Every one-step fork from ``word`` joins (bounded descendant search)."""
    succs = successors(word)
    for i, (ia, wa) in enumerate(succs):
        for ib, wb in succs[i + 1 :]:
            if not joinable(wa, wb):
                return False
    return True


def critical_pair_join(a: int, b: int) -> bool:
    """Overlapping sites ``0`` and ``1`` on the two-coefficient word ``[a, b]``."""
    if a in (-1, 0, 1) or b in (-1, 0, 1):
        return True
    word = CoeffWord((a, b))
    via_low = normalize_step(word, 0)
    via_high = normalize_step(word, 1)
    return joinable(via_low, via_high, limit=128)


def weighted_l1_increases_on_two() -> bool:
    """Witness that ``Σ |c_i| (3/2)^i`` increases on ``[2] -> [-1, 1]``."""
    before = CoeffWord((2,))
    after = normalize_step(before, 0)
    bn, bd = weighted_l1(before, 3, 2)
    an, ad = weighted_l1(after, 3, 2)
    return an * bd > bn * ad
