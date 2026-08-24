"""Failed implications as reusable knowledge.

A planner must query this before promoting a hypothesis. Schema
records are problem-independent; instance records belong on adapters.
"""

from __future__ import annotations

from dataclasses import dataclass

from research_engine.core.semantics import ClaimKind


@dataclass(frozen=True)
class ForbiddenImplication:
    id: str
    antecedent: str
    consequent: str
    from_kind: ClaimKind
    to_kind: ClaimKind
    statement: str
    counterexample: str
    generality: str = "schema"
    problem: str = ""
    closed_attacks: tuple[str, ...] = ()


GENERIC_FORBIDDEN: tuple[ForbiddenImplication, ...] = (
    ForbiddenImplication(
        id="terminal_unbounded_not_live_unbounded",
        antecedent="terminal_unbounded",
        consequent="live_unbounded",
        from_kind=ClaimKind.TERMINAL,
        to_kind=ClaimKind.LIVE,
        statement="TERMINAL geometry does not imply LIVE infinitude",
        counterexample="an unbounded terminal predicate can coexist with a bounded live slice",
    ),
    ForbiddenImplication(
        id="bounded_census_not_asymptotic",
        antecedent="finite_horizon_complete",
        consequent="asymptotic_live",
        from_kind=ClaimKind.LIVE_SLICE,
        to_kind=ClaimKind.LIVE,
        statement="a complete finite-horizon BFS is not an asymptotic live-set theorem",
        counterexample="SearchScope.BOUNDED is not SearchScope.EXACT",
    ),
    ForbiddenImplication(
        id="co_reachable_seed_not_live",
        antecedent="co_reachable_seed",
        consequent="live_set",
        from_kind=ClaimKind.CO_REACHABLE,
        to_kind=ClaimKind.LIVE,
        statement="C(seed) is not the live set",
        counterexample="a finite reverse basin of {0} need not equal R ∩ C(K)",
    ),
    ForbiddenImplication(
        id="observed_bound_not_invariant",
        antecedent="functional_sample_bound",
        consequent="functional_invariant",
        from_kind=ClaimKind.LIVE_SLICE,
        to_kind=ClaimKind.LIVE,
        statement="a finite max |ℓ| is not an invariant and not an asymptotic bound",
        counterexample="LinearFunctional.observed_bound is a sample maximum",
    ),
    ForbiddenImplication(
        id="reachable_map_law_not_live",
        antecedent="affine_image_residue",
        consequent="live_unbounded",
        from_kind=ClaimKind.REACHABLE,
        to_kind=ClaimKind.LIVE,
        statement="an exact residue law of Ax+b_u is not LIVE infinitude",
        counterexample="forced s_i ≡ 0 (mod g) constrains images, not |L|",
    ),
    ForbiddenImplication(
        id="unbounded_words_not_unbounded_terminals",
        antecedent="unbounded_accepted_words",
        consequent="unbounded_terminals",
        from_kind=ClaimKind.LIVE_SLICE,
        to_kind=ClaimKind.TERMINAL,
        statement="infinitely many accepted words do not imply infinitely many terminals",
        counterexample="a reset loop at 0 with accepting set {0}",
    ),
    ForbiddenImplication(
        id="expanding_modes_not_live_unbounded",
        antecedent="expanding_modes_unbounded",
        consequent="live_unbounded",
        from_kind=ClaimKind.REACHABLE,
        to_kind=ClaimKind.LIVE,
        statement="expanding companion modes are not LIVE infinitude",
        counterexample="a uniform unnormalized mode bound can fail on a bounded live slice",
    ),
)


@dataclass(frozen=True)
class NegativeKnowledge:
    records: tuple[ForbiddenImplication, ...] = GENERIC_FORBIDDEN

    def extend(self, extra: tuple[ForbiddenImplication, ...]) -> NegativeKnowledge:
        return NegativeKnowledge(self.records + extra)

    def forbids(self, antecedent: str, consequent: str) -> ForbiddenImplication | None:
        for record in self.records:
            if record.antecedent == antecedent and record.consequent == consequent:
                return record
        return None

    def forbids_kinds(self, from_kind: ClaimKind, to_kind: ClaimKind) -> ForbiddenImplication | None:
        if from_kind is to_kind:
            return None
        for record in self.records:
            if record.from_kind is from_kind and record.to_kind is to_kind:
                return record
        return None

    def closed_attacks(self) -> frozenset[str]:
        names: set[str] = set()
        for record in self.records:
            names.update(record.closed_attacks)
        return frozenset(names)
