"""Streamlit entry point and navigation router."""

from __future__ import annotations

import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent.parent
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

import streamlit as st

from bt.representation import encode

st.set_page_config(
    page_title="Balanced ternary laboratory",
    page_icon=":material/calculate:",
    layout="wide",
)

if "shared_odd_n" not in st.session_state:
    st.session_state.shared_odd_n = 27
if "shared_integer" not in st.session_state:
    st.session_state.shared_integer = 27
if "shared_word" not in st.session_state:
    st.session_state.shared_word = encode(27).word()

_PAGES = Path(__file__).resolve().parent / "app_pages"

pages = {
    "Balanced ternary": [
        st.Page(
            str(_PAGES / "overview.py"),
            title="Overview",
            icon=":material/home:",
            url_path="overview",
            default=True,
        ),
        st.Page(
            str(_PAGES / "calculator.py"),
            title="Calculator",
            icon=":material/calculate:",
            url_path="calculator",
        ),
        st.Page(
            str(_PAGES / "encode_analyze.py"),
            title="Encode / analyze",
            icon=":material/sync_alt:",
            url_path="encode-analyze",
        ),
        st.Page(
            str(_PAGES / "operators.py"),
            title="Operators",
            icon=":material/functions:",
            url_path="operators",
        ),
    ],
    "Calculus research": [
        st.Page(
            str(_PAGES / "residual_explorer.py"),
            title="Residual explorer",
            icon=":material/account_tree:",
            url_path="residual-explorer",
        ),
    ],
    "Collatz research": [
        st.Page(
            str(_PAGES / "number.py"),
            title="Number explorer",
            icon=":material/pin:",
            url_path="number",
        ),
        st.Page(
            str(_PAGES / "trajectory.py"),
            title="Trajectory",
            icon=":material/timeline:",
            url_path="trajectory",
        ),
        st.Page(
            str(_PAGES / "inverse_tree.py"),
            title="Inverse tree",
            icon=":material/account_tree:",
            url_path="inverse-tree",
        ),
        st.Page(
            str(_PAGES / "bt_warp.py"),
            title="BT warp",
            icon=":material/swap_horiz:",
            url_path="bt-warp",
        ),
        st.Page(
            str(_PAGES / "exponent_code.py"),
            title="Exponent-code geometry",
            icon=":material/architecture:",
            url_path="exponent-code",
        ),
        st.Page(
            str(_PAGES / "affine_census.py"),
            title="Affine-center census",
            icon=":material/query_stats:",
            url_path="affine-census",
        ),
        st.Page(
            str(_PAGES / "two_adic_automaton.py"),
            title="2-adic automaton",
            icon=":material/schema:",
            url_path="two-adic-automaton",
        ),
        st.Page(
            str(_PAGES / "odd_part_transducer.py"),
            title="Odd-part transducer",
            icon=":material/transform:",
            url_path="odd-part-transducer",
        ),
        st.Page(
            str(_PAGES / "valuation_prefixes.py"),
            title="Valuation prefixes",
            icon=":material/segment:",
            url_path="valuation-prefixes",
        ),
        st.Page(
            str(_PAGES / "valuation_languages.py"),
            title="Valuation languages",
            icon=":material/translate:",
            url_path="valuation-languages",
        ),
        st.Page(
            str(_PAGES / "joint_graph.py"),
            title="Joint graph",
            icon=":material/hub:",
            url_path="joint-graph",
        ),
    ],
}

page = st.navigation(pages, position="sidebar", expanded=False)

with st.sidebar:
    st.caption(
        "Digits: + = +1, 0 = 0, - = -1. Words display the most-significant "
        "digit first."
    )

st.title(f"{page.icon} {page.title}")
st.caption(
    "Exact balanced-ternary arithmetic. Collatz pages are one research "
    "application. Claim boundary: proved identities, bounded computations, "
    "and open questions are kept distinct."
)
page.run()
