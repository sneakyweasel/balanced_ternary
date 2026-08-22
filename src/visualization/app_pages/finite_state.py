"""Finite-state model and language pages."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from visualization.views import (
    automaton_view,
    complexity_spectrum_rows,
    cylinder_view,
    entropy_comparison_rows,
    joint_graph_view,
    odd_part_trace,
    symbolic_graph_rows,
    synchronizing_context_view,
    transducer_complexity_rows,
    valuation_prefix_view,
)


@st.cache_data(max_entries=64, show_spinner=False)
def _cached_automaton(precision: int, n: int) -> dict[str, object]:
    return automaton_view(precision, n)


@st.cache_data(max_entries=64, show_spinner=False)
def _cached_transducer(x: int, k_max: int) -> tuple[dict[str, object], list[dict[str, int]]]:
    return odd_part_trace(x), transducer_complexity_rows(k_max)


@st.cache_data(max_entries=64, show_spinner=False)
def _cached_valuation(
    precision: int, k_max: int, max_length: int
) -> dict[str, object]:
    return valuation_prefix_view(precision, k_max, max_length)


@st.cache_data(max_entries=128, show_spinner=False)
def _cached_cylinder(ks: str, leftover: int) -> dict[str, object]:
    return cylinder_view(ks, leftover_q=leftover)


@st.cache_data(max_entries=64, show_spinner=False)
def _cached_language_tables(
    length: int, k_max: int
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    return entropy_comparison_rows(length), complexity_spectrum_rows(k_max)


@st.cache_data(max_entries=32, show_spinner=False)
def _cached_symbolic_graph(
    max_length: int, k_max: int
) -> list[dict[str, object]]:
    return symbolic_graph_rows(max_length, k_max)


@st.cache_data(max_entries=32, show_spinner=False)
def _cached_joint(limit: int) -> dict[str, object]:
    return joint_graph_view(limit)


@st.cache_data(max_entries=32, show_spinner=False)
def _cached_synchronizing(precision: int, length: int) -> tuple[str, ...]:
    return synchronizing_context_view(precision, length)


def automaton_page() -> None:
    st.header("2-adic digit automaton")
    with st.form("automaton_form"):
        left, right = st.columns(2, vertical_alignment="bottom")
        precision = int(left.slider("Precision K", 2, 16, 8))
        n = int(right.number_input("Trace integer", value=27, step=1))
        submitted = st.form_submit_button(
            "Build automaton", icon=":material/schema:"
        )
    if not submitted and "automaton_result" not in st.session_state:
        st.caption("Submit a precision to classify odd residue states.")
        return
    if submitted:
        st.session_state.automaton_result = _cached_automaton(precision, n)
    payload = st.session_state.automaton_result

    with st.container(horizontal=True):
        st.metric("Modulus", payload["modulus"], border=True)
        st.metric("Odd states", payload["odd_states"], border=True)
        st.metric("Reachable from 0", payload["reachable"], border=True)
    st.dataframe(payload["rows"], hide_index=True, width="stretch")
    st.caption(
        "An exact label requires v2(3n+1) < K; AT_LEAST_K records the "
        "remaining precision class."
    )
    if st.toggle("Show residue trace", value=False, key="automaton_show_trace"):
        st.code(str(payload["report"]), language="text")
        st.caption(
            f"Final residue {payload['final_residue']} for BT({n}) = {payload['word']}."
        )


def transducer_page() -> None:
    st.header("Odd-part and division transducers")
    with st.form("transducer_form"):
        left, right = st.columns(2, vertical_alignment="bottom")
        x = int(left.number_input("Integer x", value=82, step=1))
        k_max = int(right.slider("Complexity through k", 1, 8, 4))
        submitted = st.form_submit_button(
            "Run transducer analysis", icon=":material/transform:"
        )
    if not submitted and "transducer_result" not in st.session_state:
        st.caption("Try x=82, which equals 3*27+1.")
        return
    if submitted:
        st.session_state.transducer_result = _cached_transducer(x, k_max)
    payload, complexity = st.session_state.transducer_result

    with st.container(horizontal=True):
        st.metric("x", payload["x"], border=True)
        st.metric(
            "v2(x)", "infinity" if payload["v2"] is None else payload["v2"], border=True
        )
        st.metric("BT(odd part)", payload["odd_part_BT"], border=True)
    st.code(f"BT(x) = {payload['BT']}", language="text")
    if payload["trace"]:
        st.dataframe(
            pd.DataFrame(
                payload["trace"],
                columns=["carry in", "input digit", "output digit", "carry out"],
            ),
            hide_index=True,
            width="stretch",
        )
    complexity_frame = pd.DataFrame(complexity)
    st.dataframe(complexity_frame, hide_index=True, width="stretch")
    st.bar_chart(
        complexity_frame,
        x="k",
        y=["naive_bound", "reachable", "minimized"],
        x_label="Valuation k",
        y_label="States",
    )
    st.caption(
        "The product bound is proved; reachable and minimized state counts are "
        "bounded computations."
    )


def valuation_prefix_page() -> None:
    st.header("Admissible valuation prefixes")
    with st.form("valuation_prefix_form"):
        c1, c2, c3 = st.columns(3, vertical_alignment="bottom")
        precision = int(c1.slider("Start precision P", 4, 16, 8))
        k_max = int(c2.slider("Maximum valuation", 1, 8, 5))
        length = int(c3.slider("Maximum prefix length", 1, 7, 4))
        submitted = st.form_submit_button(
            "Enumerate prefixes", icon=":material/account_tree:"
        )
    if not submitted and "valuation_prefix_result" not in st.session_state:
        st.caption("Submit finite bounds for the precision-drop automaton.")
        return
    if submitted:
        st.session_state.valuation_prefix_result = _cached_valuation(
            precision, k_max, length
        )
    payload = st.session_state.valuation_prefix_result

    with st.container(horizontal=True):
        st.metric("Admissible prefixes", payload["prefix_count"], border=True)
        st.metric("Contracting", payload["contracting"], border=True)
        st.metric("Expanding", payload["expanding"], border=True)
    st.dataframe(payload["rows"], hide_index=True, width="stretch")
    st.bar_chart(
        pd.DataFrame(payload["counts"]),
        x="length",
        y="prefixes",
        x_label="Prefix length",
        y_label="Count",
    )
    st.caption(
        f"Start odd residues: {payload['start_count']}. Budget classes compare "
        "2^sum(k) with 3^m; they are not Lyapunov claims."
    )


def valuation_languages_page() -> None:
    st.header("Valuation languages")
    section = st.segmented_control(
        "Tool",
        ("Cylinder", "Language complexity", "Symbolic futures"),
        default="Cylinder",
        key="languages_tool",
    )
    if section == "Cylinder":
        _cylinder_section()
    elif section == "Language complexity":
        _language_complexity_section()
    else:
        _symbolic_futures_section()


def _cylinder_section() -> None:
    with st.form("cylinder_form"):
        left, right = st.columns(2, vertical_alignment="bottom")
        ks = left.text_input("Valuation prefix", value="1,2")
        leftover = int(right.slider("Leftover precision Q", 1, 6, 1))
        submitted = st.form_submit_button(
            "Compute cylinder", icon=":material/calculate:"
        )
    if not submitted and "cylinder_result" not in st.session_state:
        return
    if submitted:
        try:
            st.session_state.cylinder_result = _cached_cylinder(ks, leftover)
        except ValueError as exc:
            st.error(str(exc))
            return
    payload = st.session_state.cylinder_result
    with st.container(horizontal=True):
        st.metric("Precision P", payload["precision"], border=True)
        st.metric("Classes", payload["class_count"], border=True)
        st.metric(
            "Density",
            f"{payload['density_numerator']}/{payload['density_denominator']}",
            border=True,
        )
        st.metric("Haar match", str(payload["matches_haar"]).lower(), border=True)
    st.write("Residues", payload["residues"])
    budget = payload["budget"]
    st.caption(
        f"Exact budget: 2^K={budget['two_power']} versus "
        f"3^m={budget['three_power']} ({budget['kind']})."
    )


def _language_complexity_section() -> None:
    with st.form("language_complexity_form"):
        left, right = st.columns(2, vertical_alignment="bottom")
        length = int(left.slider("Entropy length L", 2, 10, 5))
        k_max = int(right.slider("Complexity through k", 1, 8, 4))
        submitted = st.form_submit_button(
            "Compute language tables", icon=":material/table_chart:"
        )
    if not submitted and "language_tables" not in st.session_state:
        return
    if submitted:
        st.session_state.language_tables = _cached_language_tables(length, k_max)
    entropy_rows, complexity_rows = st.session_state.language_tables
    st.subheader("Cylinder entropy")
    st.dataframe(entropy_rows, hide_index=True, width="stretch")
    st.subheader("Transducer and language complexity")
    st.dataframe(complexity_rows, hide_index=True, width="stretch")
    st.caption(
        "Language sizes are verified computationally on the submitted finite bounds."
    )


def _symbolic_futures_section() -> None:
    with st.form("symbolic_graph_form"):
        left, right = st.columns(2, vertical_alignment="bottom")
        max_length = int(left.slider("Maximum prefix length", 1, 4, 2))
        k_max = int(right.slider("Maximum valuation", 1, 5, 3))
        submitted = st.form_submit_button(
            "Build symbolic graph", icon=":material/hub:"
        )
    if submitted:
        st.session_state.symbolic_graph_rows = _cached_symbolic_graph(
            max_length, k_max
        )
    if "symbolic_graph_rows" in st.session_state:
        st.dataframe(
            st.session_state.symbolic_graph_rows,
            hide_index=True,
            width="stretch",
        )
        st.caption(
            "Nodes are exact (valuation prefix, residue, precision) states, "
            "not sampled integers."
        )


def joint_graph_page() -> None:
    st.header("Sampled joint graph")
    with st.form("joint_graph_form"):
        limit = int(st.slider("Odd n at most", 10, 1000, 200, step=10))
        submitted = st.form_submit_button(
            "Build sampled graph", icon=":material/hub:"
        )
    if not submitted and "joint_graph_result" not in st.session_state:
        st.caption("This graph samples integer edges; it is not the full dynamics.")
        return
    if submitted:
        st.session_state.joint_graph_result = _cached_joint(limit)
    payload = st.session_state.joint_graph_result

    with st.container(horizontal=True):
        st.metric("Edges", payload["edge_count"], border=True)
        st.metric(
            "Images divisible by 3",
            payload["images_divisible_by_three"],
            border=True,
        )
    st.bar_chart(
        pd.DataFrame(payload["by_k"]),
        x="k",
        y="count",
        x_label="Valuation k",
        y_label="Sampled edges",
    )
    st.dataframe(payload["sample"], hide_index=True, width="stretch")
    st.caption(
        "Zero images modulo 3 is proved for every accelerated step; graph counts "
        "use only the submitted finite sample."
    )

    if st.toggle(
        "Search synchronizing right-strings",
        value=False,
        key="joint_sync_toggle",
    ):
        with st.form("synchronizing_form"):
            left, right = st.columns(2, vertical_alignment="bottom")
            precision = int(left.slider("Automaton precision", 2, 8, 4))
            length = int(right.slider("String length", 1, 4, 2))
            run = st.form_submit_button(
                "Run synchronizing search", icon=":material/search:"
            )
        if run:
            st.session_state.synchronizing_result = _cached_synchronizing(
                precision, length
            )
        if "synchronizing_result" in st.session_state:
            found = st.session_state.synchronizing_result
            st.caption(f"Found {len(found)} synchronizing strings.")
            if found:
                st.code("\n".join(found[:80]), language="text")
