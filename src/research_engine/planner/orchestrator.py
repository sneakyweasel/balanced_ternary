"""Deterministic attack order. Symbolic steps are not implemented."""

from __future__ import annotations

from dataclasses import dataclass, replace

from research_engine.attacks.affine import AffineInvariantAttack
from research_engine.attacks.block import BlockDynamicsAttack
from research_engine.attacks.closure import ExhaustiveClosureAttack
from research_engine.attacks.control_word import ControlWordAttack
from research_engine.attacks.control_obstruction import ControlObstructionAttack
from research_engine.attacks.factorization import FactorizationAttack
from research_engine.attacks.functional import FunctionalBoundAttack
from research_engine.attacks.modular import ModularInvariantAttack
from research_engine.attacks.parameter_domain import ParameterDomainAttack
from research_engine.attacks.piecewise_affine import PiecewiseAffineCensusAttack
from research_engine.attacks.reconnaissance import ReconnaissanceAttack
from research_engine.attacks.result import (
    Attack,
    AttackContext,
    AttackResult,
    AttackStatus,
    inapplicable,
)
from research_engine.attacks.reverse import ReverseGeometryAttack
from research_engine.attacks.separation import BehavioralSeparationAttack
from research_engine.attacks.spectral import SpectralClassificationAttack
from research_engine.attacks.symmetry import SymmetryAttack
from research_engine.behavior.quotient import BehavioralQuotientAttack
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import ClaimKind, SearchScope
from research_engine.planner.hypothesis import DecisionKind, Hypothesis, HypothesisStatus
from research_engine.planner.ledger import ResearchLedger
from research_engine.planner.negative import ForbiddenImplication

DEFAULT_ATTACK_ORDER: tuple[str, ...] = (
    "reconnaissance",
    "piecewise_affine",
    "parameter_domain",
    "control_word",
    "control_obstruction",
    "closure",
    "modular",
    "functional",
    "affine",
    "reverse",
    "block",
    "spectral",
    "factorization",
    "separation",
    "quotient",
    "symmetry",
)

DEFERRED_ATTACKS: tuple[str, ...] = ("symbolic",)
DEFAULT_PLANNER_HORIZON = 16

_ATTACKS: dict[str, type[Attack]] = {
    "reconnaissance": ReconnaissanceAttack,
    "piecewise_affine": PiecewiseAffineCensusAttack,
    "parameter_domain": ParameterDomainAttack,
    "control_word": ControlWordAttack,
    "control_obstruction": ControlObstructionAttack,
    "closure": ExhaustiveClosureAttack,
    "modular": ModularInvariantAttack,
    "functional": FunctionalBoundAttack,
    "affine": AffineInvariantAttack,
    "reverse": ReverseGeometryAttack,
    "block": BlockDynamicsAttack,
    "spectral": SpectralClassificationAttack,
    "factorization": FactorizationAttack,
    "separation": BehavioralSeparationAttack,
    "quotient": BehavioralQuotientAttack,
    "symmetry": SymmetryAttack,
}


@dataclass(frozen=True)
class SkipRecord:
    attack: str
    reason: str
    implication_id: str = ""


@dataclass(frozen=True)
class PlannerReport:
    results: tuple[AttackResult, ...]
    skipped: tuple[SkipRecord, ...]
    hypotheses: tuple[Hypothesis, ...]
    blocked_jumps: tuple[ForbiddenImplication, ...]
    next_attacks: tuple[str, ...] = DEFERRED_ATTACKS


class AttackPlanner:
    """Run cheap exact attacks in a fixed order.

    The planner never promotes ``LIVE_SLICE`` or ``TERMINAL`` evidence
    to an exact ``LIVE`` hypothesis.
    """

    def __init__(self, ledger: ResearchLedger | None = None) -> None:
        self.ledger = ledger if ledger is not None else ResearchLedger()

    def run(self, spec: ProblemSpec, context: AttackContext) -> PlannerReport:
        if context.max_steps is None:
            context = replace(context, max_steps=DEFAULT_PLANNER_HORIZON)
        closed = self.ledger.knowledge.closed_attacks()
        results: list[AttackResult] = []
        skipped: list[SkipRecord] = []
        blocked: list[ForbiddenImplication] = []
        for name in DEFAULT_ATTACK_ORDER:
            if name in closed:
                skipped.append(SkipRecord(name, "closed by negative knowledge"))
                continue
            if name in context.skip_attacks:
                skipped.append(SkipRecord(name, "skipped by adapter"))
                continue
            attack = _ATTACKS[name]()
            if not attack.applicable(spec, context):
                skipped.append(SkipRecord(name, "inapplicable"))
                continue
            result = attack.run(spec, context)
            if result.status is AttackStatus.INAPPLICABLE:
                skipped.append(SkipRecord(name, result.claim))
                continue
            self.ledger.record_attack(result)
            results.append(result)
            context = replace(context, prior_results=tuple(results))
            for target in (ClaimKind.LIVE, ClaimKind.TERMINAL):
                jump = self.ledger.knowledge.forbids_kinds(result.kind, target)
                if jump is not None:
                    blocked.append(jump)
        for name in DEFERRED_ATTACKS:
            skipped.append(SkipRecord(name, "not implemented in this phase"))
        self._record_census_hypothesis(spec, results)
        return PlannerReport(
            results=tuple(results),
            skipped=tuple(skipped),
            hypotheses=tuple(self.ledger.hypotheses.values()),
            blocked_jumps=tuple(_unique(blocked)),
            next_attacks=DEFERRED_ATTACKS,
        )

    def _record_census_hypothesis(self, spec: ProblemSpec, results: list[AttackResult]) -> None:
        recon = next((item for item in results if item.name == "reconnaissance"), None)
        if recon is None:
            return
        hyp_id = f"{spec.name}_live_slice_census"
        if hyp_id in self.ledger.hypotheses:
            return
        self.ledger.add_hypothesis(
            Hypothesis(
                id=hyp_id,
                statement=recon.claim,
                kind=ClaimKind.LIVE_SLICE,
                intended_scope=SearchScope.BOUNDED,
                status=HypothesisStatus.SUPPORTED,
                problem=spec.name,
                evidence=f"horizon={recon.evidence.get('horizon')}",
            )
        )


def run_named_attack(name: str, spec: ProblemSpec, context: AttackContext) -> AttackResult:
    """Run one cheap attack. Symbolic stays unimplemented."""
    if name in DEFERRED_ATTACKS:
        return inapplicable(
            name,
            f"{name} is not implemented in this phase",
            ClaimKind.REACHABLE,
        )
    cls = _ATTACKS.get(name)
    if cls is None:
        raise KeyError(f"unknown attack {name!r}")
    if context.max_steps is None:
        context = replace(context, max_steps=DEFAULT_PLANNER_HORIZON)
    context = _ensure_certificate_chain(name, spec, context)
    attack = cls()
    if not attack.applicable(spec, context):
        return inapplicable(name, "inapplicable", ClaimKind.REACHABLE)
    return attack.run(spec, context)


def _ensure_certificate_chain(
    name: str,
    spec: ProblemSpec,
    context: AttackContext,
) -> AttackContext:
    """Census then domain, so named control-word runs consume a certificate."""
    if name not in {"parameter_domain", "control_word", "control_obstruction"}:
        return context
    priors = list(context.prior_results)
    names = {item.name for item in priors}
    if "piecewise_affine" not in names:
        census = PiecewiseAffineCensusAttack()
        if census.applicable(spec, context):
            prior = census.run(spec, context)
            priors.append(prior)
            context = replace(context, prior_results=tuple(priors))
            names.add("piecewise_affine")
    if name in {"control_word", "control_obstruction"} and "parameter_domain" not in names:
        domain = ParameterDomainAttack()
        if domain.applicable(spec, context):
            prior = domain.run(spec, context)
            priors.append(prior)
            context = replace(context, prior_results=tuple(priors))
            names.add("parameter_domain")
    if name == "control_obstruction" and "control_word" not in names:
        composed = ControlWordAttack()
        if composed.applicable(spec, context):
            prior = composed.run(spec, context)
            priors.append(prior)
            context = replace(context, prior_results=tuple(priors))
    return context


def promote_if_legal(ledger: ResearchLedger, hyp_id: str, result: AttackResult) -> Hypothesis:
    """Promote only when kind and scope match. Otherwise raise ``LedgerError``."""
    return ledger.decide(
        hyp_id,
        DecisionKind.PROMOTE,
        result.claim,
        from_result=result,
    )


def _unique(items: list[ForbiddenImplication]) -> list[ForbiddenImplication]:
    seen: set[str] = set()
    out: list[ForbiddenImplication] = []
    for item in items:
        if item.id in seen:
            continue
        seen.add(item.id)
        out.append(item)
    return out
