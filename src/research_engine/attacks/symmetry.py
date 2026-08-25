"""Lightweight exact symmetry verification. Not a group engine."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from research_engine.attacks.result import AttackContext, AttackResult, AttackStatus, inapplicable
from research_engine.core.observation import has_output, observe
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import CertificateKind, ClaimKind, SearchScope


@dataclass(frozen=True)
class SymmetryCandidate:
    name: str
    kind: str
    params: tuple[int, ...] = ()
    control_kind: str = "identity"


@dataclass(frozen=True)
class SymmetryResult:
    transformation: str
    verified: bool
    state_action: str
    observation_preservation: bool
    domain_size: int
    origin_reachable_extra_classes: int
    certificate_kind: CertificateKind | None
    counterexample: tuple[Any, ...] | None = None


def apply_state(candidate: SymmetryCandidate, state: Any) -> Any:
    if not isinstance(state, tuple) or not state:
        raise TypeError("symmetry actions require a nonempty integer tuple state")
    head = int(state[0])
    tail = state[1:]
    if candidate.kind == "sign":
        return (-head,) + tuple(-int(item) for item in tail)
    if candidate.kind == "translate":
        return (head + candidate.params[0],) + tail
    if candidate.kind == "affine":
        scale, shift = candidate.params
        return (scale * head + shift,) + tail
    raise ValueError(f"unknown symmetry kind {candidate.kind!r}")


def apply_control(candidate: SymmetryCandidate, control: Any) -> Any:
    if candidate.control_kind == "identity":
        return control
    if candidate.control_kind == "sign" and isinstance(control, int):
        return -control
    if (
        candidate.control_kind == "sign"
        and isinstance(control, tuple)
        and all(isinstance(item, int) for item in control)
    ):
        return tuple(-int(item) for item in control)
    return control


def _domain(spec: ProblemSpec, context: AttackContext) -> tuple[Any, ...]:
    if context.symmetry_domain is not None:
        return tuple(sorted(context.symmetry_domain, key=repr))
    if context.candidate_region is not None:
        return tuple(sorted(context.candidate_region, key=repr))
    return (spec.canonicalize(spec.initial_state),)


def verify_symmetry(
    spec: ProblemSpec,
    candidate: SymmetryCandidate,
    context: AttackContext,
) -> SymmetryResult:
    phase = spec.initial_phase()
    domain = _domain(spec, context)
    observe_enabled = has_output(spec)
    reachable = set(context.candidate_region) if context.candidate_region is not None else set()
    extra_classes = 0
    for state in domain:
        src = spec.canonicalize(state)
        try:
            image = spec.canonicalize(apply_state(candidate, src))
        except (TypeError, ValueError) as exc:
            return SymmetryResult(
                transformation=candidate.name,
                verified=False,
                state_action=candidate.kind,
                observation_preservation=False,
                domain_size=len(domain),
                origin_reachable_extra_classes=0,
                certificate_kind=CertificateKind.EXACT_COUNTEREXAMPLE,
                counterexample=("action", src, str(exc)),
            )
        if reachable and src in reachable and image not in reachable:
            extra_classes += 1
        if candidate.kind == "congruence":
            continue
        for control in spec.legal_controls(src, phase):
            mapped_control = apply_control(candidate, control)
            nxt = spec.canonicalize(spec.transition(src, control, phase))
            try:
                mapped_src = spec.canonicalize(apply_state(candidate, src))
                expected = spec.canonicalize(apply_state(candidate, nxt))
            except (TypeError, ValueError) as exc:
                return SymmetryResult(
                    transformation=candidate.name,
                    verified=False,
                    state_action=candidate.kind,
                    observation_preservation=False,
                    domain_size=len(domain),
                    origin_reachable_extra_classes=extra_classes,
                    certificate_kind=CertificateKind.EXACT_COUNTEREXAMPLE,
                    counterexample=("state", src, control, str(exc)),
                )
            legal_mapped = spec.legal_controls(mapped_src, phase)
            if mapped_control not in legal_mapped:
                return SymmetryResult(
                    transformation=candidate.name,
                    verified=False,
                    state_action=candidate.kind,
                    observation_preservation=False,
                    domain_size=len(domain),
                    origin_reachable_extra_classes=extra_classes,
                    certificate_kind=CertificateKind.EXACT_COUNTEREXAMPLE,
                    counterexample=("illegal", src, control, mapped_control),
                )
            actual = spec.canonicalize(spec.transition(mapped_src, mapped_control, phase))
            if actual != expected:
                return SymmetryResult(
                    transformation=candidate.name,
                    verified=False,
                    state_action=candidate.kind,
                    observation_preservation=False,
                    domain_size=len(domain),
                    origin_reachable_extra_classes=extra_classes,
                    certificate_kind=CertificateKind.EXACT_COUNTEREXAMPLE,
                    counterexample=("transition", src, control, actual, expected),
                )
            if observe_enabled:
                out = observe(spec, src, control, phase)
                mapped_out = observe(spec, mapped_src, mapped_control, phase)
                if candidate.kind in {"translate", "affine", "congruence"}:
                    preserved = mapped_out == out
                elif candidate.control_kind == "sign" and isinstance(out, int) and isinstance(mapped_out, int):
                    preserved = mapped_out == -out
                else:
                    preserved = mapped_out == out
                if not preserved:
                    return SymmetryResult(
                        transformation=candidate.name,
                        verified=False,
                        state_action=candidate.kind,
                        observation_preservation=False,
                        domain_size=len(domain),
                        origin_reachable_extra_classes=extra_classes,
                        certificate_kind=CertificateKind.EXACT_COUNTEREXAMPLE,
                        counterexample=("observation", src, control, out, mapped_out),
                    )
    if candidate.kind == "congruence":
        modulus = candidate.params[0]
        for left in domain:
            for right in domain:
                if int(left[0]) % modulus != int(right[0]) % modulus:
                    continue
                for control in spec.legal_controls(left, phase):
                    if control not in spec.legal_controls(right, phase):
                        continue
                    nxt_l = spec.canonicalize(spec.transition(left, control, phase))
                    nxt_r = spec.canonicalize(spec.transition(right, control, phase))
                    if int(nxt_l[0]) % modulus != int(nxt_r[0]) % modulus:
                        return SymmetryResult(
                            transformation=candidate.name,
                            verified=False,
                            state_action=candidate.kind,
                            observation_preservation=False,
                            domain_size=len(domain),
                            origin_reachable_extra_classes=0,
                            certificate_kind=CertificateKind.EXACT_COUNTEREXAMPLE,
                            counterexample=("congruence", left, right, control),
                        )
                    if observe_enabled and observe(spec, left, control, phase) != observe(
                        spec, right, control, phase
                    ):
                        return SymmetryResult(
                            transformation=candidate.name,
                            verified=False,
                            state_action=candidate.kind,
                            observation_preservation=False,
                            domain_size=len(domain),
                            origin_reachable_extra_classes=0,
                            certificate_kind=CertificateKind.EXACT_COUNTEREXAMPLE,
                            counterexample=("congruence_out", left, right, control),
                        )
    return SymmetryResult(
        transformation=candidate.name,
        verified=True,
        state_action=candidate.kind,
        observation_preservation=True,
        domain_size=len(domain),
        origin_reachable_extra_classes=extra_classes,
        certificate_kind=CertificateKind.EXACT_CLOSURE,
    )


class SymmetryAttack:
    name = "symmetry"

    def applicable(self, spec: ProblemSpec, context: AttackContext) -> bool:
        del spec
        return bool(context.symmetry_candidates)

    def run(self, spec: ProblemSpec, context: AttackContext) -> AttackResult:
        candidates = context.symmetry_candidates
        if not candidates:
            return inapplicable(self.name, "no symmetry candidates", ClaimKind.REACHABLE)
        reports: list[SymmetryResult] = []
        for item in candidates:
            candidate = item if isinstance(item, SymmetryCandidate) else _coerce(item)
            reports.append(verify_symmetry(spec, candidate, context))
        failed = next((item for item in reports if not item.verified), None)
        if failed is not None:
            return AttackResult(
                name=self.name,
                status=AttackStatus.REFUTED,
                kind=ClaimKind.REACHABLE,
                scope=SearchScope.EXACT,
                claim=f"symmetry {failed.transformation} is not verified",
                evidence={"count": len(reports), "extra_classes": failed.origin_reachable_extra_classes},
                counterexamples=(failed.counterexample,),
                certificates=tuple(reports),
                certificate_kind=CertificateKind.EXACT_COUNTEREXAMPLE,
            )
        extra = sum(item.origin_reachable_extra_classes for item in reports)
        return AttackResult(
            name=self.name,
            status=AttackStatus.SUPPORTED,
            kind=ClaimKind.REACHABLE,
            scope=SearchScope.EXACT,
            claim=(
                f"{len(reports)} candidate symmetries verified; "
                f"{extra} images lie outside the origin-reachable set"
            ),
            evidence={"count": len(reports), "extra_classes": extra},
            certificates=tuple(reports),
            certificate_kind=CertificateKind.EXACT_CLOSURE,
        )


def _coerce(item: Any) -> SymmetryCandidate:
    if isinstance(item, dict):
        return SymmetryCandidate(
            name=str(item.get("name", item.get("kind", "candidate"))),
            kind=str(item["kind"]),
            params=tuple(item.get("params", ())),
            control_kind=str(item.get("control_kind", "identity")),
        )
    raise TypeError(f"cannot coerce {type(item).__name__} to SymmetryCandidate")
