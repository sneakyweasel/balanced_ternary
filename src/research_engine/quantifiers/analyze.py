"""Top-level quantifier entry. Opt-in; not a flood-order attack."""

from __future__ import annotations

from dataclasses import replace

from research_engine.attacks.piecewise_affine import PiecewiseAffineCensusAttack
from research_engine.attacks.result import AttackContext
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import ClaimKind, SearchScope
from research_engine.memory.types import NoveltyStatus
from research_engine.quantifiers.discipline import (
    certified_on_window_is_not_z_theorem,
    existential_cycle_is_not_all_paths_cycle,
    no_path_found_is_not_nonexistence,
    truncation_is_unknown_not_refuted,
)
from research_engine.quantifiers.probes import (
    CYCLE_CAP,
    DEFAULT_WINDOW,
    ORBIT_CAP,
    existential_cycle_witness,
    universal_termination_on_seeds,
)
from research_engine.quantifiers.relation import closure_states, relation_edges, seed_states, working_phase
from research_engine.quantifiers.types import (
    ENGINE_QUANTIFIER_VERSION,
    PathClaim,
    PathQuantifier,
    PathStatus,
    QuantifierReport,
)
from research_engine.strategy.types import (
    ObligationKind,
    ProofObligation,
    ResearchHypothesis,
    ResearchHypothesisStatus,
)

_KNOWN = {
    "hidden_nondet_stay_or_decrement": "stay-or-decrement has an existential stay cycle; not all paths cycle",
    "hidden_nondet_two_affine": "two-affine branching; existential cycle at the 2x+1 fixed point",
    "slc_sum_strip": "sum-strip relation has an existential cycle; universal termination fails on the window",
}


def _novelty(name: str) -> tuple[NoveltyStatus, str]:
    known = _KNOWN.get(name, "")
    if known:
        return NoveltyStatus.KNOWN_REDISCOVERY, known
    return NoveltyStatus.UNKNOWN, ""


def analyze(
    spec: ProblemSpec,
    context: AttackContext | None = None,
    *,
    window: tuple[int, ...] | None = None,
    max_len: int = CYCLE_CAP,
    max_depth: int = ORBIT_CAP,
) -> QuantifierReport:
    if context is not None:
        ctx = context
    else:
        maker = getattr(spec, "attack_context", None)
        ctx = maker() if callable(maker) else AttackContext()
    target = str(getattr(spec, "name", "") or "")
    novelty, _closest = _novelty(target)
    used_window = DEFAULT_WINDOW if window is None else window
    phase = working_phase(spec, ctx)
    reached, closure_complete = closure_states(spec, ctx)
    states = seed_states(spec, used_window, extra=reached if closure_complete else ())
    sample = relation_edges(spec, states, phase)
    cycle = existential_cycle_witness(spec, ctx, used_window, max_len=max_len)
    universal = universal_termination_on_seeds(
        spec, ctx, used_window, max_depth=max_depth, max_len=max_len
    )
    exist_status = PathStatus.EXISTENTIAL_WITNESS if cycle else PathStatus.NO_PATH_FOUND
    exist_statement = (
        "legal cycle witnessed under EXISTS_PATH; does not imply all_paths_cycle"
        if cycle
        else "no cycle found under the search cap; NO_PATH_FOUND is not a nonexistence theorem"
    )
    term_status = universal["status"]
    if not isinstance(term_status, PathStatus):
        term_status = PathStatus(str(term_status))
    counter = universal.get("counterexample") or ()
    if not isinstance(counter, tuple):
        counter = tuple(counter)
    claims = (
        PathClaim(
            name="existential_cycle",
            quantifier=PathQuantifier.EXISTS_PATH,
            status=exist_status,
            witness=cycle or (),
            window=used_window,
            cap=max_len,
            statement=exist_statement,
            source_target=target,
            novelty_status=novelty,
        ),
        PathClaim(
            name="universal_termination",
            quantifier=PathQuantifier.ALL_PATHS,
            status=term_status,
            counterexample=counter,
            window=used_window,
            cap=max_depth,
            statement=str(universal.get("reason") or ""),
            source_target=target,
            novelty_status=novelty,
        ),
        PathClaim(
            name="all_paths_cycle",
            quantifier=PathQuantifier.ALL_PATHS,
            status=PathStatus.UNKNOWN,
            window=used_window,
            cap=max_len,
            statement="finite search does not certify every legal path is cyclic; not ALL_PATHS",
            source_target=target,
            novelty_status=novelty,
        ),
    )
    census_skipped = not PiecewiseAffineCensusAttack().applicable(spec, ctx)
    report = QuantifierReport(
        source_target=target,
        claims=claims,
        relation_sample=sample,
        census_skipped=census_skipped,
        closure_complete=closure_complete,
        version=ENGINE_QUANTIFIER_VERSION,
        novelty_status=novelty,
    )
    if not no_path_found_is_not_nonexistence(report):
        exist = report.claim("existential_cycle")
        if exist is not None:
            exist = replace(
                exist,
                status=PathStatus.NO_PATH_FOUND,
                statement="no cycle found under the search cap; NO_PATH_FOUND is not a nonexistence theorem",
            )
            report = replace(report, claims=(exist, *report.claims[1:]))
    if not existential_cycle_is_not_all_paths_cycle(report):
        all_paths = report.claim("all_paths_cycle")
        if all_paths is not None:
            all_paths = replace(all_paths, status=PathStatus.UNKNOWN)
            report = replace(report, claims=(*report.claims[:2], all_paths))
    if not certified_on_window_is_not_z_theorem(report) or not truncation_is_unknown_not_refuted(report):
        repaired = []
        for item in report.claims:
            if item.status is PathStatus.CERTIFIED_ON_WINDOW and "not a Z-theorem" not in item.statement:
                item = replace(item, statement=f"{item.statement}; not a Z-theorem")
            repaired.append(item)
        report = replace(report, claims=tuple(repaired))
    return report


def hypotheses_from_report(report: QuantifierReport) -> tuple[ResearchHypothesis, ...]:
    items: list[ResearchHypothesis] = []
    closest = _KNOWN.get(report.source_target, "")
    novelty, _ = _novelty(report.source_target)
    exists = report.claim("existential_cycle")
    if exists is not None:
        status = ResearchHypothesisStatus.CANDIDATE
        if exists.status is PathStatus.EXISTENTIAL_WITNESS:
            status = ResearchHypothesisStatus.SEARCH_SUPPORTED
        items.append(
            ResearchHypothesis(
                id=f"hyp:{report.source_target}:existential_cycle",
                statement=exists.statement or "there exists a legal cycle",
                target=report.source_target,
                source_target=report.source_target,
                evidence=exists.status.value,
                supporting_artifacts=("quantifiers.existential_cycle",),
                counterexamples=tuple(str(item) for item in exists.witness),
                confidence=0.55 if status is ResearchHypothesisStatus.SEARCH_SUPPORTED else 0.2,
                current_status=status,
                closest_known_result=closest,
                prior_art_matches=(closest,) if closest else (),
                proof_obligations=(
                    ProofObligation(
                        kind=ObligationKind.EXISTS_PATH,
                        statement="Need: a legal cyclic path; not all_paths_cycle",
                        status="WITNESSED" if exists.status is PathStatus.EXISTENTIAL_WITNESS else "OPEN",
                    ),
                ),
                novelty_status=novelty,
                kind=ClaimKind.REACHABLE,
                intended_scope=SearchScope.BOUNDED,
                cluster_id="branching_quantifier",
            )
        )
    termination = report.claim("universal_termination")
    if termination is not None:
        status = ResearchHypothesisStatus.CANDIDATE
        obl_status = "OPEN"
        if termination.status is PathStatus.REFUTED:
            status = ResearchHypothesisStatus.REFUTED
            obl_status = "REFUTED"
        elif termination.status is PathStatus.CERTIFIED_ON_WINDOW:
            status = ResearchHypothesisStatus.SEARCH_SUPPORTED
            obl_status = "WINDOW"
        elif termination.status is PathStatus.UNKNOWN:
            status = ResearchHypothesisStatus.CANDIDATE
        items.append(
            ResearchHypothesis(
                id=f"hyp:{report.source_target}:universal_termination",
                statement=termination.statement or "every legal path from the window terminates",
                target=report.source_target,
                source_target=report.source_target,
                evidence=termination.status.value,
                supporting_artifacts=("quantifiers.universal_termination",),
                counterexamples=tuple(str(item) for item in termination.counterexample),
                confidence=0.4 if status is ResearchHypothesisStatus.SEARCH_SUPPORTED else 0.2,
                current_status=status,
                closest_known_result=closest,
                prior_art_matches=(closest,) if closest else (),
                proof_obligations=(
                    ProofObligation(
                        kind=ObligationKind.ALL_PATHS,
                        statement="Need: every legal path terminates; CERTIFIED_ON_WINDOW is not a Z-theorem",
                        status=obl_status,
                    ),
                ),
                novelty_status=novelty,
                kind=ClaimKind.REACHABLE,
                intended_scope=SearchScope.BOUNDED,
                cluster_id="branching_quantifier",
            )
        )
    all_paths = report.claim("all_paths_cycle")
    if all_paths is not None:
        items.append(
            ResearchHypothesis(
                id=f"hyp:{report.source_target}:all_paths_cycle",
                statement=all_paths.statement,
                target=report.source_target,
                source_target=report.source_target,
                evidence=all_paths.status.value,
                supporting_artifacts=("quantifiers.all_paths_cycle",),
                confidence=0.1,
                current_status=ResearchHypothesisStatus.CANDIDATE,
                closest_known_result=closest,
                prior_art_matches=(closest,) if closest else (),
                proof_obligations=(
                    ProofObligation(
                        kind=ObligationKind.ALL_PATHS,
                        statement="Need: every legal path is cyclic; finite search leaves this UNKNOWN",
                        status="OPEN",
                    ),
                ),
                novelty_status=novelty,
                kind=ClaimKind.REACHABLE,
                intended_scope=SearchScope.BOUNDED,
                cluster_id="branching_quantifier",
            )
        )
    return tuple(items)
