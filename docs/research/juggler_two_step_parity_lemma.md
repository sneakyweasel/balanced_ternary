# The nested parity discrepancy lemma (two-step parity)

Analytic document for the promoted two-step parity branch, revised by
the Phase-2 review pass (see the review record at the end). Claim
labels are per statement. Ledger row: `J-nested-parity-discrepancy`.
Not imported into the finite-dynamics note yet. Not a termination
claim.

Throughout, \(n\) is odd, \(X = n^{3/2}\), \(m = m(n) = \lfloor
n^{3/2}\rfloor = \operatorname{isqrt}(n^3)\), \(\theta = \theta_n =
\{n^{3/2}\} = X - m\), and \(\psi(x) = (-1)^{\lfloor x\rfloor}\). The
first two image parities of an odd start are \((-1)^m = \psi(n^{3/2})\)
and \((-1)^{\lfloor m^{3/2}\rfloor} = \psi(m^{3/2})\).

## Context

Theorem 5.1 of the finite-dynamics note bounds the depth-1 sum
\(\sum_{n \le N \text{ odd}} \psi(n^{3/2}) \ll N^{5/6}\). The Phase-0
census (see `juggler_two_step_parity.md`) shows the depth-2/3/4 joint
classes equidistribute empirically with envelope exponents
\(0.28\)–\(0.66\). A literature check (August 2026) found no
equidistribution result for nested floor powers
\(\lfloor\lfloor n^c\rfloor^d\rfloor\): the Piatetski-Shapiro corpus
covers single floors, intersections, and pseudo-polynomials only.
Novelty annotation: independent.

The naive Taylor expansion
\(m^{3/2} = n^{9/4} - \tfrac32\theta n^{3/4} + O(n^{-3/4})\) leaves a
fractional part with growing amplitude \(n^{3/4}\), which defeats the
van der Corput method directly (localizing \(\theta\) in short blocks
gives intervals of length \(\asymp \lambda_3^{-1/3}\), exactly the
threshold where the third-derivative test saves nothing). The route
below removes the fractional part exactly before any analysis.

## Lemma A (exact linearization) — EXACT — HUMAN PROOF

For every odd \(n \ge 3\),

\[
m^{3/2} \;=\; \tfrac32\, m\, n^{3/4} \;-\; \tfrac12\, n^{9/4}
\;+\; E(n),
\qquad
0 \;\le\; E(n) \;\le\; \tfrac38\,(n^{3/2}-1)^{-1/2}
\;\le\; \tfrac12\, n^{-3/4}.
\]

*Proof.* Let \(f(t) = (X - t)^{3/2}\) on \([0, \theta]\), so
\(f(\theta) = m^{3/2}\). Taylor with Lagrange remainder at \(0\):
\(f(\theta) = X^{3/2} - \tfrac32 X^{1/2}\theta + \tfrac38 (X -
\xi)^{-1/2}\theta^2\) for some \(\xi \in (0, \theta)\). Substitute
\(\theta = X - m\) in the linear term:
\(X^{3/2} - \tfrac32 X^{1/2}(X - m) = -\tfrac12 X^{3/2} + \tfrac32 m
X^{1/2} = -\tfrac12 n^{9/4} + \tfrac32 m n^{3/4}\). The remainder is
\(E(n) = \tfrac38 (X-\xi)^{-1/2}\theta^2 \in [0, \tfrac38(X -
1)^{-1/2}]\), and \((X-1)^{-1/2} \le \tfrac43 X^{-1/2} =
\tfrac43 n^{-3/4}\) already for \(n \ge 3\). \(\square\)

The point: the non-smooth integer \(m\) enters the phase *linearly*,
multiplied by the smooth function \(\tfrac32 n^{3/4}\); no fractional
part survives. Exact validation (`identity_scan`, scaled-integer
arithmetic at \(10^{30}\) precision): the bound holds on all odd
\(n \le 4001\) and at \(n = 10^6{+}1, 10^7{+}3, 10^9{+}1, 10^{12}{+}1\),
with worst observed ratio \(E(n) / (\tfrac12 n^{-3/4}) = 0.7494\),
matching the theoretical supremum \(3/4\) attained as
\(\theta \to 1^-\).

## Lemma B (gap cell structure) — EXACT — HUMAN PROOF

For \(h \ge 1\) and odd \(n\), let \(g(n) = m(n+2h) - m(n)\) and
\(\delta(n) = (n+2h)^{3/2} - n^{3/2}\). Then

\[
g(n) = \lfloor\delta(n)\rfloor + \kappa(n),
\qquad
\kappa(n) = \bigl[\{n^{3/2}\} \ge 1 - \{\delta(n)\}\bigr] \in \{0,1\}.
\]

*Proof.* \(g = \lfloor X + \delta \rfloor - \lfloor X \rfloor =
\lfloor \delta \rfloor + \lfloor \{X\} + \{\delta\} \rfloor\), and the
last floor is \(1\) precisely when \(\{X\} + \{\delta\} \ge 1\).
\(\square\)

Since \(\delta\) is smooth and increasing with \(\delta'(n) =
\tfrac32[(n+2h)^{1/2} - n^{1/2}] \asymp h n^{-1/2}\), the level sets of
\(G(n) = \lfloor\delta(n)\rfloor\) partition a dyadic block \(n \in
(P, 2P]\) into \(O(hP^{1/2})\) cells of length \(\asymp P^{1/2}/h\),
on which \(G\) is constant and \(G \asymp hP^{1/2}\). Exact validation
(`gap_decomposition_check`): thousands of consecutive odd \(n\) at
\(10^6\) and \(10^9\), \(h \in \{1,2,3,7\}\), all matches, only
exact-boundary samples skipped.

## Theorem C (nested parity discrepancy) — EXACT — HUMAN PROOF

For every \(\varepsilon > 0\) and every choice of signs
\((a, b) \in \{0,1\}^2\), \((a,b) \ne (0,0)\),

\[
\Bigl|\sum_{n \le N,\ n \text{ odd}}
\psi(n^{3/2})^{a}\,\psi(m(n)^{3/2})^{b}\Bigr|
\;\ll_\varepsilon\; N^{23/24 + \varepsilon}.
\]

Consequently each of the four joint parity classes of
\((m, \lfloor m^{3/2}\rfloor)\) on odd \(n \le N\) has cardinality
\(\tfrac{N}{8} + O(N^{23/24+\varepsilon})\); in particular the
odd-to-odd cylinder refines to
\(\#\{n \le N \text{ odd}: J(n) \text{ odd},\ J^2(n) \text{ even}\}
= \tfrac N8 + O(N^{23/24+\varepsilon})\),
one letter deeper than Theorem 5.1.

### Proof outline with exponent bookkeeping

Work on dyadic blocks \(n \in (P, 2P]\), odd. Fix truncations
\(J_1 = J_2 = P^{1/24}\) (wave modes), \(H = P^{1/12}\) (differencing),
\(R = P^{1/4}\) (cell modes).

**Step 1 (wave expansion).** By Vaaler's theorem applied to the
period-2 square wave, \(\psi(x) = V_J(x/2) + O(\Delta_J(x/2))\) where
\(V_J(t) = \sum_{0 < |q| \le J} a_q e(qt)\) with \(|a_q| \le
\min(1, 2/|q|)\), and \(\Delta_J \ge 0\) is a trigonometric polynomial
of degree \(J\) with constant term \(O(1/J)\) and coefficients
\(O(1/J)\). For the product, \(|\psi_1\psi_2 - V_1 V_2| \le \Delta_1 +
\Delta_2 + \Delta_1\Delta_2\), and \(\Delta^2\) is again a nonnegative
trigonometric polynomial (degree \(2J\), constant term \(O(1/J)\)),
so every error term is a majorant sum of the same shape. Expanding
both factors reduces the theorem to bounds, uniform in the mode
coefficients \(\mu, \nu \in \tfrac12\mathbb Z\) with \(|\mu| \le J_1\),
\(\tfrac12 \le |\nu| \le J_2\) (majorant modes contribute integer
\(\mu, \nu\); wave modes contribute odd-over-two values), for

\[
S_{\mu,\nu}(P) = \sum_{n \in (P,2P],\ n \text{ odd}}
e\bigl(\mu\, n^{3/2} + \nu\, m^{3/2}\bigr),
\]

plus pure first-factor majorant sums: \(\sum_n \Delta_{J_1}(n^{3/2}/2)
\ll P/J_1 + P^{5/6+\varepsilon} \ll P^{23/24+\varepsilon}\) by the
depth-1 machinery, while \(\sum_n \Delta_{J_2}(m^{3/2}/2)\) reduces to
the \(\mu = 0\) case of \(S_{\mu,\nu}\) itself. The analysis below
only uses \(|\nu| \ge \tfrac12\) and the truncation sizes; mode
weights sum to \(O(\log^2 P)\).

Below, write \(i = 2\mu\) and \(j = 2\nu\), so \(|i| \le 2J_1\),
\(1 \le |j| \le 2J_2\); every bound depends only on \(|i|, |j|\) and
absolute constants.

**Step 2 (linearization).** By Lemma A, replacing \(\tfrac j2 m^{3/2}\)
by \(\tfrac{3j}4 m n^{3/4} - \tfrac j4 n^{9/4}\) changes \(S_{\mu,\nu}\)
by at most \(2\pi \tfrac j4 \sum_{n \sim P} n^{-3/4} \ll j P^{1/4}
\le P^{7/24}\).

**Step 3 (van der Corput A-process).** With \(H = P^{1/12}\),
\(|S_{\mu,\nu}|^2 \le \tfrac{2P}H \sum_{0 \le h < H} |T_h|\), where
\(T_h\) sums \(e(\Phi(n+2h) - \Phi(n))\) over the overlap,
\(\Phi\) is the Step-2 linearized phase, and \(T_0 \le P\). The exact
rewrite \(m(n{+}2h)(n{+}2h)^{3/4} - m(n) n^{3/4} = g(n)(n{+}2h)^{3/4}
+ m(n)\,[(n{+}2h)^{3/4} - n^{3/4}]\) with \(m(n) = n^{3/2} - \theta_n\)
gives

\[
\Phi(n{+}2h) - \Phi(n) = A_h(n) +
\tfrac{3j}4\, g(n)\,(n{+}2h)^{3/4} + O(jhP^{-1/4}),
\]

where \(A_h\) is smooth (it collects the \(i\)-difference, the
\(-\tfrac j4\Delta(n^{9/4})\) term, and \(\tfrac{3j}4 n^{3/2}
\Delta(n^{3/4})\)), and the error is exactly the
\(-\tfrac{3j}4\theta_n[(n{+}2h)^{3/4} - n^{3/4}]\) term, of amplitude
\(\le \tfrac{9jh}8 P^{-1/4}\). Cumulative error cost
\(\ll jhP^{3/4} \le P^{7/8}\), and \(\tfrac PH\sum_h jhP^{3/4} \ll
jHP^{7/4} \le P^{15/8+1/24} \ll P^{23/12}\).

A cancellation makes the smooth part harmless: the two
\(n^{5/4}\)-scale contributions of \(A_h\) cancel at leading order.
In integral form \(A_h^{(5/4)} = \tfrac{9j}{16}\int_0^{2h}
(n+t)^{-1/4}[n^{3/2} - (n+t)^{3/2}]\,dt\), and the second
\(n\)-derivative of the integrand vanishes identically at \(t = 0\),
leaving \(A_h'' = \tfrac{81}{256}\,j h^2 n^{-7/4}(1 + o(1))\) plus the
\(i\)-part \(O(ihP^{-3/2})\), both \(o(jhP^{-3/4})\) in our ranges.
(The constant \(81/256 = 0.31640625\) is confirmed by the exact
scaled second-difference validator `smooth_cancellation_check`, which
returns \(0.3164\) across \(n = 10^4\) to \(10^8\) and
\(h \in \{1, 3, 10\}\).)

**Step 4 (cells).** Split \(T_h\) over the \(O(hP^{1/2})\) cells of
Lemma B. On a cell, \(g = G + \kappa\) with \(G\) constant,
\(G \asymp hP^{1/2}\), and \(\kappa(n) = [\{n^{3/2}\} \ge \rho(n)]\)
with \(\rho = 1 - \{\delta(n)\}\) smooth and monotone on the cell.
Vaaler-expand \(\kappa\) with modes \(e(r n^{3/2})\), \(0 < |r| \le
R\). The moving endpoint costs nothing: the coefficient
\(c_r(\rho(n))\) is a linear combination of \(1\) and \(e(-r\rho(n))\)
with weights \(O(1/|r|)\), and since \(\rho(n) = 1 + G - \delta(n)\),
the second piece contributes the *exact* smooth phase
\(r\delta(n)\); combined with the mode, \(e(rn^{3/2} + r\delta(n)) =
e(r(n{+}2h)^{3/2})\) up to a unimodular constant. So every
\(r\)-term falls into one of two smooth phase families,
\(e(rn^{3/2})\) or \(e(r(n{+}2h)^{3/2})\), and no partial summation
over coefficient variation is needed. The main term \(1 - \rho(n) = \delta(n) - G\) has total
variation exactly \(1\) per cell and is absorbed by one Abel
summation. The Vaaler majorant error has total mass \(O(\ell/R)\) per
cell plus mode sums of the same two families with weights
\(O(1/R)\).

**Step 5 (second-derivative test per cell).** The remaining phases are
smooth. For the \(r = 0\) parts, \(f'' = -\tfrac{9j(G+c)}{64}
(n{+}2h)^{-5/4}(1 + o(1))\), single sign, \(|f''| \asymp \lambda_0 =
jhP^{-3/4}\), and the ratio of \(f''\) across a cell is bounded (cell
length \(\ll P^{1/2} \ll P\)). Van der Corput II on a cell of length
\(\ell \asymp P^{1/2}/h\) gives \(\ll \ell\lambda_0^{1/2} +
\lambda_0^{-1/2}\); over all cells:

\[
\ll (jh)^{1/2} P^{5/8} + j^{-1/2} h^{1/2} P^{7/8}.
\]

For \(r \ne 0\), \(f''\) is dominated by the \(r\)-term
\(\asymp |r| P^{-1/2}\) of fixed sign (since \(jh \le P^{1/8} \ll
P^{1/4}\)); the same test and the \(1/|r|\) weights give
\(\ll R^{1/2}P^{3/4} + hP^{3/4}\log P \ll P^{7/8} + hP^{3/4}\log P\).
Majorant errors contribute \(O(P/R) = O(P^{3/4})\).

Total: \(|T_h| \ll P^{7/8}(1 + h^{1/2})\) uniformly in
\(|i| \le 2J_1\), \(1 \le |j| \le 2J_2\).

**Step 6 (assembly).** \(|S_{\mu,\nu}|^2 \ll P^2/H + P^{15/8} H^{1/2}
\ll P^{23/12}\) at \(H = P^{1/12}\), so \(|S_{\mu,\nu}| \ll
P^{23/24}\). Summing wave modes (\(\log^2\)), majorants, and dyadic
blocks (\(\log\)) gives the theorem with \(N^{23/24}\log^3 N\).
\(\square\)

### Review record (Phase 2)

Adversarial re-derivation of every step, at the rigor level applied to
Theorem 5.1. Checks performed and their outcomes:

- **Lemma A remainder**: re-derived with Lagrange form; the validator's
  worst ratio \(0.7494\) matches the theoretical supremum \(3/4\).
- **Smooth cancellation**: the second \(n\)-derivative of the
  \(A_h\)-integrand vanishes identically at \(t = 0\) (symbolic
  check), giving \(A_h'' = \tfrac{81}{256} jh^2 n^{-7/4}(1+o(1))\);
  the exact scaled validator returns \(0.3164 = 81/256\) across four
  decades of \(n\), confirming both the exponent and the constant.
- **Second-derivative dominance**: \(r\)-modes dominate the cell
  phases at scale \(|r|P^{-1/2}\) versus \(jhP^{-3/4}\) since
  \(jh \le P^{1/8} \ll P^{1/4}\); the \(i\)-part is smaller by
  \(P^{-3/4}\); \(f''\) ratio per cell is bounded, so the van der
  Corput II constant is absolute (Graham–Kolesnik Thm 2.2).
- **Moving Vaaler endpoint**: repaired — the coefficient
  \(n\)-dependence splits exactly into the two smooth families
  \(e(rn^{3/2})\), \(e(r(n{+}2h)^{3/2})\); no smooth-weight partial
  summation remains except one Abel summation on \(\delta - G\)
  (variation exactly 1).
- **Majorant products**: \(\Delta_1\Delta_2\)-terms are degree-\(2J\)
  nonnegative trigonometric polynomials with the same treatment;
  statement generalized to mode coefficients in \(\tfrac12\mathbb Z\).
- **Aggregation**: \(P^2/H + PH^{1/2}P^{7/8}\) balances at
  \(H = P^{1/12}\) to \(P^{23/12}\); all error channels
  (\(jP^{5/4}\), \(jHP^{7/4} \le P^{15/8+1/24}\), majorant
  \(P^{23/24}\)-terms) stay below budget.

No step failed. Exponent \(23/24\) deliberately unoptimized (slack at
every stage). Ledger row `J-nested-parity-discrepancy`; the module
flag `depth2_analytic_lemma_proved` is `True` as of this review.

Float sanity (not a verdict): \(|S_{0,1}(P)|/\#\{n\} =
0.0216,\ 0.0027,\ 0.0018\) at \(P = 10^4, 10^5, 10^6\) — cancellation
far stronger than \(P^{-1/24}\), consistent with the census envelope
exponent \(0.28\).

### Extension path (not claimed)

The same substitution linearizes every deeper letter: for the fourth
letter (even branch),
\(m^{3/4} = \tfrac34\, m\, n^{-3/8} + \tfrac14\, n^{9/8} +
O(n^{-15/8})\), with the integer again entering linearly and with
*decaying* smooth amplitude. The depth-4 extension (OOEE density
\(\tfrac1{16} + o(1)\), certified descent class \(\tfrac{13}{16}\))
is a separate phase. Import of Theorem C into the finite-dynamics
note is likewise a separate editorial phase.
