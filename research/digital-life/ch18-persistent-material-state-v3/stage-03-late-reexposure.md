# Stage 3 — Does Propagated Experience Alter Later Response?

```json
{
  "groups": 40,
  "challenge_step": 14,
  "challenge_pulse_zero_index": 0,
  "observation_steps": [
    1,
    2,
    4
  ],
  "primary_endpoint": 2,
  "primary_contrast": "difference in later-pulse response between propagated-state retained and propagated-state erased branches with identical visible morphology",
  "results": {
    "1": {
      "statistic": 0.1619246714875878,
      "p_value": 0.9826782145236509,
      "permutations": 1500,
      "null_mean": 0.3012599491305881,
      "null_q95": 0.4083174701648819,
      "null_q99": 0.4414184120919785
    },
    "2": {
      "statistic": 0.20254827531668212,
      "p_value": 0.8001332445036642,
      "permutations": 1500,
      "null_mean": 0.2558175923246884,
      "null_q95": 0.36159631001696013,
      "null_q99": 0.3984155962499989
    },
    "4": {
      "statistic": 0.19443949612510714,
      "p_value": 0.3251165889407062,
      "permutations": 1500,
      "null_mean": 0.1773820435001114,
      "null_q95": 0.24879782050051547,
      "null_q99": 0.26431874013262757
    }
  },
  "primary_test": {
    "statistic": 0.20254827531668212,
    "p_value": 0.8001332445036642,
    "permutations": 1500,
    "null_mean": 0.2558175923246884,
    "null_q95": 0.36159631001696013,
    "null_q99": 0.3984155962499989
  },
  "alpha": 0.05,
  "status": "FAILED",
  "bounded_statement": "Retained propagated material state did not establish a changed morphology response to a later identical pulse under this exploratory protocol."
}
```
