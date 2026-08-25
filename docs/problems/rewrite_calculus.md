# Rewrite calculus of balanced-ternary operators

Status: **PAPER_CANDIDATE**

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
- `knuth-taocp-vol2`, `hayes-2001-third-base`: unique balanced-ternary
  expansion; `D` / `I_a` as drop / prepend LSD. `KNOWN` /
  `REPARAMETERIZATION` for Level A slogans.
- `avizienis-1961-signed-digit`: signed-digit representation and
  limited-carry addition as an *arithmetic* algorithm. `KNOWN`. It
  does not state a TRS maximality theorem for `{D, I_a, S, N}` and
  does not classify `U(x)+V(y)=W(x+y)` on those constructors.
- `peterson-stickel-1981-unification-ac`: completion modulo AC is
  already a computer-algebra engine. `KNOWN` (method). Used to tag
  the AC-matching half of the factor-out obstruction, not the trit
  carry itself.
- `malinovsky-pioneers-soviet-computing`: Setun postfix evaluation.
  Historical frame only.

Consequence of the audit: Newman-on-a-small-fragment, unique expansion,
and carry-managed signed-digit addition are not new. The surviving
`PROJECT-SPECIFIC` package is the canonical unary fragment plus the
exact non-factorization theorem for `D(x+y)`, supported by the
constructor classification and named push-in peak.

## Branch budget

```text
Mathematical target     Is the maximal unary tree core plus the Add/carry exclusion a project-specific classification theorem after comparison with signed-digit and term-rewriting literature?
Novelty hypothesis      The coherent package—complete {D,I_a,S,N} canonical form, necessity of the oriented N–D rule, and exact exclusion of Add from a finite tree TRS—is more than unique balanced-ternary representation plus routine Newman.
Falsifier               Prior literature already proves the same maximal core and Add-exclusion for signed-digit operator algebras, leaving only renamed standard facts.
Existing machinery      Lean OpFrag proofs, human obstruction proofs, coefficient-word normalization, word-fragment PRs, theorem ledger, conjecture registry, and regression tests.
Maximum Phase-0 scope   Reconcile the open word PR stack; perform a bounded literature audit; create one dossier and one theorem-package outline; add no new rewrite rules, CLI, visualization, or census.
Promotion criterion     At least two central claims remain PROJECT-SPECIFIC and form one coherent theorem package with a clear audience and proof path.
Stop criterion          All central claims are KNOWN/REPARAMETERIZATION, or usefulness depends on adding more named word fragments rather than strengthening the classification.
```

The promotion criterion fired: maximality at `D∘S` and the six-identity
Add classification remain `PROJECT-SPECIFIC` and form one package.
The stop criterion for word-table enlargement also fired: further
`N∘M2` / `N∘Wz` / `N∘Wt` fragments would be machinery gravity.

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

Nothing on the enlargement or formalization programmes. The restricted
maximality gate is closed because a short class either assumes
D-locality/no peak repair or requires generic TRS metatheory. External
mathematical review of the publication draft is the next stage.

## Decision

`PROMOTE` the paper centered on the canonical unary theorem and
`add_not_DLocal`. `CLOSE` the restricted maximality attempt: no natural
completeness-to-locality bridge exists inside the bounded gate. The
constructor classification and named peak remain Lean-verified
supporting results. The broader English “every finite exact Add-tree
TRS is already a CAS” stays an archived human claim, not a paper or
Lean theorem. Do not open another rewrite milestone or add production
rules.

`PROMOTE` the lattice side lemma, `CLOSE` the operation-classifier.
On all of \(\mathbb Z\), \(D(\max(x,y))=\max(D(x),D(y))\) and
\(D(\min(x,y))=\min(D(x),D(y))\), so \(D\circ\max\) and \(D\circ\min\)
are `DLocal`. Addition is not a unique bilinear obstruction: in the
affine box \(axy+bx+cy+d\) with coefficients in \(\{-2,\ldots,2\}\),
\(D\circ H\) is D-local only for constants and the unary maps \(\pm x\),
\(\pm y\). Prefix \(k\)-jets that include both \(\operatorname{lsd}\)
and \(D\) reconstruct the inputs, so they do not define a locality
class. Do not add this lemma to the publication draft.

Best next question: does external mathematical review find any gap in
the definition, proof, or interpretation of the exact theorem that
`D(x+y)` does not factor through `(D(x),D(y))`?
Send the [reviewer packet](../theory/rewrite_calculus_reviewer_packet.md)
with the [publication draft](../theory/rewrite_calculus_note.md).

## Publication assessment

Status: `PAPER_CANDIDATE`.

The coherent paper has two principal results: the unary fragment
`{D,I_a,S,N}` has a canonical tree theory, and the next-state output
`D(x+y)` does not factor through `(D(x),D(y))`. The central Lean theorem
is `add_not_DLocal`; `add_requires_carry_state` is only a packaged
corollary. Universal maximality is explicitly declined. Further
implementation should stop. The publication draft is **READY FOR
EXTERNAL REVIEW**. The sendable unit is the
[reviewer packet](../theory/rewrite_calculus_reviewer_packet.md) plus
the draft. The next step is mathematical/editorial review, not more
rules.
