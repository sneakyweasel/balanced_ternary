# Balanced-ternary operators

This record is the operator branch of the project. Collatz is one
application of the same maps, not the object of search. Claim labels are
**PROVED**, **VERIFIED COMPUTATIONALLY**, **CONJECTURE**, **OBSERVATION**,
**KNOWN**, **REFUTED**. Finite checks are not infinite statements.

The implementation lives in `src/bt/operators.py`. Integer-level
`apply(n)` and word-level `apply_word(word)` are separate methods. Passing a
bare integer to `apply_word` is a `TypeError`.

Display is MSD-first. Mathematical indices are LSD-first: \(a_0\) is the last
character of the displayed word.

## Operators

| Symbol | Integer map | Word map | Domain | FST? |
| --- | --- | --- | --- | --- |
| \(S\) | \(3n\) | append LSD \(0\) | \(\mathbb{Z}\) | yes, 1 state |
| \(N\) | \(-n\) | digitwise sign flip | \(\mathbb{Z}\) | yes, 1 state |
| \(D\) | \((n-a_0)/3\) | drop LSD | \(\mathbb{Z}\) | yes, LSD sequential |
| \(I_+,I_-\) | \(3n\pm 1\) | prepend LSD \(\pm\) | \(\mathbb{Z}\) | yes, 1 state |
| \(K_3\) | \(n/3^{v_3(n)}\) | skip trailing zeros | \(\mathbb{Z}\) | yes, 2 states |
| \(W\) | A134028 reverse | reverse, canonicalize | \(\mathbb{Z}\) | not one-way sequential |
| \(W_z\) | A160652 | reverse, keep trailing zeros | \(\mathbb{Z}\) | not one-way sequential |
| \(W_t\) | A351702 | reverse all but MSD | \(\mathbb{Z}\) | not one-way sequential |
| \(M_2\) | \(2n\) | LSD doubling Mealy | \(\mathbb{Z}\) | yes, 3 states |
| \(H_2\) | \(n/2\) | LSD `/2` Mealy | \(2\mathbb{Z}\) | yes, 3 states, partial |
| \(H_3\) | \(n/3\) | \(D\) on \(a_0=0\) | \(3\mathbb{Z}\) | yes, partial |

\(I_0=S\). Polynomial evaluation \(P_n\) is a representation, not a
\(\mathbb{Z}\to\mathbb{Z}\) iterator; see
[balanced_ternary_polynomials.md](balanced_ternary_polynomials.md).

## Shift \(S\)

**PROVED.** If \(n=\sum_i a_i 3^i\) then \(3n=\sum_i a_i 3^{i+1}\). For
\(n\neq 0\), \(\mathrm{BT}(3n)\) is \(\mathrm{BT}(n)\) followed by a trailing
`0`. For \(n=0\) the canonical word stays `0`. Lean: `eval_shiftWord`.

Exact feature effects for \(n\neq 0\):

- length \(+1\)
- weight, signed digit sum, positive count, negative count unchanged
- zero count \(+1\)
- position-class sums shift index by one, with new \(S_0=0\)

## Negation \(N\)

**PROVED.** \(N(n)=-n\) is digitwise negation. \(N\circ N=\mathrm{id}\).
\(w(N(n))=w(n)\) and \(s(N(n))=-s(n)\). \(N\) commutes with \(S\) and with
\(D\). Lean: `mapNeg_involutive`, `N_commutes_S_word`.

## Digit derivative \(D\)

**PROVED.** \(a_0\in\{-1,0,+1\}\) is \(n\) reduced modulo 3 into that alphabet,
and

\[
n=a_0+3D(n),\qquad D(n)=\frac{n-a_0}{3}.
\]

This is **not** floor division: \(D(2)=1\) while \(2//3=0\), and
\(D(-1)=0\) while \((-1)//3=-1\).

**PROVED.** \(D\circ S=\mathrm{id}\). \(S\circ D(n)=n-a_0\), hence
\(S\circ D=\mathrm{id}\) if and only if \(3\mid n\). \(D\circ N=N\circ D\).
The maps \(I_{\pm}\) are sections: \(D\circ I_{\pm}=\mathrm{id}\).

**PROVED.** The \(D\)-orbit of \(n\) is \(n,D(n),\ldots,0\). Successive LSDs
recover the canonical digit sequence. For \(n\neq 0\) the number of steps to
\(0\) equals the canonical length \(L_3(n)\) (OEIS A134021, with the
convention that the zero word has length 1 so the stopping time of \(0\) is
\(0\) rather than \(1\)).

This is the natural right shift on balanced-ternary words. Combinatorial
identities that only look at suffixes of \(\mathrm{BT}(n)\) are identities
about \(D^j(n)\). That is organisational, not a new arithmetic theorem.

## Reversal family

All three maps reuse the existing encoder. Known facts are preserved:

- **REFUTED** that \(W\) is an involution. Witness \(W(3)=1\neq 3\).
- **PROVED:** \(W(W(n))=n\) iff \(n=0\) or \(3\nmid n\). Equivalently
  \(W\circ W=K_3\).
- **PROVED:** \(W_z\) and \(W_t\) are involutions on \(\mathbb{Z}\).
- **PROVED:** \(W(-n)=-W(n)\) and \(W(3^m n)=W(n)\), so \(W\circ S=W\).
- **PROVED:** \(W^3=W\) as functions, because \(W\circ K_3=K_3\circ W=W\).

Studied with \(S,N,D\) rather than with Collatz \(T\). Interaction details
are in [operator_algebra.md](operator_algebra.md).

## Digit integral

**PROVED.** \(I_d(n)=3n+d\) for \(d\in\{-1,0,+1\}\) satisfies \(D(I_d(n))=n\).
The three integrals are the complete set of right inverses of \(D\).

## Three-kernel \(K_3\)

**PROVED.** \(K_3(n)=n/3^{v_3(n)}\) (with \(K_3(0)=0\)) is LSD-first
2-state sequential: skip trailing zeros, then copy. Trailing zeros are
locally visible in balanced ternary. This is the exact contrast with
unrestricted 2-adic odd-part, which is not one finite-state transduction.

## CLI

```powershell
btlab operators apply S 42
btlab operators derivative 5
btlab operators shift 5
btlab operators id
```
