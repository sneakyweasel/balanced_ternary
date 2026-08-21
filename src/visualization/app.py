"""Streamlit research explorer for balanced ternary Collatz results.

Launch:

    python -m pip install -e ".[ui]"
    btprime collatz ui

This UI inspects exact identities already implemented. It does not claim
progress on the Collatz conjecture. Feature deltas are not Lyapunov
decreases. Finite graphs are samples, not the dynamics.
"""

from __future__ import annotations

import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent.parent
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from balanced_ternary.representation import encode
from collatz.automata.joint_graph import build_joint_graph, synchronizing_digit_contexts
from collatz.automata.two_adic import TwoAdicDigitAutomaton
from collatz.automata.valuation_shift import AdmissibleValuationAutomaton
from collatz.inverse import build_inverse_tree, format_inverse_tree
from collatz.trajectory import collatz_trajectory
from visualization.views import (
    automaton_partition_rows,
    complexity_spectrum_rows,
    cylinder_view,
    entropy_comparison_rows,
    number_view,
    odd_part_trace,
    symbolic_graph_rows,
    trajectory_rows,
    transducer_complexity_rows,
)


def launch() -> int:
    """Start Streamlit on this file. Requires the optional ``ui`` extra."""
    try:
        import streamlit  # noqa: F401
    except ImportError:
        print(
            "Streamlit is not installed. From the project directory:\n"
            '  python -m pip install -e ".[ui]"\n'
            "  btprime collatz ui"
        )
        return 1
    import subprocess

    target = Path(__file__).resolve()
    cmd = [sys.executable, "-m", "streamlit", "run", str(target), "--browser.gatherUsageStats", "false"]
    return int(subprocess.call(cmd))


def _bt_html(word: str) -> str:
    bits: list[str] = []
    for ch in word:
        if ch == "+":
            color = "#2e7d32"
        elif ch == "-":
            color = "#c62828"
        else:
            color = "#616161"
        bits.append(
            f'<span style="color:{color};font-family:ui-monospace,Consolas,monospace">{ch}</span>'
        )
    return (
        '<code style="font-size:1.2rem;letter-spacing:0.04em">'
        + "".join(bits)
        + "</code>"
    )


def _main() -> None:
    import pandas as pd
    import streamlit as st

    st.set_page_config(
        page_title="Balanced ternary Collatz explorer",
        layout="wide",
    )
    st.title("Balanced ternary Collatz explorer")
    st.caption(
        "Exact integer arithmetic on the accelerated map "
        "T(n) = (3n+1) / 2^{v2(3n+1)}. "
        "This interface does not solve the Collatz conjecture. "
        "Claim labels: PROVED / VERIFIED COMPUTATIONALLY / OBSERVATION."
    )

    page = st.sidebar.radio(
        "View",
        (
            "Overview",
            "Number explorer",
            "Trajectory",
            "Inverse tree",
            "2-adic automaton",
            "Odd-part transducer",
            "Valuation prefixes",
            "Joint graph",
            "Valuation languages",
        ),
    )
    st.sidebar.markdown(
        "Digits: **+** = +1, **0** = 0, **−** = −1. "
        "Displayed most-significant first; mathematics indexes from the LSD."
    )

    if page == "Overview":
        _page_overview(st)
    elif page == "Number explorer":
        _page_number(st, pd)
    elif page == "Trajectory":
        _page_trajectory(st, pd)
    elif page == "Inverse tree":
        _page_inverse(st)
    elif page == "2-adic automaton":
        _page_automaton(st, pd)
    elif page == "Odd-part transducer":
        _page_transducer(st, pd)
    elif page == "Valuation prefixes":
        _page_valuation(st, pd)
    elif page == "Joint graph":
        _page_joint(st, pd)
    else:
        _page_languages(st, pd)


def _page_overview(st) -> None:
    st.subheader("What this UI shows")
    c1, c2, c3 = st.columns(3)
    c1.metric("Primary map", "T, odd only")
    c2.metric("Layer A", "BT(3n+1) = BT(n)+")
    c3.metric("Layer B", "LSD /2^k FST")
    st.markdown(
        """
The explorer is a viewer for identities already proved or checked in the
library. It is not a search for a Collatz proof.

| Layer | Object | Status |
| --- | --- | --- |
| A | `BT(3n+1) = BT(n)+` and closed-form feature deltas | PROVED |
| B | LSD `/2` transducer; `/2^k` on each `L_k`; odd-part not one FST | PROVED |
| C | Residue step drops precision to `2^{P-k}`; budget `2^{sum k}` vs `3^m` | PROVED comparison |
| D | `w --k--> w'` as `odd_part(append_plus(w))`; finite `n ≤ N` is a sample | exact edge; sample graph |
| 3 | Cylinders of density `2^{-K}`; `H_L`; `N_k` spectrum; symbolic futures | density PROVED; sizes computational |

Growth-budget contraction is **not** a Lyapunov function.
        """
    )


def _page_number(st, pd) -> None:
    st.subheader("Number explorer")
    n = st.number_input("Positive odd integer n", min_value=1, value=27, step=2)
    if n % 2 == 0:
        st.error("n must be odd.")
        return
    view = number_view(int(n))
    a, b, c, d = st.columns(4)
    a.metric("n", view.n)
    b.metric("3n+1", view.three_n_plus_one)
    c.metric("v2(3n+1)", view.v2)
    d.metric("T(n)", view.T_n)
    st.markdown("**Balanced ternary (LSD on the right)**")
    st.markdown(
        f"BT(n) &nbsp; {_bt_html(view.bt_n)}<br>"
        f"BT(n)+ &nbsp; {_bt_html(view.append_plus_word)}<br>"
        f"BT(3n+1) &nbsp; {_bt_html(view.bt_y)}<br>"
        f"BT(T(n)) &nbsp; {_bt_html(view.bt_t)}",
        unsafe_allow_html=True,
    )
    ok = view.append_plus_matches and view.features_match
    st.success("Append-plus theorem holds for this n." if ok else "Mismatch — should not happen.")
    df = pd.DataFrame(
        view.feature_rows,
        columns=["feature", "n", "3n+1", "T(n)", "delta T−n"],
    )
    st.caption("Deltas are F(T(n)) − F(n): Layer A plus odd-part, not a Lyapunov decrease.")
    st.dataframe(df, hide_index=True, use_container_width=True)


def _page_trajectory(st, pd) -> None:
    st.subheader("Accelerated trajectory")
    col_a, col_b = st.columns(2)
    n = col_a.number_input("Start (odd)", min_value=1, value=27, step=2)
    max_steps = col_b.slider("Max steps", 1, 80, 20)
    if n % 2 == 0:
        st.error("n must be odd.")
        return
    traj = collatz_trajectory(int(n), int(max_steps))
    st.caption(
        f"reached 1: {traj.reached_one} · truncated: {traj.truncated} · "
        f"values: {len(traj.values)}"
    )
    rows = trajectory_rows(int(n), int(max_steps))
    if rows:
        df = pd.DataFrame(rows)
        st.dataframe(df, hide_index=True, use_container_width=True)
        chart = pd.DataFrame(
            {"n": [int(r["n"]) for r in rows] + [int(rows[-1]["T(n)"])]}
        )
        st.line_chart(chart, y="n")
        st.caption("Accelerated odd values along the truncated orbit (not a proof of convergence).")
        st.bar_chart(pd.DataFrame({"v2(3n+1)": [int(r["v2"]) for r in rows]}))
        st.caption("Valuation k at each step. Source: exact v2(3n+1).")
    else:
        st.write("No steps (n = 1 or max_steps = 0).")


def _page_inverse(st) -> None:
    st.subheader("Inverse accelerated tree")
    c1, c2, c3 = st.columns(3)
    root = c1.number_input("Root (odd)", min_value=1, value=1, step=2)
    depth = c2.slider("Depth", 0, 4, 2)
    k_max = c3.slider("k_max", 2, 16, 10)
    if root % 2 == 0:
        st.error("Root must be odd.")
        return
    tree = build_inverse_tree(int(root), depth=int(depth), k_max=int(k_max), max_nodes=4000)
    st.caption(f"nodes={tree.node_count} truncated={tree.truncated}")
    st.code(format_inverse_tree(tree), language="text")
    st.caption("The self-map 1 → 1 (k=2) is recorded as a cycle and not expanded.")


def _page_languages(st, pd) -> None:
    st.subheader("Valuation languages")
    st.caption(
        "Finite valuation cylinders are unique residue classes of density "
        "2^{-K} among odds (PROVED). Length-L word counts and N_k are "
        "VERIFIED COMPUTATIONALLY. N_k = 2^k+1 is a CONJECTURE. "
        "Budgets are not Lyapunov functions."
    )
    ks = st.text_input("Valuation prefix ks", value="1,2")
    leftover = st.slider("Leftover precision Q", 1, 4, 1)
    try:
        payload = cylinder_view(ks, leftover_q=int(leftover))
    except ValueError as exc:
        st.error(str(exc))
        return
    with st.container(horizontal=True):
        st.metric("P = Q+K", payload["precision"], border=True)
        st.metric("Classes", payload["class_count"], border=True)
        st.metric(
            "Density",
            f"{payload['density_numerator']}/{payload['density_denominator']}",
            border=True,
        )
        st.metric("Haar match", str(payload["matches_haar"]).lower(), border=True)
    budget = payload["budget"]
    st.caption(
        f"Budget 2^K={budget['two_power']} vs 3^m={budget['three_power']} "
        f"({budget['kind']}). Homogeneous estimate only."
    )
    st.write("Residues:", payload["residues"])

    length = st.slider("Entropy length L", 2, 8, 5)
    edf = pd.DataFrame(entropy_comparison_rows(int(length)))
    st.dataframe(edf, width="stretch", hide_index=True)
    st.caption(
        "H_L is (1/L) log_3 of padded length-L words. Canonical counts "
        "exclude leading zeros and are not mixed into H_L."
    )

    k_max = st.slider("Complexity k_max", 1, 6, 4)
    cdf = pd.DataFrame(complexity_spectrum_rows(int(k_max)))
    st.dataframe(cdf, width="stretch", hide_index=True)
    st.caption(
        "Naive 3^k is PROVED. N_k and A_k are VERIFIED COMPUTATIONALLY. "
        "N_k=2^k+1 is a CONJECTURE on the displayed range."
    )

    with st.expander("Symbolic futures graph"):
        gl = st.slider("Prefix length", 1, 3, 2)
        gk = st.slider("k_max", 1, 4, 3)
        sdf = pd.DataFrame(symbolic_graph_rows(int(gl), int(gk)))
        st.dataframe(sdf, width="stretch", hide_index=True)
        st.caption(
            "Nodes are (valuation prefix, residue, precision), not sampled integers."
        )


def _page_automaton(st, pd) -> None:
    st.subheader("TwoAdicDigitAutomaton(K)")
    precision = st.slider("Precision K", 2, 12, 8)
    n = st.number_input("Trace word of n", value=27, step=1)
    auto = TwoAdicDigitAutomaton(int(precision))
    a, b, c = st.columns(3)
    a.metric("Modulus 2^K", auto.modulus)
    b.metric("Odd states", len(auto.odd_states()))
    c.metric("Reachable from 0", len(auto.reachable_states()))
    df = pd.DataFrame(automaton_partition_rows(int(precision)))
    st.dataframe(df, hide_index=True, use_container_width=True)
    st.caption(
        "Exact k only when k < K. AT_LEAST_K means v2(3n+1) ≥ K. "
        "This classifies the valuation step, not T modulo 2^K."
    )
    if st.checkbox("Show residue path", value=True):
        word = encode(int(n))
        path = auto.run(word)
        st.code(auto.format_report(word), language="text")
        st.caption(f"Final residue {path[-1]} for BT({n}) = {word.word()}")


def _page_transducer(st, pd) -> None:
    st.subheader("Odd-part / LSD ÷2 transducer")
    x = st.number_input("Integer x (try 82 = 3·27+1)", value=82, step=1)
    payload = odd_part_trace(int(x))
    c1, c2, c3 = st.columns(3)
    c1.metric("x", payload["x"])
    c2.metric("v2(x)", "∞" if payload["v2"] is None else payload["v2"])
    c3.markdown("**BT(odd-part)**")
    c3.markdown(_bt_html(str(payload["odd_part_BT"])), unsafe_allow_html=True)
    st.markdown(f"BT(x) {_bt_html(str(payload['BT']))}", unsafe_allow_html=True)
    if payload["trace"]:
        df = pd.DataFrame(
            payload["trace"],
            columns=["carry in", "input digit", "output digit", "carry out"],
        )
        st.dataframe(df, hide_index=True, use_container_width=True)
        st.caption("LSD-first /2 Mealy trace. Final carry 0 on even integers.")
    k_max = st.slider("Complexity report up to k", 1, 6, 4)
    cdf = pd.DataFrame(transducer_complexity_rows(int(k_max)))
    st.dataframe(cdf, hide_index=True, use_container_width=True)
    st.bar_chart(cdf.set_index("k")[["naive_bound", "reachable", "minimized"]])
    st.caption(
        "Naive bound 3^k is PROVED as a product construction. "
        "Reachable / minimized sizes are VERIFIED COMPUTATIONALLY."
    )


def _page_valuation(st, pd) -> None:
    st.subheader("Admissible valuation prefixes")
    c1, c2, c3 = st.columns(3)
    precision = c1.slider("Start precision P", 4, 12, 8)
    k_max = c2.slider("k_max", 1, 6, 5)
    length = c3.slider("Max prefix length", 1, 5, 4)
    auto = AdmissibleValuationAutomaton(int(precision), int(k_max))
    report = auto.enumerate_admissible(int(length))
    a, b, c = st.columns(3)
    a.metric("Admissible prefixes", len(report.prefixes))
    b.metric("Contracting", report.contracting)
    c.metric("Expanding", report.expanding)
    st.caption(
        "Budget uses 2^{sum k} vs 3^m (exact integers). "
        "Contracting is the homogeneous estimate, not a Lyapunov function."
    )
    rows = []
    for L, words in report.by_length.items():
        for w in words[:30]:
            bgt = report.budgets[w]
            rows.append(
                {
                    "length": L,
                    "k-word": str(w),
                    "sum k": bgt.sum_k,
                    "2^{sum k}": bgt.two_power,
                    "3^m": bgt.three_power,
                    "budget": bgt.kind,
                }
            )
    st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)
    counts = {
        "length": list(report.by_length),
        "prefixes": [len(report.by_length[L]) for L in report.by_length],
    }
    st.bar_chart(pd.DataFrame(counts).set_index("length"))
    st.caption(f"Admissible prefix counts by length. Start odd residues: {report.start_count}. Source: automaton at P={precision}.")


def _page_joint(st, pd) -> None:
    st.subheader("Joint graph w —k→ w′")
    limit = st.slider("Odd n ≤ N", 10, 500, 200, step=10)
    graph = build_joint_graph(int(limit))
    by_k = graph.out_degree_by_k()
    a, b = st.columns(2)
    a.metric("Edges", len(graph.edges))
    b.metric("Images ≡ 0 (mod 3)", len(graph.images_divisible_by_three()))
    st.bar_chart(
        pd.DataFrame(
            {"k": list(by_k.keys()), "count": list(by_k.values())}
        ).set_index("k")
    )
    st.caption(
        f"Out-count by valuation k on odd n ≤ {limit}. "
        "This truncation is a sample, not the Collatz dynamics. "
        "Zero images mod 3 is PROVED for every T(n)."
    )
    sample = [
        {
            "n": e.n,
            "w": e.w,
            "k": e.k,
            "T(n)": e.n_prime,
            "w′": e.w_prime,
        }
        for e in graph.edges[:40]
    ]
    st.dataframe(pd.DataFrame(sample), hide_index=True, use_container_width=True)
    if st.checkbox("Search synchronizing right-strings (slow at large K)"):
        prec = st.slider("Automaton K", 2, 6, 4)
        slen = st.slider("String length", 1, 3, 2)
        found = synchronizing_digit_contexts(int(prec), int(slen))
        st.write(f"{len(found)} synchronizing strings of length {slen} at K={prec}")
        if found:
            st.code("\n".join(found[:80]), language="text")


if __name__ == "__main__":
    _main()
