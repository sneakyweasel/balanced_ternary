# Conjecture registry

Machine-readable records live under `conjectures/` with status folders:

- `active/`
- `proved/`
- `refuted/`
- `archived/`

The Python API is `research.conjectures`.

## Status values

`ACTIVE`, `PROVED`, `REFUTED`, `COMPUTATIONALLY_SUPPORTED`,
`REPARAMETERIZATION`, `ARCHIVED`.

A computational observation must not be silently stored as a conjecture.
Claim labels in the mathematical record
(`PROVED`, `VERIFIED COMPUTATIONALLY`, `CONJECTURE`, `OBSERVATION`,
`REFUTED`) remain authoritative; the YAML registry indexes them.

## Required fields

`id`, `title`, `statement`, `mathematical_domain`, `origin`, `status`,
`first_seen`, `tested_range`, `counterexamples`, `proof_reference`,
`lean_reference`, `literature`, `notes`.

## API

`register_conjecture`, `update_status`, `add_counterexample`,
`add_proof`, `add_lean_proof`, `list_conjectures`.

Rejected hypotheses from prior milestones are preserved under `refuted/`.
