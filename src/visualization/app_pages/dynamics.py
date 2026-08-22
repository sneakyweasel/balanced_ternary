"""Integer-level Collatz explorer pages."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from bt.representation import encode
from visualization.views import (
    NumberView,
    TrajectoryView,
    WarpView,
    inverse_tree_view,
    number_view,
    trajectory_view,
    warp_view,
)


@st.cache_data(max_entries=128, show_spinner=False)
def _cached_number(n: int) -> NumberView:
    return number_view(n)


@st.cache_data(max_entries=128, show_spinner=False)
def _cached_trajectory(n: int, max_steps: int) -> TrajectoryView:
    return trajectory_view(n, max_steps)


@st.cache_data(max_entries=128, show_spinner=False)
def _cached_inverse(root: int, depth: int, k_max: int) -> dict[str, object]:
    return inverse_tree_view(root, depth, k_max)


@st.cache_data(max_entries=128, show_spinner=False)
def _cached_warp(n: int) -> WarpView:
    return warp_view(n)


def _odd_input(label: str, *, key: str) -> int:
    default = int(st.session_state.get("shared_odd_n", 27))
    value = int(st.number_input(label, min_value=1, value=default, step=2, key=key))
    st.session_state.shared_odd_n = value
    st.session_state.shared_integer = value
    st.session_state.shared_word = encode(value).word()
    return value


def number_page() -> None:
    n = _odd_input("Positive odd integer", key="number_n")
    if n % 2 == 0:
        st.error("The accelerated map requires an odd integer.")
        return
    view = _cached_number(n)

    with st.container(horizontal=True):
        st.metric("n", view.n, border=True)
        st.metric("3n+1", view.three_n_plus_one, border=True)
        st.metric("v2(3n+1)", view.v2, border=True)
        st.metric("T(n)", view.T_n, border=True)

    left, right = st.columns(2)
    with left:
        st.subheader("Balanced-ternary words")
        st.code(
            "\n".join(
                (
                    f"BT(n)     {view.bt_n}",
                    f"BT(n)+    {view.append_plus_word}",
                    f"BT(3n+1)  {view.bt_y}",
                    f"BT(T(n))  {view.bt_t}",
                )
            ),
            language="text",
        )
    with right:
        st.subheader("Exact check")
        if view.append_plus_matches and view.features_match:
            st.badge(
                "Append-plus identity verified",
                icon=":material/check:",
                color="green",
            )
        else:
            st.error("Internal identity mismatch.")
        st.caption("Digits are displayed most-significant first.")

    st.subheader("Feature transition")
    st.dataframe(
        pd.DataFrame(
            view.feature_rows,
            columns=["feature", "n", "3n+1", "T(n)", "delta T-n"],
        ),
        hide_index=True,
        width="stretch",
    )
    st.caption(
        "Deltas are F(T(n)) - F(n). They are exact feature changes, not "
        "Lyapunov decreases."
    )


def trajectory_page() -> None:
    st.header("Accelerated trajectory")
    with st.form("trajectory_form"):
        left, right = st.columns(2, vertical_alignment="bottom")
        default = int(st.session_state.get("shared_odd_n", 27))
        n = int(
            left.number_input(
                "Start (odd)", min_value=1, value=default, step=2, key="trajectory_n"
            )
        )
        max_steps = int(right.slider("Maximum steps", 1, 200, 30))
        submitted = st.form_submit_button(
            "Compute trajectory", icon=":material/play_arrow:"
        )
    if not submitted and "trajectory_result" not in st.session_state:
        st.caption("Submit the bounds to compute one exact truncated trajectory.")
        return
    if submitted:
        if n % 2 == 0:
            st.error("The start must be odd.")
            return
        st.session_state.shared_odd_n = n
        st.session_state.trajectory_result = _cached_trajectory(n, max_steps)
    view: TrajectoryView = st.session_state.trajectory_result

    with st.container(horizontal=True):
        st.metric("Values", len(view.values), border=True)
        st.metric("Reached 1", str(view.reached_one).lower(), border=True)
        st.metric("Truncated", str(view.truncated).lower(), border=True)

    if not view.rows:
        st.caption("No accelerated steps were required.")
        return
    rows = pd.DataFrame(view.rows)
    st.line_chart(pd.DataFrame({"odd value": view.values}), y="odd value")
    st.dataframe(rows, hide_index=True, width="stretch")
    st.bar_chart(rows, x="i", y="v2", x_label="Step", y_label="v2(3n+1)")
    st.caption("This is a finite orbit computation, not evidence of convergence.")


def inverse_tree_page() -> None:
    st.header("Inverse accelerated tree")
    with st.form("inverse_tree_form"):
        c1, c2, c3 = st.columns(3, vertical_alignment="bottom")
        root = int(c1.number_input("Root (odd)", min_value=1, value=1, step=2))
        depth = int(c2.slider("Depth", 0, 6, 2))
        k_max = int(c3.slider("Maximum valuation", 2, 24, 10))
        submitted = st.form_submit_button(
            "Build inverse tree", icon=":material/account_tree:"
        )
    if not submitted and "inverse_tree_result" not in st.session_state:
        st.caption("Submit finite bounds to build the inverse tree.")
        return
    if submitted:
        if root % 2 == 0:
            st.error("The root must be odd.")
            return
        st.session_state.inverse_tree_result = _cached_inverse(root, depth, k_max)
    payload = st.session_state.inverse_tree_result

    with st.container(horizontal=True):
        st.metric("Nodes", payload["node_count"], border=True)
        st.metric("Truncated", str(payload["truncated"]).lower(), border=True)
    st.code(str(payload["formatted"]), language="text")
    st.caption("The self-map 1 -> 1 (k=2) is recorded as a cycle and not expanded.")


def warp_page() -> None:
    st.caption(
        "W is OEIS A134028: reverse the canonical balanced-ternary word, then "
        "decode. T is defined only on positive odd integers."
    )
    default = int(st.session_state.get("shared_odd_n", 27))
    n = int(st.number_input("Integer n", value=default, step=1, key="warp_n"))
    if n % 2 == 1 and n > 0:
        st.session_state.shared_odd_n = n
    view = _cached_warp(n)

    with st.container(horizontal=True):
        st.metric("n", view.n, border=True)
        st.metric("W(n)", view.W_n, border=True)
        st.metric("T(n)", "undefined" if view.T_n is None else view.T_n, border=True)
        st.metric(
            "Comm_WT",
            "undefined" if view.Comm_WT is None else view.Comm_WT,
            border=True,
        )

    left, right = st.columns(2)
    with left:
        st.subheader("Words")
        st.code(
            "\n".join(
                (
                    f"BT(n)      {view.bt_n}",
                    f"BT(W(n))   {view.bt_W}",
                    f"palindrome {str(view.palindrome_n).lower()}",
                    f"s3(n)      {view.s3_n}",
                    f"L3(n)      {view.L3_n}",
                )
            ),
            language="text",
        )
    with right:
        st.subheader("Domain")
        if view.t_defined:
            st.badge("T(n) defined", icon=":material/check:", color="green")
        else:
            st.badge("T(n) undefined", icon=":material/block:", color="orange")
        if view.t_of_W_defined:
            st.badge("T(W(n)) defined", icon=":material/check:", color="green")
        else:
            st.badge("T(W(n)) undefined", icon=":material/block:", color="orange")
        st.caption(
            f"W(T(n)) = {view.W_T}  ·  T(W(n)) = {view.T_W}  ·  "
            f"delta_s = {view.delta_s}  ·  delta_L = {view.delta_L}"
        )

    st.info(
        "W is not an involution when 3 divides n ≠ 0. Commutation with T is "
        "not a theorem; the smallest counterexample is n = 3.",
        icon=":material/info:",
    )
