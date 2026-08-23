# Agent guide

This is the **Balanced Ternary Mathematical Laboratory**: a
problem-independent core (`bt`) plus independent research applications
(`research.*`).

```text
cli, visualization          application edges
research.*                  problem-specific mathematics
bt.*                        problem-independent BT mathematics
```

`bt.*` must never import `research.*`. Architecture:
[docs/architecture/overview.md](docs/architecture/overview.md).

## Reading path

1. [docs/theory/balanced_ternary_calculus.md](docs/theory/balanced_ternary_calculus.md)
2. [docs/theory/cubic_newton_stratum.md](docs/theory/cubic_newton_stratum.md) — current frontier
3. [docs/theory/residual_vs_classical.md](docs/theory/residual_vs_classical.md)
4. [docs/theory/theorem_ledger.md](docs/theory/theorem_ledger.md) (generated from JSON)

Collatz is one application: [docs/collatz_mathematics.md](docs/collatz_mathematics.md).
Claim labels: [docs/README.md](docs/README.md).
Research method: [docs/methodology.md](docs/methodology.md).

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

Then implement only that scope. Search `conjectures/refuted/` and the
`REFUTED` ledger rows before re-testing a hypothesis.

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

Then stop. Machinery gravity — new structure, new CLI, new
visualization, no new mathematical consequence — means stop
implementing, find the invariant or obstruction, and decide.

## Where new math goes

| Kind of change | Home |
|----------------|------|
| Trit / `D` / `I` / jets / `≡_k` / `F_k` closed form | `src/bt/calculus/` |
| Cubic fibres, `N1`/`N0`, mismatched `Q`, stratum API | `src/research/residuals/` |
| Accelerated `T`, cylinders, cycles, warp | `src/research/collatz/` |
| Lean packaging of existing lemmas | `formal/BTCalculus/` or `formal/Problems/Collatz/` |
| Named theorem metadata | `docs/theory/theorem_ledger.json` then render |
| New research area | [docs/problems/TEMPLATE.md](docs/problems/TEMPLATE.md) + `src/research/<id>/` |

Do not add `bt.calculus` shims that re-export residual research.
Do not auto-open a numbered milestone; every branch ends in `PROMOTE`,
`PARK`, or `CLOSE`.
Do not claim a Collatz solution.

## Commands

```powershell
python -m pip install -e ".[dev,ui]"
pytest
pytest --runslow
python tools/render_theorem_ledger.py --check
$env:PATH = "$env:USERPROFILE\.elan\bin;$env:PATH"
cd formal; lake build
btprime ui
btprime calculus explorer
```

Persistent policy lives in [.cursor/rules/](.cursor/rules/). Streamlit work uses
[.agents/skills/developing-with-streamlit/SKILL.md](.agents/skills/developing-with-streamlit/SKILL.md).
