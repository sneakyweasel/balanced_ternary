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
Do not auto-open a numbered milestone.
Do not claim a Collatz solution.

## Commands

```powershell
python -m pip install -e ".[dev,ui]"
pytest
python tools/render_theorem_ledger.py --check
$env:PATH = "$env:USERPROFILE\.elan\bin;$env:PATH"
cd formal; lake build
btprime ui
btprime calculus explorer
```

Persistent policy lives in [.cursor/rules/](.cursor/rules/). Streamlit work uses
[.agents/skills/developing-with-streamlit/SKILL.md](.agents/skills/developing-with-streamlit/SKILL.md).
