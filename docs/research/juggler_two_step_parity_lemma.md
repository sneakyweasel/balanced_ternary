# The nested parity discrepancy lemma (two-step parity)

Analytic document for the promoted two-step parity branch, revised by
the Phase-2 review pass (see the review record after Theorem C) and
extended by the Phase-3 depth-4 part (Lemma D, Theorem E,
Corollary F) and the Phase-4 beyond-depth-4 part (Lemma G,
Propositions H/I/J, Conjecture K). Claim labels are per statement.
Ledger rows: `J-nested-parity-discrepancy`,
`J-fourth-letter-linearization`, `J-triple-parity-discrepancy`,
`J-four-step-descent-density`, `J-second-order-linearization`,
`J-equidistribution-implies-density-one`,
`J-even-branch-third-letter`, `J-tier2-gap-and-shifted-forms`,
`J-depth4-slow-branch`, `J-kernel-cancellation`,
`J-depth4-complete`, `J-depth5-contracting`,
`J-five-step-descent-density`,
`J-level3-inner-linearization`,
`J-scale-invariant-R-extension`,
`J-w-family-below-nine-eighths`,
`J-depth7-engine-contracting`,
`J-seven-step-descent-density`.
Imported into the finite-dynamics note (consolidation phase, August
2026): Lemmas A/B as Lemma 5.3, Theorem C as Theorem 5.4,
Proposition L as Proposition 5.5, Lemma D as Lemma 5.6, Theorem E as
Theorem 5.7, Lemma A\u2032 and Theorem Q as Theorem 5.8, Corollary F
and Proposition I as Corollary 5.9, Proposition J as Proposition 6.1,
and Conjecture O as Conjecture 6.2. The floor reductions (Lemmas B/N
pattern, the parity bridge, and the Part-VI double-gap identity) are
Lean-verified in `formal/Problems/Juggler/GapCells.lean`. Part VI
(Phases 8–9) holds the double-differencing proof of Conjecture O
(Theorem R) and the depth-4 completion (Theorem S), both re-derived
by the Phase-9 adversarial review (record in Part VI); ledger rows
`J-kernel-cancellation` (retagged) and `J-depth4-complete`. The
note's Conjecture 6.2 paragraph is superseded and awaits editorial
consolidation. Part VII (Phase 10) closes the two length-5
contracting splits OOOEE and OOEOE (Theorem T, Corollary U), lifting
the certified-descent density to \(7/8\). Part VIII (Phase 11)
isolates the OOOO\* fifth letter as the level-3 floor-defect
kernel \(K_3\) (Lemma V1, Conjecture V); the bound is not claimed.
Part IX (Phase 12) refutes the scale-invariant copy of Theorem R
(Lemma V2, Proposition W). Part X (Phase 13) closes the two
length-7 engine contractors OOEOOEE and OOOEOEE (Theorem X,
Corollary Y), lifting certified descent to \(57/64\).
Not a termination claim; the remaining depth-\(\ge5\) expanders
(OOOO\*, OOEOO, OOOEO) and the density-one statement remain open.

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
(\(d \le 3\) fully — Theorems 5.1/C plus Proposition L of Part IV,
which closed a gap in an earlier phrasing of this remark; at
\(d = 4\), every word except OOO\* via Theorems E and Q of Part V).

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
O(N^{1-\delta_w})\), \(\delta_w > 0\). Proved for \(|w| \le 3\)
(Theorems 5.1/C, Proposition L) and for every word at \(|w| = 4\)
except OOO\* (Theorems E and Q). With Proposition J this implies
density-one finite descent. The only remaining depth-4 case is
tier 2, the OOO\* split, whose precise obstruction — the kernel
\(K_c\) — is isolated in Part IV.

Import of Theorems C/E and Corollary F into the finite-dynamics note
is done (note Theorems 5.4/5.7, Corollary 5.9; consolidation phase).

## Part IV: depth-3 completion and the tier-2 kernel (Phase 5)

### Correction note

Earlier phrasings of the Proposition J remark and Conjecture K said
"proved for depth \(\le 3\)". That was ahead of the facts: Theorem C
proves the depth-3 split only on the OO branch (third letter = parity
of \(\lfloor m^{3/2}\rfloor\), weighted on odd \(m\)), and Theorem E
proves *sign classes* of \((\psi_1, \psi_2, \psi_3)\), which are word
classes only along OOE\*. The OE-branch third letter — the OEO/OEE
split, governed by \(\psi(m^{1/2})\) on even \(m\) — had not been
stated or proved. Proposition L below closes it; the remark and
Conjecture K are now accurate as written.

### Proposition L (OE-branch third letter) — EXACT — HUMAN PROOF

For \(a \in \{0,1\}\),

\[
\Bigl|\sum_{n \le N,\ n \ \mathrm{odd}} \bigl((-1)^m\bigr)^a\,
\psi\bigl(m^{1/2}\bigr)\Bigr| \;\ll_\varepsilon\; N^{7/8+\varepsilon},
\qquad m = \lfloor n^{3/2}\rfloor,
\]

and consequently \(\#\mathrm{OEO}(N),\ \#\mathrm{OEE}(N) = N/8 +
O(N^{7/8+\varepsilon})\).

*Proof.* Exact smoothing (validated, `m12_smoothing_check`, \(n\) to
\(10^{12}\)): with \(X = n^{3/2}\), \(\theta = X - m\),

\[
m^{1/2} = n^{3/4} + D_1(n),
\qquad
-\tfrac12 X^{-1/2} - \tfrac18 (X-1)^{-3/2} \;\le\; D_1 \;\le\; 0,
\]

the Taylor expansion of \((X-\theta)^{1/2}\) with both correction
terms one-signed. \(D_1\) is *decaying*, so replacing
\(\tfrac l2 m^{1/2}\) by \(\tfrac l2 n^{3/4}\) inside a Vaaler mode
costs \(\ll l \sum_{n \sim P} n^{-3/4} \ll l P^{1/4}\), absorbable at
\(l \le 2J = 2P^{1/24}\). The mode sums are then pure:
\(\sum_{n \sim P} e\bigl(\tfrac i2 n^{3/2} + \tfrac l2 n^{3/4}\bigr)\)
with \(l \ne 0\). For \(i \ne 0\): \(\varphi'' = \tfrac{3i}{8}
n^{-1/2}\bigl(1 + O(l P^{-3/4}/i)\bigr)\) is single-signed and
\(\asymp |i| P^{-1/2}\), so van der Corput II gives \(\ll i^{1/2}
P^{3/4} + i^{-1/2} P^{1/4}\). For \(i = 0\): \(\varphi'' \asymp
l P^{-5/4}\), giving \(\ll l^{1/2} P^{3/8} + l^{-1/2} P^{5/8}\). The
odd-\(n\) restriction, Vaaler majorants, truncation tails, and dyadic
assembly are verbatim from Theorem C, and every bound is
\(\ll P^{7/8}\) after summing mode weights. Branch consistency: the
\((1 + (-1)^m)/2\) factor vanishes exactly on odd \(m\), where
\(J^2\) would take the \(3/2\)-power branch, so the unconditional
\(\psi(m^{1/2})\) is only ever weighted where it computes the true
third letter — machine-checked (`oe_indicator_identity_check`,
`itinerary_word(n,3) == "OEE"` iff \(m\) and
\(\lfloor\sqrt m\rfloor\) even, all odd \(n \le 20001\)).
\(\square\)

Depth 3 is now complete: OOO, OOE (Theorem C), OEO, OEE
(Proposition L), each \(N/8 + O(N^{1-\delta})\).

### Lemma M (second-order forms, plain and shifted) — EXACT — HUMAN PROOF

Let \(n \ge 5\) be odd, \(X = n^{3/2}\), \(m = \lfloor X\rfloor\),
\(\theta = X - m\), \(G \ge 0\) an integer, \(Z = X + G\). Then

\[
m^{3/2} = -\tfrac18 X^{3/2} + \tfrac34 m X^{1/2}
+ \tfrac38 m^2 X^{-1/2} + R_5,
\qquad 0 \le R_5 \le \tfrac1{16}(X-1)^{-3/2},
\]

\[
(m+G)^{3/2} = Z^{3/2} - \tfrac32 X Z^{1/2} + \tfrac38 X^2 Z^{-1/2}
+ m\bigl(\tfrac32 Z^{1/2} - \tfrac34 X Z^{-1/2}\bigr)
+ \tfrac38 m^2 Z^{-1/2} + R_6,
\]

with \(0 \le R_6 \le \tfrac1{16}(Z-1)^{-3/2}\).

*Proof.* Both are the second-order Taylor expansion of \(t \mapsto
(B - t)^{3/2}\) at \(t = 0\) (base \(B = X\) resp. \(Z\)) evaluated at
\(t = \theta\), with \(\theta = X - m\) substituted *exactly* so that
\(\theta\) and \(\theta^2\) become polynomials in \(m\) with smooth
coefficients. The remainder \(\tfrac16 f'''(\xi)\theta^3 =
\tfrac1{16}(B-\xi)^{-3/2}\theta^3\), \(\xi \in (0, \theta)\), is
positive since \(f''' > 0\), and at most \(\tfrac1{16}(B-1)^{-3/2}\).
Coefficient sanity at \(m = X\), \(G = 0\): \(-\tfrac18 + \tfrac34 +
\tfrac38 = 1\). Validated exactly (`lemma_m_scan`) for \(n\) up to
\(10^{12}\) with realized gaps \(G = m(n{+}2h) - m(n)\), \(h \in
\{1, 2, 5\}\); the observed defect at \(n = 5\) is \(9.87\cdot
10^{-6}\), matching \(\theta^3 X^{-3/2}/16 = 0.98\cdot10^{-5}\).
\(\square\)

The point of the shifted form: on a Lemma-B cell (constant
\(g_1 = G\)) the level-2 increment \(\Delta Y = (m{+}G)^{3/2} -
m^{3/2}\) becomes a quadratic in \(m\) with smooth coefficients and
remainder \(\ll P^{-9/4}\) — absorbable even against the tier-2
weight \(W \asymp k P^{9/8}\).

### Lemma N (level-2 gap identity) — EXACT — HUMAN PROOF

With \(Y = m^{3/2}\), \(v = \lfloor Y\rfloor\), \(\theta_2 =
\{Y\}\), and \(Y_+ = Y(n + 2h)\), \(\Delta Y = Y_+ - Y \ge 0\):

\[
g_2 \;=\; v(n{+}2h) - v(n)
\;=\; \lfloor \Delta Y \rfloor + \kappa_2,
\qquad
\kappa_2 = \mathbb 1\bigl[\theta_2 \ge 1 - \{\Delta Y\}\bigr]
\in \{0, 1\}.
\]

*Proof.* Identical to Lemma B with \(X \to Y\), \(\delta \to \Delta
Y\): \(\lfloor Y + \Delta Y\rfloor = \lfloor Y\rfloor + \lfloor
\Delta Y\rfloor + \lfloor \{Y\} + \{\Delta Y\}\rfloor\), and the last
floor is the stated indicator. \(\square\) Validated on realized
orbit data (`level2_gap_check`): 800/800 at \(n \sim 10^6\) for
\(h \in \{1, 3\}\), 2995 matches and 5 guard-band skips on a wide
window at \(n \sim 10^3\).

### The kernel isolation (negative knowledge with an exact core)

Differencing the Proposition-H polynomial phase (A-process, step
\(2h\)) splits the \(v\)-block exactly as \(\Delta(vW) = g_2 W_+ +
v\,\Delta W\), where \(W = \partial\Phi_3/\partial v \asymp
\tfrac{3k}4 n^{9/8}\) is the smooth \(v\)-weight.

- \(v\,\Delta W\) is *tame*: \(\Delta W \asymp khP^{1/8}\), and the
  shifted-window Vaaler expansion of its \(\theta_2\)-content has
  window drift \(< 1\) per cell (\(\Delta W\) varies by \(\asymp
  kP^{-3/8}\) across a cell), so its mode mass is logarithmic.
- \(g_2 W_+\) is *the wall*. The exact no-floor form \(g_2 = \Delta Y
  + \theta_2 - \theta_2^+\) leaves \(\Delta Y\,W_+\) (quadratic in
  \(m\) by Lemma M — handled) plus \((\theta_2 - \theta_2^+)W_+\): a
  unit-amplitude sawtooth times a smooth coefficient of size \(\asymp
  kP^{9/8}\) whose derivative \(\asymp kP^{1/8} \gg 1\) crosses
  integers *within single steps of \(n\)*, so no cell of any usable
  length freezes its Fourier window.

Every reorganization tried funnels into the same object:
splitting \(g_2\) by Lemma N instead leaves \(\{\Delta Y\}\,W_+\)
(window drift \(kP^{5/8}/h\) per cell — same wall); the exact swap
\(e(c\,\theta_2) = e(cY)\,e(-\{c\}v)\) (valid because
\(\lfloor c\rfloor v\) is an integer) trades it for the fast sawtooth
\(\{c(n)\}\) times the huge integer \(v \asymp P^{9/4}\) — symmetric
and equally wild; a second A-process transfers the difference either
to \(v\) (reproducing gap terms carrying the *full-size* \(W\)) or to
\(W\) (already exhausted at \(\Delta W\)); and differencing the raw
phase \(\tfrac k2 v^{3/2}\) without Proposition H reproduces
\(c(n)\,g_2\) with \(c \asymp \tfrac{3k}4 v^{1/2}\). By contrast the
\(\kappa_2\)-content is harmless: \(e(\kappa_2 W_+) = 1 +
\kappa_2\,(e(W_+) - 1)\) splits into a 0/1 *indicator weight* —
Vaaler-expandable in \(Y\)-modes with the exact endpoint identity
\(e(r\{\Delta Y\}) = e(r\,\Delta Y)\) for integer \(r\) — times a
factor whose largeness sits harmlessly in the smooth phase.

**Kernel (definition).** For smooth \(c\) with \(c \asymp k P^{9/8}\)
and \(c' \asymp k P^{1/8}\) on \(n \sim P\) (the \(W\)-shaped
family),

\[
K_c(P) \;=\; \sum_{\substack{n \sim P \\ n\ \mathrm{odd}}}
e\bigl(c(n)\,\{\lfloor n^{3/2}\rfloor^{3/2}\}\bigr).
\]

### Conjecture O (kernel cancellation) — *proved: see Theorem R, Part VI*

\(K_c(P) \ll P^{1-\delta}\) for some \(\delta > 0\), uniformly over
the \(W\)-shaped family. Float probe with exact scaled phase
arithmetic (`kernel_probe`, \(c = \tfrac34 n^{9/8}\)): \(|K| = 51.9,\
124.4,\ 1017.5\) on \(5\cdot10^3,\ 5\cdot10^4,\ 5\cdot10^5\) terms —
square-root cancellation. Bounding \(K_c\) was the *precise*
remaining obstacle to the OOO\* split, hence to any depth-4 statement
beyond \(13/16\) through this program. The object is a bilinear
correlation between the fractional parts of one Piatetski–Shapiro
layer and a smooth weight at the scale of the next layer; we found no
treatment of it in the nested-floor literature. Proved in Phases 8–9
with \(\delta = 1/64\) (bounded \(k\)) and \(\delta = 1/72\) for
\(k \le P^{1/24}\): Theorem R.

### Remark (the OEO\* tier is easier — next target)

At depth 4 after OE, the fourth letter on the OEO branch is the
parity of \(\lfloor w^{3/2}\rfloor\) with \(w = \lfloor
m^{1/2}\rfloor \asymp n^{3/4}\). The growing layer here rides the
*slow* variable \(w\), which increments only once every \(\asymp
n^{1/4}\) values of \(n\): its gap variable has long constancy cells,
i.e. the Theorem-C pattern with the roles shifted one level down.
This split (and the easy decaying OEE\* one) looks closable by the
existing engine without meeting the kernel, and would settle depth 4
entirely except OOO\*. *(Done: Part V, Theorem Q.)*

## Part V: the OE\*\* splits — depth 4 complete except OOO\* (Phase 6)

Throughout: \(n\) odd, \(X = n^{3/2}\), \(m = \lfloor X\rfloor\),
\(\theta = X - m\); on the OE branch \(m\) is even and \(J^2(n) = w =
\lfloor U\rfloor\) with \(U = m^{1/2}\), \(\theta_w = U - w\). On the
OEO branch (\(w\) odd) the fourth letter is the parity of \(\lfloor
w^{3/2}\rfloor\); on the OEE branch (\(w\) even), of \(\lfloor
w^{1/2}\rfloor\).

### Lemma A′ (w-level linearization) — EXACT — HUMAN PROOF

For odd \(n \ge 5\):

\[
w^{3/2} \;=\; -\tfrac12 m^{3/4} + \tfrac32 w\, m^{1/4} + E,
\qquad 0 \le E \le \tfrac38 (U-1)^{-1/2},
\]

and since \(U m^{1/4} = m^{3/4}\) *exactly*, equivalently

\[
w^{3/2} \;=\; m^{3/4} \;-\; \tfrac32\, m^{1/4}\,\theta_w \;+\; E .
\]

*Proof.* Lemma A verbatim with base \(U\) in place of \(X\):
\(w^{3/2} = (U - \theta_w)^{3/2} = U^{3/2} - \tfrac32\theta_w U^{1/2}
+ \tfrac38\theta_w^2(U-\xi)^{-1/2}\), substitute \(\theta_w = U - w\)
exactly in the linear term, and note \(U^{3/2} = m^{3/4}\),
\(U^{1/2} = m^{1/4}\). \(\square\) Validated exactly
(`lemma_a_prime_scan`) through \(n = 10^{12}\).

**Corollary (full smoothing).** With \(d_2 = w^{3/2} - n^{9/8} +
\tfrac32 m^{1/4}\theta_w\):

\[
-\tfrac34 n^{-3/8} - \tfrac3{32}(X-1)^{-5/4}
\;\le\; d_2 \;\le\; \tfrac38 (U-1)^{-1/2},
\]

because \(m^{3/4} - X^{3/4} = -\tfrac34\theta X^{-1/4} -
\tfrac3{32}\theta^2(X-\xi')^{-5/4}\) (Taylor of \((X-\theta)^{3/4}\),
both correction terms one-signed) and \(X^{3/4} = n^{9/8}\). All
error terms decay like \(n^{-3/8}\), so for a Vaaler mode \(k\):

\[
\tfrac k2 w^{3/2} \;=\; \tfrac k2 n^{9/8}
\;-\; B(n)\,\theta_w(n) \;+\; O\bigl(k\,n^{-3/8}\bigr),
\qquad
B(n) = \tfrac{3k}4\, m^{1/4} = \tfrac{3k}4 n^{3/8}\bigl(1 +
O(n^{-3/2})\bigr),
\]

with cumulative substitution cost \(O(kP^{5/8})\) on a block
\(n \sim P\). Validated exactly (`oeo_smoothing_scan`) through
\(n = 10^{12}\). *One growing sawtooth remains* — amplitude
\(\asymp k n^{3/8}\) — riding \(\theta_w = \{m^{1/2}\}\), whose
underlying variable increments once every \(\asymp \tfrac43 n^{1/4}\)
steps.

### Theorem Q (the OE\*\* splits) — EXACT — HUMAN PROOF

\[
\#\mathrm{OEOE}(N),\ \#\mathrm{OEOO}(N) = \tfrac N{16} +
O\bigl(N^{7/8+\varepsilon}\bigr),
\qquad
\#\mathrm{OEEE}(N),\ \#\mathrm{OEEO}(N) = \tfrac N{16} +
O\bigl(N^{13/16+\varepsilon}\bigr).
\]

Together with Theorems C/E this proves every depth-4 itinerary word
class except OOO\*.

*Proof.* Indicator algebra: \(\mathrm{OEO}\ast\) is
\(\tfrac18(1+\psi_1)(1-\psi_w)(1\pm\psi(w^{3/2}))\) with \(\psi_1 =
(-1)^m\), \(\psi_w = (-1)^w\); branch-consistent because
\((1+\psi_1)\) vanishes on odd \(m\) (where \(J^2\) takes the odd
branch) and \((1-\psi_w)\) on even \(w\) (where \(J^3\) would take
the even branch) — machine-checked for all four words
(`oeo_indicator_identity_check`). Vaaler-expand the three waves with
truncations \(J_1 = J_2 = J_3 = P^{1/8}\) (majorant errors
\(3P^{7/8}\)); \(\psi_w\)-modes smooth to \(e(\tfrac j2 n^{3/4})\) by
the Proposition L brick. The nontrivial modes are \(k \ne 0\):

**Step 1 (smoothing).** By the Corollary, the mode phase is
\(\varphi_1(n) - B(n)\theta_w(n)\) up to absorbable errors, with
\(\varphi_1 = \tfrac i2 n^{3/2} + \tfrac j2 n^{3/4} + \tfrac k2
n^{9/8}\) and \(B = \tfrac{3k}4 n^{3/8}\) (replacing \(m^{1/4}\) by
\(X^{1/4}\) costs \((3k/16)\theta X^{-3/4}\,\theta_w \ll
kn^{-9/8}\)).

**Step 2 (drift-1 intervals).** \(B' \asymp k n^{-5/8}\), so \(B\)
drifts by at most \(1\) on intervals \(I\) of length \(L_0 =
P^{5/8}/k\); there are \(\asymp k P^{3/8}\) of them. On \(I\), expand
\(e(-B\{U\}) = \sum_r a_r(B)\,e(rU)\) (Fourier in \(U\), Vaaler
truncation \(|r + B| \le T = P^{5/16}\), majorant error \(\ll L_0/T\)
per interval, \(P/T = P^{11/16}\) total). Coefficients:
\(|a_r(B)| \le \min(1, |r+B|^{-1})\), window mass \(O(\log T)\); the
\(n\)-dependence through \(B(n)\) has total variation
\(\sum_r \sup_I |a_r'|\,|B'|\,L_0 \ll \sum_r |r+B|^{-2} = O(1)\),
removed by partial summation once per mode.

**Step 3 (mode sums).** Each mode is \(\sum_{n\in I}
e(\varphi_1(n) + rU(n))\); smoothing \(rU \to r n^{3/4}\) costs
\(\tfrac r2\theta X^{-1/2}\) pointwise, \(\ll |r| P^{-3/4}\cdot L_0
\ll P^{1/4}\) per interval, \(kP^{5/8}\) total. Writing \(r = -B_0 +
t\), \(|t| \le T\):

\[
\varphi'' = \tfrac{27k}{128} n^{-7/8}
- \tfrac3{16}\bigl(t + \tfrac j2\bigr) n^{-5/4}
+ \tfrac{3i}8\, n^{-1/2}.
\]

For \(i \ne 0\) the first-listed scale is dominated: \(\lambda_2
\asymp |i| P^{-1/2}\), single-signed since \(|i|P^{-1/2} \ge
P^{-1/2}\) while the others are \(\le kP^{-7/8} + TP^{-5/4} \ll
P^{-3/4}\); van der Corput II over \(I\) and summation over intervals
give \(\ll i^{1/2}P^{3/4} + i^{-1/2}kP^{5/8}\). For \(i = 0\): the
\(t\)-term satisfies \(|t + j/2|\,P^{-5/4} \le (T + J_2)P^{-5/4} \ll
kP^{-7/8}\) because \(T = P^{5/16} \ll kP^{3/8}\) for every
\(k \ge 1\); hence \(\lambda_2 \asymp k n^{-7/8}\), single-signed.
Van der Corput II per interval: \(L_0\lambda_2^{1/2} +
\lambda_2^{-1/2} \ll k^{-1/2}(P^{3/16} + P^{7/16})\); times
\(kP^{3/8}\) intervals and \(O(\log)\) mode mass:

\[
S_k \;\ll\; k^{1/2} P^{13/16+\varepsilon} .
\]

**Assembly.** With Vaaler weights \(1/k\),
\(\sum_{k\le J_3} \tfrac1k\, k^{1/2} P^{13/16} = J_3^{1/2} P^{13/16}
= P^{7/8}\), balanced against the truncation error \(P/J_3 =
P^{7/8}\) at \(J_3 = P^{1/8}\). The \(i\)- and \(j\)-weighted sums
are smaller (\(\ll P^{3/4+\varepsilon}\)); absorbable inventory:
\(kP^{5/8} \le P^{3/4}\), \(P/T = P^{11/16}\), partial-summation
factors \(O(\log)\). Total \(\ll P^{7/8+\varepsilon}\); dyadic blocks
sum to \(N^{7/8+\varepsilon}\).

**OEE branch.** The fourth letter needs \(\psi(w^{1/2})\):
\(w^{1/2} = (U - \theta_w)^{1/2} = U^{1/2} - \tfrac12\theta_w
U^{-1/2} - \tfrac18\theta_w^2(U-\xi)^{-3/2}\) — *decaying* amplitudes
only, and \(U^{1/2} = m^{1/4} \to n^{3/8}\) likewise. Pure modes
\(e(\tfrac l2 n^{3/8})\): \(\lambda_2 \asymp l P^{-13/8}\), van der
Corput II gives \(l^{1/2}P^{3/16} + l^{-1/2}P^{13/16}\); the mixed
\(i, j\) cases sit in the dominance hierarchy \(iP^{-1/2} \gg
jP^{-5/4} \gg lP^{-13/8}\) with all three second derivatives of the
same sign (no cancellation). Total \(\ll N^{13/16+\varepsilon}\).
\(\square\)

Float sanity (`oeo_mode_probe`, exact scaled phases): \(|S| = 84.8,\
1361.0,\ 6142.3\) on \(5\cdot10^3, 5\cdot10^4, 5\cdot10^5\) terms —
tracking the *coherent-cell random-walk scale* \(P^{5/8}\) (\(1333,\
5623\) predicted at the two larger sizes), far below the proven
\(P^{7/8}\): the phase is constant on each \(w\)-cell of length
\(\asymp \tfrac43 P^{1/4}\), and the \(\asymp P^{3/4}\) cell phases
equidistribute.

### Remark (why the kernel does not appear)

The differencing-free route works because the sawtooth variable
\(\theta_w = \{m^{1/2}\}\) and its coefficient \(B \asymp kn^{3/8}\)
are *both slow*: \(B\) crosses integers every \(\asymp P^{5/8}/k\)
steps, so drift-1 intervals are long enough for the shifted-window
expansion, and the mode frequencies \(r \asymp kP^{3/8}\) keep the
curvature \(rP^{-5/4} \ll\) the main scale. In the OOO\* kernel the
coefficient \(W \asymp kn^{9/8}\) crosses integers *within single
steps* (\(W' \asymp kn^{1/8} \gg 1\)) — no drift-1 interval exists.
The boundary between the two regimes is exactly \(c' \asymp 1\),
i.e. coefficient scale \(n\): itinerary letters whose phase
coefficients grow slower than \(n\) are reachable by this engine;
OOO\* sits above the line.

### Remark (Proposition J needs only O-rooted words)

The word classes in Proposition J range over all starts, but every
E-rooted word has a contracting prefix at length 1 (\(3^0 < 2\)), so
E-rooted classes never enter the exceptional set: the hypothesis only
ever consumes O-rooted class bounds, which are exactly what Theorems
5.1/C/E/L/Q prove. No further gap.

## Part VI: the kernel — a double-differencing attack (Phase 8)

**Status: reviewed.** Drafted in Phase 8 and re-derived
adversarially in Phase 9 (review record after Theorem R). The review
found two defects — one organizational, one a real error in the
draft's Step 5 — and repaired both with the part's own exact
mechanisms; the final exponents are unchanged. Theorem R and its
depth-4 corollary (Theorem S) are `EXACT — HUMAN PROOF`
(ledger rows `J-kernel-cancellation`, `J-depth4-complete`). The
finite-dynamics note is *not* yet updated: its Conjecture 6.2
paragraph is superseded by this part and awaits an editorial
consolidation phase.

Notation: \(n\) odd, \(X = n^{3/2}\), \(m = \lfloor X\rfloor\),
\(\theta = X - m\), \(Y = m^{3/2}\), \(v = \lfloor Y\rfloor\),
\(\theta_2 = Y - v\). Shifts \(d_i = 2h_i\); corner values
\(f_{ab} = f(n + a d_1 + b d_2)\) for \(a, b \in \{0, 1\}\);
\(\Delta_1 f = f_{10} - f_{00}\), \(\Delta_2 f = f_{01} - f_{00}\),
\(\Delta\Delta f = f_{11} - f_{10} - f_{01} + f_{00}\). Gap
variables: \(g_1(n) = m(n{+}d_1) - m(n)\), \(g_2(n) = v(n{+}d_1) -
v(n)\), \(W(n) = \Delta_1 Y(n)\), \(j_1(n) = \Delta_2 g_1(n) =
\Delta\Delta m(n)\).

### Why Phase 5's wall does not block this route

Phase 5 recorded: *"a second A-process transfers the difference
either to \(v\) (reproducing gap terms carrying the full-size \(W\))
or to \(W\) (already exhausted at \(\Delta W\))."* Both recorded
failures difference a **sub-organization** of the OOO\* phase (the
\(vW\)-block of Proposition H). The attack below differences the
**whole kernel phase** \(c\,\theta_2\) twice and only then
decomposes. Three exact mechanisms, none available to the
sub-organized routes, then eliminate every full-size sawtooth
coefficient:

1. **integer annihilation** — whenever an integer-valued quantity
   \(g\) multiplies \(c\), the split \(e(cg) = e(\{c\}g)\) is never
   used; instead \(g\) is reduced (by the exact identities below) to
   *bounded* or *frozen* integers \(J\), and \(e(cJ)\) is a smooth
   phase — no fractional part of \(c\) ever enters;
2. **the level-2 numerology** \(Y'' \asymp P^{1/4} \gg 1 > P^{-3/4}
   \asymp Y'''\): one differencing leaves the level-2 gap content
   unfrozen, but a second freezes it — one extra differencing per
   unit of derivative growth;
3. **the branch split**: the level-1 second gap \(j_1\) is bounded
   and its flicker is carried by indicator weights (Vaaler modes with
   \(O(1)\) coefficients), never by the phase.

### Lemma R1 (kernel reformulation) — EXACT — HUMAN PROOF

For odd \(n \ge 5\),

\[
\tfrac12\bigl(m^{9/4} - v^{3/2}\bigr)
- \tfrac34\, v^{1/2}\theta_2 \;=\; R,
\qquad 0 \le R \le \tfrac3{16}\, v^{-1/2}.
\]

Consequently the central kernel phase \(c\,\theta_2\) with \(c =
\tfrac{3k}4 v^{1/2}\) equals \(\tfrac k2\bigl(Y^{3/2} - \lfloor
Y\rfloor^{3/2}\bigr)\) up to \(kR \ll kP^{-9/8}\): **the kernel is
the exponential sum of the level-2 local floor defect**, the
second-level analog of the note's local remainder calculus. (With
Lemma D, \(v^{1/2} = n^{9/8} + O(n^{-3/8})\), so the \(n^{9/8}\)- and
\(v^{1/2}\)-normalizations of the family differ by an absorbable
phase \(\ll kP^{-3/8}\) pointwise.)

*Proof.* Taylor of \((v + \theta_2)^{3/2}\) at \(v\): \(Y^{3/2} =
v^{3/2} + \tfrac32 v^{1/2}\theta_2 + \tfrac38 (v+\xi)^{-1/2}
\theta_2^2\) with \(\xi \in (0, \theta_2)\), and \(Y^{3/2} =
m^{9/4}\). \(\square\) Validated in exact scaled integers
(`kernel_reformulation_scan`): 1003/1003 odd samples through
\(n = 10^{12}+1\), remainder one-signed in the stated envelope.

### Lemma R2 (double-gap identity) — EXACT — HUMAN PROOF

For all \(n, h_1, h_2\),

\[
\Delta_2 g_2 \;=\; \bigl\lfloor \Delta\Delta Y \bigr\rfloor
+ \kappa''
+ \Delta_2 \kappa_2,
\]

where \(\kappa'' = \mathbb 1\bigl[\{W\} \ge 1 - \{\Delta\Delta
Y\}\bigr]\) and \(\kappa_2 = \mathbb 1\bigl[\theta_2 \ge 1 -
\{W\}\bigr]\) is Lemma N's carry. Every carry is a difference of
unit sawtooths: \(\mathbb 1[\{A\} + \{B\} \ge 1] = \lfloor A +
B\rfloor - \lfloor A\rfloor - \lfloor B\rfloor = \{A\} + \{B\} -
\{A + B\}\).

*Proof.* Lemma N twice: \(g_2 = \lfloor W\rfloor + \kappa_2\), and
the gap identity applied to the real sequence \(n \mapsto W(n)\)
with shift \(d_2\) gives \(\lfloor W_{01}\rfloor - \lfloor
W_{00}\rfloor = \lfloor \Delta_2 W\rfloor + \kappa''\) with
\(\Delta_2 W = \Delta\Delta Y\). The sawtooth form of the carry is
the Lean-verified `floor_add_eq_add_carry` rearranged. \(\square\)
Lean: `seq_floor_gap_second` in `GapCells.lean` (two instances of
`seq_floor_gap` composed). Validated on orbit data
(`double_gap_identity_check`): 400/400 at \(n \sim 10^6\) for
\((h_1, h_2) \in \{(1,1), (1,3), (2,5)\}\), 2980 matches + 20
guard-band skips on a wide window at \(n \sim 10^3\).

### Lemma R3 (branch decomposition and freeze) — EXACT — HUMAN PROOF

*(Restated by the Phase-9 review; see the review record.)* Write
\(b_1 = \lfloor\Delta_1X\rfloor\), \(b_2 = \lfloor\Delta_2X\rfloor\),
\(b_{12} = \lfloor\Delta_{12}X\rfloor\) (shift \(d_1 + d_2\)) — each
constant on runs of length \(\asymp P^{1/2}/h\) — and let
\(\boldsymbol\kappa = (\kappa_1, \kappa_2, \kappa_{12}) \in
\{0,1\}^3\) be the corresponding level-1 carries, so that \(m_{10} =
m + b_1 + \kappa_1\), \(m_{01} = m + b_2 + \kappa_2\), \(m_{11} = m +
b_{12} + \kappa_{12}\). Then on each \(b\)-run intersection and each
carry branch \(\boldsymbol\kappa\),

\[
\Delta\Delta Y \;=\; F_{\boldsymbol\kappa}(m), \qquad
F_{\boldsymbol\kappa}(m) = (m + b_{12} + \kappa_{12})^{3/2}
- (m + b_1 + \kappa_1)^{3/2} - (m + b_2 + \kappa_2)^{3/2} + m^{3/2}
\]

**exactly** (no error term). The net offset \(j = (b_{12} +
\kappa_{12}) - (b_1 + \kappa_1) - (b_2 + \kappa_2)\) is bounded
(\(|j| \le 3\) for \(h_1 h_2 \le P^{1/2}/3\)), and

\[
F_{\boldsymbol\kappa} \;\asymp\; \tfrac32 |j|\, P^{3/4}
+ h_1 h_2 P^{1/4},
\qquad
F_{\boldsymbol\kappa}'(m) \;\asymp\; |j|\, P^{-3/4}
+ h_1 h_2 P^{-5/4} \;<\; 1 .
\]

Hence on each branch the floor \(\lfloor
F_{\boldsymbol\kappa}(X(n))\rfloor\) is constant on runs of length
\(\asymp \min\bigl(P^{1/4}/|j|,\; P^{3/4}/(h_1 h_2)\bigr)\), and the
\(\theta\)-correction \(F(m) = F(X) - F'(\xi)\theta\) has sub-unit
amplitude. The branch indicator \([\boldsymbol\kappa = \cdot]\) is a
finite union of arcs in the single variable \(\theta\) with slowly
moving endpoints \(1 - \{\Delta_1X\}\), \(1 - \{\Delta_2X\}\), \(1 -
\{\Delta_{12}X\}\) (drifts \(\asymp hP^{-1/2} < 1\)): exactly
Theorem C's moving-endpoint expansion.

*Proof.* The corner identities are Lemma B at the three shifts. The
bound on \(j\): \(b_{12} - b_1 - b_2 \in \{0, 1\}\) up to
\(\lfloor\Delta\Delta X\rfloor\)-corrections with \(|\Delta\Delta X|
\le 4h_1h_2\sup|X''| = 3h_1h_2P^{-1/2}\). The derivative: MVT on the
second difference of \(\tfrac32 m^{1/2}\) plus \(\tfrac34 j
(m+\xi)^{-1/2}\). \(\square\) Validated (`branch_freeze_scan`):
distinct branch-floor counts match the drift prediction at \(P =
10^6, 10^8\) (e.g. at \(P = 10^8\), \((h_1,h_2)=(1,1)\): 2 distinct
values per cell against 2.8 predicted for offset \(\pm1\), exactly 1
for offset 0).

### Negative knowledge: the raw second gap is NOT frozen

\(\lfloor \Delta\Delta Y\rfloor\) itself has mean run length
\(1.5\) and jumps of size \(\tfrac32 P^{3/4} \approx 47\,900\) at
\(P = 10^6\) (`frozen`-scan falsifier, this phase): the level-1
flicker \(j_1\) shifts \(\Delta\Delta Y\) by \(\tfrac32 j_1 m^{1/2}\)
at essentially every step. A freeze argument ignoring the branch
split is dead on arrival; the branch organization of Lemma R3 is
forced, with the flicker carried by the \([j_1 = j]\) indicator —
level-1 carries, i.e. unit sawtooths of \(X\)-forms via Lemma R2's
sawtooth identity.

### Theorem R (kernel cancellation) — EXACT — HUMAN PROOF

Let \(c\) be smooth on \((P, 2P]\) with \(c^{(r)} \asymp k
P^{9/8 - r}\) for \(r = 0, 1, 2, 3, 4\), derivative signs following
the monomial pattern (the \(W\)-shaped family; e.g. \(c = \tfrac{3k}4
n^{9/8}\)). Then

\[
K_c(P) \;\ll\; P^{1 - \delta + \varepsilon},
\qquad
\delta = \tfrac1{64} \text{ for } k \ll P^{\varepsilon},
\qquad
\delta = \tfrac1{72} \text{ uniformly for } k \le P^{1/24}.
\]

*Proof (draft).*

**Step 1 (double Weyl differencing).** With \(H_1 = P^{a}\), \(H_2 =
P^{b}\) (chosen in Step 6),

\[
|K_c|^2 \ll \frac{P^2}{H_1} + \frac P{H_1}\sum_{h_1 \le H_1}
|T_1(h_1)|,
\qquad
|T_1|^2 \ll \frac{P^2}{H_2} + \frac P{H_2}\sum_{h_2 \le H_2}
|T_2(h_1, h_2)|,
\]

\(T_2 = \sum_n e(\varphi_2)\), \(\varphi_2 = \Delta\Delta(c\,
\theta_2) = \Delta\Delta(cY) - \Delta\Delta(cv)\) — the exact split
into a real-analytic block and an integer block.

**Step 2 (exact product rule).** For both blocks,

\[
\Delta\Delta(cf) \;=\; c_{11}\,\Delta\Delta f
+ (\Delta_2 c)(n{+}d_1)\,\Delta_1 f
+ (\Delta_1 c)(n{+}d_2)\,\Delta_2 f
+ (\Delta\Delta c)\, f .
\]

Scales: \(\Delta_i c \asymp k h_i P^{1/8}\), \(\Delta\Delta c
\asymp k h_1 h_2 P^{-7/8}\).

**Step 3 (the \(Y\)-block).** Work on cell intersections (count
\(O((h_1 + h_2) P^{1/2})\) cells). Within a cell every shifted
\(Y\)-value is a smooth function of the single variable \(m = X -
\theta\) (Lemma M and its shifted form), so no \(\Delta\theta\)
cross-terms arise:

- \((\Delta\Delta c)\,Y\): smooth part curvature \(\asymp
  k h_1 h_2 P^{-5/8}\); \(\theta\)-coefficient \(\tfrac32
  \Delta\Delta c\, X^{1/2} \asymp k h_1 h_2 P^{-1/8} < 1\)
  (constraint C1: \(k h_1 h_2 \le P^{1/8}\)) — expanded in Fourier
  modes of \(\theta\) at multiplicative mode-mass cost, not
  absorbed.
- \((\Delta_2 c)\,\Delta_1 Y\) and its mirror: \(\Delta_1 Y =
  (m{+}G_1)^{3/2} - m^{3/2}\) on the cell; \(\theta\)-coefficient
  \(\asymp \Delta_2 c \cdot G_1 X^{-1/2} \asymp k h_1 h_2 P^{-1/8} <
  1\); smooth curvature \(\asymp k h_1 h_2 P^{-5/8}\).
- \(c_{11}\,\Delta\Delta Y\): Lemma R3 branches. Per branch with
  net offset \(j\): smooth part \(c\,F_{\boldsymbol\kappa}(X)\) with
  curvature \(\asymp k|j| P^{-1/8} + k h_1 h_2 P^{-5/8} < 1\),
  combined per run with Step 4's frozen floor (Step 5(i));
  \(\theta\)-content \(c\,F'\,\theta\) with coefficient \(\asymp
  k|j| P^{3/8} + k h_1 h_2 P^{-1/8}\) and window drift \((c F')'
  \asymp k|j| P^{-5/8} < 1\): shifted-window expansion, then
  \(X\)-modes \(s \asymp k|j| P^{3/8}\) with curvature \(s X''
  \asymp k|j| P^{-1/8} < 1\), van der Corput II.

**Step 4 (the \(v\)-block).** \(v\) is an integer: no fractional
part of \(c\) is ever split off.

- \((\Delta\Delta c)\,v = (\Delta\Delta c)(Y - \theta_2)\): the
  \(Y\)-part as in Step 3; the \(\theta_2\)-part has coefficient
  \(\asymp k h_1 h_2 P^{-7/8} < 1\).
- \((\Delta_2 c)\,\Delta_1 v = \Delta_2 c\,(\lfloor W\rfloor +
  \kappa_2 - \kappa_2) = \Delta_2 c\,(W - \{W\})\) plus the Lemma-N
  carry: \(\Delta_2 c \cdot W\) is smooth-in-\(m\) per cell
  (curvature \(\asymp k h_1 h_2 P^{-5/8}\), \(\theta\)-coefficient
  \(\asymp k h_1 h_2 P^{-1/8}\)); \(-\Delta_2 c\,\{W\}\) has window
  drift \((\Delta_2 c)' \asymp k h_2 P^{-7/8} < 1\): \(W\)-modes
  \(r\) with \(|r| \lesssim k h_2 P^{1/8}\), each \(rW\) again
  smooth-in-\(m\) per cell (\(\theta\)-coefficient \(\asymp r h_1
  P^{-1/4} \le k h_1 h_2 P^{-1/8} < 1\), curvature \(\asymp k h_1
  h_2 P^{-5/8}\)). Carry factors \(e(\Delta_2 c\,\kappa_2) = 1 +
  \kappa_2 (e(\Delta_2 c) - 1)\): indicator weight times a smooth
  factor; \(\kappa_2 = \{Y\} + \{W\} - \{Y{+}W\}\) (Lemma R2's
  sawtooth identity) expands into unit sawtooths of \(Y\), \(W\),
  \(Y_{10}\) with \(O(1)\) coefficients — Vaaler windows \(|r| \le
  R\), \(R = P^{\rho}\), majorant error \(P/R\) per layer; the
  \(Y\)-modes linearize (Lemma M) to \(X\)-modes \(s \asymp R
  P^{3/4}\), curvature \(sX'' \asymp R P^{1/4} \gg 1\): pieces
  without a frozen-\(J\) factor take the **third**-derivative test
  over full ranges (\(\lambda_3 = s X''' \asymp R P^{-3/4} < 1\),
  saving \(P^{1/8}/R^{1/6}\)); pieces riding a frozen-\(J\) factor
  are the mixed class, Step 5(iii).
- \(c_{11}\,\Delta\Delta v = c_{11}\,\Delta_2 g_2\): Lemma R2. The
  factor \(e(-c \lfloor \Delta\Delta Y\rfloor)\) splits over Lemma
  R3 branches: per branch the frozen integer \(J = \lfloor
  F_{\boldsymbol\kappa}(X(n))\rfloor\) (boundary toggles are
  slow-sawtooth indicators in \(\{F(X)\}\) and \(\theta\)) combines
  with the \(c_{11}\Delta\Delta Y\)-content into the smooth per-run
  phase \(c(F - J)\), curvature \(\asymp k|j| P^{-1/8} + k h_1 h_2
  P^{-5/8} < 1\), single-signed per branch (Step 5(i)); van der
  Corput II per frozen run and summation over runs give \(\ll
  (k|j|)^{1/2} P^{15/16} + |j|^{3/2} k^{-1/2} P^{13/16}\) for \(j
  \ne 0\) and \(\ll (k h_1 h_2)^{1/2} P^{11/16} + (h_1 h_2 /
  k)^{1/2} P^{9/16}\) for \(j = 0\). The carries \(\kappa''\)
  (\(W\)-, \(\Delta W\)-content only: slow modes, Step 5(ii)) and
  \(\Delta_2\kappa_2\) (\(\theta_2\)-content: Step 5(iii)/(iv)) are
  indicator weights times \(e(\mp c)\) (curvature \(c'' \asymp k
  P^{-7/8}\), smooth).

**Step 5 (dominance and mode assembly — as repaired by the review).**
Final pieces fall into four classes.

- **(i) Pure smooth pieces**, \(\lambda_2 \asymp k h_1 h_2 P^{-5/8}\)
  or \(k|j| P^{-1/8}\) — van der Corput II; the leading curvature in
  each group is a genuine double difference of a single smooth
  function per run/branch (the \(c_{11}\Delta\Delta Y\)- and
  \(-c\lfloor\Delta\Delta Y\rfloor\)-contents combine per run to the
  smooth \(c\,(F_{\boldsymbol\kappa} - J)\)), so the double MVT gives
  a single-signed \(\lambda_2\): for the monomial-pattern family the
  composite sign check is \(\alpha(\alpha{-}1)(\alpha{+}\beta{-}2)
  (\alpha{+}\beta{-}3) > 0\) at \(\alpha = \tfrac98\) with \(\beta =
  \tfrac34\) (offset branches, \(cF \asymp k\,\mathrm{off}\,
  n^{15/8}\)) and \(\beta = \tfrac14\)-composites (zero-offset,
  \(cF \asymp kh_1h_2 n^{11/8}\)) — exponents \(\tfrac{15}8,
  \tfrac{11}8 \notin \{0,1,2\}\), no vanishing. Per-run van der
  Corput II is legitimate here because \(\lambda_2^{-1/2} \asymp
  P^{1/16} \ll P^{1/4} \asymp\) run length. Saving \(\ge
  P^{1/16}/(k|j|)^{1/2}\).
- **(ii) Slow-mode pieces** (\(W\)-, \(\Delta W\)-, \(F\)-, small
  \(u\)-modes, no \(\theta_2\)-content): van der Corput II over full
  ranges at the dominant scale; dominance is clean because the
  colliding scale \(s^* \asymp kP^{3/8}\) lies outside every window
  (centers \(\ge\) width by construction; \(u \le R' = P^{1/16} \ll
  kP^{3/8}\); the Theorem-Q separation check).
- **(iii) Mixed pieces** — a frozen-\(J\) factor times a large
  \(X\)-mode \(s \asymp rP^{3/4}\) spawned by the
  \(\theta_2\)-carries (\(\kappa_2\), \(\Delta_2\kappa_2\)): here
  van der Corput II fails (\(\lambda_2 \asymp rP^{1/4} \gg 1\)) and
  per-run III gives nothing (see the review record). Repair: one
  **targeted third Weyl differencing** (shift \(2h_3\), \(h_3 \le
  H_3\)) of the piece, then the split \(J = F - \{F\}\): the
  differenced coefficient \(\Delta_3 c \asymp k h_3 P^{1/8}\) has
  window drift \(\asymp k h_3 P^{-7/8} < 1\) against the *slow*
  sawtooth \(\{F(X)\}\) (drift \(\asymp P^{-1/4}\)), so the
  shifted-window expansion applies with no run segmentation;
  \(\Delta_3\lfloor F\rfloor = \lfloor\Delta_3F\rfloor + \text{carry}
  \in \{-1,0,1\} + \text{carry}\) is bounded (gap identity on \(F\),
  \(|\Delta_3F| \asymp h_3P^{-1/4}\cdot P^{1/2}\)-drift \(< 1\)) and
  its indicators are slow; and the differenced mode curvature
  \(s(\Delta_3X)'' \asymp r h_3 P^{-3/4} < 1\) is single-signed
  (\(X''' < 0\), \(s\)-sign fixed per window) and dominant
  (\(rP^{3/8} \gg k\)): van der Corput II over full ranges gives
  \((rh_3)^{1/2}P^{5/8}\), and balancing \(H_3 = r^{-1/3}P^{1/4}\)
  yields the piece bound \(r^{1/6}P^{1-1/8}\) — the same class-(iv)
  saving as below, so nothing is lost.
- **(iv) Carry-mode pieces without frozen-\(J\)**: \(X\)-modes
  \(|s| \le RP^{3/4}\), third-derivative test over full ranges,
  \(\lambda_3 = sX''' \asymp rP^{-3/4}\), saving
  \(P^{1/8}/r^{1/6}\).

Sub-unit sawtooths cost multiplicative mode-mass \(O(\log)\) only;
mode masses multiply over at most four expansion layers plus the
targeted differencing: \(P^{\varepsilon}\). Majorant truncations
\(P/R\). With \(R = P^{\rho}\), \(\rho = 1/16\): savings
\(P^{1/16}/(k|j|)^{1/2}\), \(P^{1/8 - \rho/6}\), and truncation
\(P^{-\rho}\) balance at

\[
|T_2| \;\ll\; P^{1 - 1/16 + \varepsilon}
\quad\text{under C1: } k h_1 h_2 \le P^{1/8},
\quad h_1 h_2 \le P^{1/2}/3 .
\]

**Step 6 (assembly).** \(\eta = 1/16\). With \(k \le P^{\kappa_0}\)
and \(a + b \le \tfrac18 - \kappa_0\) (C1): \(|K_c| \ll P\,
(P^{-a/2} + P^{-b/4} + P^{-\eta/4})\). For \(\kappa_0 =
\varepsilon\): \(a = \tfrac1{32}\), \(b = \tfrac1{16}\), \(\delta =
\tfrac1{64}\). For \(\kappa_0 = \tfrac1{24}\): \(a = \tfrac1{36}\),
\(b = \tfrac1{18}\), \(\delta = \tfrac1{72}\). Exponents
deliberately unoptimized. \(\square\)

Float support (`differenced_kernel_probe`, exact scaled phases):
\(|T_1| = 267{-}288\), \(|T_2| = 70{-}158\) on \(2.5\cdot10^4\)
terms and \(|T_1| = 300{-}567\), \(|T_2| = 436{-}686\) on
\(2.5\cdot10^5\) terms across \((h_1, h_2) \in \{(1,1), (1,2),
(2,3), (5,7)\}\); triple differences \(|T_3| = 132{-}164\) and
\(213{-}369\) at the same sizes across \((h_1,h_2,h_3) \in \{(1,1,1),
(1,2,3), (2,3,5)\}\) — square-root scale throughout, consistent with
every differenced level of the argument including the targeted third
differencing.

### Review record (Phase 9)

Every step re-derived adversarially. Two defects found; both
repaired with the part's own exact mechanisms; final exponents
unchanged.

1. **Organizational (Lemma R3 as drafted).** The draft conditioned
   on "cells with fixed \((G_1, G_2)\)". But the level-1 gaps are
   *two-valued* on each \(b\)-run — the carry \(\kappa_1(\theta)\)
   toggles at essentially every step — so those "cells" are wild
   sets and the branch indicator would not have admitted the
   moving-endpoint expansion. Repaired by restating R3 over
   \(b\)-run intersections and the carry vector \(\boldsymbol\kappa
   \in \{0,1\}^3\): the eight branch indicators are arcs in \(\theta\)
   with slow endpoints (Theorem C's Step-4 pattern). The exact
   identity, offset bounds, and freeze scales are unchanged; the
   Phase-8 validator already measured the sub-runs of the repaired
   organization.
2. **Real error (Step 5 as drafted).** For mixed pieces (frozen-\(J\)
   factor × large \(X\)-mode \(s \asymp rP^{3/4}\)) the draft
   implicitly used the third-derivative test per \(J\)-run of length
   \(P^{1/4}\). That fails: the test's second term \(M^{1/2}
   \lambda_3^{-1/6}\) summed over \(P^{3/4}\) runs is \(\asymp
   r^{-1/6}P\) — the trivial bound. Repaired by the targeted third
   Weyl differencing of Step 5(iii): after \(\Delta_3\), the
   \(J\)-content splits as \(J = F - \{F\}\) with the *slow* sawtooth
   \(\{F(X)\}\) (drift \(P^{-1/4}\)) against the *small* coefficient
   \(\Delta_3c\) (window drift \(kh_3P^{-7/8} < 1\)): shifted-window
   expansion with no run segmentation, full-range van der Corput II,
   and the class-(iv) saving \(P^{1/8}/r^{1/6}\) is recovered after
   balancing \(H_3\). Float support: the \(T_3\) probes above.

Also verified in the review: the collision inventory (the crossover
scale \(s^* \asymp kP^{3/8}\) lies outside every mode window; small
\(u\)-modes never reach it since \(R' = P^{1/16}\)); single-signed
leading curvatures per branch via the monomial exponent products
\(\tfrac{15}8, \tfrac{11}8 \notin \{0,1,2\}\); the family hypothesis
extended to \(r \le 4\) (used by the double MVT on \((cF)''\));
window drifts of all shifted expansions; the odd-\(n\)
reparameterization; \(k\)-uniformity of all constants; and the
boundary/majorant inventory (\(P/R\)-losses at \(\rho = 1/16\), run
and cell boundary counts \(\ll P^{3/4+\varepsilon}\)).

### Theorem S (the OOO\* splits — depth 4 complete) — EXACT — HUMAN PROOF

For \(w \in \{\mathrm{OOOE}, \mathrm{OOOO}\}\),

\[
\#\{\text{odd } n \le N : \text{word}_4(n) = w\}
= \tfrac N{16} + O\bigl(N^{1 - 1/72 + \varepsilon}\bigr),
\]

and hence **every** depth-\(\le4\) itinerary word class satisfies
\(\#\{n \le N\} = 2^{-|w|}N + O(N^{1-\delta_w})\) with explicit
\(\delta_w > 0\): depth-4 equidistribution is complete.

*Proof.* The class indicator expands (Vaaler, truncation \(J_3 =
P^{1/24}\), error \(P/J_3 = P^{1-1/24}\)) into mode sums \(S_{ijk} =
\sum_n e\bigl(\tfrac i2 X + \tfrac j2 Y + \tfrac k2 v^{3/2}\bigr)\)
over dyadic blocks. Proposition H rewrites \(\tfrac k2 v^{3/2}\) as a
polynomial in \((m, v)\) with smooth coefficients plus an absorbable
error. Its \(v\)-linear part is \(vW\) with \(W \asymp \tfrac{3k}4
n^{9/8}\) in the Theorem-R family; the \(vm\)- and \(vm^2\)-cross
terms reduce to the same family by \(\xi v m = \xi X\,v - \xi\theta
v\) and \(\xi_2 v m^2 = \xi_2X^2\,v - 2\xi_2X\theta\,v +
\xi_2\theta^2 v\), where \(\xi \asymp kn^{-3/8}\), \(\xi_2 \asymp
kn^{-15/8}\) make every \(\theta\)-cross coefficient sub-unit
(\(\xi X \asymp kP^{-3/8}\cdot P^{3/2}\cdot P^{-3/2}\theta\)-scale
\(< 1\)) and every smooth \(v\)-coefficient a family member
(\(\xi X, \xi_2X^2 \asymp kP^{9/8}\) with monomial-pattern
derivatives). Writing \(v = Y - \theta_2\) splits each family term
into a smooth-in-\(m\) part (Lemma M) and a kernel factor
\(e(-c\,\theta_2)\). The double differencing of Theorem R applied to
the whole mode phase carries the passengers along: the pure-\(m\)
polynomial phases difference into the Step-3 classes
(\((\Delta\Delta\mu)m\)-content sub-unit under C1, crosses smooth per
cell, \(\mu\,\Delta\Delta m\) = bounded-offset branch phases with
curvature \(\asymp k|j|P^{-1/8}\), single-signed by the same
monomial-exponent check); the \(\tfrac i2X\)- and \(\tfrac
j2Y\)-passenger phases difference to \(\tfrac i2\Delta\Delta X\)
(curvature \(\ll ih_1h_2P^{-5/2}\), subdominant) and \(\tfrac
j2F_{\boldsymbol\kappa}(m)\) (real-valued, no floor: smooth plus
sub-unit \(\theta\), curvature \(\asymp jP^{-5/4}\), subdominant in
the established hierarchy); and the kernel factor is handled by
Steps 2–5 verbatim. Assembly as in Theorem R and summation over
\(k \le J_3\) with \(1/k\)-weights give \(\sum_k \tfrac1k
P^{1-1/72} + P^{1-1/24} \ll P^{1-1/72+\varepsilon}\); dyadic blocks
sum to \(N^{1-1/72+\varepsilon}\). The \(i\)- and \(j\)-weighted
sums are no larger. \(\square\)

### Consequences

1. **Conjecture O / note Conjecture 6.2 is settled** (Theorem R) for
   the \(W\)-shaped family — the exact object every Phase-5
   reorganization funnels into — and the OOO\* splits close
   (Theorem S): Conjecture K holds unconditionally at every depth
   \(\le 4\), so the base cases \(d \le 4\) of Proposition J's
   hypothesis are theorems.
2. **The certified-descent density stays \(13/16\)** at four steps:
   the OOO\*-classes are non-contracting at depth 4 (\(3^3 > 2^4\)).
   What opens is depth \(\ge 5\), where OOO-prefixed contracting
   words (e.g. OOOEE, \(3^3 < 2^5\)) live: their closure needs the
   fifth-letter machinery, not attempted here.
3. **A tier ladder.** The engine used one differencing per unit of
   derivative growth (\(Y'' \gg 1 > Y'''\)). Deeper growing layers
   need one more differencing each, with \(\delta\) roughly halving
   per level and the same exact identities — the natural attack on
   depth-5 words, not attempted here.
4. **Editorial debt.** The finite-dynamics note still states
   Conjecture 6.2 as open with the \(13/16\)/OOO\*-kernel frontier
   figure; Sections 5–6 and the figure await a consolidation phase.

### Phase-8/9 decision

Phase 8: **PROMOTE** — draft written; falsifier fired once
(raw-freeze failure, recorded above) and was met by an exact
reorganization; validators and probes all passed.

Phase 9 (review): **PROMOTE** — every step re-derived; two defects
found and repaired (review record above); Theorem R and Theorem S
tagged `EXACT — HUMAN PROOF` (ledger rows `J-kernel-cancellation`
retagged, `J-depth4-complete` added); `kernel_bound_proved` and
`depth4_complete_proved` flipped. Depth 5 is taken up in Part VII.

## Part VII: the length-5 contracting splits — density \(7/8\) (Phase 10)

Scope: the two words that raise the certified-descent density above
\(13/16\). Neither is a third growing layer of kernel type.

- **OOOEE** (\(3^3<2^5\)): fifth letter even after OOOE. Decaying
  nestings plus one slow sawtooth of coefficient \(n^{3/16}<n\),
  carried as a tame passenger on Theorem S.
- **OOEOE** (\(3^3<2^5\)): fifth letter odd after OOEO. Lemma A′ at
  \(w=\lfloor v^{1/2}\rfloor\asymp n^{9/8}\) leaves a sawtooth of
  coefficient \(n^{9/16}<n\) — engine side of the Phase-6 line.
  No kernel.

The expanding siblings OOOEO and OOEOO come free with the same
splits. OOOO\* (fifth letter odd after four odds) has coefficient
\(\asymp n^{27/16}>n\) and is **not** attempted: that is a new
supercritical kernel, not this phase.

### Lemma T1 (OOOE\* fifth-letter smoothing) — EXACT — HUMAN PROOF

Let \(z=\lfloor v^{3/2}\rfloor\). For odd \(n\ge5\),

\[
z^{1/2}
= n^{27/16}-\tfrac98 n^{3/16}\,\theta+D_5,
\qquad
|D_5|\le\tfrac34 m^{-3/8}+\tfrac12 v^{-3/4}+\tfrac9{128}n^{-7/16}.
\]

*Proof.* Three one-signed Taylor steps:
\(z^{1/2}=(v^{3/2}-\theta_z)^{1/2}=v^{3/4}-\tfrac12\theta_z v^{-3/4}
+O(v^{-9/4})\);
\(v^{3/4}=(m^{3/2}-\theta_2)^{3/4}=m^{9/8}-\tfrac34\theta_2 m^{-3/8}
+O(m^{-15/8})\);
\(m^{9/8}=(X-\theta)^{9/8}=n^{27/16}-\tfrac98\theta n^{3/16}
+\tfrac9{128}\theta^2(X-\xi)^{-7/8}\).
The \(\theta_z\) and \(\theta_2\) amplitudes decay
(\(v^{-3/4}\asymp n^{-27/32}\), \(m^{-3/8}\asymp n^{-9/16}\)).
\(\square\) Validated (`oooee_smoothing_scan`) through
\(n=10^{12}\). The remaining sawtooth has coefficient
\(\asymp kn^{3/16}<n\), derivative \(\asymp kn^{-13/16}\ll1\), so
drift-1 intervals of length \(\asymp P^{13/16}/k\) exist.

### Lemma T2 (OOEO\* fifth-letter linearization) — EXACT — HUMAN PROOF

Let \(w=\lfloor v^{1/2}\rfloor\), \(\theta_w=\{v^{1/2}\}\). For odd
\(n\ge5\),

\[
w^{3/2}
= n^{27/16}-\tfrac98 n^{3/16}\,\theta
-\tfrac32 v^{1/4}\,\theta_w+D_5',
\]

with \(D_5'\) decaying (\(|D_5'|\le\tfrac34 m^{-3/8}
+\tfrac38(U-1)^{-1/2}\), \(U=v^{1/2}\)).

*Proof.* Lemma A′ at base \(U\): \(w^{3/2}=v^{3/4}
-\tfrac32 v^{1/4}\theta_w+E\), \(0\le E\le\tfrac38(U-1)^{-1/2}\).
The \(v^{3/4}\to n^{27/16}\) chain is Lemma T1's second and third
steps. \(\square\) Validated (`ooeoe_smoothing_scan`) through
\(n=10^{12}\). Two engine sawtooths: coefficient \(n^{3/16}\) on
\(\theta\) and \(n^{9/16}\) on \(\theta_w\); both grow slower than
\(n\).

### Theorem T (the length-5 contracting splits) — EXACT — HUMAN PROOF

\[
\#\mathrm{OOOEE}(N),\;\#\mathrm{OOOEO}(N)
=\tfrac N{32}+O\bigl(N^{1-1/72+\varepsilon}\bigr),
\qquad
\#\mathrm{OOEOE}(N),\;\#\mathrm{OOEOO}(N)
=\tfrac N{32}+O\bigl(N^{43/48+\varepsilon}\bigr).
\]

*Proof.*

**OOOE\*.** Indicator algebra: OOOE\(*\) is the Theorem-S class
indicator times \(\tfrac12(1\pm\psi(z^{1/2}))\), branch-consistent
because after OOOE the image \(z=J^3(n)\) is even, so the fifth
letter is the even-branch value \(\lfloor\sqrt z\rfloor\) —
machine-checked (`oooee_indicator_identity_check`). Vaaler-expand
the fifth wave at truncation \(J_5=P^{1/24}\). Lemma T1 replaces
\(\tfrac l2 z^{1/2}\) by \(\tfrac l2 n^{27/16}
-\tfrac{9l}{16}n^{3/16}\theta\) at absorbable decaying cost.
The \(\theta\)-sawtooth has coefficient \(C\asymp l P^{3/16}<P\);
its shifted-window expansion (drift-1 length \(P^{13/16}/l\),
window \(T=P^{1/8}\ll l P^{3/16}\) for every \(l\ge1\)) produces
\(X\)-modes of size \(\asymp l P^{3/16}\), which are ordinary
first-letter passengers of Theorem S (strictly smaller than the
\(i\le P^{1/24}\) budget already carried). The smooth chirp
\(e(\tfrac l2 n^{27/16})\) has curvature \(\asymp l P^{-5/16}\),
subdominant to every retained Theorem-S scale. Theorem S therefore
applies verbatim and gives \(N/32+O(N^{1-1/72+\varepsilon})\).

**OOEO\*.** Indicator: \(\mathrm{OOEO}\ast
=\tfrac1{16}(1-\psi(m))(1+\psi(v))(1-\psi(w))
(1\pm\psi(w^{3/2}))\), branch-consistent on the OOEO cylinder
(`ooeoe_indicator_identity_check`). Vaaler-expand the four waves.
The \(k=0\) cases are Theorem E. For \(k\ne0\), Lemma T2 writes
the fifth-letter phase as \(\tfrac k2 n^{27/16}-C\theta-B\theta_w\)
with \(B=\tfrac{3k}4 v^{1/4}\asymp k n^{9/16}\) and
\(C=\tfrac{9k}{16}n^{3/16}\).

Expand \(e(-B\theta_w)=e(-B\{v^{1/2}\})\) on drift-1 intervals of
length \(L_B=P^{7/16}/k\) (there are \(\asymp k P^{9/16}\) of
them; \(B'\asymp k n^{-7/16}\)). Window \(T_w=P^{1/4}\ll
k P^{9/16}\) for every \(k\ge1\); majorant \(P/T_w=P^{3/4}\).
At frequency \(\ell=-B+t\), \(|t|\le T_w\), the combined phase
is \(-\tfrac k4 v^{3/4}+t\,v^{1/2}\) plus passengers. Linearizing
\(v^{3/4}\) and \(v^{1/2}\) by Lemmas T1/T2, the \(\theta\)
coefficients from the two expansions cancel at the window centre
up to a residual \(C_{\mathrm{net}}\asymp k n^{3/16}\). One slow
\(\theta\)-sawtooth remains.

Expand \(e(-C_{\mathrm{net}}\theta)\) on the same intervals
(\(C_{\mathrm{net}}\) drifts by \(P^{-3/8}\ll1\) on each \(I\);
window \(T_\theta=P^{1/8}\ll k P^{3/16}\); majorant \(P^{7/8}\)).
The resulting smooth phase has curvature
\[
\lambda_2
=\Bigl(-\tfrac{297k}{1024}+\tfrac{27k}{128}+O(T_w P^{-7/8})
+O(JP^{-1/2})\Bigr)n^{-5/16}
\asymp k\,n^{-5/16},
\]
single-signed: the two leading coefficients are
\(-0.290k+0.211k=-0.079k\neq0\), and the \(t\)- and \(i\)-errors
are \(O(P^{-5/8})\) and \(O(P^{-3/8})\). Van der Corput II on
each \(I\): \(L_B\lambda_2^{1/2}+\lambda_2^{-1/2}
\ll k^{-1/2}P^{21/32}\). Times \(k P^{3/16}\) intervals:
\(S_k\ll k^{1/2}P^{27/32+\varepsilon}\). Balance
\(J_5^{1/2}P^{27/32}=P/J_5\) at \(J_5=P^{5/48}\) gives
\(P^{43/48}\). Dyadic blocks sum to
\(N^{43/48+\varepsilon}\). \(\square\)

Float sanity: `oooee_mode_probe` / `ooeoe_mode_probe` at
\(P=10^4\) give \(|S|=16.3\) on \(636\) OOOE terms and
\(|S|=32.5\) on \(618\) OOEO terms — far below the cylinder
size. Depth-5 census at \(N=10^5\): the four classes lie in
\([3138,3181]\) against \(3125\).

### Corollary U (certified-descent density \(7/8\)) — EXACT — HUMAN PROOF

The class of starts carrying a uniform power-envelope descent
certificate of length at most five — evens, OE, OOEE, OOOEE,
OOEOE — has natural density \(7/8\). Each of OOOEE and OOEOE
has cardinality \(N/32+O(N^{43/48+\varepsilon})\), and
\(3^3<2^5\) forces \(J^5(n)<n\) on both words for \(n\ge2\).

*Proof.* Densities \(\tfrac12+\tfrac14+\tfrac1{16}+\tfrac1{32}
+\tfrac1{32}=\tfrac78\). The new cylinders are Theorem T. The
contraction is Corollary 2.3 of the finite-dynamics note
(\(3^3=27<32=2^5\)). \(\square\)

This is the first increment past the one-growing-layer ceiling of
Proposition I. The leftover \(1/8\) is the expanding length-5
tree OOEOO \(\cup\) OOOEO \(\cup\) OOOO\*. Of those, OOEOO and
OOOEO are now *counted* (Theorem T) and still do not contract;
OOOO\* is uncounted and supercritical.

### Phase-10 decision

**PROMOTE.** Both contracting length-5 words close under the
existing engine: OOOEE is a tame passenger on Theorem S, OOEOE
is a Theorem-Q argument at coefficient \(n^{9/16}\). Certified
density moves \(13/16\to7/8\). No new kernel, no note import,
no all-depth claim. The next mathematical question is whether
the OOOO\* fifth letter (coefficient \(n^{27/16}>n\)) admits a
scale-invariant extension of Theorem R, which is the first
rung of a Terras induction; that is a different phase.

## Part VIII: the OOOO\* kernel — isolation (Phase 11)

Scope: name the supercritical fifth-letter object and decide
whether Theorem R's numerology iterates. No bound, no density
claim, no triple-differencing draft.

Notation as in Part VI, plus \(Z = v^{3/2}\), \(z = \lfloor Z\rfloor\),
\(\theta_3 = Z - z\). After four odds the fifth letter is the
parity of \(\lfloor z^{3/2}\rfloor\). Branch consistency is
machine-checked (`oooo_indicator_identity_check`).

### Lemma V1 (level-3 kernel reformulation) — EXACT — HUMAN PROOF

For odd \(n \ge 5\),

\[
\tfrac12\bigl(v^{9/4} - z^{3/2}\bigr)
- \tfrac34\, z^{1/2}\theta_3 \;=\; R_3,
\qquad
0 \le R_3 \le \tfrac3{16}\, z^{-1/2}.
\]

Consequently the central kernel phase \(c\,\theta_3\) with
\(c = \tfrac{3k}4 z^{1/2}\) equals \(\tfrac k2\bigl(Z^{3/2} -
\lfloor Z\rfloor^{3/2}\bigr)\) up to \(k R_3 \ll k n^{-27/16}\):
**the OOOO\* kernel is the exponential sum of the level-3 local
floor defect**, Lemma R1 with \((m,v)\) replaced by \((v,z)\).
Since \(z \asymp n^{27/8}\), the coefficient is
\(c \asymp k n^{27/16} > n\).

*Proof.* Taylor of \((z + \theta_3)^{3/2}\) at \(z\):
\(Z^{3/2} = z^{3/2} + \tfrac32 z^{1/2}\theta_3 +
\tfrac38 (z+\xi)^{-1/2}\theta_3^2\) with \(\xi \in (0,\theta_3)\),
and \(Z^{3/2} = v^{9/4}\). \(\square\) Validated in exact scaled
integers (`level3_reformulation_scan`): odd samples through
\(n = 10^{12}+1\), remainder one-signed in the stated envelope.

### Kernel (definition)

For smooth \(c\) with \(c \asymp k P^{27/16}\) and
\(c' \asymp k P^{11/16}\) on \(n \sim P\) (the \(z^{1/2}\)-shaped
family),

\[
K_3(P) \;=\; \sum_{\substack{n \sim P \\ n\ \mathrm{odd}}}
e\bigl(c(n)\,\{\lfloor\lfloor n^{3/2}\rfloor^{3/2}\rfloor^{3/2}\}
\bigr).
\]

This is the \(W\)-family of Theorem R with one extra nesting:
coefficient \(\alpha = 27/16\) in place of \(9/8\).

### Smooth numerology iterates

The smooth model \(G(n) = n^{27/8}\) (replacing every floor by
the real power) has

\[
G''' \asymp P^{3/8} \gg 1 > P^{-5/8} \asymp G^{(4)}.
\]

Theorem R used \(Y'' \asymp P^{1/4} \gg 1 > P^{-3/4} \asymp Y'''\)
and two Weyl steps. The same "one extra differencing per unit of
derivative growth" therefore predicts **three** Weyl steps here.
This is the scale-invariant pattern *of the smooth model*, not
of the nested floors. Phase 12 (Part IX) shows the prediction
does not descend: there are no \(v\)-level \(b\)-runs, and the
forced inner linearization produces a \(W\)-family at
\(\alpha = 45/16 > 9/4\).

Closed form only; the derivatives are elementary. A float check
of \(n^{27/8}\) at \(P = 10^4\) matches \(G'''\) and \(G^{(4)}\)
to relative error \(< 1\%\).

### Negative knowledge: raw \(\Delta^4 Z\) is not frozen

The discrete \(Z = v^{3/2}\) inherits jumps from both inner
floors. At \(P = 10^4, 10^5, 10^6\), the mean
\(|\Delta^3 Z|\) is \(10^4\)–\(10^7\) times the smooth
\(G'''\), and \(|\Delta^4 Z|\) is \(10^8\)–\(10^{11}\) rather
than \(\ll 1\) (`level3_raw_gap_wildness`). A freeze argument
that ignores the nested carry lattice — level-1 carries of
\(m = \lfloor n^{3/2}\rfloor\) and level-2 carries of
\(v = \lfloor m^{3/2}\rfloor\) — is dead on arrival. This is
the Phase-8 raw-freeze falsifier one layer up, recorded now so
it is not rediscovered as a "new" obstruction.

The branch set is a *product* of two Lemma-R3 lattices, not a
copy of Lemma R3. The inner variable \(v\) jumps by
\(\asymp n^{5/4}\) per step of \(n\). Inherited Phase-5 dead
routes (composed Lemma-B cells, the swap
\(e(c\theta_3) = e(cZ)\,e(-\{c\}z)\), a second A-process on
\(z^{3/2}\), fibre + van der Corput II, shifted-window Vaaler
on a full-size sawtooth) remain dead; they were not retested.

### Float support

Exact scaled phases (`level3_kernel_probe`,
\(c = \tfrac34 z^{1/2}\)): \(|K_3| = 30.1,\ 59.5,\ 423.7\) on
\(2.5\cdot10^3,\ 2.5\cdot10^4,\ 10^5\) terms — square-root
scale (predicted \(\sqrt N = 50,\ 158,\ 316\)). On the OOOO
cylinder at \(P = 10^5\): \(|K_3| = 59.1\) on \(6207\) terms
(\(\sqrt N = 79\)). Differenced probes at \(P = 2\cdot10^4\):
\(|T_1| = 182\), \(|T_2| = 47\), \(|T_3| = 62\) on \(10^4\)
terms (\(\sqrt N = 100\)).

### What a bound would *not* do

Even a power-saving bound on \(K_3\) at depth 5 only *counts*
OOOOE and OOOOO. Neither contracts:
\(3^4 = 81 > 32 = 2^5\). Certified descent stays \(7/8\).
The first OOOO-prefixed contractor is OOOOEEE
(\(81 < 128 = 2^7\)), a length-7 word, not this phase.

A saving \(\delta\) that halves per extra nesting
(\(1/72 \to 1/144 \to \cdots\)) does **not** feed the
Hoeffding argument of Proposition J at all depths. Terras
still needs \(\delta\) uniform in the depth or at least
\(\ge c/d^2\). Isolation of \(K_3\) is the first rung of
that program, not the program.

### Conjecture V (level-3 kernel cancellation)

\(K_3(P) \ll P^{1-\delta}\) for some \(\delta > 0\), uniformly
over the \(z^{1/2}\)-shaped family \(c \asymp k P^{27/16}\),
\(k \le P^{\varepsilon}\). Supported by the probe; not claimed.

### Phase-11 decision

**PROMOTE** the isolation. Lemma V1 is exact; the object is
named; the smooth numerology iterates; the probe cancels; the
raw-freeze route is recorded dead; no new unnamed wild sum
appeared. The bound is a different phase: it must show that
the *product* of the two carry lattices still kills every
full-size sawtooth coefficient, or exhibit a new wall.

`depth5_kernel_isolated` flipped; `depth5_kernel_bound_proved`
and `density_one_claimed` stay `False`. No ledger row (no
bound, no density increment). No note import. The
scale-invariant copy is taken up — and refuted — in Part IX.

## Part IX: the \(v\)-level wall (Phase 12)

Scope: the Phase-11 question — does the product of the two
carry lattices still kill every full-size sawtooth in \(K_3\),
or is there a new wall at the \(v\)-level? Answer: a new wall.
No bound draft.

### Lemma V2 (forced inner linearization) — EXACT — HUMAN PROOF

For odd \(n \ge 5\),

\[
v^{3/2}
= m^{9/4} - \tfrac32 m^{3/4}\,\theta_2 + E_2,
\qquad
0 \le E_2 \le \tfrac38\, v^{-1/2}.
\]

*Proof.* Taylor of \((Y - \theta_2)^{3/2}\) at \(Y\):
\(v^{3/2} = Y^{3/2} - \tfrac32 Y^{1/2}\theta_2 +
\tfrac38 (Y-\xi)^{-1/2}\theta_2^2\) with \(\xi \in (0,\theta_2)\),
\(Y^{3/2} = m^{9/4}\), \(Y^{1/2} = m^{3/4}\), and
\(Y - \xi \ge v\). \(\square\) Validated
(`level3_inner_linearization_scan`) through \(n = 10^{12}+1\).

Restoring the outer coefficient \(c \asymp k z^{1/2}
\asymp k n^{27/16}\) of Lemma V1, the phase \(c\,v^{3/2}\)
splits as a smooth chirp \(c\,m^{9/4}\) minus the \(W\)-family
phase \(C\,\theta_2\) with

\[
C = \tfrac{3c}2 m^{3/4} \asymp k n^{45/16},
\]

plus a remainder phase \(c E_2 \asymp k n^{9/16}\theta_2^2\)
(engine-side: coefficient \(< n\), derivative
\(\asymp n^{-7/16} < 1\)). The remainder is not the wall.
The main term is.

This linearization is forced if \(Z = v^{3/2}\) is to become
smooth in \(m\). Not linearizing leaves \(Z\) as a function of
the integer \(v = \lfloor Y\rfloor\), which is the other dead
route below.

### Proposition W (no \(v\)-level cells; \(\alpha = 45/16\) past the engine line) — EXACT — HUMAN PROOF / REFUTED method

Two independent deaths of "copy Theorem R one nesting up."

**(i) No \(b\)-runs.** Theorem R segments on runs where
\(\lfloor\Delta X\rfloor\) is constant, of length
\(\asymp P^{1/2}/h\). The \(v\)-level analogue is runs of
\(\lfloor\Delta Y\rfloor\) or of \(\Delta v\). But
\(Y' \asymp P^{5/4}\) and \(Y'' \asymp P^{1/4} \gg 1\), so
\(\lfloor\Delta Y\rfloor\) changes at every step of \(n\).
Measured (`v_level_cell_scan`): mean and max run length \(1\)
at \(P = 10^4, 10^5, 10^6\), both for \(\lfloor\Delta Y\rfloor\)
and for \(\Delta v\). Lemma R3 cannot be restated at the
\(v\)-level: its cells have length \(1\).

**(ii) The forced \(W\)-family is past the engine line.**
For a \(W\)-family \(e(C\theta_2)\) with \(C \asymp k P^{\alpha}\),
Theorem R's Step-3 \(\theta\)-coefficient of \((\Delta\Delta C)\,Y\)
is \(\asymp k h_1 h_2 P^{\alpha - 5/4}\). This is

- sub-unit (R's constraint C1) iff \(\alpha \le 5/4\),
- engine-treatable (coefficient \(< P\) and derivative \(< 1\))
  iff \(\alpha < 9/4\).

Lemma V2 produces \(\alpha = 45/16 = 2.8125 > 9/4\). The spawned
\(\theta\)-sawtooth then has coefficient
\(\asymp k h_1 h_2 P^{25/16} > P\) and derivative
\(\asymp k h_1 h_2 P^{9/16} \gg 1\): a unit sawtooth whose
coefficient exceeds \(n\) and which crosses integers within
single steps. That is the Phase-5 wall, at a larger scale.

The two Phase-11 routes therefore die by recorded mechanisms,
not by a new unnamed sum:

- copy R with \((X,m,Y,v)\mapsto(Y,v,Z,z)\): dies by (i);
- linearize through the inner floor, then invoke R: dies by (ii).

Inherited Phase-5 dead routes (composed Lemma-B cells, the
swap \(e(c\theta_3)=e(cZ)\,e(-\{c\}z)\), a second A-process
on \(z^{3/2}\)) remain dead and were not retested.

### What this does *not* refute

Conjecture V — that \(K_3\) itself cancels — is untouched.
The Phase-11 probe still shows square-root cancellation.
What is refuted is the *method*: a scale-invariant copy of
Theorem R with \(\delta(\alpha)\) read off from the smooth
model \(G(n)=n^{27/8}\). The smooth numerology of Part VIII
is correct as a statement about \(n^{27/8}\) and false as a
statement about \(\{\lfloor Y\rfloor^{3/2}\}\).

A bound on \(K_3\) would still not raise certified descent
at depth 5, and a \(\delta\) that halves per nesting would
still not give Terras. The new information is sharper:
the engine/kernel line of the \(W\)-family is \(\alpha = 9/4\)
for R's own Step-3 bookkeeping, and the first supercritical
OOOO\* coefficient already overshoots it.

### Phase-12 decision

**PROMOTE** the obstruction. Lemma V2 is exact; the missing
\(v\)-level cells are measured; the \(\alpha = 45/16\) wall
is the Phase-5 object at a named larger scale. The
scale-invariant R-extension is **REFUTED** (ledger row
`J-scale-invariant-R-extension`). Conjecture V stays a
conjecture; `depth5_kernel_bound_proved` and
`density_one_claimed` stay `False`.
`scale_invariant_R_extension_refuted` flipped. No note
import, no density claim, no rescue draft. The Terras
increment that does *not* need \(K_3\) is taken up in Part X.

## Part X: the length-7 engine contractors — density \(57/64\) (Phase 13)

Scope: the two leftover words that contract at length 7
*without* meeting \(K_3\). The third length-7 contractor
OOOOEEE still needs the OOOO\* split and is not attempted.

- **OOEOOEE** (\(3^4<2^7\)): sixth letter after the Theorem-T
  class OOEOO. The naive \(\theta_w\)-coefficient
  \(n^{45/32}>n\) rearranges (Lemma X1, the A′ pattern) into
  an integer-\(w\) block whose first gap freezes on runs of
  length \(\asymp P^{7/8}\), plus a \(W\)-family at
  \(\alpha=33/32<9/8\) (Corollary R′) and engine sawtooths.
- **OOOEOEE** (\(3^4<2^7\)): Lemma A′ at
  \(s=\lfloor z^{1/2}\rfloor\), same coefficient budget.

### Corollary R′ (\(W\)-family for \(\alpha\le 9/8\)) — EXACT — HUMAN PROOF

Theorem R's bound \(K_c(P)\ll P^{1-1/72+\varepsilon}\) holds
for every monomial family \(c^{(r)}\asymp k P^{\alpha-r}\)
with \(0<\alpha\le 9/8\) and the same sign pattern, uniformly
for \(k\le P^{1/24}\).

*Proof.* Every constraint in the Phase-9 proof of Theorem R
is monotone in \(\alpha\) on \((0,9/8]\): C1 becomes
\(k h_1 h_2\le P^{5/4-\alpha}\), which is weaker than
\(P^{1/8}\) as \(\alpha\) drops; every curvature and window
drift shrinks; the mixed-piece third differencing has smaller
modes. Sign-dominance
\(\alpha(\alpha-1)(\alpha+\beta-2)(\alpha+\beta-3)>0\) holds
at \(\beta\in\{1/4,3/4\}\) throughout the interval (both
factors \(\alpha+\beta-2\) and \(\alpha+\beta-3\) stay
negative, the first two stay positive). The assembly
exponents of Step 6 only improve. The case \(\alpha=33/32\)
used below is an instance. \(\square\)

### Lemma X1 (OOEOO\* sixth-letter rearrangement) — EXACT — HUMAN PROOF

Let \(w=\lfloor v^{1/2}\rfloor\), \(p=\lfloor w^{3/2}\rfloor\),
\(\theta_p=\{w^{3/2}\}\). For odd \(n\ge5\),

\[
p^{3/2}
= -\tfrac54 v^{9/8} + \tfrac94 w\, v^{5/8}
- \tfrac32 w^{3/4}\,\theta_p + E_X,
\]

with \(0\le E_X\le \tfrac38 p^{-1/2} + \tfrac{45}{32} v^{1/8}\).

*Proof.* Taylor of \((w^{3/2}-\theta_p)^{3/2}\) at \(w^{3/2}\)
gives \(p^{3/2}=w^{9/4}-\tfrac32 w^{3/4}\theta_p+E_p\). Taylor
of \((v^{1/2}-\theta_w)^{9/4}\) at \(v^{1/2}\) gives
\(w^{9/4}=v^{9/8}-\tfrac94 v^{5/8}\theta_w+E_w\). The identity
\(\theta_w=v^{1/2}-w\) rearranges the middle term:
\(v^{9/8}-\tfrac94 v^{5/8}(v^{1/2}-w)
=-\tfrac54 v^{9/8}+\tfrac94 w\,v^{5/8}\). \(\square\)
Validated (`sixth_ooeoo_scan`) through \(n=10^{12}+1\).

The naive coefficient \(\tfrac94 v^{5/8}\asymp n^{45/32}>n\)
of \(\theta_w\) is gone. Remaining sawtooth \(\theta_p\) has
coefficient \(n^{27/32}<n\), derivative \(n^{-5/32}<1\).

### Lemma X2 (OOOEO\* sixth-letter A′) — EXACT — HUMAN PROOF

Let \(z=\lfloor v^{3/2}\rfloor\), \(s=\lfloor z^{1/2}\rfloor\).
For odd \(n\ge5\),

\[
s^{3/2}
= -\tfrac12 z^{3/4} + \tfrac32 s\, z^{1/4} + E,
\qquad
0\le E\le\tfrac38(U-1)^{-1/2},\quad U=z^{1/2}.
\]

*Proof.* Lemma A′ at base \(U=z^{1/2}\). \(\square\)
Validated (`sixth_oooeo_scan`) through \(n=10^{12}+1\).

### Lemma X3 (\(w\)-gap freeze) — EXACT — HUMAN PROOF

On the OOEO cylinder, \(U=v^{1/2}\) has
\(U''\asymp P^{-7/8}<1\), so \(\lfloor\Delta U\rfloor\) is
constant on runs of length \(\asymp P^{7/8}/h\). The integer
gap \(\Delta w=\lfloor\Delta U\rfloor+\kappa_w\) is a frozen
floor plus a 0/1 carry. Measured (`w_gap_freeze_scan`): a
single run covers a window of \(400\) OOEO terms at
\(P=10^4,10^5,10^6\).

### Theorem X (the length-7 engine splits) — EXACT — HUMAN PROOF

\[
\#\mathrm{OOEOOEE}(N),\;\#\mathrm{OOEOOEO}(N),\;
\#\mathrm{OOEOOOE}(N),\;\#\mathrm{OOEOOOO}(N)
=\tfrac N{128}+O\bigl(N^{43/48+\varepsilon}\bigr),
\]
and the same bound for the four OOOEO\*\* words.

*Proof.*

**OOEOO\*\*.** Indicator: the Theorem-T class OOEOO times
\(\tfrac12(1\pm\psi(p^{3/2}))\tfrac12(1\pm\psi(q^{1/2}))\),
branch-consistent (`ooeooee_indicator_identity_check`).
Vaaler-expand the new waves. Lemma X1 writes the sixth-letter
phase as a smooth function of \((v,w)\) minus an engine
\(\theta_p\)-sawtooth. Expand \(v^{9/8}\) and \(v^{5/8}\) by
Lemma A/M:

- first-letter content of \(m^{27/16}\) is a chirp
  \(e(C n^{3/2})e(-C m)\) with \(C\asymp n^{33/32}\),
  curvature \(\asymp n^{17/32}\), van der Corput II;
- \(\theta_2\)-content of \(w\,m^{-1/16}\) has coefficient
  \(\asymp n^{33/32}\), a \(W\)-family with
  \(\alpha=33/32<9/8\), Corollary R′;
- remaining \(\theta_2\)-amplitudes are \(O(n^{9/32})\),
  engine;
- the integer block \(e(\xi w)\) with
  \(\xi\asymp n^{45/32}\) is handled on the frozen
  \(\lfloor\Delta U\rfloor\)-runs of Lemma X3: per run
  \(\Delta w=J+\kappa_w\) with \(J\) frozen, \(e(\xi J)\) a
  smooth chirp, \(\kappa_w\) an indicator weight (Theorem Q
  / R3 pattern at the \(w\)-level);
- \(\theta_p\) expands on drift-1 intervals of length
  \(P^{5/32}\), window \(T\ll P^{27/32}\), producing
  \(X\)-modes smaller than Theorem T's budget.

The seventh letter is the even-branch square root of
\(q=\lfloor p^{3/2}\rfloor\): decaying amplitudes (Lemma D
one level up). Theorem T therefore applies as a passenger
theorem and gives \(N/128+O(N^{43/48+\varepsilon})\).

**OOOEO\*\*.** Lemma X2 plus the \(z^{3/4}\to n^{81/32}\)
chain of Lemma T1 (raised to the \(3/2\)): the same four
classes of terms (chirp, \(W\)-family at \(33/32\), engine
sawtooths, integer-\(s\) block with
\(\lfloor\Delta z^{1/2}\rfloor\)-runs of length
\(\asymp P^{5/16}\)). Same exponent. \(\square\)

Depth-7 census at \(N=10^5\): OOEOOEE \(792\), OOOEOEE
\(787\) against \(391\) — within the
\(\max(N^{2/3},\,\cdot)\) envelope of the depth-6 test
(deviation \(400\ll 1.5\cdot N^{2/3}\)). Every start in
either class with \(n\le 10^5\) satisfied \(J^7(n)<n\).

### Corollary Y (certified-descent density \(57/64\)) — EXACT — HUMAN PROOF

The class of starts carrying a uniform power-envelope descent
certificate of length at most seven — the Corollary-U class
together with OOEOOEE and OOOEOEE — has natural density
\(57/64\). Both new words have cardinality
\(N/128+O(N^{43/48+\varepsilon})\), and \(3^4<2^7\) forces
\(J^7(n)<n\) for \(n\ge2\).

*Proof.* Densities \(\tfrac78+\tfrac1{128}+\tfrac1{128}
=\tfrac{56}{64}+\tfrac{1}{64}=\tfrac{57}{64}\). The new
cylinders are Theorem X. The contraction is
\(81<128\). \(\square\)

The leftover \(\tfrac7{64}\) is the OOOO\* tree (still
uncounted, blocked by Phase 12) together with the expanding
length-7 siblings of OOEOO\*\* and OOOEO\*\* (now counted).
The next contractor in the leftover is OOOOEEE, which
requires \(K_3\).

### Phase-13 decision

**PROMOTE.** The two length-7 contractors that avoid
OOOO\* close under the existing engine plus Corollary R′.
Certified density moves \(7/8\to 57/64\). This is the first
Terras increment that does not need a new kernel, and it
shows the leftover \(1/8\) was not a single obstruction:
two-thirds of its first contracting layer is engine. OOOOEEE
and Conjecture V remain open. No note import, no
density-one claim. `depth7_engine_contracting_proved`
flipped.
