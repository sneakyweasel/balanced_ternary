"""Ostrowski instance records of failed implications.

These restate existing REFUTED ledger rows as planner schemas.
They are not new theorems and do not decide |L_0|.
"""

from __future__ import annotations

from research_engine.core.semantics import ClaimKind, SearchScope
from research_engine.planner.hypothesis import Hypothesis, HypothesisStatus
from research_engine.planner.negative import ForbiddenImplication

L0_HYPOTHESIS = Hypothesis(
    id="ostrowski_L0_infinite",
    statement="the origin-reachable live set L_0 is infinite",
    kind=ClaimKind.LIVE,
    intended_scope=SearchScope.EXACT,
    status=HypothesisStatus.PARKED,
    problem="ostrowski",
    evidence="PARK |L_0|; no contraction on ker(u_n) and no explicit unbounded live family",
)

OSTROWSKI_FORBIDDEN: tuple[ForbiddenImplication, ...] = (
    ForbiddenImplication(
        id="ostrowski_unbounded_K_not_L0",
        antecedent="terminal_unbounded",
        consequent="live_unbounded",
        from_kind=ClaimKind.TERMINAL,
        to_kind=ClaimKind.LIVE,
        statement="unbounded K does not imply unbounded L_0",
        counterexample="kernel family t_n lies in K_n and is unbounded, not shown in R(0)",
        generality="instance",
        problem="ostrowski",
    ),
    ForbiddenImplication(
        id="ostrowski_long_words_not_infinite_L0",
        antecedent="long_accepted_words",
        consequent="infinite_terminals",
        from_kind=ClaimKind.SUFFIX,
        to_kind=ClaimKind.LIVE,
        statement="long origin-accepted words do not force infinitely many remaining-0 terminals (OST-np-long-words-infinite-L0)",
        counterexample="recurrence resets reuse terminals",
        generality="instance",
        problem="ostrowski",
    ),
    ForbiddenImplication(
        id="ostrowski_zero_value_not_monoid",
        antecedent="zero_value",
        consequent="monoid",
        from_kind=ClaimKind.REACHABLE,
        to_kind=ClaimKind.REACHABLE,
        statement="complete zero-value words do not form a monoid (OST-np-complete-zero-monoid)",
        counterexample="concatenating the hub word (1,-2) with itself",
        generality="instance",
        problem="ostrowski",
    ),
    ForbiddenImplication(
        id="ostrowski_C0_not_live",
        antecedent="co_reachable_seed",
        consequent="live_set",
        from_kind=ClaimKind.CO_REACHABLE,
        to_kind=ClaimKind.LIVE,
        statement="C({0}) is not the adder live set",
        counterexample="the accepting plane {s3=0} is infinite; reverse contraction bounds a seed, not L_0",
        generality="instance",
        problem="ostrowski",
    ),
    ForbiddenImplication(
        id="ostrowski_unnormalized_mode_not_L0_bound",
        antecedent="expanding_modes_unbounded",
        consequent="live_unbounded",
        from_kind=ClaimKind.REACHABLE,
        to_kind=ClaimKind.LIVE,
        statement="unbounded expanding companion modes are not an L_0 bound (OST-np-unnormalized-mode-bound)",
        counterexample="origin-live remaining-0 slices already violate a uniform |z_j|<=C",
        generality="instance",
        problem="ostrowski",
    ),
    ForbiddenImplication(
        id="ostrowski_extra_terminal_congruence",
        antecedent="s1_divisible_by_3",
        consequent="stronger_F_congruence",
        from_kind=ClaimKind.TERMINAL,
        to_kind=ClaimKind.TERMINAL,
        statement="no extra remaining-0 congruence on F beyond 3|a (OST-np-extra-terminal-congruence)",
        counterexample="observed terminals span 3Z x Z in F at finite horizon",
        generality="instance",
        problem="ostrowski",
    ),
)
