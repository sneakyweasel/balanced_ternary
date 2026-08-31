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

1. [docs/theory/juggler_finite_dynamics_note.md](docs/theory/juggler_finite_dynamics_note.md) — Paper A: cycle-length lower bounds (word obstructions + finance)
2. [docs/theory/juggler_parity_discrepancy_note.md](docs/theory/juggler_parity_discrepancy_note.md) — Paper B: parity discrepancy of nested floor powers
3. [docs/juggler_branch_ledger.md](docs/juggler_branch_ledger.md) — every branch, decision, and strongest evidence
4. [docs/theory/juggler_cycle_finance_note.md](docs/theory/juggler_cycle_finance_note.md) and [docs/theory/juggler_run_survivor_lattice_note.md](docs/theory/juggler_run_survivor_lattice_note.md) — the cycle frontier

Claim labels: [docs/README.md](docs/README.md).
Research method: [docs/methodology.md](docs/methodology.md).
BT-core theory (STRUCTURAL, parked): `docs/theory/balanced_ternary_calculus.md`,
`cubic_newton_stratum.md`; the rewrite-calculus note remains ready to send
for external review.

## Juggler state of the problem

- **Cycles:** no nontrivial cycle of period \(\le 50507\) (laboratory
  certified descent floor \(N_0=26254995\),
  `J-residual-floor-twenty-six-million` /
  `J-cycle-period-fifty-thousand`; Paper A still prints the \(10^6\)
  instance, cutoff \(25780\)). First survivor \(L=50508\) with
  \(n_{\max}^{\mathrm{par}}=1.63\cdot 10^8\); \(19\) parity leftovers
  through \(2\cdot 10^5\). At the published floor the survivors are the
  \(99\)-length lattice on the unimodular basis
  \((25781,16266),(1054,665)\) (`RunSurvivorLattice.lean`). Killing
  leftovers is Diophantine (\(|3^o-2^L|\) near-convergents); the direct
  Baker/SdW transfer is **REFUTED** (`juggler_cycle_gap_baker`), the
  Paper A × Paper B merge is CLOSE (`juggler_cycle_paper_merge`), and
  further \(N_0\) campaigns are PARK — the \(10^7\)/\(10^8\) decades buy
  nothing; the next useful floor is \(1.63\cdot 10^8\).
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

Persistent policy lives in [.cursor/rules/](.cursor/rules/). Streamlit work uses
[.agents/skills/developing-with-streamlit/SKILL.md](.agents/skills/developing-with-streamlit/SKILL.md).
