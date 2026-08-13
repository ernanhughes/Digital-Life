# Stage 4 — Bounded Chapter 24 V1 Verdict

```json
{
  "validity": {
    "valid": true,
    "coverage_gate": true,
    "capacity_gate": true
  },
  "H1": {
    "status": "FAILED",
    "result": {
      "group_delta_G_local": {
        "n": 48,
        "mean": 0.16674107142857142,
        "ci95_low": -0.07830109126984128,
        "ci95_high": 0.43116691468253976,
        "half_width": 0.25473400297619053
      },
      "minimum_effect": 0.15,
      "signflip": {
        "n": 48,
        "observed_mean": 0.16674107142857142,
        "p_value": 0.10536182977127859,
        "permutations": 8000
      }
    }
  },
  "H2": {
    "status": "SUPPORTED",
    "result": {
      "group_delta_promoted_frontier": {
        "n": 48,
        "mean": 1.2588293650793652,
        "ci95_low": 1.1960987103174603,
        "ci95_high": 1.3249410962301589,
        "half_width": 0.0644211929563493
      },
      "minimum_effect": 1.0,
      "signflip": {
        "n": 48,
        "observed_mean": 1.2588293650793652,
        "p_value": 0.00012498437695288088,
        "permutations": 8000
      }
    }
  },
  "overall_status": "FRONTIER_GEOMETRY_CONTRAST_SUPPORTED_GAIN_LINK_FAILED",
  "bounded_claim": "The matched high-FCP sites created more frontier opportunity as designed, but the frozen experiment did not establish a scientifically meaningful increase in transient causal gain.",
  "what_this_does_not_establish": [
    "FCP is the only determinant of causal gain",
    "causal-gain field is a physical field",
    "high-gain regions",
    "spatial clustering",
    "temporal persistence",
    "percolation",
    "criticality",
    "phase transition",
    "coherent structure",
    "natural boundary",
    "individuality",
    "organism",
    "life"
  ],
  "next_if_supported": "Map a validated local gain proxy across whole frontiers and test whether high-gain locations cluster in space beyond matched radial/density controls.",
  "next_if_failed": "Do not add a classifier. Audit which local geometric term actually distinguishes causal gain before attempting spatial maps."
}
```
