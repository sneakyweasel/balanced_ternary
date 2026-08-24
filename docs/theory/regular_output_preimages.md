# Regular-output preimages of \(x^2\)

Master record for the promoted safety-preimage gate. Claim labels have
the usual meaning. This is **not** a Collatz note and is **not** the
unrestricted count \(M_k(x^2)\).

Python: `research.regular_output_preimages`. Dossier:
[regular_output_preimages.md](../problems/regular_output_preimages.md).
Literature:
[ahmed-savchuk-2020-polynomial-tree-endomorphisms](../../literature/ahmed-savchuk-2020-polynomial-tree-endomorphisms.json),
[anashin-2012-automata-finiteness](../../literature/anashin-2012-automata-finiteness.json),
[grigorchuk-savchuk-2023-solenoidal-maps](../../literature/grigorchuk-savchuk-2023-solenoidal-maps.json).

## The pair

Let \(F(x)=x^2\in\mathbb Z[x]\) and let \(Y=\{0,+\}^\omega\) be the
infinite output language that never emits \(-1\). Write
\(X=F^{-1}(Y)\) for the set of 3-adic inputs whose residual output
word lies in \(Y\). On finite words, \(L\) is the language of trit
words \(w\) such that every output trit of the residual machine of
\(x^2\) along \(w\) lies in \(\{0,+\}\).

The residual of \(x^2\) along the live prefix \((1,0^m)\) is

\[
g_m(x)=3^{m+1}x^2+2x.
\]

## Non-regularity

**EXACT — HUMAN PROOF** (`BTR-x2-safety-nonsific`). For \(m\ge 0\) let
\(w_m=(-1)^{m+1}0\). Then \(w_m\) is accepted by \(g_m\) and rejected
by every \(g_n\) with \(n>m\). Consequently the prefixes \(10^m\) are
pairwise Myhill–Nerode inequivalent in \(L\), so \(L\) is not regular
and \(X\) is not sofic.

The packing identities are

\[
\operatorname{pack}((-1)^k)=-\frac{3^k-1}{2},
\qquad
1-3^k=(+,\ 0^{k-1},\ -)
\]

in balanced digits (the first \(k\) digits of \(1-3^k\) are
\((+,\ 0^{k-1})\)). The correction \(3^{m+1}p_k^2\) has valuation
\(m+1\), so it does not affect those \(k\) digits whenever
\(k\le m+1\). The next letter is then \(0\) for \(g_m\) exactly at
\(k=m+1\), and forbidden for every later \(g_n\).

The human proof is written in the dossier. The tests check the family
and the packing identities on a finite range; they do not replace the
argument.

## What is not claimed

- Ahmed–Savchuk: unrestricted \(x^2\) is infinite-state. `KNOWN`. That
  fact does not name a regular output language whose preimage is
  non-regular. Zero-output lifting (`BTL-zero-output`) is a proper
  subset of \(L\).
- The linear control \(F(x)=x\) has a regular preimage \(\{0,+\}^*\).
  That is the Ahmed–Savchuk linear case and is `KNOWN`.
- Unrestricted residual complexity \(M_k(x^2)=(3^k-1)/2\)
  (`BTA-x2-mn`) is a different theorem.
- Other output languages are not opened.
- No Collatz statement.

## Literature

- `KNOWN`: unrestricted nonlinear polynomials are infinite-state;
  finite-Mealy criteria for 1-Lipschitz maps; lifting equals the
  zero-output subtree.
- `PROJECT-SPECIFIC`: the pair \((x^2,\{0,+\}^\omega)\) is not sofic,
  via the family \(10^m\) / \(w_m\).

## Formalization

Ledger row `BTR-x2-safety-nonsific`. Lean is deferred. No `sorry`.

## Code

- `research.regular_output_preimages.triage`
- `tests/research/regular_output_preimages/test_triage.py`
