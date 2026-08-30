# Formal vs realized AboveAnchor language

Bounded census of prefix-noncontracting words versus
`AboveAnchor` prefixes. A missing word is
`NOT_OBSERVED_WITHIN_BOUND`. That is not global
non-realizability.

## Layout

```text
README.md
provenance.json
summary.{json,md}
formal_words_N.bin          # packed uint32, LSB = first letter
aa_words_N.bin
minimal_unobserved.jsonl
hard_starts.jsonl
```

Science window: `k_max=20`, odd `n<=10^6`, hold-out `5e5`,
leftovers `37,365,501,1517,6187`.

Regenerate with:

```text
python -m research.juggler_sequence.formal_realized_gap
```
