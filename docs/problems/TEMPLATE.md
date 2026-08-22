# Problem template

Copy this page to `docs/problems/<id>.md` and add `src/research/<id>/` without
editing `bt.*`.

## Problem

Name and one-sentence topic.

## Exact statement

The mathematical question, with quantifiers.

## Current literature

Known results and how this project relates (`known` / `reproduced` /
`extended` / `independent` / `refuted`). Cite `literature/` ids.

## Balanced-ternary formulation

How the objects are written in canonical balanced ternary.

## Why BT may be relevant

Representation, operators, automata, or sparsity — not a claim that BT solves the problem.

## Candidate operations / invariants

Maps and functions to try. Label each PROVED / CONJECTURE / OBSERVATION.

## Experiments

Registered runners, ranges, and output schema.

## Conjectures

Ids in `conjectures/`. Computational observations are not conjectures.

## Counterexamples

Smallest witnesses, with tests under `tests/regression/`.

## Formalization

Lean modules, or an explicit statement that none exist yet. No `sorry`.

## Results

Exact theorems and computational verifications.

## Open questions

What remains.

## Publication assessment

Status: `EXPLORATORY` | `STRUCTURAL` | `THEOREM` | `PAPER_CANDIDATE` | `ARCHIVED`.

`PAPER_CANDIDATE` requires at least one exact theorem or a genuinely
nontrivial computational result with a clear literature distinction.
