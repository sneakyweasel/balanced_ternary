# Juggler first positive-drift crossing

Phase-0 census of actual orbits until the first G_k > 0.
Prefix-NC snapshots record exact endpoint metrics. This is not
a proof that tau_+ is finite and not a termination theorem.

```text
README.md
manifest.json
config.json
ranges/
traces/
summaries/
analysis/
```

From the repository root:

```text
python -m research.juggler_sequence.drift_crossing
```

The Research Engine control layer is not used. ResidualStep is
not extended. Prefix-NC word admissibility is not reopened.
