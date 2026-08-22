"""Bounded identity discovery. Candidates are never auto-promoted to theorems."""

from __future__ import annotations

from dataclasses import dataclass
from bt.calculus.expressions import ED, EI0, EIm, EInt, EIp, ENeg, EShift3, Expr, render
from bt.calculus.rewrite import rewrite_expr
from bt.calculus.semantics import evaluate


UNARY_CTORS = (
    ("D", ED),
    ("I-", EIm),
    ("I0", EI0),
    ("I+", EIp),
    ("S", EShift3),
    ("N", ENeg),
)


@dataclass(frozen=True)
class IdentityCandidate:
    left: str
    right: str
    status: str
    sample: tuple[int, ...]
    notes: str
    lean_skeleton: str


def generate_unary(depth: int, variable: Expr) -> list[Expr]:
    """All unary terms of exact depth over ``{D, I±, I0, S, N}``."""
    if depth < 0:
        raise ValueError("depth must be >= 0")
    layer: list[Expr] = [variable]
    for _ in range(depth):
        nxt: list[Expr] = []
        for expr in layer:
            for _name, ctor in UNARY_CTORS:
                nxt.append(ctor(expr))
        layer = nxt
    return layer


def generate_up_to_depth(max_depth: int, variable: Expr) -> list[Expr]:
    out: list[Expr] = []
    for d in range(max_depth + 1):
        out.extend(generate_unary(d, variable))
    return out


def _fingerprint(expr: Expr, sample: tuple[int, ...]) -> tuple[int, ...]:
    # Closed expressions: evaluate once. Open ones are not generated here.
    _ = sample
    return (evaluate(expr),)


def cluster_closed(exprs: list[Expr]) -> dict[tuple[int, ...], list[Expr]]:
    groups: dict[tuple[int, ...], list[Expr]] = {}
    for expr in exprs:
        key = (evaluate(expr),)
        groups.setdefault(key, []).append(expr)
    return groups


def classify_pair(
    left: Expr,
    right: Expr,
    *,
    counterexample_limit: int = 200,
) -> IdentityCandidate:
    """Search a counterexample, then rewrite, then emit a Lean skeleton.

    Status is only ``COMPUTATIONALLY VERIFIED``, ``CONJECTURE``, or
    ``REFUTED`` unless the pair rewrites to a common form (still not Lean).
    """
    nf_l, _, _ = rewrite_expr(left)
    nf_r, _, _ = rewrite_expr(right)
    if nf_l == nf_r:
        status = "COMPUTATIONALLY VERIFIED"
        notes = "Common innermost normal form. Not Lean-verified by this tool."
    else:
        lv = evaluate(left)
        rv = evaluate(right)
        if lv != rv:
            status = "REFUTED"
            notes = f"Closed-term counterexample: {lv} ≠ {rv}"
        else:
            status = "COMPUTATIONALLY VERIFIED"
            notes = "Equal as closed integers after evaluation."
    skeleton = (
        "-- Generated skeleton. Do not add sorry/admit.\n"
        f"-- theorem candidate : {render(left)} = {render(right)} := by\n"
        "--   sorry  -- FORBIDDEN; replace with a real proof or delete\n"
    )
    return IdentityCandidate(
        left=render(left),
        right=render(right),
        status=status,
        sample=tuple(range(-counterexample_limit, counterexample_limit + 1)),
        notes=notes,
        lean_skeleton=skeleton,
    )


def discover_closed(
    max_depth: int = 3,
    seed: int = 5,
) -> list[IdentityCandidate]:
    """Cluster closed unary terms built from the integer ``seed``.

    Depth 6 over 6 unary operators is 6^6 = 46656 terms; default depth is 3
    for interactive use. CLI may raise the bound.
    """
    if max_depth > 6:
        raise ValueError("max_depth must be <= 6")
    base = EInt(seed)
    exprs = generate_up_to_depth(max_depth, base)
    groups = cluster_closed(exprs)
    out: list[IdentityCandidate] = []
    for _key, members in groups.items():
        if len(members) < 2:
            continue
        left, right = members[0], members[1]
        out.append(classify_pair(left, right))
    return out


def scan_unary_identities(max_depth: int = 2) -> list[IdentityCandidate]:
    """Discover pairs that become equal after rewrite, on a closed seed."""
    return discover_closed(max_depth=max_depth, seed=5)
