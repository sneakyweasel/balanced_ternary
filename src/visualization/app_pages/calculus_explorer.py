"""Residual Explorer Streamlit workspace."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from bt.calculus.section import IntPoly
from visualization.residual_explorer import (
    DEFAULT_DEFICIT,
    DEFAULT_K,
    DEFAULT_POLY,
    LIFT_KIND_LABEL,
    PRESETS,
    CompareView,
    LiftingView,
    MinimalStateView,
    NodeInspection,
    TreeNode,
    census_view,
    compare_states,
    demo_delayed_pair,
    depth_from_mode,
    expand_subtree_words,
    dual_census,
    fibre_view,
    filter_nodes,
    format_word,
    inspect_node,
    is_x3,
    lift_table_rows,
    lift_tree_svg,
    lifting_view,
    minimal_state_view,
    node_table_rows,
    quotient_compare_view,
    quotient_invariant_view,
    parse_word,
    resolve_polynomial,
    tree_svg,
    visible_subtree,
)


def _init_state() -> None:
    defaults = {
        "re_poly": DEFAULT_POLY,
        "re_custom": "",
        "re_k": DEFAULT_K,
        "re_mode": "deficit",
        "re_mode_label": "deficit r",
        "re_m": DEFAULT_K - 1 - DEFAULT_DEFICIT,
        "re_r": DEFAULT_DEFICIT,
        "re_explain": "Research",
        "re_allow_expensive": False,
        "re_selected": format_word(tuple([0] * (DEFAULT_K - 1 - DEFAULT_DEFICIT))),
        "re_expanded": [],
        "re_a": "",
        "re_b": "",
        "re_focus_depth": DEFAULT_K - 1 - DEFAULT_DEFICIT,
        "re_filter": "all",
        "re_class_filter": "all",
        "re_secondary": "Fibre",
        "re_lift_levels": 4,
        "re_lift_r": 2,
        "re_lift_selected": "none",
        "re_lift_witness": False,
        "re_ready": True,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


@st.cache_data(max_entries=32, show_spinner="Computing residual tree…")
def _cached_tree(
    poly_text: str,
    custom: str,
    k: int,
    expanded: tuple[tuple[int, ...], ...],
    focus_depth: int | None,
) -> tuple[TreeNode, ...]:
    f = resolve_polynomial(poly_text, custom)
    return visible_subtree(
        f,
        k,
        expanded=frozenset(expanded),
        focus_depth=focus_depth,
    )


@st.cache_data(max_entries=64, show_spinner=False)
def _cached_inspect(poly_text: str, custom: str, word_text: str, k: int) -> NodeInspection:
    f = resolve_polynomial(poly_text, custom)
    return inspect_node(f, parse_word(word_text), k)


@st.cache_data(max_entries=16, show_spinner="Computing class census…")
def _cached_census(poly_text: str, custom: str, k: int, allow: bool):
    f = resolve_polynomial(poly_text, custom)
    return census_view(f, k, allow_expensive=allow)


@st.cache_data(max_entries=8, show_spinner="Comparing x^2 and x^3…")
def _cached_dual(k: int, allow: bool):
    return dual_census(k, allow_expensive=allow)


@st.cache_data(max_entries=32, show_spinner="Building lifting tree…")
def _cached_lifting(poly_text: str, custom: str, levels: int, r: int) -> LiftingView:
    f = resolve_polynomial(poly_text, custom)
    return lifting_view(f, levels, r)


@st.cache_data(max_entries=32, show_spinner="Comparing state descriptions…")
def _cached_minimal_state(
    poly_text: str, custom: str, levels: int, r: int
) -> MinimalStateView:
    f = resolve_polynomial(poly_text, custom)
    return minimal_state_view(f, levels, r)


def _poly() -> IntPoly:
    return resolve_polynomial(st.session_state.re_poly, st.session_state.re_custom)


def _selected_word() -> tuple[int, ...]:
    try:
        return parse_word(st.session_state.re_selected)
    except ValueError:
        return ()


def _step_cb(trit: int) -> None:
    word = _selected_word()
    k = int(st.session_state.re_k)
    if len(word) >= k - 1:
        return
    nxt = word + (trit,)
    st.session_state.re_selected = format_word(nxt)
    cur = [tuple(w) for w in st.session_state.re_expanded]
    if word not in cur:
        cur.append(word)
        st.session_state.re_expanded = cur


def _expand_selected_cb() -> None:
    word = _selected_word()
    cur = [tuple(w) for w in st.session_state.re_expanded]
    if word not in cur:
        cur.append(word)
        st.session_state.re_expanded = cur


def _expand_subtree_cb() -> None:
    extra = expand_subtree_words(_selected_word(), int(st.session_state.re_k), cap=80)
    cur = [tuple(w) for w in st.session_state.re_expanded]
    for word in extra:
        if word not in cur:
            cur.append(word)
    st.session_state.re_expanded = cur


def _set_a_cb() -> None:
    st.session_state.re_a = st.session_state.re_selected


def _set_b_cb() -> None:
    st.session_state.re_b = st.session_state.re_selected


def _highlight_merged_cb() -> None:
    st.session_state.re_filter = "merged"


def _focus_layer_cb(r: int) -> None:
    k = int(st.session_state.re_k)
    st.session_state.re_mode = "deficit"
    st.session_state.re_mode_label = "deficit r"
    st.session_state.re_r = r
    st.session_state.re_m = k - 1 - r
    st.session_state.re_focus_depth = k - 1 - r
    st.session_state.re_selected = format_word(tuple([0] * (k - 1 - r)))


def _load_delayed_pair_cb() -> None:
    _f, wa, wb = demo_delayed_pair()
    st.session_state.re_poly = "x^3"
    st.session_state.re_custom = ""
    st.session_state.re_k = 2
    st.session_state.re_mode = "explicit"
    st.session_state.re_mode_label = "explicit m"
    st.session_state.re_m = 1
    st.session_state.re_r = 0
    st.session_state.re_focus_depth = 1
    st.session_state.re_a = format_word(wa)
    st.session_state.re_b = format_word(wb)
    st.session_state.re_selected = format_word(wa)
    st.session_state.re_secondary = "Compare"


def _badge(payload: dict[str, str] | None) -> None:
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


def _horizon_warning(k: int) -> None:
    if k >= 14:
        st.warning(
            "k = 14 keeps a lazy tree. Full class census is opt-in and enumerates "
            "millions of residuals."
        )
    elif k >= 12:
        st.warning(
            "k ≥ 12: the tree stays lazy. A full Newton-image census is expensive."
        )


def residual_explorer_page() -> None:
    _init_state()
    st.caption(
        "Prefix tree → residual polynomial → Newton coordinates → "
        "3-adic visibility → equivalence / fibre. "
        "Higher k = finer arithmetic resolution mod 3^k."
    )

    with st.form("residual_explorer_form"):
        row = st.container(horizontal=True)
        with row:
            st.selectbox("Polynomial", list(PRESETS), key="re_poly")
            st.text_input(
                "Custom polynomial",
                key="re_custom",
                placeholder="parse_poly syntax, e.g. x^3+x",
            )
            k = st.slider("Horizon k", min_value=1, max_value=14, key="re_k")
        st.segmented_control(
            "Depth mode",
            ["explicit m", "deficit r"],
            key="re_mode_label",
        )
        depth_row = st.container(horizontal=True)
        with depth_row:
            m_in = st.number_input(
                "Depth m",
                min_value=0,
                max_value=max(int(k) - 1, 0),
                key="re_m",
            )
            r_in = st.number_input(
                "Deficit r",
                min_value=0,
                max_value=max(int(k) - 1, 0),
                key="re_r",
            )
            st.segmented_control(
                "Panel mode",
                ["Explain", "Research"],
                key="re_explain",
            )
            st.checkbox("Allow expensive census", key="re_allow_expensive")
        submitted = st.form_submit_button("Run", icon=":material/play_arrow:")

    if submitted:
        st.session_state.re_mode = (
            "deficit" if st.session_state.re_mode_label == "deficit r" else "explicit"
        )
        try:
            focused = depth_from_mode(
                int(k),
                mode=st.session_state.re_mode,
                m=int(m_in),
                r=int(r_in),
            )
        except ValueError as exc:
            st.error(str(exc))
            return
        st.session_state.re_focus_depth = focused
        st.session_state.re_selected = format_word(tuple([0] * focused))
        st.session_state.re_ready = True

    _horizon_warning(int(st.session_state.re_k))
    if not st.session_state.re_ready:
        st.caption("Submit Run to compute.")
        return

    try:
        f = _poly()
    except ValueError as exc:
        st.error(f"Could not parse polynomial: {exc}")
        return

    k = int(st.session_state.re_k)
    focus = int(st.session_state.re_focus_depth)
    expanded = tuple(tuple(w) for w in st.session_state.re_expanded)
    try:
        nodes = _cached_tree(
            st.session_state.re_poly,
            st.session_state.re_custom,
            k,
            expanded,
            focus,
        )
    except ValueError as exc:
        st.error(str(exc))
        return

    ids = [n.id for n in nodes]
    if st.session_state.re_selected not in ids and ids:
        st.session_state.re_selected = ids[0]

    tree_col, state_col, explain_col = st.columns([1.15, 1.05, 0.9])
    with tree_col:
        _tree_panel(nodes, k)
    with state_col:
        _state_panel(f, k)
    with explain_col:
        _explain_panel(f, k)

    _precision_strip(f, k)
    if is_x3(f):
        _q_invariant_panel(f, k)
    _layer_strip(k)
    _secondary(f, k, nodes)


def _tree_panel(nodes: tuple[TreeNode, ...], k: int) -> None:
    st.subheader("Prefix / residual tree")
    filt = st.segmented_control(
        "Filter",
        ["all", "merged", "singletons", "selected depth", "focus class"],
        key="re_filter",
    )
    class_ids = ["all"] + [str(cid) for cid in sorted({n.class_id for n in nodes})]
    class_choice = st.selectbox("Show only class", class_ids, key="re_class_filter")
    selected = st.session_state.re_selected
    shown = filter_nodes(
        nodes,
        class_id=None if class_choice == "all" else int(class_choice),
        merged_only=filt == "merged",
        singleton_only=filt == "singletons",
        depth=len(_selected_word()) if filt == "selected depth" else None,
        focus_class=filt == "focus class",
        selected_id=selected,
    )
    st.html(tree_svg(shown if shown else nodes, selected_id=selected))
    st.caption(
        "Colour = fibre / class among loaded nodes. Square = merged in the "
        "visible set. Circle = singleton. Class id is written on the node."
    )
    options = [n.id for n in (shown if shown else nodes)]
    if selected not in options and options:
        selected = options[0]
        st.session_state.re_selected = selected
    st.selectbox("Selected residual", options, key="re_selected")
    nav = st.container(horizontal=True)
    with nav:
        st.button("Step −1", key="re_step_m", on_click=_step_cb, args=(-1,))
        st.button("Step 0", key="re_step_z", on_click=_step_cb, args=(0,))
        st.button("Step +1", key="re_step_p", on_click=_step_cb, args=(1,))
        st.button("Expand selected", key="re_expand", on_click=_expand_selected_cb)
        st.button("Expand subtree", key="re_expand_sub", on_click=_expand_subtree_cb)
        st.button("Set A", key="re_set_a", on_click=_set_a_cb)
        st.button("Set B", key="re_set_b", on_click=_set_b_cb)
    st.dataframe(pd.DataFrame(node_table_rows(shown if shown else nodes)), hide_index=True)


def _state_panel(f: IntPoly, k: int) -> None:
    st.subheader("Current state")
    view = _cached_inspect(
        st.session_state.re_poly,
        st.session_state.re_custom,
        st.session_state.re_selected,
        k,
    )
    st.markdown(f"**Exact residual**")
    st.code(f"f_{{{view.state.m},{view.state.p}}}(x) = {view.state.exact}", language="text")
    st.markdown(f"**Observable class**")
    st.code(f"Φ_{k}(f) = {view.newton.class_key}", language="text")
    with st.container(horizontal=True):
        st.metric("m", view.state.m, border=True)
        st.metric("p", view.state.p, border=True)
        st.metric("r = k−1−m", view.visibility.r, border=True)
        st.metric("word", view.state.word_text, border=True)
    st.markdown("Newton coordinates")
    for coord in view.newton.coords:
        vis = "visible" if coord.visible else "zero modulo 3^k"
        st.code(
            "\n".join(
                (
                    f"N{coord.index}",
                    f"exact:     {coord.exact}",
                    f"mod 3^{k}: {coord.mod_value}",
                    f"v3:        {coord.valuation}",
                    f"visibility:{vis}",
                    f"3-adic:    {coord.bar}",
                )
            ),
            language="text",
        )


def _explain_panel(f: IntPoly, k: int) -> None:
    st.subheader("Mathematical explanation")
    view = _cached_inspect(
        st.session_state.re_poly,
        st.session_state.re_custom,
        st.session_state.re_selected,
        k,
    )
    story = view.visibility
    if st.session_state.re_explain == "Explain":
        st.markdown(
            f"""
**Current visibility**

depth deficit: `r = {story.r}`

{story.n2_sees}

{story.n1_line}

{story.n0_line}
            """
        )
        if story.extra:
            st.caption(story.extra)
    else:
        st.markdown(f"`r = {story.r}`  ·  `{story.n2_sees}`")
        st.code(
            "\n".join(
                (
                    f"source = {view.state.source_poly}",
                    f"word   = {view.state.word_text}  (LSD-first)",
                    f"m, p   = {view.state.m}, {view.state.p}",
                    f"phi    = {view.newton.phi}",
                    f"digits = {view.digits}",
                )
            ),
            language="text",
        )
        _badge(story.badge)
        if story.extra:
            st.caption(story.extra)
    if view.source_is_x3 and story.r == 2:
        st.info("N₂ sees p mod 9.", icon=":material/visibility:")


def _precision_strip(f: IntPoly, k: int) -> None:
    view = _cached_inspect(
        st.session_state.re_poly,
        st.session_state.re_custom,
        st.session_state.re_selected,
        k,
    )
    st.subheader("3-adic / precision strip")
    digit_bits = "  ".join(f"{a:+d}" for a in view.digits) if view.digits else "(empty prefix)"
    highlight = min(max(view.visibility.r, 0), view.state.m)
    st.code(
        "\n".join(
            (
                f"p = {view.state.p}",
                f"digits a0 … a{max(view.state.m - 1, 0)} (LSD-first): {digit_bits}",
                f"visible under N2: first {highlight} low-order trits"
                if view.source_is_x3
                else "x^2: the linear coefficient 2p is fully visible",
                *[f"p mod {mod} = {res}" for mod, res in view.mods],
            )
        ),
        language="text",
    )
    census = _cached_census(
        st.session_state.re_poly,
        st.session_state.re_custom,
        k,
        bool(st.session_state.re_allow_expensive),
    )
    with st.container(horizontal=True):
        st.metric("Raw residual states", census.raw if census.raw is not None else "—", border=True)
        st.metric(
            "Observable states",
            census.observable if census.observable is not None else "—",
            border=True,
        )
        merged = census.merged if census.merged is not None else "—"
        st.metric("States merged", merged, border=True)
    st.caption(census.caption)
    if census.warning:
        st.warning(census.warning)
    if st.session_state.re_explain == "Research":
        _badge(census.badge)
    if census.merged not in (None, 0):
        st.button(
            "Highlight merged states",
            key="re_highlight_merged",
            icon=":material/filter_alt:",
            on_click=_highlight_merged_cb,
        )


def _q_invariant_panel(_f: IntPoly, k: int) -> None:
    view = _cached_inspect(
        st.session_state.re_poly,
        st.session_state.re_custom,
        st.session_state.re_selected,
        k,
    )
    r = view.visibility.r
    card = quotient_invariant_view(view.state.p, k, r)
    with st.expander("Mismatched quotient invariant", expanded=False):
        st.caption("Two-scale reading of Q on the surviving 3^r locus.")
        if not card.on_locus:
            st.write(card.note)
            return
        st.code(
            "\n".join(
                (
                    f"u = {card.u} = {card.a} + 3^{card.t}*{card.b}",
                    f"low part a = {card.a}",
                    f"high part b = {card.b}",
                    f"a^3 low t digits B_t(u) = {card.B_t}",
                    f"Q(u) = {card.Q}",
                    f"expansion D^t(a^3)+3a^2 b+… = {card.expansion}",
                    *card.psi_lines,
                    card.note,
                )
            ),
            language="text",
        )
        left, right = st.columns(2)
        with left:
            u_in = st.number_input("Compare u", value=int(card.u), key="re_q_u")
        with right:
            v_in = st.number_input("Compare v", value=int(card.u), key="re_q_v")
        if st.button("Compare Q and Ψ", key="re_q_cmp", icon=":material/compare_arrows:"):
            try:
                cmp_view = quotient_compare_view(
                    int(u_in), int(v_in), card.t, card.K, card.W
                )
            except ValueError as exc:
                st.error(str(exc))
                return
            st.metric("Same candidate Ψ4", "YES" if cmp_view.same_psi4 else "NO", border=True)
            st.metric("Same Q", "YES" if cmp_view.same_Q else "NO", border=True)
            st.code(cmp_view.block, language="text")
            if cmp_view.missing:
                st.write("Missing information")
                for line in cmp_view.missing:
                    st.write(line)


def _layer_strip(k: int) -> None:
    st.caption("Depth-deficit layers for the current horizon")
    chips = st.container(horizontal=True)
    with chips:
        for r, label, sees in (
            (0, "r=0 deepest", "N2: none"),
            (1, "r=1 one above", "N2: mod 3"),
            (2, "r=2 two above", "N2: mod 9"),
        ):
            if k - 1 - r < 0:
                continue
            st.button(
                f"{label} · {sees}",
                key=f"re_layer_{r}",
                on_click=_focus_layer_cb,
                args=(r,),
            )


def _secondary(f: IntPoly, k: int, nodes: tuple[TreeNode, ...]) -> None:
    choice = st.segmented_control(
        "Secondary view",
        ["Fibre", "Compare", "x^2 vs x^3", "Congruence / lifting"],
        key="re_secondary",
    )
    if choice == "Fibre":
        _fibre_card(f, k, nodes)
    elif choice == "Compare":
        _compare_card(f, k)
    elif choice == "Congruence / lifting":
        _lifting_card()
    else:
        _dual_card(k)


def _lifting_card() -> None:
    controls = st.container(horizontal=True)
    with controls:
        levels = st.slider("Levels k", min_value=1, max_value=7, key="re_lift_levels")
        depth = st.slider("Horizon r", min_value=1, max_value=4, key="re_lift_r")
    view = _cached_lifting(
        st.session_state.re_poly,
        st.session_state.re_custom,
        int(levels),
        int(depth),
    )
    st.markdown(f"**Lifting tree** of `{view.poly}` for `f(x) = 0 mod 3^k`")
    counts = st.container(horizontal=True)
    with counts:
        st.metric(f"Roots mod 3^{view.k}", view.level_counts[-1], border=True)
        st.metric("Brute force agrees", "YES" if view.brute_force_agrees else "NO", border=True)
        st.metric("Nodes shown", len(view.nodes), border=True)
    if view.truncated:
        st.warning("Tree is larger than the display budget; deeper nodes are omitted.")
    options = ["none"] + [node.id for node in view.nodes]
    if st.session_state.re_lift_selected not in options:
        st.session_state.re_lift_selected = "none"
    selected = st.selectbox("Highlight node", options, key="re_lift_selected")
    st.html(lift_tree_svg(view.nodes, selected_id=None if selected == "none" else selected))
    st.caption(
        "Colour encodes lift type: green unique, orange singular with three "
        "lifts, blue several children below the root, grey no lift. The "
        "balanced residue is under each node and the number of lifts inside it."
    )
    legend = st.container(horizontal=True)
    with legend:
        for kind, count in view.kind_census:
            st.metric(kind, count, border=True, help=LIFT_KIND_LABEL[kind])
    st.write(f"Level counts N_0 … N_{view.k}: {list(view.level_counts)}")
    st.write(
        "Distinct depth-"
        f"{view.r} subtrees per level: "
        f"{[f'level {lvl}: {n}' for lvl, n in view.distinct_subtrees]}"
    )
    st.dataframe(pd.DataFrame(lift_table_rows(view.nodes)), hide_index=True)
    if st.session_state.re_explain == "Explain":
        for line in view.notes:
            st.write(line)
    else:
        for line in view.notes:
            st.caption(line)
    _minimal_state_panel(int(levels), int(depth))


def _minimal_state_panel(levels: int, depth: int) -> None:
    with st.expander("Minimal state: valuation vs Newton jet vs behaviour"):
        state = _cached_minimal_state(
            st.session_state.re_poly,
            st.session_state.re_custom,
            levels,
            depth,
        )
        counts = st.container(horizontal=True)
        with counts:
            st.metric(
                "Valuation classes",
                state.valuation_classes,
                border=True,
                help="the capped pair of 3-adic valuations; determines nothing",
            )
            st.metric(
                f"Phi_{state.r} classes",
                state.phi_classes,
                border=True,
                help="sufficient for the depth-r subtree, but not minimal",
            )
            st.metric(
                "Behaviour classes",
                state.behaviour_classes,
                border=True,
                help="the ordered trit-labelled depth-r subtree, minimal by definition",
            )
        deep = st.container(horizontal=True)
        with deep:
            st.metric("Deep Phi_r states", state.deep_phi_states, border=True)
            st.metric("Unit-scaling orbits", state.deep_orbits, border=True)
            st.metric("Deep minimal L_r", state.deep_minimal, border=True)
        if st.button("Find two live nodes with different jets and identical futures"):
            st.session_state.re_lift_witness = True
        if st.session_state.get("re_lift_witness"):
            if state.witness is None:
                st.info(
                    "No live jet-redundant pair in this tree at this horizon. Try "
                    "x^2-9 at k = 4, or compare x against -x directly."
                )
            else:
                left, right, shared = state.witness
                st.success(f"{left}  and  {right}")
                st.code(f"shared depth-{state.r} behaviour: {shared}", language="text")
        st.dataframe(pd.DataFrame(list(state.rows)), hide_index=True)
        for line in state.notes:
            st.caption(line)


def _fibre_card(f: IntPoly, k: int, nodes: tuple[TreeNode, ...]) -> None:
    selected = next((n for n in nodes if n.id == st.session_state.re_selected), None)
    class_id = selected.class_id if selected else None
    view = fibre_view(f, _selected_word(), k, class_id=class_id)
    st.markdown(f"**Fibre** class `{view.class_key}` · size {view.size} · scope {view.scope}")
    if view.truncated:
        st.warning("Layer is too large to enumerate; showing the selected state only.")
    if st.session_state.re_explain == "Explain":
        st.write("Why equivalent?" if view.size > 1 else "This visible class is a singleton.")
        for line in view.criterion:
            st.write(line)
    else:
        for line in view.criterion:
            st.code(line, language="text")
        _badge(view.badge)
    rows = [
        {"w": m.word_text, "m": m.m, "p": m.p, "residual": m.residual}
        for m in view.members[:48]
    ]
    if rows:
        st.dataframe(pd.DataFrame(rows), hide_index=True)
    if view.size > 48:
        st.caption(f"Showing 48 of {view.size} members.")
    if (
        is_x3(f)
        and k <= 8
        and st.button("Load full cross-depth fibre", key="re_full_fibre")
    ):
        full = fibre_view(f, _selected_word(), k, full_cross_depth=True, class_id=class_id)
        st.dataframe(
            pd.DataFrame(
                [
                    {"w": m.word_text, "m": m.m, "p": m.p, "residual": m.residual}
                    for m in full.members
                ]
            ),
            hide_index=True,
        )


def _compare_card(f: IntPoly, k: int) -> None:
    row = st.container(horizontal=True)
    with row:
        st.button(
            "Load delayed-distinction pair",
            key="re_demo_pair",
            icon=":material/science:",
            on_click=_load_delayed_pair_cb,
        )
        st.caption(f"A = {st.session_state.re_a or '—'}    B = {st.session_state.re_b or '—'}")
    if not st.session_state.re_a or not st.session_state.re_b:
        st.caption("Set A and Set B on two residuals, then compare.")
        return
    try:
        view = compare_states(f, parse_word(st.session_state.re_a), parse_word(st.session_state.re_b), k)
    except ValueError as exc:
        st.error(str(exc))
        return
    _render_compare(view, k)


def _render_compare(view: CompareView, k: int) -> None:
    left, right = st.columns(2)
    with left:
        st.markdown("**State A**")
        st.code(_state_block(view.left), language="text")
    with right:
        st.markdown("**State B**")
        st.code(_state_block(view.right), language="text")
    st.markdown("**Finite-horizon relation**")
    st.metric("Same class", "YES" if view.same_class else "NO", border=True)
    rows = [
        {
            "coord": f"N{row.index}",
            "A": row.left,
            "B": row.right,
            f"A mod 3^{k}": row.left_mod,
            f"B mod 3^{k}": row.right_mod,
            "verdict": "equal" if row.equal else "DIFFERENT",
        }
        for row in view.newton_rows
    ]
    st.dataframe(pd.DataFrame(rows), hide_index=True)
    if view.first_difference:
        st.write(f"First visible difference: coordinate {view.first_difference}")
    st.write(view.explanation)
    if view.tau is not None:
        st.write(f"First distinguishing horizon τ = {view.tau}. Same through k = {view.same_through}.")
    if view.shortest:
        st.write(f"Shortest distinguishing continuation: {format_word(view.shortest)}")
    st.markdown("**Difference microscope**")
    st.code(
        "\n".join(
            (
                f"h(x) = {view.difference_poly}",
                f"Newton Δ^j h(0) = {view.difference_newton}",
                f"v3 = {view.difference_valuations}",
                f"At horizon k={k}: {'equivalent' if view.same_class else 'distinguishable'}",
            )
        ),
        language="text",
    )
    if st.session_state.re_explain == "Research":
        _badge(view.badge)


def _state_block(state) -> str:
    return "\n".join(
        (
            f"prefix: {state.word_text}",
            f"m: {state.m}",
            f"p: {state.p}",
            f"f(x): {state.exact}",
        )
    )


def _dual_card(k: int) -> None:
    x2, x3 = _cached_dual(k, bool(st.session_state.re_allow_expensive))
    left, right = st.columns(2)
    with left:
        st.markdown("**x^2**")
        st.caption(x2.caption)
        st.metric("Merged", x2.merged if x2.merged is not None else "—", border=True)
        st.metric("Raw / observable", f"{x2.raw} / {x2.observable}", border=True)
        if st.session_state.re_explain == "Research":
            _badge(x2.badge)
    with right:
        st.markdown("**x^3**")
        st.caption(x3.caption)
        st.metric("Merged", x3.merged if x3.merged is not None else "—", border=True)
        st.metric("Raw / observable", f"{x3.raw} / {x3.observable}", border=True)
        if x3.warning:
            st.warning(x3.warning)
        if st.session_state.re_explain == "Research":
            _badge(x3.badge)
