import Problems.Juggler.CycleCore
import Problems.Juggler.CycleObstructions
import Problems.Juggler.CycleExtrema

/-!
# Fixed cycle words (re-export)

`CycleCore` plus named-word exclusions plus `CycleExtrema`.
Existing `import Problems.Juggler.Cycles` compiles the three
layers. Declarations live in those files; this barrel does not
restate them. Leftover proofs that need a named word import
`CycleObstructions`. Foundations stay on `CycleCore`.
-/
