"""Exact compatibility of Collatz exponent-code coordinates.

The four exposed coordinates are the refined 2-adic realizer ``R``, Kramer's
3-adic endpoint representative ``M``, the balanced-ternary representation of
``R``, and the exact real drift powers ``(3^m, 2^K)``.  All are deterministic
functions of the retained exponent prefix.

The older nested-cylinder helpers remain available at the end of this module.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from collatz.cylinders import belongs_to_cylinder, parse_ks
from collatz.dual_code import CollatzDualCode
from collatz.endpoint_3adic import (
    KramerEndpoint,
    endpoint_residue_rate,
    real_drift,
    start_residue_rate,
)
from collatz.features import BalancedTernaryFeatures
from collatz.min_realizer import min_realizer, nested_realizers


@dataclass(frozen=True)
class ExponentCodeDiagnostic:
    """Kramer's 2-3-infinity diagnostic plus this project's refined data."""

    valuations: tuple[int, ...]
    m: int
    K: int
    C: int
    R: int
    r: int
    M: int
    balanced_ternary_R: str
    lift_digits: tuple[int, ...]
    canonical_endpoint: int
    three_power: int
    two_power: int
    d: float
    rho_r: float
    rho_M: float

    @classmethod
    def from_valuations(
        cls, valuations: tuple[int, ...] | list[int] | str
    ) -> "ExponentCodeDiagnostic":
        dual = CollatzDualCode.from_valuations(valuations)
        return cls.from_dual_code(dual)

    @classmethod
    def from_dual_code(cls, dual: CollatzDualCode) -> "ExponentCodeDiagnostic":
        """Construct from the project's authoritative exact dual code."""
        if not isinstance(dual, CollatzDualCode) or not dual.validates():
            raise ValueError("dual must be a valid CollatzDualCode")
        endpoint = KramerEndpoint.from_valuations(dual.valuations)
        r = 0 if dual.m == 0 else dual.R % (1 << dual.K)
        diagnostic = cls(
            valuations=dual.valuations,
            m=dual.m,
            K=dual.K,
            C=dual.C,
            R=dual.R,
            r=r,
            M=endpoint.M,
            balanced_ternary_R=dual.balanced_ternary_R,
            lift_digits=dual.lift_digits,
            canonical_endpoint=dual.endpoints[-1],
            three_power=3**dual.m,
            two_power=1 << dual.K,
            d=real_drift(dual.K, dual.m),
            rho_r=start_residue_rate(r, dual.m),
            rho_M=endpoint_residue_rate(endpoint.M, dual.m),
        )
        if not diagnostic.validates():
            raise ArithmeticError("exponent-code diagnostic failed validation")
        return diagnostic

    @property
    def exact_drift(self) -> tuple[int, int]:
        """The exact homogeneous pair ``(3^m, 2^K)``."""
        return self.three_power, self.two_power

    def validates(self) -> bool:
        try:
            dual = CollatzDualCode.from_valuations(self.valuations)
            endpoint = KramerEndpoint.from_valuations(self.valuations)
        except (ArithmeticError, TypeError, ValueError):
            return False
        expected_r = 0 if self.m == 0 else self.R % (1 << self.K)
        return (
            self.m == dual.m
            and self.K == dual.K
            and self.C == dual.C
            and self.R == dual.R
            and self.r == expected_r
            and self.M == endpoint.M
            and self.balanced_ternary_R == dual.balanced_ternary_R
            and self.lift_digits == dual.lift_digits
            and self.canonical_endpoint == dual.endpoints[-1]
            and self.three_power == 3**self.m
            and self.two_power == 1 << self.K
            and self.three_power * self.R + self.C
            == self.two_power * self.canonical_endpoint
            and endpoint.contains(self.canonical_endpoint)
            and self.d == real_drift(self.K, self.m)
            and self.rho_r == start_residue_rate(self.r, self.m)
            and self.rho_M == endpoint_residue_rate(self.M, self.m)
        )

    def as_dict(self) -> dict[str, object]:
        return {
            "valuations": list(self.valuations),
            "m": self.m,
            "K": self.K,
            "C": self.C,
            "R": self.R,
            "r": self.r,
            "M": self.M,
            "BT(R)": self.balanced_ternary_R,
            "lift_digits": list(self.lift_digits),
            "canonical_endpoint": self.canonical_endpoint,
            "exact_drift": [self.three_power, self.two_power],
            "d": self.d,
            "rho_r": self.rho_r,
            "rho_M": self.rho_M,
            "floating_fields": ["d", "rho_r", "rho_M"],
            "status": "EXACT except labeled floating estimates",
        }


@dataclass(frozen=True)
class CompatibilityState:
    """Immutable exact state for one finite exponent prefix."""

    valuations: tuple[int, ...]
    m: int
    K: int
    C: int
    R: int
    r: int
    M: int
    balanced_ternary_R: str
    features: BalancedTernaryFeatures
    lift_digits: tuple[int, ...]
    canonical_endpoint: int
    three_power: int
    two_power: int

    @classmethod
    def from_valuations(
        cls, valuations: tuple[int, ...] | list[int] | str
    ) -> "CompatibilityState":
        dual = CollatzDualCode.from_valuations(valuations)
        return cls.from_dual_code(dual)

    @classmethod
    def from_dual_code(cls, dual: CollatzDualCode) -> "CompatibilityState":
        """Construct without introducing an alternative arithmetic path."""
        if not isinstance(dual, CollatzDualCode) or not dual.validates():
            raise ValueError("dual must be a valid CollatzDualCode")
        diagnostic = ExponentCodeDiagnostic.from_dual_code(dual)
        state = cls(
            valuations=dual.valuations,
            m=dual.m,
            K=dual.K,
            C=dual.C,
            R=dual.R,
            r=diagnostic.r,
            M=diagnostic.M,
            balanced_ternary_R=dual.balanced_ternary_R,
            features=dual.features,
            lift_digits=dual.lift_digits,
            canonical_endpoint=dual.endpoints[-1],
            three_power=diagnostic.three_power,
            two_power=diagnostic.two_power,
        )
        if not state.validates():
            raise ArithmeticError("compatibility state failed validation")
        return state

    @property
    def exact_drift(self) -> tuple[int, int]:
        return self.three_power, self.two_power

    def diagnostic(self) -> ExponentCodeDiagnostic:
        return ExponentCodeDiagnostic.from_valuations(self.valuations)

    def extend(self, valuation: int) -> "CompatibilityState":
        if (
            isinstance(valuation, bool)
            or not isinstance(valuation, int)
            or valuation < 1
        ):
            raise ValueError("valuation must be an integer >= 1")
        return CompatibilityState.from_valuations(self.valuations + (valuation,))

    def extensions(self, k_max: int) -> tuple["CompatibilityState", ...]:
        if isinstance(k_max, bool) or not isinstance(k_max, int) or k_max < 1:
            raise ValueError("k_max must be an integer >= 1")
        return tuple(self.extend(k) for k in range(1, k_max + 1))

    def validates(self) -> bool:
        try:
            dual = CollatzDualCode.from_valuations(self.valuations)
            diagnostic = ExponentCodeDiagnostic.from_valuations(self.valuations)
        except (ArithmeticError, TypeError, ValueError):
            return False
        return (
            dual.validates()
            and self.m == dual.m
            and self.K == dual.K
            and self.C == dual.C
            and self.R == dual.R
            and self.r == diagnostic.r
            and self.M == diagnostic.M
            and self.balanced_ternary_R == dual.balanced_ternary_R
            and self.features == dual.features
            and self.lift_digits == dual.lift_digits
            and self.canonical_endpoint == dual.endpoints[-1]
            and self.exact_drift == diagnostic.exact_drift
            and belongs_to_cylinder(self.R, self.valuations)
            and self.three_power * self.R + self.C
            == self.two_power * self.canonical_endpoint
            and self.canonical_endpoint % self.three_power
            == self.M % self.three_power
        )

    def as_dict(self) -> dict[str, object]:
        data = self.diagnostic().as_dict()
        data["features"] = self.features.as_dict()
        return data


@dataclass(frozen=True)
class CompatibilityEdge:
    source: tuple[int, ...]
    target: tuple[int, ...]
    valuation: int
    lift_digit: int


@dataclass(frozen=True)
class CompatibilityGraph:
    root: CompatibilityState
    nodes: tuple[CompatibilityState, ...]
    edges: tuple[CompatibilityEdge, ...]
    max_depth: int
    k_max: int

    def validates(self) -> bool:
        by_word = {state.valuations: state for state in self.nodes}
        if len(by_word) != len(self.nodes) or self.root.valuations not in by_word:
            return False
        if any(not state.validates() for state in self.nodes):
            return False
        for edge in self.edges:
            source = by_word.get(edge.source)
            target = by_word.get(edge.target)
            if source is None or target is None:
                return False
            expected = source.extend(edge.valuation)
            if target != expected or target.lift_digits[-1] != edge.lift_digit:
                return False
        return True


def build_compatibility_graph(
    max_depth: int,
    k_max: int,
    root: tuple[int, ...] | list[int] | str = (),
) -> CompatibilityGraph:
    """Build the finite prefix tree through exact state extensions."""
    if isinstance(max_depth, bool) or not isinstance(max_depth, int) or max_depth < 0:
        raise ValueError("max_depth must be an integer >= 0")
    if isinstance(k_max, bool) or not isinstance(k_max, int) or k_max < 1:
        raise ValueError("k_max must be an integer >= 1")
    root_state = CompatibilityState.from_valuations(root)
    nodes = [root_state]
    edges: list[CompatibilityEdge] = []
    frontier = [root_state]
    for _ in range(max_depth):
        next_frontier: list[CompatibilityState] = []
        for source in frontier:
            for target in source.extensions(k_max):
                nodes.append(target)
                next_frontier.append(target)
                edges.append(
                    CompatibilityEdge(
                        source=source.valuations,
                        target=target.valuations,
                        valuation=target.valuations[-1],
                        lift_digit=target.lift_digits[-1],
                    )
                )
        frontier = next_frontier
    graph = CompatibilityGraph(
        root=root_state,
        nodes=tuple(nodes),
        edges=tuple(edges),
        max_depth=max_depth,
        k_max=k_max,
    )
    if not graph.validates():
        raise ArithmeticError("compatibility graph failed validation")
    return graph


class RealizabilityClass(str, Enum):
    FINITELY_TWO_ADICALLY_REALIZABLE = "FINITELY_2-ADICALLY_REALIZABLE"
    TWO_ADICALLY_REALIZABLE = "2-ADICALLY_REALIZABLE"
    REALIZED_BY_A_POSITIVE_INTEGER = "REALIZED_BY_A_POSITIVE_INTEGER"
    REALIZED_BY_A_POSITIVE_INFINITE_TRAJECTORY = (
        "REALIZED_BY_A_POSITIVE_INFINITE_COLLATZ_TRAJECTORY"
    )


def observed_nonconstant_monotone(r_seq: tuple[int, ...]) -> bool:
    """Whether a finite sample is monotone and has at least one increase.

    This finite observation is not evidence that the infinite sequence is
    unbounded. The implication ``R_m -> inf => no positive integer realizer``
    is **PROVED** independently.
    """
    if len(r_seq) < 2:
        return False
    return r_seq[-1] > r_seq[0] and r_seq == tuple(sorted(r_seq))


def positive_integer_would_bound_R(n: int, r_seq: tuple[int, ...]) -> bool:
    """If ``n`` realises every prefix, then ``n >= max R_m``."""
    if not r_seq:
        return n >= 1
    return n >= max(r_seq)


@dataclass(frozen=True)
class NestedCylinderReport:
    ks: tuple[int, ...]
    realizers: tuple[int, ...]
    monotone: bool
    strictly_increasing_in_sample: bool
    constant_in_sample: bool
    class_labels: tuple[str, ...]
    status: str

    def format(self) -> str:
        return (
            f"Nested cylinders  ks={self.ks}\n"
            f"R_m={self.realizers}\n"
            f"monotone={str(self.monotone).lower()}  "
            f"[PROVED for leftover Q=1]\n"
            f"strictly_increasing_in_sample="
            f"{str(self.strictly_increasing_in_sample).lower()}  "
            f"[COMPUTATIONAL on this prefix]\n"
            f"constant_in_sample={str(self.constant_in_sample).lower()}\n"
            f"classes: {', '.join(self.class_labels)}\n"
            f"status: {self.status}\n"
            "If R_m -> infinity, no finite positive integer realises the "
            "entire infinite itinerary. [PROVED]\n"
        )


def nested_cylinder_report(ks: tuple[int, ...] | str | list[int]) -> NestedCylinderReport:
    ks = parse_ks(ks)
    rs = nested_realizers(ks)
    monotone = all(rs[i] <= rs[i + 1] for i in range(len(rs) - 1))
    strict = all(rs[i] < rs[i + 1] for i in range(len(rs) - 1)) if len(rs) > 1 else False
    constant = all(r == rs[0] for r in rs)
    labels = (
        RealizabilityClass.FINITELY_TWO_ADICALLY_REALIZABLE.value,
        RealizabilityClass.TWO_ADICALLY_REALIZABLE.value,
    )
    return NestedCylinderReport(
        ks=ks,
        realizers=rs,
        monotone=monotone,
        strictly_increasing_in_sample=strict,
        constant_in_sample=constant,
        class_labels=labels,
        status="EXACT residues; finite constancy is COMPUTATIONAL",
    )


def child_realizer_delta(parent: tuple[int, ...], j: int) -> tuple[int, int, int]:
    """Return ``(R_parent, R_child, t)`` with ``R_child = R_parent + t * 2^{K_p+1}``."""
    parent = parse_ks(parent)
    if isinstance(j, bool) or not isinstance(j, int) or j < 1:
        raise ValueError(f"j must be an integer >= 1, got {j!r}")
    r_p = min_realizer(parent)
    r_c = min_realizer(parent + (j,))
    mod = 1 << (sum(parent) + 1)
    if (r_c - r_p) % mod != 0:
        raise ArithmeticError("child residue does not lift the parent")
    t = (r_c - r_p) // mod
    return r_p, r_c, t
