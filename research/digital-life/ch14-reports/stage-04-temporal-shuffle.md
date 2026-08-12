# Stage 4 — Destroy Temporal Order

For each nonconstant source, the exact sampled values are shuffled before
growth. This preserves the value distribution while destroying temporal order.

Standardized morphology-centroid shifts, ordered vs shuffled:

```json
{
  "sine": 0.48957346226750753,
  "square": 1.6077134021692885,
  "saw": 0.3744639997402444,
  "white_noise": 0.27005595279400363,
  "random_walk": 0.24750345227751006
}
```

Cached shuffled runs reused: **0/600**

A nonzero descriptive shift is not enough by itself. Stage 7 asks whether
ordered and shuffled crystals can actually be distinguished on held-out runs.
