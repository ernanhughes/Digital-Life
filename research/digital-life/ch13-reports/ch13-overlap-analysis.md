# Chapter 13 — Outlier Overlap / Positivity Analysis

## Purpose

This analysis tests whether the Chapter 13 comparison between same-family and
different-family motion pairs has adequate spatial overlap.

It reuses the **exact pair-construction and matched-analysis implementation**
from `ch11_outlier_distance_matched.py`.

It does not silently substitute a new matching estimator.

## Source specimen

- Database: `data\digital-life\outlier.sqlite3`
- Outlier run ID: **1**
- Grid: **512 × 512**
- Generations: **1600**
- Persisted pair dataset key: `f58110a7b2263f3a619481df`
- Pair records: **2,617,077**

## Original Chapter 13 pair-construction parameters

```json
{
  "pair_radius": 96.0,
  "flow_radius": 48.0,
  "density_radius": 32.0,
  "flow_min_neighbors": 3,
  "max_pairs_per_tick": 2500,
  "time_bin_width": 25,
  "max_matches_per_stratum": 5000,
  "seed": 42
}
```

Distance bins are the original Chapter 13 bins:

```text
[0.0, 4.0, 8.0, 12.0, 16.0, 24.0, 32.0, 48.0, 64.0, 96.0]
```

## Primary common-support rule

> largest contiguous ORIGINAL Chapter 13 distance-bin region with at least 100 same-family and 100 different-family raw pair records per bin

Primary threshold:

**100 rows per group per distance bin**

Resulting common-support interval:

**[4.0, 64.0) cells**

Coverage:

- same-family inside: **196,657 / 710,596**
- different-family inside: **951,361 / 1,906,481**
- supported distance bins: **7 / 9**

## Estimand A — raw descriptive effect inside common support

This estimate is descriptive only. It weights every pair equally and does not
balance the original time/distance/density strata.

```json
{
  "same_mean": 0.1732066656062538,
  "different_mean": 0.1165883464790153,
  "difference": 0.05661831912723851,
  "same_n": 196657,
  "different_n": 951361
}
```

## Estimands B/C — original balanced matching inside common support

The original Chapter 13 matcher performs exact matching on:

```text
time_bin
distance_bin
density_bin
```

Within each stratum it selects equal numbers of same-family and
different-family pairs.

Results:

- matched same-family mean: **+0.150823**
- matched different-family mean: **+0.157890**
- balanced matched pooled effect: **-0.007067**
- equal-stratum effect: **-0.026463**
- bootstrap 95% interval: **[-0.066450, +0.012172]**
- matched pairs per group: **64,948**
- matched strata: **659**

### Why the matched pooled and equal-stratum effects differ

They are different estimands.

The matched pooled effect gives strata weight in proportion to the number of
matched pairs they contribute.

The equal-stratum effect first computes one same-minus-different effect for
each matched stratum and then gives every stratum equal weight.

A difference between them is therefore expected when large and small strata
have different effects.

## Original apparent family gap

Before spatial matching, the stronger pair-excluded analysis reported:

- same recent-c2 ancestor: **0.746**
- comparison group: **0.101**
- apparent gap: **0.645**

Inside primary common support, the upper bootstrap bound is:

**+0.012172**

As a fraction of the original apparent gap:

**1.89%**

This is the useful quantitative bound.

## Support-threshold sensitivity

The support rule was repeated under several minimum-count thresholds.

```json
[
  {
    "threshold": 50,
    "supported": true,
    "lower": 4.0,
    "upper": 96.0,
    "same_raw_n": 196717,
    "different_raw_n": 1906468,
    "raw_effect": 0.07382230959121897,
    "matched_pairs_per_group": 65008,
    "matched_strata": 661,
    "matched_same_mean": 0.1515076343686673,
    "matched_different_mean": 0.1573563370270071,
    "matched_pooled_effect": -0.0058487026583398105,
    "equal_stratum_effect": -0.018156441822795782,
    "bootstrap_95_low": -0.05810687328244094,
    "bootstrap_95_high": 0.02366389314544426
  },
  {
    "threshold": 100,
    "supported": true,
    "lower": 4.0,
    "upper": 64.0,
    "same_raw_n": 196657,
    "different_raw_n": 951361,
    "raw_effect": 0.05661831912723851,
    "matched_pairs_per_group": 64948,
    "matched_strata": 659,
    "matched_same_mean": 0.15082315233393326,
    "matched_different_mean": 0.15788972569829532,
    "matched_pooled_effect": -0.007066573364362061,
    "equal_stratum_effect": -0.026462612862070547,
    "bootstrap_95_low": -0.06645028719387464,
    "bootstrap_95_high": 0.012172493449979185
  },
  {
    "threshold": 250,
    "supported": true,
    "lower": 4.0,
    "upper": 64.0,
    "same_raw_n": 196657,
    "different_raw_n": 951361,
    "raw_effect": 0.05661831912723851,
    "matched_pairs_per_group": 64948,
    "matched_strata": 659,
    "matched_same_mean": 0.15082315233393326,
    "matched_different_mean": 0.15788972569829532,
    "matched_pooled_effect": -0.007066573364362061,
    "equal_stratum_effect": -0.026462612862070547,
    "bootstrap_95_low": -0.06645028719387464,
    "bootstrap_95_high": 0.012172493449979185
  },
  {
    "threshold": 500,
    "supported": true,
    "lower": 4.0,
    "upper": 64.0,
    "same_raw_n": 196657,
    "different_raw_n": 951361,
    "raw_effect": 0.05661831912723851,
    "matched_pairs_per_group": 64948,
    "matched_strata": 659,
    "matched_same_mean": 0.15082315233393326,
    "matched_different_mean": 0.15788972569829532,
    "matched_pooled_effect": -0.007066573364362061,
    "equal_stratum_effect": -0.026462612862070547,
    "bootstrap_95_low": -0.06645028719387464,
    "bootstrap_95_high": 0.012172493449979185
  }
]
```

The conclusion is more credible if the support interval and matched effect do
not depend qualitatively on one arbitrary count threshold.

CSV:

`research\digital-life\ch13-reports\ch13-overlap-sensitivity.csv`

## Distance-bin counts

CSV:

`research\digital-life\ch13-reports\ch13-distance-bin-counts.csv`

## Figures

- `static\images\books\digital-life\ch13-outlier-distance-overlap.png`
- `static\images\books\digital-life\ch13-outlier-overlap-effect-by-distance.png`

## Bounded conclusion

> **Within the empirically supported distance region [4.0, 64.0) cells under the declared minimum-count criterion, the original balanced time/distance/density matching gives a same-family minus different-family effect of -0.0071. The equal-stratum effect is -0.0265 with a bootstrap 95% interval [-0.0665, +0.0122]. The upper bound is 1.9% of the original apparent 0.645 family gap. Outside adequate common support, especially at the shortest separations if different-family controls are sparse there, this experiment does not identify an independent ancestry effect.**

## Scope limitation

This analysis hardens inference only for the existing Chapter 13 Outlier run.

It does **not** establish that the same result applies to the larger published
causal regime.

```text
our run
512 × 512
1,600 generations

published causal study
1024 × 1024
20,000 updates
```

The very-short-range region should be described as unresolved whenever the
different-family comparison population is insufficient for the declared
common-support criterion.

## Evidence architecture improvement

The derived pair-level evidence is now persisted in SQLite:

```text
ch13_pair_datasets
ch13_pair_records
```

Future overlap, matching, or sensitivity analyses can therefore operate on
the same frozen pair dataset instead of silently reconstructing it.
