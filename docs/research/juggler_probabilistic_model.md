# Juggler 2025 random-walk / large-deviation model

Status: **MODEL RECONSTRUCTION**

This page reconstructs the probabilistic model used by Prasad–Prasad
2025 (`prasad-prasad-2025-juggler-like`) for *juggler-like* sequences,
and maps it onto the laboratory coordinates. Every quantity below is a
**MODEL ASSUMPTION** or a **derived MODEL PREDICTION**. None of it is a
theorem about the exact floor-power map

\[
J(n)=\lfloor\sqrt{n}\rfloor\ (n\text{ even}),\qquad
J(n)=\lfloor n^{3/2}\rfloor\ (n\text{ odd}).
\]

The exact map remains `floor_power` / `isqrt`. Floating logarithms are
diagnostics. This is not a termination theorem, not a proof that \(J\)
is random, and not a proof of any asymptotic constant on exact \(J\).

The comparison experiment is
[juggler_probabilistic_vs_exact.md](juggler_probabilistic_vs_exact.md).
The previous statistical census
([juggler_probabilistic.md](juggler_probabilistic.md)) measured drift
and did **not** reconstruct the optimizer below.

Natural logarithm is used throughout. The paper’s reported numerical
constants are recovered from the same Bernoulli / Cramér problem; they
are not copied as oracles.

---

## 1. Coordinate transform

**Formula.** For \(x\ge 3\),

\[
L(x)=\log\log x.
\]

On an exact trajectory \(x_0=n\), \(x_{i+1}=J(x_i)\),

\[
L_i=L(x_i),\qquad
\Delta L_i=L_{i+1}-L_i
\quad\text{when }x_i\ge 3\text{ and }x_{i+1}\ge 3.
\]

**Units / normalization.** \(L\) is dimensionless. The laboratory
comparison chart is

\[
t_i=\frac{i}{\log n},\qquad
Z_i=\frac{L_i}{\log n}=\frac{\log\log x_i}{\log n}.
\]

**Assumptions.** \(n\ge 3\) so \(\log n>0\) and \(L(n)\) is defined.
The paper treats \(L(J(n))-L(n)\) as an increment of a real random
walk. Floor and the restriction to integers are ignored.

**Finite-sample interpretation.** \(Z_0=\log\log n/\log n\to 0\), but
at \(n\le 10^5\) one has \(Z_0\in[0.15,0.35]\). Any comparison that
pretends \(Z(0)=0\) is an asymptotic cartoon, not a finite-\(n\)
prediction. The experiment uses the finite-size path
\(Z(t)=Z_0+a\,t\) on the ascent.

**Notation map.**

| This page | Typical paper language | Laboratory exact object |
| --- | --- | --- |
| \(L=\log\log x\) | log-log height of a juggler-like term | diagnostic only |
| \(Z=L/\log n\) | normalized excursion | same diagnostic |
| \(t=i/\log n\) | normalized time | step index \(i\) |
| \(J\) | juggler-like map | exact `floor_power` |
| \(\xi\in\{\log\tfrac32,\log\tfrac12\}\) | idealized increment | \(\Delta L=\) term \(+\) floor error |

---

## 2. Increment distribution

**Ideal increments (MODEL ASSUMPTION).**

\[
\xi=
\begin{cases}
\log(3/2) & \text{on branch }O,\\
\log(1/2) & \text{on branch }E.
\end{cases}
\]

Numerically \(\log(3/2)\approx 0.405465\), \(\log(1/2)\approx -0.693147\).

**Exact floating identity (not a model).** Whenever \(x\ge 16\) and
\(J(x)\ge 3\),

\[
\Delta L(x)=\log c+\varepsilon_{\mathrm{floor}}(x),
\qquad
c=\tfrac32\ (O)\ \text{or}\ \tfrac12\ (E),
\]

\[
\varepsilon_{\mathrm{floor}}(x)
=\log\log J(x)-\log\bigl(c\log x\bigr).
\]

The model sets \(\varepsilon_{\mathrm{floor}}=0\).

**Units.** Each increment is dimensionless (difference of log-logs).

**Finite-sample interpretation.** The identity is an algebraic rewrite
of two floating logs. It does not define \(J\). Floor error must be
measured, not assumed negligible, on the bit lengths that actually
occur on hard trajectories.

---

## 3. Probabilistic assumptions

The 2025 juggler-like analysis treats branch choice as a random
process independent of the current integer. The baseline model used
for the optimizer is

**M0 (iid fair parity) — MODEL ASSUMPTION.**

\[
\mathbb{P}(O)=\mathbb{P}(E)=\tfrac12,
\quad
\text{independent of history and of }x.
\]

The walk is \(S_k=\sum_{i=1}^k\xi_i\) with iid copies of \(\xi\).

**Implied mean and second moment.**

\[
\mu
=\tfrac12\log\tfrac32+\tfrac12\log\tfrac12
=\tfrac12\log\tfrac34
=\tfrac12\log 3-\log 2
\approx -0.143841.
\]

\[
\mathbb{E}[\xi^2]
=\tfrac12\bigl(\log^2\tfrac32+\log^2\tfrac12\bigr)
\approx 0.322428,
\qquad
\mathrm{Var}(\xi)=\mathbb{E}[\xi^2]-\mu^2\approx 0.301737.
\]

**Moment generating function.**

\[
M(\theta)
=\tfrac12\bigl(\tfrac32\bigr)^\theta+\tfrac12\bigl(\tfrac12\bigr)^\theta
=2^{-\theta-1}(3^\theta+1).
\]

Special value: \(M(1)=1\). This is why the Cramér tilt \(\theta^*=1\)
is available.

**What M0 is not.** It is not an exact law of \(J\). Uniform integers
have one-step \(\mathbb{P}(O)=1/2\) by counting. Orbit-induced
parity, Markov dependence, and scale drift are empirical questions.

**Second-order models (only if M0 fails).**

- M1: one-step Markov on \(\{O,E\}\) with empirical
  \(\mathbb{P}(O\mid O)\), \(\mathbb{P}(O\mid E)\).
- M2: scale-conditioned \(\mathbb{P}(O\mid x\in\text{bin})\).

No automaton is built from either.

---

## 4. Large-deviation rate function

**Bernoulli Sanov rate (MODEL ASSUMPTION, derived).** Let \(p\) be the
empirical odd frequency on a block of steps. The rate relative to
fair coins is the KL divergence

\[
I_{\mathrm{Ber}}(p)
=p\log(2p)+(1-p)\log\bigl(2(1-p)\bigr)
=p\log p+(1-p)\log(1-p)+\log 2,
\]

in nats per step. \(I_{\mathrm{Ber}}(1/2)=0\).

**Mean increment at frequency \(p\).**

\[
m(p)
=p\log\tfrac32+(1-p)\log\tfrac12
=p\log 3-\log 2.
\]

Positive drift requires

\[
p>p_0:=\frac{\log 2}{\log 3}\approx 0.630930.
\]

**Cramér rate on the increment.**

\[
I_\xi(x)=\sup_{\theta\in\mathbb{R}}\bigl(\theta x-\log M(\theta)\bigr).
\]

Because \(\xi\) is two-point, \(I_\xi(m(p))=I_{\mathrm{Ber}}(p)\).
The two parameterizations are the same model.

**Zero-drift cost.** At \(p=p_0\), \(m(p_0)=0\) and

\[
I_0:=I_{\mathrm{Ber}}(p_0)\approx 0.034688.
\]

This is also \(I_\xi(0)\). **Finite-sample interpretation:**
\(\mathbb{P}(\text{empirical drift }\ge 0\text{ for }k\text{ steps})
\lesssim e^{-k I_0}\). This is a model tail, not an exact bound on
\(J\).

---

## 5. Predicted extremal slope \(a^*\)

**Optimization (derived, not copied).** The cheapest way to gain
height \(h\) in \(L\) is to travel at a constant frequency \(p>p_0\)
for time \(t=h/m(p)\), at cost \(t\,I_{\mathrm{Ber}}(p)\). The cost
per unit height is \(I_{\mathrm{Ber}}(p)/m(p)\). Minimize over
\(p\in(p_0,1]\).

Critical-point equations: \(I'(p)/I(p)=m'(p)/m(p)\). Here
\(I'(p)=\log(p/(1-p))\) and \(m'(p)=\log 3\). The unique solution in
\((p_0,1)\) is

\[
p^*=\frac34.
\]

The same \(p^*\) is the exponentially tilted odd probability at
\(\theta=1\):

\[
p_\theta=\frac{3^\theta}{3^\theta+1},\qquad p_1=\frac34.
\]

**Slope.**

\[
a^*
:=m(p^*)
=\frac34\log 3-\log 2
\approx 0.130812.
\]

Also \(I_{\mathrm{Ber}}(p^*)=a^*\), so the height cost is exactly
\(1\) nat per unit of \(L\):

\[
\mathbb{P}(\max S\ge h)\asymp e^{-h}
\quad\text{(MODEL PREDICTION)}.
\]

**Units.** \(a^*\) is \(dL/di\), nats of log-log per exact step.
On the \((t,Z)\) chart the model ascent is the straight line

\[
Z_{\mathrm{asc}}(t)=Z_0+a^*\,t.
\]

**Finite-sample interpretation.** A fitted pre-peak slope on a short
word is not \(a^*\). Window dependence must be reported. Agreement
means the fitted slope moves toward \(0.1308\) as the pre-peak length
grows, not that one interval looks linear.

---

## 6. Predicted maximum-excursion constant \(\rho^*\)

**Definition used here.**

\[
\rho(n)=\frac{\log\log(\max_i x_i)}{\log n}=Z_{\mathrm{peak}}.
\]

**Asymptotic MODEL PREDICTION.** Among an ensemble of size \(\asymp n\)
independent M0 walks, the extreme height of \(S\) above \(L_0\) is
\(\log n+O(1)\), because the tail of the maximum is \(e^{-h}\).
Therefore

\[
L_{\mathrm{peak}}
=L_0+\log n+O(1)
=\log\log n+\log n+O(1),
\]

\[
\rho^*
:=\lim\frac{L_{\mathrm{peak}}}{\log n}
=1.
\]

Finite-size predictor (used in the tables):

\[
\rho_{\mathrm{pred}}(n)=1+\frac{\log\log n}{\log n}.
\]

The public summary of the 2025 work reports a maximum-excursion
constant \(\rho\approx 1\). That matches \(\rho^*\) under this
normalization. Label: **MODEL PREDICTION**, not an exact \(J\) limit.

**Units.** Dimensionless. \(\rho=1\) means \(\log(\mathrm{peak})\asymp n\),
i.e. \(\mathrm{peak}\asymp e^{n}\), which is an asymptotic cartoon.
At laboratory \(n\), \(\rho_{\mathrm{pred}}(n)\) is \(1.2\)–\(1.5\),
and the exact peak is far smaller.

---

## 7. Predicted stopping-time constant \(\gamma\)

**Zero-drift tail (derived).** Under M0, the probability of a
non-contracting block of length \(k\) is governed by \(I_0\):

\[
\mathbb{P}(H\ge k)
\lesssim C\,e^{-k I_0}
=C\,e^{-k/\gamma},
\]

\[
\gamma
:=\frac{1}{I_0}
=\frac{1}{I_{\mathrm{Ber}}(\log 2/\log 3)}
\approx 28.82826.
\]

The public summary of the 2025 work reports a stopping constant
\(\gamma\approx 28.828\). That number is \(1/I_0\) to all printed
digits. Label: **MODEL PREDICTION**.

**Units.** \(\gamma\) is in *steps*. It is the exponential scale of
the model tail of the non-contracting duration \(H\), equivalently
the model law

\[
\frac{\max_{m\le N} H(m)}{\log N}\to\gamma
\]

for independent M0 walks. It is **not** \(\mathbb{E}[H]\) and not
\(H/\log\log n\).

**A second, geometric time (also derived).** The cheapest path that
spends a cost budget of \(\log n\) nats to climb and then descends
with typical drift \(\mu\) has normalized times

\[
t_{\mathrm{peak}}^*=\frac{1}{a^*}\approx 7.6446,
\qquad
t_{\mathrm{stop}}^*
=\frac{1}{a^*}+\frac{1}{\lvert\mu\rvert}
\approx 14.5967.
\]

These are \((t,Z)\)-chart times, not \(\gamma\). The experiment
compares both: \(\gamma\) against the *tail* of \(H\), and
\(t_{\mathrm{peak}}^*\), \(t_{\mathrm{stop}}^*\) against record
*geometry*.

**Finite-sample interpretation.** At \(n=4000\), \(\gamma\log n\approx 239\),
while the exact delay record is \(H(3889)=77\). A finite window cannot
confirm \(\gamma\). The object to watch is the residual
\(\log\mathbb{P}(H\ge k)+k I_0\), not a fitted intercept promoted to
a theorem.

---

## 8. Asymptotic normalization (summary)

On the chart \((t,Z)\):

| object | model value | meaning |
| --- | --- | --- |
| start | \(Z_0=\log\log n/\log n\) | vanishes slowly |
| ascent slope | \(a^*\approx 0.130812\) | \(dZ/dt=a^*\) |
| odd frequency on ascent | \(p^*=3/4\) | LD optimizer |
| peak height | \(Z_{\mathrm{peak}}\to 1\) | \(\rho^*=1\) |
| finite-size peak | \(1+Z_0\) | used in tables |
| peak time | \(t_{\mathrm{peak}}\to 1/a^*\) | steps \(\sim\log n/a^*\) |
| typical descent slope | \(\mu\approx -0.143841\) | M0 mean |
| geometric stop time | \(t_{\mathrm{stop}}^*\approx 14.597\) | climb then typical descent |
| duration tail | \(\mathbb{P}(H\ge k)\sim e^{-k/\gamma}\) | \(\gamma\approx 28.828\) |

**Normalized record table (what the experiment prints).**

\[
\frac{\log\log(\mathrm{peak})}{\log n}
\ \text{vs}\ 1+\frac{\log\log n}{\log n},
\qquad
\frac{i_{\mathrm{peak}}}{\log n}
\ \text{vs}\ \frac{1}{a^*},
\qquad
\frac{H}{\log n}
\ \text{vs}\ t_{\mathrm{stop}}^*\ \text{and vs}\ \gamma,
\qquad
p_O
\ \text{vs}\ \tfrac34.
\]

Agreement is a residual, not a proof.

---

## 9. Assumption status of every named constant

| parameter | value | source | assumption_status |
| --- | --- | --- | --- |
| \(L=\log\log x\) | coordinate | paper / this reconstruction | MODEL ASSUMPTION |
| \(\xi_O=\log(3/2)\) | \(0.405465\) | ideal odd power | MODEL ASSUMPTION |
| \(\xi_E=\log(1/2)\) | \(-0.693147\) | ideal even power | MODEL ASSUMPTION |
| \(\mathbb{P}(O)=1/2\) iid | \(1/2\) | M0 | MODEL ASSUMPTION |
| \(\mu\) | \(-0.143841\) | \(M'(0)\) | derived from M0 |
| \(M(1)=1\) | \(1\) | two-point mgf | derived from M0 |
| \(p_0=\log 2/\log 3\) | \(0.630930\) | \(m(p)=0\) | derived from M0 |
| \(I_0=I_{\mathrm{Ber}}(p_0)\) | \(0.034688\) | Sanov | derived from M0 |
| \(p^*\) | \(3/4\) | LD optimizer | derived from M0 |
| \(a^*=(3/4)\log 3-\log 2\) | \(0.130812\) | \(m(p^*)\) | derived from M0 |
| \(\rho^*\) | \(1\) | extreme-value of \(e^{-h}\) tail | derived from M0 |
| \(\gamma=1/I_0\) | \(28.82826\) | duration tail scale | derived from M0; matches reported \(28.828\) |
| \(t_{\mathrm{peak}}^*\) | \(7.64456\) | \(1/a^*\) | derived from M0 |
| \(t_{\mathrm{stop}}^*\) | \(14.5967\) | \(1/a^*+1/\lvert\mu\rvert\) | derived from M0 |
| floor error \(=0\) | \(0\) | paper idealization | MODEL ASSUMPTION |
| independent increments | — | paper idealization | MODEL ASSUMPTION |

`assumption_status` values used in `model_parameters.json`:
`MODEL_ASSUMPTION`, `DERIVED_FROM_M0`, `LITERATURE_REPORTED`,
`FINITE_SAMPLE_PREDICTOR`.

---

## 10. What this model is forbidden to imply

- Negative \(\mu\) does not imply every exact orbit reaches \(1\).
- \(e^{-h}\) small does not imply an exact trajectory is impossible.
- \(\mathbb{P}(O)\approx 1/2\) on a census does not imply iid parity.
- A fitted \(\gamma\) on \(n\le 4000\) is not the asymptotic constant.
- The optimizer \((p^*,a^*)\) is the most expensive *model* path, not
  a certificate that exact \(J\) can or cannot realize it.

The exact-versus-model experiment tests the *geometry* of the hardest
computed trajectories against this optimizer, and asks whether the
deviations have deterministic arithmetic structure.
