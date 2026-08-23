# Rewrite-calculus reviewer packet

Send this page and the
[publication draft](rewrite_calculus_note.md).
Do not send the whole laboratory.

**Review question.** Is there a gap in the hypotheses or interpretation
of the restricted carry-state theorem `add_requires_carry_state`?

## What to read

| File | Role |
|------|------|
| [rewrite_calculus_note.md](rewrite_calculus_note.md) | the paper |
| this page | claim map |
| [rewrite_calculus_formalization.md](rewrite_calculus_formalization.md) | Lean targets, if needed |

Lean façades, if a proof is in doubt:
`formal/BTCalculus/RewriteCore.lean` and
`formal/BTCalculus/RewriteAddBoundary.lean`.

Do not review word-table fragments, coefficient-word confluence,
cubic residuals, or Collatz. Those are other objects.

## The theorem that is on offer

Exact integer addition is not \(D\)-local. Every exact identity
\(U(x)+V(y)=W(x+y)\) on \(\{S,I_+,I_-,N\}\) is one of six parameterized
rows. The named carry-free push-in extension
\(S(x+y)\to S(x)+S(y)\) fails local confluence at \(D\circ S\).
Therefore a complete exact treatment of `Add` needs carry state (or a
coefficient word / constant), which is a strict extension of the unary
tree calculus on \(\{D,I_a,S,N\}\).

This is a theorem about one concrete operator language. It is not an
impossibility theorem for arbitrary rewrite systems or for addition
itself.

## Claim map

Two axes. Do not collapse them.

| Claim | Evidence | Novelty | Lean name / ledger |
|-------|----------|---------|--------------------|
| Unique balanced-ternary expansion | classical | `KNOWN` | not claimed here |
| Newman / Knuth–Bendix | classical method | `KNOWN` | used, not contributed |
| Avizienis signed-digit addition | classical arithmetic | `KNOWN` | not a TRS theorem |
| AC completion | classical method | `KNOWN` | not used in Lean |
| Unary \(\{D,I_a,S,N\}\) is a complete canonical form | **EXACT — LEAN VERIFIED** | `PROJECT-SPECIFIC` (method `KNOWN`) | `unary_complete_canonical_form`; `BTC-op-fragment-nd-nf`, `BTC-op-fragment-nd-semantic` |
| Add is not \(D\)-local | **EXACT — LEAN VERIFIED** | `PROJECT-SPECIFIC` | `add_not_DLocal`; `BTC-add-not-D-local` |
| Constructor-sum identities are the six rows | **EXACT — LEAN VERIFIED** | `PROJECT-SPECIFIC` | `exactTriple_characterization`; `BTC-constructor-sum-class` |
| Named carry-free push-in fails at \(D\circ S\) | **EXACT — LEAN VERIFIED** | `PROJECT-SPECIFIC` | `pushIn_not_locally_confluent`; `BTC-push-in-S-peak` |
| Restricted carry-state conjunction | **EXACT — LEAN VERIFIED** | `PROJECT-SPECIFIC` | `add_requires_carry_state`; `BTC-add-requires-carry-state` |
| Every finite exact Add-tree TRS is already a CAS | **EXACT — HUMAN PROOF** | `PROJECT-SPECIFIC` | `BTC-add-affine-only`, `BTC-add-factor-cas-obstruction`, `BTC-unary-s-distrib-obstruction` |

The last row is the only central claim that is **not** Lean. “CAS” is
not a formal predicate. Do not treat that English sentence as a Lean
theorem.

## What the Lean theorem actually says

```text
¬ DLocal (fun x y => x + y)
∧ (∀ W, ¬ exactTriple Ip Ip W)
∧ (∀ W, ¬ exactTriple Im Im W)
∧ PushInStep pushInPeak (Add X Y)
∧ PushInStep pushInPeak (D (Add (S X) (S Y)))
∧ irreducible (Add X Y)
∧ irreducible (D (Add (S X) (S Y)))
```

Hypotheses fixed in Lean: exact maps on \(\mathbb Z\); \(D\)-locality
as existence of \(G\) with \(D(F(x,y))=G(D(x),D(y))\); affine
constructors \(\{S,I_+,I_-,N\}\); one named push-in relation on
`AddTree`. No quantification over arbitrary TRS engines.

## Minimal witnesses

| Statement | Witness |
|-----------|---------|
| Add is not \(D\)-local | \(D(0)=D(1)=0\), but \(D(0+0)=0\) and \(D(1+1)=1\) |
| \(D(x+y)=D(x)+D(y)\) is false | \(D(1+1)=1\neq 0\) |
| Same-sign \(I_+\) is not a constructor identity | \(I_+(x)+I_+(y)=3(x+y)+2\); residue \(2\) is not a trit |
| Named push-in peak | \(D(S(X+Y))\to X+Y\) and \(D(S(X)+S(Y))\); both irreducible, both denote \(x+y\) |

## What it does not claim

- That addition has no finite rewrite presentation. Coefficient-word
  normalization already is one, and it lives outside the unary tree TRS.
- That Avizienis-style limited-carry addition is impossible. That is
  an arithmetic algorithm, not this operator calculus.
- That the production word table is confluent. It is not; that
  appendix is closed.
- That the laboratory frontier has moved off cubic residuals.

## Suggested falsifiers

A review kills the package if any of the following holds.

1. Prior work already proves the same maximality / non-\(D\)-locality /
   six-row classification for this operator algebra, not merely unique
   expansion plus Newman or signed-digit addition.
2. \(D\)-locality as defined is the wrong locality, so the carry-state
   interpretation does not follow.
3. The constructor class \(\{S,I_+,I_-,N\}\) omits an exact identity
   that should have been included.
4. The named push-in system is not the natural carry-free extension,
   or the peak joins under the stated rules.
5. The note presents the human “any Add-tree TRS is a CAS” sentence as
   Lean-proved.

Items 2–4 are the intended mathematical review. Item 1 is the novelty
audit. Item 5 is an editorial / claim-tag check.

## Build, if wanted

```text
cd formal
lake build BTCalculus
```

From the repository root:
```text
python -m pytest tests/unit/test_operator_fragment_nf.py tests/unit/test_rewrite_add_boundary.py -q
```
