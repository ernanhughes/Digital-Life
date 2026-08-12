# Stage 0 — Freeze the Substrate

Digital Crystal v1 is unchanged from Chapter 15. RNG-consuming frontier
traversal remains canonicalized with `sorted(frontier)`.

```json
{
  "canonical_rng_traversal": "sorted(frontier)",
  "repeat_from_identical_state_exact": true,
  "morphology_hash_a": "5fd54c923adbc247272c7ada",
  "morphology_hash_b": "5fd54c923adbc247272c7ada"
}
```

This stage must pass before any message experiment is interpreted.
