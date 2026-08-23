---
name: add-ledger-row
description: Add or retag a theorem-ledger row from JSON and regenerate the markdown. Use when adding a named theorem, changing a claim tag, or editing docs/theory/theorem_ledger.json.
---

# Add a theorem-ledger row

`docs/theory/theorem_ledger.json` is the source of truth.
`docs/theory/theorem_ledger.md` is generated. Never edit the markdown by hand.

## Tags

Use exactly one:

- `EXACT — HUMAN PROOF`
- `EXACT — LEAN VERIFIED`
- `VERIFIED COMPUTATIONALLY`
- `CONJECTURE`
- `OBSERVATION`
- `REFUTED`
- `REPARAMETERIZATION`

Do not write `PROVED` in the JSON. Docs may say `PROVED` / `PROVED — LEAN`; those map to the two `EXACT` tags.

Empty `lean` is allowed only when the tag is **not** `EXACT — LEAN VERIFIED`.
Every `source`, `tests[]`, and nonempty `lean` path must exist (Lean paths are relative to `formal/`).

## Steps

1. Choose a stable id (`BTA-…`, `BTJ-…`, `C-…`). Ids must be unique.
2. Append an object with `id`, `tag`, `statement`, `source`, `lean`, `tests`, `related_conjectures`.
3. Point `tests` at files that actually exist (`tests/unit/…` or `tests/research/…`).
4. From the repo root:

```powershell
python tools/render_theorem_ledger.py
python tools/render_theorem_ledger.py --check
python -m pytest tests/unit/test_theorem_ledger.py
```

5. Retag to `EXACT — LEAN VERIFIED` only when the Lean theorem covers the English statement.
