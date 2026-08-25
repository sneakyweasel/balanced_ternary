"""Target D candidate sketches. Scoring is not an autonomous mathematician."""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd
from typing import cast

from research.mx_plus_r.spec import mx_plus_r_spec
from research_engine.algebra.linear_functionals import LinearFunctional
from research_engine.attacks.result import AttackContext
from research_engine.benchmarks.hidden_piecewise import HiddenCongruenceASpec, HiddenParityCarrySpec
from research_engine.core.phase import IntPhase
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import State
from research_engine.diagnosis.corpus import ResearchCorpus
from research_engine.diagnosis.fingerprint import fingerprint_from_report
from research_engine.diagnosis.loop import diagnose
from research_engine.diagnosis.selection import score_candidate
from research_engine.diagnosis.types import CandidateSketch, SelectionReport
from research_engine.planner.orchestrator import AttackPlanner


CONTROL = 0


@dataclass(frozen=True)
class IntegerPolynomialSpec:
    """Integer polynomial map. The adapter does not name a Julia set."""

    start: int = 3
    start_remaining: int = 8
    state_cap: int = 16
    name: str = "integer_polynomial_x2_minus_2"
    dimension: int = 1

    def _step(self, x: int) -> int:
        return x * x - 2

    @property
    def initial_state(self) -> State:
        return (self.start,)

    def transition(self, state: State, control: object, phase: IntPhase) -> State:
        del control, phase
        return (self._step(int(state[0])),)

    def output(self, state: State, control: object, phase: IntPhase | None = None) -> int:
        del control, phase
        return int(state[0])

    def legal_controls(self, state: State, phase: IntPhase) -> tuple[object, ...]:
        del state
        if phase.value <= 0:
            return ()
        return (CONTROL,)

    def next_phase(self, phase: IntPhase, control: object) -> IntPhase:
        del control
        if phase.value > 0:
            return IntPhase(phase.value - 1)
        return phase

    def is_terminal(self, state: State, phase: IntPhase) -> bool:
        del state
        return phase.value >= 0

    def is_accepting(self, state: State, phase: IntPhase) -> bool:
        del state
        return phase.value == 0

    def initial_phase(self) -> IntPhase:
        return IntPhase(self.start_remaining)

    def canonicalize(self, state: State) -> State:
        return (int(state[0]),)

    def affine_system(self):
        return None

    def attack_context(self, **kwargs) -> AttackContext:
        nxt = (self._step(self.start),)
        kwargs.setdefault("live_only", False)
        kwargs.setdefault("max_states", self.state_cap)
        kwargs.setdefault("max_steps", self.start_remaining)
        kwargs.setdefault("functional", LinearFunctional((1,)))
        kwargs.setdefault("pair", (self.initial_state, nxt))
        return AttackContext(**kwargs)


def _reduce_pair(p: int, q: int) -> State:
    if q == 0:
        raise ValueError("denominator vanished")
    if q < 0:
        p, q = -p, -q
    g = gcd(abs(p), abs(q)) or 1
    return (p // g, q // g)


@dataclass(frozen=True)
class IntegerMobiusSpec:
    """Pair encoding of x ↦ (2x+1)/(x+1). No Möbius name is installed."""

    p0: int = 2
    q0: int = 1
    start_remaining: int = 8
    state_cap: int = 32
    name: str = "integer_mobius_pair"
    dimension: int = 2

    def __post_init__(self) -> None:
        if self.q0 == 0:
            raise ValueError("q0 must be nonzero")

    @property
    def initial_state(self) -> State:
        return _reduce_pair(self.p0, self.q0)

    def transition(self, state: State, control: object, phase: IntPhase) -> State:
        del control, phase
        p, q = int(state[0]), int(state[1])
        return _reduce_pair(2 * p + q, p + q)

    def output(self, state: State, control: object, phase: IntPhase | None = None) -> tuple[int, int]:
        del control, phase
        return (int(state[0]), int(state[1]))

    def legal_controls(self, state: State, phase: IntPhase) -> tuple[object, ...]:
        if phase.value <= 0:
            return ()
        if len(state) != 2 or int(state[1]) + int(state[0]) == 0:
            return ()
        return (CONTROL,)

    def next_phase(self, phase: IntPhase, control: object) -> IntPhase:
        del control
        if phase.value > 0:
            return IntPhase(phase.value - 1)
        return phase

    def is_terminal(self, state: State, phase: IntPhase) -> bool:
        del state
        return phase.value >= 0

    def is_accepting(self, state: State, phase: IntPhase) -> bool:
        del state
        return phase.value == 0

    def initial_phase(self) -> IntPhase:
        return IntPhase(self.start_remaining)

    def canonicalize(self, state: State) -> State:
        return _reduce_pair(int(state[0]), int(state[1]))

    def affine_system(self):
        return None

    def attack_context(self, **kwargs) -> AttackContext:
        nxt = self.transition(self.initial_state, CONTROL, self.initial_phase())
        kwargs.setdefault("live_only", False)
        kwargs.setdefault("max_states", self.state_cap)
        kwargs.setdefault("max_steps", self.start_remaining)
        kwargs.setdefault("functional", LinearFunctional((1, 1)))
        kwargs.setdefault("pair", (self.initial_state, nxt))
        return AttackContext(**kwargs)


@dataclass(frozen=True)
class SubtractiveEuclideanSpec:
    """Subtractive remainder dynamics. Quotient count is not a control."""

    a0: int = 1071
    b0: int = 462
    start_remaining: int = 24
    state_cap: int = 64
    name: str = "subtractive_euclidean"
    dimension: int = 2

    def __post_init__(self) -> None:
        if self.a0 <= self.b0 or self.b0 <= 0:
            raise ValueError("seed must satisfy a0 > b0 > 0")

    @property
    def initial_state(self) -> State:
        return (self.a0, self.b0)

    def transition(self, state: State, control: object, phase: IntPhase) -> State:
        del control, phase
        a, b = int(state[0]), int(state[1])
        if b == 0:
            return (a, 0)
        if a >= b:
            return (a - b, b)
        return (a, b - a)

    def output(self, state: State, control: object, phase: IntPhase | None = None) -> tuple[int, int]:
        del control, phase
        return (int(state[0]), int(state[1]))

    def legal_controls(self, state: State, phase: IntPhase) -> tuple[object, ...]:
        if phase.value <= 0:
            return ()
        if len(state) != 2 or int(state[1]) == 0 or int(state[0]) == 0:
            return ()
        return (CONTROL,)

    def next_phase(self, phase: IntPhase, control: object) -> IntPhase:
        del control
        if phase.value > 0:
            return IntPhase(phase.value - 1)
        return phase

    def is_terminal(self, state: State, phase: IntPhase) -> bool:
        if self.is_accepting(state, phase):
            return True
        return phase.value > 0

    def is_accepting(self, state: State, phase: IntPhase) -> bool:
        if phase.value == 0:
            return True
        return len(state) == 2 and (int(state[0]) == 0 or int(state[1]) == 0)

    def initial_phase(self) -> IntPhase:
        return IntPhase(self.start_remaining)

    def canonicalize(self, state: State) -> State:
        return (int(state[0]), int(state[1]))

    def affine_system(self):
        return None

    def attack_context(self, **kwargs) -> AttackContext:
        nxt = self.transition(self.initial_state, CONTROL, self.initial_phase())
        kwargs.setdefault("live_only", False)
        kwargs.setdefault("max_states", self.state_cap)
        kwargs.setdefault("max_steps", self.start_remaining)
        kwargs.setdefault("functional", LinearFunctional((1, 1)))
        kwargs.setdefault("pair", (self.initial_state, nxt))
        return AttackContext(**kwargs)


def _fingerprint_of(spec: ProblemSpec, corpus: ResearchCorpus):
    report = AttackPlanner().run(spec, spec.attack_context())
    return diagnose(spec, report, spec.attack_context(), corpus).fingerprint


def candidate_sketches(corpus: ResearchCorpus) -> tuple[CandidateSketch, ...]:
    seven = mx_plus_r_spec(7, 1)
    seven_fp = None
    for record in corpus.records:
        if record.target == seven.name:
            seven_fp = record.fingerprint
            break
    if seven_fp is None:
        seven_fp = _fingerprint_of(cast(ProblemSpec, seven), corpus)

    return (
        CandidateSketch(
            name=seven.name,
            fingerprint=seven_fp,
            exact_semantics=True,
            finite_horizon_tractable=True,
            lean_certifiable=True,
            prior_art_classified=True,
            experimental_cost=1.0,
        ),
        CandidateSketch(
            name="hidden_congruence_piecewise",
            fingerprint=_fingerprint_of(cast(ProblemSpec, HiddenCongruenceASpec()), corpus),
            exact_semantics=True,
            finite_horizon_tractable=True,
            lean_certifiable=True,
            prior_art_classified=True,
            experimental_cost=1.0,
        ),
        CandidateSketch(
            name="integer_mobius_pair",
            fingerprint=_fingerprint_of(cast(ProblemSpec, IntegerMobiusSpec()), corpus),
            exact_semantics=True,
            finite_horizon_tractable=True,
            lean_certifiable=True,
            prior_art_classified=True,
            experimental_cost=1.5,
        ),
        CandidateSketch(
            name="transducer_parity_carry",
            fingerprint=_fingerprint_of(cast(ProblemSpec, HiddenParityCarrySpec()), corpus),
            exact_semantics=True,
            finite_horizon_tractable=True,
            lean_certifiable=True,
            prior_art_classified=True,
            experimental_cost=1.0,
        ),
        CandidateSketch(
            name="integer_polynomial_x2_minus_2",
            fingerprint=_fingerprint_of(cast(ProblemSpec, IntegerPolynomialSpec()), corpus),
            exact_semantics=True,
            finite_horizon_tractable=True,
            lean_certifiable=True,
            prior_art_classified=True,
            experimental_cost=1.0,
        ),
        CandidateSketch(
            name="subtractive_euclidean",
            fingerprint=_fingerprint_of(cast(ProblemSpec, SubtractiveEuclideanSpec()), corpus),
            exact_semantics=True,
            finite_horizon_tractable=True,
            lean_certifiable=True,
            prior_art_classified=True,
            experimental_cost=1.0,
        ),
    )


def score_pool(corpus: ResearchCorpus) -> tuple[SelectionReport, ...]:
    reports = tuple(score_candidate(sketch, corpus) for sketch in candidate_sketches(corpus))
    return tuple(sorted(reports, key=lambda item: (-item.value, item.name)))


def spec_for_selection(name: str) -> ProblemSpec:
    mapping: dict[str, ProblemSpec] = {
        mx_plus_r_spec(7, 1).name: cast(ProblemSpec, mx_plus_r_spec(7, 1)),
        "hidden_congruence_piecewise": cast(ProblemSpec, HiddenCongruenceASpec()),
        "integer_mobius_pair": cast(ProblemSpec, IntegerMobiusSpec()),
        "transducer_parity_carry": cast(ProblemSpec, HiddenParityCarrySpec()),
        "integer_polynomial_x2_minus_2": cast(ProblemSpec, IntegerPolynomialSpec()),
        "subtractive_euclidean": cast(ProblemSpec, SubtractiveEuclideanSpec()),
    }
    if name not in mapping:
        raise KeyError(name)
    return mapping[name]


def fingerprint_from_spec(spec: ProblemSpec):
    report = AttackPlanner().run(spec, spec.attack_context())
    return fingerprint_from_report(spec, report, spec.attack_context())
