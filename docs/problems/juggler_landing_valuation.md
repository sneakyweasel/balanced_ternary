# Juggler 2-adic landing obstruction

Status: **EXPLORATORY**

Standalone arithmetic layer on the rewritten Juggler formalization. It
is **not** a Research Engine control-layer experiment and not a claim
that every positive integer reaches 1.

## Problem

Does the 2-adic structure of \(\rho_y=y^3-T(y)^2\) on an odd-to-odd
landing carry history from a previous persistent expanding block and
constrain the next landing?

## Exact statement

For odd \(y\) with odd landing \(z=T(y)\),

\[
y^3=z^2+\rho,\qquad \rho=y^3-z^2.
\]

The already-known fact is that \(\rho\) is even. The Phase-0 question
is the exact possible values of \(v_2(\rho)\), whether they are
functions of \(y\bmod 2^k\), and whether the law becomes stronger when
\(y\) is the endpoint of a persistent expanding residual block.

The desired mechanism was

\[
\text{PE history}\Longrightarrow
\text{2-adic constraint on }y\Longrightarrow
\text{constraint on }T(y)\Longrightarrow
\text{restricted next residual block}.
\]

Do not assume that such a restriction exists. This says nothing about
totality.

## Current literature

- Odd-odd remainder even —
  **EXACT — LEAN VERIFIED** in `Problems.Juggler.SequentialMordell`.
- Odd squares \(\equiv 1\pmod 8\) —
  **EXACT — LEAN VERIFIED** as `odd_sq_mod_eight`.
- Residue modulo \(8\) does not decide PE continuation —
  **REFUTED** in the two-block and expanding-grammar dossiers.
- Landing \(\theta=\rho/(2T+1)\) unrestricted —
  **CLOSE** as `LANDING_THETA_UNRESTRICTED`.
- Sequential near-Mordell composition is OO defect —
  **CLOSE** as `SEQUENTIAL_MORDELL_IS_OO_DEFECT`.
- Residual-state finite quotients need the integer itself —
  **CLOSE** as `RESIDUAL_STATE_NEEDS_X`.

Project relationship: **extended**.

## Branch budget

```text
Mathematical target     What 2-adic restrictions does y³-z² satisfy
                        when both y,z are odd, and does PE history
                        strengthen them?
Novelty hypothesis      A history-sensitive valuation bound
                        v₂(ρ_y)≥r>1, or a finite 2-adic state that
                        restricts the next odd-run grammar
Falsifier               The law is y mod 8; PE endpoints realise
                        every generic pattern including v₂=1
Existing machinery      odd_remainder_even, odd_sq_mod_eight,
                        PersistentExpandingResidual, PE walker
Maximum Phase-0 scope   Classify v₂(ρ) mod 8; compare generic
                        odd-odd vs PE endpoints; formalize the
                        residue law; one PE v₂=1 witness. No halt
Promotion criterion     PE ⇒ v₂≥r>1, or a 2-adic state that
                        restricts the next residual grammar
Stop criterion          Falsifiers A–E; residue rewrite only;
                        machinery gravity
```

## Balanced-ternary formulation

None required. The map is on ordinary positive integers.

## Why BT may be relevant

It is not required.

## Candidate operations / invariants

- `landingRemainder` / `oddOddLanding` / `landingValuation` —
  **REPARAMETERIZATION** of `localDefectOdd` and \(v_2\)
- \(\rho\equiv y-1\pmod 8\) on odd-odd —
  **EXACT — LEAN VERIFIED**
- \(y\equiv 3,7\pmod 8\Rightarrow v_2(\rho)=1\);
  \(y\equiv 5\pmod 8\Rightarrow v_2=2\);
  \(y\equiv 1\pmod 8\) and \(\rho\neq 0\Rightarrow v_2\ge 3\) —
  **EXACT — LEAN VERIFIED**
- \(y\equiv 1\pmod{2^r}\Rightarrow v_2(\rho)\ge r\) —
  **REFUTED** at \(r=4\): \(y=33\equiv 1\pmod{16}\) has \(v_2=3\)
- PE endpoint \(\Rightarrow v_2(\rho)\ge r>1\) —
  **REFUTED** (`pe_endpoint_763_valuation`)
- History changes the 2-adic landing law —
  **REFUTED** on the scanned window
- \(v_2(\rho)\) locks the next odd-run grammar —
  **REFUTED** on the scanned window
- Infinite odd-odd orbit — not claimed

## Experiments

Cheap integer census, not a new raw search.

- Odd-odd starts \(n\le 4000\): 1009 landings. \(\rho\equiv y-1
  \pmod 8\) always. Valuation is a function of \(y\bmod 8\):
  \(y\equiv 3,7\Rightarrow v_2=1\); \(y\equiv 5\Rightarrow v_2=2\);
  \(y\equiv 1\Rightarrow v_2\ge 3\) or \(\rho=0\). Exact squares
  (\(\rho=0\)) occupy only the class \(y\equiv 1\pmod 8\).
- Higher moduli do not refine the classes \(3,5,7\pmod 8\).
  \(y\equiv 1\pmod{16}\) still realises \(v_2=3\) (example \(33\)).
  The floor constraint does not strengthen the congruence.
- Next-step parity is mixed at every observed valuation, including
  \(v_2=1,2,3\).
- PE endpoints \(n\le 4000\): 350 landings. All odd classes modulo
  \(8\) occur. \(v_2=1\) occurs 165 times. The valuation table is
  the same residue law. Word type (`OOE`, `OOOE`, …) does not
  shift it.
- PE valuation sequences: \(r_i=1\) can repeat
  (\(321\): \(1,1,1,3\)); the \(365\) chain is \(1,2,1\), not
  monotone. No transition \(r_i\ge r\Rightarrow r_{i+1}\ge r'\).

Tests: `tests/research/juggler_sequence/test_landing_valuation.py`.

## Conjectures

None opened in `conjectures/`.

## Counterexamples

- “\(y\equiv 1\pmod{16}\) forces \(v_2\ge 4\).” False:
  \(33\to 189\), \(\rho=216\), \(v_2=3\),
  **EXACT — LEAN VERIFIED**.
- “A PE endpoint has \(v_2(\rho)\ge r>1\).” False:
  \(365\xrightarrow{\mathrm{OOE}}763\), \(763\equiv 3\pmod 8\),
  \(v_2=1\), **EXACT — LEAN VERIFIED**.
- “PE history changes the 2-adic law.” False on \(n\le 4000\):
  every PE pair \((v_2,y\bmod 8)\) except one rare high valuation
  already occurs among generic odd-odd starts, and the missing
  generic pair is the same \(y\equiv 1\) family.
- “\(v_2\) locks the next residual word.” False: \(v_2=1\)
  continues as persistent `OOE` and as non-persistent `OOEE`.
- “Valuation is monotone along a PE run.” False: \(365\) gives
  \(1,2,1\).

## Formalization

`formal/Problems/Juggler/LandingValuation.lean`, after
`SequentialMordell`. No `sorry`. No halt theorem. No 2-adic
continuation automaton. No `landing2AdicState`.

## Results

- The 2-adic landing law is \(\rho\equiv y-1\pmod 8\).
- Valuation is a function of \(y\bmod 8\), except that
  \(y\equiv 1\pmod 8\) only forces \(v_2\ge 3\) or \(\rho=0\).
- The floor metric does not add a stronger 2-adic constraint.
- PE history does not change the law and does not force
  \(v_2>1\).
- The valuation is not transported: it does not decide the next
  landing or the next residual word.

## Open questions

The leftover is still whether an odd-to-odd residual chain can
continue indefinitely. That is not a 2-adic remainder-valuation
problem. Predecessor cylinders do not restore history either;
see [juggler_preimage_cylinders.md](juggler_preimage_cylinders.md).
Do not reopen residues, \(\theta\), sequential Mordell,
or expanding-word grammar.

## Decision

**CLOSE** the 2-adic landing attack as
`LANDING_VALUATION_IS_Y_MOD_8`. The exact classification is
elementary odd-cube / odd-square arithmetic. Persistent-expanding
history does not strengthen it, and the valuation does not
restrict the next residual block. The bound \(\rho\ge 2\) is the
already-known evenness of an odd-odd remainder. Do not claim
termination.

Best next question: is there any arithmetic, other than the integer
\(y\) itself, that decides whether a persistent residual landing
stays odd-to-odd?

## Publication assessment

Status: `EXPLORATORY`. An exact residue-valuation lemma and a
negative history result, not a paper candidate and not a Juggler
totality result.
