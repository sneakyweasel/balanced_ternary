# Juggler word atlas native engine

CUDA/C++ backend for Milestone 1. Python is the research interface
(`research.juggler_sequence.atlas`). Lean remains the certification
boundary. This directory is not a new mathematical theory.

## Build

```text
cmake -S atlas -B atlas/build -G Ninja
cmake --build atlas/build
```

CUDA is optional. Without a toolkit the CPU census binary still builds.
`atlas/scripts/build_windows.bat` uses the newest installed toolkit
under `CUDA\v*`. CUDA 12.8+ compiles native `sm_120`; 12.6 emits
`75-virtual` PTX for the 5090 driver to JIT.

```text
atlas/build/juggler-atlas-census --k-max 12 --n-max 1000000 --backend cpu --output census.tsv
```

## Semantics

`floor_power` matches Lean `floorPower` and Python `math.isqrt`:
even `isqrt(n)`, odd `isqrt(n^3)`. Packed words use LSB = first
symbol, `0=E`, `1=O`. Kernel A walks each start and `atomicMin`s the
observed minimum for every prefix. It does not classify PE.

Wide intermediates that exceed the native limb budget are reported as
overflows and finished by the Python exact reference.

## Tests

```text
atlas/build/juggler-atlas-tests
pytest tests/research/juggler_sequence/test_word_atlas.py
```
