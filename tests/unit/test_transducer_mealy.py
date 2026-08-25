"""Generic Mealy minimization extracted from the /2^k product machine."""

from __future__ import annotations

from bt.transducers.divide_by_two_power import ALPHABET, DivideByTwoPowerTransducer, _compose_step
from bt.transducers.mealy import mealy_partition, minimize_mealy_count


def test_divide_by_two_power_still_minimizes_through_the_helper():
    machine = DivideByTwoPowerTransducer(1)
    reachable = machine.reachable_states()
    assert machine.minimized_state_count() == 3
    assert minimize_mealy_count(reachable, ALPHABET, _compose_step) == 3
    assert len(mealy_partition(reachable, ALPHABET, _compose_step)) == 3
