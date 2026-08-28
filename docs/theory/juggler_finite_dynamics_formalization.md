# Juggler finite-dynamics formalization map

This page is the formal companion to
[the finite-dynamics paper](juggler_finite_dynamics_note.md). It identifies
the Lean objects used by the paper and records their exact scope. The
development is in `formal/Problems/Juggler/`; it contains no `sorry` or
`admit`.

The package formalizes finite trajectories and conditional cycle structure.
It does not prove that every positive integer reaches \(1\), that every orbit
has a contracting prefix, or that nontrivial cycles are impossible.

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
```

This refines the power envelope by naming all accumulated floor slack. The
normalized-defect and lower-bound modules provide exact consequences of this
identity. They do not turn the defect into a state-independent contraction
budget.

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

Thus even and odd-to-even starts have automatic finite progress. The universal
premise remains open precisely beyond that automatic coverage; the theorem
does not assert that every odd-to-odd start eventually descends.

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
- `formal/Problems/Juggler/Cycles.lean`.

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

They constrain a minimum-based orientation but do not eliminate the remaining
`OOOEOE` or `OOOOEE` cases, all length-six words, or all cycles.

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
