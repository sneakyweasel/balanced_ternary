"""Layer C: admissible valuation prefixes and growth budget.

A state is a pair ``(r, P)`` meaning ``n ≡ r (mod 2^P)`` with ``r`` odd.
If ``v2(3r+1) = k`` is exact (``k < P``), the next state is

    (((3r+1) mod 2^P) >> k,  P - k)

This is the residue transition Milestone 1 refused: division by ``2^k``
lowers the modulus to ``2^{P-k}``. Never divide modulo ``2^P``.

A finite word ``k1...km`` is admissible iff some odd integer realizes those
successive valuations. At a fixed starting precision ``P``:

- **ADMISSIBLE**: some residue completes every exact-k test
- **INCONCLUSIVE**: every attempt hits ``AT_LEAST_K`` before the word ends
  (need more precision)
- **FORBIDDEN**: some prefix is fully testable and no residue matches it

Growth budget uses the exact comparison ``2^{sum k}`` vs ``3^m`` (no floats).
``sign(sum k - m log2 3) = sign(2^{sum k} - 3^m)``. Equality is impossible
for ``m > 0`` because ``log2 3`` is irrational. This is the *homogeneous*
size estimate; the affine ``+1`` terms of T are not included. Contraction
is not a Lyapunov function and is not a proof of Collatz.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product

from research.collatz.core import collatz_step, collatz_valuation
from research.collatz.valuation import classify_collatz_valuation


@dataclass(frozen=True)
class PrecisionState:
    residue: int
    precision: int

    def modulus(self) -> int:
        return 1 << self.precision


def exact_collatz_residue_step(
    state: PrecisionState, k: int
) -> PrecisionState | None:
    """Take an exact-k edge, or ``None`` if k is not determined / does not match."""
    if k < 1 or k >= state.precision:
        return None
    cls = classify_collatz_valuation(state.residue, state.precision)
    if not cls.is_exact or cls.exact_k != k:
        return None
    modulus = state.modulus()
    y = (3 * state.residue + 1) % modulus
    nxt = PrecisionState(residue=y >> k, precision=state.precision - k)
    nxt_mod = nxt.modulus()
    return PrecisionState(residue=nxt.residue % nxt_mod, precision=nxt.precision)


def follow_path(
    start: PrecisionState, ks: tuple[int, ...]
) -> tuple[PrecisionState | None, str]:
    """Walk ``ks`` from ``start``.

    Returns ``(final_state, status)`` where status is
    ``ok``, ``mismatch``, or ``insufficient_precision``.
    """
    state = start
    for k in ks:
        if k >= state.precision:
            return None, "insufficient_precision"
        cls = classify_collatz_valuation(state.residue, state.precision)
        if not cls.is_exact:
            return None, "insufficient_precision"
        if cls.exact_k != k:
            return None, "mismatch"
        stepped = exact_collatz_residue_step(state, k)
        if stepped is None:
            return None, "mismatch"
        state = stepped
    return state, "ok"


class AdmissibleValuationAutomaton:
    """Exact-k labelled graph on ``(residue, precision)`` states."""

    def __init__(self, precision: int, k_max: int):
        if isinstance(precision, bool) or not isinstance(precision, int) or precision < 2:
            raise ValueError(f"precision must be an integer >= 2, got {precision!r}")
        if isinstance(k_max, bool) or not isinstance(k_max, int) or k_max < 1:
            raise ValueError(f"k_max must be an integer >= 1, got {k_max!r}")
        self.precision = precision
        self.k_max = k_max

    def start_states(self) -> tuple[PrecisionState, ...]:
        return tuple(
            PrecisionState(r, self.precision)
            for r in range(1, 1 << self.precision, 2)
        )

    def unique_exact_edge(self, state: PrecisionState) -> tuple[int, PrecisionState] | None:
        cls = classify_collatz_valuation(state.residue, state.precision)
        if not cls.is_exact:
            return None
        k = cls.exact_k
        assert k is not None
        if k > self.k_max:
            return None
        nxt = exact_collatz_residue_step(state, k)
        if nxt is None:
            return None
        return k, nxt

    def path_from(self, start: PrecisionState, max_length: int) -> tuple[int, ...]:
        ks: list[int] = []
        state = start
        for _ in range(max_length):
            edge = self.unique_exact_edge(state)
            if edge is None:
                break
            k, state = edge
            ks.append(k)
        return tuple(ks)

    def classify_word(self, ks: tuple[int, ...]) -> str:
        saw_ok = False
        saw_insufficient = False
        for start in self.start_states():
            _, status = follow_path(start, ks)
            if status == "ok":
                saw_ok = True
                break
            if status == "insufficient_precision":
                saw_insufficient = True
        if saw_ok:
            return "ADMISSIBLE"
        if saw_insufficient:
            return "INCONCLUSIVE"
        return "FORBIDDEN"

    def enumerate_admissible(self, length: int) -> AdmissiblePrefixReport:
        if isinstance(length, bool) or not isinstance(length, int) or length < 1:
            raise ValueError(f"length must be an integer >= 1, got {length!r}")
        prefixes: set[tuple[int, ...]] = set()
        full_paths: list[tuple[int, ...]] = []
        for start in self.start_states():
            path = self.path_from(start, length)
            full_paths.append(path)
            for i in range(1, len(path) + 1):
                prefixes.add(path[:i])
        by_length: dict[int, list[tuple[int, ...]]] = {}
        for word in prefixes:
            by_length.setdefault(len(word), []).append(word)
        for lst in by_length.values():
            lst.sort()
        budgets = {word: growth_budget(word) for word in prefixes}
        return AdmissiblePrefixReport(
            precision=self.precision,
            k_max=self.k_max,
            length=length,
            start_count=1 << (self.precision - 1),
            prefixes=frozenset(prefixes),
            by_length={L: tuple(ws) for L, ws in sorted(by_length.items())},
            budgets=budgets,
            contracting=sum(1 for b in budgets.values() if b.kind == "contracting"),
            expanding=sum(1 for b in budgets.values() if b.kind == "expanding"),
        )


@dataclass(frozen=True)
class GrowthBudget:
    ks: tuple[int, ...]
    sum_k: int
    steps: int
    two_power: int
    three_power: int
    kind: str  # contracting | expanding | equal

    def as_dict(self) -> dict[str, object]:
        return {
            "ks": list(self.ks),
            "sum_k": self.sum_k,
            "steps": self.steps,
            "two_power": self.two_power,
            "three_power": self.three_power,
            "kind": self.kind,
        }


def growth_budget(ks: tuple[int, ...]) -> GrowthBudget:
    m = len(ks)
    s = sum(ks)
    two_p = 1 << s
    three_p = 3**m
    if two_p > three_p:
        kind = "contracting"
    elif two_p < three_p:
        kind = "expanding"
    else:
        kind = "equal"
    return GrowthBudget(
        ks=ks, sum_k=s, steps=m, two_power=two_p, three_power=three_p, kind=kind
    )


def forbidden_patterns(
    automaton: AdmissibleValuationAutomaton, length: int
) -> tuple[tuple[int, ...], ...]:
    """Length-``length`` words over ``1..k_max`` that are FORBIDDEN at this P."""
    alphabet = range(1, automaton.k_max + 1)
    out: list[tuple[int, ...]] = []
    for word in product(alphabet, repeat=length):
        if automaton.classify_word(word) == "FORBIDDEN":
            out.append(word)
    return tuple(out)


def verify_residue_step_against_T(n: int, precision: int) -> bool:
    """``T(n) mod 2^{P-k}`` equals the residue step from ``n mod 2^P``."""
    if n % 2 == 0:
        raise ValueError("n must be odd")
    k = collatz_valuation(n)
    if k >= precision:
        return True  # not exact at this precision; nothing to check
    start = PrecisionState(n % (1 << precision), precision)
    nxt = exact_collatz_residue_step(start, k)
    if nxt is None:
        return False
    t = collatz_step(n)
    return t % nxt.modulus() == nxt.residue


@dataclass
class AdmissiblePrefixReport:
    precision: int
    k_max: int
    length: int
    start_count: int
    prefixes: frozenset[tuple[int, ...]]
    by_length: dict[int, tuple[tuple[int, ...], ...]]
    budgets: dict[tuple[int, ...], GrowthBudget]
    contracting: int
    expanding: int

    def format(self) -> str:
        lines = [
            f"Admissible valuation prefixes  P={self.precision}  "
            f"k_max={self.k_max}  length<={self.length}",
            f"start odd residues: {self.start_count}",
            f"admissible prefixes: {len(self.prefixes)}  "
            f"contracting={self.contracting}  expanding={self.expanding}",
            "",
        ]
        for L, words in self.by_length.items():
            n_c = sum(1 for w in words if self.budgets[w].kind == "contracting")
            n_e = len(words) - n_c
            lines.append(f"length {L}: {len(words)}  contracting={n_c} expanding={n_e}")
            sample = words[:12]
            for w in sample:
                b = self.budgets[w]
                lines.append(
                    f"  {w}  sum={b.sum_k}  2^sum={b.two_power}  "
                    f"3^m={b.three_power}  {b.kind}"
                )
            if len(words) > 12:
                lines.append(f"  ... ({len(words) - 12} more)")
        lines.append("")
        lines.append(
            "Budget is the homogeneous estimate 2^{sum k} vs 3^m. "
            "It is not a Lyapunov function."
        )
        lines.append("")
        return "\n".join(lines)
