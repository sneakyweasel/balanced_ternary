# Rewrite-calculus explorer — UI/UX plan

Status: **Phase 0 merged into the laboratory Streamlit app**
(`btlab ui` → Calculus research → Rewrite calculus). Isolated
reviewer deploy is deferred; this UI is for laboratory use. This is
infrastructure for a surviving paper candidate, not a new rewrite
theorem.

Sendable paper unit remains the
[reviewer packet](rewrite_calculus_reviewer_packet.md) plus the
[publication draft](rewrite_calculus_note.md). The UI is a companion
that *instantiates* those theorems. Lean stays the proof authority.

```text
Mathematical target     none — presentation of existing theorems
Novelty hypothesis      none
Falsifier               the UI invites new rules, word-table play, or
                        treats a census as a proof
Existing machinery      rewrite_expr / rewrite_once, TREE_RULES, D / I_a,
                        test_rewrite_add_boundary witnesses, Streamlit
                        app_pages + st.navigation
Maximum Phase-0 scope   one isolated 5-page Streamlit app over the four
                        Lean witnesses and the unary stepper; no new
                        rules, CLI census, or lab-sidebar dump
Promotion criterion     a reviewer can replay the packet witnesses
                        without opening residuals or Collatz
Stop criterion          a rule editor, word-fragment view, Add installed
                        in _step, or a second paper repo
```

## 1. Audience and job

Two users, one implementation.

| User | Job | Success |
|------|-----|---------|
| Author | play the four witnesses and the unary stepper | every packet row is one click |
| Reviewer | check interpretation of `add_requires_carry_state` | they never leave the paper spine |

The existing laboratory UI fails that job. `btlab ui` is a
Collatz-and-residuals shell. The packet already says not to send the
laboratory. Do **not** add this as another page under
“Calculus research” next to the Residual explorer as the reviewer
entry point.

## 2. Product shape

**One isolated Streamlit app**, launched by a dedicated command
(`btlab rewrite explorer`), with its own `st.navigation` and **no**
Residual / Collatz / Calculator pages.

Reuse the current stack: Streamlit, `app_pages/`, native widgets,
Material icons, sentence case, no custom CSS. Math logic stays in
`bt.calculus`. A thin view-model
`src/visualization/rewrite_explorer.py` formats witnesses. Pages live
in `src/visualization/app_pages/rewrite_*.py`. The dossier module
`research.rewrite_calculus` stays a pointer; it does not grow a UI
engine.

Optional later, and only after Phase 0 works: a single caption link
from the laboratory Overview. Never the reverse — the paper app must
not link into Collatz or residuals.

### What “play” means

Play is **instantiate a proved statement**, not invent a rewrite
system.

Allowed:

- build a unary `{D, I_a, S, N}` term and step `rewrite_once`;
- evaluate at an integer;
- change `(x, y)` and watch \(D(x+y)\) versus \(D(x)+D(y)\);
- pick constructors \(U,V,W\) and see whether \(U(x)+V(y)=W(x+y)\);
- inspect the named peak \(D(S(X+Y))\).

Forbidden:

- add or edit rules;
- install `Add` / `Mul` in `_step`;
- open `WORD_*` fragments;
- run a census and badge it as a proof;
- quantify over “any TRS”.

## 3. Information architecture

Five pages, **top navigation**, paper order. Few pages: Streamlit
guidance is top nav, not a lab sidebar.

```text
Claim map → Unary calculus → Carry → Constructor sums → Push-in peak
```

Persistent chrome (every page):

- title: “Rewrite calculus companion”
- caption: “Lean is the proof authority. This UI only instantiates
  the paper witnesses.”
- badges for the page claim: `LEAN VERIFIED` / `HUMAN PROOF` /
  `KNOWN`
- a short “not claimed” line
- links: packet, note section, Lean theorem name

Deep links (query params) so a reviewer can be sent one witness:

| URL fragment | Lands on |
|--------------|----------|
| `?page=claims` | claim map |
| `?page=unary&preset=nd` | `N(D(x))` vs `D(N(x))` |
| `?page=carry&x=0&y=0` / `&x=1&y=1` | D-locality pair |
| `?page=sums&U=Ip&V=Ip&W=S` | same-sign failure |
| `?page=peak` | named push-in peak |

## 4. Page wireframes

Native Streamlit only: `st.metric`, `st.container(border=True)`,
`st.segmented_control`, `st.pills`, `st.dataframe`, `st.form` for
integer pairs. Prefer `st.container(horizontal=True)` over dense
column grids. No Plotly, no custom HTML term editor.

### 4.1 Claim map (home)

Purpose: stop the reviewer misreading the package.

```text
┌─────────────────────────────────────────────────────────────┐
│ Rewrite calculus companion                                  │
│ Review question: gap in add_requires_carry_state?           │
├──────────────┬──────────────┬──────────────┬────────────────┤
│ Unary        │ Not D-local  │ Six rows     │ Named peak     │
│ LEAN         │ LEAN         │ LEAN         │ LEAN           │
├──────────────┴──────────────┴──────────────┴────────────────┤
│ Claim table (packet map): evidence × novelty                │
│ Last row highlighted: “any Add-tree TRS is a CAS” = HUMAN   │
├─────────────────────────────────────────────────────────────┤
│ What this is not: addition impossible; Avizienis refuted;   │
│ word table confluent; cubic frontier moved                  │
└─────────────────────────────────────────────────────────────┘
```

Widgets: four metric cards (click or pills jump to the page).
Dataframe is the packet claim map. No computation.

### 4.2 Unary calculus

Purpose: feel Claim A. The oriented rule `N(D)→D(N)` is the point.

```text
┌─ Builder ──────────────────┬─ Reduction ────────────────────┐
│ pills: D  I-  I0  I+  S  N │ current term                    │
│ [clear] [step] [normalize] │ last rule                       │
│ presets: N∘D, D∘N, D∘S∘I+  │ rank (I0, N-inv, size)          │
│ evaluate at n: [  ]        │ value at n                      │
└────────────────────────────┴────────────────────────────────┘
│ Compare A | B   same NF?   same value at n?                  │
│ Without N(D) they are distinct irreducibles (shown as text)  │
```

Implementation: build `Expr` with `ED` / `EIm` / `EI0` / `EIp` /
`EShift3` / `ENeg` over a hole (`EInt` only at evaluate time, or a
named `var` displayed as `x`). Step with `rewrite_once`. Normalize
with `rewrite_expr`. Do not expose `EAdd` on this page.

Preset `N(D(x))` vs `D(N(x))` is required. Show they share a normal
form **with** the commute, and state that without it they were the
semantic twins (`BTC-op-fragment-semantic-nf`, REFUTED).

### 4.3 Carry / non-D-locality

Purpose: the `(0,0)` vs `(1,1)` witness becomes visible.

```text
┌─ Inputs (form) ────────────┬─ Trits ────────────────────────┐
│ x [ number ]  y [ number ] │ lsd(x)  lsd(y)  carry          │
│ presets: (0,0)  (1,1)      │                                │
├──────────────┬─────────────┼──────────────┬─────────────────┤
│ D(x)         │ D(y)        │ D(x+y)       │ D(x)+D(y)       │
└──────────────┴─────────────┴──────────────┴─────────────────┘
│ Verdict: D(x+y) = D(x)+D(y)+carry                           │
│ If D(x)=D(y)=0 and D(x+y) differs, Add is not D-local       │
```

Use `st.form` so dragging numbers does not rerun mid-edit. Preset
pills set `(0,0)` and `(1,1)` without typing. Show the identity
`D_add` as the explanation, not as a new theorem.

Optional second row: “try to invent \(G(D(x),D(y))\)” is **not**
offered. The existence failure is the theorem; a search box would
fake a census.

### 4.4 Constructor sums

Purpose: the six-row classification is exhaustive on `{S,I+,I-,N}`.

```text
│ U [S|I+|I-|N]   V [S|I+|I-|N]   W [S|I+|I-|N]               │
│ slopes / constants                                           │
│ exact?  yes → which row     no → residue or slope mismatch   │
│                                                              │
│ Table of the eight concrete triples (I_a parameterized = 6)  │
│ Highlight: I++I+ = 3(x+y)+2, residue 2 is not a trit         │
```

`st.segmented_control` for `U,V,W`. Evaluate the identity at a small
default pair and algebraically via slope/const (already the Lean
criterion). Dataframe of exact triples is static. Same-sign `I+` /
`I-` and mixed `N+S` are the required negative rows.

### 4.5 Push-in peak

Purpose: one named carry-free extension fails, and that is all Lean
claims.

```text
│ Term: D(S(Add(X,Y)))                                         │
│ Left descendant: Add(X,Y)          rule D∘S                  │
│ Right descendant: D(Add(S(X),S(Y))) rule S-through-Add       │
│ Both irreducible in the named system                         │
│ Both evaluate to x+y   (optional X,Y integers)               │
│ Caption: not a theorem about every TRS containing Add        │
```

This page **simulates** the named `AddTree` relation. It must not
call production `rewrite_expr` on `EAdd` (those rules are not in
`_step`). Hard-code the two `PushInStep` edges from the Lean file
and evaluate the integer semantics. That keeps the UI honest: Add
is displayed as a *counterexample object*, not as a new engine.

## 5. Reviewer-facing UX rules

1. **Proof authority is written on every page.** Badges: Lean name,
   ledger id, evidence tag. A green “works” metric is not a proof.
2. **Presets before free play.** The packet witnesses are pills at
   the top of each page. Free integers come second.
3. **The human corollary is visually weaker.** On the claim map the
   CAS sentence is a separate, non-green row. Do not put it in a
   metric card.
4. **No laboratory gravity in the chrome.** No Residual explorer,
   no Collatz, no word-table toggle, no “open the ledger app”.
5. **Centered layout**, readable width. This is a paper companion,
   not a dashboard. `layout="centered"` except the constructor table
   if it needs `wide`.
6. **Empty / error states.** Hole-only term: “this is already
   irreducible.” Huge integers: cap evaluate-at `n` to a modest
   range; the theorems are identities, not a stress test.
7. **Mobile.** Top nav plus stacked containers. Do not rely on a
   four-column grid.

## 6. How a reviewer sees it

Do **not** create a second GitHub repo for this. Deploy or share the
isolated entry.

| Stage | How the reviewer sees it |
|-------|--------------------------|
| Now (no UI) | packet + note |
| After Phase 0 | `btlab rewrite explorer` on a tagged commit |
| After Phase 1 | same command, or Streamlit Community Cloud pointed at the isolated entry file only |
| Never | `btlab ui` as the review surface |

A Cloud deploy is optional packaging. It is not a new research
module. Pin a tag. If Cloud is too coupled to the monorepo, a
screen-share or a short recorded click-through of the four presets
is enough. The paper remains the artifact; the UI is a witness
player.

## 7. Implementation layers (when built)

```text
visualization/rewrite_streamlit_app.py   isolated entry, top nav
visualization/app_pages/rewrite_*.py     five page scripts
visualization/rewrite_explorer.py        view-model, cached, no Streamlit
bt.calculus.{rewrite,derivative,integral}  existing math only
```

`visualization` may import `bt.*`. It must not import
`research.residuals` or `research.collatz`. Do not add shims in
`bt.calculus`.

Tests: page-level view-model tests that the four packet witnesses
render the Lean numbers (`D(0+0)=0`, `D(1+1)=1`, `I++I+` residue 2,
peak descendants). No Streamlit screenshot tests. No new ledger row.

## 8. Phased build

**Phase 0 — witness player (stop here if this is enough)**

- isolated entry + three pages: Carry, Constructor sums, Push-in peak
- claim badges and “not claimed” captions
- presets only; unary stepper deferred
- command `btlab rewrite explorer`

Promotion: a reviewer can replay `add_requires_carry_state` without
the laboratory shell.

**Phase 1 — unary stepper**

- Claim map + Unary page
- `rewrite_once` / `rewrite_expr` on `{D,I_a,S,N}` only
- `N(D)` vs `D(N)` preset

**Phase 2 — reviewer packaging**

- query-param deep links
- packet/note links in chrome
- optional Streamlit Cloud on a tag
- one Overview caption in the lab app, outbound only

Do not open a Phase 3. A term-graph visualizer, a critical-pair
browser, or a word-fragment toggle would be machinery gravity.

## 9. Explicit non-goals

- a public paper GitHub repo
- editing Lean from the UI
- coefficient-word / `Confluence.lean` explorer
- word-table `SIMP` / `WN` / `WND` playground
- Residual explorer restyling
- claiming the UI “verifies” anything

## 10. Decision after the plan

If this plan is accepted, implement **Phase 0 only**, then stop and
look at it in the browser. If Phase 0 already lets you play the
carry-state theorem, Phase 1 is optional polish, not a requirement
for sending the paper.
