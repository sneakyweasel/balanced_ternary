"""Classified rewrite rules for operator words and calculus expressions.

Word-level rules are the canonical store previously kept in
``research.operator_dynamics.algebra``. Tree rules are added only when
they are exact integer identities.
"""

from __future__ import annotations

from dataclasses import dataclass

from bt.calculus.expressions import (
    EAdd,
    ECmp3,
    ED,
    EI0,
    EIm,
    EInt,
    EIp,
    EMul,
    ENeg,
    ENormalize,
    ESelect3,
    EShift3,
    ETrit,
    Expr,
)


@dataclass(frozen=True)
class WordRewriteRule:
    """Rewrite on operator words in mathematical (left-last) order."""

    src: tuple[str, ...]
    dst: tuple[str, ...]
    reason: str
    sound: bool = True
    terminating: bool = True
    simplifying: bool = True
    reversible: bool = False


# Exact identities on the intersection of domains. Classification is
# local: each rule is sound and size-nonincreasing on words. The whole
# table is not locally confluent (peak N∘W∘W → N∘K3 | K3∘N) and the
# two-way commutes are not terminating. The simplifying-only fragment
# ``WORD_SIMP_RULES`` is terminating and locally confluent. The opt-in
# fragment ``WORD_WN_RULES`` adds one-way N∘S, N∘W, and N∘K3; it is
# also terminating and locally confluent. The opt-in fragment
# ``WORD_WND_RULES`` further adds one-way N∘D and the exact I±
# sign-flips N∘Ip→Im∘N, N∘Im→Ip∘N; it is terminating and locally
# confluent. Default production rules are not widened: N∘K3 and the
# I± sign-flips are not installed here.
WORD_REWRITE_RULES: tuple[WordRewriteRule, ...] = (
    WordRewriteRule(("N", "N"), (), "N∘N = id", reversible=True),
    WordRewriteRule(("D", "S"), (), "D∘S = id"),
    WordRewriteRule(("D", "Ip"), (), "D∘Ip = id"),
    WordRewriteRule(("D", "Im"), (), "D∘Im = id"),
    WordRewriteRule(("D", "I0"), (), "D∘I0 = id"),
    WordRewriteRule(("Wz", "Wz"), (), "Wz∘Wz = id", reversible=True),
    WordRewriteRule(("Wt", "Wt"), (), "Wt∘Wt = id", reversible=True),
    WordRewriteRule(("H2", "M2"), (), "H2∘M2 = id"),
    WordRewriteRule(("H3", "S"), (), "H3∘S = id"),
    WordRewriteRule(("K3", "K3"), ("K3",), "K3 is a projection"),
    WordRewriteRule(("W", "W"), ("K3",), "W∘W = K3 (strip factors of 3)"),
    WordRewriteRule(("W", "S"), ("W",), "W∘S = W  (appending zeros does not change W)"),
    WordRewriteRule(("K3", "S"), ("K3",), "K3∘S = K3"),
    WordRewriteRule(
        ("K3", "W"),
        ("W",),
        "K3∘W = W  (W(n) is never divisible by 3 unless 0)",
    ),
    WordRewriteRule(("W", "K3"), ("W",), "W∘K3 = W"),
    WordRewriteRule(("N", "S"), ("S", "N"), "N∘S = S∘N", reversible=True, simplifying=False),
    WordRewriteRule(("S", "N"), ("N", "S"), "S∘N = N∘S", reversible=True, simplifying=False),
    WordRewriteRule(("N", "D"), ("D", "N"), "N∘D = D∘N", reversible=True, simplifying=False),
    WordRewriteRule(("D", "N"), ("N", "D"), "D∘N = N∘D", reversible=True, simplifying=False),
    WordRewriteRule(("N", "W"), ("W", "N"), "N∘W = W∘N", reversible=True, simplifying=False),
    WordRewriteRule(("W", "N"), ("N", "W"), "W∘N = N∘W", reversible=True, simplifying=False),
    WordRewriteRule(("N", "M2"), ("M2", "N"), "N∘M2 = M2∘N", reversible=True, simplifying=False),
    WordRewriteRule(("M2", "N"), ("N", "M2"), "M2∘N = N∘M2", reversible=True, simplifying=False),
    WordRewriteRule(("N", "Wz"), ("Wz", "N"), "N∘Wz = Wz∘N", reversible=True, simplifying=False),
    WordRewriteRule(("Wz", "N"), ("N", "Wz"), "Wz∘N = N∘Wz", reversible=True, simplifying=False),
    WordRewriteRule(("N", "Wt"), ("Wt", "N"), "N∘Wt = Wt∘N", reversible=True, simplifying=False),
    WordRewriteRule(("Wt", "N"), ("N", "Wt"), "Wt∘N = N∘Wt", reversible=True, simplifying=False),
    WordRewriteRule(("S", "M2"), ("M2", "S"), "S∘M2 = M2∘S", reversible=True, simplifying=False),
    WordRewriteRule(("M2", "S"), ("S", "M2"), "M2∘S = S∘M2", reversible=True, simplifying=False),
    WordRewriteRule(("Wz", "S"), ("S", "Wz"), "Wz∘S = S∘Wz", reversible=True, simplifying=False),
    WordRewriteRule(("S", "Wz"), ("Wz", "S"), "S∘Wz = Wz∘S", reversible=True, simplifying=False),
    WordRewriteRule(("I0",), ("S",), "I0 = S", reversible=True),
)


# Named production fragment: every ``simplifying=True`` row. No Add,
# no two-way commutes, no ``N∘K3`` (that commute is not in the table).
WORD_SIMP_RULES: tuple[WordRewriteRule, ...] = tuple(
    rule for rule in WORD_REWRITE_RULES if rule.simplifying
)


def _production_rule(src: tuple[str, ...]) -> WordRewriteRule:
    for rule in WORD_REWRITE_RULES:
        if rule.src == src:
            return rule
    raise KeyError(src)


# Exact (K3 strips factors of 3; v3(-n)=v3(n)). Not a production row.
WORD_N_K3_RULE = WordRewriteRule(
    ("N", "K3"),
    ("K3", "N"),
    "N∘K3 = K3∘N",
    simplifying=False,
    reversible=True,
)


# Opt-in W+N fragment: SIMP plus one-way N∘S, N∘W, and N∘K3.
# Does not include N∘D (peak N∘D∘I± without word I± sign-flips)
# or any reverse commute. The W+N+D enlargement is WORD_WND_RULES.
WORD_WN_RULES: tuple[WordRewriteRule, ...] = WORD_SIMP_RULES + (
    _production_rule(("N", "S")),
    _production_rule(("N", "W")),
    WORD_N_K3_RULE,
)


# Exact on ℤ: I_a(x)=a+3x, so N(I+(n))=I-(-n) and N(I-(n))=I+(-n).
# Tree rules N(I+(x))→I-(N(x)) and N(I-(x))→I+(N(x)). Not production rows.
WORD_N_IP_RULE = WordRewriteRule(
    ("N", "Ip"),
    ("Im", "N"),
    "N∘Ip = Im∘N",
    simplifying=False,
    reversible=True,
)
WORD_N_IM_RULE = WordRewriteRule(
    ("N", "Im"),
    ("Ip", "N"),
    "N∘Im = Ip∘N",
    simplifying=False,
    reversible=True,
)


# Opt-in W+N+D fragment: WN plus one-way N∘D and the I± sign-flips.
# Reverse N∘D and reverse sign-flips are length-preserving cycles.
WORD_WND_RULES: tuple[WordRewriteRule, ...] = WORD_WN_RULES + (
    _production_rule(("N", "D")),
    WORD_N_IP_RULE,
    WORD_N_IM_RULE,
)


# Compatibility tuple used by research.operator_dynamics.algebra.
REWRITE_RULES: tuple[tuple[tuple[str, ...], tuple[str, ...], str], ...] = tuple(
    (rule.src, rule.dst, rule.reason) for rule in WORD_REWRITE_RULES
)


def rewrite_word(
    factors: tuple[str, ...],
    *,
    simplifying_only: bool = False,
    rules: tuple[WordRewriteRule, ...] | None = None,
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """Left-to-right word rewrite until stable.

    The full table is not locally confluent. Pass
    ``simplifying_only=True`` for ``WORD_SIMP_RULES``,
    ``rules=WORD_WN_RULES`` for the opt-in W+N fragment, or
    ``rules=WORD_WND_RULES`` for the opt-in W+N+D fragment. Default
    production ``WORD_REWRITE_RULES`` is unchanged.
    """
    if rules is not None:
        table = rules
    elif simplifying_only:
        table = WORD_SIMP_RULES
    else:
        table = WORD_REWRITE_RULES
    word = list(factors)
    used: list[str] = []
    changed = True
    while changed:
        changed = False
        for rule in table:
            k = len(rule.src)
            if k == 0:
                continue
            i = 0
            while i + k <= len(word):
                if tuple(word[i : i + k]) == rule.src:
                    word[i : i + k] = list(rule.dst)
                    used.append(rule.reason)
                    changed = True
                    i = max(0, i - k)
                else:
                    i += 1
    return tuple(word), tuple(used)


def _map_arg(expr: Expr, fn) -> Expr:
    if isinstance(expr, (EInt, ETrit)):
        return expr
    if isinstance(expr, ENeg):
        return ENeg(fn(expr.arg))
    if isinstance(expr, ED):
        return ED(fn(expr.arg))
    if isinstance(expr, EIm):
        return EIm(fn(expr.arg))
    if isinstance(expr, EI0):
        return EI0(fn(expr.arg))
    if isinstance(expr, EIp):
        return EIp(fn(expr.arg))
    if isinstance(expr, EShift3):
        return EShift3(fn(expr.arg))
    if isinstance(expr, ENormalize):
        return ENormalize(fn(expr.arg))
    if isinstance(expr, EAdd):
        return EAdd(fn(expr.left), fn(expr.right))
    if isinstance(expr, EMul):
        return EMul(fn(expr.left), fn(expr.right))
    if isinstance(expr, ECmp3):
        return ECmp3(fn(expr.left), fn(expr.right))
    if isinstance(expr, ESelect3):
        return ESelect3(fn(expr.cond), fn(expr.x_minus), fn(expr.x_zero), fn(expr.x_plus))
    raise TypeError(f"unknown expression {type(expr).__name__}")


def _step(expr: Expr) -> tuple[Expr, str | None]:
    """One outermost exact tree rule, or None if this node is not a redex."""
    if isinstance(expr, EI0):
        return EShift3(expr.arg), "I0(x) → S(x)"
    if isinstance(expr, ENormalize):
        return expr.arg, "Nrm(x) → x"
    if isinstance(expr, ED):
        inner = expr.arg
        if isinstance(inner, EIm):
            return inner.arg, "D(I-(x)) → x"
        if isinstance(inner, EIp):
            return inner.arg, "D(I+(x)) → x"
        if isinstance(inner, EI0):
            return inner.arg, "D(I0(x)) → x"
        if isinstance(inner, EShift3):
            return inner.arg, "D(S(x)) → x"
    if isinstance(expr, ENeg):
        inner = expr.arg
        if isinstance(inner, ENeg):
            return inner.arg, "N(N(x)) → x"
        if isinstance(inner, EShift3):
            return EShift3(ENeg(inner.arg)), "N(S(x)) → S(N(x))"
        if isinstance(inner, EI0):
            return EShift3(ENeg(inner.arg)), "N(I0(x)) → S(N(x))"
        if isinstance(inner, EIm):
            return EIp(ENeg(inner.arg)), "N(I-(x)) → I+(N(x))"
        if isinstance(inner, EIp):
            return EIm(ENeg(inner.arg)), "N(I+(x)) → I-(N(x))"
        if isinstance(inner, ED):
            return ED(ENeg(inner.arg)), "N(D(x)) → D(N(x))"
    return expr, None


def rewrite_once(expr: Expr) -> tuple[Expr, str | None]:
    """Innermost-left rewrite: contract a redex after rewriting children."""
    rewritten = _map_arg(expr, lambda child: rewrite_once(child)[0])
    nxt, reason = _step(rewritten)
    return nxt, reason


def rewrite_expr(expr: Expr, *, max_steps: int = 10_000) -> tuple[Expr, tuple[str, ...], int]:
    """Innermost rewrite until a normal form or ``max_steps``.

    Termination holds for the operator fragment ``{D, I_a, S, N}`` because
    every rule strictly decreases the lex rank ``(I0-count, N-inversion,
    size)``, where ``N-inversion`` counts pairs ``(N-node, pushable
    descendant)`` and pushable means ``S``, ``I±``, ``I0``, or ``D``.
    ``N(D(x)) → D(N(x))`` drops the inversion coordinate by one. Global
    confluence of the full expression language is not claimed.
    Exact push-in ``S``-distributivity through ``Add`` or ``Mul``
    overlaps ``D∘S = id`` in a non-joining peak; finite factor-out
    Add is already AC-engine / CAS territory. Integer sums of
    constructor terms are affine / coefficient-word objects, not a
    tree TRS on ``Add``. Those rules stay out of ``_step`` (see
    ``docs/theory/rewrite_calculus.md``).
    """
    used: list[str] = []
    steps = 0
    current = expr
    while steps < max_steps:
        nxt, reason = rewrite_once(current)
        if reason is None and nxt == current:
            break
        if reason is not None:
            used.append(reason)
        if nxt == current:
            break
        current = nxt
        steps += 1
    return current, tuple(used), steps


# Tree rules that are exact as integer identities (for documentation / Lean).
TREE_RULES: tuple[tuple[str, str], ...] = (
    ("D(I-(x))", "x"),
    ("D(I0(x))", "x"),
    ("D(I+(x))", "x"),
    ("D(S(x))", "x"),
    ("I0(x)", "S(x)"),
    ("N(N(x))", "x"),
    ("N(S(x))", "S(N(x))"),
    ("N(I-(x))", "I+(N(x))"),
    ("N(I+(x))", "I-(N(x))"),
    ("N(D(x))", "D(N(x))"),
    ("Nrm(x)", "x"),
)
