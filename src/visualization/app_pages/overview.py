"""Orientation page for the Streamlit explorer."""

from __future__ import annotations

import streamlit as st


def overview_page() -> None:
    st.header("Research map")
    st.caption(
        "Exact arithmetic first. Bounded computations are labelled and are not proofs."
    )

    with st.container(horizontal=True):
        st.metric("Primary map", "Accelerated odd-only T", border=True)
        st.metric("Exact code state", "(m, K, C, R, M, X)", border=True)
        st.metric("Current geometry", "Affine center n*", border=True)

    left, right = st.columns(2)
    with left:
        with st.container(border=True):
            st.subheader("From integers to exponent codes")
            st.markdown(
                """
1. Balanced ternary gives an exact canonical word for every integer.
2. The accelerated map records `k = v2(3n+1)` at each odd step.
3. A finite valuation word defines one 2-adic cylinder and affine iterate.
4. The canonical realizer `R` has unique mixed-radix lift digits.
                """
            )
    with right:
        with st.container(border=True):
            st.subheader("Four coordinates and a center")
            st.markdown(
                """
- `R` is the refined 2-adic start representative.
- `M` is Kramer's least-positive 3-adic endpoint representative.
- `BT(R)` is an exact representation of `R`, not an independent coordinate.
- `n* = C/(2^K-3^m)` centers the affine iterate exactly.
                """
            )

    st.subheader("Implemented research layers")
    st.dataframe(
        [
            {
                "layer": "Balanced ternary",
                "object": "Canonical words, arithmetic, features, residue automata",
                "status": "PROVED / exact implementation",
            },
            {
                "layer": "Finite-state Collatz",
                "object": "2-adic valuation classifiers and division transducers",
                "status": "PROVED with bounded model sizes",
            },
            {
                "layer": "Exponent codes",
                "object": "Cylinders, affine formula, canonical realizers, lift digits",
                "status": "PROVED; key statements Lean verified",
            },
            {
                "layer": "Compatibility",
                "object": "2-adic start, 3-adic endpoint, BT(R), real drift",
                "status": "Exact; strong BT independence refuted",
            },
            {
                "layer": "Affine-center geometry",
                "object": "Fixed center, centered scaling, regime inequalities",
                "status": "Exact identities plus bounded censuses",
            },
        ],
        hide_index=True,
        width="stretch",
    )

    st.info(
        "Nothing in this explorer proves convergence of Collatz trajectories. "
        "Contraction of the homogeneous factor is not a Lyapunov function.",
        icon=":material/info:",
    )


overview_page()
