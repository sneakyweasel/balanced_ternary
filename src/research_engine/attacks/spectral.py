"""Companion classification of A. Expansion is not live infinitude."""

from __future__ import annotations

from research_engine.algebra.lattices import characteristic_polynomial
from research_engine.algebra.spectral import (
    cubic_roots,
    exact_pisot_cubic_certificate,
    is_monic_cubic,
)
from research_engine.attacks.result import AttackContext, AttackResult, AttackStatus
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import ClaimKind, SearchScope


class SpectralClassificationAttack:
    """Classify the companion of ``A``. Floats never decide status."""

    name = "spectral"

    def applicable(self, spec: ProblemSpec, context: AttackContext) -> bool:
        del spec
        return context.affine is not None

    def run(self, spec: ProblemSpec, context: AttackContext) -> AttackResult:
        del spec
        affine = context.affine
        if affine is None:
            return AttackResult(
                name=self.name,
                status=AttackStatus.INAPPLICABLE,
                kind=ClaimKind.REACHABLE,
                scope=SearchScope.BOUNDED,
                claim="spectral classification needs an AffineSystem; floats are not an acceptance predicate",
            )
        poly = characteristic_polynomial(affine.A)
        evidence: dict[str, object] = {
            "characteristic_polynomial": poly,
            "floats_are_labels_only": True,
        }
        if not is_monic_cubic(poly):
            return AttackResult(
                name=self.name,
                status=AttackStatus.OBSERVATION,
                kind=ClaimKind.REACHABLE,
                scope=SearchScope.EXACT,
                claim=(
                    "characteristic polynomial of A is not a monic cubic; "
                    "companion classification is not a Pisot certificate. "
                    "This is a map law, not live infinitude"
                ),
                evidence=evidence,
                recommended_next_attacks=("modular", "block"),
            )
        cert = exact_pisot_cubic_certificate(poly)
        evidence["certificate"] = cert
        evidence["root_moduli_labels"] = tuple(abs(z) for z in cubic_roots(poly))
        decisive = bool(cert["pisot"] or cert["perron_non_pisot"])
        if cert["pisot"]:
            label = "Pisot"
        elif cert["perron_non_pisot"]:
            label = "Perron non-Pisot"
        else:
            label = "not a decisive Pisot/Perron cubic"
        claim = (
            f"companion of A is an exact {label} cubic; "
            "this classifies the linear map, not live infinitude. "
            "Float root labels are not used as status"
        )
        if decisive:
            return AttackResult(
                name=self.name,
                status=AttackStatus.SUPPORTED,
                kind=ClaimKind.REACHABLE,
                scope=SearchScope.EXACT,
                claim=claim,
                evidence=evidence,
                certificates=(
                    {
                        "pisot": cert["pisot"],
                        "perron_non_pisot": cert["perron_non_pisot"],
                        "characteristic_polynomial": poly,
                    },
                ),
                recommended_next_attacks=("block", "reconnaissance"),
            )
        return AttackResult(
            name=self.name,
            status=AttackStatus.OBSERVATION,
            kind=ClaimKind.REACHABLE,
            scope=SearchScope.EXACT,
            claim=claim,
            evidence=evidence,
            recommended_next_attacks=("modular", "block"),
        )
