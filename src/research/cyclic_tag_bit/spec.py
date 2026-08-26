"""Hint-free one-variable integer map with a binary-word rewrite successor.

The integer is a sentinel encoding of a finite {0,1}-word. Successor is
the rewrite that drops the first symbol and appends 0 if it was 0, or 11
if it was 1. Empty has no successor. No literature names or affine hint.
"""

from __future__ import annotations

from dataclasses import dataclass

from research_engine.algebra.linear_functionals import LinearFunctional
from research_engine.attacks.result import AttackContext
from research_engine.core.phase import IntPhase
from research_engine.core.semantics import State

CONTROL = 0
INPUT_LENGTH = 16
INTEGER_STATE_CAP = 32
MAX_WORD_LEN = 64

TERMINAL = "TERMINAL"
DEFINED = "DEFINED"
TRANSITION_UNRESOLVED = "TRANSITION_UNRESOLVED"


def _require_int(value: int, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be int, got {type(value).__name__}")
    return value


def _require_word(word: str) -> str:
    if not isinstance(word, str) or any(ch not in "01" for ch in word):
        raise TypeError("word must be a {0,1}-string")
    return word


def encode_word(word: str) -> int:
    word = _require_word(word)
    if not word:
        return 0
    return (1 << len(word)) | int(word, 2)


def decode_word(n: int) -> str:
    n = _require_int(n, "n")
    if n <= 1:
        return ""
    width = n.bit_length() - 1
    return format(n & ((1 << width) - 1), f"0{width}b")


def word_length(n: int) -> int:
    return len(decode_word(n))


def over_budget(word: str) -> bool:
    return len(word) > MAX_WORD_LEN


def step_word(word: str) -> str | None:
    word = _require_word(word)
    if not word:
        return None
    if word[0] == "0":
        nxt = word[1:] + "0"
    else:
        nxt = word[1:] + "11"
    if over_budget(nxt):
        return None
    return nxt


def transition_status(n: int) -> str:
    n = _require_int(n, "n")
    word = decode_word(n)
    if not word:
        return TERMINAL
    if over_budget(word):
        return TRANSITION_UNRESOLVED
    if step_word(word) is None:
        return TRANSITION_UNRESOLVED
    return DEFINED


def map_images(n: int) -> tuple[int, ...]:
    n = _require_int(n, "n")
    nxt = step_word(decode_word(n))
    if nxt is None:
        return ()
    return (encode_word(nxt),)


@dataclass(frozen=True)
class WordRewriteSpec:
    """One-variable encoded-word dynamics with length observation and dummy control."""

    start_word: str
    start_remaining: int = INPUT_LENGTH
    state_cap: int = INTEGER_STATE_CAP
    name: str = ""
    dimension: int = 1

    def __post_init__(self):
        object.__setattr__(self, "start_word", _require_word(self.start_word))
        if self.start_remaining < 0:
            raise ValueError("start_remaining must be nonnegative")
        if self.state_cap < 1:
            raise ValueError("state_cap must be a positive integer")
        if not self.name:
            object.__setattr__(self, "name", "cyclic_tag_bit")

    @property
    def start(self) -> int:
        return encode_word(self.start_word)

    def successors(self, x: int) -> tuple[int, ...]:
        return map_images(x)

    @property
    def initial_state(self) -> State:
        return (self.start,)

    def transition(self, state: State, control: object, phase: IntPhase) -> State:
        del control, phase
        images = self.successors(int(state[0]))
        if len(images) != 1:
            raise ValueError(f"no unique successor at {state}")
        return (images[0],)

    def output(self, state: State, control: object, phase: IntPhase | None = None) -> int:
        del control, phase
        return word_length(int(state[0]))

    def legal_controls(self, state: State, phase: IntPhase) -> tuple[object, ...]:
        if phase.value <= 0:
            return ()
        n = int(state[0])
        if transition_status(n) != DEFINED:
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
        del state
        return phase.value == 0

    def initial_phase(self) -> IntPhase:
        return IntPhase(self.start_remaining)

    def canonicalize(self, state: State) -> State:
        return (int(state[0]),)

    def affine_system(self):
        return None

    def attack_context(self, **kwargs) -> AttackContext:
        images = self.successors(self.start)
        nxt = (images[0],) if len(images) == 1 else self.initial_state
        kwargs.setdefault("live_only", False)
        kwargs.setdefault("max_states", self.state_cap)
        kwargs.setdefault("max_steps", self.start_remaining)
        kwargs.setdefault("functional", LinearFunctional((1,)))
        kwargs.setdefault("pair", (self.initial_state, nxt))
        kwargs.setdefault("phases", (self.initial_phase(), IntPhase(0)))
        return AttackContext(**kwargs)


def map_spec(*, start_word: str = "101") -> WordRewriteSpec:
    return WordRewriteSpec(start_word=start_word, name="cyclic_tag_bit")
