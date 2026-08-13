# Chapter 28 — Geometry-Matched Causal Modularity Null (V2)

## Run metadata

```json
{
  "experiment_version": "digital-crystal-causal-modularity-v2",
  "schema_version": 2,
  "chapter": 28,
  "chapter_title": "Does Causal Modularity Exceed a Geometry-Matched Null?",
  "profile": "full",
  "seed": 20260917,
  "fresh_seed": true,
  "horizon": 8,
  "region_radius": 4,
  "excess_SEI": 0.1,
  "allocation_policy": "true_unbounded",
  "started_at_unix": 1786658387.812737,
  "finished_at_unix": 1786660811.8207638,
  "final_status": "EXCESS_CAUSAL_MODULARITY_BOUNDED_BELOW_SEI"
}
```

---

## Stage 0 — Frozen Chapter 28 V2 Protocol

```json
{
  "status": "FROZEN",
  "primary_question": "Do V1-selected radius-4 regions exceed geometry-matched same-checkpoint controls in causal modularity?",
  "primary_estimand": "mean_group(observed_module_score - matched_control_module_score)",
  "excess_SEI": 0.1,
  "region_radius": 4,
  "horizon": 8,
  "matching": {
    "same_checkpoint": true,
    "outcome_blind": true,
    "controls_per_observed": 2,
    "features": [
      "occupancy_fraction",
      "center_radial_distance",
      "occupied_count",
      "internal_frontier_count",
      "external_frontier_count",
      "internal_probe_depth_mean",
      "external_probe_depth_mean",
      "boundary_occupied_fraction"
    ],
    "max_occupancy_diff": 0.08,
    "max_radial_diff": 6,
    "max_occupied_count_diff": 8,
    "max_internal_frontier_diff": 4,
    "max_external_frontier_diff": 4,
    "max_standardized_distance": 4.0
  },
  "stop_rule": "No metric/radius/matching rescue. Increase groups only if UNRESOLVED solely because MDE exceeds 0.10."
}
```

---

## Stage 1 — Same-Checkpoint Match Support

```json
{
  "requested_groups": 192,
  "covered_groups": 192,
  "coverage_fraction": 1.0,
  "median_matched_observed_regions_per_covered_group": 3.0,
  "median_controls_per_matched_observed": 2.0,
  "total_matches": 1151,
  "support_rows": [
    {
      "group": 0,
      "candidate_count": 378,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 1,
      "candidate_count": 217,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 2,
      "candidate_count": 289,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 3,
      "candidate_count": 313,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 4,
      "candidate_count": 334,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 5,
      "candidate_count": 343,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 6,
      "candidate_count": 352,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 7,
      "candidate_count": 224,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 8,
      "candidate_count": 235,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 9,
      "candidate_count": 170,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 10,
      "candidate_count": 329,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 11,
      "candidate_count": 221,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 12,
      "candidate_count": 207,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 13,
      "candidate_count": 247,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 14,
      "candidate_count": 324,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 15,
      "candidate_count": 228,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 16,
      "candidate_count": 270,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 17,
      "candidate_count": 324,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 18,
      "candidate_count": 263,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 19,
      "candidate_count": 294,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 20,
      "candidate_count": 393,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 21,
      "candidate_count": 332,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 22,
      "candidate_count": 250,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 23,
      "candidate_count": 346,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 24,
      "candidate_count": 255,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 25,
      "candidate_count": 418,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 26,
      "candidate_count": 232,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 27,
      "candidate_count": 310,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 28,
      "candidate_count": 262,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 29,
      "candidate_count": 235,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 30,
      "candidate_count": 291,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 31,
      "candidate_count": 316,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 32,
      "candidate_count": 299,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 33,
      "candidate_count": 373,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 34,
      "candidate_count": 329,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 35,
      "candidate_count": 258,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 36,
      "candidate_count": 268,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 37,
      "candidate_count": 286,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 38,
      "candidate_count": 313,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 39,
      "candidate_count": 311,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 40,
      "candidate_count": 294,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 41,
      "candidate_count": 249,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 42,
      "candidate_count": 307,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 43,
      "candidate_count": 385,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 44,
      "candidate_count": 341,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 45,
      "candidate_count": 320,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 46,
      "candidate_count": 204,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 47,
      "candidate_count": 269,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 48,
      "candidate_count": 412,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 49,
      "candidate_count": 390,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 50,
      "candidate_count": 315,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 51,
      "candidate_count": 329,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 52,
      "candidate_count": 325,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 53,
      "candidate_count": 263,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 54,
      "candidate_count": 284,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 55,
      "candidate_count": 396,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 56,
      "candidate_count": 320,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 57,
      "candidate_count": 328,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 58,
      "candidate_count": 374,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 59,
      "candidate_count": 325,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 60,
      "candidate_count": 300,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 61,
      "candidate_count": 297,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 62,
      "candidate_count": 312,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 63,
      "candidate_count": 285,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 64,
      "candidate_count": 232,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 65,
      "candidate_count": 297,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 66,
      "candidate_count": 420,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 67,
      "candidate_count": 242,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 68,
      "candidate_count": 341,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 69,
      "candidate_count": 332,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 70,
      "candidate_count": 307,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 71,
      "candidate_count": 314,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 72,
      "candidate_count": 176,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 73,
      "candidate_count": 327,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 74,
      "candidate_count": 341,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 75,
      "candidate_count": 282,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 76,
      "candidate_count": 298,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 77,
      "candidate_count": 284,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 78,
      "candidate_count": 210,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 79,
      "candidate_count": 211,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 80,
      "candidate_count": 158,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 81,
      "candidate_count": 344,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 82,
      "candidate_count": 326,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 83,
      "candidate_count": 269,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 84,
      "candidate_count": 367,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 85,
      "candidate_count": 272,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 86,
      "candidate_count": 320,
      "observed_count": 3,
      "matched_pair_count": 5,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 87,
      "candidate_count": 285,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 88,
      "candidate_count": 230,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 89,
      "candidate_count": 240,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 90,
      "candidate_count": 254,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 91,
      "candidate_count": 354,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 92,
      "candidate_count": 253,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 93,
      "candidate_count": 223,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 94,
      "candidate_count": 354,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 95,
      "candidate_count": 364,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 96,
      "candidate_count": 315,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 97,
      "candidate_count": 303,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 98,
      "candidate_count": 390,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 99,
      "candidate_count": 266,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 100,
      "candidate_count": 294,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 101,
      "candidate_count": 278,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 102,
      "candidate_count": 330,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 103,
      "candidate_count": 327,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 104,
      "candidate_count": 347,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 105,
      "candidate_count": 341,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 106,
      "candidate_count": 345,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 107,
      "candidate_count": 384,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 108,
      "candidate_count": 355,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 109,
      "candidate_count": 368,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 110,
      "candidate_count": 362,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 111,
      "candidate_count": 303,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 112,
      "candidate_count": 249,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 113,
      "candidate_count": 336,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 114,
      "candidate_count": 277,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 115,
      "candidate_count": 423,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 116,
      "candidate_count": 344,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 117,
      "candidate_count": 394,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 118,
      "candidate_count": 293,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 119,
      "candidate_count": 274,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 120,
      "candidate_count": 297,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 121,
      "candidate_count": 288,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 122,
      "candidate_count": 377,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 123,
      "candidate_count": 345,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 124,
      "candidate_count": 242,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 125,
      "candidate_count": 334,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 126,
      "candidate_count": 271,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 127,
      "candidate_count": 206,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 128,
      "candidate_count": 251,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 129,
      "candidate_count": 362,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 130,
      "candidate_count": 311,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 131,
      "candidate_count": 390,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 132,
      "candidate_count": 331,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 133,
      "candidate_count": 327,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 134,
      "candidate_count": 369,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 135,
      "candidate_count": 303,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 136,
      "candidate_count": 356,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 137,
      "candidate_count": 332,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 138,
      "candidate_count": 369,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 139,
      "candidate_count": 397,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 140,
      "candidate_count": 292,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 141,
      "candidate_count": 298,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 142,
      "candidate_count": 266,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 143,
      "candidate_count": 277,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 144,
      "candidate_count": 363,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 145,
      "candidate_count": 332,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 146,
      "candidate_count": 265,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 147,
      "candidate_count": 319,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 148,
      "candidate_count": 359,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 149,
      "candidate_count": 215,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 150,
      "candidate_count": 326,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 151,
      "candidate_count": 245,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 152,
      "candidate_count": 346,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 153,
      "candidate_count": 286,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 154,
      "candidate_count": 374,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 155,
      "candidate_count": 266,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 156,
      "candidate_count": 292,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 157,
      "candidate_count": 356,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 158,
      "candidate_count": 348,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 159,
      "candidate_count": 322,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 160,
      "candidate_count": 339,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 161,
      "candidate_count": 358,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 162,
      "candidate_count": 344,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 163,
      "candidate_count": 348,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 164,
      "candidate_count": 284,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 165,
      "candidate_count": 322,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 166,
      "candidate_count": 274,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 167,
      "candidate_count": 343,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 168,
      "candidate_count": 277,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 169,
      "candidate_count": 221,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 170,
      "candidate_count": 396,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 171,
      "candidate_count": 346,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 172,
      "candidate_count": 385,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 173,
      "candidate_count": 195,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 174,
      "candidate_count": 328,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 175,
      "candidate_count": 261,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 176,
      "candidate_count": 322,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 177,
      "candidate_count": 353,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 178,
      "candidate_count": 320,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 179,
      "candidate_count": 395,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 180,
      "candidate_count": 282,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 181,
      "candidate_count": 407,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 182,
      "candidate_count": 291,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 183,
      "candidate_count": 328,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 184,
      "candidate_count": 339,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 185,
      "candidate_count": 233,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 186,
      "candidate_count": 311,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 187,
      "candidate_count": 241,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 188,
      "candidate_count": 215,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 189,
      "candidate_count": 295,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 190,
      "candidate_count": 174,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    },
    {
      "group": 191,
      "candidate_count": 247,
      "observed_count": 3,
      "matched_pair_count": 6,
      "matched_observed_count": 3,
      "supported": true
    }
  ]
}
```

---

## Stage 2 — Geometry Match Quality

```json
{
  "n_matches": 1151,
  "distance": {
    "mean": 1.1766987291296374,
    "median": 1.1234765725661215,
    "max": 3.0623741170091137
  },
  "occupancy_diff": {
    "mean": 0.026990072780618435,
    "max": 0.0655737704918033
  },
  "radial_diff": {
    "mean": 1.7801911381407471,
    "max": 6
  },
  "occupied_count_diff": {
    "mean": 1.6463944396177237,
    "max": 4
  },
  "internal_frontier_diff": {
    "mean": 0.9252823631624674,
    "max": 4
  },
  "external_frontier_diff": {
    "mean": 0.4152910512597741,
    "max": 4
  }
}
```

---

## Stage 3 — Construct Validity

```json
{
  "group_coverage_fraction": 1.0,
  "required_group_coverage": 0.9,
  "median_matched_observed_regions_per_covered_group": 3.0,
  "required_median_matched_observed_regions_per_group": 2.0,
  "median_controls_per_matched_observed": 2.0,
  "required_median_controls_per_observed": 1.0,
  "far_expected_effect_max_abs": 0.0,
  "far_assertion_tolerance": 1e-12,
  "far_zero_assertion_pass": true,
  "matching_outcome_blind": true,
  "same_checkpoint_matching": true,
  "control_reuse_within_group": false,
  "scientific_valid": true,
  "status": "PASS"
}
```

---

## Stage 4 — Excess Causal Modularity Above Geometry Null

```json
{
  "estimand": "observed module score - matched-control module score",
  "EXCESS_SEI": 0.1,
  "result": {
    "n": 192,
    "mean": -0.012264901112053186,
    "sd": 0.14756423546558212,
    "se": 0.010649531383601895,
    "ci95_low": -0.032729925902717345,
    "ci95_high": 0.007196615033407114,
    "achieved_mde80_one_sided": 0.0264797920616916
  },
  "status": "BOUNDED_BELOW_SEI",
  "directional_substatus": "DIRECTION_UNRESOLVED",
  "observed_module_score": {
    "n": 192,
    "mean": 0.443627960584466,
    "sd": 0.15860615504281061,
    "se": 0.01144641328863728,
    "ci95_low": 0.42116114131509336,
    "ci95_high": 0.46581386448068873,
    "achieved_mde80_one_sided": 0.02846121888536886
  },
  "matched_control_module_score": {
    "n": 192,
    "mean": 0.45589286169651927,
    "sd": 0.12161742943563025,
    "se": 0.008776981952851431,
    "ci95_low": 0.4390125487153215,
    "ci95_high": 0.4733017265829603,
    "achieved_mde80_one_sided": 0.02182374497704132
  }
}
```

---

## Stage 5 — Excess-Modularity Decomposition

```json
{
  "excess_internal_retention": {
    "n": 192,
    "mean": -0.006571643933766518,
    "sd": 0.10950487733140293,
    "se": 0.007902833800607804,
    "ci95_low": -0.02218523544540807,
    "ci95_high": 0.009264216769893927,
    "achieved_mde80_one_sided": 0.019650197572113694
  },
  "excess_external_penetration": {
    "n": 192,
    "mean": 0.005693257178286668,
    "sd": 0.10953024950694316,
    "se": 0.007904664879655065,
    "ci95_low": -0.010104673132818766,
    "ci95_high": 0.021587943405820407,
    "achieved_mde80_one_sided": 0.019654750504132342
  },
  "identity": "excess_module = excess_internal_retention - excess_external_penetration",
  "interpretation": {
    "positive_excess_internal_retention": "observed regions retain more internally generated causal mass",
    "negative_excess_external_penetration": "observed regions admit less externally generated causal mass"
  }
}
```

---

## Stage 6 — Chapter 28 V2 Verdict

```json
{
  "validity": {
    "group_coverage_fraction": 1.0,
    "required_group_coverage": 0.9,
    "median_matched_observed_regions_per_covered_group": 3.0,
    "required_median_matched_observed_regions_per_group": 2.0,
    "median_controls_per_matched_observed": 2.0,
    "required_median_controls_per_observed": 1.0,
    "far_expected_effect_max_abs": 0.0,
    "far_assertion_tolerance": 1e-12,
    "far_zero_assertion_pass": true,
    "matching_outcome_blind": true,
    "same_checkpoint_matching": true,
    "control_reuse_within_group": false,
    "scientific_valid": true,
    "status": "PASS"
  },
  "primary_status": "BOUNDED_BELOW_SEI",
  "directional_substatus": "DIRECTION_UNRESOLVED",
  "overall_status": "EXCESS_CAUSAL_MODULARITY_BOUNDED_BELOW_SEI",
  "bounded_claim": "At frozen radius 4, any excess causal modularity of V1-selected regions over same-checkpoint geometry-matched controls was bounded below the predeclared +0.10 meaningful margin.",
  "V1_status_preserved": "RAW_CAUSAL_MODULARITY_SUPPORTED",
  "claim_boundary": {
    "supported_if_positive": "privileged causal region relative to this matched spatial null",
    "not_established": [
      "organism",
      "self",
      "agent",
      "autonomy",
      "biological individual",
      "homeostasis",
      "life"
    ]
  },
  "stop_rule": "No metric/radius/matching rescue. Increase independent groups only if unresolved solely because MDE exceeds 0.10."
}
```
