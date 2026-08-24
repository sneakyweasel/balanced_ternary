# Residual counts versus classical \(p\)-adic polynomial algebra

One page. The section operator and Newton / Mahler bases are not new.
The residual-state counts are the project-specific object.

## Reparameterization (not claimed as new)

The \((3)\)-section

\[
\mathfrak D_a f(x)=\frac{f(a+3x)-\rho_a(f)}{3}
\]

is a Cartier / \(p\)-kernel operator on \(\mathbb Z[x]\). Finite differences
\(\Delta^j f(0)\) are the Newton (binomial) coordinates of
\(\operatorname{Int}(\mathbb Z)\). See
[cahen-chabert-1997-integer-valued-polynomials](../../literature/cahen-chabert-1997-integer-valued-polynomials.json)
and
[kempner-1921-polynomials-residue-systems](../../literature/kempner-1921-polynomials-residue-systems.json).
The kernel statement “\(f\equiv_k g\) iff \(3^k\) divides \((f-g)(n)\) for
all \(n\)” is this dictionary plus prefix locality. Ledger tag:
**REPARAMETERIZATION.**

## What this repository adds

1. The residual Mealy machine of the section operator on LSD-first trit
   words, and the Myhill–Nerode count \(M_k(f)\).
2. The exact quadratic count \(M_k(x^2)=R_k(x^2)=(3^k-1)/2\).
3. The Newton-stratum fibre laws for \(x^3\): \(N_2\) visibility
   \(p\equiv q\pmod{3^r}\), the \(N_1\) valuation filter, and the mismatched
   quotient \(Q_{t,K,W}\) for the surviving \(N_0\) term.
   In degree \(\le 3\) at deficit \(1\), residue visibility is exactly
   \(v_3(a_3)=0\).
   See [cubic_newton_stratum.md](cubic_newton_stratum.md) and the short
   extract [newton_stratum_note.md](newton_stratum_note.md).

Those fibre laws are not in Cahen–Chabert or Kempner. They are also not a
Collatz theorem. No closed formula for \(M_k(x^3)\) is claimed.

The Eisenstein dictionary \(3\sim(1-\omega)^2\) in \(\mathbb Z[\omega]\)
is **KNOWN**
([eisenstein-3-ramification](../../literature/eisenstein-3-ramification.json)).
Rewriting \(N_2\) visibility as \(p\equiv q\pmod{(1-\omega)^{2r}}\) is a
change of uniformizer: **REPARAMETERIZATION** of the existing cubic law,
not a theorem about \(\operatorname{Int}(\mathbb Z[\omega])\). That
\(\mathbb Q(\omega)\) is a Pólya field (cyclotomic;
[zantema-1982-integer-valued-number-fields](../../literature/zantema-1982-integer-valued-number-fields.json))
is likewise **KNOWN** and does not mention residual fibres.

## What is not claimed

- A solution of the Collatz conjecture.
- That balanced ternary is an independent solving coordinate for \(T\).
- That \(M_k(x^d)\) is classical for \(d\ge 3\).
