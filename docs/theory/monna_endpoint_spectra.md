# Balanced-Monna endpoint spectra

Master record for the promoted Monna gate. Claim labels have the usual
meaning. This is **not** a Collatz note and is **not** an
\(M_k(x^3)\) count.

Python: `research.monna_endpoint_spectra`. Dossier:
[monna_endpoint_spectra.md](../problems/monna_endpoint_spectra.md).
Literature: [monna-1952-digit-reversal](../../literature/monna-1952-digit-reversal.json).

## The map

The balanced Monna map reads a 3-adic expansion as a real series:

\[
\mathcal B\Bigl(\sum_{i\ge 0}a_i 3^i\Bigr)
=\sum_{i\ge 0}a_i 3^{-i-1},
\qquad a_i\in\{-1,0,+1\}.
\]

**REPARAMETERIZATION** (`BTM-balanced-monna`). This is the affine
conjugate of Monna’s 1952 digit-reversal map on standard digits
\(\{0,1,2\}\). The residual graph recursion

\[
\Gamma_F=\bigcup_{a\in\{-1,0,+1\}}
S_{a,\rho_a(F)}(\Gamma_{\mathfrak D_a F}),
\qquad
S_{a,b}(u,v)=\Bigl(\frac{a+u}{3},\frac{b+v}{3}\Bigr)
\]

is the same residual Mealy machine already recorded in
[residual_state_complexity.md](residual_state_complexity.md). It is
not a new dynamical invariant.

`B` is not `bt_reverse`. It is not a Collatz 3-adic endpoint.

## Endpoint pairs

Two distinct 3-adic integers form an *endpoint pair* when they have a
common finite prefix of length \(n\), one boundary digit, and opposite
infinite tails, so that \(\mathcal B(u)=\mathcal B(v)\). Kind `plus`
has tails \((+,\ ---{\ldots})\) versus \((0,\ +++{\ldots})\); kind
`minus` has tails \((0,\ ---{\ldots})\) versus \((-, +++{\ldots})\).
These are the only real collisions of \(\mathcal B\).

In values, with midpoint \(\zeta=(u+v)/2\),

\[
u=\zeta+2\cdot 3^n,\qquad
v=\zeta-2\cdot 3^n,\qquad
u-v=4\cdot 3^n.
\]

## Three notions

Keep these separate.

- **Preservation:** \(\mathcal B(F(u))=\mathcal B(F(v))\).
- **\(3\)-adic divergence depth:** \(t=v_3(F(u)-F(v))\).
- **Euclidean jump:** \(\lvert\mathcal B(F(u))-\mathcal B(F(v))\rvert\),
  zero if and only if preservation holds.

A matching valuation is not preservation. The image pair
\((F(u),F(v))\) is an endpoint pair only if the difference is
\(\pm 4\cdot 3^k\) *and* the tails have the form above.

## Cubic identities

**EXACT — LEAN VERIFIED** (`BTM-x3-depth`). For every endpoint pair,

\[
u^3-v^3=4\cdot 3^n\bigl(3\zeta^2+4\cdot 3^{2n}\bigr).
\]

Hence

\[
t=v_3(u^3-v^3)=n+\min\bigl(1+2v_3(\zeta),\,2n\bigr),
\]

or \(t=3n\) when \(\zeta=0\). The two arguments of the minimum have
opposite parity whenever \(\zeta\neq 0\), so there is never a
cancellation tie.

**EXACT — LEAN VERIFIED** (`BTM-x3-no-preserve`). The factor
\(3\zeta^2+4\cdot 3^{2n}\) is never \(\pm 3^k\). Cubing therefore
never sends an endpoint pair to an endpoint pair, and the Euclidean
jump of \(x^3\) is never zero.

Verified on all 728 pairs through \(n\le 5\).

## Spectrum

**EXACT — HUMAN PROOF** (`BTM-x3-spectrum`). At level \(n=0\) both
kinds have depth \(0\). For \(n\ge 1\):

- depth \(3n\) occurs twice (the zero prefix, both kinds);
- depth \(n+1+2s\) occurs \(4\cdot 3^{n-s-1}\) times for each
  \(0\le s<n\) (exact midpoint valuation \(s\), two signs, two kinds).

This matches the enumeration through \(n\le 5\).

## Controls (not ledger rows)

- \(x\), \(-x\), and constants preserve every pair.
- \(x+1\) fails exactly on kind `plus` with prefix \(+^n\), including
  the empty prefix at \(n=0\): adding one carries through the balanced
  window into the boundary. All other pairs through \(n\le 5\) are
  preserved.
- \(2x+1\) preserves none: the difference is \(8\cdot 3^n\), which is
  not of the form \(\pm 4\cdot 3^k\).

## Literature

- `KNOWN`: Monna 1952; radix-\(3\) endpoint ambiguity; real plots of
  1-Lipschitz maps after digit reversal; polarity of \(-x\).
- `REPARAMETERIZATION`: balanced digits as an affine conjugate of the
  standard Monna map; \(\Gamma_F\) as the residual machine.
- `PROJECT-SPECIFIC`: the cubic valuation law, the closed spectrum,
  and the proof that \(x^3\) never preserves an endpoint pair.

## What is not claimed

- A new \(3\)-adic ring or topology.
- That \(\dim_H\Gamma_F\) is a nontrivial invariant. Every
  1-Lipschitz \(F:\mathbb Z_3\to\mathbb Z_3\) has graph dimension \(1\).
- Any closed form for \(M_k(x^3)\). That counting line is closed.
- Any Collatz statement, and any identification with `bt_reverse`.

## Formalization

Ledger rows `BTM-balanced-monna`, `BTM-x3-depth`, `BTM-x3-spectrum`,
`BTM-x3-no-preserve`. `BTM-x3-depth` and `BTM-x3-no-preserve` are
`formal/BTCalculus/MonnaEndpointCube.lean`. Spectrum remains human.
No `sorry`.

## Code

- `research.monna_endpoint_spectra.triage`
- `tests/research/monna_endpoint_spectra/test_triage.py`
