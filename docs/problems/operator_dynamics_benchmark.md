# Operator-dynamics v2 benchmark

Status: **ARCHIVED**

First test of whether Research Engine v2 can diagnose a new integer
dynamical system from generic attacks, without a problem-specific
theory. The archived `{S,N,D,W}` identity census stays closed. This
dossier does not reopen signed-digit, Collatz, primes, jets, or
Ostrowski.

CLI `btlab research analyze operator_dynamics` (aliases
`operator_dynamics_benchmark`, `signed_p0`, `nsd`).

## Problem

Which structural regime does the existing word \(N\circ I_0\circ D\)
occupy, when the engine is not told the invariant?

## Exact statement

The preferred family

\[
F_{a,b}(n)=I_a(D(I_b(n)))
\]

collapses: \(D\circ I_b=\mathrm{id}\), so \(F_{a,b}=I_a\), i.e.
\(n\mapsto 3n+a\). That is the forbidden reduction. It is not a
benchmark target.

The smallest surviving word in \(\{D,I_{-1},I_0,I_1,N\}\) with
nontrivial iteration is

\[
F(n)=N(I_0(D(n)))=\operatorname{lsd}(n)-n=-P_0(n).
\]

Then \(F^2=P_0\), \(F^3=F\), and every orbit has size at most 3. The
reachable set from a seed is finite. The union over \(\mathbb{Z}\) is
an infinite disjoint union of those orbits. The integer box
\(|n|\le 2\) is not invariant (\(F(2)=-3\)). Sign observation merges
the two positive points on the seed orbit of \(4\).

## Current literature

- \(D\circ I_a=\mathrm{id}\) and the left-zero band \(P_a\circ P_b=P_a\)
  are `KNOWN` (ledger `BTC-D-I`, `BTC-P-band`).
- OpFrag classifies the **map** \(N(I_0(D(x)))\) as an irreducible.
  It does not classify the **iterates**.
- Near-negation \(n\mapsto c-n\) is a classical involution. The trit
  perturbation \(n\mapsto\operatorname{lsd}(n)-n\) and the orbit law
  are a `NEW FORMULATION` of the band plus \(N\).
- Expanding \(T(n)=3n-\operatorname{lsd}(n)\) is a different map.

## Branch budget

Written before substantial implementation. See
[methodology.md](../methodology.md).

```text
Mathematical target     Can v2 diagnose the structural regime of one new
                        integer map built from existing BT operators,
                        without a problem-specific theory in advance?
Novelty hypothesis      Either a new finite/observational class, or an
                        exact obstruction, or a correct CLOSE as known
                        BT algebra — the diagnosis is the result.
Falsifier               The chosen word rewrites to n, -n, 3n+a, or D(n);
                        or the engine is fed the expected invariant.
Existing machinery      ProblemSpec, AttackPlanner, CertificateKind,
                        ComplexityProfile, envelope vs reachable,
                        separate_states, Mealy quotient; D, I_a, N, P_a
                        already in bt.calculus; archived {S,N,D,W} census
                        stays closed.
Maximum Phase-0 scope   One operator word; one integer-state adapter;
                        generic planner; bounded seeds; one proof if a
                        concrete identity appears; one Lean theorem.
Promotion criterion     Exact residual/orbit/obstruction theorem with
                        certificates, not a restatement of P_a∘P_b=P_a.
Stop criterion          Rewrite collapse; machinery gravity; or
                        INCONCLUSIVE with no compact residual.
```

## Balanced-ternary formulation

\(F\) is the word `N I0 D` in mathematical order: apply \(D\), then
\(I_0=S\), then \(N\). Observation is \(\operatorname{sign}(n)\), not
LSD (which is \(0\) after one step) and not \(v_3\).

## Why BT may be relevant

The local operators are the calculus. The question is whether generic
attacks see the orbit geometry without being told \(P_0\).

## Candidate operations / invariants

- \(I_a(D(I_b(n)))=I_a(n)\). **EXACT — LEAN VERIFIED** (`D_after_I`)
- \(F^2=P_0\). **EXACT — LEAN VERIFIED**
- \(F^3=F\); every orbit has size at most 3. **EXACT — LEAN VERIFIED**
- The box \(|n|\le 2\) is invariant. **REFUTED** (\(F(2)=-3\))
- \(V(n)=n\) is a Lyapunov. **REFUTED**
- \(\mathbb{Z}\) is a single finite residual. **REFUTED** (disjoint
  orbits of \(3\) and \(6\))
- Distinct positives on the seed orbit of \(4\) are sign-equivalent.
  **EXACT** (engine `separate_states`)

## Experiments

- `btlab research analyze|attack|reproduce|report operator_dynamics`
- Discovery: `src/research/operator_dynamics/signed_p0/discovery.py`
- Tests: `tests/research/operator_dynamics/test_signed_p0.py`
- Records in `experiments/balanced_ternary/operator_dynamics/`

Planner decisions (no modulus-3 or \(P_0\) hint):

| attack | status | reason |
|--------|--------|--------|
| reconnaissance | OBSERVATION | bounded census |
| closure | SUPPORTED EXACT | seed orbit size 3, `EXACT_CLOSURE` |
| functional | OBSERVATION | sample bound, not a Lyapunov |
| affine | REFUTED | box \(\lvert n\rvert\le 2\) leaks |
| reverse | SUPPORTED EXACT | basin of \(0\) is \(\{-1,0,1\}\) |
| separation | EXACT | seed vs image distinguished by sign |
| quotient | SUPPORTED EXACT | \(M=2<\|R\|=3\) on the seed orbit |
| modular, spectral, block, factorization, symmetry | skipped | inapplicable |
| symbolic | skipped | not implemented |

## Conjectures

None opened.

## Counterexamples

- \(F_{a,b}\) collapses: \(I_1(D(I_{-1}(5)))=I_1(5)=16\).
- Interval leak: \(F(-2)=3\) and \(F(2)=-3\).
- Lyapunov: \(F(-3)=3\not< -3\).
- Global residual: orbits \(\{3,-3\}\) and \(\{6,-6\}\) are disjoint.

## Formalization

`formal/Problems/BalancedTernary/SignedP0.lean`. No `sorry`. Theorems
`signedP0_sq_eq_P0`, `signedP0_cube_eq_self`, `signedP0_orbit_finite`.

## Results

v2 takes integer state, a dummy control, and sign observation.

- Question A: per-seed residual is finite; the map on \(\mathbb{Z}\) is
  not one finite residual.
- Question B: the minimal per-seed residual is the orbit
  \(\{n,F(n),P_0(n)\}\), size at most 3.
- Question C: the interval envelope \(\lvert n\rvert\le 2\) is strictly
  larger than, and does not contain, the seed orbit of \(4\).
- Question D: sign merges \(4\sim 3\) on that orbit; \(4\not\sim -3\).
- Question E: the mechanism is \(F=-P_0\) with \(P_0\) a projection,
  not \(v_3\) rigidity and not expansion.
- Question F: `EXACT_CLOSURE` for the seed orbit and the Mealy
  quotient; `EXACT_COUNTEREXAMPLE` for the interval leak; bounded
  reconnaissance stays an observation.

Complexity profile of the seed \(4\) versus the reference systems is
structural, not a forced numeric identification:

| system | regime |
|--------|--------|
| signed-digit residual | finite residual, interval fill, no merge when \(3\nmid\lambda\) |
| D+Add | finite 3-state carry residual |
| Collatz shortcut | integer BFS cap, exact expanding block |
| prime observation | sieve finite, primality not a residual |
| \(N\circ I_0\circ D\) | infinite disjoint union of orbits of size \(\le 3\); sign quotient \(M<\|R\|\) |

Similarity to signed-digit is rejected: there is a behavioral merge,
no gain \(\lambda\), and no 3-adic separator. Similarity to Collatz is
rejected: every orbit is finite. Similarity to expanding \(T\) is
rejected: \(\lvert F(n)\rvert\not> \lvert n\rvert\) in general, and LSD
dies after one step.

## Open questions

Nothing on this line. Do not enumerate other operator words.

## Decision

`CLOSE`. The map is the known projection \(P_0\) composed with \(N\).
The orbit law is a short corollary, not a new residual class. The
benchmark succeeded: v2 diagnosed finite per-orbit closure, a leaking
envelope, and a sign quotient without being told \(P_0\).

Best next question: none on this line; do not start another operator
word.

## Publication assessment

Status: `ARCHIVED`.

The operator identities were already recorded. The v2 diagnosis is
supporting evidence that the engine classifies a new integer map, not
a literature-separated theorem.
