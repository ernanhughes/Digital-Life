# Chapter 28 V2 — Spatial-Overlap Robustness Audit

> **Epistemic status: POST-HOC ROBUSTNESS ONLY.** This audit does not replace or modify the frozen V2 result.

## Baseline reproduction

The audit first re-aggregates all existing V2 pairs using the group as the independent unit.

```text
groups             192
pairs              1151
mean excess M      -0.012225
95% CI             [-0.033122, 0.008056]
```

## Existing-pair spatial overlap

```text
matched pairs                    1151
strict non-overlap pairs         339
strict non-overlap fraction      0.2945
pairs center distance <= 1       179
pairs center distance <= 2       299
pairs disk overlap >= 0.50       400
pairs disk overlap >= 0.75       179
```

Center-distance quantiles:

```json
{
  "min": 1.0,
  "q05": 1.0,
  "q25": 2.0,
  "median": 5.0,
  "q75": 9.0,
  "q95": 20.0,
  "max": 34.0,
  "mean": 7.005212858384014
}
```

Disk-overlap-fraction quantiles:

```json
{
  "min": 0.0,
  "q05": 0.0,
  "q25": 0.0,
  "median": 0.32786885245901637,
  "q75": 0.7049180327868853,
  "q95": 0.8524590163934426,
  "max": 0.8524590163934426,
  "mean": 0.35363404594721626
}
```

Probe-overlap-fraction quantiles:

```json
{
  "min": 0.0,
  "q05": 0.0,
  "q25": 0.0,
  "median": 0.4,
  "q75": 0.6666666666666666,
  "q95": 1.0,
  "max": 1.0,
  "mean": 0.39916015059368665
}
```

Occupied-cell-overlap-fraction quantiles:

```json
{
  "min": 0.0,
  "q05": 0.0,
  "q25": 0.0,
  "median": 0.3,
  "q75": 0.6896551724137931,
  "q95": 0.9,
  "max": 1.0,
  "mean": 0.36519604891466084
}
```

## Post-hoc sensitivity grid

Each row recomputes the excess-modularity contrast after a spatial-distinctness filter. Within an observed region, retained controls are averaged first; observed regions are then averaged within group. Groups remain the independent statistical unit.

| Filter | Pairs | Groups | Coverage | Mean excess M | 95% CI | MDE80 | Reference only |
|---|---:|---:|---:|---:|---:|---:|---|
| baseline_all_existing_pairs | 1151 | 192 | 1.000 | -0.0122 | [-0.0331, 0.0081] | 0.0265 | CONSISTENT_WITH_FROZEN_BOUNDED_BELOW_SEI |
| center_distance_ge_2 | 972 | 192 | 1.000 | -0.0166 | [-0.0396, 0.0068] | 0.0297 | CONSISTENT_WITH_FROZEN_BOUNDED_BELOW_SEI |
| center_distance_ge_4 | 751 | 191 | 0.995 | -0.0172 | [-0.0462, 0.0110] | 0.0366 | CONSISTENT_WITH_FROZEN_BOUNDED_BELOW_SEI |
| center_distance_ge_6 | 554 | 183 | 0.953 | -0.0185 | [-0.0514, 0.0147] | 0.0419 | CONSISTENT_WITH_FROZEN_BOUNDED_BELOW_SEI |
| center_distance_ge_8 | 399 | 158 | 0.823 | -0.0050 | [-0.0422, 0.0327] | 0.0473 | CONSISTENT_WITH_FROZEN_BOUNDED_BELOW_SEI |
| center_distance_ge_9 | 339 | 140 | 0.729 | -0.0120 | [-0.0505, 0.0274] | 0.0496 | CONSISTENT_WITH_FROZEN_BOUNDED_BELOW_SEI |
| disk_overlap_fraction_le_0_75 | 972 | 192 | 1.000 | -0.0166 | [-0.0409, 0.0063] | 0.0297 | CONSISTENT_WITH_FROZEN_BOUNDED_BELOW_SEI |
| disk_overlap_fraction_le_0_5 | 751 | 191 | 0.995 | -0.0172 | [-0.0456, 0.0121] | 0.0366 | CONSISTENT_WITH_FROZEN_BOUNDED_BELOW_SEI |
| disk_overlap_fraction_le_0_25 | 536 | 181 | 0.943 | -0.0167 | [-0.0491, 0.0155] | 0.0420 | CONSISTENT_WITH_FROZEN_BOUNDED_BELOW_SEI |
| disk_overlap_fraction_le_0_1 | 428 | 165 | 0.859 | -0.0093 | [-0.0461, 0.0292] | 0.0469 | CONSISTENT_WITH_FROZEN_BOUNDED_BELOW_SEI |
| disk_overlap_fraction_le_0_0 | 339 | 140 | 0.729 | -0.0120 | [-0.0513, 0.0273] | 0.0496 | CONSISTENT_WITH_FROZEN_BOUNDED_BELOW_SEI |
| strict_disk_nonoverlap | 339 | 140 | 0.729 | -0.0120 | [-0.0502, 0.0277] | 0.0496 | CONSISTENT_WITH_FROZEN_BOUNDED_BELOW_SEI |
| occupied_overlap_fraction_smaller_le_0_75 | 926 | 192 | 1.000 | -0.0213 | [-0.0463, 0.0028] | 0.0313 | CONSISTENT_WITH_FROZEN_BOUNDED_BELOW_SEI |
| occupied_overlap_fraction_smaller_le_0_5 | 706 | 190 | 0.990 | -0.0066 | [-0.0369, 0.0238] | 0.0389 | CONSISTENT_WITH_FROZEN_BOUNDED_BELOW_SEI |
| occupied_overlap_fraction_smaller_le_0_25 | 541 | 183 | 0.953 | -0.0133 | [-0.0458, 0.0195] | 0.0414 | CONSISTENT_WITH_FROZEN_BOUNDED_BELOW_SEI |
| occupied_overlap_fraction_smaller_le_0_1 | 442 | 169 | 0.880 | -0.0167 | [-0.0534, 0.0199] | 0.0468 | CONSISTENT_WITH_FROZEN_BOUNDED_BELOW_SEI |
| occupied_overlap_fraction_smaller_le_0_0 | 365 | 150 | 0.781 | -0.0061 | [-0.0467, 0.0320] | 0.0498 | CONSISTENT_WITH_FROZEN_BOUNDED_BELOW_SEI |

## Interpretation boundary

This audit may support statements such as:

```text
the frozen V2 result is / is not robust when near-overlapping
selected-control pairs are removed
```

It does **not** change the frozen V2 status and does not create a new confirmatory threshold.

If strict spatial separation leaves poor support, the correct next step is an explicitly labelled outcome-blind rematching sensitivity analysis — not weakening the separation rule after looking at the causal result.

## Warnings

- Strict non-overlap retains fewer than 90% of groups. Do not treat the strict-filter estimate as a clean replacement for frozen V2; consider a separately labelled outcome-blind rematching sensitivity analysis.
