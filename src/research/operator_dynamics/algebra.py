"""Symbolic compositions and commutators of balanced-ternary operators.

Composition strings are written in mathematical order: ``W D N S`` means
``W ∘ D ∘ N ∘ S``, i.e. apply ``S``, then ``N``, then ``D``, then ``W``.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product

from bt.calculus.rewrite import REWRITE_RULES
from bt.operators import (
    ALGEBRA_GENERATORS,
    OperatorDomainError,
    get_operator,
)
from bt.representation import encode


@dataclass(frozen=True)
class Composition:
    """Operator word in mathematical (left-last) order."""

    factors: tuple[str, ...]

    def __str__(self) -> str:
        return " ".join(self.factors) if self.factors else "id"

    @property
    def application_order(self) -> tuple[str, ...]:
        return tuple(reversed(self.factors))

    def apply(self, n: int) -> int:
        value = n
        for symbol in self.application_order:
            value = get_operator(symbol).apply(value)
        return value

    def in_domain(self, n: int) -> bool:
        value = n
        for symbol in self.application_order:
            op = get_operator(symbol)
            if not op.in_domain(value):
                return False
            try:
                value = op.apply(value)
            except OperatorDomainError:
                return False
        return True

    def simplify(self) -> tuple["Composition", tuple[str, ...]]:
        """Apply exact rewrite rules, left-to-right, until stable."""
        word = list(self.factors)
        used: list[str] = []
        changed = True
        while changed:
            changed = False
            for src, dst, reason in REWRITE_RULES:
                k = len(src)
                if k == 0:
                    continue
                i = 0
                while i + k <= len(word):
                    if tuple(word[i : i + k]) == src:
                        word[i : i + k] = list(dst)
                        used.append(reason)
                        changed = True
                        i = max(0, i - k)
                    else:
                        i += 1
        return Composition(tuple(word)), tuple(used)


def parse_composition(text: str) -> Composition:
    parts = tuple(p for p in text.replace("∘", " ").split() if p and p != "id")
    for p in parts:
        get_operator(p)
    return Composition(parts)


class CommutationClass(str):
    EXACT = "exact_commutation"
    SUBSET = "commutation_on_natural_subset"
    ANTI = "anti_commutation"
    CONJUGACY = "conjugacy"
    BOUNDED_DEFECT = "bounded_defect"
    UNBOUNDED_DEFECT = "unbounded_defect"
    NONE = "no_simple_relationship"


@dataclass(frozen=True)
class InteractionRecord:
    left: str
    right: str
    classification: str
    identity: str
    proof_status: str
    subset: str | None
    defect_formula: str | None
    sample_defect: int | None
    notes: str


def _max_abs_defect(a: str, b: str, limit: int) -> int:
    op_a = get_operator(a)
    op_b = get_operator(b)
    best = 0
    for n in range(-limit, limit + 1):
        if not (op_b.in_domain(n) and op_a.in_domain(n)):
            continue
        try:
            bn = op_b.apply(n)
            an = op_a.apply(n)
        except OperatorDomainError:
            continue
        if not (op_a.in_domain(bn) and op_b.in_domain(an)):
            continue
        try:
            left = op_a.apply(bn)
            right = op_b.apply(an)
        except OperatorDomainError:
            continue
        best = max(best, abs(left - right))
    return best


def classify_pair(a: str, b: str, *, limit: int = 400) -> InteractionRecord:
    """Exact identities first; computational defect only as a witness."""
    key = (a, b)
    known: dict[tuple[str, str], InteractionRecord] = {
        ("N", "N"): InteractionRecord(
            "N", "N", CommutationClass.EXACT, "N∘N = id", "EXACT — HUMAN PROOF", None, "0", 0,
            "Involution.",
        ),
        ("S", "N"): InteractionRecord(
            "S", "N", CommutationClass.EXACT, "S∘N = N∘S = -3n", "EXACT — HUMAN PROOF", None, "0", 0,
            "Both are Z-linear.",
        ),
        ("N", "S"): InteractionRecord(
            "N", "S", CommutationClass.EXACT, "N∘S = S∘N", "EXACT — HUMAN PROOF", None, "0", 0,
            "Both are Z-linear.",
        ),
        ("D", "N"): InteractionRecord(
            "D", "N", CommutationClass.EXACT, "D∘N = N∘D", "EXACT — HUMAN PROOF", None, "0", 0,
            "a0(-n) = -a0(n), so the quotient commutes with sign.",
        ),
        ("N", "D"): InteractionRecord(
            "N", "D", CommutationClass.EXACT, "N∘D = D∘N", "EXACT — HUMAN PROOF", None, "0", 0,
            "Digitwise negation commutes with dropping the LSD.",
        ),
        ("D", "S"): InteractionRecord(
            "D", "S", CommutationClass.CONJUGACY, "D∘S = id, S∘D(n) = n - a0(n)",
            "EXACT — HUMAN PROOF", None, "a0(n) in {-1,0,1}", 1,
            "S is a section of D. Defect of the other order is bounded.",
        ),
        ("S", "D"): InteractionRecord(
            "S", "D", CommutationClass.BOUNDED_DEFECT, "S∘D(n) - D∘S(n) = -a0(n)",
            "EXACT — HUMAN PROOF", "3Z for equality with id after D∘S", "a0(n)", 1,
            "D∘S = id always. S∘D = id iff 3 divides n.",
        ),
        ("W", "N"): InteractionRecord(
            "W", "N", CommutationClass.EXACT, "W∘N = N∘W", "EXACT — HUMAN PROOF", None, "0", 0,
            "Lean: warpWord_mapNeg.",
        ),
        ("N", "W"): InteractionRecord(
            "N", "W", CommutationClass.EXACT, "N∘W = W∘N", "EXACT — HUMAN PROOF", None, "0", 0,
            "Lean: warpWord_mapNeg.",
        ),
        ("W", "S"): InteractionRecord(
            "W", "S", CommutationClass.UNBOUNDED_DEFECT, "W∘S = W, S∘W(n) = 3 W(n)",
            "EXACT — HUMAN PROOF", None, "-2 W(n)", None,
            "Appending a trailing 0 is stripped by reverse+canonicalize. REFUTED: W(3n)=3W(n).",
        ),
        ("S", "W"): InteractionRecord(
            "S", "W", CommutationClass.UNBOUNDED_DEFECT, "S∘W(n) - W∘S(n) = 2 W(n)",
            "EXACT — HUMAN PROOF", None, "2 W(n)", None,
            "Defect is unbounded because W is unbounded.",
        ),
        ("S", "M2"): InteractionRecord(
            "S", "M2", CommutationClass.EXACT, "S∘M2 = M2∘S = 6n", "EXACT — HUMAN PROOF", None, "0", 0,
            "Multiplication operators commute.",
        ),
        ("M2", "S"): InteractionRecord(
            "M2", "S", CommutationClass.EXACT, "M2∘S = S∘M2", "EXACT — HUMAN PROOF", None, "0", 0,
            "Multiplication operators commute.",
        ),
        ("M2", "N"): InteractionRecord(
            "M2", "N", CommutationClass.EXACT, "M2∘N = N∘M2", "EXACT — HUMAN PROOF", None, "0", 0,
            "Z-linear.",
        ),
        ("N", "M2"): InteractionRecord(
            "N", "M2", CommutationClass.EXACT, "N∘M2 = M2∘N", "EXACT — HUMAN PROOF", None, "0", 0,
            "Z-linear.",
        ),
        ("Wz", "S"): InteractionRecord(
            "Wz", "S", CommutationClass.EXACT, "Wz∘S = S∘Wz", "EXACT — HUMAN PROOF", None, "0", 0,
            "Wz(3n)=3 Wz(n) because trailing zeros are kept.",
        ),
        ("S", "Wz"): InteractionRecord(
            "S", "Wz", CommutationClass.EXACT, "S∘Wz = Wz∘S", "EXACT — HUMAN PROOF", None, "0", 0,
            "Companion of Wz∘S = S∘Wz.",
        ),
        ("W", "Wz"): InteractionRecord(
            "W", "Wz", CommutationClass.SUBSET, "W = Wz on {n : 3 does not divide n} ∪ {0}",
            "EXACT — HUMAN PROOF", "3-free integers", None, 0,
            "Wz(n)=W(n) 3^{v3(n)}.",
        ),
        ("Wz", "W"): InteractionRecord(
            "Wz", "W", CommutationClass.SUBSET, "same as W vs Wz",
            "EXACT — HUMAN PROOF", "3-free integers", None, 0,
            "On 3Z they differ.",
        ),
        ("W", "Wt"): InteractionRecord(
            "W", "Wt", CommutationClass.UNBOUNDED_DEFECT,
            "no exact commutation on Z",
            "COMPUTATIONALLY VERIFIED", None, None, None,
            "Equal on palindromes of length <= 2; defect grows with length.",
        ),
        ("Wt", "W"): InteractionRecord(
            "Wt", "W", CommutationClass.UNBOUNDED_DEFECT,
            "no exact commutation on Z",
            "COMPUTATIONALLY VERIFIED", None, None, None,
            "Symmetric entry.",
        ),
        ("D", "W"): InteractionRecord(
            "D", "W", CommutationClass.UNBOUNDED_DEFECT,
            "D∘W(n) = W_tailish of prefix; not W∘D",
            "EXACT — HUMAN PROOF", None, None, None,
            "D∘W drops the MSD of n (LSD of W(n)). W∘D drops the LSD then reverses. Equal iff length <= 1.",
        ),
        ("W", "D"): InteractionRecord(
            "W", "D", CommutationClass.UNBOUNDED_DEFECT,
            "W∘D reverses the suffix after a0",
            "EXACT — HUMAN PROOF", None, None, None,
            "Companion of D∘W.",
        ),
        ("D", "M2"): InteractionRecord(
            "D", "M2", CommutationClass.BOUNDED_DEFECT,
            "no exact commutation; defect depends on LSD carry of doubling",
            "COMPUTATIONALLY VERIFIED", None, None, None,
            "Doubling can emit a new LSD, so D∘M2 is not M2∘D.",
        ),
        ("M2", "D"): InteractionRecord(
            "M2", "D", CommutationClass.BOUNDED_DEFECT,
            "companion of D∘M2",
            "COMPUTATIONALLY VERIFIED", None, None, None,
            "See D∘M2.",
        ),
        ("W", "M2"): InteractionRecord(
            "W", "M2", CommutationClass.UNBOUNDED_DEFECT,
            "W(2n) is not 2 W(n) in general",
            "COMPUTATIONALLY VERIFIED", None, None, None,
            "Reverse does not commute with the doubling carry.",
        ),
        ("M2", "W"): InteractionRecord(
            "M2", "W", CommutationClass.UNBOUNDED_DEFECT,
            "companion of W∘M2",
            "COMPUTATIONALLY VERIFIED", None, None, None,
            "See W∘M2.",
        ),
        ("W", "H2"): InteractionRecord(
            "W", "H2", CommutationClass.UNBOUNDED_DEFECT,
            "partial: H2 only on evens; W does not preserve evenness",
            "COMPUTATIONALLY VERIFIED", "even n with W(n) even", None, None,
            "Domain of H2∘W is a proper subset of 2Z.",
        ),
        ("H2", "W"): InteractionRecord(
            "H2", "W", CommutationClass.UNBOUNDED_DEFECT,
            "partial companion",
            "COMPUTATIONALLY VERIFIED", "even n with W(n) even", None, None,
            "See W∘H2.",
        ),
        ("Wz", "Wt"): InteractionRecord(
            "Wz", "Wt", CommutationClass.UNBOUNDED_DEFECT,
            "two different involutive reversals",
            "COMPUTATIONALLY VERIFIED", None, None, None,
            "Agree on 3-free palindromic length-1 blocks only in trivial cases.",
        ),
        ("Wt", "Wz"): InteractionRecord(
            "Wt", "Wz", CommutationClass.UNBOUNDED_DEFECT,
            "companion",
            "COMPUTATIONALLY VERIFIED", None, None, None,
            "See Wz∘Wt.",
        ),
        ("D", "Wz"): InteractionRecord(
            "D", "Wz", CommutationClass.UNBOUNDED_DEFECT,
            "Wz preserves v3, D decreases length by 1",
            "COMPUTATIONALLY VERIFIED", None, None, None,
            "On 3-free integers Wz=W, reducing to D vs W.",
        ),
        ("Wz", "D"): InteractionRecord(
            "Wz", "D", CommutationClass.UNBOUNDED_DEFECT,
            "companion of D∘Wz",
            "COMPUTATIONALLY VERIFIED", None, None, None,
            "See D∘Wz.",
        ),
        ("H2", "M2"): InteractionRecord(
            "H2", "M2", CommutationClass.EXACT, "H2∘M2 = id", "EXACT — HUMAN PROOF", None, "0", 0,
            "On all of Z, because M2 lands in 2Z.",
        ),
        ("M2", "H2"): InteractionRecord(
            "M2", "H2", CommutationClass.EXACT, "M2∘H2 = id on 2Z", "EXACT — HUMAN PROOF", "2Z", "0", 0,
            "Partial identity.",
        ),
        ("K3", "W"): InteractionRecord(
            "K3", "W", CommutationClass.EXACT, "K3∘W = W∘K3 = W", "EXACT — HUMAN PROOF", None, "0", 0,
            "W(n) is 3-free for every n.",
        ),
        ("W", "K3"): InteractionRecord(
            "W", "K3", CommutationClass.EXACT, "W∘K3 = K3∘W = W", "EXACT — HUMAN PROOF", None, "0", 0,
            "Companion.",
        ),
        ("K3", "N"): InteractionRecord(
            "K3", "N", CommutationClass.EXACT, "K3∘N = N∘K3", "EXACT — HUMAN PROOF", None, "0", 0,
            "v3(-n)=v3(n).",
        ),
        ("N", "K3"): InteractionRecord(
            "N", "K3", CommutationClass.EXACT, "N∘K3 = K3∘N", "EXACT — HUMAN PROOF", None, "0", 0,
            "Companion.",
        ),
        ("K3", "S"): InteractionRecord(
            "K3", "S", CommutationClass.EXACT, "K3∘S = K3", "EXACT — HUMAN PROOF", None, None, 0,
            "S multiplies by 3, which K3 erases.",
        ),
        ("S", "K3"): InteractionRecord(
            "S", "K3", CommutationClass.UNBOUNDED_DEFECT, "S∘K3(n) = 3 n / 3^{v3(n)}",
            "EXACT — HUMAN PROOF", None, None, None,
            "Equals K3∘S = K3 only at 0.",
        ),
    }
    if key in known:
        rec = known[key]
        if rec.sample_defect is None and rec.classification in (
            CommutationClass.UNBOUNDED_DEFECT,
            CommutationClass.BOUNDED_DEFECT,
        ):
            sample = _max_abs_defect(a, b, min(limit, 80))
            return InteractionRecord(
                rec.left, rec.right, rec.classification, rec.identity,
                rec.proof_status, rec.subset, rec.defect_formula, sample, rec.notes,
            )
        return rec

    defect = _max_abs_defect(a, b, min(limit, 80))
    if defect == 0:
        classification = CommutationClass.EXACT
        status = "COMPUTATIONALLY VERIFIED"
        identity = f"{a}∘{b} = {b}∘{a} on [-{min(limit, 80)}, {min(limit, 80)}] ∩ domains"
    else:
        classification = CommutationClass.UNBOUNDED_DEFECT
        status = "COMPUTATIONALLY VERIFIED"
        identity = f"{a}∘{b} ≠ {b}∘{a}"
    return InteractionRecord(
        a, b, classification, identity, status, None, None, defect,
        "Unlisted pair; classification is only as strong as the scan.",
    )


def interaction_table(
    symbols: tuple[str, ...] | None = None, *, limit: int = 400
) -> list[InteractionRecord]:
    if symbols is None:
        symbols = ("S", "N", "D", "W", "Wz", "Wt", "M2", "H2")
    rows: list[InteractionRecord] = []
    for a in symbols:
        for b in symbols:
            if a == b and a in ("N", "Wz", "Wt"):
                rows.append(classify_pair(a, b, limit=limit))
            elif a <= b or True:
                rows.append(classify_pair(a, b, limit=limit))
    return rows


@dataclass(frozen=True)
class CompositionCensus:
    depth: int
    enumerated: int
    simplified_classes: int
    identities: tuple[tuple[str, str], ...]
    involutions: tuple[str, ...]
    projections: tuple[str, ...]
    notes: str


def census_compositions(
    generators: tuple[str, ...] | None = None,
    *,
    max_depth: int = 3,
    sample_limit: int = 40,
) -> CompositionCensus:
    """Pairwise and length-3 compositions. Depth 6 is not brute-forced."""
    if generators is None:
        generators = ALGEBRA_GENERATORS
    if max_depth > 4:
        raise ValueError("max_depth > 4 is refused: expand only when structure appears")
    words: list[Composition] = [Composition(())]
    for depth in range(1, max_depth + 1):
        for factors in product(generators, repeat=depth):
            words.append(Composition(factors))
    simplified: dict[tuple[str, ...], list[Composition]] = {}
    for w in words:
        simp, _ = w.simplify()
        simplified.setdefault(simp.factors, []).append(w)
    identities: list[tuple[str, str]] = []
    involutions: list[str] = []
    projections: list[str] = []
    sample = range(-sample_limit, sample_limit + 1)
    for factors, group in simplified.items():
        if not factors:
            continue
        c = Composition(factors)
        acts_id = True
        acts_involution = True
        acts_projection = True
        for n in sample:
            if not c.in_domain(n):
                continue
            try:
                y = c.apply(n)
            except OperatorDomainError:
                continue
            if y != n:
                acts_id = False
            if c.in_domain(y):
                try:
                    z = c.apply(y)
                except OperatorDomainError:
                    acts_involution = False
                    acts_projection = False
                else:
                    if z != n:
                        acts_involution = False
                    if z != y:
                        acts_projection = False
            else:
                acts_involution = False
                acts_projection = False
            if not acts_id and not acts_involution and not acts_projection:
                break
        label = str(c)
        if acts_id:
            identities.append((label, "id"))
        elif acts_involution and not acts_projection:
            involutions.append(label)
        elif acts_projection:
            projections.append(label)
    return CompositionCensus(
        depth=max_depth,
        enumerated=len(words),
        simplified_classes=len(simplified),
        identities=tuple(identities[:80]),
        involutions=tuple(involutions[:80]),
        projections=tuple(projections[:80]),
        notes=(
            "Rewrite rules are exact. Identity/involution/projection flags "
            f"are only scanned on [-{sample_limit}, {sample_limit}] ∩ domains."
        ),
    )


def word_hamming(a: int, b: int) -> int:
    """Hamming distance of LSD-padded canonical words."""
    da = list(encode(a).digits_lsd())
    db = list(encode(b).digits_lsd())
    n = max(len(da), len(db))
    da.extend([0] * (n - len(da)))
    db.extend([0] * (n - len(db)))
    return sum(x != y for x, y in zip(da, db))
