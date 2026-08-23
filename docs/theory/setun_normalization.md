# Setun and normalization

This page is **not** a cycle-accurate emulator. It records how a tiny
AST compiles to coefficient normalization, and it separates historical
fact from sketch.

## Historical fact

Only claims supported by [setun_connection.md](setun_connection.md) or
a `literature/*.json` record (Hayes 2001, Knuth vol. 2, Malinovsky):

- Setun used signed trits `{-1,0,+1}`.
- Arithmetic used balanced-ternary addition, subtraction, and
  multiplication with a local carry/borrow of at most one.
- The sign of a word was the leading trit; comparison used that sign.

Those facts motivate the rewrite `c = 3q + r` and the `CMP3` node.
They do **not** attribute our abstract `→` relation, parallel depth,
or FMA cost gap to Brusentsov’s machines.

## Historical sketches

The following remain sketches unless a cited source is added:

- 18-trit hardware registers as a universal Setun word size
- a dedicated `-+-` normalize opcode in a published ISA
- a fused multiply-add micro-operation as a documented instruction

`bt.normtheory.setun_subset.label` returns `HISTORICAL SKETCH` for
those strings and `HISTORICAL FACT` only when the claim matches the
fact list above.

## Tiny AST

Nodes: `Lit`, `ADD`, `SUB`, `MUL`, `FMA`, `SHIFT`, `NORMALIZE`, `CMP3`.

Compilation:

| Node | Meaning |
|------|---------|
| `ADD`/`SUB`/`MUL` | coefficient add / convolution, then Strategy A |
| `FMA` | `normalize(PQ+R)` |
| `SHIFT` | prepend `0` (`S` / `I_0` on coefficients) |
| `NORMALIZE` | Strategy A |
| `CMP3` | `sign(value(P)-value(Q))` as a one-trit word |

This is a mathematical subset of the calculus/normtheory operators, not
an ISA decoder.

## Calculus link

On `CoeffWord`, `D_coeff` drops `c_0`, `I_a` prepends a trit, `S`
prepends `0`.

`D(normalize(P)) = normalize(D_coeff(P))` holds when `c_0` is already
a trit. It **fails** if `c_0` is noncanonical: the low coefficient
still contributes to the integer until it is rewritten. Smallest
witness: `[2]` (`D` of the NF is `1`, `D_coeff` of the raw word is
`0`).
