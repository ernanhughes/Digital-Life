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
        "mean": 291.421875,
        "median": 292.0,
        "std": 2.6089071436858386,
        "ci95_low": 290.726171875,
        "ci95_high": 291.875,
        "min": 272.0,
        "max": 292.0
      },
      "truncation_rate": 0.01171875
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
        "mean": 290.0,
        "median": 292.0,
        "std": 5.1020829079896375,
        "ci95_low": 288.671875,
        "ci95_high": 291.109375,
        "min": 266.0,
        "max": 292.0
      },
      "truncation_rate": 0.0296875
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
        "mean": 287.78125,
        "median": 292.0,
        "std": 8.316904378282823,
        "ci95_low": 285.476171875,
        "ci95_high": 289.640625,
        "min": 238.0,
        "max": 292.0
      },
      "truncation_rate": 0.05390625
    }
  },
  "requested_totals_exactly_equal": true,
  "status": "MEASURED",
  "bounded_statement": "Requested copy quantity is exact by construction. Applied copy quantity and truncation are audited because timing can alter later eligibility."
}
```
