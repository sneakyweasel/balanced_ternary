"""Affine-law extraction before region attachment. Does not reorder infer_region."""

from __future__ import annotations

from research_engine.attacks.piecewise_affine import (
    DEFAULT_FALSIFY_WINDOW,
    DEFAULT_SAMPLE_WINDOW,
    MIN_SUPPORT,
    RegionKind,
    _collect_samples,
    _eval_map,
    _holds,
    _parameterized_families,
    _region_contains,
    candidate_affine_laws,
    infer_region,
    run_piecewise_affine_census,
)
from research_engine.attacks.result import AttackContext
from research_engine.core.problem_spec import ProblemSpec
from research_engine.law.types import (
    AffineLaw,
    DomainAttachment,
    DomainEvidence,
    LawDomainPair,
    LawEvidence,
)

_LAW_CAP = 8


def _falsify_law(
    spec: ProblemSpec,
    p: int,
    q: int,
    r: int,
    phase: object,
    window: tuple[int, ...],
) -> tuple[int, ...]:
    hits: list[int] = []
    for value in window:
        image = _eval_map(spec, int(value), phase)
        if image is None:
            continue
        if not _holds(p, q, r, int(value), image):
            hits.append(int(value))
            if len(hits) >= 8:
                break
    return tuple(hits)


def _law_from_line(
    spec: ProblemSpec,
    p: int,
    q: int,
    r: int,
    support: set[int],
    phase: object,
    falsify_window: tuple[int, ...],
    target: str,
) -> AffineLaw:
    leaks = _falsify_law(spec, p, q, r, phase, falsify_window)
    if leaks:
        evidence = LawEvidence.LAW_REFUTED
        statement = f"q y = p x + r leaks off the sample window ({p},{q},{r})"
    elif len(support) >= MIN_SUPPORT:
        evidence = LawEvidence.LAW_CERTIFIED
        statement = f"q y = {p} x + {r} with q={q} holds on the sample/falsify windows; not a Z-theorem"
    else:
        evidence = LawEvidence.LAW_CANDIDATE
        statement = f"underdetermined line ({p},{q},{r})"
    return AffineLaw(
        p=p,
        q=q,
        r=r,
        support=tuple(sorted(support)),
        evidence=evidence,
        counterexamples=leaks,
        source_target=target,
        statement=statement,
    )


def _attach_domain(
    law: AffineLaw,
    domain: set[int],
    target: str,
) -> DomainAttachment:
    support = set(law.support)
    if not support:
        return DomainAttachment(
            region=None,
            evidence=DomainEvidence.DOMAIN_UNKNOWN,
            source_target=target,
            statement="no support to attach a region",
        )
    region = infer_region(support, domain)
    region_pts = tuple(sorted(x for x in domain if _region_contains(region, x)))
    covered = set(region_pts)
    truncated = bool(covered) and covered < support
    if region.kind in {RegionKind.UNKNOWN.value, RegionKind.FINITE_SET.value}:
        evidence = DomainEvidence.DOMAIN_UNKNOWN
        statement = "infer_region did not return a structured domain"
    elif truncated:
        evidence = DomainEvidence.DOMAIN_TRUNCATED
        statement = (
            f"infer_region attached {region.kind} on a proper subset of the law support; "
            "not a complete cover and not DOMAIN_CERTIFIED"
        )
    elif covered >= support and region.kind != RegionKind.UNKNOWN.value:
        evidence = DomainEvidence.DOMAIN_CERTIFIED
        statement = (
            f"infer_region {region.kind} covers the law support on the sample window; "
            "not a Z-domain theorem"
        )
    else:
        evidence = DomainEvidence.DOMAIN_CANDIDATE
        statement = "region attachment is incomplete"
    return DomainAttachment(
        region=region,
        evidence=evidence,
        region_points=region_pts,
        truncated=truncated,
        source_target=target,
        statement=statement,
    )


def _family_law(family, target: str) -> AffineLaw:
    return AffineLaw(
        p=family.p,
        q=None,
        r=family.r,
        support=tuple(family.support),
        evidence=LawEvidence.LAW_CERTIFIED,
        family_base=family.base,
        observed_k=tuple(family.observed_k),
        source_target=target,
        statement=(
            f"parameterized family {family.base}^k y = {family.p} x + {family.r}; "
            "not a global branch theorem"
        ),
    )


def extract_pairs(
    spec: ProblemSpec,
    context: AttackContext,
) -> tuple[LawDomainPair, ...]:
    target = str(getattr(spec, "name", "") or "")
    samples = _collect_samples(spec, context, DEFAULT_SAMPLE_WINDOW)
    phase = spec.initial_phase()
    domain = set(samples)
    pairs: list[LawDomainPair] = []
    families = _parameterized_families(samples)
    if families:
        law = _family_law(families[0], target)
        domain_att = _attach_domain(law, domain, target)
        if domain_att.evidence is DomainEvidence.DOMAIN_CERTIFIED:
            from dataclasses import replace

            domain_att = replace(
                domain_att,
                evidence=DomainEvidence.DOMAIN_CANDIDATE,
                statement="parameterized family domain remains a sample predicate, not DOMAIN_CERTIFIED",
            )
        pairs.append(LawDomainPair(law=law, domain=domain_att))
    ranked = sorted(
        candidate_affine_laws(samples).items(),
        key=lambda item: len(item[1]),
        reverse=True,
    )
    for (p, q, r), support in ranked[:_LAW_CAP]:
        law = _law_from_line(spec, p, q, r, support, phase, DEFAULT_FALSIFY_WINDOW, target)
        domain_att = _attach_domain(law, domain, target)
        pairs.append(LawDomainPair(law=law, domain=domain_att))
    return tuple(pairs)


def flood_census_kind(spec: ProblemSpec, context: AttackContext) -> str:
    census = run_piecewise_affine_census(spec, context)
    return census.census_kind
