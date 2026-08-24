# Zero-lift dynamics and infinite itinerary compatibility

Milestone 5. This document studies the lift process of nested valuation
cylinders. It does not claim progress on the Collatz conjecture.

Claim labels are **EXACT — HUMAN PROOF**, **COMPUTATIONALLY VERIFIED**, **CONJECTURE**,
and **OBSERVATION**. Finite checks are never proofs.

Let \(\mathbf{k}=(k_0,k_1,\ldots)\), let

\[
K_m=\sum_{i<m}k_i,\qquad
R_m=R(k_0,\ldots,k_{m-1}),
\]

and define the exact lift coefficient

\[
t_m=\frac{R_{m+1}-R_m}{2^{K_m+1}}.
\]

Nested-cylinder compatibility gives

\[
R_{m+1}=R_m+t_m2^{K_m+1},\qquad t_m\in\mathbb Z_{\ge0}.
\]

This is **EXACT — HUMAN PROOF**. The implementation is `lift_digit` and `lift_digits` in
`src/research/collatz/zero_lift.py`.

## A. Exact infinite-itinerary dichotomy

For every infinite valuation itinerary, the following are equivalent:

1. a positive odd integer realizes every finite prefix;
2. \(R_m\) is eventually constant;
3. \(t_m=0\) eventually.

This equivalence is **EXACT — HUMAN PROOF**.

Suppose a positive integer \(n\) realizes every prefix. At depth \(m\),

\[
n\equiv R_m\pmod {2^{K_m+1}},\qquad
1\le R_m<2^{K_m+1}.
\]

Because every \(k_i\ge1\), the modulus tends to infinity. Once
\(2^{K_m+1}>n\), the positive representative of \(n\)'s class below the
modulus is \(n\) itself. Hence \(R_m=n\) from that point onward.

Conversely, suppose \(R_m=r\) for all \(m\ge N\). For \(m<N\), choose
any \(q\ge N\). The depth-\(q\) cylinder is nested inside the depth-\(m\)
cylinder, so \(r=R_q\) belongs to the depth-\(m\) class. For \(m\ge N\),
\(r=R_m\) belongs directly. Thus the positive odd integer \(r\) realizes
every prefix.

Finally,

\[
R_{m+1}=R_m
\quad\Longleftrightarrow\quad
t_m2^{K_m+1}=0
\quad\Longleftrightarrow\quad
t_m=0,
\]

because \(2^{K_m+1}>0\). Therefore eventual stabilization and eventual
zero lift are equivalent.

The Mathlib-backed project under `formal/` compiles these statements with
Lean 4. `NestedCylinderSystem` records self-realization, nesting,
uniqueness below the modulus, positivity, and eventual modulus growth;
`LiftSystem` records the exact lift equation and digit bound. The
realizer/stabilization/zero-lift equivalences compile without `sorry`.
These results are **EXACT — LEAN VERIFIED**.

## B. Unique zero-lift extension

Fix a finite prefix \(u\), put \(R=R(u)\), and let

\[
x=T^{|u|}(R).
\]

Because \(R\) realizes \(u\), \(x\) is a positive odd integer. Define

\[
k_0=v_2(3x+1).
\]

Then \(R\) realizes \(u\mathbin{\cdot}(k_0)\), so the minimum realizer of
that child is at most \(R\). Nested monotonicity makes it at least \(R\).
Thus it equals \(R\), and \(t(u,k_0)=0\).

For \(j\ne k_0\), the integer \(R\) does not have next valuation \(j\),
so it does not belong to the child cylinder \(u\mathbin{\cdot}(j)\).
That child's minimum cannot equal \(R\). Nested monotonicity then gives
\(R(u\mathbin{\cdot}(j))>R\), hence \(t(u,j)>0\).

Therefore every prefix has exactly one zero-lift extension. This is
**EXACT — HUMAN PROOF** and implemented by `zero_lift_k`.

## C. Deterministic successor map

The canonical state is

\[
(u,R,x,m,K),\qquad x=T^m(R).
\]

Its deterministic successor is

\[
k=v_2(3x+1),\qquad
(u,R,x,m,K)\longmapsto
(u\mathbin{\cdot}k,R,T(x),m+1,K+k).
\]

The realizer \(R\) stays fixed. The \(x\)-coordinate follows the ordinary
accelerated Collatz map exactly. This is **EXACT — HUMAN PROOF** and implemented by
`ZeroLiftState.step`.

Consequently, a complete classification of zero-lift paths would include
a classification of accelerated Collatz orbits. The successor map is an
exact re-encoding, not a simplification theorem.

## D. Periodic and eventually periodic itineraries

Let \(v=(k_0,\ldots,k_{p-1})\), \(K=\sum k_i\), and \(C=C(v)>0\). If the
infinite periodic itinerary \(v^\omega\) has a positive realizer \(n\),
one block acts by

\[
F(n)=\frac{3^pn+C}{2^K}.
\]

Let \(F(x)=(3^px+C)/2^K\) and \(d=2^K-3^p\). Exact integrality of every
block iterate gives

\[
dF^q(n)-C=\frac{3^{pq}}{2^{Kq}}(dn-C)\in\mathbb Z.
\]

Since \(3\) is odd, \(2^{Kq}\) divides \(dn-C\) for every \(q\). A fixed
nonzero integer cannot be divisible by unbounded powers of two, so
\(dn-C=0\). Therefore

\[
n(2^K-3^p)=C.
\]

Hence there is at most one candidate:

\[
n=\frac{C}{2^K-3^p}.
\]

If \(2^K<3^p\), the candidate is negative, so no positive realizer
exists. Equality is impossible for \(p>0\). If \(2^K>3^p\), exact
divisibility, positivity, oddness, and cylinder membership decide
compatibility. These statements are **EXACT — HUMAN PROOF**.

For an eventually periodic itinerary \(uv^\omega\), first find the cycle
point \(n_v\). The only possible initial realizer is

\[
n=\frac{n_v2^{K_u}-C(u)}{3^{|u|}},
\]

followed by exact integrality and cylinder checks. This is **EXACT — HUMAN PROOF** and
implemented in `src/research/collatz/periodic_itineraries.py`.

The bounded search currently finds only repetitions of the known
\((2)^\omega\) cycle at \(n=1\). That result is **COMPUTATIONALLY VERIFIED** only; excluding all other positive cycles is the
Collatz cycle problem.

## E. Finite certificates for positive lift

For a canonical prefix state, retain only

\[
x=T^m(R)\pmod {2^P}.
\]

If \(3x+1\not\equiv0\pmod {2^P}\), its valuation below \(P\) is exact.
The proposed extension \(j\) has zero lift exactly when it equals that
valuation; every other \(j\) has positive lift.

If \(3x+1\equiv0\pmod {2^P}\), the finite state proves only that the true
valuation is at least \(P\). It still certifies positive lift for every
proposed \(j<P\), while proposals \(j\ge P\) remain unresolved.

This finite abstraction and its certificates are **EXACT — HUMAN PROOF**. It is
implemented by `finite_lift_certificate`. It abstracts the immediate lift
decision, not the whole Collatz map. A fixed precision does not resolve
all extensions, because valuations are unbounded.

The collision census for `R mod 2^P` across prefixes is **OBSERVATION**:
collisions with different zero-lift successors show that this coarser
state alone does not determine the next valuation.

## F. Budget connection remains open

The only all-zero-lift finite words starting from the empty prefix are
\((2)^m\). Therefore every expanding finite word has at least one
positive lift. This is **EXACT — HUMAN PROOF**, but it is weak: the same early lift
can witness the statement for arbitrarily many later prefixes.

No theorem here says that sustained low \(K_m/m\) forces infinitely many
positive \(t_m\). That implication remains a **CONJECTURE**. It must not
be inferred from finite expanding-word censuses or from the homogeneous
comparison \(2^{K_m}\) versus \(3^m\).

## Commands

```powershell
btlab collatz zero-lift --ks 1,2 --steps 8 --candidate-k 3 --precision 4
btlab collatz periodic-itinerary 2
btlab collatz zero-lift-census --max-length 4 --max-k 4 --precision 4
```
