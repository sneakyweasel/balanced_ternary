# Juggler drift-first-passage tree

Phase-0 census of nested realizing sets A_w of actual
prefix-NC words, plus a modest tau_+ hunt. This is not a
proof that tau_+ is finite and not a termination theorem.
A window-empty child is not A_w empty.

```text
README.md
manifest.json
config.json
ranges/
prefixes/
classes/
record_trajectories/
summaries/
analysis/
```

From the repository root:

```text
python -m research.juggler_sequence.drift_first_passage
```

The Research Engine control layer is not used. ResidualStep is
not extended. Prefix-NC word admissibility is not reopened.
Endpoint filtration is not reopened.
