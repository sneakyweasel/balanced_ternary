# Generalized Ostrowski order-(m) adder

Status: **EXPLORATORY**

What residual/carry state is required to recognize addition in
Baranwal’s order-\(m\) \(\Gamma\)-numeration system? The quadratic
Ostrowski adder is already in the literature. This branch does not
rebuild it.

## Problem

Construct, or obstruct, a finite-state recognizer of
\(\operatorname{Add}_\Gamma(x,y,z)\) for a genuine order-\(m>2\)
system in the sense of Baranwal’s thesis §5.3, and identify the
minimal carry residual that makes the recognizer work.

## Exact statement

Let \(\Gamma=(\alpha_1,\ldots,\alpha_m)\) with
\(\alpha_k=[0;d_{k,1},d_{k,2},\ldots]\). Place values (Baranwal 2020,
§5.3):

\[
q_i=
\begin{cases}
0 & i<0,\\
1 & i=0,\\
\sum_{k=1}^{m}d_{k,i}\,q_{i-k} & i>0.
\end{cases}
\qquad
N=[a_{n-1}\cdots a_0]_\Gamma=\sum_{0\le i<n}a_i q_i.
\]

Proposed canonicality, transcribed from the thesis (pp. 49–50), not
invented here:

1. \(a_0<d_{1,1}\);
2. \(0\le a_i\le d_{1,i+1}\) for \(i\ge 1\);
3. for all \(i\ge 1\), if \(a_i=d_{1,i+1}\) then there exists
   \(k\le m\) such that \(a_{i-k}<d_{k,i+1}\).

Missing digits with negative index are read as \(0\). These three
rules are proposed, not proved unique or complete.

Addition:

\[
\operatorname{Add}_\Gamma(x,y,z)
\iff
\operatorname{val}_\Gamma(x)+\operatorname{val}_\Gamma(y)
=\operatorname{val}_\Gamma(z).
\]

The machine reads \((x_i,y_i,z_i)\) in parallel. Thesis Theorem 2.2
is MSD-first with unread-tail residual. LSD-first is tested only
after a finite MSD box exists.

Phase-0 case:

\[
\Gamma=\bigl([0;\overline{2}],[0;\overline{1}],[0;\overline{1}]\bigr),
\qquad
q_i=2q_{i-1}+q_{i-2}+q_{i-3}.
\]

The characteristic polynomial \(x^3-2x^2-x-1\) is irreducible over
\(\mathbb Q\), so this is not a disguised Ostrowski system. The
dominant root is Pisot, so existence of *some* adder is `KNOWN` by
Frougny–Solomyak. That is not the target.

The target: does the unread-tail residual live in a finite
\(m\)-dimensional box, giving an explicit analog of Theorem 2.2?

## Current literature

- `hieronymi-terry-2018-ostrowski-addition`: addition in Ostrowski-\(\alpha\)
  is finite-automaton recognizable when \(\alpha\) is quadratic.
  `KNOWN`.
- `baranwal-2020-ostrowski-thesis`,
  `baranwal-schaeffer-shallit-2021-ostrowski-automatic`: explicit
  4-input DFA with states \((r,s)\in\{-1,0,1\}^2\), seven states after
  pruning; Walnut 3-input compilation for quadratic \(\alpha\).
  Theorem 2.2 / TCS Theorem 4. `KNOWN`. The \(m\)-dimensional state
  is proposed in thesis §5.3, p. 50, not constructed.
- `shallit-1994-numeration-regular`: a finite-alphabet language of
  representations of \(\mathbb N\) is regular only under a linear
  recurrence / periodic continued-fraction hypothesis. A 3-input
  finite-alphabet adder for one fixed non-quadratic \(\alpha\) is
  already impossible. `KNOWN` (negative).
- `frougny-solomyak-1996-linear-numeration`: constant-coefficient
  Pisot linear systems have finite-state normalization, hence
  addition. Different hypothesis (constant coefficients, Pisot root),
  not a solution of §5.3. `KNOWN` under that hypothesis.
- `hieronymi-et-al-2024-sturmian-decidability`: uniform
  \(\omega\)-automatic / Büchi use of the BSS *order-2* 4-input
  adder. `KNOWN`. Does not treat \(m>2\).
- Tribonacci / Narayana Walnut adders: Pisot / Dumont–Thomas,
  not Baranwal \(\Gamma\)-systems (Narayana has a zero coefficient).
  `KNOWN` / not this definition.
- Multidimensional continued fractions (Jacobi–Perron, Brun): not
  identified with §5.3 in the citing literature. Not used here.

Classification used in this dossier:

```text
order-2 / quadratic adder              KNOWN
m-dimensional carry idea               KNOWN as a suggestion; OPEN as a theorem
general order-m adder existence        OPEN for Baranwal Gamma-systems
Pisot linear adders                    KNOWN (different hypothesis)
minimal Box / |Q|                      OPEN
3-input adder, one non-quadratic α     KNOWN negative
uniform encoded adder, arbitrary α     KNOWN (order 2 only)
```

No 2022–2026 paper found that constructs the §5.3 adder, proves a
general existence theorem for it, or gives a state-dimension lower
bound. The TCS 858 open-problems page was not retrieved; the quote
is from the thesis, which supplied Chapters 2 and 5 of that paper.

## Branch budget

```text
Mathematical target     For Baranwal’s genuine order-3 Γ-system, does the unread-tail residual live in a finite m-dimensional box, giving an explicit analog of thesis Theorem 2.2?
Novelty hypothesis      The m-dimensional carry construction was only proposed. An explicit finite box, a sharp unbounded-carry obstruction, or a necessary/sufficient condition would be new. Existence of some adder for Pisot linear systems is not new.
Falsifier               (A) a 2022–2026 paper already gives the construction; (B) the example is disguised order-2; (C) residuals unbounded with no useful condition; (D) the only theorem is Frougny–Solomyak under another name; (E) |Q| is an implementation artifact.
Existing machinery      BT carry-boundary (add_not_DLocal, D_add) for comparison only; distinguish / Myhill–Nerode; research template. No Ostrowski/Fibonacci/numeration-adder code existed.
Maximum Phase-0 scope   Dossier + literature IDs + faithful §5.3 objects + symbolic residual recurrence + order-2 regression + one order-3 Γ + finite-box search + bounded exhaustive verification. No CLI, Walnut, Lean, order 4, or general numeration framework.
Promotion criterion     A genuine order-3 carry invariant with finite closure not already in the literature, or a new finite-state condition, or a precise obstruction that is not a Pisot reparameterization.
Stop criterion          The construction is already published; the example is not genuine order-3; residuals grow with no interesting condition; or every statement is KNOWN/REPARAMETERIZATION.
```

## Balanced-ternary formulation

This is not a balanced-ternary numeration system. Digits are
nonnegative and constrained by \(\Gamma\). The comparison with BT is
only the carry-boundary principle: digit-local arithmetic stops when
addition needs extra residual state.

## Why BT may be relevant

The rewrite-calculus theorem `add_not_DLocal` isolates the LSD carry
as the missing state for \(D(x+y)\). The Ostrowski question is
whether a higher-dimensional unread-tail residual plays the same
role. The systems are not identified.

## Candidate operations / invariants

- Place-value recurrence of §5.3 — **KNOWN** (definition).
- Proposed three-rule canonicality — **REFUTED** as a unique complete
  system: complete on \([0,q_L)\) for the Phase-0 \(\Gamma\) at
  \(L\le 7\), not injective from \(L=3\). The same rules also fail to
  recover Zeckendorf uniqueness.
- Unread-tail residual
  \(E_i=\sum_{j<i}w_j q_j=\sum_{k=1}^{m}s_k q_{i-m+k}\) with
  \(w_j=z_j-(x_j+y_j)\) — **PROVED** as an identity of the recurrence
  (human + computational check). Analog of thesis (2.1).
- Deterministic transition
  \(t_1=s_m d_{m,i}\),
  \(t_j=s_{j-1}+s_m d_{m-j+1,i}\) for \(2\le j\le m-1\),
  \(t_m=s_{m-1}+s_m d_{1,i}-w\) — **PROVED** by substitution
  (human + order-2 regression). Analog of (2.3).
- Unrestricted reachable \(s\in\mathbb Z^m\) lie in a finite box —
  **REFUTED** computationally: coordinates grow once
  \(|t_m|\) is unrestricted.
- Restricted box \(|t_m|\le 1\) is a sufficient adder — **REFUTED**
  at length \(5\) (false rejects).
- Restricted box \(|t_m|\le 2\) is a sufficient adder — **OBSERVATION**
  / `COMPUTATIONALLY VERIFIED` for \(\mathrm{val}<q_5\). Not a proof.
- Order-2 specialisation recovers Theorem 2.2 — **PROVED** in the
  source; Phase 0 regresses it.

## Experiments

No registered CLI runner. Phase-0 functions in
`research.ostrowski` and tests in
`tests/research/ostrowski/test_triage.py`.

Ranges actually run: canonicality \(L\le 7\); unrestricted addition
at Fibonacci length \(6\) and Phase-0 length \(5\); boxed addition
at length \(5\). Finite tests are `COMPUTATIONALLY VERIFIED`, not
proofs.

Recorded fields for each system:

```text
order m
parameter definition
place-value recurrence
digit constraints
canonicality
LSD/MSD direction
raw states
reachable states
minimal states
maximum carry coordinate
transition count
final-state condition
proof status
```

## Conjectures

None registered. Computational observations stay in this dossier.

## Counterexamples

Recorded in `tests/research/ostrowski/test_triage.py`.

- Proposed §5.3 rules on Fibonacci, length 7: 25 colliding values.
  Classical Ostrowski (Def. 2.1) is unique and complete on the same
  range. The order-\(m\) rules do not specialise to Ostrowski
  uniqueness.
- Phase-0 \(\Gamma\), length 3:
  \(\operatorname{val}(0,0,1)=\operatorname{val}(1,2,0)=5=q_2=2q_1+q_0\).
  The recurrence identity is a legal rewrite under rule 3.
- \(|t_m|\le 1\) boxed adder: false rejects at length \(4\) (3 pairs),
  length \(5\) (25 pairs), length \(6\) (185 pairs). The naive copy of
  Theorem 2.2’s \(\{-1,0,1\}\) last coordinate is not sufficient.

## Formalization

None. No `formal/BTCalculus/OstrowskiAdder.lean` in Phase 0. No
`sorry`.

## Results

Phase-0 system
\(\Gamma=([0;\overline{2}],[0;\overline{1}],[0;\overline{1}])\),
\(q=(1,2,5,13,33,84,214,\ldots)\). Characteristic polynomial
\(x^3-2x^2-x-1\) is irreducible over \(\mathbb Q\) (Falsifier B
fails). Dominant root is Pisot, so existence of *some* adder is
`KNOWN` (`frougny-solomyak-1996-linear-numeration`).

| field | Phase-0 record |
|---|---|
| order \(m\) | 3 |
| parameter definition | \(\Gamma=([0;\overline{2}],[0;\overline{1}],[0;\overline{1}])\) |
| place-value recurrence | \(q_i=2q_{i-1}+q_{i-2}+q_{i-3}\) |
| digit constraints | §5.3 proposed rules |
| canonicality | complete, not unique from length 3 |
| LSD/MSD direction | MSD unread-tail (LSD with the same formula fails) |
| raw boxed states | 85 at \(\lvert t_m\rvert\le 2\) |
| reachable unrestricted | grows with the coordinate cap |
| minimal live states | 64; some carry vectors merge |
| maximum carry coordinate | 4 on the \(\lvert t_m\rvert\le 2\) graph |
| transition count | boxed graph on alphabet \(\{-4,\ldots,2\}\) |
| final-state condition | \(s_m=0\) |
| proof status | recurrence exact; box `COMPUTATIONALLY VERIFIED` |

The unrestricted 3-input residual machine accepts a padded triple iff
\(\operatorname{val}(x)+\operatorname{val}(y)=\operatorname{val}(z)\),
checked exhaustively for Fibonacci Ostrowski words of length \(6\) and
for Phase-0 proposed-canonical words of length \(5\). Finite checks
are not a proof of arbitrary-length correctness of the *box*.

Minimality: raw \(85\) states, Hopcroft \(65\) parts including the
sink (\(64\) live). Minimal states are not in bijection with carry
vectors.

## Open questions

Is \(\lvert t_m\rvert\le 2\) (or another explicit \(B_\Gamma\)) closed
for every length on this \(\Gamma\)? Do not open order 4, Walnut,
Lean, or a numeration framework to answer that.

## Decision

`PARK`. The unread-tail recurrence is the analog of Theorem 2.2 and
is exact. A finite \(\lvert t_m\rvert\le 2\) table exists
computationally and matches addition below \(q_5\). That is not a
proved finite-state theorem, and existence of some adder is already
`KNOWN` by Pisot theory. The \(m\)-dimensional state was suggested
in the source. The proposed §5.3 digit rules are not a unique
numeration system. Do not `PROMOTE`. Do not `CLOSE`: the uniqueness
failure, the insufficiency of \(\lvert t_m\rvert\le 1\), and the
explicit residual recurrence are recorded and would be rediscovered.
No Phase 1, CLI, Walnut, Lean, or order-4 experiment.

Best next question: prove that the \(\lvert t_m\rvert\le 2\) residual
box is closed for this \(\Gamma\), or exhibit an accepting path that
leaves it.

## Publication assessment

Status: `EXPLORATORY`. No exact finite-state theorem. Not a
`PAPER_CANDIDATE`.
