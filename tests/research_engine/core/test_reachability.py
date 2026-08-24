"""Forward/reverse search results carry an explicit bounded scope."""

from __future__ import annotations

from dataclasses import dataclass

from research_engine.acceptance.live import filter_terminal, live_intersection
from research_engine.acceptance.suffix import is_co_live, is_suffix_accepted, live_extensions
from research_engine.core.phase import IntPhase
from research_engine.core.semantics import ClaimKind, SearchScope
from research_engine.reachability.forward import forward_search
from research_engine.reachability.reverse import reverse_closure, reverse_predecessors_among
from research_engine.reachability.shortest import shortest_word


@dataclass(frozen=True)
class CountdownSpec:
    """One-dimensional countdown. Every positive remaining is terminal."""

    name: str = "countdown_toy"
    dimension: int = 1
    initial_state: tuple[int, ...] = (0,)
    start_remaining: int = 2

    def transition(self, state: tuple[int, ...], control: int, phase: IntPhase) -> tuple[int, ...]:
        del phase
        return (state[0] + control,)

    def legal_controls(self, state: tuple[int, ...], phase: IntPhase) -> tuple[int, ...]:
        del state
        if phase.value <= 0:
            return ()
        return (-1, 0, 1)

    def next_phase(self, phase: IntPhase, control: int) -> IntPhase:
        del control
        return IntPhase(phase.value - 1)

    def is_terminal(self, state: tuple[int, ...], phase: IntPhase) -> bool:
        del state
        return True

    def is_accepting(self, state: tuple[int, ...], phase: IntPhase) -> bool:
        return phase.value == 0 and state[0] == 0

    def initial_phase(self) -> IntPhase:
        return IntPhase(self.start_remaining)

    def canonicalize(self, state: tuple[int, ...]) -> tuple[int, ...]:
        return tuple(state)


def test_forward_search_is_bounded_and_distinguishes_layer_from_union():
    spec = CountdownSpec()
    result = forward_search(spec, live_only=True)
    assert result.scope == SearchScope.BOUNDED
    assert result.kind == ClaimKind.LIVE_SLICE
    assert result.complete
    assert result.horizon == 2
    start_layer = result.layer_at(IntPhase(2))
    mid_layer = result.layer_at(IntPhase(1))
    end_layer = result.layer_at(IntPhase(0))
    assert start_layer == frozenset({(0,)})
    assert (0,) in end_layer
    assert result.union == start_layer | mid_layer | end_layer
    assert start_layer != result.union
    assert result.terminal_image == frozenset({(0,)})


def test_shortest_word_reaches_origin_at_remaining_zero():
    spec = CountdownSpec()
    result = forward_search(spec, live_only=True)
    word = shortest_word(result, (0,), IntPhase(0))
    assert word is not None
    assert len(word) == 2
    assert sum(word) == 0
    assert is_suffix_accepted(spec, spec.initial_state, spec.initial_phase(), word)


def test_live_slice_is_not_co_reachable_and_not_live():
    spec = CountdownSpec()
    reachable = forward_search(spec, live_only=False)
    slice_result = filter_terminal(spec, reachable)
    co_reachable = reverse_closure(
        ((0,),),
        lambda state: (),
    )
    live = live_intersection(reachable, co_reachable)
    assert slice_result.kind == ClaimKind.LIVE_SLICE
    assert co_reachable.kind == ClaimKind.CO_REACHABLE
    assert live.kind == ClaimKind.LIVE
    assert co_reachable.scope == SearchScope.EXACT
    assert live.union == frozenset({(0,)})
    assert slice_result.union != live.union


def test_reverse_predecessors_among_inverts_a_step():
    spec = CountdownSpec()
    hits = reverse_predecessors_among(
        spec,
        (1,),
        IntPhase(1),
        IntPhase(2),
        ((0,), (1,), (2,)),
    )
    assert ((0,), 1) in hits
    assert set(hits) == {((0,), 1), ((1,), 0), ((2,), -1)}


def test_live_extensions_and_illegal_suffix():
    spec = CountdownSpec()
    assert live_extensions(spec, (0,), IntPhase(2)) == (-1, 0, 1)
    assert live_extensions(spec, (0,), IntPhase(0)) == ()
    assert is_co_live(spec, (0,), IntPhase(2), max_depth=2)
    assert is_suffix_accepted(spec, (0,), IntPhase(2), (1, 0)) is False
