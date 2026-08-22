# Exponent languages and low-amplitude Collatz cycles

This note records Milestone 11. Claim labels are **EXACT — LEAN VERIFIED**,
**EXACT — HUMAN PROOF** / **PROVED**, **COMPUTATIONALLY VERIFIED**,
**CONJECTURE**, and **REFUTED**. Nothing here is a proof or disproof of
the Collatz conjecture. The OEIS / warp branch remains frozen.

The affine identities

\[
T^p(n)=\frac{3^p n+C}{2^K},\qquad
n(2^K-3^p)=C
\]

are **not new**. They are the existing periodic fixed-point formula.
This milestone starts from exponent words and asks which primitive words
can be exact positive accelerated cycles, especially at low amplitude.

## Objects

A nonempty word \(\mathbf{k}=(k_0,\ldots,k_{p-1})\) is **primitive** when
it is not \(u\) repeated \(r>1\) times. The canonical representative of a
rotation class is the lexicographically minimal rotation.

`PeriodicExponentCode` distinguishes:

- algebraic candidate \(C/D\), \(D=2^K-3^p\);
- integral positive odd candidate;
- exact period (valuations match and the orbit closes);
- exact primitive cycle.

The affine formula alone does not certify the valuation word.

## Amplitude

Accelerated states are odd. This repository uses

\[
A_{\mathrm{add}}=\max n_i-\min n_i,\qquad
A_{\mathrm{mul}}=\frac{\max n_i}{\min n_i}.
\]

**PROVED; LEAN VERIFIED:** \(A_{\mathrm{add}}\) is even. These are not
assumed to match any preprint. Literature adapters:

- Fernández–Ibáñez / Terras: Syracuse parity bits, \(N=K\), \(r=p\);
- Lebel radius: Hamming distance to a Christoffel exponent word of the
  same length.

The trivial cycle \((2)\) has \(A_{\mathrm{add}}=0\) and \(A_{\mathrm{mul}}=1\).
Additive bound \(A=1\) is empty among odd states.

## Recorded census

Exact enumeration of all words with \(1\le p\le 6\) and \(1\le k_i\le 4\):

| stage | count |
| --- | --- |
| enumerated | 5460 |
| primitive | 5356 |
| contracting \(2^K>3^p\) | 5332 |
| \(D\mid C\) | 6 |
| integral positive odd | 6 |
| exact period | 6 |
| exact primitive cycle | 1 |
| distinct canonical cycles | 1 |

The six integral words are \((2)^p\) for \(p=1,\ldots,6\). The unique
primitive exact cycle is \((2)\) at \(n=1\). A finite search does not
exclude other cycles.

Low-amplitude languages in this bound: \(L_{A_{\mathrm{add}}=0}=\{(2)\}\).
All larger additive bounds in the same search contain only that cycle.

## Theorems

1. Expanding periods have no positive candidate. **PROVED; LEAN VERIFIED**.
2. \(n(2^K-3^p)=C\) implies \(D\mid C\). **PROVED; LEAN VERIFIED**.
3. Primitive \(\Leftrightarrow\) not a proper repetition. **PROVED; LEAN VERIFIED**
   at the list level (`IsPrimitive`, \(u{+}{+}u\) is not primitive).
4. Rotation of an exact affine block: if \(2^{k_0}x=3n+1\) and
   \(2^{k_0}C'=3C+D\), then \(xD=C'\). **PROVED; LEAN VERIFIED**.
   Amplitude is rotation-invariant on exact cycles. **PROVED**.
5. Additive amplitude of odd states is even. **PROVED; LEAN VERIFIED**.
6. \(R(\mathbf{k})=1\) iff \(\mathbf{k}=(2)^p\). A nontrivial exact cycle
   therefore has a nested-realizer path with at least one positive lift.
   After the period is realized, further lifts of the repeating word of
   \(n=1\) are zero. **PROVED**.
7. All-ones words are expanding, hence not positive cycles. **PROVED**.

## Divisibility

If \(q\mid D\) and \(q\neq 3\), then \(q\mid C\) iff
\(\sum_{j<p}2^{K_j}3^{-j}=0\) in \(\mathbb F_q\). This is exact and
divisor-specific. It is not a universal residue pin on \(C\).

**PROVED:** \(D=2^K-3^p\not\equiv 0\pmod 3\) for \(p\ge 1\), so \(3\nmid D\).
A claimed obstruction that needs \(3\mid D\) does not apply to this \(D\).

No word-level condition stronger than \(D\nmid C\) was proved for a
positive-density family beyond expanding codes and the all-twos
identity \(C=D\), \(n=1\).

## Repeated factors

Low additive amplitude does not force a nontrivial repeated factor beyond
the trivial cycle. The only exact cycle in the recorded bound is a single
letter. The candidate “low amplitude \(\Rightarrow\) a block must repeat”
is **vacuous** on the known cycle and **not a theorem** for unknown cycles.

## Restrictions classified on the recorded exact-cycle set

| statement | status |
| --- | --- |
| exact cycle \(\Rightarrow\) contracting | **PROVED** |
| additive amplitude even | **PROVED** |
| \(n=1\) iff primitive code \((2)\) | **PROVED** |
| nontrivial \(\Rightarrow\) some positive lift on the nested path | **PROVED** |
| no cycle with \(\max k=1\) | **PROVED** |
| \(K\le 2p\) for exact cycles | **COMPUTATIONALLY VERIFIED** for \(p\le 6\), \(k_i\le 4\); not a proof |
| Christoffel Syracuse words yield only \((2)^p\) | **COMPUTATIONALLY VERIFIED** in the recorded Christoffel sample |

## Strongest new theorem

The genuinely new packaged theorems are the rotation identity for \(C'\)
and the lift dichotomy for nontrivial versus trivial cycles, together
with the even-amplitude law. They are structural. They do not exclude a
positive-density family of low-amplitude nontrivial cycles beyond the
already-known expanding obstruction.

## Assessment

**Useful symbolic cycle structure.** Exact language objects, pruning
counts, rotation and lift closure, and an independent literature
dictionary. Not a publishable exclusion of nontrivial cycles, and not a
major Collatz result.

Do not start another milestone from this note.
