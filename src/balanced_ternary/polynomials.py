"""Compatibility shim. Core: :mod:`bt.polynomials`. Mahler: research."""

from bt.polynomials import *  # noqa: F403


def mahler_measure(*args, **kwargs):
    from research.sparse_polynomials import mahler_measure as _impl

    return _impl(*args, **kwargs)


def prime_polynomial_factors(*args, **kwargs):
    from research.sparse_polynomials import prime_polynomial_factors as _impl

    return _impl(*args, **kwargs)
