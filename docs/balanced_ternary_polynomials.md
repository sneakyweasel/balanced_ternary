# Signed-ternary polynomials

To the canonical expansion \(n=\sum_i a_i 3^i\) associate

\[
P_n(x)=\sum_i a_i x^i\in\mathbb{Z}[x],\qquad a_i\in\{-1,0,+1\}.
\]

Implementation: `src/bt/polynomials.py`. Coefficients are
LSD-first. No general-purpose computer-algebra system is required for
evaluation, reciprocity, or trial division by \(x\pm 1\) and small
cyclotomics.

## Evaluation identities (EXACT — HUMAN PROOF)

\[
P_n(3)=n,\qquad
P_n(1)=\sum_i a_i=s_3(n)\quad(\mathrm{A065363}),\qquad
P_n(-1)=\sum_i a_i(-1)^i\quad(\mathrm{A065364}).
\]

Lean: `evalPoly_reverse_three`, `evalPoly_reverse_one`. Weight of \(n\)
equals the coefficient Hamming weight of \(P_n\).

## Reciprocity

**EXACT — HUMAN PROOF.** The canonical word is a palindrome (A134027) if and only if
\(P_n\) is palindromic as a coefficient tuple, i.e. \(x^d P_n(1/x)=P_n(x)\)
with \(d=\deg P_n\). For \(n\neq 0\) the leading coefficient is nonzero, so
this is the usual reciprocal polynomial.

\(x-1\) divides \(P_n\) iff \(P_n(1)=0\). \(x+1\) divides \(P_n\) iff
\(P_n(-1)=0\).

## Factorization versus the integer \(n\)

A factorization \(P_n=QR\) in \(\mathbb{Z}[x]\) implies
\(n=P_n(3)=Q(3)R(3)\), so it **does** constrain the integer when both
factors have degree at least 1 and \(\lvert Q(3)\rvert>1\). It does **not**
mean that a factorization of \(P_n\) is a previously unknown factorization
of a prime: if \(n=p\) is prime then one of \(Q(3),R(3)\) is \(\pm 1\).

**Example (EXACT — HUMAN PROOF by direct division).** \(13=1+3+9\), word `+++`,
\(P_{13}(x)=1+x+x^2=\Phi_3(x)\), irreducible over \(\mathbb{Q}\) of degree 2.
Here \(P_{13}(3)=13\) is prime and the polynomial is a cyclotomic.

Trial division by \(\Phi_n\) for small \(n\) is implemented; leftover
factors with coefficients outside \(\{-1,0,+1\}\) are named, not recoded
as balanced polynomials.

## Mahler measure (exploratory)

Numerical Mahler measure is computed by a truncated Jensen integral on
the unit circle. It is an **OBSERVATION**. No progress on Lehmer's
problem or Littlewood's problem is claimed. Polynomials with all roots
on the unit circle have Mahler measure 1 when monic (Kronecker); several
cyclotomic \(P_n\) fall in that class and are identified by trial
division, not by the numerical integral.

Bounded-degree, bounded-weight search for “interesting” Mahler values
was not turned into a conjecture. No isolated numerical coincidence
survived the standard of this repository.

## CLI

```powershell
btlab operators poly 13
btlab operators sequences
```
