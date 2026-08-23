"""View-models for the Residual Explorer. No Streamlit import here.

Every numerical field is computed by ``bt.calculus``. This module only
assembles display records, lazy trees, and SVG layout.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from itertools import product

from bt.calculus.cubic import F_k, cubic_residual_formula, image_profile, raw_count_x3
from bt.calculus.myhill_nerode import distinguish_pair, myhill_nerode_count, raw_count
from bt.calculus.poly_congruence import (
    first_distinction_horizon,
    function_equiv,
    newton_coeffs,
    pad_phi,
    phi_k,
)
from bt.calculus.quadratic import pack_word, quadratic_residual_formula
from bt.calculus.residual import TRITS, residual_along
from bt.calculus.section import IntPoly, parse_poly
from bt.metrics import v3
from bt.representation import encode
from research.residuals.cubic_deepest import deepest_fibre_of
from research.residuals.cubic_deficit_two import def2_fibre_of
from research.residuals.cubic_fibres import depth_image, fibre_of
from research.residuals.cubic_layer import inter_fibre_of
from visualization.theorem_ledger import badge_payload

PRESETS: tuple[str, ...] = ("x", "x+1", "2x+1", "x^2", "x^3", "x^4")
DEFAULT_POLY = "x^3"
DEFAULT_K = 10
DEFAULT_DEFICIT = 2
DEFAULT_TREE_LEVELS = 3
MAX_TREE_NODES = 120
MAX_LAYER_PREFIXES = 3**8
CENSUS_AUTO_MAX_K = 11
FULL_FIBRE_MAX_K = 8
MN_CENSUS_MAX_K = 6

TRIT_CHAR = {-1: "-", 0: "0", 1: "+"}
CHAR_TRIT = {"-": -1, "0": 0, "+": 1}
CLASS_COLORS = (
    "#4e79a7",
    "#f28e2b",
    "#e15759",
    "#76b7b2",
    "#59a14f",
    "#edc948",
    "#b07aa1",
    "#ff9da7",
    "#9c755f",
    "#bab0ac",
    "#86bcb6",
    "#d37295",
)


def parse_polynomial(text: str) -> IntPoly:
    return parse_poly(text.strip())


def resolve_polynomial(preset: str, custom: str = "") -> IntPoly:
    source = custom.strip() if custom and custom.strip() else preset
    return parse_polynomial(source)


@lru_cache(maxsize=8)
def _poly(text: str) -> IntPoly:
    return parse_poly(text)


def is_x2(f: IntPoly) -> bool:
    return f.coeffs == _poly("x^2").coeffs


def is_x3(f: IntPoly) -> bool:
    return f.coeffs == _poly("x^3").coeffs


def depth_from_mode(k: int, *, mode: str, m: int | None = None, r: int | None = None) -> int:
    """Return the focused depth. Deficit mode uses ``m = k-1-r``."""
    if mode == "deficit":
        if r is None:
            raise ValueError("deficit mode requires r")
        if r < 0:
            raise ValueError("depth deficit must be nonnegative")
        focused = k - 1 - r
        if focused < 0:
            raise ValueError(f"deficit r={r} exceeds k-1={k - 1}")
        return focused
    if m is None:
        raise ValueError("explicit mode requires m")
    if m < 0 or m >= k:
        raise ValueError(f"depth m must satisfy 0 <= m < k, got m={m}, k={k}")
    return m


def deficit_of(k: int, m: int) -> int:
    return k - 1 - m


def format_word(word: tuple[int, ...]) -> str:
    if not word:
        return "ε"
    return "".join(TRIT_CHAR[a] for a in word)


def parse_word(text: str) -> tuple[int, ...]:
    raw = text.strip()
    if raw in {"", "ε", "e"}:
        return ()
    out: list[int] = []
    for ch in raw:
        if ch not in CHAR_TRIT:
            raise ValueError(f"unknown trit {ch!r}")
        out.append(CHAR_TRIT[ch])
    return tuple(out)


def residual_of(f: IntPoly, word: tuple[int, ...]) -> IntPoly:
    if is_x3(f):
        return cubic_residual_formula(word)
    if is_x2(f):
        return quadratic_residual_formula(word)
    return residual_along(f, word)


def prefix_digits(p: int, m: int) -> tuple[int, ...]:
    """Fixed-width LSD-first digits of a packed prefix of length ``m``."""
    if m < 0:
        raise ValueError("m must be nonnegative")
    if m == 0:
        return ()
    digits = list(encode(p).digits_lsd())
    if digits == [0] and p == 0:
        digits = []
    if len(digits) > m:
        digits = digits[:m]
    while len(digits) < m:
        digits.append(0)
    return tuple(digits)


def prefix_mods(p: int, m: int) -> tuple[tuple[int, int], ...]:
    """``(3^j, p mod 3^j)`` for ``j = 1..m``."""
    return tuple((3**j, p % (3**j)) for j in range(1, m + 1))


@dataclass(frozen=True)
class ResidualState:
    polynomial: str
    m: int
    p: int
    word: tuple[int, ...]
    word_text: str
    exact: str
    source_poly: str


@dataclass(frozen=True)
class NewtonCoord:
    index: int
    exact: int
    mod_value: int
    valuation: int | None
    visible: bool
    bar: str


@dataclass(frozen=True)
class NewtonState:
    coords: tuple[NewtonCoord, ...]
    phi: tuple[int, ...]
    class_key: str


@dataclass(frozen=True)
class VisibilityStory:
    r: int
    m: int
    k: int
    n2_sees: str
    n1_line: str
    n0_line: str
    extra: str
    theorem_id: str
    badge: dict[str, str] | None


@dataclass(frozen=True)
class NodeInspection:
    state: ResidualState
    newton: NewtonState
    visibility: VisibilityStory
    digits: tuple[int, ...]
    mods: tuple[tuple[int, int], ...]
    source_is_x2: bool
    source_is_x3: bool


@dataclass(frozen=True)
class TreeNode:
    id: str
    word: tuple[int, ...]
    depth: int
    packed_p: int
    residual: str
    phi: tuple[int, ...]
    class_id: int
    visible_count: int
    merged_visible: bool
    children_ids: tuple[str, ...]
    parent_id: str | None


@dataclass(frozen=True)
class FibreMember:
    m: int
    p: int
    word_text: str
    residual: str


@dataclass(frozen=True)
class FibreView:
    class_key: str
    class_id: int | None
    size: int
    scope: str
    members: tuple[FibreMember, ...]
    criterion: tuple[str, ...]
    theorem_id: str
    badge: dict[str, str] | None
    truncated: bool


@dataclass(frozen=True)
class CoordVerdict:
    index: int
    left: int
    right: int
    left_mod: int
    right_mod: int
    equal: bool


@dataclass(frozen=True)
class CompareView:
    left: ResidualState
    right: ResidualState
    newton_rows: tuple[CoordVerdict, ...]
    same_class: bool
    first_difference: str | None
    tau: int | None
    same_through: int | None
    shortest: tuple[int, ...] | None
    difference_poly: str
    difference_newton: tuple[int, ...]
    difference_valuations: tuple[int | None, ...]
    explanation: str
    theorem_id: str
    badge: dict[str, str] | None


@dataclass(frozen=True)
class CensusView:
    k: int
    source: str
    raw: int | None
    observable: int | None
    merged: int | None
    computed: bool
    warning: str
    theorem_id: str
    badge: dict[str, str] | None
    caption: str


def valuation_bar(v: int | None, k: int) -> str:
    """Compact 3-adic visibility ruler ``0 … k`` with horizon at ``k``."""
    marks: list[str] = []
    for i in range(k + 1):
        if v is None:
            marks.append("█")
        elif i < v:
            marks.append("|")
        elif i == v:
            marks.append("█")
        else:
            marks.append(".")
    return " ".join(marks)


def _n2_sees_text(r: int) -> str:
    if r <= 0:
        return "N2 sees: nothing about p"
    if r == 1:
        return "N2 sees: p mod 3"
    if r == 2:
        return "N2 sees: p mod 9"
    return f"N2 sees: p mod 3^{r}"


def visibility_story(f: IntPoly, m: int, k: int) -> VisibilityStory:
    r = deficit_of(k, m)
    if is_x3(f):
        extra = ""
        if r > 2:
            extra = (
                "The depth-deficit law is Lean-verified for general r "
                "with r+1 ≤ k; the r=0,1,2 labels are the current research focus."
            )
        return VisibilityStory(
            r=r,
            m=m,
            k=k,
            n2_sees=_n2_sees_text(r),
            n1_line="N1: quadratic / valuation refinement",
            n0_line="N0: cubic quotient refinement",
            extra=extra,
            theorem_id="BTA-x3-vis",
            badge=badge_payload("BTA-x3-vis"),
        )
    if is_x2(f):
        return VisibilityStory(
            r=r,
            m=m,
            k=k,
            n2_sees="quadratic coefficient 2p remains fully visible",
            n1_line="degree ≤ 2 is coefficient congruence modulo 3^k",
            n0_line="distinct residuals stay distinct at every finite horizon",
            extra="The residual tree of x^2 is preserved.",
            theorem_id="BTA-x2-mn",
            badge=badge_payload("BTA-x2-mn"),
        )
    return VisibilityStory(
        r=r,
        m=m,
        k=k,
        n2_sees="observable class is Φ_k, the Newton residues modulo 3^k",
        n1_line="equivalence is function congruence modulo 3^k",
        n0_line="",
        extra="",
        theorem_id="BTA-fn-congr",
        badge=badge_payload("BTA-fn-congr"),
    )


def inspect_node(f: IntPoly, word: tuple[int, ...], k: int) -> NodeInspection:
    poly = residual_of(f, word)
    m = len(word)
    p = pack_word(word)
    newt = newton_coeffs(poly)
    ph = phi_k(poly, k)
    mod = 3**k if k else 1
    coords = []
    for i, exact in enumerate(newt):
        val = v3(exact)
        coords.append(
            NewtonCoord(
                index=i,
                exact=exact,
                mod_value=exact % mod,
                valuation=val,
                visible=(exact % mod) != 0,
                bar=valuation_bar(val, k),
            )
        )
    state = ResidualState(
        polynomial=poly.render(),
        m=m,
        p=p,
        word=word,
        word_text=format_word(word),
        exact=poly.render(),
        source_poly=f.render(),
    )
    return NodeInspection(
        state=state,
        newton=NewtonState(
            coords=tuple(coords),
            phi=ph,
            class_key=_class_key(ph),
        ),
        visibility=visibility_story(f, m, k),
        digits=prefix_digits(p, m),
        mods=prefix_mods(p, m),
        source_is_x2=is_x2(f),
        source_is_x3=is_x3(f),
    )


def _class_key(phi: tuple[int, ...]) -> str:
    return ",".join(str(x) for x in phi)


def _zero_spine(m: int) -> list[tuple[int, ...]]:
    return [tuple([0] * i) for i in range(m + 1)]


def _children(word: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    return tuple(word + (a,) for a in TRITS)


def expand_subtree_words(
    word: tuple[int, ...],
    k: int,
    *,
    cap: int = 80,
) -> tuple[tuple[int, ...], ...]:
    """Ancestors of ``word`` plus a breadth-first subtree, capped."""
    out: list[tuple[int, ...]] = []
    seen: set[tuple[int, ...]] = set()
    for i in range(len(word) + 1):
        prefix = word[:i]
        if prefix not in seen and len(prefix) < k:
            seen.add(prefix)
            out.append(prefix)
    frontier = [word]
    while frontier and len(out) < cap:
        cur = frontier.pop(0)
        if len(cur) >= k - 1:
            continue
        for child in _children(cur):
            if child in seen or len(child) >= k:
                continue
            seen.add(child)
            out.append(child)
            frontier.append(child)
            if len(out) >= cap:
                break
    return tuple(out)


def visible_words(
    k: int,
    *,
    expanded: frozenset[tuple[int, ...]] = frozenset(),
    focus_depth: int | None = None,
    default_levels: int = DEFAULT_TREE_LEVELS,
    max_nodes: int = MAX_TREE_NODES,
) -> tuple[tuple[int, ...], ...]:
    """Lazily chosen prefixes with ``|w| < k``."""
    cap = min(default_levels, max(k - 1, 0))
    wanted: set[tuple[int, ...]] = {()}
    for m in range(1, cap + 1):
        wanted.update(product(TRITS, repeat=m))
    expand = set(expanded)
    if focus_depth is not None:
        focus_depth = max(0, min(focus_depth, k - 1))
        for word in _zero_spine(focus_depth):
            if len(word) < k:
                wanted.add(word)
            if word and len(word) <= k - 1:
                parent = word[:-1]
                expand.add(parent)
            if len(word) < k - 1 or (len(word) < k and word in expand):
                expand.add(word)
        for word in _zero_spine(max(focus_depth - 1, 0)):
            expand.add(word)
    frontier = list(wanted)
    seen = set(wanted)
    for word in list(expand):
        if word not in seen and len(word) < k:
            seen.add(word)
            frontier.append(word)
        if len(word) >= k - 1:
            continue
        for child in _children(word):
            if child not in seen and len(child) < k:
                seen.add(child)
                frontier.append(child)
    ordered = sorted(seen, key=lambda w: (len(w), w))
    if len(ordered) > max_nodes:
        ordered = ordered[:max_nodes]
    return tuple(ordered)


def visible_subtree(
    f: IntPoly,
    k: int,
    *,
    expanded: frozenset[tuple[int, ...]] = frozenset(),
    focus_depth: int | None = None,
    default_levels: int = DEFAULT_TREE_LEVELS,
    max_nodes: int = MAX_TREE_NODES,
) -> tuple[TreeNode, ...]:
    words = visible_words(
        k,
        expanded=expanded,
        focus_depth=focus_depth,
        default_levels=default_levels,
        max_nodes=max_nodes,
    )
    present = set(words)
    records: list[tuple[tuple[int, ...], IntPoly, tuple[int, ...]]] = []
    for word in words:
        poly = residual_of(f, word)
        records.append((word, poly, phi_k(poly, k)))
    classes: dict[tuple[int, ...], int] = {}
    for _word, _poly, ph in sorted(records, key=lambda row: row[2]):
        if ph not in classes:
            classes[ph] = len(classes)
    counts: dict[tuple[int, ...], int] = {}
    for _word, _poly, ph in records:
        counts[ph] = counts.get(ph, 0) + 1
    nodes: list[TreeNode] = []
    for word, poly, ph in records:
        parent = word[:-1] if word else None
        child_ids = tuple(
            format_word(child) for child in _children(word) if child in present
        )
        nodes.append(
            TreeNode(
                id=format_word(word),
                word=word,
                depth=len(word),
                packed_p=pack_word(word),
                residual=poly.render(),
                phi=ph,
                class_id=classes[ph],
                visible_count=counts[ph],
                merged_visible=counts[ph] > 1,
                children_ids=child_ids,
                parent_id=format_word(parent) if parent is not None else None,
            )
        )
    return tuple(nodes)


def filter_nodes(
    nodes: tuple[TreeNode, ...],
    *,
    class_id: int | None = None,
    merged_only: bool = False,
    singleton_only: bool = False,
    depth: int | None = None,
    focus_class: bool = False,
    selected_id: str | None = None,
) -> tuple[TreeNode, ...]:
    selected = next((n for n in nodes if n.id == selected_id), None)
    out = nodes
    if focus_class and selected is not None:
        out = tuple(n for n in out if n.class_id == selected.class_id)
    if class_id is not None:
        out = tuple(n for n in out if n.class_id == class_id)
    if merged_only:
        out = tuple(n for n in out if n.merged_visible)
    if singleton_only:
        out = tuple(n for n in out if not n.merged_visible)
    if depth is not None:
        out = tuple(n for n in out if n.depth == depth)
    return out


def _member_record(f: IntPoly, m: int, p: int) -> FibreMember:
    digits = prefix_digits(p, m)
    word_text = format_word(digits)
    poly = residual_of(f, digits)
    return FibreMember(m=m, p=p, word_text=word_text, residual=poly.render())


def _layer_members(f: IntPoly, m: int, p: int, k: int) -> tuple[list[tuple[int, int]], str, bool]:
    r = deficit_of(k, m)
    if not is_x3(f):
        return ([(m, p)], "singleton", False)
    if 3**m > MAX_LAYER_PREFIXES:
        return ([(m, p)], "too-large", True)
    if r == 0 and m == k - 1:
        return ([(m, q) for q in deepest_fibre_of(p, k)], "deepest-layer", False)
    if r == 1 and m == k - 2:
        return ([(m, q) for q in inter_fibre_of(p, k)], "deficit-1", False)
    if r == 2 and m == k - 3:
        return ([(m, q) for q in def2_fibre_of(p, k)], "deficit-2", False)
    buckets = depth_image(k, m)
    return ([(m, q) for q in buckets[F_k(m, p, k)]], "same-depth", False)


def fibre_view(
    f: IntPoly,
    word: tuple[int, ...],
    k: int,
    *,
    full_cross_depth: bool = False,
    class_id: int | None = None,
) -> FibreView:
    m = len(word)
    p = pack_word(word)
    poly = residual_of(f, word)
    ph = phi_k(poly, k)
    truncated = False
    if full_cross_depth and is_x3(f) and k <= FULL_FIBRE_MAX_K:
        pairs = fibre_of(m, p, k)
        scope = "cross-depth"
    else:
        pairs, scope, truncated = _layer_members(f, m, p, k)
    members = tuple(_member_record(f, mm, pp) for mm, pp in pairs)
    criterion = _fibre_criterion(f, word, k, members)
    theorem = "BTA-x3-n2" if is_x3(f) else "BTA-fn-congr"
    if is_x3(f) and deficit_of(k, m) in {0, 1, 2}:
        theorem = "BTA-x3-vis"
    return FibreView(
        class_key=_class_key(ph),
        class_id=class_id,
        size=len(members),
        scope=scope,
        members=members,
        criterion=criterion,
        theorem_id=theorem,
        badge=badge_payload(theorem),
        truncated=truncated,
    )


def _fibre_criterion(
    f: IntPoly,
    word: tuple[int, ...],
    k: int,
    members: tuple[FibreMember, ...],
) -> tuple[str, ...]:
    if len(members) <= 1:
        if is_x2(f):
            return (
                "singleton: distinct x^2 residuals remain ≡_k-separated",
                "M_k(x^2) = R_k(x^2)",
            )
        return ("singleton at this scope",)
    if not is_x3(f):
        return ("same Φ_k Newton residues",)
    r = deficit_of(k, len(word))
    lines = [
        f"N2: equal  (p agree modulo 3^{max(r, 0)})",
        "N1: equal",
        "N0: equal",
        "Therefore: same Φ_k class",
    ]
    return tuple(lines)


def compare_states(
    f: IntPoly,
    word_a: tuple[int, ...],
    word_b: tuple[int, ...],
    k: int,
) -> CompareView:
    left_poly = residual_of(f, word_a)
    right_poly = residual_of(f, word_b)
    left = ResidualState(
        polynomial=left_poly.render(),
        m=len(word_a),
        p=pack_word(word_a),
        word=word_a,
        word_text=format_word(word_a),
        exact=left_poly.render(),
        source_poly=f.render(),
    )
    right = ResidualState(
        polynomial=right_poly.render(),
        m=len(word_b),
        p=pack_word(word_b),
        word=word_b,
        word_text=format_word(word_b),
        exact=right_poly.render(),
        source_poly=f.render(),
    )
    na = newton_coeffs(left_poly)
    nb = newton_coeffs(right_poly)
    n = max(len(na), len(nb))
    na_p = pad_phi(na, n)
    nb_p = pad_phi(nb, n)
    mod = 3**k if k else 1
    rows = tuple(
        CoordVerdict(
            index=i,
            left=na_p[i],
            right=nb_p[i],
            left_mod=na_p[i] % mod,
            right_mod=nb_p[i] % mod,
            equal=(na_p[i] % mod) == (nb_p[i] % mod),
        )
        for i in range(n)
    )
    same = function_equiv(left_poly, right_poly, k)
    first = None
    for row in reversed(rows):
        if not row.equal:
            first = f"N{row.index}"
            break
    tau = first_distinction_horizon(left_poly, right_poly)
    same_through = None if tau is None else max(tau - 1, 0)
    pair = distinguish_pair(left_poly, right_poly, k)
    shortest = tuple(pair["shortest"]) if pair.get("shortest") else None
    h = left_poly.sub(right_poly)
    h_newt = newton_coeffs(h)
    explanation = explain_comparison(same, rows, k, tau)
    theorem = "BTA-fn-congr"
    if is_x3(f) and {word_a, word_b} == {(-1,), (1,)}:
        theorem = "BTA-x3-merge"
    return CompareView(
        left=left,
        right=right,
        newton_rows=rows,
        same_class=same,
        first_difference=None if same else first,
        tau=tau,
        same_through=same_through,
        shortest=shortest,
        difference_poly=h.render(),
        difference_newton=h_newt,
        difference_valuations=tuple(v3(c) for c in h_newt),
        explanation=explanation,
        theorem_id=theorem,
        badge=badge_payload(theorem),
    )


def explain_comparison(
    same: bool,
    rows: tuple[CoordVerdict, ...],
    k: int,
    tau: int | None,
) -> str:
    if same:
        return (
            f"Their Newton coordinates agree modulo 3^{k}. "
            "The machine cannot distinguish them using only k output trits."
        )
    first = next((row for row in reversed(rows) if not row.equal), None)
    if first is None:
        return "The states are distinct at this horizon."
    agrees = [f"N{row.index}" for row in reversed(rows) if row.equal]
    head = ""
    if agrees:
        head = f"They have the same {', '.join(agrees)} value, but "
    split = f"different N{first.index} values."
    extra = ""
    if tau is not None:
        extra = f" First distinguishing horizon τ = {tau}."
    return (
        f"{head}{split} At this precision, N{first.index} can still see this "
        f"difference.{extra}"
    )


def demo_delayed_pair() -> tuple[IntPoly, tuple[int, ...], tuple[int, ...]]:
    """Pinned first x^3 merge: residuals along (−1) and (+1)."""
    return parse_poly("x^3"), (-1,), (1,)


@lru_cache(maxsize=16)
def _x3_image_profile(k: int) -> dict[str, object]:
    return image_profile(k)


def census_view(
    f: IntPoly,
    k: int,
    *,
    allow_expensive: bool = False,
) -> CensusView:
    if is_x2(f):
        raw = (3**k - 1) // 2 if k else 1
        return CensusView(
            k=k,
            source="x^2",
            raw=raw,
            observable=raw,
            merged=0,
            computed=True,
            warning="",
            theorem_id="BTA-x2-mn",
            badge=badge_payload("BTA-x2-mn"),
            caption="x^2: residual tree preserved",
        )
    if is_x3(f):
        if k > CENSUS_AUTO_MAX_K and not allow_expensive:
            return CensusView(
                k=k,
                source="x^3",
                raw=raw_count_x3(k),
                observable=None,
                merged=None,
                computed=False,
                warning=(
                    f"Full Newton-image census at k={k} enumerates "
                    f"{raw_count_x3(k)} residuals. Enable expensive census to run it."
                ),
                theorem_id="BTA-x3-Fk",
                badge=badge_payload("BTA-x3-Fk"),
                caption="x^3: residual tree compressed by finite Newton-function equivalence",
            )
        rec = _x3_image_profile(k)
        return CensusView(
            k=k,
            source="x^3",
            raw=int(rec["R"]),
            observable=int(rec["M"]),
            merged=int(rec["collisions"]),
            computed=True,
            warning="",
            theorem_id="BTA-x3-Fk",
            badge=badge_payload("BTA-x3-Fk"),
            caption="x^3: residual tree compressed by finite Newton-function equivalence",
        )
    if k > MN_CENSUS_MAX_K and not allow_expensive:
        return CensusView(
            k=k,
            source=f.render(),
            raw=None,
            observable=None,
            merged=None,
            computed=False,
            warning=f"Myhill–Nerode census for general polynomials is limited to k≤{MN_CENSUS_MAX_K}.",
            theorem_id="BTA-fn-congr",
            badge=badge_payload("BTA-fn-congr"),
            caption="general polynomial: census not computed",
        )
    raw = raw_count(f, k)
    observable = myhill_nerode_count(f, k)
    return CensusView(
        k=k,
        source=f.render(),
        raw=raw,
        observable=observable,
        merged=raw - observable,
        computed=True,
        warning="",
        theorem_id="BTA-fn-congr",
        badge=badge_payload("BTA-fn-congr"),
        caption=f"{f.render()}: finite-horizon Myhill–Nerode count",
    )


def dual_census(k: int, *, allow_expensive: bool = False) -> tuple[CensusView, CensusView]:
    return (
        census_view(_poly("x^2"), k, allow_expensive=allow_expensive),
        census_view(_poly("x^3"), k, allow_expensive=allow_expensive),
    )


def _layout_positions(nodes: tuple[TreeNode, ...]) -> dict[str, tuple[float, float]]:
    by_id = {n.id: n for n in nodes}
    children: dict[str, list[str]] = {n.id: list(n.children_ids) for n in nodes}
    roots = [n.id for n in nodes if n.parent_id not in by_id]
    if not roots:
        roots = [nodes[0].id] if nodes else []

    widths: dict[str, float] = {}

    def width_of(nid: str) -> float:
        if nid in widths:
            return widths[nid]
        kids = [c for c in children.get(nid, []) if c in by_id]
        widths[nid] = 1.0 if not kids else sum(width_of(c) for c in kids)
        return widths[nid]

    for nid in roots:
        width_of(nid)

    pos: dict[str, tuple[float, float]] = {}

    def place(nid: str, x0: float) -> None:
        node = by_id[nid]
        kids = [c for c in children.get(nid, []) if c in by_id]
        w = width_of(nid)
        cx = x0 + w / 2.0
        pos[nid] = (cx, float(node.depth))
        cursor = x0
        for child in kids:
            place(child, cursor)
            cursor += width_of(child)

    cursor = 0.0
    for nid in roots:
        place(nid, cursor)
        cursor += width_of(nid)
    return pos


def tree_svg(
    nodes: tuple[TreeNode, ...],
    *,
    selected_id: str | None = None,
    width: int = 640,
    row_h: int = 56,
) -> str:
    """SVG of the visible ternary subtree. Colour encodes class; shape encodes merge."""
    if not nodes:
        return '<svg xmlns="http://www.w3.org/2000/svg" width="640" height="80"></svg>'
    pos = _layout_positions(nodes)
    by_id = {n.id: n for n in nodes}
    xs = [xy[0] for xy in pos.values()]
    min_x, max_x = min(xs), max(xs)
    span = max(max_x - min_x, 1.0)
    pad_x, pad_y = 36, 28
    max_depth = max(n.depth for n in nodes)
    height = pad_y * 2 + row_h * (max_depth + 1)

    def px(nid: str) -> tuple[float, float]:
        x, y = pos[nid]
        sx = pad_x + (x - min_x) / span * (width - 2 * pad_x)
        sy = pad_y + y * row_h
        return sx, sy

    parts = [
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'role="img" aria-label="Residual prefix tree">'
        )
    ]
    for node in nodes:
        if node.parent_id and node.parent_id in by_id:
            x1, y1 = px(node.parent_id)
            x2, y2 = px(node.id)
            trit = node.word[-1] if node.word else 0
            parts.append(
                f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                f'stroke="#8a8a8a" stroke-width="1.2"/>'
            )
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            parts.append(
                f'<text x="{mx:.1f}" y="{my - 4:.1f}" font-size="10" '
                f'font-family="ui-monospace, monospace" fill="#666" '
                f'text-anchor="middle">{trit:+d}</text>'
            )
    for node in nodes:
        x, y = px(node.id)
        color = CLASS_COLORS[node.class_id % len(CLASS_COLORS)]
        selected = node.id == selected_id
        stroke = "#f5d76e" if selected else "#222"
        sw = 3.5 if selected else 1.2
        r = 12
        if node.merged_visible:
            parts.append(
                f'<rect x="{x - r:.1f}" y="{y - r:.1f}" width="{2 * r}" height="{2 * r}" '
                f'fill="{color}" stroke="{stroke}" stroke-width="{sw}" '
                f'rx="2"><title>{_node_title(node)}</title></rect>'
            )
        else:
            parts.append(
                f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{color}" '
                f'stroke="{stroke}" stroke-width="{sw}">'
                f"<title>{_node_title(node)}</title></circle>"
            )
        parts.append(
            f'<text x="{x:.1f}" y="{y + 22:.1f}" font-size="10" '
            f'font-family="ui-monospace, monospace" text-anchor="middle" '
            f'fill="#333">{node.id}</text>'
        )
        parts.append(
            f'<text x="{x:.1f}" y="{y + 4:.1f}" font-size="9" '
            f'font-family="ui-monospace, monospace" text-anchor="middle" '
            f'fill="#111">{node.class_id}</text>'
        )
    parts.append("</svg>")
    return "".join(parts)


def _node_title(node: TreeNode) -> str:
    kind = "merged" if node.merged_visible else "singleton"
    return (
        f"w={node.id} m={node.depth} p={node.packed_p} "
        f"class={node.class_id} ({kind}, visible size {node.visible_count})"
    )


@dataclass(frozen=True)
class QuotientInvariantView:
    t: int
    K: int
    W: int
    r: int
    on_locus: bool
    u: int | None
    a: int | None
    b: int | None
    B_t: int | None
    Q: int | None
    expansion: int | None
    psi_lines: tuple[str, ...]
    note: str


@dataclass(frozen=True)
class QuotientCompareView:
    same_psi4: bool
    same_Q: bool
    missing: tuple[str, ...]
    block: str


def quotient_invariant_view(p: int, k: int, r: int) -> QuotientInvariantView:
    """Two-scale Q card for a packed prefix, when the node is on ``3^r Z``."""
    from research.residuals.mismatched_cubic import q_mod, q_params
    from research.residuals.mismatched_invariant import B_t, q_expansion, split_two_scale

    if k < 4 * r + 1:
        return QuotientInvariantView(
            t=-1, K=k, W=-1, r=r, on_locus=False,
            u=None, a=None, b=None, B_t=None, Q=None, expansion=None,
            psi_lines=(),
            note="unexhausted N0: scaled cube, not a Q-instance",
        )
    t, K, W = q_params(k, r)
    if r and p % (3**r) != 0:
        return QuotientInvariantView(
            t=t, K=K, W=W, r=r, on_locus=False,
            u=None, a=None, b=None, B_t=None, Q=None, expansion=None,
            psi_lines=(),
            note="N1 has already separated this prefix: 3^r does not divide p",
        )
    u = p // (3**r if r else 1)
    a, b = split_two_scale(t, u)
    return QuotientInvariantView(
        t=t,
        K=K,
        W=W,
        r=r,
        on_locus=True,
        u=u,
        a=a,
        b=b,
        B_t=B_t(t, u),
        Q=q_mod(t, K, u),
        expansion=q_expansion(t, a, b),
        psi_lines=(
            f"v3(u) = {v3(u)}",
            f"u mod 3^{t} = {u % (3**t if t else 1)}",
            f"B_t(u) = {B_t(t, u)}",
        ),
        note="Ψ4 is (v3, u mod 3^t, B_t); it does not classify Q-fibres",
    )


def quotient_compare_view(u: int, v: int, t: int, K: int, W: int) -> QuotientCompareView:
    from research.residuals.mismatched_invariant import invariant_compare

    rec = invariant_compare(t, K, W, u, v)
    same_psi4 = bool(rec["psi"]["psi4"]["same"])
    lines = [
        f"u = {rec['a_u']} + 3^{t}*{rec['b_u']}",
        f"v = {rec['a_v']} + 3^{t}*{rec['b_v']}",
        f"Q(u) = {rec['Q_u']}   Q(v) = {rec['Q_v']}",
        f"same Q = {rec['same_Q']}",
        f"same Ψ4 = {same_psi4}",
        *rec["missing"],
    ]
    return QuotientCompareView(
        same_psi4=same_psi4,
        same_Q=bool(rec["same_Q"]),
        missing=tuple(rec["missing"]),
        block="\n".join(lines),
    )


LIFT_KIND_COLORS: dict[str, str] = {
    "unique": "#59a14f",
    "splitting": "#4e79a7",
    "singular-persistent": "#f28e2b",
    "terminal": "#bab0ac",
}
LIFT_KIND_LABEL: dict[str, str] = {
    "unique": "unique lift (3 does not divide f')",
    "splitting": "several children below the root",
    "singular-persistent": "singular, three lifts",
    "terminal": "no lift",
}
MAX_LIFT_NODES = 160


@dataclass(frozen=True)
class LiftTreeNode:
    id: str
    word: tuple[int, ...]
    depth: int
    residue: int
    digits: str
    residual: str
    f_value: int
    f_prime: int
    v3_f: int | None
    v3_f_prime: int | None
    newton: tuple[int, ...]
    phi: tuple[int, ...]
    kind: str
    lift_trits: tuple[int, ...]
    children_ids: tuple[str, ...]
    parent_id: str | None
    shape_widths: tuple[int, ...]


@dataclass(frozen=True)
class LiftingView:
    poly: str
    k: int
    r: int
    nodes: tuple[LiftTreeNode, ...]
    level_counts: tuple[int, ...]
    kind_census: tuple[tuple[str, int], ...]
    brute_force_agrees: bool
    distinct_subtrees: tuple[tuple[int, int], ...]
    truncated: bool
    notes: tuple[str, ...]


def _lift_node_id(word: tuple[int, ...]) -> str:
    return format_word(word) if word else "e"


def lifting_view(f: IntPoly, k: int, r: int = 2) -> LiftingView:
    """Lifting tree of ``f(x) = 0 mod 3^k`` with per-node residual state."""
    from bt.calculus.lifting import (
        brute_force_roots,
        depth_r_shape,
        level_nodes,
        lift_tree,
    )
    from bt.calculus.lifting import shape_widths as _widths

    k = max(int(k), 0)
    r = max(int(r), 1)
    raw = lift_tree(f, k)
    truncated = len(raw) > MAX_LIFT_NODES
    kept = raw[:MAX_LIFT_NODES]
    kept_words = {node.word for node in kept}
    nodes = tuple(
        LiftTreeNode(
            id=_lift_node_id(node.word),
            word=node.word,
            depth=node.level,
            residue=node.residue,
            digits=node.digits or "e",
            residual=node.residual.render(),
            f_value=node.f_value,
            f_prime=node.f_prime,
            v3_f=node.v3_f,
            v3_f_prime=node.v3_f_prime,
            newton=node.newton,
            phi=phi_k(node.residual, r),
            kind=node.kind,
            lift_trits=node.children,
            children_ids=tuple(
                _lift_node_id(node.word + (a,))
                for a in node.children
                if node.word + (a,) in kept_words
            ),
            parent_id=None if not node.word else _lift_node_id(node.word[:-1]),
            shape_widths=_widths(node.residual, r),
        )
        for node in kept
    )
    census: dict[str, int] = {}
    for node in nodes:
        census[node.kind] = census.get(node.kind, 0) + 1
    counts = tuple(len(level_nodes(raw, level)) for level in range(k + 1))
    top = tuple(sorted(node.residue for node in level_nodes(raw, k)))
    distinct = tuple(
        (
            level,
            len({depth_r_shape(node.residual, r) for node in level_nodes(raw, level)}),
        )
        for level in range(k + 1)
        if level_nodes(raw, level)
    )
    notes = (
        "A node is a solution of f(x) = 0 mod 3^k exactly when every output "
        "trit of the residual machine along its word vanishes, so this tree "
        "is the zero-output subtree.",
        "The residual state is the scaled Taylor jet: its linear coefficient "
        "is f'(n) and, on the tree, its constant coefficient is f(n)/3^k.",
        f"Phi_{r} determines the depth-{r} subtree; the pair of valuations "
        "does not, as x^2 + 9 and x^2 - 9 show at the level-1 node 0.",
        "Lifting trees and root counting modulo 3^k are classical. No "
        "counting or complexity improvement is claimed here.",
    )
    return LiftingView(
        poly=f.render(),
        k=k,
        r=r,
        nodes=nodes,
        level_counts=counts,
        kind_census=tuple(sorted(census.items())),
        brute_force_agrees=top == brute_force_roots(f, k),
        distinct_subtrees=distinct,
        truncated=truncated,
        notes=notes,
    )


def _lift_node_title(node: LiftTreeNode) -> str:
    v_f = "inf" if node.v3_f is None else str(node.v3_f)
    v_fp = "inf" if node.v3_f_prime is None else str(node.v3_f_prime)
    lifts = "".join(f"{a:+d}" for a in node.lift_trits) or "none"
    return (
        f"w={node.digits} x={node.residue} f(x)={node.f_value} "
        f"v3(f)={v_f} v3(f')={v_fp} residual={node.residual} "
        f"{LIFT_KIND_LABEL[node.kind]} lifts={lifts}"
    )


def lift_tree_svg(
    nodes: tuple[LiftTreeNode, ...],
    *,
    selected_id: str | None = None,
    width: int = 640,
    row_h: int = 56,
) -> str:
    """SVG of a lifting tree. Colour encodes lift type, not residual class."""
    if not nodes:
        return (
            '<svg xmlns="http://www.w3.org/2000/svg" width="640" height="80">'
            '<text x="16" y="44" font-size="12" font-family="ui-monospace, monospace" '
            'fill="#666">no solutions at this level</text></svg>'
        )
    by_id = {n.id: n for n in nodes}
    children: dict[str, list[str]] = {n.id: list(n.children_ids) for n in nodes}
    widths: dict[str, float] = {}

    def width_of(nid: str) -> float:
        if nid in widths:
            return widths[nid]
        kids = [c for c in children.get(nid, []) if c in by_id]
        widths[nid] = 1.0 if not kids else sum(width_of(c) for c in kids)
        return widths[nid]

    pos: dict[str, tuple[float, float]] = {}

    def place(nid: str, x0: float) -> None:
        node = by_id[nid]
        cursor = x0
        pos[nid] = (x0 + width_of(nid) / 2.0, float(node.depth))
        for child in [c for c in children.get(nid, []) if c in by_id]:
            place(child, cursor)
            cursor += width_of(child)

    roots = [n.id for n in nodes if n.parent_id not in by_id]
    cursor = 0.0
    for nid in roots or [nodes[0].id]:
        width_of(nid)
        place(nid, cursor)
        cursor += width_of(nid)

    xs = [xy[0] for xy in pos.values()]
    min_x, max_x = min(xs), max(xs)
    span = max(max_x - min_x, 1.0)
    pad_x, pad_y = 36, 28
    max_depth = max(n.depth for n in nodes)
    height = pad_y * 2 + row_h * (max_depth + 1)

    def px(nid: str) -> tuple[float, float]:
        x, y = pos[nid]
        return pad_x + (x - min_x) / span * (width - 2 * pad_x), pad_y + y * row_h

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'role="img" aria-label="Lifting tree of a polynomial congruence">'
    ]
    for node in nodes:
        if node.parent_id and node.parent_id in by_id:
            x1, y1 = px(node.parent_id)
            x2, y2 = px(node.id)
            colour = LIFT_KIND_COLORS[by_id[node.parent_id].kind]
            parts.append(
                f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                f'stroke="{colour}" stroke-width="2"/>'
            )
            trit = node.word[-1] if node.word else 0
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            parts.append(
                f'<text x="{mx:.1f}" y="{my - 4:.1f}" font-size="10" '
                f'font-family="ui-monospace, monospace" fill="#666" '
                f'text-anchor="middle">{trit:+d}</text>'
            )
    for node in nodes:
        x, y = px(node.id)
        colour = LIFT_KIND_COLORS[node.kind]
        selected = node.id == selected_id
        stroke = "#f5d76e" if selected else "#222"
        sw = 3.5 if selected else 1.2
        r = 12
        if node.kind == "terminal":
            parts.append(
                f'<rect x="{x - r:.1f}" y="{y - r:.1f}" width="{2 * r}" height="{2 * r}" '
                f'fill="{colour}" stroke="{stroke}" stroke-width="{sw}" rx="2">'
                f"<title>{_lift_node_title(node)}</title></rect>"
            )
        else:
            parts.append(
                f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{colour}" '
                f'stroke="{stroke}" stroke-width="{sw}">'
                f"<title>{_lift_node_title(node)}</title></circle>"
            )
        parts.append(
            f'<text x="{x:.1f}" y="{y + 24:.1f}" font-size="10" '
            f'font-family="ui-monospace, monospace" text-anchor="middle" '
            f'fill="#333">{node.residue}</text>'
        )
        parts.append(
            f'<text x="{x:.1f}" y="{y + 4:.1f}" font-size="9" '
            f'font-family="ui-monospace, monospace" text-anchor="middle" '
            f'fill="#111">{len(node.lift_trits)}</text>'
        )
    parts.append("</svg>")
    return "".join(parts)


def lift_table_rows(nodes: tuple[LiftTreeNode, ...]) -> list[dict[str, object]]:
    rows = []
    for node in nodes:
        rows.append(
            {
                "word": node.digits,
                "level": node.depth,
                "x": node.residue,
                "f(x)": node.f_value,
                "v3(f)": "inf" if node.v3_f is None else node.v3_f,
                "v3(f')": "inf" if node.v3_f_prime is None else node.v3_f_prime,
                "residual": node.residual,
                "newton": list(node.newton),
                "lift type": node.kind,
                "lifts": len(node.lift_trits),
            }
        )
    return rows


def node_table_rows(nodes: tuple[TreeNode, ...]) -> list[dict[str, object]]:
    rows = []
    for node in nodes:
        rows.append(
            {
                "id": node.id,
                "depth": node.depth,
                "p": node.packed_p,
                "class": node.class_id,
                "visible size": node.visible_count,
                "kind": "merged" if node.merged_visible else "singleton",
                "residual": node.residual,
            }
        )
    return rows
