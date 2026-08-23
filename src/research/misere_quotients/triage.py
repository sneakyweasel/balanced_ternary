"""Exact Phase-0 tests for finite-context misere signatures.

This module does not implement MisereSolver, a generic rules engine, or a
claim that a finite table is a misere quotient. It computes

    FINITE-CONTEXT EQUIVALENCE

on bounded heap universes, and compares that relation to the published
0.123 quotient and to published Dawson’s Kayles single-heap outcomes.

Empty positions and other terminal positions are N: the player to move
cannot move, so the previous player made the last legal move and loses.
"""

from __future__ import annotations

from collections import defaultdict
from functools import lru_cache
from itertools import combinations_with_replacement
from typing import Iterable, Literal

from research.misere_quotients.reference import (
    DAWSON_Q33_P_SIZE,
    DAWSON_Q_CHECKPOINTS,
    Q123_ELEMENTS,
    Q123_P,
    dawson_phi_predicts_P,
    q123_is_P,
    q123_multiply,
    q123_position_phi,
)

Position = tuple[int, ...]
Outcome = Literal["P", "N"]
Game = Literal["0.123", "0.07"]

# Phase-0 budgets. Dawson Q_33 / Q_34 reconstruction is out of scope.
Q123_MAX_HEAP = 16
Q123_MAX_HEAPS = 5
Q123_MAX_TOTAL = 24
Q123_CONTEXT_TOTALS: tuple[int, ...] = (0, 1, 2, 3, 4, 6, 8, 12)

DAWSON_MAX_HEAP = 8
DAWSON_MAX_HEAPS = 4
DAWSON_MAX_TOTAL = 16
DAWSON_SINGLE_HEAP_BOUND = 33
DAWSON_CONTEXT_TOTALS: tuple[int, ...] = (0, 2, 4, 6, 8)


def _require_game(game: str) -> Game:
    if game not in ("0.123", "0.07"):
        raise ValueError("game must be '0.123' or '0.07'")
    return game  # type: ignore[return-value]


def _require_nonneg(n: int, name: str) -> int:
    if isinstance(n, bool) or not isinstance(n, int) or n < 0:
        raise ValueError(f"{name} must be a nonnegative int")
    return n


def canonicalize(heaps: Iterable[int]) -> Position:
    """Sorted tuple of positive heap sizes."""

    values = []
    for heap in heaps:
        if isinstance(heap, bool) or not isinstance(heap, int) or heap < 0:
            raise ValueError("heap sizes must be nonnegative ints")
        if heap > 0:
            values.append(heap)
    return tuple(sorted(values))


def add_positions(left: Position, right: Position) -> Position:
    return canonicalize(left + right)


def size(position: Position) -> int:
    return sum(position)


def context_key(position: Position) -> tuple[int, int, Position]:
    """Distinguishing-context metric: total stones, then heap count, then tuple."""

    return (size(position), len(position), position)


def options(game: Game, position: Position) -> tuple[Position, ...]:
    """Legal options of one coded octal game. Not a generic rules engine."""

    game = _require_game(game)
    seen: set[Position] = set()
    if game == "0.123":
        for index, heap in enumerate(position):
            rest = position[:index] + position[index + 1 :]
            if heap == 1:
                seen.add(rest)
            if heap > 2:
                seen.add(canonicalize(rest + ((heap - 2),)))
            if heap >= 3:
                seen.add(canonicalize(rest + ((heap - 3),)))
    else:
        for index, heap in enumerate(position):
            rest = position[:index] + position[index + 1 :]
            if heap < 2:
                continue
            for start in range(heap - 1):
                left = start
                right = heap - (start + 2)
                extra: list[int] = []
                if left:
                    extra.append(left)
                if right:
                    extra.append(right)
                seen.add(canonicalize(rest + tuple(extra)))
    return tuple(sorted(seen, key=context_key))


@lru_cache(maxsize=None)
def misere_outcome(game: Game, position: Position) -> Outcome:
    """Exact misere outcome. Terminals are N."""

    game = _require_game(game)
    for child in options(game, position):
        if misere_outcome(game, child) == "P":
            return "N"
    return "N" if not options(game, position) else "P"


def bounded_positions(max_heap: int, max_heaps: int, max_total: int) -> tuple[Position, ...]:
    """All sorted heap tuples inside the three bounds, including empty."""

    max_heap = _require_nonneg(max_heap, "max_heap")
    max_heaps = _require_nonneg(max_heaps, "max_heaps")
    max_total = _require_nonneg(max_total, "max_total")
    positions = [()]
    for count in range(1, max_heaps + 1):
        for combo in combinations_with_replacement(range(1, max_heap + 1), count):
            if sum(combo) <= max_total:
                positions.append(combo)
    return tuple(sorted(positions, key=context_key))


def context_signature(
    game: Game,
    position: Position,
    contexts: Iterable[Position],
) -> tuple[Outcome, ...]:
    """Finite-context signature Σ_C(G) = (o^-(G+X))_{X in C}."""

    game = _require_game(game)
    return tuple(
        misere_outcome(game, add_positions(position, context)) for context in contexts
    )


def distinguish(
    game: Game,
    left: Position,
    right: Position,
    contexts: Iterable[Position],
) -> Position | None:
    """Least context in ``contexts`` that separates the two positions, if any."""

    game = _require_game(game)
    if left == right:
        return None
    for context in sorted(contexts, key=context_key):
        if misere_outcome(game, add_positions(left, context)) != misere_outcome(
            game, add_positions(right, context)
        ):
            return context
    return None


def refine_partition(
    game: Game,
    positions: Iterable[Position],
    contexts: Iterable[Position],
) -> dict[tuple[Outcome, ...], tuple[Position, ...]]:
    """Partition a finite universe by a finite context signature."""

    game = _require_game(game)
    groups: dict[tuple[Outcome, ...], list[Position]] = defaultdict(list)
    context_list = tuple(contexts)
    for position in positions:
        groups[context_signature(game, position, context_list)].append(position)
    return {
        signature: tuple(sorted(members, key=context_key))
        for signature, members in groups.items()
    }


def class_count(game: Game, positions: Iterable[Position], contexts: Iterable[Position]) -> int:
    return len(refine_partition(game, positions, contexts))


def candidate_quotient(
    game: Game,
    positions: Iterable[Position],
    contexts: Iterable[Position],
) -> dict[str, object]:
    """Audit the finite-context classes as a multiplication table.

    This is a candidate, not a misere quotient. Products that leave the
    finite universe are unresolved.
    """

    game = _require_game(game)
    universe = tuple(sorted(set(positions), key=context_key))
    present = set(universe)
    partition = refine_partition(game, universe, contexts)
    signature_of = {
        member: signature
        for signature, members in partition.items()
        for member in members
    }
    products: dict[tuple[tuple[Outcome, ...], tuple[Outcome, ...]], set[tuple[Outcome, ...]]] = (
        defaultdict(set)
    )
    unresolved = 0
    for left in universe:
        for right in universe:
            total = add_positions(left, right)
            if total not in present:
                unresolved += 1
                continue
            products[(signature_of[left], signature_of[right])].add(signature_of[total])
    ill_defined = sum(1 for images in products.values() if len(images) > 1)
    identity = signature_of[()]
    identity_ok = all(
        signature_of[add_positions(position, ())] == signature_of[position]
        for position in universe
    )
    representatives = {signature: members[0] for signature, members in partition.items()}
    p_classes = [
        signature
        for signature, members in partition.items()
        if misere_outcome(game, members[0]) == "P"
    ]
    return {
        "positions": len(universe),
        "contexts": len(tuple(contexts)),
        "classes": len(partition),
        "p_classes": len(p_classes),
        "identity": identity,
        "identity_acts": identity_ok,
        "defined_products": len(products),
        "ill_defined_products": ill_defined,
        "unresolved_products": unresolved,
        "well_defined_on_represented_products": ill_defined == 0,
        "representatives": {
            _signature_label(signature): list(rep)
            for signature, rep in representatives.items()
        },
    }


def refinement_trace(
    game: Game,
    positions: Iterable[Position],
    context_totals: Iterable[int],
    *,
    max_heap: int,
    max_heaps: int,
) -> list[dict[str, object]]:
    """Class counts along C_t = { positions of total size ≤ t }."""

    universe = tuple(positions)
    rows = []
    previous = 1
    for total in context_totals:
        contexts = bounded_positions(max_heap, max_heaps, total)
        count = class_count(game, universe, contexts)
        rows.append(
            {
                "context_total": total,
                "contexts": len(contexts),
                "classes": count,
                "new_splits": count - previous,
            }
        )
        previous = count
    return rows


def q123_monoid_self_check() -> dict[str, object]:
    """Internal consistency of the published 20-element table."""

    e = "e"
    x, z, a, b = "x", "z", "a", "b"
    relations = {
        "x2": q123_multiply(x, x) == e,
        "a2": q123_multiply(a, a) == e,
        "z4_eq_z2": q123_multiply(q123_multiply(z, z), q123_multiply(z, z))
        == q123_multiply(z, z),
        "b4_eq_b2": q123_multiply(q123_multiply(b, b), q123_multiply(b, b))
        == q123_multiply(b, b),
        "abz_eq_b": q123_multiply(q123_multiply(a, b), z) == b,
        "b3x_eq_b2": q123_multiply(q123_multiply(q123_multiply(b, b), b), x)
        == q123_multiply(b, b),
        "z3a_eq_z2": q123_multiply(q123_multiply(q123_multiply(z, z), z), a)
        == q123_multiply(z, z),
    }
    commutative = True
    associative_sample = True
    for left in Q123_ELEMENTS:
        for right in Q123_ELEMENTS:
            if q123_multiply(left, right) != q123_multiply(right, left):
                commutative = False
        if q123_multiply(e, left) != left or q123_multiply(left, e) != left:
            commutative = False
    for left in (e, x, z, a, b, "xa", "b2"):
        for mid in (e, x, z, a, b):
            for right in (e, x, z, a, b):
                lm = q123_multiply(left, mid)
                mr = q123_multiply(mid, right)
                if q123_multiply(lm, right) != q123_multiply(left, mr):
                    associative_sample = False
    return {
        "order": len(Q123_ELEMENTS),
        "p_size": len(Q123_P),
        "relations": relations,
        "relations_hold": all(relations.values()),
        "commutative": commutative,
        "associative_on_generator_sample": associative_sample,
        "even_order": len(Q123_ELEMENTS) % 2 == 0,
    }


def q123_outcome_agreement(
    positions: Iterable[Position],
) -> dict[str, object]:
    """Published monoid P-set versus exact misere outcomes."""

    disagreements: list[dict[str, object]] = []
    for position in positions:
        predicted = "P" if q123_is_P(q123_position_phi(position)) else "N"
        actual = misere_outcome("0.123", position)
        if predicted != actual:
            disagreements.append(
                {
                    "position": list(position),
                    "phi": q123_position_phi(position),
                    "predicted": predicted,
                    "actual": actual,
                }
            )
            if len(disagreements) >= 8:
                break
    universe = tuple(positions)
    return {
        "positions": len(universe),
        "disagreements": disagreements,
        "agrees": not disagreements,
    }


def q123_class_recovery(
    positions: Iterable[Position],
    contexts: Iterable[Position],
) -> dict[str, object]:
    """Finite-context classes versus published monoid images on a finite U."""

    universe = tuple(positions)
    context_list = tuple(contexts)
    partition = refine_partition("0.123", universe, context_list)
    phi_of: dict[tuple[Outcome, ...], set[str]] = defaultdict(set)
    for signature, members in partition.items():
        for member in members:
            phi_of[signature].add(q123_position_phi(member))
    mixed = {
        _signature_label(signature): sorted(images)
        for signature, images in phi_of.items()
        if len(images) > 1
    }
    recovered = {next(iter(images)) for images in phi_of.values() if len(images) == 1}
    representatives = {
        q123_position_phi(members[0]): members[0]
        for members in partition.values()
        if len({q123_position_phi(member) for member in members}) == 1
    }
    pairwise_witnesses = 0
    missing_witnesses = 0
    sample_witnesses: list[dict[str, object]] = []
    names = sorted(representatives)
    for i, left_name in enumerate(names):
        for right_name in names[i + 1 :]:
            witness = distinguish(
                "0.123",
                representatives[left_name],
                representatives[right_name],
                context_list,
            )
            if witness is None:
                missing_witnesses += 1
            else:
                pairwise_witnesses += 1
                if len(sample_witnesses) < 6:
                    sample_witnesses.append(
                        {
                            "left": left_name,
                            "right": right_name,
                            "left_position": list(representatives[left_name]),
                            "right_position": list(representatives[right_name]),
                            "context": list(witness),
                            "context_size": size(witness),
                        }
                    )
    product_mismatches = 0
    product_checks = 0
    present = set(universe)
    for left in universe:
        for right in universe:
            total = add_positions(left, right)
            if total not in present:
                continue
            product_checks += 1
            if q123_position_phi(total) != q123_multiply(
                q123_position_phi(left), q123_position_phi(right)
            ):
                product_mismatches += 1
    return {
        "positions": len(universe),
        "contexts": len(context_list),
        "finite_context_classes": len(partition),
        "published_elements_seen": len({q123_position_phi(pos) for pos in universe}),
        "mixed_finite_context_classes": mixed,
        "recovered_published_classes": len(recovered),
        "pairwise_witnesses": pairwise_witnesses,
        "missing_witnesses": missing_witnesses,
        "sample_witnesses": sample_witnesses,
        "product_checks": product_checks,
        "product_mismatches": product_mismatches,
        "recovers_published_classes": (
            not mixed and len(recovered) == len({q123_position_phi(pos) for pos in universe})
        ),
    }


def dawson_single_heap_check(bound: int = DAWSON_SINGLE_HEAP_BOUND) -> dict[str, object]:
    """Exact single-heap outcomes versus published Q33 Phi P-membership."""

    bound = _require_nonneg(bound, "bound")
    rows: list[dict[str, object]] = []
    disagreements: list[dict[str, object]] = []
    for heap in range(0, bound + 1):
        actual = misere_outcome("0.07", () if heap == 0 else (heap,))
        predicted = dawson_phi_predicts_P(heap)
        predicted_outcome = None if predicted is None else ("P" if predicted else "N")
        row = {
            "heap": heap,
            "actual": actual,
            "published_phi": None if heap > 33 else True,
            "predicted": predicted_outcome,
        }
        rows.append(row)
        if predicted_outcome is not None and predicted_outcome != actual:
            disagreements.append(row)
    return {
        "bound": bound,
        "checked": len(rows),
        "disagreements": disagreements,
        "agrees": not disagreements,
        "p_heaps": [row["heap"] for row in rows if row["actual"] == "P"],
    }


def dawson_refinement_boundary() -> dict[str, object]:
    """Bounded finite-context growth for 0.07. Not |Q_n|."""

    universe = bounded_positions(DAWSON_MAX_HEAP, DAWSON_MAX_HEAPS, DAWSON_MAX_TOTAL)
    trace = refinement_trace(
        "0.07",
        universe,
        DAWSON_CONTEXT_TOTALS,
        max_heap=DAWSON_MAX_HEAP,
        max_heaps=DAWSON_MAX_HEAPS,
    )
    return {
        "label": "FINITE-CONTEXT EQUIVALENCE",
        "universe_max_heap": DAWSON_MAX_HEAP,
        "universe_max_heaps": DAWSON_MAX_HEAPS,
        "universe_max_total": DAWSON_MAX_TOTAL,
        "positions": len(universe),
        "trace": trace,
        "published_Q_n_checkpoints": [
            {"heap_bound": heap, "quotient_order": order}
            for heap, order in DAWSON_Q_CHECKPOINTS
        ],
        "published_Q33_P_size": DAWSON_Q33_P_SIZE,
        "q34_attempted": False,
        "classification": (
            "Finite-context class counts on a bounded-multiplicity slice "
            "are not the partial quotients Q_n. Nontermination or growth "
            "is not evidence that Q_34 is infinite."
        ),
    }


def triage_report() -> dict[str, object]:
    """Complete bounded report. No automatic promotion."""

    universe = bounded_positions(Q123_MAX_HEAP, Q123_MAX_HEAPS, Q123_MAX_TOTAL)
    empty_contexts = ((),)
    heap_contexts = ((),) + tuple((n,) for n in range(1, Q123_MAX_HEAP + 1))
    full_contexts = bounded_positions(Q123_MAX_HEAP, Q123_MAX_HEAPS, 12)
    monoid = q123_monoid_self_check()
    outcomes = q123_outcome_agreement(universe)
    recovery = q123_class_recovery(universe, full_contexts)
    q123_trace = refinement_trace(
        "0.123",
        universe,
        Q123_CONTEXT_TOTALS,
        max_heap=Q123_MAX_HEAP,
        max_heaps=Q123_MAX_HEAPS,
    )
    audit = candidate_quotient("0.123", universe, full_contexts)
    dawson_heaps = dawson_single_heap_check()
    dawson_boundary = dawson_refinement_boundary()
    same_as_published_algorithm = (
        monoid["relations_hold"]
        and outcomes["agrees"]
        and recovery["recovers_published_classes"]
        and dawson_heaps["agrees"]
    )
    return {
        "game_validation": "0.123",
        "open_target": "0.07 Q_34 not attempted",
        "q123": {
            "monoid": monoid,
            "outcome_agreement": outcomes,
            "refinement": q123_trace,
            "recovery": recovery,
            "candidate_audit": {
                "classes": audit["classes"],
                "p_classes": audit["p_classes"],
                "ill_defined_products": audit["ill_defined_products"],
                "unresolved_products": audit["unresolved_products"],
                "well_defined_on_represented_products": audit[
                    "well_defined_on_represented_products"
                ],
            },
            "empty_context_classes": class_count("0.123", universe, empty_contexts),
            "single_heap_context_classes": class_count("0.123", universe, heap_contexts),
        },
        "dawson": {
            "single_heap": dawson_heaps,
            "finite_context_boundary": dawson_boundary,
        },
        "method_transfer": {
            "bt_arithmetic_used": False,
            "signature_witness_quotient_used": True,
            "classical_name": "indistinguishability congruence / reducedness",
        },
        "gate": "CLOSE",
        "classification": "REPARAMETERIZATION",
        "same_as_published_algorithm": same_as_published_algorithm,
    }


def _signature_label(signature: tuple[Outcome, ...]) -> str:
    return "".join(signature)
