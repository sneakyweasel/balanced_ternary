# The nested parity discrepancy lemma (two-step parity)

Analytic document for the promoted two-step parity branch, revised by
the Phase-2 review pass (see the review record after Theorem C) and
extended by the Phase-3 depth-4 part (Lemma D, Theorem E,
Corollary F) and the Phase-4 beyond-depth-4 part (Lemma G,
Propositions H/I/J, Conjecture K). Claim labels are per statement.
Ledger rows: `J-nested-parity-discrepancy`,
`J-fourth-letter-linearization`, `J-triple-parity-discrepancy`,
`J-four-step-descent-density`, `J-second-order-linearization`,
`J-equidistribution-implies-density-one`.
Not imported into the finite-dynamics note yet. Not a termination
claim; the tier-2 discrepancy bound and density-one statement are
NOT claimed unconditionally.

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

## Part II: the depth-4 extension

Throughout Part II, additionally \(v = v(n) = \lfloor m^{3/2}\rfloor
= \operatorname{isqrt}(m^3)\), \(Y = m^{3/2}\), \(\theta_2 = \{m^{3/2}\}
= Y - v\). For an odd start with \(m\) odd, \(J^2(n) = v\); if
moreover \(v\) is even, \(J^3(n) = \lfloor v^{1/2}\rfloor\). The three
sign functions are \(\psi_1 = \psi(n^{3/2}) = (-1)^m\),
\(\psi_2 = \psi(m^{3/2}) = (-1)^v\), and \(\psi_3 = \psi(v^{1/2}) =
(-1)^{\lfloor\sqrt v\rfloor}\), each evaluated unconditionally (no
branch condition).

**Branch consistency.** The OOEE class is exactly \(\{n \text{ odd}:
\psi_1 = -1,\ \psi_2 = +1,\ \psi_3 = +1\}\): the factor
\((1+\psi_2)/2\) in the indicator algebra vanishes precisely when
\(v\) is odd, i.e. exactly where \(J^3\) would take the odd branch, so
the unconditional \(\psi_3\) is only ever weighted on the even branch,
where it computes the true fourth letter. Exact check
(`ooee_indicator_identity_check`): `itinerary_word(n,4) == "OOEE"` iff
\((\psi_1,\psi_2,\psi_3) = (-1,+1,+1)\) for all odd \(n \le 20001\).

### Lemma D (fourth-letter linearization) — EXACT — HUMAN PROOF

For every odd \(n \ge 3\),

\[
v^{1/2} \;=\; n^{9/8} \;+\; D(n),
\qquad
-\tfrac34\, n^{-3/8} - n^{-9/8} \;\le\; D(n) \;\le\; 0 .
\]

More precisely \(D(n) = -\tfrac34\theta\, n^{-3/8}
- \tfrac12\theta_2\, m^{-3/4} - E_3(n) - E_2(n)\) with
\(0 \le E_3 \le \tfrac3{32}(X-1)^{-5/4}\) and
\(0 \le E_2 \le \tfrac18 (Y-1)^{-3/2}\).

*Proof.* Two applications of the Lemma A pattern. First, with
\(f(t) = (Y-t)^{1/2}\) on \([0,\theta_2]\), Taylor with Lagrange
remainder gives \(v^{1/2} = Y^{1/2} - \tfrac12\theta_2 Y^{-1/2} -
E_2\), \(E_2 = \tfrac18(Y-\xi)^{-3/2}\theta_2^2 \in [0,
\tfrac18(Y-1)^{-3/2}]\), and \(Y^{1/2} = m^{3/4}\),
\(Y^{-1/2} = m^{-3/4}\). Second, with \(f(t) = (X-t)^{3/4}\) on
\([0,\theta]\): \(m^{3/4} = X^{3/4} - \tfrac34\theta X^{-1/4} - E_3\),
\(E_3 = \tfrac3{32}(X-\xi')^{-5/4}\theta^2 \in [0,
\tfrac3{32}(X-1)^{-5/4}]\), and \(X^{3/4} = n^{9/8}\),
\(\theta X^{-1/4} = \theta n^{-3/8}\). Combine; every term is
nonnegative, and \(\tfrac12 m^{-3/4} + E_3 + E_2 \le n^{-9/8}\) for
\(n \ge 3\) (the three subdominant amplitudes are \(\asymp
\tfrac12 n^{-9/8}, n^{-15/8}, n^{-27/8}\)). \(\square\)

The decisive feature: unlike the depth-2 layer, *every* non-smooth
term now has decaying amplitude. The cumulative phase cost of
replacing \(\tfrac k2 v^{1/2}\) by the smooth \(\tfrac k2 n^{9/8}\)
over a dyadic block \(n \sim P\) is
\(\ll k \sum_{n \sim P} n^{-3/8} \ll k P^{5/8}\), which for
\(k \le P^{1/24}\) is \(\ll P^{2/3}\), negligible against the target
\(P^{23/24}\). Exact validation (`fourth_letter_scan`, scaled-integer
arithmetic at \(10^{30}\)): the two-sided bound holds on all odd
\(n \le 4001\) and at \(n = 10^6{+}1, 10^7{+}3, 10^9{+}1,
10^{12}{+}1\), worst ratio \(|D|/\text{bound} = 0.9970\), consistent
with the supremum \(1\) approached as \(\theta \to 1^-\).

### Theorem E (triple parity discrepancy) — EXACT — HUMAN PROOF

For every \(\varepsilon > 0\) and every
\((a,b,c) \in \{0,1\}^3 \setminus \{(0,0,0)\}\),

\[
\Bigl|\sum_{n \le N,\ n \text{ odd}}
\psi(n^{3/2})^{a}\,\psi(m^{3/2})^{b}\,\psi(v^{1/2})^{c}\Bigr|
\;\ll_\varepsilon\; N^{23/24+\varepsilon}.
\]

Consequently each of the eight sign classes of
\((\psi_1, \psi_2, \psi_3)\) on odd \(n \le N\) has cardinality
\(\tfrac N{16} + O(N^{23/24+\varepsilon})\).

*Proof.* The \(c = 0\) cases are Theorem C and Theorem 5.1. For
\(c = 1\), wave-expand all present sign factors as in Step 1 of
Theorem C (Vaaler modes and majorants; mode coefficients
\(\mu, \nu, \rho \in \tfrac12\mathbb Z\), truncations
\(J_1 = J_2 = J_3 = P^{1/24}\); double and triple majorant products
are again nonnegative trigonometric polynomials whose mode sums fall
into the same families). Writing \(i = 2\mu\), \(j = 2\nu\),
\(k = 2\rho\), it suffices to bound, uniformly for \(|i| \le 2J_1\),
\(|j| \le 2J_2\), \(1 \le |k| \le 2J_3\),

\[
S_{i,j,k}(P) = \sum_{n \in (P,2P],\ n \text{ odd}}
e\bigl(\tfrac i2 n^{3/2} + \tfrac j2 m^{3/2} + \tfrac k2 v^{1/2}\bigr).
\]

**Smoothing the fourth letter.** By Lemma D, replacing
\(\tfrac k2 v^{1/2}\) by \(\tfrac k2 n^{9/8}\) changes \(S_{i,j,k}\)
by at most \(2\pi\tfrac{|k|}2 \sum_{n \sim P}\bigl(\tfrac34 n^{-3/8}
+ n^{-9/8}\bigr) \ll |k| P^{5/8} \le P^{2/3}\).

**Case \(j = 0\) (pure fourth-letter modes).** The remaining sum is a
single smooth exponential sum with phase \(\varphi(n) = \tfrac i2
n^{3/2} + \tfrac k2 n^{9/8}\) (the odd-\(n\) restriction adds only a
linear phase \(n/2\), invisible to derivative tests). Both curvature
terms are positive for \(i, k > 0\):
\(\varphi'' = \tfrac{3i}8 n^{-1/2} + \tfrac{9k}{128} n^{-7/8}\)
(conjugate for negative modes; for mixed signs with \(|i| \ge 1\) the
first term dominates the second by \(\gg P^{3/8 - 1/24}\), so the sign
is still fixed). Van der Corput II on the block: for \(i = 0\),
\(\lambda \asymp |k| P^{-7/8}\) gives \(\ll |k|^{1/2} P^{9/16} +
|k|^{-1/2} P^{7/16} \ll P^{5/8}\); for \(|i| \ge 1\),
\(\lambda \asymp |i| P^{-1/2}\) gives \(\ll |i|^{1/2} P^{3/4} +
P^{1/4} \ll P^{3/4 + 1/48}\). Both are \(\ll P^{23/24}\).

**Case \(j \ne 0\) (mixed modes).** After the smoothing step the
phase is exactly the Theorem C phase plus the smooth passenger
\(\tfrac k2 n^{9/8}\). Run Steps 2–6 of Theorem C verbatim; the
passenger only modifies the smooth part \(A_h\) of the differenced
phase by \(\tfrac k2[(n{+}2h)^{9/8} - n^{9/8}]\), whose second
derivative is \(\ll |k| h P^{-15/8}\) — smaller than the retained cell
curvature \(jhP^{-3/4}\) by \(P^{-9/8}|k/j| \ll 1\) and than the
\(r\)-mode curvature \(|r|P^{-1/2}\) by more. Every sign-dominance
and ratio check of Theorem C holds with these margins, so
\(|S_{i,j,k}| \ll P^{23/24}\) uniformly.

Summing mode weights (\(O(\log^3 P)\)), majorant families, and dyadic
blocks gives the theorem. \(\square\)

### Corollary F (four-step descent density 13/16) — EXACT — HUMAN PROOF

\[
\#\{n \le N: n \text{ odd},\ \text{itinerary } OOEE\}
= \tfrac N{16} + O(N^{23/24+\varepsilon}),
\]

and the class of starts with a certified descent within four steps —
evens (one step), \(OE\) (two steps), \(OOEE\) (four steps) — has
cardinality

\[
\tfrac N2 + \tfrac N4 + \tfrac N{16} + O(N^{23/24+\varepsilon})
= \tfrac{13N}{16} + O(N^{23/24+\varepsilon}).
\]

*Proof.* By branch consistency,
\(\#OOEE = \tfrac18\sum_{n \le N \text{ odd}}
(1-\psi_1)(1+\psi_2)(1+\psi_3)\); expanding gives the main term
\(\tfrac18 \cdot \tfrac N2\) and seven sign sums bounded by
Theorem E. Every \(OOEE\) start descends within four steps by the
power envelope: the word \(OOEE\) has \(3^2 < 2^4\), so the
Lean-verified contraction (`J-power-envelope-contraction`) applies.
The even class and the \(OE\) class carry their existing one- and
two-step certificates (Theorem 5.1 machinery,
`floorPower_odd_even_two_step_lt`). The three classes are disjoint: the
parity of \(n\) separates the evens, and the second letter separates
\(OE\) from \(OOEE\). \(\square\)

Census cross-check: at \(N = 10^7\) the observed OOEE fraction of odd
starts is \(0.125039\) (pinned in `test_two_step_parity.py`),
i.e. \(N/16\) overall, matching the theorem's main term.

### Review record (Phase 3)

Same adversarial standard as the Phase-2 review; the new surface is
small because Theorem C's machinery is reused unchanged.

- **Lemma D remainder chain**: both Taylor steps re-derived with
  Lagrange form; all four terms of \(D(n)\) are nonpositive, so the
  two-sided bound is exact, and the validator's worst ratio
  \(0.9970\) approaches the theoretical supremum \(1\).
- **Cumulative absorption**: the fourth letter is smoothed *before*
  any differencing, at cost \(kP^{5/8}\); no \(\theta\)- or
  \(\theta_2\)-dependence survives into the van der Corput stage.
  This is the structural reason depth 4 is easier than depth 2: the
  amplitude \(n^{-3/8}\) decays, whereas the depth-2 layer carried
  the growing amplitude \(n^{3/4}\) that forced Lemma A.
- **Pure-\(k\) curvature**: \(\varphi'' > 0\) termwise for positive
  modes; for mixed-sign \((i,k)\) the \(i\)-term dominates by
  \(P^{9/24}\)-margins, so van der Corput II applies with an absolute
  constant on each dyadic block.
- **Mixed-mode dominance**: the passenger curvature
  \(|k|hP^{-15/8}\) is checked against *both* retained scales
  (\(jhP^{-3/4}\) cells, \(|r|P^{-1/2}\) modes); margins \(\ge
  P^{9/8}/|k| \ge P^{9/8 - 1/24}\).
- **Branch consistency**: verified exactly on a window
  (`ooee_indicator_identity_check`), and structurally: the
  \((1+\psi_2)\) factor annihilates the odd-\(v\) terms where the
  unconditional \(\psi_3\) would misreport the fourth letter.
- **Float sanity** (not a verdict): \(|S_{0,0,1}(P)|/\#\{n\} =
  0.0002,\ 0.007,\ 0.00001\) at \(P = 10^4, 10^5, 10^6\), well below
  the proven \(P^{-7/16}\)-scale envelope.

No step failed. The exponent \(23/24\) is inherited from Theorem C
and remains deliberately unoptimized.

## Part III: beyond depth 4 — tier structure and the density-one program

Part III is the Phase-4 record: what generalizes for free, what the
exact ceiling of the current machinery is, the proved algebraic
bricks for the next tier, two recorded route obstructions, and the
conditional density-one theorem. The tier-2 discrepancy bound itself
is **not claimed**.

**Layer bookkeeping.** Along a word, the \((t{+}1)\)-th letter is the
parity of \(\lfloor x_t^{3/2}\rfloor\) (odd branch) or
\(\lfloor x_t^{1/2}\rfloor\) (even branch), with \(x_t \asymp
n^{\gamma_t}\), \(\gamma_t = \prod_{s\le t} e_s\), \(e_s \in
\{3/2, 1/2\}\). Linearizing the new floor leaves a non-smooth layer of
amplitude \(\asymp x_t^{e-1}\): **growing** (\(x_t^{1/2} =
n^{\gamma_t/2}\)) on an odd branch, **decaying** (\(x_t^{-1/2}\)) on
an even branch. Parts I–II carry exactly one growing layer (the
\(m^{3/2}\) layer serving letters 2 and 3) plus any number of decaying
ones.

### Proposition I (one-growing-layer ceiling) — EXACT — HUMAN PROOF

Within the machinery of Parts I–II, the certifiable contracting
prefixes are exactly \(E\), \(OE\), and \(OOEE\), and the certified
descent density \(13/16\) of Corollary F is the exact ceiling of the
method. Any further certified density requires a second growing
layer.

*Proof.* A word is contracting at length \(\ell\) with \(o\) odd
letters iff \(3^o < 2^\ell\). The method proves letters at positions
1–3 of any word (one growing layer) and further letters only along
even branches (decaying layers). Hence the analyzable words have all
odd letters at positions \(\le 2\): the contracting minimal ones are
\(E\) (\(3^0 < 2\)), \(OE\) (\(3 < 4\)), and \(OOE^k\) with
\(9 < 2^{k+2}\), minimal at \(k = 2\), i.e. \(OOEE\). Extensions of a
contracting word certify no new starts. Densities: \(\tfrac12 +
\tfrac14 + \tfrac1{16} = \tfrac{13}{16}\). Any other contracting word
has an odd letter at a position \(\ge 3\), whose parity needs the
\(x_t^{3/2}\) layer with growing amplitude \(n^{\gamma_t/2}\) —
a second growing layer. \(\square\)

### Lemma G (second-order exact linearization) — EXACT — HUMAN PROOF

For odd \(n \ge 5\), with \(X = n^{3/2}\), \(m = \lfloor X\rfloor\),
\(\theta = X - m\):

\[
m^{3/4} = \tfrac5{32}n^{9/8} + \tfrac{15}{16}m\,n^{-3/8}
- \tfrac3{32}m^2 n^{-15/8} - R_3,
\qquad 0 \le R_3 \le \tfrac5{128}(X-1)^{-9/4},
\]

\[
m^{9/4} = \tfrac5{32}n^{27/8} - \tfrac9{16}m\,n^{15/8}
+ \tfrac{45}{32}m^2 n^{3/8} + R_4,
\qquad -\tfrac{15}{128}(X-1)^{-3/4} \le R_4 \le 0 .
\]

*Proof.* Taylor to third order with Lagrange remainder for
\(f(t) = (X-t)^{3/4}\) resp. \((X-t)^{9/4}\) at \(t = \theta\), then
the exact substitution \(\theta = X - m\) in **both** the linear and
the quadratic terms. For \(m^{3/4}\): \(f = X^{3/4} -
\tfrac34\theta X^{-1/4} - \tfrac3{32}\theta^2 X^{-5/4} -
\tfrac5{128}\theta^3 (X-\xi)^{-9/4}\); substituting turns the three
polynomial terms into \(\tfrac5{32}X^{3/4} + \tfrac{15}{16}mX^{-1/4}
- \tfrac3{32}m^2X^{-5/4}\) (coefficient check at \(m = X\):
\(\tfrac5{32} + \tfrac{30}{32} - \tfrac3{32} = 1\)). For
\(m^{9/4}\): \(f = X^{9/4} - \tfrac94\theta X^{5/4} +
\tfrac{45}{32}\theta^2 X^{1/4} - \tfrac{15}{128}\theta^3
(X-\xi)^{-3/4}\), and substitution gives the stated form (check:
\(\tfrac5{32} - \tfrac{18}{32} + \tfrac{45}{32} = 1\)). \(\square\)

The novelty over Lemma A: the integer \(m\) now enters
*quadratically* with smooth coefficients, and the remainders decay
(\(n^{-27/8}\) and \(n^{-9/8}\) scales). Exact validation
(`second_order_scan`, scale \(10^{60}\) — needed because the
identities cancel to \(n^{-9/8}\) out of \(n^{27/8}\)-size terms):
all odd \(5 \le n \le 2001\) and \(n = 10^6{+}1, 10^7{+}3, 10^9{+}1,
10^{12}{+}1\).

### Proposition H (polynomial phase for the OOO\* layer) — EXACT — HUMAN PROOF

For odd \(n \ge 5\), with \(v = \lfloor m^{3/2}\rfloor\):

\[
v^{3/2} = -\tfrac5{64}n^{27/8} + \tfrac9{32}m\,n^{15/8}
- \tfrac{45}{64}m^2 n^{3/8} + \tfrac{15}{64}v\,n^{9/8}
+ \tfrac{45}{32}vm\,n^{-3/8} - \tfrac9{64}vm^2 n^{-15/8}
+ \mathrm{err}(n),
\qquad |\mathrm{err}| \le \tfrac34 n^{-9/8}.
\]

*Proof.* Lemma A at \(Y = m^{3/2}\) gives \(v^{3/2} =
\tfrac32 v\,m^{3/4} - \tfrac12 m^{9/4} + E_5\), \(0 \le E_5 \le
\tfrac38(Y-1)^{-1/2}\); insert both Lemma G identities. The error
collects \(E_5 - \tfrac32 vR_3 - \tfrac12 R_4\), bounded by
\((\tfrac38 + \tfrac{15}{256} + \tfrac{15}{256})n^{-9/8}(1+o(1)) <
\tfrac34 n^{-9/8}\) for \(n \ge 5\) (using \(v \le X^{3/2}\), so
\(vX^{-9/4} \le X^{-3/4}\)). Coefficient sanity at the nominal point
\((m, v) = (X, X^{3/2})\): \((-5 + 18 - 45 + 15 + 90 - 9)/64 = 1\),
recovering \(v^{3/2} = n^{27/8}\). \(\square\)

So the OOO\* mode phase \(\tfrac k2 v^{3/2}\) is, up to absorbable
errors, a *polynomial of degree \((2,1)\) in the integer pair
\((m, v)\)* with smooth coefficients — the analogue of the linear
structure that made Theorem C possible. Validated exactly through
\(n = 10^{12}\) (`second_order_scan`, identity `v32`). The branch
algebra also mirrors Corollary F exactly: `itinerary_word(n,4) ==
"OOOE"` iff \(((-1)^m, (-1)^v, (-1)^{\lfloor v^{3/2}\rfloor}) =
(-1, -1, +1)\), machine-checked (`ooo_indicator_identity_check`);
the \((1-\psi_2)\) factor vanishes exactly where \(J^3\) would take
the even branch.

### Two route obstructions (negative knowledge)

**Composed cells fail.** On a Lemma-B cell (where \(g_1 = m(n{+}2h) -
m(n)\) is constant) the second-level gap \(g_2 = v(n{+}2h) - v(n)\)
takes a new value at essentially every point: \(\Delta Y =
(m{+}G)^{3/2} - m^{3/2}\) varies by \(\asymp h P^{3/4}\) across the
cell, so the sub-cells of constant \(g_2\) have sub-unit length.
Validated (`second_gap_collision_check` at \(n \sim 10^6\),
\(h \in \{1,3\}\)): distinct-value ratio \(1.0000\). The naive
two-level composition of Lemma B is dead; do not retry it.

**The fiber transform loses to sparsity.** Reindexing by \(m\) (each
\(m\) has at most one odd \(n\)-preimage, present iff
\(\lceil m^{2/3}\rceil < (m{+}1)^{2/3}\) with the right parity)
strips one nesting level: \(\psi_1\) becomes the *linear* phase
\((-1)^m\), \(\psi_2\) a single-layer and \(\psi_4\) a double-layer
(Theorem-C shaped) object in \(m\). But the fiber indicator has
density \(\asymp \tfrac23 m^{-1/3}\) on the range \(Q = N^{3/2}\):
its sawtooth part produces full-length mode sums
\(\sum_m e(rm^{2/3} + \cdots)\) that must beat the sparsity exponent
\(1/3\), while the engine saves only \(1/24\); already the \(r = 1\)
mode is fatal (van der Corput II gives exactly \(Q^{2/3}\), the
trivial target, with zero margin). Route parked, recorded.

### The viable route (program, not a claim)

Difference the Proposition-H polynomial phase once in \(n\)
(A-process, Lemma-B cells): the quadratic terms leave \(\theta\)- and
\(m\)-linear structures with coefficients of size \(\asymp
khn^{7/8}\) — genuinely growing sawtooth amplitudes, unlike Part I
where they decayed. These require shifted-window Vaaler expansions
(modes concentrated near the amplitude), after which the phases are
\(rn^{3/2}\)-type with \(r \lesssim khP^{7/8}\); third-derivative
tests give per-mode savings \(\asymp P^{5/48}\), and a second
differencing handles the \(g_2\)-content via the *smooth-in-\(m\)*
expansion \(e(r'[(m{+}G)^{3/2} - m^{3/2}])\), which linearizes by
Lemma A again. Expected outcome: the OOO\* discrepancy at
\(O(N^{1-\delta_2})\) with \(\delta_2\) of order \(10^{-2}\). Status:
**CONJECTURE** (route sketch with proved bricks; the float sanity
\(|S_{v^{3/2}}|/\#\{n\} = 0.009, 0.003, 0.001\) at \(P = 10^4, 10^5,
10^6\) shows the target sum cancels strongly).

### Proposition J (equidistribution implies density-one descent) — EXACT — HUMAN PROOF

Let \(d \ge 1\) and suppose that for every itinerary word \(w\) of
length \(d\) (over all starts, first letter = parity of \(n\)),

\[
\bigl|\#\{n \le N : \mathrm{word}_d(n) = w\} - 2^{-d}N\bigr|
\;\le\; E_d(N).
\]

Then the starts with **no** contracting prefix of length \(\le d\)
number at most

\[
e^{-cd}\,N \;+\; 2^d E_d(N),
\qquad
c \;=\; 2\Bigl(\tfrac{\log 2}{\log 3} - \tfrac12\Bigr)^2
\;>\; 0.0342 .
\]

Every other start \(n \ge 2\) satisfies \(T^t(n) < n\) for some
\(t \le d\) with a uniform power-envelope certificate
(`J-power-envelope-contraction`). Consequently, if \(E_d(N) =
O_d(N^{1-\delta_d})\) with \(\delta_d > 0\) for every \(d\), the set
of starts admitting a finite descent certificate has natural density
\(1\).

*Proof.* A word \(w\) of length \(d\) has a contracting prefix iff
\(3^{o_t} < 2^t\) for some \(t \le d\), where \(o_t\) counts odd
letters among the first \(t\). If \(w\) has no contracting prefix
then in particular \(3^{o_d} \ge 2^d\), i.e. \(o_d \ge \beta d\) with
\(\beta = \log 2/\log 3 = 0.6309\ldots\) The number of such words is
\(2^d\,\Pr[\mathrm{Bin}(d, \tfrac12) \ge \beta d] \le 2^d
e^{-2(\beta - 1/2)^2 d}\) by Hoeffding's inequality. Each word class
has at most \(2^{-d}N + E_d(N)\) members; summing over the
non-contracting words gives the count. The density-one statement
follows by letting \(d \to \infty\) slowly with \(N\) (e.g. any
\(d(N) \to \infty\) with \(2^{d}E_d(N)/N \to 0\)). \(\square\)

This is the Juggler analogue of the Terras program for Collatz:
all-depth parity equidistribution (Conjecture K below) implies that
almost every start descends below itself. The implication is
unconditional; only the hypothesis is open beyond the proved cases
(\(d \le 3\) fully; \(d = 4\) even branch).

### Census gate at depth 6 — COMPUTATIONALLY VERIFIED

Exact census of all 32 depth-6 words on odd \(n \le 2\cdot10^6\):
every word is realized, and the deviations obey the two-regime
minimal-scale envelope

\[
|D_w| \;\le\; C\,\max\bigl((N/2)\,N^{-\gamma_{\min}(w)},\
N^{2/3}\bigr),
\qquad
\gamma_{\min}(w) = \min_t \gamma_t,
\]

with \(C = 0.61\) (and \(C = 0.40, 1.02\) at \(N = 10^5, 5\cdot
10^5\)). E-heavy words (e.g. \(OEEEE\ast\), whose deepest value is
\(\asymp N^{3/32} \approx 4\)) are boundary-dominated and *cannot*
look equidistributed at feasible \(N\); words whose scales stay
\(\ge N^{3/8}\) deviate by \(\le 14\%\) of their expectation. No
structural bias beyond the boundary effect. This also predicts the
word-dependent exponents any proof must produce: \(\delta_w\)
degrades as \(\gamma_{\min}(w)\) shrinks.

### Conjecture K (all-depth equidistribution)

For every fixed itinerary word \(w\): \(\#\{n \le N:
\mathrm{word}(n) \text{ has prefix } w\} = 2^{-|w|}N +
O(N^{1-\delta_w})\), \(\delta_w > 0\). Proved for \(|w| \le 3\), and
for \(|w| = 4\) on the even branch (Theorems C/E). With
Proposition J this implies density-one finite descent. The next
concrete case is tier 2: the OOO\* split via the double-differencing
route above.

Import of Theorems C/E and Corollary F into the finite-dynamics note
remains a separate editorial phase.
