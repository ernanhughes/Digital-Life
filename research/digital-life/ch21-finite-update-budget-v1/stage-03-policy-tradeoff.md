# Stage 3 — At Equal Budget, What Gets Built?

```json
{
  "role": "PRIMARY FIXED-BUDGET ALLOCATION TRADEOFF",
  "budget": 256,
  "loss_rate": 0.08,
  "policies_use_history": false,
  "policy_summary": {
    "high_support": {
      "mean_late_population": 1923.1649305555554,
      "mean_reoccupation_per_loss": 0.9587803634787203,
      "mean_first_occupations_per_1000_evals": 187.5623346430792,
      "mean_reoccupations_per_1000_evals": 456.1111659406393,
      "mean_lost_site_reoccupied_fraction": 0.9757026466405115,
      "mean_evaluation_fraction": 0.8409969058995337,
      "mean_late_net": 24.272569444444446,
      "collapsed_fraction": 0.0
    },
    "neutral": {
      "mean_late_population": 1722.7569444444443,
      "mean_reoccupation_per_loss": 0.8439579238175184,
      "mean_first_occupations_per_1000_evals": 212.15684919727119,
      "mean_reoccupations_per_1000_evals": 379.45303942824984,
      "mean_lost_site_reoccupied_fraction": 0.8878280180013007,
      "mean_evaluation_fraction": 0.6526805146628013,
      "mean_late_net": 10.041666666666666,
      "collapsed_fraction": 0.0
    },
    "low_support": {
      "mean_late_population": 1130.779513888889,
      "mean_reoccupation_per_loss": 0.533529684606526,
      "mean_first_occupations_per_1000_evals": 249.14525447081232,
      "mean_reoccupations_per_1000_evals": 189.65040888951148,
      "mean_lost_site_reoccupied_fraction": 0.5423924058963626,
      "mean_evaluation_fraction": 0.5264750798162504,
      "mean_late_net": -1.5399305555555556,
      "collapsed_fraction": 0.0
    }
  },
  "high_minus_low_reoccupation_per_loss": {
    "n": 48,
    "mean": 0.42525067887219437,
    "median": 0.4242884192440429,
    "std": 0.010958624535401987,
    "ci95_low": 0.4223096370669325,
    "ci95_high": 0.4284771275434652
  },
  "reoccupation_directional_test": {
    "observed_mean": 0.42525067887219437,
    "p_value": 0.00024993751562109475,
    "alternative": "greater",
    "permutations": 4000
  },
  "reoccupation_sei": 0.15,
  "low_minus_high_first_occupations_per_1000_evals": {
    "n": 48,
    "mean": 61.582919827733086,
    "median": 61.52668206393129,
    "std": 5.90981717974606,
    "ci95_low": 59.90029819126394,
    "ci95_high": 63.15771837751961
  },
  "first_occupation_directional_test": {
    "observed_mean": 61.582919827733086,
    "p_value": 0.00024993751562109475,
    "alternative": "greater",
    "permutations": 4000
  },
  "first_occupation_sei": 100.0,
  "status": "MEASURED"
}
```
