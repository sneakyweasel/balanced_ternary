# Juggler cumulative floor loss

Status: **EXPLORATORY**

Standalone application phase on the Juggler floor-power map. It is
**not** a Research Engine control-layer experiment, not a local-defect
reopen, not a modulus search, not a two-sided corridor, not p-adic
machinery, not Paper A, and not a claim that every positive integer
reaches 1.

Parity-balance, corridor, cube-boundary, odd-chain, and odd/even-reset
attacks closed after replacing \(T(x)=\lfloor x^{3/2}\rfloor\) by
inequalities such as \(T(x)^2\le x^3\). This phase asks whether the
forgotten integer floor loss accumulates into a survival-margin
obstruction.

## Problem

Can the exact floor remainders of a long `AboveAnchor` escape remain
simultaneously compatible with all preceding and following floor
equations strongly enough to force `FiniteProgress`?

## Exact statement

Write \(\delta_O(x)=x^3-T(x)^2\) and \(\delta_E(x)=x-T(x)^2\), both
in \(\{0,\ldots,2T(x)\}\). For an odd run of length \(r\) set

\[
\Delta_r=x_0^{3^r}-x_r^{2^r}.
\]

The candidate product

\[
\frac{x_r^{2^r}}{x_0^{3^r}}
=
\prod_{i=0}^{r-1}
\Bigl(1-\frac{\delta_i}{x_i^3}\Bigr)^{2^{r-1-i}}
\]

is tested against the existing identity
\(n^{3^{\#O}}=T_w(n)^{2^{|w|}}+\Delta_w(n)\). Mechanism A is
\(\Delta_r\) exceeding the formal surplus
\(n^{3^r}-n^{2^r}\). Mechanism B is the same deficit making the
first even reset stricter than generic `OE`.

Named first runs: \(37,69,89,365,501,1517,6187\). Long laboratories:
\(241,329\), and \(33391\to 67709\). This is not a halt theorem.

## Current literature

- Local remainders \(\delta_E,\delta_O\) in \([0,2T+1)\) —
  **EXACT — LEAN VERIFIED** (`localDefectEven`, `localDefectOdd`)
- \(\Delta_w=n^{3^o}-T_w^{2^k}\) with exact composition —
  **EXACT — LEAN VERIFIED** (`J-global-defect-identity`)
- Multiplicative slack \(1+q\) and concatenation —
  **EXACT — LEAN VERIFIED** (`onePlusSlack_concat`)
- \(R=\Delta/S\le 1\) iff \(T_w(n)\ge n\) when \(S>0\) —
  **EXACT — LEAN VERIFIED** (`defectRatio_le_one_iff_image_ge`);
  already flagged as endpoint reparameterization in
  `juggler_normalized_defect.md`
- First-defect Amplify, cubic lift factor \(3\) —
  **EXACT — LEAN VERIFIED**; beating surplus is \(T<n\) —
  **REFUTED** (`juggler_defect_lower_bound.md`,
  `juggler_amplify_surplus.md`)
- Sequential \(x^9-z^4\) is `globalDefect(OO)` —
  **EXACT — LEAN VERIFIED** (`sequentialDefect`)
- Prefix retention \(F_k\ge n^{2^k-3^O}\) is \(x_k\ge n\) —
  **REPARAMETERIZATION** (`J-prefix-retention-budget`)
- Whole-odd-chain compression —
  **CLOSE** (`juggler_odd_chain_minimality.md`)
- Reset \(\Psi=x_r^3-s^4\) is generic `OE` —
  **CLOSE** (`juggler_odd_even_reset.md`)
- Mixed-word local strictness \(T(n)^2<n^3\) —
  **REFUTED** at \(n=9\)
- OEIS A007320 (`oeis-A007320`): step counts to 1. **known**.
  Totality is not claimed

Project relationship: **reparameterized**. The discarded-floor
question after the reset close.

## Branch budget

```text
Mathematical target     does forgotten floor loss accumulate
                        past the AboveAnchor survival margin?
Novelty hypothesis      amplified Delta exceeds slack
                        independently of T<n, or the reset
                        becomes non-generic
Falsifier A             Delta_r is globalDefect
Falsifier B             the proposed rho-product is false
Falsifier C             R>1 is T<n
Falsifier D             first defects can vanish
Falsifier E             long admissible runs keep small eps
Falsifier F             reset is already generic OE
Existing machinery      localDefect; globalDefect; 1+q;
                        amplifyDefect; sequentialDefect;
                        defectRatio_le_one_iff_image_ge
Maximum Phase-0 scope   named first runs; odd squares;
                        329/67709 local eps; no Lean;
                        no p-adic; no analytic NT
Promotion criterion     a deficit that is not T<n and not
                        EnvelopeState, with a FiniteProgress
                        bridge
Stop criterion          Falsifier A–F; machinery gravity;
                        FloorLoss Lean without a new law
```

## Balanced-ternary formulation

None required. The map is on ordinary positive integers.

## Why BT may be relevant

It is not required.

## Candidate operations / invariants

- \(\delta_O,\delta_E\) —
  **KNOWN** (`localDefectOdd`, `localDefectEven`)
- \(\Delta_r=x_0^{3^r}-x_r^{2^r}\) —
  **KNOWN** (`globalDefect` on \(O^r\))
- proposed weighted \(\rho\)-product —
  **REFUTED** for \(r\ge 2\) unless earlier odd steps are tight;
  it omits the cubic lift of running slack
- correct multiplicative form \((1+q)\mapsto(1+q)^3(1+\eta)^{2^k}\) —
  **EXACT — LEAN VERIFIED**
- \(D_2>d_0+d_1\) —
  **OBSERVATION**; the cubic lift is already `accumulateOdd`
- \(R>1\) as an independent obstruction —
  **REPARAMETERIZATION** of \(T_w(n)<n\)
- \(\delta_0=0\) on odd squares —
  **OBSERVATION** (\(9,25,49,\ldots\)); \(37\) also hits the
  odd square \(225\)
- Mechanism B (reset) —
  **REPARAMETERIZATION** of generic `OE` (`juggler_odd_even_reset.md`)
- global halt — not claimed

## Experiments

- Probe: `research.juggler_sequence.cumulative_floor_loss`
- Records: [juggler_cumulative_floor_loss.md](../research/juggler_cumulative_floor_loss.md),
  [juggler_cumulative_floor_loss.json](../research/juggler_cumulative_floor_loss.json)
- Tests: `tests/research/juggler_sequence/test_cumulative_floor_loss.py`

No CLI. No Lean. No \(p\)-adic. No huge-power \(\Delta\) on
\(329\).

## Conjectures

None opened.

## Counterexamples

“The weighted \(\rho\)-product is the exact odd-run identity” is
false. For every named start with \(r\ge 2\) it fails. It holds
for a single odd step, and for longer runs only if every earlier
odd step is tight. The missing term is the cubic lift of the
running slack, already `accumulateOdd`.

“A first nonzero defect is forced” is false. Every odd square has
\(\delta_O=0\). On \(37\) the second odd state is the odd square
\(225\).

“Amplified \(\Delta\) exceeds the survival surplus on an
`AboveAnchor` odd run” is false. On every measurable named first
run \(R\le 1\) with image \(\ge n\). That comparison is
`defectRatio_le_one_iff_image_ge`.

“Long odd runs cannot keep small normalized loss” is false.
\(329\) has an \(8\)-step run with \(\varepsilon\) down to
\(0.025\) and still lands above the start.

## Formalization

None added. The catalog is already in `Defect`, `GlobalDefect`,
`NormalizedDefect`, `DefectLowerBound`, and `SequentialMordell`.
No `FloorLoss.lean`. No `CumulativeLoss.lean`. Paper A is
unchanged. No `sorry`.

## Results

Classification **CUMULATIVE_FLOOR_LOSS_CLOSED**.

The discarded floor information is already assembled:

\[
n^{3^{\#O}}=T_w(n)^{2^{|w|}}+\Delta_w(n),
\]

with \(\Delta_w=\) `globalDefect`. Envelope nonnegativity is
\(\Delta\ge 0\). Early remainders are amplified by
\(\rho_i^{2^i}\le\Delta\) and by the cubic lift. The dimensionless
form is \(1+q\), not the proposed \(\rho\)-product.

Mechanism A is the endpoint test \(R>1\Leftrightarrow T<n\). It
does not fire on any named `AboveAnchor` first run. Leftover first
runs are `OO` then even (`OOE`); their \(D_2\) is
`sequentialDefect` / `globalDefect(OO)` and is larger than
\(d_0+d_1\), as the cubic lift requires, without beating the
surplus.

Mechanism B does not reopen: the first even reset is generic `OE`
(`juggler_odd_even_reset.md`). The episode source does not tighten
\((\delta,\varepsilon)\).

This is Falsifier A–F.

## Open questions

None from cumulative floor loss. Do not add `FloorLoss`. Do not
take logarithms of \(\Lambda_r\). Do not start an analytic
approximation branch. The leftover hole is unchanged: a cube cell
without a square cell.

## Decision

**CLOSE**. The forgotten floor is not forgotten: it is
`globalDefect`. The proposed product identity is false. The
budget comparison \(\Lambda_r\) versus survival margin is
\(T_w(n)\ge n\). Vanishing and near-vanishing remainders exist.
The reset adds nothing beyond generic `OE`. A branch whose
statements are all `KNOWN` or `REPARAMETERIZATION` is a close.

Best next question: none from cumulative floor loss.

## Publication assessment

Status: `EXPLORATORY`.

A negative identification of a proposed identity with the existing
defect spine. Not a paper candidate and not a Juggler totality
result.
