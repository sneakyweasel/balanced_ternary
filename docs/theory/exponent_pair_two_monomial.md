# A two-monomial exponent-pair question

Status: **external mathematics**. Not a laboratory branch, not a
Juggler construction, and not a Phase-0. The objects are a clean
two-monomial exponential sum and the classical exponent-pair hull.

## The question

Let \(c\neq 0\) and \(1\le\lvert j\rvert\le M^{2/5}\). Write

\[
f(m)=c\,m^{9/4}-j\,m^{2/3},\qquad
T_j(M)=\sum_{m\le M}e\bigl(f(m)\bigr).
\]

An exponent pair \((p,q)\) is *applicable* to \(f\) when the standard
derivative hypotheses of the pair hold on the relevant dyadic blocks
(Graham–Kolesnik / van der Corput: the first derivative of \(f\) is
monotonic of size \(\asymp M^{5/4}\)). Any such pair yields the block
bound \(T_j\ll M^{(5/4)p+q}\).

\[
\boxed{\text{Can one prove }\tfrac54 p+q<\tfrac23
\text{ for an exponent pair applicable to }cm^{9/4}-jm^{2/3}?}
\]

Equivalently: produce any applicable pair below that line, or any
specialized two-monomial bound of the same strength. Either would give
the sub-density estimate \(T_j=o(M^{2/3})\).

On those blocks the \(9/4\)-term dominates every derivative uniformly
in \(\lvert j\rvert\le M^{2/5}\) once the block length is
\(\gg M^{0.27}\); smaller blocks are already below \(M^{2/3}\). The
first-derivative scale is \(T\asymp M^{9/4}\), so
\(\alpha=\log M/\log T=4/9\).

## Known values

The functional \(\phi(p,q)=\tfrac54 p+q\) on recorded pairs and
ceilings (exact arithmetic):

| Source | Pair or bound | \(\phi\) |
|---|---|---|
| van der Corput derivative tests | \((1/6,2/3)\), \((1/14,11/14)\); \(k=3,4,5\) tests | \(7/8\) |
| Huxley 2005 | \((32/205,269/410)\) | \(349/410\approx 0.851\) |
| Bourgain 2017 | \((13/84,55/84)\) | \(95/112\approx 0.848\) |
| Bombieri–Iwaniec dream ceiling | \(p=3/20\) on \(q=p+\tfrac12\) | \(67/80=0.8375\) |
| Needed for \(T_j=o(M^{2/3})\) | — | \(<2/3\) |
| Exponent-pair conjecture | \((0,1/2)\) | \(1/2\) |

Literature: `bourgain-2017-exponent-pair`, `huxley-2005-zeta-v`,
`huxley-1996-area-lattice-points`,
`kuipers-niederreiter-1974-uniform-distribution`.

## What is already settled

**Generic hull pairs miss (KNOWN).** The recorded minimum of
\(\phi\) on the known exponent-pair hull is Bourgain's
\(95/112\approx 0.848\), above \(2/3\). Huxley's pre-decoupling pair
is slightly worse. Van der Corput tests land at \(7/8\).

**Bombieri–Iwaniec cannot reach the line, even conjecturally within
the method (KNOWN).** BI-type pairs sit on the half-line
\(q=p+\tfrac12\). There \(\phi=(9/4)p+\tfrac12\), and
\(\phi=2/3\) at exactly \(p=2/27\). In the zeta normalization a
half-line pair gives \(\zeta(\tfrac12+it)\ll t^{\theta}\) with
\(\theta=p\). Even a complete resolution of both spacing problems
cannot get the zeta exponent below \(3/20\) (Huxley; Encyclopedia of
Mathematics, “Bombieri–Iwaniec method”). Hence no BI-producible pair
has \(p<3/20\), and

\[
\frac{3/20}{2/27}=\frac{81}{40}=2.025.
\]

The dream-ceiling functional is \(67/80=0.8375\), still far above
\(2/3\). Bourgain's \(13/84\) already resolves the first spacing
problem optimally; the remaining within-method slack is the second
spacing problem, and zeroing it cannot reach \(2/27\).

The \(B\)-process fixes the half-line pointwise. The \(A\)-process
worsens \(\phi\) precisely when \(p<1/6\) (exact root of
\(9p^2+\tfrac92 p-1\)), which covers every historical BI pair. No
\(A\)/\(B\) transform escapes. The regime \(\alpha=4/9\) sits in the
method's middle range \((2/5,1/2)\): there is no boundary loophole.

**The secondary monomial is inert (KNOWN).** On the blocks that
matter, \(-jm^{2/3}\) is lower order in every derivative and does not
change the resonance geometry. A native run of the method on
\((T,M)=(M^{9/4},M)\) is subject to the same ceiling.

## What would count as a solution

Any one of the following:

- a new exponent pair \((p,q)\) applicable to \(f\) with
  \(\tfrac54 p+q<\tfrac23\);
- a specialized bound for this two-monomial phase (not necessarily
  packaged as a generic pair) giving \(T_j=o(M^{2/3})\).

The exponent-pair conjecture point \((0,1/2)\) would clear the line
with a power saving. No currently published pair or BI-refinement
does.

Not claimed: that \(T_j=o(M^{2/3})\) is false. The sum is expected
to sit at square-root scale; the missing object is a proof past the
known hull.

This is a question in the theory of exponent pairs. It is not a
dynamical construction, and it should not be rewritten as one.

## Appendix: laboratory origin

The phase \(f(m)=cm^{9/4}-jm^{2/3}\) is the Vaaler fluctuation of a
Piatetski–Shapiro inversion
\(S_c(N)=\sum_{m\le\lfloor N^{3/2}\rfloor}r(m)\,e(cm^{9/4})\),
\(r\in\{0,1\}\). The laboratory records of that reduction and of the
BI-ceiling comparison are
[juggler_ps_inversion_barrier.md](../problems/juggler_ps_inversion_barrier.md)
and
[juggler_bi_resonance_limit.md](../problems/juggler_bi_resonance_limit.md).
Both branches are **CLOSE**. This page is the export of the remaining
external question; it is not a successor research phase.
