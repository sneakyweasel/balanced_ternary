# Juggler finite-dynamics formalization map

This page is the Lean companion to the math note
[juggler_finite_dynamics_note.md](juggler_finite_dynamics_note.md).
The note is written to be readable without this page. The development is
in `formal/Problems/Juggler/`; it contains no `sorry` or `admit`.
The review object for the math note is the paper barrel
`formal/Problems/JugglerPaper.lean` (`lake build Problems.JugglerPaper`).
That file imports only the modules named below. Laboratory satellites
remain in `formal/Problems/Juggler.lean` and are not the review object.

The package formalizes finite trajectories and conditional cycle structure.
It does not prove that every positive integer reaches \(1\), that every orbit
has a contracting prefix, or that nontrivial cycles are impossible.

The paper-central one-way import graph is drawn in
[figures/juggler_lean_layers.png](figures/juggler_lean_layers.png)
from source [figures/juggler_lean_layers.mmd](figures/juggler_lean_layers.mmd).
Satellite modules omitted from that figure remain in
`formal/Problems/Juggler.lean`.

## 1. Map and iteration

Source: `formal/Problems/Juggler/Dynamics.lean`.

`floorPower` is the integer map
\[
J(n)=
\begin{cases}
\lfloor\sqrt n\rfloor,&n\equiv0\pmod2,\\
\lfloor n^{3/2}\rfloor=\operatorname{isqrt}(n^3),&n\equiv1\pmod2.
\end{cases}
\]

The even and odd branches are implemented by exact natural-number square-root
operations. Positivity, parity-specific bounds, and monotonicity are proved
without floating-point arithmetic.

Iteration and the reachability predicate `ReachesOne` are developed in
`Iteration.lean` and `Termination.lean`. The finite lemmas there are not a
universal termination theorem.

## 2. Itineraries

Source: `formal/Problems/Juggler/Itinerary.lean`.

```text
inductive Branch where | even | odd
bit     : Nat -> Branch
word    : Nat -> Nat -> List Branch
follows : Nat -> List Branch -> Prop
image   : Nat -> List Branch -> Nat
```

The central semantic bridge is

```text
follows_iff_word (n) :
  follows n w ↔ word n w.length = w
```

The endpoint has the intended iterative semantics:

```text
image_eq_iterate (n) :
  image n w = floorPower^[w.length] n
```

Concatenation is exact:

```text
image_append
follows_append
follows_of_append_left
follows_of_append_right
```

In particular, a realized word decomposes into a realized prefix and a
realized suffix from the prefix endpoint.

The fixed-word image is monotone on its realizing set:

```text
image_monotone_of_follows :
  follows n w -> follows m w -> n <= m -> image n w <= image m w
```

This theorem does not say that two different words share a common monotone
extension or that a realizing set is an interval.

## 3. Word statistics and languages

Sources:

- `formal/Problems/Juggler/WordStats.lean`;
- `formal/Problems/Juggler/WordLanguage.lean`;
- `formal/Problems/Juggler/ExpandingGrammar.lean`.

`oddCount w` counts odd letters. The exponent comparison is represented by
\[
3^{\#O(w)}\quad\hbox{versus}\quad2^{|w|}.
\]

The formal languages are existential:

```text
jugglerLanguage w             := ∃ n, follows n w
expandingLanguage w           := ∃ n, follows n w ∧ n < image n w
persistentExpandingLanguage w := ∃ n, follows n w ∧
  PersistentExpandingResidual n (image n w)
```

The realizable language is factor-closed (`jugglerLanguage_factor`), while the
existential expanding language is not
(`expandingLanguage_not_factor_closed`). These predicates must not be replaced
by the syntactic exponent comparison.

## 4. Power envelope and contraction

Source: `formal/Problems/Juggler/Envelope.lean`.

For every realized finite word,
\[
J^{|w|}(n)^{2^{|w|}}\le n^{3^{\#O(w)}}.
\]

Lean:

```text
power_bound_word (hw : follows n w) :
  (floorPower^[w.length] n) ^ (2 ^ w.length) <=
    n ^ (3 ^ oddCount w)
```

The strict contraction corollary is:

```text
power_bound_contracts
  (hn : 2 <= n)
  (hw : follows n w)
  (hgap : 3 ^ oddCount w < 2 ^ w.length) :
  floorPower^[w.length] n < n
```

Thus the exponent gap is sufficient for contraction along a realized word.
No theorem states that every trajectory realizes such a word.

## 5. Exact defects

Sources:

- `formal/Problems/Juggler/Defect.lean`;
- `formal/Problems/Juggler/GlobalDefect.lean`;
- `formal/Problems/Juggler/DefectLowerBound.lean`;
- `formal/Problems/Juggler/NormalizedDefect.lean`.

Local floor loss is represented by branch defects. The branch identity is
the exact equality
\[
x^e=J(x)^2+\rho,
\]
where \(e=1\) on an even step and \(e=3\) on an odd step.

The recursively lifted global defect satisfies:

```text
global_defect_identity (hw : follows n w) :
  n ^ (3 ^ oddCount w) =
    image n w ^ (2 ^ w.length) + globalDefect n w

global_defect_eq_zero_iff_localsTight (hw : follows n w) :
  globalDefect n w = 0 ↔ localsTight n w

global_defect_append (hu : follows n u) (hv : follows (image n u) v) :
  globalDefect n (u ++ v) =
    powGap (image n u ^ (2 ^ u.length)) (globalDefect n u)
      (3 ^ oddCount v) +
    powGap (image (image n u) v ^ (2 ^ v.length))
      (globalDefect (image n u) v) (2 ^ u.length)
```

This is the weighted lift of local remainders, not an additive path sum.
Zero defect recovers local tightness and the rigid monochrome towers. The
normalized-defect and lower-bound modules provide exact consequences of this
identity. They do not turn the defect into a state-independent contraction
budget. The math note now states the identity, vanishing, and composition
as Theorems 2.4--2.6.

## 6. Residual steps and finite progress

Sources:

- `formal/Problems/Juggler/Residuals.lean`;
- `formal/Problems/Juggler/Progress.lean`;
- `formal/Problems/Juggler/Minimal.lean`;
- `formal/Problems/Juggler/FirstPassage.lean`.

`ResidualStep x y` records a realized block \(O^aE^b\), with \(b\ge1\),
whose endpoint is \(y\). `ResidualChain`, `ReturnBelow`,
`PersistentOddResidual`, and `PersistentExpandingResidual` package finite
first-return structure.

Representative exact results include:

```text
odd_even_residual_trichotomy
minimal_first_even_dichotomy
residualStep_global_defect
two_block_ooe_365
```

The last theorem certifies the persistent expanding chain
\[
365\xrightarrow{OOE}763\xrightarrow{OOE}1749.
\]

`FiniteProgress`, `MinimalNonTerm`, and the coefficient-stop statements
separate a sufficient finite descent certificate from the unproved universal
claim. In particular, `MinimalImpliesCoeffStop` is a proposition, not a proved
theorem.

The exact induction boundary is:

```text
reachesOne_of_all_finiteProgress :
  (∀ n, 1 < n -> FiniteProgress n) ->
  ∀ n, 1 <= n -> ReachesOne n

even_finiteProgress :
  2 <= n -> n % 2 = 0 -> FiniteProgress n

odd_even_finiteProgress :
  2 <= n -> n % 2 = 1 -> floorPower n % 2 = 0 ->
  FiniteProgress n

unresolved_is_odd_odd :
  2 <= n -> ¬FiniteProgress n ->
  n % 2 = 1 ∧ floorPower n % 2 = 1
```

Thus even and odd-to-even starts have automatic finite progress. The note's
density-\(3/4\) corollary counts that uniform short-certificate class. It
is not a Lean cardinality theorem, not a density of all `FiniteProgress`,
and not a `ReachesOne` density. Odd-to-odd starts may still descend after
a longer word. The Terras analogue on that class remains open.

## 7. Exact inverse cells

Sources:

- `formal/Problems/Juggler/Cells.lean`;
- `formal/Problems/Juggler/PreimageCylinders.lean`.

The one-step fibers are:
\[
J(n)=q\iff q^2\le n<(q+1)^2
\quad(n\ {\rm even}),
\]
and
\[
J(n)=m\iff m^2\le n^3<(m+1)^2
\quad(n\ {\rm odd}).
\]

Lean names:

```text
even_cell_iff
odd_cell_iff
odd_cell_unique
```

`odd_cell_unique` proves that an odd inverse cell contains at most one integer.
Even cells can contain many even predecessors. This is the exact inverse-cell
asymmetry used in the paper.

`squareCylinder` and `wordCylinder` iterate the cell semantics. The theorem

```text
ooe_cylinder_both_next_parities
```

certifies two `OOE` cylinders, at starts \(3461\) and \(3803\), whose next
landings have opposite parity. It is a counterexample to treating the tested
cylinder data as a complete next-parity state.

## 8. Cycles

Sources:

- `formal/Problems/Juggler/Residuals.lean`;
- `formal/Problems/Juggler/Cycles.lean`;
- `formal/Problems/Juggler/LeftoverEval.lean`;
- `formal/Problems/Juggler/LeftoverCycles.lean`.

```text
CycleWord n w :=
  follows n w ∧ image n w = n ∧ 1 <= w.length
```

Every nontrivial cycle word based at \(n\ge2\) is formally expanding:

```text
cycle_word_formally_expanding :
  2 ^ w.length < 3 ^ oddCount w
```

The formal cycle stack also includes:

```text
cycle_pow_le_lowerDenom
cycleMin_start_odd
cycleMax_start_even
cycle_peak_descent
cycle_remainder_balance
cycle_distinguished_order
```

`cycle_distinguished_order` packages the nested order and cell relations among
the cycle minimum, maximum, peak predecessor, and return landing.

Two recent boundary lemmas are:

```text
cycleMin_not_end_odd
cycleMin_prefix_ooo_even_sqrt_ne
```

They constrain a minimum-based orientation. The two leftover legal
orientations are then excluded separately:

```text
no_cycle_word_oooeoe
no_cycle_word_ooooee
```

The finite range \(n<256\) is evaluated in `LeftoverEval.lean`. The tail
\(n\ge256\) uses the last-even cell against the coarse lower envelope
`LowerPowerBound`, via the comparison \(n^{81}>2^{130}(n+1)^{64}\).
This is not a length-six census, not an exclusion of odd-terminating
cycle words, and not a halt theorem.

## 9. Evidence boundary

Lean certifies the definitions and theorem statements above. It does not
certify:

- the Word Atlas census or its GPU implementation;
- the analytic \(N^{5/6}\) discrepancy argument;
- statistical drift estimates;
- the empirical failure of every tested quotient;
- universal Juggler termination.

Those claims have separate evidence labels and reproducibility records in the
paper and its [reviewer packet](juggler_finite_dynamics_reviewer_packet.md).
