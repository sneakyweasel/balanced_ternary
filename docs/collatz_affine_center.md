# Affine-center geometry of Collatz exponent codes

This milestone studies exact inequalities among coordinates already present
in the project. It adds no new numeration system.

## Exact center

For a nonempty exponent code \(\mathbf{k}\), write

\[
m=|\mathbf{k}|,\qquad K=\sum_i k_i,\qquad
X=T^m(R)=\frac{3^mR+C}{2^K}.
\]

Set

\[
D=2^K-3^m.
\]

Since a positive power of \(2\) cannot equal a positive power of \(3\),
\(D\ne0\). The affine map

\[
F(n)=\frac{3^m n+C}{2^K}
\]

has the unique rational fixed center

\[
\boxed{n_*=\frac{C}{D}.}
\]

The implementation records \(m,K,C,R,X,M,n_*\), \(D\), and every rational
quantity as an exact numerator/denominator pair.

## Centered numerator identities

From \(3^mR+C=2^KX\),

\[
\boxed{D R-C=2^K(R-X),}
\]

\[
\boxed{D X-C=3^m(R-X).}
\]

Therefore

\[
R-n_*=\frac{DR-C}{D},\qquad
X-n_*=\frac{DX-C}{D},
\]

and

\[
\boxed{
X-n_*=\frac{3^m}{2^K}(R-n_*).
}
\]

These identities are **PROVED** and **LEAN VERIFIED** in cross-multiplied
integer form. They explain the geometry without floating-point logs.

## Exact regime geometry

### Expanding codes: \(2^K<3^m\)

Here \(D<0\), while \(C,R,X,M>0\). Consequently,

\[
\boxed{n_*<0<M,\qquad n_*<R<X.}
\]

The endpoint lies farther from the center:

\[
|X-n_*|>|R-n_*|.
\]

### Contracting codes: \(2^K>3^m\)

Here \(D>0\) and \(n_*>0\). The centered factor is less than one:

\[
|X-n_*|\le |R-n_*|.
\]

Equality holds exactly when \(R=X=n_*\), as for the code \((2)\). Otherwise
\(R\) and \(X\) lie strictly on the same side of \(n_*\), with \(X\) closer
to the center.

### Endpoint representative

Kramer's least-positive representative satisfies

\[
X\equiv M\pmod{3^m}.
\]

Because \(X,M>0\) and \(M\) is least positive,

\[
\boxed{X=M+q3^m,\qquad q\in\mathbb N,}
\]

so \(M\le X\). This is **PROVED** and the inequality is **LEAN VERIFIED**
from the lift decomposition.

## Critical-near partition

For nonempty codes there is no exactly critical case \(D=0\). A bounded
experiment may declare

\[
|D|\le G
\]

to be `critical-near`, where the integer threshold \(G\) is stored in the
manifest. Absolute gap is scale-sensitive, so every row also retains
\((3^m,2^K)\); results at different scales must not be compared using
\(|D|\) alone.

The recorded run used \(G=10\), \(1\le m\le6\), and \(1\le k_i\le4\).
Among 5,460 exact rows it found:

- 15 `critical-near`;
- 5,321 contracting;
- 124 expanding.

All theorem-backed identities and inequalities had zero failures.

## Coordinate-order tests

The same census preserves witnesses in both directions for each of

\[
R\le M,\quad M\le R,\quad C\le R,\quad R\le C.
\]

Thus none is a universal inequality. It also finds counterexamples to both
\(n_*\le M\) and \(M\le n_*\) when regimes are mixed. The exact universal
comparisons established here are the regime-dependent center inequalities
and \(M\le X\), not a total ordering of \(R,M,C,n_*\).

One stronger pattern survived:

\[
\boxed{n_*\le R.}
\]

It had no failure in the 5,460-row recorded census or in a separate streamed
search of 2,015,539 prefixes with \(m\le8\) and \(k_i\le6\). This is a
**CONJECTURE**, not a theorem. In the contracting regime it is equivalent
to \(X\le R\); a proof or counterexample is the main follow-up question.

## Reproducibility

Use:

```powershell
btprime collatz affine-center 1,4,2
btprime collatz affine-center-census --max-length 6 --max-k 4 `
  --critical-gap 10 --closest-count 20 --write
```

Rows use schema `collatz-affine-center/v1`. JSONL and Parquet artifacts are
ignored by Git; the manifest records all bounds and claim statuses.

Nothing here proves or assumes the Collatz conjecture.
