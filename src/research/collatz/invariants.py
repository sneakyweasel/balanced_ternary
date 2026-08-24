"""Executable Collatz / balanced ternary identities.

Every check is a verification of a claimed identity. Finite-range success
is recorded as COMPUTATIONALLY VERIFIED unless a proof is given in
``docs/collatz_mathematics.md``.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from bt.metrics import weight
from bt.representation import decode, encode
from research.collatz.automata.two_adic import TwoAdicDigitAutomaton
from bt.arithmetic import add_one, multiply_by_three, three_n_plus_one_word
from research.collatz.core import collatz_step, collatz_valuation, three_n_plus_one
from research.collatz.features import extract_features
from research.collatz.inverse import collatz_predecessors
from research.collatz.theorems import append_plus, predicted_features_after_append_plus
from research.collatz.transducers.odd_part import odd_part_word
from research.collatz.valuation import classify_collatz_valuation, v2


@dataclass
class InvariantFailure:
    name: str
    n: int
    detail: str


@dataclass
class CollatzInvariantReport:
    limit: int
    checked_odd: int
    failures: list[InvariantFailure] = field(default_factory=list)
    automaton_precision: int = 8
    inverse_k_max: int = 16

    @property
    def ok(self) -> bool:
        return not self.failures


def check_odd_weight(n: int) -> bool:
    """``n`` odd iff ``weight(BT(n))`` odd. EXACT — HUMAN PROOF (existing parity theorem)."""
    return (n % 2) == (weight(encode(n)) % 2)


def check_three_n_plus_one_even_weight(n: int) -> bool:
    """For odd ``n``, ``3n+1`` is even so its balanced ternary weight is even."""
    y = 3 * n + 1
    return (y % 2 == 0) and (weight(encode(y)) % 2 == 0)


def check_T_odd_and_not_divisible_by_three(n: int) -> bool:
    t = collatz_step(n)
    return t % 2 == 1 and t % 3 != 0


def check_ternary_shift_add_one(n: int) -> bool:
    word = encode(n)
    return (
        decode(multiply_by_three(word)) == 3 * n
        and decode(add_one(multiply_by_three(word))) == 3 * n + 1
        and three_n_plus_one_word(word) == encode(3 * n + 1)
    )


def check_valuation_classification(n: int, precision: int) -> bool:
    actual = v2(3 * n + 1)
    if actual is None:
        return False
    cls = classify_collatz_valuation(n % (1 << precision), precision)
    if cls.is_exact:
        return actual == cls.exact_k
    return actual >= precision


def check_automaton_residue(n: int, precision: int) -> bool:
    auto = TwoAdicDigitAutomaton(precision)
    return auto.residue(encode(n)) == n % auto.modulus


def check_append_plus_theorem(n: int) -> bool:
    """``BT(3n+1) = BT(n)+`` and closed-form features. ``n != 0``."""
    if n == 0:
        return True
    word = encode(n)
    plus = append_plus(word)
    if plus != encode(3 * n + 1):
        return False
    return predicted_features_after_append_plus(word) == extract_features(plus)


def check_odd_part_collatz(n: int) -> bool:
    """``odd_part(BT(n)+) == BT(T(n))`` for positive odd n."""
    w = encode(n)
    return odd_part_word(append_plus(w)) == encode(collatz_step(n))


def check_inverse_round_trip(m: int, k_max: int) -> bool:
    for k, pred in collatz_predecessors(m, k_max):
        if collatz_step(pred) != m:
            return False
        if collatz_valuation(pred) != k:
            return False
    return True


def verify_collatz_invariants(
    limit: int,
    automaton_precision: int = 8,
    inverse_k_max: int = 16,
) -> CollatzInvariantReport:
    """Check Milestone-1 identities for every odd ``n`` with ``1 <= n <= limit``."""
    if isinstance(limit, bool) or not isinstance(limit, int) or limit < 1:
        raise ValueError(f"limit must be an integer >= 1, got {limit!r}")
    report = CollatzInvariantReport(
        limit=limit,
        checked_odd=0,
        automaton_precision=automaton_precision,
        inverse_k_max=inverse_k_max,
    )
    auto = TwoAdicDigitAutomaton(automaton_precision)
    modulus = auto.modulus
    for n in range(1, limit + 1, 2):
        report.checked_odd += 1
        if not check_odd_weight(n):
            report.failures.append(
                InvariantFailure(
                    "odd_weight",
                    n,
                    f"n mod 2 = {n % 2}, weight mod 2 = {weight(encode(n)) % 2}",
                )
            )
        if not check_three_n_plus_one_even_weight(n):
            y = three_n_plus_one(n)
            report.failures.append(
                InvariantFailure(
                    "even_weight_3n_plus_1",
                    n,
                    f"3n+1={y}, weight mod 2 = {weight(encode(y)) % 2}",
                )
            )
        if not check_T_odd_and_not_divisible_by_three(n):
            t = collatz_step(n)
            report.failures.append(
                InvariantFailure(
                    "T_odd_not_div3",
                    n,
                    f"T(n)={t}",
                )
            )
        if not check_ternary_shift_add_one(n):
            report.failures.append(
                InvariantFailure(
                    "ternary_shift_add_one",
                    n,
                    f"word={encode(n).word()} 3n+1={3 * n + 1}",
                )
            )
        if not check_append_plus_theorem(n):
            report.failures.append(
                InvariantFailure(
                    "append_plus",
                    n,
                    f"BT(n)+ != BT(3n+1) or feature prediction failed",
                )
            )
        if not check_odd_part_collatz(n):
            report.failures.append(
                InvariantFailure(
                    "odd_part",
                    n,
                    f"odd_part(BT(n)+) != BT(T(n))",
                )
            )
        if not check_valuation_classification(n, automaton_precision):
            actual = v2(3 * n + 1)
            cls = classify_collatz_valuation(n % modulus, automaton_precision)
            report.failures.append(
                InvariantFailure(
                    "valuation_class",
                    n,
                    f"actual v2={actual}, class={cls.label()}",
                )
            )
        word = encode(n)
        if auto.residue(word) != n % modulus:
            report.failures.append(
                InvariantFailure(
                    "two_adic_residue",
                    n,
                    f"automaton={auto.residue(word)}, n mod 2^K={n % modulus}",
                )
            )
        if not check_inverse_round_trip(n, inverse_k_max):
            report.failures.append(
                InvariantFailure(
                    "inverse_round_trip",
                    n,
                    f"a predecessor of {n} failed T(pred)=n",
                )
            )
    return report
