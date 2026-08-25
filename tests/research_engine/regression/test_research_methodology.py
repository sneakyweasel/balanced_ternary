"""Research-methodology regressions for the v2 engine layers."""

from __future__ import annotations

from research.balanced_ternary.d_add_spec import DAddResidualSpec, minimized_state_count, raw_state_count
from research.collatz_finite_descent.blocks import all_odd_image, all_odd_witness
from research.collatz_finite_descent.spec import shortcut_spec
from research.multiplicative_residual.discovery import (
    doubled_product_report,
    pair_controls,
    raw_image,
    three_trit_report,
    triple_controls,
    two_trit_report,
)
from research.multiplicative_residual.spec import ProductResidualSpec
from research.prime_residual_complexity.sieve import sieve_census
from research.prime_residual_complexity.spec import PrimeSpec, SieveSpec
from research.signed_digit_residual.discovery import (
    finite_from_origin,
    geometry_perturbation,
    lambda1_reachable_radius,
    lambda2_reachable_radius,
    origin_complexity_profile,
    origin_reachable_report,
    reachable_from,
    residual_complexity,
)
from research.signed_digit_residual.spec import SignedDigitResidualSpec, signed_digit_spec
from research.signed_digit_residual_geometry.discovery import singleton_two_witness
from research.signed_digit_residual_minimality.discovery import (
    lambda3_translate_witness,
    predicted_sep_len,
    shortest_separating_word,
    val3_gap_plus_one_predictor,
)
from research_engine.attacks.envelope import (
    compare_envelope_to_reachable,
    compute_exact_reachable,
    envelope_from_interval,
    reachable_from_ints,
)
from research_engine.attacks.result import AttackContext, AttackStatus
from research_engine.attacks.separation import separate_states
from research_engine.attacks.symmetry import SymmetryCandidate, verify_symmetry
from research_engine.behavior.mealy import minimize_mealy_count
from research_engine.core.contribution import FactorizationStatus, check_control_factorization
from research_engine.core.observation import observe
from research_engine.core.semantics import CertificateKind, SearchScope
from research_engine.planner.orchestrator import AttackPlanner
from bt.transducers.mealy import minimize_mealy_count as bt_minimize_mealy_count


def test_signed_digit_observation_matches_emit():
    spec = signed_digit_spec(bound=2, gain=1)
    phase = spec.initial_phase()
    for state in (-1, 0, 1):
        for control in spec.digits:
            nxt, out = spec.emit(state, control)
            assert spec.transition((state,), control, phase) == (nxt,)
            assert observe(spec, (state,), control, phase) == out
            assert spec.raw_contribution(control) == control


def test_signed_digit_finite_phase_and_sharp_bounds():
    assert finite_from_origin(1, 2) is True
    assert finite_from_origin(2, 2) is True
    assert finite_from_origin(3, 2) is False
    for bound in range(0, 7):
        report = origin_reachable_report(bound, 1)
        radius = lambda1_reachable_radius(bound)
        assert report["reachable"] == tuple(range(-radius, radius + 1))
        assert report["reachable_count"] == 2 * radius + 1
    for bound in range(0, 6):
        report = origin_reachable_report(bound, 2)
        radius = lambda2_reachable_radius(bound)
        assert report["reachable"] == tuple(range(-radius, radius + 1, 2))


def test_envelope_preserves_known_holes():
    singleton = singleton_two_witness()
    envelope = envelope_from_interval(-1, 1, as_states=False)
    reached = reachable_from_ints(singleton["reachable"], as_states=False)
    comparison = compare_envelope_to_reachable(envelope, reached)
    assert set(singleton["reachable"]) == {0, 1}
    assert comparison.holes == frozenset({-1})

    sparse_g1 = geometry_perturbation()["sparse_2_g1"]
    box = envelope_from_interval(-1, 1, as_states=False)
    sparse_reached = reachable_from_ints(sparse_g1["reachable"], as_states=False)
    sparse_cmp = compare_envelope_to_reachable(box, sparse_reached)
    assert sparse_g1["reachable"] == (-1, 0, 1)
    assert sparse_cmp.envelope_equals_reachable is True

    sparse_g2 = geometry_perturbation()["sparse_2_g2"]
    box2 = envelope_from_interval(-2, 2, as_states=False)
    reached2 = reachable_from_ints(sparse_g2["reachable"], as_states=False)
    cmp2 = compare_envelope_to_reachable(box2, reached2)
    assert sparse_g2["reachable"] == (-2, 0, 2)
    assert cmp2.holes == frozenset({-1, 1})

    u2_g2 = origin_reachable_report(2, 2)
    u2_box = envelope_from_interval(-lambda2_reachable_radius(2), lambda2_reachable_radius(2), as_states=False)
    u2_reached = reachable_from_ints(u2_g2["reachable"], as_states=False)
    u2_cmp = compare_envelope_to_reachable(u2_box, u2_reached)
    assert u2_g2["reachable"] == (-2, 0, 2)
    assert u2_cmp.holes == frozenset({-1, 1})


def test_signed_digit_complexity_profile_keeps_counts_distinct():
    profile = origin_complexity_profile(2, 1)
    assert profile.control_count == 5
    assert profile.raw_contribution_count == 5
    assert profile.invariant_state_count == 3
    assert profile.reachable_state_count == 3
    assert profile.minimal_machine_count == 3
    assert profile.closure_status == "EXACT_CLOSURE"
    text = profile.format_report()
    assert "raw controls" in text
    assert "reachable residual states" in text
    assert "minimal Mealy states" in text


def test_product_factorization_keeps_four_counts_distinct():
    controls = pair_controls()
    spec = ProductResidualSpec()
    states = tuple((s,) for s in range(-4, 5))
    fact = check_control_factorization(spec, states=states, controls=controls)
    assert fact.status is FactorizationStatus.VERIFIED
    assert fact.control_count == 9
    assert fact.contribution_count == 3
    two = two_trit_report(1)
    assert two["raw_controls"] == 9
    assert two["raw_contribution_count"] == 3
    assert two["reachable_count"] == 1
    assert two["mealy"] == 1
    three = three_trit_report(1)
    assert len(triple_controls()) == 27
    assert raw_image(triple_controls()) == frozenset({-1, 0, 1})
    assert three["reachable"] == (0,)
    doubled = doubled_product_report(1)
    assert doubled["raw_contributions"] == (-2, 0, 2)
    assert doubled["reachable"] == (-1, 0, 1)
    assert residual_complexity(2) == 3
    assert reachable_from(0, (-2, -1, 0, 1, 2), 1) == frozenset({-1, 0, 1})


def test_engine_separation_matches_val3_predictor():
    spec = SignedDigitResidualSpec(bound=0, gain=1, start_remaining=8)
    result = separate_states(
        spec,
        (0,),
        (3,),
        predictor=val3_gap_plus_one_predictor,
    )
    word = shortest_separating_word(0, 3, (0,), 1)
    assert result.separated is True
    assert result.witness_word == word == (0, 0)
    assert result.witness_length == predicted_sep_len(0, 3) == 2
    assert result.predictor == ("v_3_gap_plus_one", 2)
    assert result.scope is SearchScope.EXACT


def test_lambda3_symmetry_is_global_but_not_origin_reachable():
    spec = SignedDigitResidualSpec(bound=1, gain=3, start_remaining=4)
    context = spec.attack_context()
    domain = frozenset((n,) for n in range(-3, 4))
    context = AttackContext(
        candidate_region=spec.candidate_region,
        symmetry_domain=domain,
        symmetry_candidates=(
            SymmetryCandidate(name="translate_3", kind="translate", params=(3,)),
        ),
    )
    report = verify_symmetry(
        spec,
        SymmetryCandidate(name="translate_3", kind="translate", params=(3,)),
        context,
    )
    assert report.verified is True
    assert spec.candidate_region == frozenset({(0,)})
    assert report.origin_reachable_extra_classes >= 1
    witness = lambda3_translate_witness()
    assert witness["sep_len"] is None or witness["word"] is None


def test_d_add_three_state_carry_and_factorization():
    assert raw_state_count(1) == 3
    assert minimized_state_count(1) == 3
    spec = DAddResidualSpec()
    closure = compute_exact_reachable(spec, spec.attack_context())
    assert closure.complete is True
    assert closure.size == 3
    assert closure.certificate_kind is CertificateKind.EXACT_CLOSURE
    fact = check_control_factorization(spec, states=tuple(spec.candidate_region))
    assert fact.status is FactorizationStatus.VERIFIED
    assert fact.control_count == 9
    assert fact.contribution_count == 5
    engine_count = minimize_mealy_count(
        tuple(spec.candidate_region),
        spec.legal_controls(spec.initial_state, spec.initial_phase()),
        lambda state, control: (spec.transition(state, control, spec.initial_phase()), spec.output(state, control)),
    )
    assert engine_count == bt_minimize_mealy_count(
        tuple(spec.candidate_region),
        spec.legal_controls(spec.initial_state, spec.initial_phase()),
        lambda state, control: (spec.transition(state, control, spec.initial_phase()), spec.output(state, control)),
    )
    assert engine_count == 3


def test_expanding_d_observation_is_next_residue():
    from research.balanced_ternary.expanding_spec import ExpandingDResidueSpec, T_CONTROL

    spec = ExpandingDResidueSpec()
    phase = spec.initial_phase()
    assert observe(spec, (1,), T_CONTROL, phase) == spec.transition((1,), T_CONTROL, phase)[0]


def test_collatz_all_odd_is_exact_unbounded_witness():
    for length in range(1, 8):
        n = all_odd_witness(length)
        image = all_odd_image(length)
        assert n == 2**length - 1
        assert image == 3**length - 1
    spec = shortcut_spec(start_remaining=6, start=27)
    assert not hasattr(spec, "output") or not callable(getattr(spec, "output", None))
    recon = AttackPlanner().run(spec, spec.attack_context())
    recon_result = next(item for item in recon.results if item.name == "reconnaissance")
    closure = next(item for item in recon.results if item.name == "closure")
    assert recon_result.status is AttackStatus.OBSERVATION
    assert recon_result.certificate_kind is CertificateKind.BOUNDED_RECONNAISSANCE
    assert closure.status is AttackStatus.INCONCLUSIVE
    assert closure.scope is SearchScope.BOUNDED
    assert closure.certificate_kind is None


def test_prime_sieve_closes_and_integer_prime_does_not():
    sieve = SieveSpec()
    census = sieve_census()
    assert census.minimized_states >= 1
    closure = compute_exact_reachable(sieve, sieve.attack_context())
    assert closure.complete is True
    assert closure.certificate_kind is CertificateKind.EXACT_CLOSURE
    assert observe(sieve, sieve.initial_state, 0, sieve.initial_phase()) is sieve.is_accepting(
        sieve.initial_state, sieve.initial_phase()
    )
    prime = PrimeSpec(state_cap=8, start_remaining=4)
    prime_closure = compute_exact_reachable(prime, prime.attack_context())
    assert prime_closure.complete is False
    assert prime_closure.status is AttackStatus.INCONCLUSIVE
