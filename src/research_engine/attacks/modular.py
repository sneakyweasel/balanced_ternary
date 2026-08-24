"""Modular forcing of affine images. A residue law is not a live-set theorem."""

from __future__ import annotations

from research_engine.algebra.lattices import vector_gcd
from research_engine.attacks.result import AttackContext, AttackResult, AttackStatus
from research_engine.core.affine_system import AffineSystem
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import ClaimKind, SearchScope


def coordinate_forcing_gcds(system: AffineSystem) -> tuple[int, ...]:
    """``g_i = gcd(A_{i,*}, (b_u)_i)``. If ``g_i>1`` then image ``i`` is ``0 mod g_i``."""
    out: list[int] = []
    for i in range(system.dimension):
        entries = list(system.A[i])
        for translation in system.translations.values():
            entries.append(translation[i])
        out.append(vector_gcd(entries))
    return tuple(out)


class ModularInvariantAttack:
    name = "modular"

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
                claim="modular forcing needs an AffineSystem; a live-slice census is not a residue law",
            )
        gcds = coordinate_forcing_gcds(affine)
        certificates = tuple(
            {"coordinate": i, "gcd": g, "image_residue": 0}
            for i, g in enumerate(gcds)
            if g > 1
        )
        identically_zero = tuple(i for i, g in enumerate(gcds) if g == 0)
        if certificates or identically_zero:
            parts = [
                f"coordinate {c['coordinate']} ≡ 0 (mod {c['gcd']})" for c in certificates
            ]
            if identically_zero:
                parts.append(f"coordinates {identically_zero} identically 0")
            claim = (
                "all affine images satisfy "
                + "; ".join(parts)
                + ". This is a map law, not infinitude of LIVE"
            )
            return AttackResult(
                name=self.name,
                status=AttackStatus.SUPPORTED,
                kind=ClaimKind.REACHABLE,
                scope=SearchScope.EXACT,
                claim=claim,
                evidence={"forcing_gcds": gcds, "moduli_requested": context.moduli},
                certificates=certificates + tuple({"coordinate": i, "identically_zero": True} for i in identically_zero),
                recommended_next_attacks=("reconnaissance", "functional"),
            )
        return AttackResult(
            name=self.name,
            status=AttackStatus.OBSERVATION,
            kind=ClaimKind.REACHABLE,
            scope=SearchScope.EXACT,
            claim="no coordinate of Ax+b_u is forced to a nontrivial residue class",
            evidence={"forcing_gcds": gcds, "moduli_requested": context.moduli},
            recommended_next_attacks=("functional", "block"),
        )
