"""Rewrite-calculus companion, merged into the laboratory Streamlit app."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from visualization.rewrite_explorer import (
    AFFINE_HELP,
    CLAIM_ROWS,
    CTORS,
    EXACT_TRIPLES,
    OPERATOR_HELP,
    UNARY_OPS,
    UNARY_PRESETS,
    UnaryTerm,
    carry_view,
    constructor_sum_view,
    normalize_unary,
    push_in_peak,
    step_unary,
    unary_from_ops,
    wrap_unary,
)
from visualization.theorem_ledger import badge_payload


def _init_state() -> None:
    defaults = {
        "rw_view": "Carry",
        "rw_ops": (),
        "rw_last_rule": "",
        "rw_n": 0,
        "rw_x": 1,
        "rw_y": 1,
        "rw_U": "S",
        "rw_V": "S",
        "rw_W": "S",
        "rw_sx": 0,
        "rw_sy": 0,
        "rw_px": 1,
        "rw_py": 1,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def _badge(theorem_id: str) -> None:
    payload = badge_payload(theorem_id)
    if not payload:
        return
    kind = payload["kind"]
    color = {
        "proved": "green",
        "computed": "blue",
        "conjecture": "orange",
        "refuted": "red",
        "reparameterization": "violet",
        "other": "gray",
    }.get(kind, "gray")
    st.badge(payload["tag"], color=color)
    lean = payload.get("lean") or ""
    extra = f" · Lean `{lean}`" if lean else ""
    st.caption(f"{payload['id']}{extra}")


def _term() -> UnaryTerm:
    return unary_from_ops(tuple(st.session_state.rw_ops))


def _set_ops(ops: tuple[str, ...], rule: str = "") -> None:
    st.session_state.rw_ops = ops
    st.session_state.rw_last_rule = rule


def _claim_map() -> None:
    st.caption(
        "Lean is the proof authority. The last row is a human corollary, "
        "not a Lean theorem."
    )
    _badge("BTC-add-requires-carry-state")
    cards = st.container(horizontal=True)
    with cards:
        st.metric("Unary core", "LEAN", border=True)
        st.metric("Not D-local", "LEAN", border=True)
        st.metric("Six rows", "LEAN", border=True)
        st.metric("Named peak", "LEAN", border=True)
    st.dataframe(pd.DataFrame(CLAIM_ROWS), hide_index=True, width="stretch")
    st.info(
        "This page does not claim that addition is impossible, that "
        "Avizienis addition is false, or that the production word table "
        "is confluent.",
        icon=":material/info:",
    )


def _unary() -> None:
    st.caption(
        "Open terms in {D, I_a, S, N}. Stepping uses rewrite_once. "
        "Add is not a constructor here."
    )
    _badge("BTC-op-fragment-nd-nf")

    def _apply_preset() -> None:
        name = st.session_state.get("rw_preset")
        if name:
            _set_ops(UNARY_PRESETS[name])

    st.pills(
        "Presets",
        list(UNARY_PRESETS),
        selection_mode="single",
        key="rw_preset",
        on_change=_apply_preset,
    )

    op_row = st.container(horizontal=True)
    with op_row:
        for op in UNARY_OPS:
            if st.button(op, key=f"rw_wrap_{op}", help=OPERATOR_HELP[op]):
                _set_ops(wrap_unary(_term(), op).ops)
        if st.button("Clear", icon=":material/backspace:", key="rw_clear"):
            _set_ops(())
        if st.button("Step", icon=":material/skip_next:", key="rw_step"):
            nxt, reason = step_unary(_term())
            _set_ops(nxt.ops, reason or "already irreducible")
        if st.button("Normalize", icon=":material/done_all:", key="rw_norm"):
            nxt, reasons, _steps = normalize_unary(_term())
            _set_ops(nxt.ops, " ; ".join(reasons) if reasons else "already irreducible")

    with st.expander("Operator definitions", expanded=False):
        for op in UNARY_OPS:
            st.markdown(f"**{op}.** {OPERATOR_HELP[op]}")

    term = _term()
    nf, _reasons, _steps = normalize_unary(term)
    left, right = st.columns(2)
    with left:
        with st.container(border=True):
            st.subheader("Current term")
            st.code(term.render())
            last = st.session_state.rw_last_rule or "—"
            st.caption(f"Last rule: {last}")
            i0, inv, size = term.rank()
            st.metric("Lex rank (I0, N-inv, size)", f"{i0}, {inv}, {size}", border=True)
    with right:
        with st.container(border=True):
            st.subheader("Normal form")
            st.code(nf.render())
            st.caption("Unique syntactic NF of the enlarged unary TRS.")
            n = int(st.number_input("Evaluate at n", step=1, key="rw_n"))
            st.metric("Value", term.evaluate(n), border=True)
            if term.ops != nf.ops:
                st.caption(f"NF value at n is {nf.evaluate(n)}.")

    if term.render() in {"N(D(x))", "D(N(x))"}:
        st.info(
            "N(D(x)) and D(N(x)) share the NF D(N(x)). Without the oriented "
            "commute they were distinct irreducibles with the same semantics.",
            icon=":material/info:",
        )


def _carry() -> None:
    st.caption(
        "D(x+y) = D(x)+D(y)+carry(lsd x, lsd y). The pair (0,0) vs (1,1) "
        "shows that no G(D(x), D(y)) can recover D(x+y)."
    )
    _badge("BTC-add-not-D-local")

    def _carry_preset(x: int, y: int) -> None:
        st.session_state.rw_x = x
        st.session_state.rw_y = y

    presets = st.container(horizontal=True)
    with presets:
        st.button("(0, 0)", key="rw_carry_00", on_click=_carry_preset, args=(0, 0))
        st.button("(1, 1)", key="rw_carry_11", on_click=_carry_preset, args=(1, 1))
        st.button("(1, 0)", key="rw_carry_10", on_click=_carry_preset, args=(1, 0))

    inputs = st.container(horizontal=True)
    with inputs:
        x = int(st.number_input("x", step=1, key="rw_x"))
        y = int(st.number_input("y", step=1, key="rw_y"))

    view = carry_view(x, y)
    trit_row = st.container(horizontal=True)
    with trit_row:
        st.metric(
            "lsd(x)",
            view.lsd_x,
            border=True,
            help="Least-significant balanced trit of x, in {−1, 0, +1}.",
        )
        st.metric(
            "lsd(y)",
            view.lsd_y,
            border=True,
            help="Least-significant balanced trit of y, in {−1, 0, +1}.",
        )
        st.metric(
            "carry",
            view.carry,
            border=True,
            help="carry = D(x+y) − D(x) − D(y), itself a trit.",
        )
    d_row = st.container(horizontal=True)
    with d_row:
        st.metric("D(x)", view.d_x, border=True, help=OPERATOR_HELP["D"])
        st.metric("D(y)", view.d_y, border=True, help=OPERATOR_HELP["D"])
        st.metric("D(x+y)", view.d_sum, border=True, help=OPERATOR_HELP["D"])
        st.metric(
            "D(x)+D(y)",
            view.d_sum_naive,
            border=True,
            help="Naive carry-free sum of D-states. Equals D(x+y) iff the carry is 0.",
        )

    if view.d_sum != view.d_sum_naive:
        st.warning(
            f"D(x+y) − D(x) − D(y) = {view.carry}. Carry-free D-through-Add is unsound.",
            icon=":material/warning:",
        )
    else:
        st.success("On this pair the carry is 0, so the naive rule happens to hold.", icon=":material/check:")
    if view.not_d_local_witness:
        st.error(
            "Same operand D-states (0, 0), different D(x+y). This is the Lean witness.",
            icon=":material/block:",
        )


def _sums() -> None:
    st.caption(
        "U(x)+V(y)=W(x+y) on {S, I+, I−, N} iff slopes match and constants add. "
        "Same-sign I+ is never a constructor identity."
    )
    _badge("BTC-constructor-sum-class")

    pick = st.container(horizontal=True)
    with pick:
        u = st.segmented_control("U", CTORS, key="rw_U", help=AFFINE_HELP)
        v = st.segmented_control("V", CTORS, key="rw_V", help=AFFINE_HELP)
        w = st.segmented_control("W", CTORS, key="rw_W", help=AFFINE_HELP)
    if u is None:
        u = "S"
    if v is None:
        v = "S"
    if w is None:
        w = "S"

    xy = st.container(horizontal=True)
    with xy:
        x = int(st.number_input("x", step=1, key="rw_sx"))
        y = int(st.number_input("y", step=1, key="rw_sy"))

    view = constructor_sum_view(u, v, w, x, y)
    metrics = st.container(horizontal=True)
    with metrics:
        st.metric("Exact identity?", "yes" if view.exact else "no", border=True)
        st.metric("U(x)+V(y)", view.left, border=True)
        st.metric("W(x+y)", view.right, border=True)
    st.caption(
        f"slopes ({view.slope_u}, {view.slope_v}) → {view.slope_w}; "
        f"constants {view.const_u}+{view.const_v} vs {view.const_w}. {view.reason}."
    )
    if u == "I+" and v == "I+":
        st.warning(
            "I+(x)+I+(y)=3(x+y)+2. The residue 2 is not a trit.",
            icon=":material/warning:",
        )

    rows = [
        {
            "U": a,
            "V": b,
            "W": c,
            "identity": f"{a}(x)+{b}(y)={c}(x+y)",
        }
        for a, b, c in EXACT_TRIPLES
    ]
    st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch")


def _peak() -> None:
    st.caption(
        "Named carry-free system only: D(S(t))→t and S(Add(t,u))→Add(S(t),S(u)). "
        "This is not production rewrite_expr, and not a theorem about every TRS."
    )
    _badge("BTC-push-in-S-peak")

    xy = st.container(horizontal=True)
    with xy:
        x = int(st.number_input("X", step=1, key="rw_px"))
        y = int(st.number_input("Y", step=1, key="rw_py"))

    view = push_in_peak(x, y)
    st.code(view.peak)
    cols = st.columns(2)
    with cols[0]:
        with st.container(border=True):
            st.subheader("D∘S")
            st.code(view.left)
            st.metric("Value", view.left_value, border=True)
            st.caption("Irreducible in the named system.")
    with cols[1]:
        with st.container(border=True):
            st.subheader("S through Add")
            st.code(view.right)
            st.metric("Value", view.right_value, border=True)
            st.caption("Irreducible in the named system.")
    if view.agree:
        st.info(
            "Semantic twins: both denote X+Y. The peak does not join.",
            icon=":material/info:",
        )


def rewrite_calculus_page() -> None:
    _init_state()
    st.caption(
        "Paper companion for the unary rewrite calculus and the carry "
        "boundary. Lean is the proof authority. This UI only instantiates "
        "witnesses. Word-table fragments stay closed."
    )
    view = st.segmented_control(
        "View",
        ["Claim map", "Unary", "Carry", "Constructor sums", "Push-in peak"],
        key="rw_view",
    )
    if view == "Claim map":
        _claim_map()
    elif view == "Unary":
        _unary()
    elif view == "Constructor sums":
        _sums()
    elif view == "Push-in peak":
        _peak()
    else:
        _carry()


rewrite_calculus_page()
