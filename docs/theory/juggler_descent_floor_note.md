# Verified descent floor versus the Juggler period cutoff

Status: laboratory extract. Date: 31 August 2026.

This is the sensitivity analysis of Paper A Theorem 4.6: how
much period bound is purchased by raising the verified descent
floor. It is not a second manuscript, not a halt theorem, and
not a claim that a larger finite search found no cycles.

Parent: [juggler_cycle_finance_note.md](juggler_cycle_finance_note.md).
Dossier: [juggler_descent_floor.md](../problems/juggler_descent_floor.md).
Probe: `research.juggler_sequence.cycle_floor_sensitivity`.

The central logic is unchanged:

\[
\text{exact cells}
\to
\text{cycle minimum}
\to
\text{finance}
\to
n_{\max}(L)
\to
\text{verified descent floor}
\to
\text{period bound}.
\]

## Three layers (do not mix)

1. **Exact theorem.** `cycleMin_finance`:
   \(n\log n\cdot(3^o-2^L)\le L\cdot 3^o\). Lean, constant \(1\).
   The published computational table uses the conservative
   \(6/5\) unroll and the length-only parity charge
   (Theorem 4.6). Run-packing is Theorem 4.7.
2. **Numerical optimization.** The padded Python comparisons
   `parity_excludes` / `budget_excludes` already used to
   certify the published leftover lists. Every \(L_{\max}\)
   below is this comparison, not a new proof.
3. **Heuristic extrapolation.** Wall-clock estimates from a
   previous \(68\)M progress log. Never used for
   certification.

## 1. What floor is currently available?

Two certified floors already exist.

- Lean residual floor \(261\) (`reachesOne_of_lt_two_hundred_sixty_one`).
- Python first-passage: every \(2\le n\le 2\cdot 10^6\) reaches
  \(1\) (`J-residual-floor-two-million`). Paper A Theorem 4.6
  prints the weaker published floor \(N_0=10^6\).

A previous unfinished science run at \(N_0=6.8\cdot 10^7\)
reached \(97\%\) with two failures and a peak of
\(82\,265\,352\) bits, above the old \(80\)M-bit cap. That run
is not a certificate. The working bit cap is now \(128\)M.

## 2. What period bound does it produce?

At \(N_0=10^6\), the implemented parity \(6/5\) table excludes
every \(L\le 25780\). First survivor \(L=25781\),
\(n_{\max}^{\mathrm{par}}(25781)=26254995\). Through \(L\le 10^5\)
there are \(141\) leftovers. The laboratory crude table at
\(2\cdot 10^6\) has the same prefix.

Replacing \(6/5\) by \(1\) on the same parity charge still has
first survivor \(25781\)
(\(n_{\max}^{\mathrm{par},1}(25781)=22102111\)). The cutoff
\(25781\) is not an artifact of \(6/5\).

## 3. What would \(10^7\), \(10^8\), \(10^9\) produce?

Implemented contiguous cutoff \(L_{\max}(N_0)\), scan
\(L\le 2\cdot 10^5\):

| Verified floor \(N_0\) | \(L_{\max}\) parity \(6/5\) | Gain over \(25780\) | First survivor | Leftovers in scan | Required computation |
|-----------------------:|----------------------------:|--------------------:|---------------:|------------------:|---------------------:|
| \(10^6\) | \(25780\) | baseline | \(25781\) | \(141\) through \(10^5\) | existing |
| \(10^7\) | \(25780\) | \(0\) | \(25781\) | \(48\) | about \(10\times\) the published floor |
| \(26254995\) | \(50507\) | \(+24727\) | \(50508\) | \(19\) | cheapest jump |
| \(6.8\cdot 10^7\) | \(50507\) | \(+24727\) | \(50508\) | \(6\) | crude kill of \(25781\); same cutoff |
| \(10^8\) | \(50507\) | \(+24727\) | \(50508\) | \(4\) | no further cutoff gain |
| \(162848325\) | \(101015\) | \(+75235\) | \(101016\) | \(3\) | kills \(50508\) only |
| \(162849448\) | \(176250\) | \(+150470\) | \(176251\) | \(1\) | kills the \(50508\)-cluster |
| \(10^9\) | \(176250\) | \(+150470\) | \(176251\) | \(1\) | still one leftover |
| \(1044093214\) | \(\ge 2\cdot 10^5\) | table | none in scan | \(0\) through \(2\cdot 10^5\) | next record \(176251\) |

Run-packing (Theorem 4.7) does **not** change any of these
first survivors except by lowering some later \(n_{\max}\):
\(n_{\max}^{\mathrm{run}}(25781)=19010076\) still exceeds
\(10^6\), and \(n_{\max}^{\mathrm{run}}(50508)=117641110\)
still exceeds \(10^8\). The period cutoff is not an artifact
of refusing to use Theorem 4.4 directly: constant-\(1\)
parity gives the same first survivors at these floors.

Empirical scaling, not a theorem: leftovers are
near-convergents of \(\ln 2/\ln 3\). The cutoff is constant
between record \(n_{\max}\) values and then jumps to the next
record. Decade-by-decade \(N_0\) is the wrong mesh.

## 4. What does each threshold cost?

The existing verifier walks only odd starts, with exact
integer `isqrt`, until the iterate is strictly below the
start. Evens drop in one step. The induction is: first
passage below the start, then strong induction to \(1\).

Measured on this machine during the \(N_0=26254995\) run:
about \(1.1\cdot 10^5\) to \(1.8\cdot 10^5\) starts per
second at \(23\) workers, until a hard seed appears. A
previous \(68\)M attempt averaged \(2.2\cdot 10^4\) n/s
because it hit an \(82\)M-bit peak.

Asymptotic cost: \(\Theta(N_0)\) starting values, \(\Theta(N_0)\)
odd walks, a few cheap steps on almost every seed, and a thin
set of million-bit orbits whose `isqrt` dominates. Memory is
\(O(1)\) per worker plus optional chunk JSON. The work is
embarrassingly parallel. Memoization does not help: the
algorithm already stops at \(x<n\), and the expensive
intermediates are far above \(N_0\). Arbitrary-precision
arithmetic is the bottleneck on those hard seeds, not
Python-loop overhead on typical seeds.

Heuristic wall-clock, linear in \(N_0\) at \(1.5\cdot 10^5\) n/s:

| \(N_0\) | Heuristic time |
|--------:|---------------:|
| \(2.63\cdot 10^7\) | a few minutes |
| \(10^8\) | about \(10\) minutes |
| \(1.63\cdot 10^8\) | about \(20\) minutes |
| \(10^9\) | about \(2\) hours |

Hard-seed `isqrt` can add more than the linear model. These
times are diagnostics, not certificates.

The implementation scales safely to \(10^7\) and \(10^8\).
It can run \(10^9\) with the \(128\)M-bit cap, but that is
the wrong question.

## 5. Which threshold has the best cost/benefit?

**\(N_0=26254995\).**

It is the least verified floor at which the implemented
Theorem 4.6 architecture excludes \(L=25781\), and it jumps
the cutoff from \(25780\) to \(50507\). The next decade
\(10^8\) is the same theorem. The previous decade \(10^7\)
is the same theorem as \(10^6\).

A later equally efficient jump exists at
\(N_0=162849448\) (cutoff \(176250\)). It is six times the
starts and still a convergent leftover, not a new inequality.

## 6. Does further computation remain worthwhile?

After the \(26254995\) floor: **no**, not as the next
research move.

- Computation is no longer the limiter of the published
  cutoff: \(25781\) is dead.
- Finance is the limiter of \(L=50508\): its parity
  \(n_{\max}\) is \(1.63\cdot 10^8\).
- Run-packing is not the limiter of the first jump, and it
  does not bring \(50508\) down to a cheap floor.
- The leftover structure (near-convergents of
  \(\ln 2/\ln 3\)) is the same obstruction the Baker / Rhin,
  prefix-weight, and packing attacks already met.

Further verification is possible. It is not the cheapest
source of a stronger theorem.

## 7. What should replace it?

A length-only improvement of the defect sum that kills
\(L=50508\) at the new floor — the Paper A Section 5
state-distribution program, parked — or a new exact
constraint on near-convergent words. Not another \(N_0\)
campaign, and not a hypothetical stronger inequality
without a proof.

## Recommendation

After the certified run at \(N_0=26254995\):

\[
\boxed{\text{STOP COMPUTING — IMPROVE THE MATHEMATICS}}
\]

The one computation this phase justifies is exactly that
floor. Do not raise \(N_0\) to \(10^8\) for a visually
larger search. Do not treat finance-survivor lengths as
candidate cycles. Do not claim totality.

## Recomputed theorem (instance of Theorem 4.6)

Once the first-passage certificate at \(N_0=26254995\)
verifies:

\[
\boxed{\text{No nontrivial Juggler cycle has length at most }50507.}
\]

Equivalently, any nontrivial cycle has period at least
\(50508\). This uses the existing \(6/5\) parity architecture
and the new verified floor. It is not a termination proof.
The first finance-survivor is \(L=50508\), with
\(n_{\max}^{\mathrm{par}}=162848325\).

## Verifier bottleneck

Current implementation: `verify_floor` /
`verify_floor_certified` in
`research.juggler_sequence`. Exact integer parity and
`isqrt`. Chunked, resumable, SHA-256 of chunk records.
Floating point is not used for certification.

What limits a larger run is rare high-bit orbits (the
unfinished \(68\)M log peaked at \(82\)M bits), not the
number of starts and not GPU occupancy. Certificate harvest
to \(10^9\) on CUDA is a different computation (bounded
first-descent words) and is not a descent floor.
