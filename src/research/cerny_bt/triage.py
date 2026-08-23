"""Exact Phase-0 tests for a transition-closed residual quotient.

Finite-horizon ``≡_r`` is not a transition congruence:
``p ≡_r q`` yields only ``D_a p ≡_{r-1} D_a q``. The coarsest
transition congruence contained in ``≡_r`` for ``r ≥ 1`` is

    p ≈_r q  iff  for every trit word u,  D_u p ≡_r D_u q.

On ``Z[x]`` that relation is full Mealy equivalence, hence raw
polynomial equality. Affine residual closures are finite; every
polynomial of degree at least two has infinitely many distinct
sections by leading-coefficient growth.

No reset words, ranks, pair compression, or Černý bounds are computed.
Bounded ``≈_r`` checks are validation, not proofs.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Iterable

from bt.calculus.myhill_nerode import distinguish, equiv_recursive
from bt.calculus.residual import TRITS, delta, residual_along
from bt.calculus.section import IntPoly, parse_poly
from bt.normtheory.rewrite import balanced_divmod

AFFINE_SPECS: tuple[str, ...] = (
    "0",
    "1",
    "-1",
    "2",
    "x",
    "x+1",
    "x-1",
    "2x+1",
    "2x-1",
    "-x",
    "3x+1",
    "-2x+1",
)

NONLINEAR_SPECS: tuple[str, ...] = ("x^2", "x^3", "2x^2+1")

_CLOSURE_CAP = 32


def _require_horizon(r: int) -> int:
    if isinstance(r, bool) or not isinstance(r, int) or r < 0:
        raise ValueError("horizon must be a nonnegative int")
    return r


def section_leading_coefficient(f: IntPoly, depth: int) -> int:
    """``LC(f) * 3^{depth * (deg f - 1)}`` for ``deg f ≥ 1``."""

    if isinstance(depth, bool) or not isinstance(depth, int) or depth < 0:
        raise ValueError("depth must be a nonnegative int")
    if f.degree <= 0:
        return f.lc()
    return f.lc() * 3 ** (depth * (f.degree - 1))


def observed_leading_coefficient(f: IntPoly, word: tuple[int, ...]) -> int:
    return residual_along(f, word).lc()


def affine_intercept_bound(slope: int, intercept: int) -> int:
    """Every residual of ``slope * x + intercept`` stays inside this bound."""

    return max(abs(slope), abs(intercept))


def affine_step(slope: int, intercept: int, trit: int) -> int:
    """Intercept of ``D_a(slope * x + intercept)``; the slope is invariant."""

    if trit not in TRITS:
        raise ValueError(f"input must be a trit, got {trit}")
    _residue, quotient = balanced_divmod(intercept + trit * slope)
    return quotient


def affine_closure(slope: int, intercept: int) -> frozenset[int]:
    """Exact residual intercepts of ``slope * x + intercept``."""

    bound = affine_intercept_bound(slope, intercept)
    seen = {intercept}
    frontier = [intercept]
    while frontier:
        nxt: list[int] = []
        for value in frontier:
            for trit in TRITS:
                child = affine_step(slope, value, trit)
                if abs(child) > bound:
                    raise RuntimeError("affine intercept escaped the proved bound")
                if child not in seen:
                    seen.add(child)
                    nxt.append(child)
        frontier = nxt
    return frozenset(seen)


@dataclass(frozen=True)
class ClosureRecord:
    polynomial: str
    degree: int
    finite: bool
    state_count: int | None
    states: tuple[str, ...]
    truncated: bool
    leading_coefficients: tuple[int, ...]


def residual_closure(f: IntPoly, max_states: int = _CLOSURE_CAP) -> ClosureRecord:
    """Enumerate residual polynomials until the set closes or hits ``max_states``."""

    if isinstance(max_states, bool) or not isinstance(max_states, int) or max_states < 1:
        raise ValueError("max_states must be a positive int")
    seen: dict[tuple[int, ...], IntPoly] = {f.coeffs: f}
    frontier = [f]
    truncated = False
    while frontier and not truncated:
        nxt: list[IntPoly] = []
        for poly in frontier:
            for trit in TRITS:
                child = delta(poly, trit)
                if child.coeffs in seen:
                    continue
                if len(seen) >= max_states:
                    truncated = True
                    break
                seen[child.coeffs] = child
                nxt.append(child)
            if truncated:
                break
        frontier = nxt
    states = tuple(poly.render() for poly in seen.values())
    finite = (not truncated) and f.degree <= 1
    return ClosureRecord(
        polynomial=f.render(),
        degree=f.degree,
        finite=finite,
        state_count=len(seen) if not truncated else None,
        states=states,
        truncated=truncated,
        leading_coefficients=tuple(section_leading_coefficient(f, depth) for depth in range(4)),
    )


def approx_r(
    left: IntPoly,
    right: IntPoly,
    r: int,
    prefix_bound: int,
) -> bool:
    """Bounded check of ``≈_r``: every prefix of length ``≤ prefix_bound``."""

    r = _require_horizon(r)
    if isinstance(prefix_bound, bool) or not isinstance(prefix_bound, int) or prefix_bound < 0:
        raise ValueError("prefix_bound must be a nonnegative int")
    for length in range(prefix_bound + 1):
        for word in product(TRITS, repeat=length):
            if not equiv_recursive(residual_along(left, word), residual_along(right, word), r):
                return False
    return True


def horizon_not_congruence_witness() -> dict[str, object]:
    """Smallest pair with ``p ≡_1 q`` but ``D_0 p ≢_1 D_0 q``."""

    left = parse_poly("x")
    right = parse_poly("x+3")
    child_left = delta(left, 0)
    child_right = delta(right, 0)
    return {
        "p": left.render(),
        "q": right.render(),
        "horizon": 1,
        "equiv_at_horizon": equiv_recursive(left, right, 1),
        "letter": 0,
        "D_p": child_left.render(),
        "D_q": child_right.render(),
        "children_equiv_at_same_horizon": equiv_recursive(child_left, child_right, 1),
        "approx_r_on_prefixes": approx_r(left, right, 1, prefix_bound=1),
        "shortest_distinction": list(distinguish(left, right, 2) or ()),
    }


def _affine_coeffs(f: IntPoly) -> tuple[int, int]:
    if f.degree > 1:
        raise ValueError("expected an affine polynomial")
    return f.coefficient(1), f.coefficient(0)


def affine_family_record(spec: str) -> dict[str, object]:
    f = parse_poly(spec)
    slope, intercept = _affine_coeffs(f)
    intercepts = affine_closure(slope, intercept)
    closure = residual_closure(f)
    states = {parse_poly(name) for name in closure.states}
    return {
        "family": spec,
        "polynomial": f.render(),
        "degree": f.degree,
        "slope": slope,
        "intercept_bound": affine_intercept_bound(slope, intercept),
        "intercepts": sorted(intercepts),
        "state_count": closure.state_count,
        "states": list(closure.states),
        "finite": closure.finite,
        "transition_closed": all(
            delta(state, trit) in states for state in states for trit in TRITS
        ),
    }


def nonlinear_family_record(spec: str) -> dict[str, object]:
    f = parse_poly(spec)
    formula = tuple(section_leading_coefficient(f, depth) for depth in range(4))
    observed = tuple(
        observed_leading_coefficient(f, (0,) * depth) for depth in range(4)
    )
    return {
        "family": spec,
        "polynomial": f.render(),
        "degree": f.degree,
        "finite": False,
        "leading_formula": list(formula),
        "leading_observed": list(observed),
        "distinct_leading_coefficients": len(set(formula)) == 4,
    }


def approx_equals_raw_on_sample(
    specs: Iterable[str] = AFFINE_SPECS,
    *,
    r: int = 1,
    prefix_bound: int = 2,
) -> bool:
    """Distinct affine residuals fail the bounded ``≈_r`` check for ``r ≥ 1``."""

    r = _require_horizon(r)
    if r == 0:
        return True
    for spec in specs:
        f = parse_poly(spec)
        if f.degree > 1:
            continue
        closure = residual_closure(f)
        states = [parse_poly(name) for name in closure.states]
        for i, left in enumerate(states):
            for right in states[i:]:
                expected = left.coeffs == right.coeffs
                if approx_r(left, right, r, prefix_bound) != expected:
                    return False
    return True


def triage_report() -> dict[str, object]:
    """Complete bounded report. The gate does not promote synchronization."""

    affine = tuple(affine_family_record(spec) for spec in AFFINE_SPECS)
    nonlinear = tuple(nonlinear_family_record(spec) for spec in NONLINEAR_SPECS)
    witness = horizon_not_congruence_witness()
    return {
        "affine_families": list(affine),
        "nonlinear_families": list(nonlinear),
        "horizon_not_congruence": witness,
        "approx_equals_raw_on_sample": approx_equals_raw_on_sample(),
        "canonical_nonaffine_finite_quotient": False,
        "gate": "CLOSE",
        "classification": "REPARAMETERIZATION",
    }
