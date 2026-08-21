"""Branching lift tree and bounded precision-drop dual automaton.

The tree contains every finite valuation extension in the requested
bounded alphabet. Positive-lift edges are valid cylinder extensions, not
forbidden transitions.

The precision state stores a canonical endpoint modulo ``2^P`` and the
step index modulo a sufficient power-of-two period. A transition by ``k``
computes the exact lift digit when ``k < P`` and drops precision from
``P`` to ``P-k``. This is a bounded information model, not an automaton
for unrestricted Collatz dynamics.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from collatz.dual_code import CollatzDualCode


class LiftEdgeClass(str, Enum):
    ZERO_LIFT = "ZERO_LIFT"
    POSITIVE_LIFT = "POSITIVE_LIFT"


@dataclass(frozen=True)
class LiftTreeNode:
    itinerary: tuple[int, ...]
    m: int
    K: int
    C: int
    residue: int
    modulus: int
    R: int
    balanced_ternary_R: str
    endpoint: int

    @classmethod
    def from_itinerary(cls, itinerary: tuple[int, ...]) -> "LiftTreeNode":
        dual = CollatzDualCode.from_valuations(itinerary)
        return cls(
            itinerary=dual.valuations,
            m=dual.m,
            K=dual.K,
            C=dual.C,
            residue=dual.R,
            modulus=dual.modulus,
            R=dual.R,
            balanced_ternary_R=dual.balanced_ternary_R,
            endpoint=dual.endpoints[-1],
        )

    def as_dict(self) -> dict[str, object]:
        return {
            "itinerary": list(self.itinerary),
            "m": self.m,
            "K": self.K,
            "C": self.C,
            "residue": self.residue,
            "modulus": self.modulus,
            "R": self.R,
            "BT(R)": self.balanced_ternary_R,
            "canonical_endpoint": self.endpoint,
            "status": "EXACT",
        }


@dataclass(frozen=True)
class LiftTreeEdge:
    parent: tuple[int, ...]
    child: tuple[int, ...]
    next_k: int
    lift_digit: int
    child_R: int
    child_K: int
    budget_delta: str
    edge_class: LiftEdgeClass

    def as_dict(self) -> dict[str, object]:
        return {
            "parent": list(self.parent),
            "child": list(self.child),
            "next_k": self.next_k,
            "lift_digit": self.lift_digit,
            "child_R": self.child_R,
            "child_K": self.child_K,
            "budget_delta": self.budget_delta,
            "edge_class": self.edge_class.value,
            "status": "EXACT",
        }


@dataclass(frozen=True)
class LiftTree:
    max_depth: int
    k_max: int
    nodes: tuple[LiftTreeNode, ...]
    edges: tuple[LiftTreeEdge, ...]
    truncated: bool

    def zero_lift_edges(self) -> tuple[LiftTreeEdge, ...]:
        return tuple(e for e in self.edges if e.edge_class is LiftEdgeClass.ZERO_LIFT)

    def positive_lift_edges(self) -> tuple[LiftTreeEdge, ...]:
        return tuple(
            e for e in self.edges if e.edge_class is LiftEdgeClass.POSITIVE_LIFT
        )


def build_lift_tree(
    max_depth: int,
    k_max: int,
    max_nodes: int = 100_000,
) -> LiftTree:
    if isinstance(max_depth, bool) or not isinstance(max_depth, int) or max_depth < 0:
        raise ValueError("max_depth must be an integer >= 0")
    if isinstance(k_max, bool) or not isinstance(k_max, int) or k_max < 1:
        raise ValueError("k_max must be an integer >= 1")
    if isinstance(max_nodes, bool) or not isinstance(max_nodes, int) or max_nodes < 1:
        raise ValueError("max_nodes must be an integer >= 1")
    nodes: list[LiftTreeNode] = [LiftTreeNode.from_itinerary(())]
    edges: list[LiftTreeEdge] = []
    frontier = [nodes[0]]
    truncated = False
    for _depth in range(max_depth):
        next_frontier: list[LiftTreeNode] = []
        for parent in frontier:
            for k in range(1, k_max + 1):
                if len(nodes) >= max_nodes:
                    truncated = True
                    return LiftTree(
                        max_depth=max_depth,
                        k_max=k_max,
                        nodes=tuple(nodes),
                        edges=tuple(edges),
                        truncated=truncated,
                    )
                child = LiftTreeNode.from_itinerary(parent.itinerary + (k,))
                t = (child.R - parent.R) // parent.modulus
                edge_class = (
                    LiftEdgeClass.ZERO_LIFT
                    if t == 0
                    else LiftEdgeClass.POSITIVE_LIFT
                )
                budget_delta = "expanding" if k == 1 else "contracting"
                nodes.append(child)
                next_frontier.append(child)
                edges.append(
                    LiftTreeEdge(
                        parent=parent.itinerary,
                        child=child.itinerary,
                        next_k=k,
                        lift_digit=t,
                        child_R=child.R,
                        child_K=child.K,
                        budget_delta=budget_delta,
                        edge_class=edge_class,
                    )
                )
        frontier = next_frontier
    return LiftTree(
        max_depth=max_depth,
        k_max=k_max,
        nodes=tuple(nodes),
        edges=tuple(edges),
        truncated=truncated,
    )


def _exponent_period(precision: int) -> int:
    """A sufficient period for powers of 3 modulo ``2^precision``."""
    return 1 if precision <= 2 else 1 << (precision - 2)


@dataclass(frozen=True)
class DualPrecisionState:
    endpoint_residue: int
    precision: int
    m_mod: int

    def __post_init__(self) -> None:
        if self.precision < 1:
            raise ValueError("precision must be >= 1")
        modulus = 1 << self.precision
        if not 0 <= self.endpoint_residue < modulus:
            raise ValueError("endpoint residue outside precision modulus")
        if self.endpoint_residue % 2 == 0:
            raise ValueError("canonical endpoint residue must be odd")
        period = _exponent_period(self.precision)
        if not 0 <= self.m_mod < period:
            raise ValueError("m_mod outside exponent period")

    @classmethod
    def initial(cls, precision: int) -> "DualPrecisionState":
        return cls(endpoint_residue=1, precision=precision, m_mod=0)


@dataclass(frozen=True)
class DualPrecisionTransition:
    source: DualPrecisionState
    valuation: int
    lift_digit: int
    target: DualPrecisionState
    status: str = "EXACT_AT_STATED_PRECISION"


def precision_transition(
    state: DualPrecisionState,
    k: int,
) -> DualPrecisionTransition:
    """Exact paired transition when ``1 <= k < state.precision``."""
    if isinstance(k, bool) or not isinstance(k, int) or not 1 <= k < state.precision:
        raise ValueError("k must satisfy 1 <= k < available precision")
    P = state.precision
    q_modulus = 1 << (P - 1)
    q = ((3 * state.endpoint_residue + 1) // 2) % q_modulus
    digit_modulus = 1 << k
    a_for_digit = pow(3, state.m_mod + 1, digit_modulus)
    t = ((1 << (k - 1)) - q) * pow(a_for_digit, -1, digit_modulus)
    t %= digit_modulus
    a = pow(3, state.m_mod + 1, q_modulus)
    numerator = (q + a * t) % q_modulus
    divisor = 1 << (k - 1)
    if numerator % divisor:
        raise ArithmeticError("finite paired transition is not divisible")
    new_precision = P - k
    target_modulus = 1 << new_precision
    endpoint = (numerator // divisor) % target_modulus
    if endpoint % 2 == 0:
        raise ArithmeticError("finite paired transition did not preserve oddness")
    period = _exponent_period(new_precision)
    target = DualPrecisionState(
        endpoint_residue=endpoint,
        precision=new_precision,
        m_mod=(state.m_mod + 1) % period,
    )
    return DualPrecisionTransition(
        source=state,
        valuation=k,
        lift_digit=t,
        target=target,
    )


def follow_dual_precision(
    valuations: tuple[int, ...],
    precision: int,
) -> tuple[tuple[int, ...], DualPrecisionState]:
    state = DualPrecisionState.initial(precision)
    digits: list[int] = []
    for k in valuations:
        transition = precision_transition(state, k)
        digits.append(transition.lift_digit)
        state = transition.target
    return tuple(digits), state


def precision_agrees_with_exact(
    valuations: tuple[int, ...],
    precision: int,
) -> bool:
    """Cross-check the bounded model against exact dual coding."""
    try:
        digits, state = follow_dual_precision(valuations, precision)
    except ValueError:
        return False
    exact = CollatzDualCode.from_valuations(valuations)
    return (
        digits == exact.lift_digits
        and state.endpoint_residue
        == exact.endpoints[-1] % (1 << state.precision)
    )
