"""Finite-dynamics companion, merged into the laboratory Streamlit app."""

from __future__ import annotations

import altair as alt
import pandas as pd
import streamlit as st

from visualization.juggler_finite_dynamics import (
    CENSUS_LEDGER_IDS,
    CLAIM_ROWS,
    CYCLE_WORD_MAX,
    CYCLE_WORD_PRESETS,
    DESCENT_WINDOW_MAX,
    LEFTOVER_CUTOFF,
    N_PRESETS,
    NOTE_ORBIT_3,
    NOTE_PEAK_37,
    ORBIT_STEPS_MAX,
    WORD_MAX,
    WORD_PRESETS,
    census_inventory,
    classify_word,
    compose_view,
    cycle_class_view,
    descent_view,
    descent_window,
    envelope_view,
    even_cell_view,
    format_int,
    four_block_replay,
    leftover_table,
    leftover_words,
    length_eight_open_words,
    next_square_view,
    odd_cell_view,
    parse_cycle_word,
    parse_word,
    try_cycle_word,
    walk_orbit,
)
from visualization.theorem_ledger import badge_payload


def _init_state() -> None:
    defaults = {
        "juggler_view": "Orbit",
        "juggler_n": 3,
        "juggler_word": "OOE",
        "juggler_cycle_word": "OEO",
        "juggler_cycle_shift": 0,
        "juggler_steps": 20,
        "juggler_split": 1,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
    st.session_state.shared_integer = int(st.session_state.juggler_n)


def _badge(theorem_id: str) -> None:
    payload = badge_payload(theorem_id)
    if not payload:
        return
    kind = payload["kind"]
    color = {
        "exact": "green",
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


def _set_n(n: int) -> None:
    st.session_state.juggler_n = n
    st.session_state.shared_integer = n


def _n_controls() -> int:
    def _apply_preset() -> None:
        name = st.session_state.get("juggler_n_preset")
        if name:
            _set_n(N_PRESETS[name])

    st.pills(
        "Start presets",
        list(N_PRESETS),
        selection_mode="single",
        key="juggler_n_preset",
        on_change=_apply_preset,
    )
    n = int(
        st.number_input(
            "Start n",
            min_value=1,
            step=1,
            key="juggler_n",
            help="Positive integer. Shared with the rest of the laboratory.",
        )
    )
    st.session_state.shared_integer = n
    return n


def _word_controls() -> str:
    def _apply_preset() -> None:
        name = st.session_state.get("juggler_word_preset")
        if name:
            st.session_state.juggler_word = name

    st.pills(
        "Word presets",
        list(WORD_PRESETS),
        selection_mode="single",
        key="juggler_word_preset",
        on_change=_apply_preset,
    )
    raw = st.text_input(
        "Parity word",
        key="juggler_word",
        help=f"Letters O and E only, length at most {WORD_MAX}.",
    )
    word = parse_word(raw)
    if word is None:
        st.warning(
            f"Use only O and E, with length at most {WORD_MAX}.",
            icon=":material/warning:",
        )
        return "OOE"
    return word


def _cycle_word_controls() -> str:
    def _apply_preset() -> None:
        name = st.session_state.get("juggler_cycle_preset")
        if name:
            st.session_state.juggler_cycle_word = name
            st.session_state.juggler_cycle_shift = 0

    st.pills(
        "Cycle-word presets",
        list(CYCLE_WORD_PRESETS),
        selection_mode="single",
        key="juggler_cycle_preset",
        on_change=_apply_preset,
    )
    raw = st.text_input(
        "Cycle word",
        key="juggler_cycle_word",
        help=(
            f"Letters O and E only, length at most {CYCLE_WORD_MAX}. "
            "Rotations are the same cyclic class."
        ),
    )
    word = parse_cycle_word(raw)
    if word is None:
        st.warning(
            f"Use only O and E, with length at most {CYCLE_WORD_MAX}.",
            icon=":material/warning:",
        )
        return "OEO"
    return word


def _claim_map() -> None:
    st.caption(
        "Lean is the proof authority. This page instantiates the finite-dynamics "
        "note. It does not prove arrival at 1."
    )
    _badge("J-small-cycle-census-seven")
    cards = st.container(horizontal=True)
    with cards:
        st.metric("Census", "period ≥ 8", border=True)
        st.metric("Length ≤ 7", "LEAN", border=True)
        st.metric("Length 8", "open", border=True)
        st.metric("ReachesOne", "not claimed", border=True)
    st.dataframe(pd.DataFrame(CLAIM_ROWS), hide_index=True, width="stretch")
    st.info(
        "No density result is stated or used in the note. Finite leftover "
        "tables are checks, not a termination proof. Length eight is the "
        "first open even-terminating expanding length.",
        icon=":material/info:",
    )


def _orbit() -> None:
    st.caption(
        "The orbit of 3 is 3, 5, 11, 36, 6, 2, 1. The orbit of 37 peaks at "
        f"{NOTE_PEAK_37}. Walks stop at 1, at the step cap, or when a state "
        "exceeds the display bit cap."
    )
    _badge("J-itinerary-semantics")
    n = int(st.session_state.juggler_n)
    steps = int(
        st.slider(
            "Step cap",
            min_value=1,
            max_value=ORBIT_STEPS_MAX,
            key="juggler_steps",
        )
    )
    view = walk_orbit(n, steps)
    metrics = st.container(horizontal=True)
    with metrics:
        st.metric("Word", view.word or "—", border=True)
        st.metric("Steps recorded", len(view.states) - 1, border=True)
        st.metric("Reached 1", "yes" if view.reached_one else "no", border=True)
        st.metric("Last state", format_int(view.states[-1]), border=True)
    if view.too_large or view.bit_capped:
        st.warning(
            "A state exceeded the display bit cap. The walk stopped.",
            icon=":material/warning:",
        )
    if n == 3 and view.states[: len(NOTE_ORBIT_3)] == NOTE_ORBIT_3:
        st.success("This is the note orbit of 3.", icon=":material/check:")
    if n == 37 and NOTE_PEAK_37 in view.states:
        st.success("The recorded peak of 37 is on this walk.", icon=":material/check:")
    chart_df = pd.DataFrame(view.rows)
    chart = (
        alt.Chart(chart_df)
        .mark_line(point=True)
        .encode(
            x=alt.X("step:Q", title="step"),
            y=alt.Y("state:Q", title="state", scale=alt.Scale(type="log")),
            color=alt.Color("parity:N", title="parity"),
            tooltip=["step", "state", "letter", "bits"],
        )
    )
    st.altair_chart(chart, width="stretch")
    st.dataframe(chart_df, hide_index=True, width="stretch")


def _envelope() -> None:
    st.caption(
        "On a realized word, $J^{|w|}(n)^{2^{|w|}}\\le n^{3^{\\#O(w)}}$. "
        "The exact slack is $\\Delta_w(n)$. Powers are instantiated only "
        "inside the existing defect bit budget."
    )
    _badge("J-power-envelope-contraction")
    _badge("J-global-defect-identity")
    n = int(st.session_state.juggler_n)
    word = _word_controls()
    view = envelope_view(n, word)
    metrics = st.container(horizontal=True)
    with metrics:
        st.metric("#O", view.odd, border=True)
        st.metric("Regime", view.regime, border=True)
        st.metric("Realized", "yes" if view.follows else "no", border=True)
        st.metric(
            "Image vs n",
            f"{format_int(view.image)} {view.compared} {n}" if view.image is not None else "—",
            border=True,
        )
    if not view.follows:
        st.warning(
            f"Letter {view.fail_index} fails at state {view.fail_state}.",
            icon=":material/warning:",
        )
    slack_row = st.container(horizontal=True)
    with slack_row:
        if view.slack is not None:
            st.metric("Envelope slack Δ", format_int(view.slack), border=True)
        elif view.slack_too_large:
            st.metric("Envelope slack Δ", "too large to instantiate", border=True)
        else:
            st.metric("Envelope slack Δ", "—", border=True)
        if view.delta is not None:
            st.metric("Recurrence Δ", format_int(view.delta), border=True)
        elif view.delta_too_large:
            st.metric("Recurrence Δ", "too large to instantiate", border=True)
        else:
            st.metric("Recurrence Δ", "—", border=True)
        st.metric("Vanishing", view.vanishing, border=True)
    if view.follows and view.slack is not None and view.delta is not None:
        if view.slack == view.delta:
            st.success(
                "The identity $n^{3^{\\#O}}=m^{2^{k}}+\\Delta$ holds on this pair.",
                icon=":material/check:",
            )
    if view.steps:
        st.dataframe(pd.DataFrame(view.steps), hide_index=True, width="stretch")

    st.subheader("Composition")
    st.caption(
        "Theorem 2.6: concatenation is a two-term power-gap, not a sum of remainders."
    )
    if len(word) < 1:
        st.caption("Enter a nonempty word to split the composition.")
        composed = None
    else:
        if st.session_state.juggler_split > len(word):
            st.session_state.juggler_split = len(word)
        split = int(
            st.slider(
                "Split after this many letters",
                min_value=0,
                max_value=len(word),
                key="juggler_split",
            )
        )
        composed = compose_view(n, word[:split], word[split:])
    if composed is None:
        pass
    elif not composed.follows:
        st.caption("The concatenated word is not realized at this start.")
    elif composed.too_large:
        st.caption("The composition gaps are too large to instantiate.")
    else:
        row = st.container(horizontal=True)
        with row:
            st.metric("Δ(u)", composed.delta_u, border=True)
            st.metric("Δ(v)", composed.delta_v, border=True)
            st.metric("Δ(uv)", composed.delta_uv, border=True)
            st.metric(
                "Compose formula",
                composed.composed if composed.composed is not None else "—",
                border=True,
            )
        if composed.composed is not None and composed.composed == composed.delta_uv:
            st.success("The two-term power-gap equals Δ(uv).", icon=":material/check:")


def _cells() -> None:
    st.caption(
        "Even fibers are parity-restricted square intervals. An odd fiber "
        "contains at most one integer. The census excludes every even-terminating "
        "expanding word of length at most seven."
    )
    for theorem_id in CENSUS_LEDGER_IDS:
        _badge(theorem_id)

    left, right = st.columns(2)
    with left:
        with st.container(border=True):
            st.subheader("Even cell")
            q = int(st.number_input("Image q", min_value=0, step=1, value=6, key="juggler_q"))
            cell = even_cell_view(q)
            st.metric("Interval", f"[{cell.lo}, {cell.hi})", border=True)
            st.caption(f"{cell.even_count} even predecessors.")
            st.dataframe(
                pd.DataFrame({"even n": list(cell.evens)}),
                hide_index=True,
                width="stretch",
            )
            if cell.truncated:
                st.caption("List truncated.")
    with right:
        with st.container(border=True):
            st.subheader("Odd cell")
            m = int(st.number_input("Image m", min_value=0, step=1, value=11, key="juggler_m"))
            odd = odd_cell_view(m)
            st.metric("Integers", len(odd.integers), border=True)
            if odd.integers:
                st.dataframe(
                    pd.DataFrame({"odd n": list(odd.integers)}),
                    hide_index=True,
                    width="stretch",
                )
            else:
                st.caption("Empty odd fiber.")

    st.subheader("Word playground")
    word = _word_controls()
    info = classify_word(word)
    kind_row = st.container(horizontal=True)
    with kind_row:
        st.metric("Expanding", "yes" if info.expanding else "no", border=True)
        st.metric("Ends even", "yes" if info.even_terminating else "no", border=True)
        st.metric("Kind", info.kind, border=True)
    st.caption(info.reason)

    n = int(st.session_state.juggler_n)
    prefix = st.segmented_control(
        "Next-square prefix",
        ["OO", "OOO"],
        default="OO",
        key="juggler_prefix",
    )
    if prefix is None:
        prefix = "OO"
    square = next_square_view(n, prefix)
    sq_row = st.container(horizontal=True)
    with sq_row:
        st.metric("Realizes prefix", "yes" if square.follows else "no", border=True)
        st.metric(
            "Image",
            format_int(square.image) if square.image is not None else "—",
            border=True,
        )
        st.metric("Threshold (n+1)²", square.threshold, border=True)
        st.metric(
            "Image ≥ threshold",
            "yes" if square.met else "no" if square.met is False else "—",
            border=True,
        )

    st.subheader("Leftover tables")
    st.caption(
        "Lemma 3.5 checks 2 ≤ n < 256. Lemma 3.7 checks 2 ≤ n < 14. "
        "These are finite evaluations, not a halt proof."
    )
    with st.form("juggler_leftover_form"):
        leftover = st.selectbox(
            "Leftover word",
            leftover_words(),
            index=0,
            key="juggler_leftover",
        )
        submitted = st.form_submit_button("Replay leftover table", icon=":material/table:")
    if submitted:
        table = leftover_table(leftover)
        hits = st.container(horizontal=True)
        with hits:
            st.metric("Checked", table.checked, border=True)
            st.metric("Realized", table.follows, border=True)
            st.metric("Returns", len(table.hits), border=True)
            st.metric("Cutoff n", table.n_hi, border=True)
        if table.hits:
            st.error(f"Unexpected return at {table.hits}.", icon=":material/block:")
        else:
            st.success(
                f"No return on 2 ≤ n < {table.n_hi} for {table.word}.",
                icon=":material/check:",
            )
        st.dataframe(pd.DataFrame(table.rows), hide_index=True, width="stretch")
    else:
        st.caption(
            "Submit the form to evaluate "
            + ", ".join(f"{word} below {cut}" for word, cut in LEFTOVER_CUTOFF.items())
            + "."
        )

    st.subheader("Census inventory")
    st.dataframe(pd.DataFrame(census_inventory()), hide_index=True, width="stretch")
    with st.expander("Length-eight expanding even-terminating words"):
        st.caption(
            "Open list only. The note does not exclude cycles of length eight."
        )
        open_words = length_eight_open_words()
        st.dataframe(
            pd.DataFrame({"word": list(open_words), "status": ["open"] * len(open_words)}),
            hide_index=True,
            width="stretch",
        )


def _descent() -> None:
    st.caption(
        "Even starts have the one-letter certificate E. Odd-to-even starts "
        "have OE. The leftover class is odd-to-odd. A window count is not "
        "a density theorem."
    )
    _badge("J-finite-progress-boundary")
    n = int(st.session_state.juggler_n)
    view = descent_view(n)
    row = st.container(horizontal=True)
    with row:
        st.metric("Bucket", view.bucket, border=True)
        st.metric("Short certificate", view.certificate, border=True)
    if view.residual:
        st.dataframe(pd.DataFrame([view.residual]), hide_index=True, width="stretch")

    window = int(
        st.slider(
            "Window n_max",
            min_value=2,
            max_value=DESCENT_WINDOW_MAX,
            value=80,
            key="juggler_window",
        )
    )
    counts = descent_window(window)
    st.dataframe(
        pd.DataFrame(
            [
                {
                    "even": counts["EVEN_PROGRESS"],
                    "odd-to-even": counts["OE_PROGRESS"],
                    "odd-to-odd leftover": counts["ODD_ODD"],
                    "n_max": counts["n_max"],
                }
            ]
        ),
        hide_index=True,
        width="stretch",
    )
    st.caption("Bounded window counts. The note states no density result.")

    st.subheader("Four-block chain at 1999")
    st.caption(
        "An existence example of four consecutive expanding blocks. "
        "It is not a uniform run bound."
    )
    chain = four_block_replay()
    st.dataframe(
        pd.DataFrame(
            [
                {
                    "start": step.start,
                    "word": step.word,
                    "image": step.image,
                    "realized": step.follows,
                    "matches note": step.matches,
                }
                for step in chain
            ]
        ),
        hide_index=True,
        width="stretch",
    )
    if all(step.matches for step in chain):
        st.success(
            "1999 —OOE→ 5169 —OOOOEE→ 50093 —OOE→ 193753 —OOE→ 887471.",
            icon=":material/check:",
        )


def _cycle_words() -> None:
    st.caption(
        "A cycle word is a cyclic object. Type a parity word, rotate it, "
        "and read the recorded obstruction. Lean is the authority. This "
        "view does not invent exclusions: length eight beyond the two-even "
        "leftovers remains open, and arrival at 1 is not claimed."
    )
    _badge("J-cycle-finite-structure")
    _badge("J-small-cycle-census-seven")
    word = _cycle_word_controls()
    if len(word) >= 2:
        if st.session_state.juggler_cycle_shift >= len(word):
            st.session_state.juggler_cycle_shift = 0
        rotate_row = st.container(horizontal=True)
        with rotate_row:
            if st.button("Rotate left", icon=":material/rotate_left:", key="juggler_rot_left"):
                st.session_state.juggler_cycle_shift = (
                    int(st.session_state.juggler_cycle_shift) + 1
                ) % len(word)
                st.rerun()
            if st.button("Rotate right", icon=":material/rotate_right:", key="juggler_rot_right"):
                st.session_state.juggler_cycle_shift = (
                    int(st.session_state.juggler_cycle_shift) - 1
                ) % len(word)
                st.rerun()
        shift = int(
            st.slider(
                "Left rotation",
                min_value=0,
                max_value=len(word) - 1,
                key="juggler_cycle_shift",
                help="The same cyclic class; only the base letter changes.",
            )
        )
    else:
        shift = 0
    view = cycle_class_view(word, shift)
    metrics = st.container(horizontal=True)
    with metrics:
        st.metric("Spelling", view.current or "—", border=True)
        st.metric("#O / #E", f"{view.odd} / {view.even}", border=True)
        st.metric("Expanding", "yes" if view.expanding else "no", border=True)
        st.metric(
            "This class",
            "cannot exist" if view.verdict == "excluded" else view.verdict,
            border=True,
        )
    if view.ledger:
        _badge(view.ledger)
    if view.verdict == "excluded":
        st.error(view.verdict_reason, icon=":material/block:")
    elif view.verdict == "open":
        st.warning(view.verdict_reason, icon=":material/help:")
    else:
        st.info("Enter a nonempty O/E word.", icon=":material/info:")

    st.subheader("This spelling")
    spelling = st.container(horizontal=True)
    with spelling:
        st.metric("Kind", view.current_kind, border=True)
        st.metric("CycleMin", "yes" if view.current_legal else "no", border=True)
        st.metric(
            "Blocked by",
            view.current_blocked_by or "—",
            border=True,
        )
    st.caption(view.current_reason)

    st.subheader("Why this class cannot exist")
    for step in view.steps:
        with st.container(border=True):
            status_color = {
                "ok": "green",
                "blocks": "red",
                "open": "orange",
                "info": "gray",
            }.get(step.status, "gray")
            head = st.container(horizontal=True)
            with head:
                st.markdown(f"**{step.title}**")
                st.badge(step.status, color=status_color)
            st.caption(step.body)
            if step.ledger:
                _badge(step.ledger)

    st.subheader("Rotations")
    st.dataframe(
        pd.DataFrame(
            [
                {
                    "shift": row.shift,
                    "word": row.word,
                    "ends E": row.even_terminating,
                    "expanding": row.expanding,
                    "CycleMin": row.legal_cyclemin,
                    "blocked by": row.blocked_by or "—",
                    "kind": row.kind,
                    "reason": row.reason,
                    "selected": row.selected,
                }
                for row in view.rotations
            ]
        ),
        hide_index=True,
        width="stretch",
    )

    st.subheader("Try this spelling at n")
    st.caption(
        "If the word were a cycle at the shared start n, the image after "
        "the word would equal n. A missed letter or a non-return is a "
        "witness at this n only, not a census."
    )
    trial = try_cycle_word(int(st.session_state.juggler_n), view.current)
    try_row = st.container(horizontal=True)
    with try_row:
        st.metric("Realized", "yes" if trial.follows else "no", border=True)
        st.metric(
            "Image",
            format_int(trial.image) if trial.image is not None else "—",
            border=True,
        )
        st.metric(
            "Returned",
            "yes" if trial.returned else "no" if trial.returned is False else "—",
            border=True,
        )
    if trial.bit_capped:
        st.warning(
            "A state exceeded the display bit cap. The walk stopped.",
            icon=":material/warning:",
        )
    elif not trial.follows and trial.fail_index is not None:
        st.caption(
            f"Letter {trial.fail_index} fails at state "
            f"{format_int(trial.fail_state) if trial.fail_state is not None else '—'}."
        )
    elif trial.returned:
        st.error(
            "Unexpected return at this n. The recorded census claims none.",
            icon=":material/block:",
        )
    elif trial.follows:
        st.success(
            "This spelling is realized at n and does not return.",
            icon=":material/check:",
        )


def juggler_finite_dynamics_page() -> None:
    _init_state()
    st.caption(
        "Paper companion for Small cycles of the Juggler map. Lean is the "
        "proof authority. This UI only instantiates witnesses. Arrival at 1 "
        "is not claimed."
    )
    view = st.segmented_control(
        "View",
        ["Claim map", "Orbit", "Envelope", "Cells and census", "Cycle words", "Descent"],
        key="juggler_view",
    )
    _n_controls()
    if view == "Claim map":
        _claim_map()
    elif view == "Orbit":
        _orbit()
    elif view == "Envelope":
        _envelope()
    elif view == "Cells and census":
        _cells()
    elif view == "Cycle words":
        _cycle_words()
    else:
        _descent()


juggler_finite_dynamics_page()
