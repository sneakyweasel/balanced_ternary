"""Mismatched-width cubic quotient Q_{t,K,W}."""

from __future__ import annotations

import io
from contextlib import redirect_stdout

from balanced_ternary.cli import main
from research.residuals.cubic_fibres import prefixes_at
from research.residuals.cubic_n0_reduction import n0_fibre_after_n21, n0_scaled
from research.residuals.mismatched_cubic import (
    bal_digits,
    q_compare,
    q_eq,
    q_eq_iff,
    q_fibre,
    q_image,
    q_int,
    q_mod,
    q_params,
    q_prefix_state_counts,
    q_recon_delta,
    q_report,
    q_split_high,
    q_val_int,
    q_visibility,
    unit_extra_collisions,
    visibility_bound,
)
from bt.calculus.quadratic import iter_dz


def test_reconstruction_criterion():
    for t in range(0, 4):
        for K in range(1, 5):
            for u in range(-20, 21):
                for v in range(-20, 21):
                    assert q_eq(t, K, u, v) is q_eq_iff(t, K, u, v)
                    assert q_recon_delta(t, u, v) == 3**t * (q_int(t, u) - q_int(t, v))


def test_bal_plus_quotient():
    for t in (0, 1, 2, 3):
        for z in range(-40, 41):
            assert z == bal_digits(z, t) + 3**t * iter_dz(z, t)


def test_two_regime_on_u():
    for t in range(0, 6):
        for u in range(-30, 31):
            assert q_int(t, u) == q_val_int(t, u)


def test_high_trit_expansion():
    for t in range(0, 4):
        for a in range(-6, 7):
            for b in range(-4, 5):
                assert q_int(t, a + 3**t * b) == q_split_high(t, a, b)


def test_exhausted_specialization():
    t, K, W = q_params(9, 2)
    assert (t, K, W) == (0, 9, 4)
    for u in prefixes_at(W):
        assert n0_scaled(u, 9, 2) == q_int(t, u)
        assert q_mod(t, K, u) == (u**3) % (3**9)


def test_r1_params():
    t, K, W = q_params(8, 1)
    assert t == 3
    assert W == 5
    assert W - t == 2


def test_zero_fibre_in_q_language():
    # (r,k)=(2,9): Q(u)=u^3 mod 3^9 on P_4. Full Newton fibre of 0 is {-243,0,243}.
    t, K, W = q_params(9, 2)
    zeros = [u for u in prefixes_at(W) if q_mod(t, K, u) == 0]
    assert 0 in zeros
    assert 27 in zeros and -27 in zeros
    assert n0_fibre_after_n21(0, 9, 2) == [-243, 0, 243]


def test_visibility_sufficient_not_necessary():
    t, K, W = 1, 3, 4
    s = visibility_bound(t, K)
    for u in prefixes_at(W):
        for w in range(-1, 2):
            v = u + w * (3**s)
            if abs(v) > (3**W - 1) // 2:
                continue
            assert q_eq(t, K, u, v)
    extras = unit_extra_collisions(t, K, W)
    for u, v in extras:
        assert q_eq_iff(t, K, u, v)


def test_cube_mod_not_necessary():
    # Reconstruction, not raw cube congruence, is the exact law.
    found = False
    for t, K in ((1, 2), (2, 3)):
        for u in range(-15, 16):
            for v in range(u + 1, 16):
                if q_eq(t, K, u, v) and (u**3 - v**3) % (3 ** (t + K)) != 0:
                    found = True
                    break
            if found:
                break
        if found:
            break
    assert found


def test_report_and_cli():
    rec = q_report(0, 9, 4)
    assert rec["classes"] >= 1
    assert rec["width_excess"] == 4

    def _run(*args: str) -> str:
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = main(["calculus", *args])
        assert code == 0
        return buf.getvalue()

    out = _run("cubic-quotient", "--t", "0", "--modulus", "9", "--width", "4")
    assert "t = 0" in out
    assert "K = 9" in out
    assert "W = 4" in out
    one = _run("cubic-quotient-fibre", "0", "--t", "0", "--modulus", "9", "--width", "4")
    assert "fibre_size =" in one
    cmp_ = _run("compare-cubic-quotient", "27", "0", "--t", "0", "--modulus", "9")
    assert "equal = True" in cmp_
    still = _run("n0-reduction", "--k", "8", "--deficit", "1")
    assert "formula ok = True" in still


def test_image_counts_r2_k9():
    image = q_image(0, 9, 4)
    assert 0 in image
    assert set(image[0]) >= {-27, 0, 27}


def test_r3_exhausted_params():
    t, K, W = q_params(13, 3)
    assert (t, K, W) == (0, 13, 6)
    assert W - t == 6


def test_unexhausted_not_q():
    try:
        q_params(9, 3)
        raise AssertionError("k=9, r=3 is unexhausted")
    except ValueError:
        pass


def test_visibility_zero_fibre():
    vis = q_visibility(0, 9, 4, 0)
    assert vis["fibre"] == [-27, 0, 27]
    assert vis["agrees_mod_s"] is False
    assert vis["common_mod_exp"] == 3
    assert vis["cube_mod_necessary_on_fibre"] is True


def test_unit_extra_collisions_r1():
    extras = unit_extra_collisions(1, 6, 3)
    assert (-13, -2) in extras
    assert (-1, 1) in extras
    for u, v in extras:
        assert u % 3 != v % 3


def test_same_bal_makes_cube_mod_necessary():
    t, K = 2, 3
    for u in range(-12, 13):
        for v in range(u, 13):
            if bal_digits(u**3, t) != bal_digits(v**3, t):
                continue
            assert q_eq(t, K, u, v) is ((u**3 - v**3) % (3 ** (t + K)) == 0)


def test_prefix_state_counts_shape():
    counts = q_prefix_state_counts(0, 5, 2)
    assert counts == [1, 3, 9]


def test_compare_cli_chain():
    def _run(*args: str) -> str:
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = main(["calculus", *args])
        assert code == 0
        return buf.getvalue()

    out = _run(
        "compare-cubic-quotient",
        "-13",
        "-2",
        "13",
        "--t",
        "1",
        "--modulus",
        "6",
    )
    assert out.count("equal =") == 2
    fib = _run("cubic-quotient-fibre", "0", "--t", "0", "--modulus", "9", "--width", "4")
    assert "visibility s bound" in fib
    assert "discarded bal_t values" in fib
