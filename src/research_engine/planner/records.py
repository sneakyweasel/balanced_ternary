"""Shared YAML experiment records. Not the named theorem ledger."""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

from research_engine.attacks.result import AttackResult, AttackStatus
from research_engine.core.semantics import SearchScope
from research_engine.planner.hypothesis import PriorArtStatus
from research_engine.planner.orchestrator import PlannerReport
from research_engine.verification.targets import TheoremTarget


def record_status(result: AttackResult, *, lean_theorem: str = "") -> str:
    """Map engine outcomes onto the Phase-0 record vocabulary."""
    if result.status is AttackStatus.REFUTED:
        return "REFUTED"
    if result.status is AttackStatus.OBSERVATION:
        return "OBSERVED"
    if result.status is AttackStatus.INCONCLUSIVE:
        return "OBSERVED"
    if result.status is AttackStatus.INAPPLICABLE:
        return "OBSERVED"
    if lean_theorem:
        return "LEAN_VERIFIED"
    if result.status is AttackStatus.SUPPORTED and result.scope is SearchScope.EXACT:
        return "EXACT"
    if result.status is AttackStatus.SUPPORTED:
        return "SUPPORTED"
    return "OBSERVED"


def render_record(
    result: AttackResult,
    *,
    problem: str,
    lean_theorem: str = "",
    prior_art_status: str = "",
    novelty_note: str = "",
    branch_status: str = "",
    witness: str = "",
) -> str:
    evidence = "; ".join(
        f"{key}={result.evidence[key]}"
        for key in (
            "union_size",
            "complete",
            "horizon",
            "state_cap",
            "leak_count",
            "observed_bound",
            "forcing_gcds",
            "quotient_count",
            "control_count",
            "contribution_count",
            "separated",
        )
        if key in result.evidence
    )
    counters = repr(tuple(result.counterexamples[:4]))
    kind = "" if result.certificate_kind is None else result.certificate_kind.value
    if not witness and result.counterexamples:
        witness = repr(result.counterexamples[0])
    return (
        f"problem: {problem}\n"
        f"attack: {result.name}\n"
        f"claim: {result.claim}\n"
        f"status: {record_status(result, lean_theorem=lean_theorem)}\n"
        f"scope: {result.scope.value}\n"
        f"evidence: {evidence}\n"
        f"counterexamples: {counters}\n"
        f"lean_theorem: {lean_theorem}\n"
        f"certificate_kind: {kind}\n"
        f"witness: {witness}\n"
        f"prior_art_status: {prior_art_status}\n"
        f"novelty_note: {novelty_note}\n"
        f"branch_status: {branch_status}\n"
    )


def write_records(
    report: PlannerReport,
    targets: Sequence[TheoremTarget],
    *,
    directory: Path,
    problem: str,
    prior_art_status: str = "",
    novelty_note: str = "",
    branch_status: str = "",
) -> tuple[Path, ...]:
    folder = directory
    folder.mkdir(parents=True, exist_ok=True)
    linked = {target.attack: target for target in targets if target.linked}
    written: list[Path] = []
    for result in report.results:
        target = linked.get(result.name)
        lean = ""
        if target is not None:
            lean = f"{target.lean_module}.{target.lean_theorem}"
        path = folder / f"{result.name}.yaml"
        path.write_text(
            render_record(
                result,
                problem=problem,
                lean_theorem=lean,
                prior_art_status=prior_art_status,
                novelty_note=novelty_note,
                branch_status=branch_status,
            ),
            encoding="utf-8",
        )
        written.append(path)
    skipped_lines = [
        f"problem: {problem}",
        "attack: skipped",
        "claim: inapplicable or deferred",
        "status: OBSERVED",
        "scope: BOUNDED",
        "evidence: "
        + "; ".join(f"{item.attack}={item.reason}" for item in report.skipped),
        "counterexamples: ()",
        "lean_theorem: ",
        "certificate_kind: ",
        "witness: ",
        f"prior_art_status: {prior_art_status or PriorArtStatus.UNKNOWN.value}",
        f"novelty_note: {novelty_note}",
        f"branch_status: {branch_status}",
    ]
    skip_path = folder / "skipped.yaml"
    skip_path.write_text("\n".join(skipped_lines) + "\n", encoding="utf-8")
    written.append(skip_path)
    return tuple(written)
