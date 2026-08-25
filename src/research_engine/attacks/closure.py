"""Capped exhaustive residual-state closure.

Queue exhaustion is an exact finite reachable set at the frozen initial
phase. Hitting the state cap is not infinitude, and a complete countdown
DAG is not this certificate.
"""

from __future__ import annotations

from collections import deque

from research_engine.attacks.result import AttackContext, AttackResult, AttackStatus
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import CertificateKind, ClaimKind, SearchScope, State

DEFAULT_CLOSURE_STATE_CAP = 256


def _word_to(parents: dict[State, tuple[State, object] | None], state: State) -> tuple[object, ...]:
    path: list[object] = []
    current = state
    while True:
        record = parents.get(current)
        if record is None:
            break
        prev, control = record
        path.append(control)
        current = prev
    path.reverse()
    return tuple(path)


class ExhaustiveClosureAttack:
    """BFS of residual states at the initial phase, independent of countdown."""

    name = "closure"

    def applicable(self, spec: ProblemSpec, context: AttackContext) -> bool:
        del spec, context
        return True

    def run(self, spec: ProblemSpec, context: AttackContext) -> AttackResult:
        cap = context.max_states if context.max_states is not None else DEFAULT_CLOSURE_STATE_CAP
        start = spec.canonicalize(spec.initial_state)
        phase = spec.initial_phase()
        seen: set[State] = {start}
        queue: deque[State] = deque([start])
        parents: dict[State, tuple[State, object] | None] = {start: None}
        table: dict[State, tuple[tuple[object, State], ...]] = {}
        truncated = False

        while queue:
            if len(seen) > cap:
                truncated = True
                break
            state = queue.popleft()
            edges: list[tuple[object, State]] = []
            for control in spec.legal_controls(state, phase):
                nxt = spec.canonicalize(spec.transition(state, control, phase))
                edges.append((control, nxt))
                if nxt in seen:
                    continue
                seen.add(nxt)
                parents[nxt] = (state, control)
                queue.append(nxt)
                if len(seen) > cap:
                    truncated = True
                    break
            table[state] = tuple(edges)
            if truncated:
                break

        union = frozenset(seen)
        witnesses = {state: _word_to(parents, state) for state in union}
        evidence = {
            "union_size": len(union),
            "complete": not truncated,
            "state_cap": cap,
            "union": tuple(sorted(union)),
            "witnesses": tuple(sorted((state, word) for state, word in witnesses.items())),
            "transition_rows": len(table),
        }
        if truncated:
            return AttackResult(
                name=self.name,
                status=AttackStatus.INCONCLUSIVE,
                kind=ClaimKind.REACHABLE,
                scope=SearchScope.BOUNDED,
                claim=(
                    f"residual-state BFS hit the cap {cap}; "
                    "this is not infinitude and not a finite-closure theorem"
                ),
                evidence=evidence,
                recommended_next_attacks=("reconnaissance", "reverse"),
            )
        certificate = {
            "states": tuple(sorted(union)),
            "size": len(union),
            "witnesses": tuple(sorted((state, word) for state, word in witnesses.items())),
        }
        return AttackResult(
            name=self.name,
            status=AttackStatus.SUPPORTED,
            kind=ClaimKind.REACHABLE,
            scope=SearchScope.EXACT,
            claim=(
                f"exact residual closure has size {len(union)}; "
                "queue exhaustion at the frozen initial phase, not a countdown DAG"
            ),
            evidence=evidence,
            certificates=(certificate,),
            recommended_next_attacks=("reverse", "affine"),
            certificate_kind=CertificateKind.EXACT_CLOSURE,
        )
