# Agent guide

This is the **Balanced Ternary Mathematical Laboratory**: a
problem-independent core (`bt`) plus independent research applications
(`research.*`). The active application is the **Juggler map**
\(T(n)=\lfloor\sqrt n\rfloor\) (\(n\) even), \(\lfloor n\sqrt n\rfloor\)
(\(n\) odd).

```text
cli, visualization          application edges
research.*                  problem-specific mathematics
research_engine             problem-independent experimental dynamics
bt.*                        problem-independent BT mathematics
```

`bt.*` must never import `research.*` or `research_engine`. Architecture:
[docs/architecture/overview.md](docs/architecture/overview.md).

## Juggler reading path

1. [docs/theory/juggler_finite_dynamics_note.md](docs/theory/juggler_finite_dynamics_note.md) — Paper A: cycle-length lower bounds (word obstructions + finance + the §5 walk-charge envelope; lab extract in [juggler_walk_charge_note.md](docs/theory/juggler_walk_charge_note.md))
2. [docs/theory/juggler_parity_discrepancy_note.md](docs/theory/juggler_parity_discrepancy_note.md) — Paper B: parity discrepancy of nested floor powers
3. [docs/juggler_branch_ledger.md](docs/juggler_branch_ledger.md) — every branch, decision, and strongest evidence
4. [docs/theory/juggler_cycle_finance_note.md](docs/theory/juggler_cycle_finance_note.md) and [docs/theory/juggler_run_survivor_lattice_note.md](docs/theory/juggler_run_survivor_lattice_note.md) — the cycle frontier

Claim labels: [docs/README.md](docs/README.md).
Research method: [docs/methodology.md](docs/methodology.md).
BT-core theory (STRUCTURAL, parked): `docs/theory/balanced_ternary_calculus.md`,
`cubic_newton_stratum.md`; the rewrite-calculus note remains ready to send
for external review.

## Juggler state of the problem

- **Cycles:** no nontrivial cycle of period \(<478245\) at the
 laboratory certified descent floor \(N_0=162849448\)
 (`J-residual-floor-one-hundred-sixty-two-million`,
 `J-cycle-period-four-hundred-seventy-eight-thousand`): the floor
 certificate is complete (547 chunks, zero failures, peak
 \(463362780\) bits) and the walk charge kills all \(15\) parity
 leftovers below the blocker \(478245=176251+301994\) (\(k=1\)
 semiconvergent fan, required \(19.46\), DK break-even
 \(3.48\cdot 10^8\) — Diophantine, not computational).
 Since the 1 Sep 2026 consolidation Paper A prints the
 \(26254995\) floor: parity cutoff \(50507\) (§5.1), then the
 walk-charge envelope — transport, hug adversary, word identity,
 Denjoy–Koksma over certified Ostrowski blocks, window theorem on
 \([50508,301994)\) — gives period \(\ge 176251\) (§5.2–5.7,
 `J-cyclemin-walk-charge-instance`), and Corollary 5.10 prints the
 second floor \(162849448\) with period \(\ge 478245\); the
 \(10^6\) base instance and
 the \(99\)-length survivor lattice on \((25781,16266),(1054,665)\)
 (`RunSurvivorLattice.lean`) stay in §4. Discrete word layer,
 quotient arithmetic, general Ostrowski numeration (window digit
 cap \(s(L)\le 47\) structural), the transport inequality of
 Thm 5.3, the defect-to-hug-charge chain (§5.2 + Thm 5.4
 analytic half), the Thm 4.6 certified identity
 (`cycleMin_defect_finance`), and the Thm 5.9 kill template
 (`cycleMin_hug_kill_criterion`) are Lean (`WalkChargeWords.lean`,
 `OstrowskiSandwich.lean`, `OstrowskiNumeration.lean`,
 `WalkTransport.lean`, `WalkChargeMax.lean`,
 `DefectFinance.lean`); of the §5 envelope chain only the
 rotation average, Denjoy–Koksma, and the per-length kill
 evaluations remain analytic prose / verified computation. The walk program is terminal: the
 fan-minimum reduction (`juggler_walk_fan_minimum_law`, CONJECTURE)
 ties further asymptotic progress to unbounded partial quotients of
 \(\log 2/\log 3\) — classical OPEN. Killing the
 remaining near-convergents (first \(478245\)) is Diophantine; the
 direct Baker/SdW transfer is **REFUTED** (`juggler_cycle_gap_baker`),
 the Paper A × Paper B merge is CLOSE (`juggler_cycle_paper_merge`),
 and further \(N_0\) campaigns are PARK (the next useful floor is
 \(3.48\cdot 10^8\)).
- **Termination:** certified descent density \(29/32\); the pointwise route
  is parked behind the \(K_3\) obstruction ladder BB/GG/JJ. Not claimed.
- **Local attacks are closed.** Fibres are parity + interval only
  (`even_cell_iff`, `odd_cell_unique`, `cell_same_next_state`): no finite
  local configuration around a hypothetical cycle is contradictory. Seam,
  ancestry, provenance, collision-pair, word-order, error-transport, and
  cycle-lift drops all reduce to Collision Factorization (first meeting iff
  the parent is off-cycle) or the lift identity \(T^L(t)=c\ge n\). Do not
  reopen them; the ledger and `conjectures/refuted/` list each kill.
- **Anti-overclaim:** never claim a halt theorem, "no cycle of any
  length", or a Collatz/Juggler solution. Finite checks are not proofs.

## Juggler file map

| Artifact | Home |
|----------|------|
| Probes / censuses | `src/research/juggler_sequence/<branch>.py` |
| Tests (fast suite) | `tests/research/juggler_sequence/test_<branch>.py` |
| Data artifacts | `data/research/juggler/.../summary.json` |
| Lean (words, cells, CycleMin, finance, lattice) | `formal/Problems/Juggler/` |
| Branch dossier | `docs/problems/juggler_<id>.md` (all TEMPLATE headings; enforced by `tests/integration/test_problem_dossiers.py`) |
| Conjecture record | `conjectures/{active,refuted,proved,archived}/<id>.json` |
| Journal entry | `docs/research_journal.md` (consolidations allowed; no auto-milestones) |
| Named theorem metadata | `docs/theory/theorem_ledger.json`, then render |

## How a direction runs

`explore → distill → prove/refute → decide`. Before substantial
implementation, output a triage block:

```text
Mathematical target     one precise question
Novelty hypothesis      what could possibly be new
Falsifier               the observation that kills the idea
Existing machinery      what the platform already provides
Maximum Phase-0 scope   the smallest experiment that answers the target
Promotion criterion     what would justify PROMOTE
Stop criterion          what forces PARK or CLOSE
```

Implement only that scope. Search `conjectures/refuted/`, the branch
ledger, and the `REFUTED` ledger rows before re-testing a hypothesis.

At the end of a phase, report:

```text
What was learned      3–7 concise points
Strongest theorem     one statement
Strongest refutation  one false hypothesis or counterexample, if any
Reusable machinery    what enters the platform
Branch status         PROMOTE | PARK | CLOSE
Why                   one short paragraph
Best next question    exactly one
```

Then stop. Machinery gravity — new structure, new CLI, new visualization,
no new mathematical consequence — means stop implementing, find the
invariant or obstruction, and decide. Every branch ends in `PROMOTE`,
`PARK`, or `CLOSE`; do not auto-open the next one. Do not raise \(N_0\),
reopen finance, or edit Paper A from a Phase-0 branch.

## Where non-Juggler math goes

Trit / `D` / jets / `≡_k` → `src/bt/calculus/`; cubic strata →
`src/research/residuals/`; Collatz → `src/research/collatz/`; generic Lean
→ `formal/BTCalculus/`. No `bt.calculus` shims, no compatibility packages.
New research area: [docs/problems/TEMPLATE.md](docs/problems/TEMPLATE.md)
plus `src/research/<id>/`.

## Commands

```powershell
python -m pip install -e ".[dev,ui]"
pytest                                              # fast suite
pytest tests/research/juggler_sequence -q           # Juggler only
pytest --runslow
python -m research.juggler_sequence.<branch>        # run a probe
python tools/render_theorem_ledger.py --check
$env:PATH = "$env:USERPROFILE\.elan\bin;$env:PATH"
cd formal; lake build                               # no sorry / admit
```
## Remarks

If you're Fable don't spend ages fixing tests - focus on the math.

You have access to a Windows 11 machine with an AMD Ryzen 9 3900X (12C/24T), 64 GB RAM, and an RTX 5090 (32 GB VRAM, CUDA 13.3), so don't be afraid to use it.

Persistent policy lives in [.cursor/rules/](.cursor/rules/). Streamlit work uses
[.agents/skills/developing-with-streamlit/SKILL.md](.agents/skills/developing-with-streamlit/SKILL.md).
