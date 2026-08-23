"""View-model for the rewrite-calculus companion page.

Instantiates existing ``bt.calculus`` maps and ``rewrite_once``. Does not
install Add rules, does not expose word-table fragments, and does not
prove anything: Lean remains the authority.
"""

from __future__ import annotations

from dataclasses import dataclass

from bt.calculus.derivative import D, lsd
from bt.calculus.expressions import ED, EI0, EIm, EInt, EIp, ENeg, EShift3, Expr, render
from bt.calculus.integral import I_minus, I_plus
from bt.calculus.rewrite import rewrite_expr, rewrite_once

UNARY_OPS: tuple[str, ...] = ("D", "I-", "I0", "I+", "S", "N")
PUSHABLE: frozenset[str] = frozenset({"D", "I-", "I0", "I+", "S"})
CTORS: tuple[str, ...] = ("S", "I+", "I-", "N")

OPERATOR_HELP: dict[str, str] = {
    "D": "D(n) = (n − lsd(n))/3. Drops the least-significant balanced trit.",
    "I-": "I−(x) = −1 + 3x. Prepends trit −1. Left inverse of D on that residue.",
    "I0": "I0(x) = 3x. Prepends trit 0. Same integer map as S; the rule I0 → S orients the spelling.",
    "I+": "I+(x) = 1 + 3x. Prepends trit +1. Left inverse of D on that residue.",
    "S": "S(n) = 3n. Shift: append a zero trit. Same integer map as I0.",
    "N": "N(n) = −n. Negation. The oriented commute is N(D(t)) → D(N(t)).",
}
AFFINE_HELP = (
    "Affine constructors: S(x)=3x, I+(x)=1+3x, I−(x)=−1+3x, N(x)=−x. "
    "I0 is identified with S."
)

# (U, V, W) — eight concrete triples; I_a rows are the six parameterized ones.
EXACT_TRIPLES: tuple[tuple[str, str, str], ...] = (
    ("S", "S", "S"),
    ("N", "N", "N"),
    ("I+", "S", "I+"),
    ("S", "I+", "I+"),
    ("I-", "S", "I-"),
    ("S", "I-", "I-"),
    ("I+", "I-", "S"),
    ("I-", "I+", "S"),
)

_WRAP: dict[str, type] = {
    "D": ED,
    "I-": EIm,
    "I0": EI0,
    "I+": EIp,
    "S": EShift3,
    "N": ENeg,
}

_PEEL: dict[type, str] = {cls: name for name, cls in _WRAP.items()}

_SLOPE_CONST: dict[str, tuple[int, int]] = {
    "S": (3, 0),
    "I+": (3, 1),
    "I-": (3, -1),
    "N": (-1, 0),
}

UNARY_PRESETS: dict[str, tuple[str, ...]] = {
    "N(D(x))": ("N", "D"),
    "D(N(x))": ("D", "N"),
    "D(S(x))": ("D", "S"),
    "N(I+(x))": ("N", "I+"),
    "I0(x)": ("I0",),
    "x": (),
}

CLAIM_ROWS: tuple[dict[str, str], ...] = (
    {
        "claim": "Unique balanced-ternary expansion",
        "evidence": "classical",
        "novelty": "KNOWN",
        "ledger": "—",
    },
    {
        "claim": "Newman / Knuth–Bendix",
        "evidence": "classical method",
        "novelty": "KNOWN",
        "ledger": "—",
    },
    {
        "claim": "Unary {D, I_a, S, N} canonical form",
        "evidence": "EXACT — LEAN VERIFIED",
        "novelty": "PROJECT-SPECIFIC",
        "ledger": "BTC-op-fragment-nd-nf",
    },
    {
        "claim": "Add is not D-local",
        "evidence": "EXACT — LEAN VERIFIED",
        "novelty": "PROJECT-SPECIFIC",
        "ledger": "BTC-add-not-D-local",
    },
    {
        "claim": "Constructor-sum identities are the six rows",
        "evidence": "EXACT — LEAN VERIFIED",
        "novelty": "PROJECT-SPECIFIC",
        "ledger": "BTC-constructor-sum-class",
    },
    {
        "claim": "Named carry-free push-in fails at D∘S",
        "evidence": "EXACT — LEAN VERIFIED",
        "novelty": "PROJECT-SPECIFIC",
        "ledger": "BTC-push-in-S-peak",
    },
    {
        "claim": "Restricted carry-state conjunction",
        "evidence": "EXACT — LEAN VERIFIED",
        "novelty": "PROJECT-SPECIFIC",
        "ledger": "BTC-add-requires-carry-state",
    },
    {
        "claim": "Every finite exact Add-tree TRS is already a CAS",
        "evidence": "EXACT — HUMAN PROOF",
        "novelty": "PROJECT-SPECIFIC",
        "ledger": "BTC-add-affine-only",
    },
)


@dataclass(frozen=True)
class UnaryTerm:
    """Outermost-first unary spine over a hole ``x``."""

    ops: tuple[str, ...]

    def render(self) -> str:
        text = "x"
        for op in reversed(self.ops):
            text = f"{op}({text})"
        return text

    def i0_count(self) -> int:
        return self.ops.count("I0")

    def n_inversions(self) -> int:
        inv = 0
        for i, op in enumerate(self.ops):
            if op == "N":
                inv += sum(1 for inner in self.ops[i + 1 :] if inner in PUSHABLE)
        return inv

    def size(self) -> int:
        return len(self.ops) + 1

    def rank(self) -> tuple[int, int, int]:
        return (self.i0_count(), self.n_inversions(), self.size())

    def as_expr(self, hole: Expr) -> Expr:
        expr = hole
        for op in reversed(self.ops):
            expr = _WRAP[op](expr)
        return expr

    def evaluate(self, n: int) -> int:
        from bt.calculus.semantics import evaluate

        return int(evaluate(self.as_expr(EInt(n))))


def unary_from_ops(ops: tuple[str, ...]) -> UnaryTerm:
    unknown = [op for op in ops if op not in _WRAP]
    if unknown:
        raise ValueError(f"unknown unary op {unknown[0]}")
    return UnaryTerm(ops)


def _peel(expr: Expr) -> UnaryTerm | None:
    ops: list[str] = []
    cur: Expr = expr
    while not isinstance(cur, EInt):
        name = _PEEL.get(type(cur))
        if name is None or not hasattr(cur, "arg"):
            return None
        ops.append(name)
        cur = cur.arg  # type: ignore[attr-defined]
    return UnaryTerm(tuple(ops))


def wrap_unary(term: UnaryTerm, op: str) -> UnaryTerm:
    if op not in _WRAP:
        raise ValueError(f"unknown unary op {op}")
    return UnaryTerm((op,) + term.ops)


def step_unary(term: UnaryTerm) -> tuple[UnaryTerm, str | None]:
    nxt, reason = rewrite_once(term.as_expr(EInt(0)))
    peeled = _peel(nxt)
    if peeled is None:
        return term, reason
    return peeled, reason


def normalize_unary(term: UnaryTerm) -> tuple[UnaryTerm, tuple[str, ...], int]:
    nf, reasons, steps = rewrite_expr(term.as_expr(EInt(0)))
    peeled = _peel(nf)
    if peeled is None:
        return term, reasons, steps
    return peeled, reasons, steps


@dataclass(frozen=True)
class CarryView:
    x: int
    y: int
    lsd_x: int
    lsd_y: int
    d_x: int
    d_y: int
    d_sum: int
    d_sum_naive: int
    carry: int
    not_d_local_witness: bool


def carry_view(x: int, y: int) -> CarryView:
    dx, dy = D(x), D(y)
    dsum = D(x + y)
    carry = dsum - dx - dy
    same_d = dx == 0 and dy == 0
    return CarryView(
        x=x,
        y=y,
        lsd_x=int(lsd(x)),
        lsd_y=int(lsd(y)),
        d_x=dx,
        d_y=dy,
        d_sum=dsum,
        d_sum_naive=dx + dy,
        carry=carry,
        not_d_local_witness=same_d and dsum != 0,
    )


def apply_ctor(name: str, t: int) -> int:
    if name == "S":
        return 3 * t
    if name == "I+":
        return I_plus(t)
    if name == "I-":
        return I_minus(t)
    if name == "N":
        return -t
    raise ValueError(f"unknown constructor {name}")


@dataclass(frozen=True)
class ConstructorSumView:
    u: str
    v: str
    w: str
    slope_u: int
    slope_v: int
    slope_w: int
    const_u: int
    const_v: int
    const_w: int
    exact: bool
    left: int
    right: int
    residue: int | None
    reason: str


def constructor_sum_view(u: str, v: str, w: str, x: int = 0, y: int = 0) -> ConstructorSumView:
    su, cu = _SLOPE_CONST[u]
    sv, cv = _SLOPE_CONST[v]
    sw, cw = _SLOPE_CONST[w]
    exact = su == sw and sv == sw and cu + cv == cw
    left = apply_ctor(u, x) + apply_ctor(v, y)
    right = apply_ctor(w, x + y)
    residue = None
    if exact:
        reason = "slopes match and constants add"
    elif su != sw or sv != sw:
        reason = "slope mismatch: W cannot be a function of x+y alone"
    else:
        residue = cu + cv - cw
        reason = f"constant mismatch; residue {residue} is not a trit" if residue not in (
            -1,
            0,
            1,
        ) else f"constant mismatch; residue {residue}"
    return ConstructorSumView(
        u=u,
        v=v,
        w=w,
        slope_u=su,
        slope_v=sv,
        slope_w=sw,
        const_u=cu,
        const_v=cv,
        const_w=cw,
        exact=exact,
        left=left,
        right=right,
        residue=residue,
        reason=reason,
    )


@dataclass(frozen=True)
class PushInPeakView:
    x: int
    y: int
    peak: str
    left: str
    right: str
    left_value: int
    right_value: int
    agree: bool


def push_in_peak(x: int = 1, y: int = 1) -> PushInPeakView:
    left = x + y
    right = D((3 * x) + (3 * y))
    return PushInPeakView(
        x=x,
        y=y,
        peak="D(S(Add(X, Y)))",
        left="Add(X, Y)",
        right="D(Add(S(X), S(Y)))",
        left_value=left,
        right_value=right,
        agree=left == right,
    )


def render_closed(expr: Expr) -> str:
    return render(expr)
