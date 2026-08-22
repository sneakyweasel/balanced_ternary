"""Balanced-ternary laboratory pages: calculator, encode/analyze, operators."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from bt.operators import OPERATORS
from bt.representation import encode
from visualization.views import (
    BINARY_CALCULATOR_OPS,
    AnalyzeView,
    CalculatorView,
    analyze_view,
    apply_operator_view,
    calculator_view,
    operator_catalog_rows,
    parse_value,
)


ARITHMETIC_LABELS: dict[str, str] = {
    "Add": "add",
    "Subtract": "subtract",
    "Negate": "negate",
    "Add one": "add_one",
    "Multiply by 2": "multiply_by_2",
    "Multiply by 3": "multiply_by_3",
    "Divide by 2": "divide_by_2",
    "Divide by 3": "divide_by_3",
}

_EXAMPLE_INTEGERS: tuple[int, ...] = (27, 42, -5, 8, 0)


def _init_shared() -> None:
    if "shared_integer" not in st.session_state:
        seed = int(st.session_state.get("shared_odd_n", 27))
        st.session_state.shared_integer = seed
    if "shared_word" not in st.session_state:
        st.session_state.shared_word = encode(int(st.session_state.shared_integer)).word()


def _remember(n: int, word: str) -> None:
    st.session_state.shared_integer = n
    st.session_state.shared_word = word
    if n > 0 and n % 2 == 1:
        st.session_state.shared_odd_n = n


def _set_example(n: int) -> None:
    word = encode(n).word()
    _remember(n, word)
    st.session_state.calc_left_integer = n
    st.session_state.calc_left_word = word
    st.session_state.analyze_integer = n
    st.session_state.analyze_word = word
    st.session_state.operator_integer = n


def _example_buttons() -> None:
    with st.container(horizontal=True):
        for n in _EXAMPLE_INTEGERS:
            st.button(
                str(n),
                key=f"bt_example_{n}",
                on_click=_set_example,
                args=(n,),
            )


def _operand_inputs(
    *,
    prefix: str,
    source_default: str = "Integer",
) -> tuple[str, int, str]:
    source = st.segmented_control(
        "Input as",
        ["Integer", "Word"],
        default=source_default,
        key=f"{prefix}_source",
    )
    if source is None:
        source = source_default
    default_n = int(st.session_state.get("shared_integer", 27))
    default_word = str(st.session_state.get("shared_word", encode(default_n).word()))
    integer = int(
        st.number_input(
            "Integer",
            value=default_n,
            step=1,
            format="%d",
            key=f"{prefix}_integer",
        )
    )
    word = st.text_input(
        "Balanced ternary word",
        value=default_word,
        placeholder="+000",
        key=f"{prefix}_word",
        help="Digits +, 0, -; most-significant digit first.",
    )
    return ("integer" if source == "Integer" else "word"), integer, word


def _show_value(n: int, word: str, *, label: str) -> None:
    with st.container(horizontal=True):
        st.metric(f"{label} integer", n, border=True)
        st.metric(f"{label} length", len(word), border=True)
    st.code(word, language="text")


def _show_metrics(rows: tuple[tuple[str, object], ...]) -> None:
    st.dataframe(
        pd.DataFrame(rows, columns=["metric", "value"]),
        hide_index=True,
        width="stretch",
    )


def calculator_page() -> None:
    _init_shared()
    st.caption(
        "Exact word arithmetic and first-class operators. Domain errors are "
        "reported; they are not crashes."
    )
    _example_buttons()

    left_col, right_col = st.columns(2)
    with left_col:
        with st.container(border=True):
            st.subheader("Left operand")
            left_source, left_integer, left_word = _operand_inputs(prefix="calc_left")
            preview = parse_value(
                source=left_source, integer=left_integer, word=left_word
            )
            if preview.ok:
                st.caption(f"{preview.n} = `{preview.word}`")
            else:
                st.error(preview.error)

    with right_col:
        with st.container(border=True):
            st.subheader("Operation")
            family = st.segmented_control(
                "Family",
                ["Arithmetic", "Operator"],
                default="Arithmetic",
                key="calc_family",
            )
            if family is None:
                family = "Arithmetic"
            if family == "Arithmetic":
                label = st.selectbox(
                    "Operation",
                    list(ARITHMETIC_LABELS),
                    key="calc_arith_op",
                )
                operation = ARITHMETIC_LABELS[label]
            else:
                operation = st.selectbox(
                    "Operator",
                    list(OPERATORS),
                    key="calc_named_op",
                )
                notes = OPERATORS[operation].metadata().notes
                st.caption(f"Domain: {OPERATORS[operation].integer_domain}. {notes}")

            needs_right = operation in BINARY_CALCULATOR_OPS
            right_source, right_integer, right_word = "integer", 0, "0"
            if needs_right:
                st.subheader("Right operand")
                right_source, right_integer, right_word = _operand_inputs(
                    prefix="calc_right",
                    source_default="Integer",
                )

    view: CalculatorView = calculator_view(
        left_source=left_source,
        left_integer=left_integer,
        left_word=left_word,
        operation=operation,
        right_source=right_source,
        right_integer=right_integer,
        right_word=right_word,
    )
    if not view.ok:
        st.error(view.error)
        return

    _remember(view.result_n, view.result_word)
    st.subheader("Result")
    if st.button("Use result as left operand", icon=":material/west:"):
        st.session_state.calc_left_integer = view.result_n
        st.session_state.calc_left_word = view.result_word
        st.rerun()
    _show_value(view.result_n, view.result_word, label="Result")
    _show_metrics(view.metric_rows)
    st.caption(
        "The displayed word is the unique canonical representative. "
        "Leading zeros in a typed word are stripped on normalize."
    )


@st.cache_data(max_entries=256, show_spinner=False)
def _cached_analyze(n: int) -> AnalyzeView:
    return analyze_view(n)


def encode_analyze_page() -> None:
    _init_shared()
    st.caption(
        "Round-trip between integers and canonical words, with the same "
        "metrics as `btprime analyze`."
    )
    _example_buttons()

    from_integer, from_word = st.tabs(["From integer", "From word"])
    with from_integer:
        n = int(
            st.number_input(
                "Integer",
                value=int(st.session_state.shared_integer),
                step=1,
                format="%d",
                key="analyze_integer",
            )
        )
        view = _cached_analyze(n)
        _remember(view.n, view.word)
        _show_value(view.n, view.word, label="Canonical")
        if view.canonical:
            st.badge("Canonical word", icon=":material/check:", color="green")
        _show_metrics(view.metric_rows)
        st.subheader("Residues")
        st.dataframe(
            pd.DataFrame(view.residue_rows, columns=["modulus", "n mod q"]),
            hide_index=True,
            width="stretch",
        )

    with from_word:
        typed = st.text_input(
            "Balanced ternary word",
            value=str(st.session_state.shared_word),
            placeholder="+000",
            key="analyze_word",
        )
        parsed = parse_value(source="word", word=typed)
        if not parsed.ok:
            st.error(parsed.error)
            return
        decoded = _cached_analyze(parsed.n)
        _remember(decoded.n, decoded.word)
        if parsed.was_canonical:
            st.badge("Already canonical", icon=":material/check:", color="green")
        else:
            st.badge("Normalized", icon=":material/info:", color="orange")
        _show_value(decoded.n, decoded.word, label="Decoded")
        _show_metrics(decoded.metric_rows)


def operators_page() -> None:
    _init_shared()
    st.caption(
        "Integer-level and word-level maps are distinct. The laboratory "
        "applies both and checks that they agree."
    )
    _example_buttons()

    n = int(
        st.number_input(
            "Integer",
            value=int(st.session_state.shared_integer),
            step=1,
            format="%d",
            key="operator_integer",
        )
    )
    symbol = st.selectbox("Operator", list(OPERATORS), key="operator_symbol")
    applied = apply_operator_view(symbol, n)
    _remember(n, encode(n).word())

    if not applied.ok:
        st.error(applied.error)
    else:
        _show_value(applied.result_n, applied.result_word, label="Image")
        if applied.consistent:
            st.badge(
                "Integer and word maps agree",
                icon=":material/check:",
                color="green",
            )
        else:
            st.error(applied.error or "Integer and word results disagree.")

    st.subheader("Catalog")
    st.dataframe(
        pd.DataFrame(operator_catalog_rows()),
        hide_index=True,
        width="stretch",
    )
