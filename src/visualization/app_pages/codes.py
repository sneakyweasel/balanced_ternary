"""Exponent-code compatibility and affine-center pages."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from visualization.views import (
    AffineCenterCensusView,
    ExponentCodeView,
    affine_center_census_view,
    exponent_code_view,
)


@st.cache_data(max_entries=256, show_spinner=False)
def _cached_code_geometry(valuations: str, critical_gap: int) -> ExponentCodeView:
    return exponent_code_view(valuations, critical_gap=critical_gap)


@st.cache_data(max_entries=24, show_spinner=False)
def _cached_census(
    max_length: int,
    max_k: int,
    critical_gap: int,
    closest_count: int,
) -> AffineCenterCensusView:
    return affine_center_census_view(
        max_length, max_k, critical_gap, closest_count
    )


def exponent_code_page() -> None:
    st.header("Exponent-code geometry")
    st.caption(
        "One finite valuation code viewed through exact 2-adic, 3-adic, "
        "balanced-ternary, drift, lift, and affine-center coordinates."
    )
    if "code_valuations" not in st.session_state:
        st.session_state.code_valuations = str(st.query_params.get("ks", "1,4,2"))

    with st.form("exponent_code_form"):
        left, right = st.columns([3, 1], vertical_alignment="bottom")
        valuations = left.text_input(
            "Valuations k0,k1,...",
            key="code_valuations",
            help="Every valuation must be a positive integer.",
        )
        critical_gap = int(
            right.number_input(
                "Critical gap",
                min_value=0,
                value=1,
                step=1,
                help="Codes with |2^K-3^m| at most this value are critical-near.",
            )
        )
        submitted = st.form_submit_button(
            "Compute exact state", icon=":material/calculate:"
        )

    if not submitted and "code_geometry_result" not in st.session_state:
        st.caption("Submit a nonempty valuation code.")
        return
    if submitted:
        try:
            result = _cached_code_geometry(valuations, critical_gap)
        except (ArithmeticError, TypeError, ValueError) as exc:
            st.error(str(exc))
            return
        st.session_state.code_geometry_result = result
        st.query_params["ks"] = ",".join(map(str, result.valuations))
    view: ExponentCodeView = st.session_state.code_geometry_result

    st.subheader("Exact compatibility coordinates")
    with st.container(horizontal=True):
        for label, value in view.coordinates:
            st.metric(label, value, border=True)
    st.code(f"BT(R) = {view.balanced_ternary_R}", language="text")
    st.caption(
        "R is the refined start representative; r follows Kramer's modulus "
        "2^K convention; M is the least-positive endpoint residue modulo 3^m; "
        "X is the canonical endpoint."
    )

    left, right = st.columns(2)
    with left:
        with st.container(border=True):
            st.subheader("Lift and drift")
            st.metric("Exact drift 3^m / 2^K", view.exact_drift)
            st.code(
                "lift digits = " + repr(view.lift_digits),
                language="text",
            )
            st.caption(
                "Lift digits are exact mixed-radix blocks of the canonical "
                "2-adic representative."
            )
    with right:
        with st.container(border=True):
            st.subheader("Affine center")
            st.badge(
                view.regime,
                color="blue" if view.regime == "contracting" else "orange",
            )
            st.dataframe(
                pd.DataFrame(view.affine_rows, columns=["quantity", "exact value"]),
                hide_index=True,
                width="stretch",
            )

    st.subheader("Theorem-backed checks")
    st.dataframe(
        pd.DataFrame(view.inequalities, columns=["identity or inequality", "holds"]),
        hide_index=True,
        width="stretch",
        column_config={
            "holds": st.column_config.CheckboxColumn("Holds", disabled=True)
        },
    )
    with st.expander("Kramer floating diagnostics", icon=":material/query_stats:"):
        st.dataframe(
            pd.DataFrame(view.floating_rates, columns=["estimate", "value"]),
            hide_index=True,
            width="stretch",
        )
        st.caption(
            "Only d, rho_r, and rho_M in this section are floating estimates. "
            "All coordinates and center quantities above are exact."
        )


def affine_census_page() -> None:
    st.header("Affine-center census")
    st.caption(
        "Exhaustive finite products of valuation codes. Rows use exact integers "
        "and rationals; universality labels apply only to the submitted census."
    )
    with st.form("affine_census_form"):
        c1, c2, c3, c4 = st.columns(4, vertical_alignment="bottom")
        max_length = int(c1.slider("Maximum length", 1, 6, 4))
        max_k = int(c2.slider("Maximum valuation", 1, 5, 4))
        critical_gap = int(c3.number_input("Critical gap", min_value=0, value=1))
        closest_count = int(
            c4.slider("Near-critical rows", 1, 50, 12)
        )
        submitted = st.form_submit_button(
            "Run bounded census", icon=":material/play_arrow:"
        )
    if not submitted and "affine_census_result" not in st.session_state:
        st.caption("Submit bounded parameters to run the census in memory.")
        return
    if submitted:
        with st.status(
            "Enumerating exact affine centers", expanded=False
        ) as status:
            result = _cached_census(
                max_length, max_k, critical_gap, closest_count
            )
            st.session_state.affine_census_result = result
            status.update(label="Census complete", state="complete")
    view: AffineCenterCensusView = st.session_state.affine_census_result

    with st.container(horizontal=True):
        st.metric("Exact rows", view.row_count, border=True)
        for partition, count in view.partition_counts:
            st.metric(partition, count, border=True)

    mode = st.segmented_control(
        "Census result",
        ("Near-critical", "Proved checks", "Candidate orders"),
        default="Near-critical",
        key="affine_census_mode",
    )
    if mode == "Near-critical":
        st.dataframe(view.closest_rows, hide_index=True, width="stretch")
        st.caption("Sorted by exact |2^K-3^m|, then by code size.")
    elif mode == "Proved checks":
        st.dataframe(view.inequality_rows, hide_index=True, width="stretch")
        st.caption(
            "These relations are theorem-backed; the census is a regression check."
        )
    else:
        st.dataframe(
            view.coordinate_order_rows,
            hide_index=True,
            width="stretch",
        )
        st.caption(
            "Candidate coordinate orders are bounded computations. Smallest "
            "false codes preserve counterexamples to universal readings."
        )
