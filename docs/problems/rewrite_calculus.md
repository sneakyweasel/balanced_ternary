# Rewrite calculus of balanced-ternary operators

Status: **PAPER_CANDIDATE — PRIOR-ART CORRECTED**

A canonical rewrite system for the unary constructors
`{D, I_a, S, N}` and an exact locality boundary:
`D(x+y)` is not determined by `(D(x),D(y))`. Canonical mathematics:
[rewrite_calculus.md](../theory/rewrite_calculus.md). Publication draft:
[rewrite_calculus_note.md](../theory/rewrite_calculus_note.md).
Reviewer packet:
[rewrite_calculus_reviewer_packet.md](../theory/rewrite_calculus_reviewer_packet.md).
This is **not** a Collatz problem and not the cubic-residual frontier.
Engine discovery of the residual that repairs `D(x+y)` lives in
[d_add_residual.md](d_add_residual.md) and does not reopen this paper.

## Problem

Whether the natural balanced-ternary unary operators admit a canonical
tree rewrite system, and whether the next state of exact addition
factors through the unary `D`-states of its operands.

## Exact statement

Let `I_a(x) = a + 3x` for `a ∈ {-1,0,+1}`, `S = I_0`,
`D(x) = (x - lsd(x))/3`, and `N(x) = -x`. Write `OpFrag` for the free
unary algebra on `{D, I_a, S, N}` over a hole `x`.

1. The finite tree TRS on `OpFrag` is terminating, confluent, and
   semantically canonical.
2. For the binary output `H(x,y)=D(x+y)`, there is no `G` satisfying
   `H(x,y)=G(D(x),D(y))` for every `x,y`.
3. The exact carry identity explains the missing state, and the named
   carry-free `S`-through-`Add` extension is not locally confluent.

## Current literature

- `newman-1942-confluence`, `baader-nipkow-1998-term-rewriting`:
  termination + local confluence ⇒ confluence; critical-pair /
  Knuth–Bendix method. `KNOWN` (method).
- `contejean-marche-rabehasaina-1997-rta` and the associated report:
  direct prior art. CMR97 uses balanced-ternary digit append
  \(x :_t a=3x+a\), the same integer map as \(I_a\), and gives
  terminating and confluent arithmetic rewrite systems modulo AC.
  Balanced-ternary arithmetic rewriting is `KNOWN`.
- `walters-zantema-1994-integer-arithmetic`: arbitrary-radix
  digit-application arithmetic TRSs. `KNOWN`.
- `bergstra-ponse-2016-ddrs-integers`: later source explicitly
  comparing CMR97 with digit-append DDRSs.
- `knuth-taocp-vol2`, `hayes-2001-third-base`: unique balanced-ternary
  expansion and least-digit quotient. `KNOWN`; \(D\) / \(I_a\) are
  `KNOWN / REFORMULATED`.
- `avizienis-1961-signed-digit`: signed-digit representation and
  limited-carry addition as an arithmetic algorithm. `KNOWN`.
- `heuberger-prodinger-2003-carry`: automata for carry propagation in
  signed-digit systems, explicitly including balanced ternary.
  Finite-state carry is `KNOWN`.
- `frougny-pelantova-svobodova-2011-parallel-addition`,
  `frougny-pelantova-svobodova-2013-minimal-digits`, and
  `frougny-heller-pelantova-svobodova-2014-k-block`: local/parallel
  addition, minimal alphabets, and block locality are `KNOWN`.
- `peterson-stickel-1981-unification-ac`: completion modulo AC is
  already a computer-algebra engine. `KNOWN` (method). Used to tag
  the AC-matching half of the factor-out obstruction, not the trit
  carry itself.
- `malinovsky-pioneers-soviet-computing`: Setun postfix evaluation.
  Historical frame only.

Consequence of the audit: digit append, balanced quotienting, arithmetic
rewriting, finite-state carry, and local/parallel addition are not new.
The surviving package is a `NEW FORMALIZATION` of the exact open unary
grammar, its semantic-injectivity theorem, and the exact
non-factorization theorem for `D(x+y)`, supported by the constructor
classification and named push-in peak. No historical priority is
claimed for those theorem statements. Full comparison:
[rewrite_calculus_prior_art.md](../theory/rewrite_calculus_prior_art.md).

## Branch budget

```text
Mathematical target     Which claims in the rewrite-calculus note survive direct comparison with CMR97 and signed-digit/parallel-addition literature?
Novelty hypothesis      The exact open {D,I_a,S,N} canonical form, necessity of the oriented N–D rule, semantic injectivity, and D-locality obstruction remain a coherent theorem/formalization package.
Falsifier               Prior literature already proves the same destructor algebra, semantic normal-form theorem, and D-locality obstruction, leaving only notation.
Existing machinery      Lean OpFrag proofs, human obstruction proofs, coefficient-word normalization, word-fragment PRs, theorem ledger, conjecture registry, and regression tests.
Maximum Phase-0 scope   Literature and documentation correction only; add no mathematics, rewrite rules, CLI, visualization, or census.
Promotion criterion     A concrete theorem-level or formalization-level distinction remains after explicit translation and conservative classification.
Stop criterion          Only notation remains, or usefulness depends on importing Paper B's research engine to manufacture novelty.
```

The promotion criterion fired narrowly: the open unary semantic
canonicality theorem and `add_not_DLocal` remain a coherent,
Lean-verified package whose scope differs from CMR97's arithmetic TRS.
The broad arithmetic novelty hypothesis was refuted. Word-table
enlargement remains closed.

## Balanced-ternary formulation

A unary term is a composition of `D`, `I_a`, `S`, `N` applied to an
integer hole. Evaluation is exact on `ℤ`. Operator words are strings
over the production alphabet (`N`, `D`, `S`, `W`, `K3`, `I±`, …).
Sums are not letters of that alphabet and are not tree constructors
in `rewrite._step`.

## Why BT may be relevant

The digit set `{-1,0,+1}` makes `I_a` and `D` exact inverses and
makes the carry of `1+1` visible as a non-trit residue `±2`. That is
what turns “add `S`-distributivity” and “factor out `I_a`” into a
named obstruction rather than a missing rule.

## Candidate operations / invariants

- OpFrag lex rank `(I0-count, N-inversion, size)` — **EXACT — HUMAN PROOF**.
- NF grammar `w(D^d(x))` or `w(D^d(N(x)))`, `w ∈ {I-,I+,S}*` — **EXACT — HUMAN PROOF**.
- Exact constructor identities `U(x)+V(y)=W(x+y)` — **EXACT — HUMAN PROOF** (six rows).
- Full `WORD_REWRITE_RULES` as a confluent TRS — **REFUTED**.
- Unified tree canonicalizer including `Add` — **REFUTED**.

## Experiments

No new runners. Existing unit tests are regression guards, not a
census programme:

- `tests/unit/test_operator_fragment_nf.py`
- `tests/unit/test_rewrite_signature_enlargement.py`
- `tests/unit/test_rewrite_factor_out_add.py`
- `tests/unit/test_rewrite_add_affine_only.py`
- `tests/unit/test_rewrite_word_fragments.py`

## Conjectures

Proved: `op_fragment_nd_semantic`, `add_affine_only`,
`add_factor_cas_obstruction`, `word_simp_nf`, `word_wn_nf`,
`word_wnd_nf`.

Refuted: `op_fragment_semantic_nf`, `add_s_push_lc`, `mul_s_push_lc`,
`add_n_push_semantic`, `add_factor_binary_semantic`,
`add_factor_ac_semantic`, `w_nd_word_lc`, `word_full_lc`,
`word_simp_nd_lc`.

No active conjecture on this line.

## Counterexamples

Named peaks, recorded in the tests above and on the ledger:

- `N(D(x))` vs `D(N(x))` without the oriented commute.
- `D(S(x+y)) → x+y | D(S(x)+S(y))`.
- `D(S(x*y)) → x*y | D(S(x)*y)`.
- `S(x)+(S(y)+z)` vs `S(x+y)+z` (binary factor-out).
- `I+(x)+S(y)+I+(z)` vs two same-sign descendants (AC factor-out).
- `N∘W∘W → N∘K3 | K3∘N` (production word table).
- `N∘D∘I± → D∘N∘I± | N` without word sign-flips.

## Formalization

Gate note: [rewrite_calculus_formalization.md](../theory/rewrite_calculus_formalization.md).
Lean, no `sorry`:

- `formal/BTCalculus/OpFrag.lean`
- `formal/BTCalculus/OpFragNewman.lean` — `BTC-op-fragment-nd-nf`
- `formal/BTCalculus/OpFragSemantic.lean` — `BTC-op-fragment-nd-semantic`
- `formal/BTCalculus/Rewrite.lean` — integer soundness of the tree rules
- `formal/BTCalculus/RewriteCore.lean` — Claim A façade
- `formal/BTCalculus/RewriteAddBoundary.lean` — restricted Claim B
  (`BTC-add-not-D-local`, `BTC-constructor-sum-class`,
  `BTC-push-in-S-peak`, `BTC-add-requires-carry-state`)
- `formal/BTCalculus/WordSimp.lean`,
  `formal/BTCalculus/WordSimpNewman.lean` — `BTC-word-simp-nf`

The English “any finite exact Add-tree TRS is a CAS” remains human
(`BTC-add-affine-only`, `BTC-add-factor-cas-obstruction`,
`BTC-unary-s-distrib-obstruction`). `WORD_WN` / `WORD_WND` Newman
certificates stay human. Do not edit `formal/BTCalculus/Confluence.lean`.

Phase-0 Lean packaging of `BTC-add-affine-only` (2026-08-25): wrapping
`RewriteAddBoundary` only restates restricted Claim B. The unrestricted
maximality quantification is not a short sorry-free proof (no AC engine).
It remains deferred and outside the paper; the tag stays
**EXACT — HUMAN PROOF**. No stub module.

## Results

- Enlarged OpFrag TRS is a complete canonical form (**EXACT — LEAN VERIFIED**).
- The next-state output `D(x+y)` is not D-local; constructor-sum
  identities are the six parameterized rows; the named carry-free
  push-in system fails local confluence (**EXACT — LEAN VERIFIED**).
- The unrestricted “any Add-tree TRS is a CAS” wording remains human
  (**EXACT — HUMAN PROOF**).
- Production word table is not locally confluent; `WORD_SIMP` has a
  unique syntactic NF (**EXACT — LEAN VERIFIED**); `WORD_WN` /
  `WORD_WND` stay human; the full table and SIMP+`N∘D` are **REFUTED**.
- Word-table enlargement beyond `WORD_WND_RULES` is closed.

## Open questions

Nothing on the enlargement programme. Lean packaging of
`BTC-add-affine-only` remains deferred: maximality over every finite
exact Add-tree TRS is not a short theorem without generic TRS / AC machinery.
The restricted maximality gate remains closed. External mathematical
review of the publication draft is the next stage.

## Decision

`PROMOTE`.

CMR97 refutes the broad novelty framing: this project did not originate
balanced-ternary digit append or convergent arithmetic rewriting.
Avižienis, Heuberger--Prodinger, and Frougny and coauthors likewise
establish signed-digit carry, automata, and parallel locality as
background. The revised paper survives only as an operator-oriented,
formally verified treatment of the exact open unary grammar, together
with semantic injectivity and the `add_not_DLocal` state-factorization
theorem. The named peak and constructor classification remain
supporting results. Universal Add-tree maximality, word-table
enlargement, and Paper B's research engine remain outside the paper.

Best next question: does external review accept the theorem-scope
distinction between CMR97's arithmetic TRS and the open unary semantic
canonicality theorem?

## Publication assessment

Status: `PAPER_CANDIDATE — PRIOR-ART CORRECTED`.

The coherent paper has two principal results: the unary fragment
`{D,I_a,S,N}` has a canonical tree theory, and the next-state output
`D(x+y)` does not factor through `(D(x),D(y))`. The central Lean theorem
is `add_not_DLocal`; `add_requires_carry_state` is only a packaged
corollary. CMR97 is the central arithmetic-rewriting antecedent, and
\(I_a\) is explicitly identified with its digit append. Universal
maximality is declined. Further implementation should stop. The
sendable unit is the
[reviewer packet](../theory/rewrite_calculus_reviewer_packet.md) plus
the draft and [prior-art audit](../theory/rewrite_calculus_prior_art.md).
The next step is mathematical/editorial review, not more rules.
