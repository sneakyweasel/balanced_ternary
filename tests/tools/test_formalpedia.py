"""The theorem index, and the two invariants it exists to keep honest.

The corpus is sorry-free and all but a named handful is kernel-checked.  Both facts are
asserted in the manuscripts, so both are worth a test that reads the Lean rather than the
prose: Paper A's Section 1.2 states the trust boundary positively, and a new
``native_decide`` slipping in anywhere would make that sentence false.
"""

from __future__ import annotations

import io
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
TOOLS = REPO / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import formalpedia as fp

JUGGLER_COMPILER_TRUST = {
    "greedy_eq_ostro_below_window",
    "window_digit_scan",
}
"""The two Ostrowski scans Paper A names as the only proofs off the kernel in its layer."""


def test_the_index_covers_the_libraries_and_not_the_build_output() -> None:
    paths = fp.sources()
    assert paths, "no Lean sources found"
    assert not any(".lake" in p.parts for p in paths)


def test_every_declaration_carries_its_location_and_trust() -> None:
    index = fp.build()
    assert index["totals"]["declarations"] > 3000
    for d in index["declarations"]:
        assert d["name"] and d["module"] and d["file"]
        assert d["line"] >= 1
        assert d["trust"] in {"kernel", "compiler", "open"}


def test_the_corpus_carries_no_sorry() -> None:
    index = fp.build()
    open_ = [d["name"] for d in index["declarations"] if d["trust"] == "open"]
    assert open_ == [], open_


def test_the_juggler_layer_keeps_only_the_two_named_scans_off_the_kernel() -> None:
    index = fp.build()
    found = {
        d["name"]
        for d in index["declarations"]
        if d["trust"] == "compiler" and d["module"].startswith("Problems.Juggler")
    }
    assert found == JUGGLER_COMPILER_TRUST, found


def test_a_docstring_belongs_to_the_declaration_it_sits_above() -> None:
    """Regression: reaching backwards for any earlier ``/--`` gave one paragraph to many."""
    text = "/-- First. -/\ntheorem a : True := trivial\n\ntheorem b : True := trivial\n"
    assert fp._docstring(text, text.index("theorem a")) == "First."
    assert fp._docstring(text, text.index("theorem b")) == ""


def test_dependents_reverses_the_import_graph() -> None:
    index = fp.build()
    rev = fp.dependents(index)
    for target, importers in rev.items():
        for name in importers:
            assert target in index["modules"][name]["imports"]


def test_impact_of_a_leaf_is_a_superset_of_its_direct_importers() -> None:
    index = fp.build()
    rev = fp.dependents(index)
    for module in list(index["modules"])[:40]:
        assert set(rev.get(module, [])) <= set(fp.transitive(rev, module))


def test_the_claim_graph_is_acyclic_and_reduced() -> None:
    """A DAG is only useful if it is both: cycles make it unreadable, redundancy makes it long."""
    index = fp.build()
    ledger = json.load(io.open(fp.LEDGER, encoding="utf-8"))
    g = fp.dag(index, ledger)
    edges = {name: set(node["depends_on"]) for name, node in g["nodes"].items()}

    # acyclic: a depth-first walk never revisits a node on its own stack
    state: dict[str, int] = {}

    def visit(n: str) -> None:
        state[n] = 1
        for d in edges.get(n, ()):
            assert state.get(d) != 1, f"cycle through {n} -> {d}"
            if state.get(d) is None:
                visit(d)
        state[n] = 2

    for n in edges:
        if state.get(n) is None:
            visit(n)

    # reduced: no edge is implied by a two-step path already in the graph
    for n, ds in edges.items():
        for d in ds:
            assert not (edges.get(d, set()) & ds), f"{n} -> {d} is implied by another path"

    assert g["totals"]["edges"] < g["totals"]["edges_before_reduction"]


def test_every_graph_node_carries_at_least_one_ledger_row() -> None:
    """The graph is over claims, not over the whole corpus; a node with no row is noise."""
    index = fp.build()
    ledger = json.load(io.open(fp.LEDGER, encoding="utf-8"))
    g = fp.dag(index, ledger)
    empty = [n for n, node in g["nodes"].items() if not node["ledger"]]
    assert empty == [], empty


def test_proposals_are_never_written_into_the_ledger() -> None:
    """The queue is advisory. Its own calibration is why: 96% precision is one wrong
    mapping in twenty-five, fine for a list a person reads and wrong for a ledger whose
    purpose is making a claim checkable."""
    index = fp.build()
    ledger = json.load(io.open(fp.LEDGER, encoding="utf-8"))
    out = fp.propose(index, ledger)
    proposed = {r["id"] for r in out["rows"]}
    resolved = {r["id"] for r in ledger if r.get("decl")}
    assert not (proposed & resolved), sorted(proposed & resolved)[:5]
    for r in out["rows"]:
        assert r["confidence"] in {"review", "low"}


def test_every_proposed_candidate_lives_in_the_row_s_own_file() -> None:
    index = fp.build()
    ledger = json.load(io.open(fp.LEDGER, encoding="utf-8"))
    by_file = {}
    for d in index["declarations"]:
        by_file.setdefault(d["file"], set()).add(d["name"])
    for r in fp.propose(index, ledger)["rows"]:
        lean = r.get("lean")
        if not (isinstance(lean, str) and lean.endswith(".lean")):
            continue
        names = by_file.get("formal/" + lean, set())
        for c in r["candidates"]:
            assert c["decl"] in names, f"{r['id']}: {c['decl']} not in {lean}"


PAPER_A_OFF_KERNEL = ["greedy_eq_ostro_below_window", "window_digit_scan"]
"""Paper A's Section 1.2 states the trust boundary positively: kernel-checked throughout the
layer except the two Ostrowski scans.  This is that sentence, as an assertion."""


def test_paper_a_keeps_exactly_the_two_ostrowski_scans_off_the_kernel() -> None:
    surface = fp.paper_surface(fp.build())["Paper A"]
    assert surface["present"], "Problems.JugglerPaper is missing from the index"
    assert surface["compiler_trusted"] == PAPER_A_OFF_KERNEL, surface["compiler_trusted"]


def test_paper_b_is_kernel_checked_throughout() -> None:
    surface = fp.paper_surface(fp.build())["Paper B"]
    assert surface["present"], "Problems.JugglerParityPaper is missing from the index"
    assert surface["compiler_trusted"] == [], surface["compiler_trusted"]


def test_no_paper_reaches_a_sorry() -> None:
    """A `sorry` anywhere under a paper root would make its verification claim false."""
    for label, surface in fp.paper_surface(fp.build()).items():
        if surface["present"]:
            assert surface["open"] == [], f"{label}: {surface['open']}"


def test_paper_reachability_is_not_the_same_set_as_the_directory() -> None:
    """Why the paper roots matter: the Juggler directory holds modules no paper imports, so a
    directory count answers a different question than a trust sentence does.  If these ever
    coincided the distinction would be free, and the roots could be dropped."""
    index = fp.build()
    reach = fp.reachable(index)
    root = fp.PAPER_ROOTS["Paper A"]
    reached = reach.get(root, set()) | {root}
    in_dir = {m for m in index["modules"] if m.startswith("Problems.Juggler")}
    assert in_dir - reached, "every Juggler module is now reachable from Paper A"
    assert reached & in_dir, "Paper A reaches no Juggler module at all"


def test_declares_requires_the_name_to_end_at_the_match() -> None:
    """The corpus names helper lemmas by extending their main theorem, so 535 of 4,588 names
    are a proper prefix of another. A substring check cannot tell them apart; this one can."""
    text = (
        "theorem power_bound_compensated_contracts_follows (h : True) : True := trivial\n"
    )
    assert not fp.declares(text, "power_bound_compensated_contracts")
    assert fp.declares(text, "power_bound_compensated_contracts_follows")


def test_declares_finds_a_real_declaration_in_the_corpus() -> None:
    path = fp.ROOT / "formal" / "Problems" / "Juggler" / "CycleFinance.lean"
    text = path.read_text(encoding="utf-8")
    assert fp.declares(text, "cycleMin_finance")
    assert not fp.declares(text, "cycleMin_financ")
    assert not fp.declares(text, "cycleMin_finance_extra_suffix")


def test_the_prefix_collision_surface_is_real_and_measured() -> None:
    """If this ever drops to zero the `declares` boundary stops mattering and can go."""
    names = {d["name"] for d in fp.build()["declarations"]}
    shadowed = {n for n in names if any(o != n and o.startswith(n) for o in names)}
    assert len(shadowed) > 100, len(shadowed)


def test_the_index_sees_declarations_behind_a_modifier() -> None:
    """Regression: a pattern anchored at ``theorem`` misses ``private theorem`` silently.

    62 declarations were invisible until the modifier list existed, and the four
    ``native_decide`` lemmas among them were being charged to a kernel-checked neighbour.
    """
    index = fp.build()
    found = {d["name"]: d for d in index["declarations"]}
    for name in ("odd_all_odd_state", "pow_mono_base", "fanLambda", "carry"):
        assert name in found, name
    assert found["fanLambda"]["kind"] == "def"
    assert found["odd_all_odd_state"]["kind"] == "theorem"


def test_native_decide_is_charged_to_the_lemma_that_calls_it() -> None:
    """The four Ostrowski residue scans are private, so a modifier-blind index attributed all
    four to ``origin_reachable_pred`` above them -- which uses no such thing."""
    index = fp.build()
    trust = {d["name"]: d["trust"] for d in index["declarations"]
             if d["module"] == "Problems.Ostrowski.NP.Reachability"}
    assert trust["origin_reachable_pred"] == "kernel"
    for suffix in ("four", "eight", "sixteen", "twenty"):
        assert trust[f"combo_residue_ne_zero_{suffix}"] == "compiler", suffix


def test_prose_that_wraps_onto_the_word_theorem_is_not_a_declaration() -> None:
    """``LeftoverFamilies.lean`` ends a docstring line with "not a `CycleItinerary`" and starts
    the next with "theorem at a non-minimum start". Read as source that declares ``at``, whose
    name then matched the ``at`` of every ``rw ... at h`` in the corpus: 512 phantom edges."""
    index = fp.build()
    names = {d["name"] for d in index["declarations"]}
    assert "at" not in names
    assert "needs" not in names


def test_the_comment_stripper_preserves_every_offset() -> None:
    """Positions are reported from the stripped text into the original, so the two must agree
    character for character."""
    for path in fp.sources()[:60]:
        text = path.read_text(encoding="utf-8")
        assert len(fp._strip_comments(text)) == len(text), path


def test_the_statement_proof_cut_ignores_an_assignment_inside_a_binder() -> None:
    """An optional argument writes ``:=`` inside its own binder; the cut must pass over it."""
    statement, proof = fp._split("theorem t (h : P := by simp) : Q := by exact foo h")
    assert statement == "theorem t (h : P := by simp) : Q "
    assert proof == " by exact foo h"
    assert fp._split("def f : Nat := 3") == ("def f : Nat ", " 3")
    assert fp._split("def f : Nat -> Nat | 0 => 1")[1] == "", "no value half to find"


def test_a_neighbours_docstring_is_not_a_dependency() -> None:
    """A declaration's slice runs to the next one's start, so it carries that neighbour's
    prose -- and the house style cites theorems by name in prose."""
    slice_ = "theorem a : P := trivial\n\n/-- Follows from `cited_lemma`. -/\n"
    statement, proof = fp._split(fp._strip_comments(slice_))
    known = {"cited_lemma", "trivial"}
    assert fp._uses(proof, known, "a") == ["trivial"]
    assert "cited_lemma" not in fp._uses(statement + proof, known, "a")

    index = fp.build()
    finance = next(d for d in index["declarations"] if d["name"] == "cycleMin_finance")
    assert finance["type_deps"] == ["CycleMin", "oddCount"], finance["type_deps"]


def test_dependencies_point_at_declarations_that_exist() -> None:
    index = fp.build()
    names = {d["name"] for d in index["declarations"]}
    for d in index["declarations"]:
        assert d["name"] not in d["type_deps"] and d["name"] not in d["value_deps"]
        assert set(d["type_deps"]) <= names
        assert set(d["value_deps"]) <= names
    assert index["totals"]["type_edges"] > 1000
    assert index["totals"]["value_edges"] > index["totals"]["type_edges"]


def test_a_statement_dependency_is_not_merely_a_proof_dependency() -> None:
    """The split is the point: if every proof dependency were also a statement one, the module
    graph would already say everything this adds."""
    index = fp.build()
    proof_only = sum(
        1 for d in index["declarations"]
        for n in d["value_deps"] if n not in d["type_deps"]
    )
    assert proof_only > index["totals"]["type_edges"] / 4, proof_only
