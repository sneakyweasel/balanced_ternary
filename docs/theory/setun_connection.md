# Setun connection

This page separates **historical fact**, **engineering motivation**, and
**our mathematical interpretation**. No theorem in `bt.calculus` is
attributed to Setun unless a cited source states that theorem.

## Historical fact

The following are standard, independently reported facts about the
Setun machines at Moscow State University. They are recorded here as
history, not as lemmas.

- Setun (operational 1958–1959) was a serial balanced-ternary computer
  designed under N. P. Brusentsov. Digits were the signed trits
  `{-1, 0, +1}`.
- Arithmetic used balanced-ternary addition, subtraction, and
  multiplication with a local carry/borrow of at most one.
- The sign of a word was visible as the leading trit. Comparison and
  some control decisions used that sign.
- Operand length was not a single fixed 32/64-bit convention in the
  later Setun-70 design: the machine worked with variable-length
  ternary words and a postfix / two-stack evaluation style for
  mathematical expressions.
- English-language secondary accounts include Knuth’s discussion of
  balanced ternary in *The Art of Computer Programming*, vol. 2, and
  Hayes, “Third Base”, *American Scientist* 89 (2001). Soviet-era
  primary papers by Brusentsov and colleagues, and Malinovsky’s
  historical survey of Soviet computing, are the sources to use for
  hardware claims. Registry ids: `hayes-2001-third-base`,
  `knuth-taocp-vol2`, `malinovsky-pioneers-soviet-computing`.

We do **not** treat later popular claims (speed advantages, “optimal
radix”, or any Collatz-related story) as theorems.

## Engineering motivation

Ideas that are visible in the design and that we chose to study
mathematically:

| Setun / Setun-70 motif | What we do **not** claim | What we formalize |
|------------------------|--------------------------|-------------------|
| Signed trit as a digit | That `{-1,0,+1}` is a Boolean algebra | Trit lattice / Kleene algebra |
| Sign trit as control | That Setun implemented `select3` | `cmp3` / `select3` |
| Variable word length | A hardware cost model | `D` / `I_a` as drop/prepend LSD |
| Postfix math expressions | Cycle-accurate emulation | Calculus stack VM |
| Combined arithmetic ops | A unique “ternary ALU law” | Exact `D` sum/product corrections |
| Threshold / ternary logic | Łukasiewicz as Setun’s logic | Separate lattice vs arithmetic |

## Our mathematical interpretation

The calculus asks whether those motifs generate a coherent algebra:

```text
integer  ↔  balanced-ternary word  ↔  trit sequence
         ↔  symbolic expression    ↔  operator system
```

Answers so far (see [balanced_ternary_calculus.md](balanced_ternary_calculus.md)):

- The trit lattice is real, small, and already known.
- `D` / `I_a` are the unique digit destructor/constructors of the
  balanced expansion. Most identities are restatements of uniqueness.
- The twisted product rule and the projection band `{P_a}` are exact
  and Lean-verified. They are calculus *language*, not new number
  theory.
- The postfix VM is an evaluator, not Setun-70.
- Coefficient-vector normalization (Milestone 14) is recorded in
  [setun_normalization.md](setun_normalization.md). ISA normalize/FMA
  details stay sketches unless a cited source is added.
- Section/jet calculus (Milestone 15) is recorded in
  [polynomial_jet_calculus.md](polynomial_jet_calculus.md). No Setun
  attribution: the 3-section operator is standard algebra; `hat D` and
  the `[2]` normalization boundary are this repository’s packaging.

If a later source is found that already states `D(xy)` in this form,
the ledger should be updated to **KNOWN** rather than presented as
new.
