"""Parameter-domain certification of a reconstructed affine family.

A sample-supported family is not a Z-theorem. Mere divisibility is not
exact parameter selection.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from enum import Enum
from types import MappingProxyType
from typing import Any

from research_engine.attacks.piecewise_affine import (
    DEFAULT_FALSIFY_WINDOW,
    DEFAULT_SAMPLE_WINDOW,
    _collect_samples,
    _eval_map,
    _is_power_of_base,
)
from research_engine.attacks.result import AttackContext, AttackResult, AttackStatus, inapplicable
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import CertificateKind, ClaimKind, SearchScope

LEAN_IDENTITY = "Problems.Engine.mul_pow_eq_iff_padicValInt"


class PredicateDirection(str, Enum):
    NECESSARY_ONLY = "NECESSARY_ONLY"
    SUFFICIENT_ONLY = "SUFFICIENT_ONLY"
    EXACT = "EXACT"
    REFUTED = "REFUTED"
    UNDERDETERMINED = "UNDERDETERMINED"


class DomainEvidence(str, Enum):
    SAMPLE_SUPPORTED = "SAMPLE_SUPPORTED"
    COUNTEREXAMPLE_SURVIVED = "COUNTEREXAMPLE_SURVIVED"
    FINITE_RANGE_VERIFIED = "FINITE_RANGE_VERIFIED"
    NECESSARY_PROVED = "NECESSARY_PROVED"
    SUFFICIENT_PROVED = "SUFFICIENT_PROVED"
    EXACT_PROVED = "EXACT_PROVED"
    LEAN_CERTIFIED = "LEAN_CERTIFIED"


@dataclass(frozen=True)
class AffineFamily:
    """Parameterized relation ``b^k y = p x + r``. Not a map-specific certificate."""

    p: int
    r: int
    base: int
    observed_k: tuple[int, ...]
    status: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "p": self.p,
            "r": self.r,
            "base": self.base,
            "q_base": self.base,
            "observed_k": self.observed_k,
            "status": self.status,
        }


@dataclass(frozen=True)
class ParameterDomain:
    """Arithmetic predicate. Maximal exponent is a divisibility conjunction."""

    kind: str
    parameters: Mapping[str, Any] = field(default_factory=dict)
    presentation: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "parameters", MappingProxyType(dict(self.parameters)))

    def as_dict(self) -> dict[str, Any]:
        payload = {"kind": self.kind, **dict(self.parameters)}
        if self.presentation:
            payload["presentation"] = self.presentation
        return payload


@dataclass(frozen=True)
class DomainCertificate:
    parameter: int
    domain: ParameterDomain
    direction: str
    evidence: str
    counterexamples_necessary: tuple[int, ...] = ()
    counterexamples_sufficient: tuple[int, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        return {
            "parameter": self.parameter,
            "domain": self.domain.as_dict(),
            "direction": self.direction,
            "evidence": self.evidence,
            "counterexamples_necessary": self.counterexamples_necessary,
            "counterexamples_sufficient": self.counterexamples_sufficient,
        }


@dataclass(frozen=True)
class AffineFamilyCertificate:
    family: AffineFamily | None
    domains: tuple[DomainCertificate, ...]
    divisibility_checks: tuple[DomainCertificate, ...]
    coverage: str
    soundness: str
    completeness: str
    globality: str
    branch_validity: str
    domain_soundness: str
    domain_completeness: str
    parameter_completeness: str
    lean: str
    queries: int
    overlap: int

    def as_dict(self) -> dict[str, Any]:
        return {
            "family": None if self.family is None else self.family.as_dict(),
            "domains": tuple(item.as_dict() for item in self.domains),
            "divisibility_checks": tuple(item.as_dict() for item in self.divisibility_checks),
            "coverage": self.coverage,
            "soundness": self.soundness,
            "completeness": self.completeness,
            "globality": self.globality,
            "branch_validity": self.branch_validity,
            "domain_soundness": self.domain_soundness,
            "domain_completeness": self.domain_completeness,
            "parameter_completeness": self.parameter_completeness,
            "lean": self.lean,
            "queries": self.queries,
            "overlap": self.overlap,
            "predicate_count": len(self.domains),
            "reconstructed_affine": None,
        }


def _q(p: int, r: int, x: int) -> int:
    return p * x + r


def _divides(base: int, exponent: int, value: int) -> bool:
    if exponent < 0:
        return False
    if value == 0:
        return True
    return value % (base ** exponent) == 0


def _maximal_divides(base: int, exponent: int, value: int) -> bool:
    if value == 0:
        return False
    return _divides(base, exponent, value) and not _divides(base, exponent + 1, value)


def _label_samples(
    samples: Mapping[int, int],
    p: int,
    r: int,
    base: int,
) -> dict[int, list[int]]:
    labeled: dict[int, list[int]] = {}
    for x, y in samples.items():
        if y == 0:
            continue
        target = _q(p, r, x)
        if target % y != 0:
            continue
        k = _is_power_of_base(target // y, base)
        if k is None:
            continue
        labeled.setdefault(k, []).append(x)
    return labeled


def _domain_from_part(part: Mapping[str, Any]) -> ParameterDomain:
    kind = str(part.get("kind", ""))
    params = {key: value for key, value in part.items() if key not in {"kind", "presentation"}}
    return ParameterDomain(kind, params, presentation=str(part.get("presentation", "")))


def predicate_holds(domain: ParameterDomain, x: int, p: int, r: int, base: int) -> bool:
    params = domain.parameters
    kind = domain.kind
    value = _q(p, r, x)
    if kind == "divisibility":
        return _divides(base, int(params.get("k", 0)), value)
    if kind == "maximal_divisibility":
        return _maximal_divides(base, int(params.get("k", 0)), value)
    if kind == "congruence":
        return x % int(params["modulus"]) == int(params["residue"])
    if kind == "residue_set":
        return x % int(params["modulus"]) in set(params["residues"])
    if kind == "sign":
        if params.get("sign") == "nonneg":
            return x >= 0
        return x < 0
    if kind == "interval":
        return int(params["lo"]) <= x <= int(params["hi"])
    if kind == "conjunction":
        parts = params.get("parts", ())
        return all(predicate_holds(_domain_from_part(part), x, p, r, base) for part in parts)
    return False


def _parameter_matches(
    k: int,
    x: int,
    y: int,
    p: int,
    r: int,
    base: int,
) -> bool:
    target = _q(p, r, x)
    if y == 0:
        return target == 0 and k == 0
    if target % y != 0:
        return False
    return _is_power_of_base(target // y, base) == k


def classify_predicate(
    domain: ParameterDomain,
    k: int,
    labeled: Mapping[int, Sequence[int]],
    spec: ProblemSpec,
    phase: object,
    p: int,
    r: int,
    base: int,
    window: Sequence[int],
) -> tuple[str, tuple[int, ...], tuple[int, ...], int]:
    support = set(labeled.get(k, ()))
    fail_necessary: list[int] = []
    fail_sufficient: list[int] = []
    queries = 0
    others = {item for key, group in labeled.items() if key != k for item in group}
    for x in support:
        queries += 1
        if not predicate_holds(domain, x, p, r, base):
            fail_necessary.append(x)
    for value in window:
        queries += 1
        point = int(value)
        if not predicate_holds(domain, point, p, r, base):
            continue
        if point in others:
            fail_sufficient.append(point)
            continue
        image = _eval_map(spec, point, phase)
        if image is None:
            continue
        if not _parameter_matches(k, point, image, p, r, base):
            fail_sufficient.append(point)
    necessary_ok = not fail_necessary
    sufficient_ok = not fail_sufficient
    if necessary_ok and sufficient_ok:
        direction = PredicateDirection.EXACT.value
    elif necessary_ok:
        direction = PredicateDirection.NECESSARY_ONLY.value
    elif sufficient_ok:
        direction = PredicateDirection.SUFFICIENT_ONLY.value
    else:
        direction = PredicateDirection.REFUTED.value
    return direction, tuple(fail_necessary[:8]), tuple(fail_sufficient[:8]), queries


def _images_coprime_to_base(
    samples: Mapping[int, int],
    labeled: Mapping[int, Sequence[int]],
    base: int,
) -> bool:
    for group in labeled.values():
        for x in group:
            if samples[x] % base == 0:
                return False
    return True


def _residue_restriction(
    labeled_points: Sequence[int],
    sampled_points: Sequence[int],
) -> ParameterDomain | None:
    points = set(labeled_points)
    sampled = set(sampled_points)
    if not sampled or points >= sampled:
        return None
    best: ParameterDomain | None = None
    best_gap = 0
    for modulus in range(2, 13):
        have = {x % modulus for x in points}
        all_res = {x % modulus for x in sampled}
        gap = len(all_res) - len(have)
        if gap > best_gap and have and have != all_res:
            best_gap = gap
            best = ParameterDomain(
                "residue_set",
                {"modulus": modulus, "residues": tuple(sorted(have))},
            )
    return best


def _with_presentation(domain: ParameterDomain, presentation: str) -> ParameterDomain:
    return ParameterDomain(domain.kind, dict(domain.parameters), presentation=presentation)


def _make_conjunction(*domains: ParameterDomain) -> ParameterDomain:
    parts = []
    for domain in domains:
        if domain.kind == "conjunction":
            parts.extend(domain.parameters.get("parts", ()))
        else:
            parts.append(domain.as_dict())
    return ParameterDomain("conjunction", {"parts": tuple(parts)})


def _is_maximal_kind(domain: ParameterDomain) -> bool:
    if domain.kind == "maximal_divisibility":
        return True
    if domain.kind == "conjunction":
        return any(
            str(part.get("kind")) == "maximal_divisibility"
            for part in domain.parameters.get("parts", ())
        )
    return False


def _evidence_for(direction: str, domain: ParameterDomain, coprime: bool) -> str:
    if direction != PredicateDirection.EXACT.value:
        if direction == PredicateDirection.NECESSARY_ONLY.value:
            return DomainEvidence.SAMPLE_SUPPORTED.value
        if direction == PredicateDirection.REFUTED.value:
            return DomainEvidence.SAMPLE_SUPPORTED.value
        return DomainEvidence.COUNTEREXAMPLE_SURVIVED.value
    if _is_maximal_kind(domain) and coprime:
        return DomainEvidence.LEAN_CERTIFIED.value
    if _is_maximal_kind(domain):
        return DomainEvidence.EXACT_PROVED.value
    return DomainEvidence.COUNTEREXAMPLE_SURVIVED.value


def _certificate_for(
    k: int,
    domain: ParameterDomain,
    direction: str,
    nec: Sequence[int],
    suf: Sequence[int],
    coprime: bool,
    p: int,
    r: int,
    base: int,
) -> DomainCertificate:
    presentation = ""
    if direction == PredicateDirection.EXACT.value and _is_maximal_kind(domain):
        presentation = f"k = v_{base}({p}x+{r})"
    return DomainCertificate(
        parameter=k,
        domain=_with_presentation(domain, presentation),
        direction=direction,
        evidence=_evidence_for(direction, domain, coprime),
        counterexamples_necessary=tuple(nec),
        counterexamples_sufficient=tuple(suf),
    )


def certify_parameterized_family(
    spec: ProblemSpec,
    context: AttackContext,
    family_data: Mapping[str, Any],
) -> AffineFamilyCertificate:
    p = int(family_data["p"])
    r = int(family_data["r"])
    base = int(family_data.get("base") or family_data.get("q_base") or 2)
    samples = _collect_samples(spec, context, DEFAULT_SAMPLE_WINDOW)
    labeled = _label_samples(samples, p, r, base)
    phase = spec.initial_phase()
    coprime = _images_coprime_to_base(samples, labeled, base)
    restriction = _residue_restriction(
        tuple(x for group in labeled.values() for x in group),
        tuple(samples),
    )
    domains: list[DomainCertificate] = []
    divisibility_checks: list[DomainCertificate] = []
    queries = 0
    overlap = 0
    seen: dict[int, int] = {}
    observed = tuple(sorted(labeled))
    for k in observed:
        divisibility = ParameterDomain("divisibility", {"k": k, "base": base, "p": p, "r": r})
        maximal = ParameterDomain("maximal_divisibility", {"k": k, "base": base, "p": p, "r": r})
        d_dir, d_nec, d_suf, d_count = classify_predicate(
            divisibility, k, labeled, spec, phase, p, r, base, DEFAULT_FALSIFY_WINDOW
        )
        queries += d_count
        div_cert = _certificate_for(k, divisibility, d_dir, d_nec, d_suf, False, p, r, base)
        divisibility_checks.append(div_cert)
        m_dir, m_nec, m_suf, m_count = classify_predicate(
            maximal, k, labeled, spec, phase, p, r, base, DEFAULT_FALSIFY_WINDOW
        )
        queries += m_count
        max_cert = _certificate_for(k, maximal, m_dir, m_nec, m_suf, coprime, p, r, base)
        chosen = max_cert
        if m_dir != PredicateDirection.EXACT.value and restriction is not None:
            mixed = _make_conjunction(restriction, maximal)
            mix_dir, mix_nec, mix_suf, mix_count = classify_predicate(
                mixed, k, labeled, spec, phase, p, r, base, DEFAULT_FALSIFY_WINDOW
            )
            queries += mix_count
            mix_cert = _certificate_for(k, mixed, mix_dir, mix_nec, mix_suf, coprime, p, r, base)
            if mix_dir == PredicateDirection.EXACT.value:
                chosen = mix_cert
        if chosen.direction == PredicateDirection.EXACT.value:
            for x in labeled[k]:
                if x in seen and seen[x] != k:
                    overlap += 1
                seen[x] = k
        domains.append(chosen)
    labeled_points = {x for group in labeled.values() for x in group}
    uncovered = set(samples) - labeled_points
    exact_domains = [item for item in domains if item.direction == PredicateDirection.EXACT.value]
    lean = ""
    globality = "empirical"
    if exact_domains and coprime and any(
        item.evidence == DomainEvidence.LEAN_CERTIFIED.value for item in exact_domains
    ):
        lean = LEAN_IDENTITY
        globality = "relation_certified_map_empirical"
    family = AffineFamily(
        p=p,
        r=r,
        base=base,
        observed_k=observed,
        status="SUPPORTED_BY_SAMPLES",
    )
    return AffineFamilyCertificate(
        family=family,
        domains=tuple(domains),
        divisibility_checks=tuple(divisibility_checks),
        coverage="complete" if not uncovered else "partial",
        soundness="certified" if exact_domains else "empirical",
        completeness="empirical" if uncovered else "certified",
        globality=globality,
        branch_validity="empirical" if exact_domains else "uncertified",
        domain_soundness="certified" if exact_domains else "empirical",
        domain_completeness="empirical" if uncovered else "window_complete",
        parameter_completeness="complete" if labeled and not uncovered else "partial",
        lean=lean,
        queries=queries,
        overlap=overlap,
    )


def _region_match(domain: ParameterDomain, x: int) -> bool:
    return predicate_holds(domain, x, 0, 0, 2)


def certify_finite_branches(
    spec: ProblemSpec,
    context: AttackContext,
    branches: Sequence[Mapping[str, Any]],
) -> AffineFamilyCertificate:
    samples = _collect_samples(spec, context, DEFAULT_SAMPLE_WINDOW)
    phase = spec.initial_phase()
    domains: list[DomainCertificate] = []
    queries = 0
    explained: set[int] = set()
    for index, branch in enumerate(branches):
        region = branch.get("region") or {}
        kind = str(region.get("kind", "unknown"))
        params = {key: value for key, value in region.items() if key != "kind"}
        domain = ParameterDomain(kind, params)
        support = set(branch.get("support") or ())
        explained.update(support)
        p = int(branch["p"])
        q = int(branch["q"])
        r = int(branch["r"])
        fail_nec: list[int] = []
        fail_suf: list[int] = []
        for x in support:
            queries += 1
            if not _region_match(domain, x):
                fail_nec.append(x)
        for value in DEFAULT_FALSIFY_WINDOW:
            queries += 1
            if not _region_match(domain, int(value)):
                continue
            image = _eval_map(spec, int(value), phase)
            if image is None:
                continue
            if q * image != p * int(value) + r:
                fail_suf.append(int(value))
        necessary_ok = not fail_nec
        sufficient_ok = not fail_suf
        if necessary_ok and sufficient_ok:
            direction = PredicateDirection.EXACT.value
            evidence = DomainEvidence.COUNTEREXAMPLE_SURVIVED.value
        elif necessary_ok:
            direction = PredicateDirection.NECESSARY_ONLY.value
            evidence = DomainEvidence.SAMPLE_SUPPORTED.value
        else:
            direction = PredicateDirection.REFUTED.value
            evidence = DomainEvidence.SAMPLE_SUPPORTED.value
        domains.append(
            DomainCertificate(
                parameter=index,
                domain=domain,
                direction=direction,
                evidence=evidence,
                counterexamples_necessary=tuple(fail_nec[:8]),
                counterexamples_sufficient=tuple(fail_suf[:8]),
            )
        )
    uncovered = set(samples) - explained
    exact = [item for item in domains if item.direction == PredicateDirection.EXACT.value]
    return AffineFamilyCertificate(
        family=None,
        domains=tuple(domains),
        divisibility_checks=(),
        coverage="complete" if not uncovered else "partial",
        soundness="empirical",
        completeness="empirical",
        globality="empirical",
        branch_validity="window" if exact else "uncertified",
        domain_soundness="window" if exact else "empirical",
        domain_completeness="window" if not uncovered else "partial",
        parameter_completeness="finite",
        lean="",
        queries=queries,
        overlap=0,
    )


def _prior_piecewise(context: AttackContext) -> Any | None:
    for item in reversed(context.prior_results):
        if getattr(item, "name", None) == "piecewise_affine":
            return item
    return None


def run_parameter_domain(
    spec: ProblemSpec,
    context: AttackContext,
) -> AffineFamilyCertificate | None:
    prior = _prior_piecewise(context)
    if prior is None:
        return None
    kind = prior.evidence.get("census_kind")
    family = prior.evidence.get("family")
    branches = prior.evidence.get("branches") or ()
    if kind == "PARAMETERIZED_CENSUS" and family:
        return certify_parameterized_family(spec, context, family)
    if kind == "FINITE_CENSUS" and branches:
        return certify_finite_branches(spec, context, branches)
    return None


class ParameterDomainAttack:
    """Certify arithmetic domains of a reconstructed family. Does not seed a map law."""

    name = "parameter_domain"

    def applicable(self, spec: ProblemSpec, context: AttackContext) -> bool:
        del spec
        prior = _prior_piecewise(context)
        if prior is None:
            return False
        kind = prior.evidence.get("census_kind")
        return kind in {"PARAMETERIZED_CENSUS", "FINITE_CENSUS"}

    def run(self, spec: ProblemSpec, context: AttackContext) -> AttackResult:
        if not self.applicable(spec, context):
            return inapplicable(
                self.name,
                "parameter-domain certification needs a prior piecewise_affine census",
                ClaimKind.REACHABLE,
            )
        certificate = run_parameter_domain(spec, context)
        if certificate is None:
            return AttackResult(
                name=self.name,
                status=AttackStatus.INCONCLUSIVE,
                kind=ClaimKind.REACHABLE,
                scope=SearchScope.BOUNDED,
                claim="prior census did not yield a family or finite branches",
            )
        evidence = certificate.as_dict()
        exact = [
            item
            for item in certificate.domains
            if item.direction == PredicateDirection.EXACT.value
        ]
        necessary_only = [
            item
            for item in certificate.domains
            if item.direction == PredicateDirection.NECESSARY_ONLY.value
        ]
        if certificate.lean:
            claim = (
                "arithmetic parameter domain certified: maximal divisibility "
                "is necessary and sufficient for the reconstructed family; "
                "map globality on Z remains empirical"
            )
            return AttackResult(
                name=self.name,
                status=AttackStatus.SUPPORTED,
                kind=ClaimKind.REACHABLE,
                scope=SearchScope.EXACT,
                claim=claim,
                evidence=evidence,
                certificates=(certificate.as_dict(),),
                certificate_kind=CertificateKind.EXACT_ARITHMETIC_IDENTITY,
                recommended_next_attacks=("control_word", "closure"),
            )
        if exact:
            claim = (
                f"window-exact parameter domains for {len(exact)} parameters; "
                "this is not a Z-wide map theorem"
            )
            return AttackResult(
                name=self.name,
                status=AttackStatus.OBSERVATION,
                kind=ClaimKind.REACHABLE,
                scope=SearchScope.BOUNDED,
                claim=claim,
                evidence=evidence,
                certificates=(certificate.as_dict(),),
                recommended_next_attacks=("control_word", "closure"),
            )
        if necessary_only:
            claim = (
                "divisibility is necessary but not sufficient for parameter "
                "selection on the sample window"
            )
            return AttackResult(
                name=self.name,
                status=AttackStatus.OBSERVATION,
                kind=ClaimKind.REACHABLE,
                scope=SearchScope.BOUNDED,
                claim=claim,
                evidence=evidence,
                recommended_next_attacks=("control_word", "closure"),
            )
        return AttackResult(
            name=self.name,
            status=AttackStatus.INCONCLUSIVE,
            kind=ClaimKind.REACHABLE,
            scope=SearchScope.BOUNDED,
            claim="parameter domains remain underdetermined on the sample window",
            evidence=evidence,
        )
