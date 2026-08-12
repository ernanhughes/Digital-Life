# Stage 1 — Replay Integrity

```json
{
  "groups": 64,
  "summary": {
    "aligned": {
      "requested_total": {
        "n": 64,
        "mean": 292.0,
        "median": 292.0,
        "std": 0.0,
        "ci95_low": 292.0,
        "ci95_high": 292.0,
        "min": 292.0,
        "max": 292.0
      },
      "applied_total": {
        "n": 64,
        "mean": 292.0,
        "median": 292.0,
        "std": 0.0,
        "ci95_low": 292.0,
        "ci95_high": 292.0,
        "min": 292.0,
        "max": 292.0
      },
      "truncation_rate": 0.0
    },
    "shuffled": {
      "requested_total": {
        "n": 64,
        "mean": 292.0,
        "median": 292.0,
        "std": 0.0,
        "ci95_low": 292.0,
        "ci95_high": 292.0,
        "min": 292.0,
        "max": 292.0
      },
      "applied_total": {
        "n": 64,
        "mean": 289.640625,
        "median": 291.0,
        "std": 3.7054317709782487,
        "ci95_low": 288.71875,
        "ci95_high": 290.539453125,
        "min": 276.0,
        "max": 292.0
      },
      "truncation_rate": 0.034375
    },
    "shifted": {
      "requested_total": {
        "n": 64,
        "mean": 292.0,
        "median": 292.0,
        "std": 0.0,
        "ci95_low": 292.0,
        "ci95_high": 292.0,
        "min": 292.0,
        "max": 292.0
      },
      "applied_total": {
        "n": 64,
        "mean": 289.53125,
        "median": 291.0,
        "std": 3.9329090299039464,
        "ci95_low": 288.5625,
        "ci95_high": 290.414453125,
        "min": 271.0,
        "max": 292.0
      },
      "truncation_rate": 0.03671875
    }
  },
  "requested_totals_exactly_equal": true,
  "status": "MEASURED",
  "bounded_statement": "Requested copy quantity is exact by construction. Applied copy quantity and truncation are audited because timing can alter later eligibility."
}
```
