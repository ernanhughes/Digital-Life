# Chapter 28 — Does a Causal Individual Emerge? (V1)

## Run metadata

```json
{
  "experiment_version": "digital-crystal-causal-modularity-v1",
  "schema_version": 1,
  "chapter": 28,
  "chapter_title": "Does a Causal Individual Emerge?",
  "profile": "full",
  "seed": 20260916,
  "fresh_seed": true,
  "horizon": 8,
  "region_radii": [
    2,
    3,
    4,
    5
  ],
  "primary_region_radius": 4,
  "module_SEI": 0.15,
  "allocation_policy": "true_unbounded",
  "started_at_unix": 1786652449.8744862,
  "finished_at_unix": 1786657561.3276806,
  "final_status": "CAUSAL_MODULARITY_SUPPORTED"
}
```

---

## Stage 0 — Frozen Chapter 28 V1 Protocol

```json
{
  "status": "FROZEN",
  "question": "Does a predeclared spatial region exhibit stronger internal causal retention than penetration from an equivalently local external perturbation?",
  "primary_radius": 4,
  "primary_metric": "internal_retention - external_penetration",
  "module_SEI": 0.15,
  "causal_mass": "sum absolute expected probability differences over H=8",
  "allocation": "true_unbounded",
  "region_selection": "outcome-blind fixed-radius disks; no module-score maximization",
  "forbidden_claims": [
    "organism",
    "self",
    "agent",
    "autonomy",
    "homeostasis",
    "life"
  ],
  "stop_rule": "No radius or metric rescue. Increase groups only if unresolved solely because MDE exceeds SEI."
}
```

---

## Stage 1 — Candidate Region Support

```json
{
  "2": {
    "groups_with_regions": 170,
    "coverage_fraction": 0.8854166666666666,
    "regions": 406,
    "mean_regions_per_requested_group": 2.1145833333333335
  },
  "3": {
    "groups_with_regions": 192,
    "coverage_fraction": 1.0,
    "regions": 576,
    "mean_regions_per_requested_group": 3.0
  },
  "4": {
    "groups_with_regions": 192,
    "coverage_fraction": 1.0,
    "regions": 576,
    "mean_regions_per_requested_group": 3.0
  },
  "5": {
    "groups_with_regions": 192,
    "coverage_fraction": 1.0,
    "regions": 576,
    "mean_regions_per_requested_group": 3.0
  }
}
```

---

## Stage 2 — Construct Validity

```json
{
  "primary_radius": 4,
  "group_coverage_fraction": 1.0,
  "required_group_coverage": 0.9,
  "mean_regions_per_covered_group": 3.0,
  "required_mean_regions_per_covered_group": 2.0,
  "far_expected_effect_max_abs": 0.0,
  "far_assertion_tolerance": 1e-12,
  "far_zero_assertion_pass": true,
  "outcome_dependent_region_selection": false,
  "scientific_valid": true,
  "status": "PASS"
}
```

---

## Stage 3 — Primary Causal Modularity Test

```json
{
  "primary_radius": 4,
  "module_score": {
    "n": 192,
    "mean": 0.4402085598899139,
    "sd": 0.14924454599771653,
    "se": 0.010770797350858142,
    "ci95_low": 0.4193782331581624,
    "ci95_high": 0.4614487176025127,
    "achieved_mde80_one_sided": 0.026781316840711427
  },
  "status": "SUPPORTED",
  "internal_retention": {
    "n": 192,
    "mean": 0.7755433652328604,
    "sd": 0.12484573806310367,
    "se": 0.009009965059738802,
    "ci95_low": 0.7578066618727277,
    "ci95_high": 0.7934937962507193,
    "achieved_mde80_one_sided": 0.022403051615243634
  },
  "external_penetration": {
    "n": 192,
    "mean": 0.3353348053429466,
    "sd": 0.1133706106424294,
    "se": 0.008181819071574859,
    "ci95_low": 0.3191772603099483,
    "ci95_high": 0.35127384969474257,
    "achieved_mde80_one_sided": 0.02034388743482986
  },
  "SEI": 0.15
}
```

---

## Stage 4 — Descriptive Spatial Scale Sweep

```json
{
  "2": {
    "internal_retention": {
      "n": 170,
      "mean": 0.3984547752041692,
      "sd": 0.14585972065904798,
      "se": 0.01118692990285473,
      "ci95_low": 0.37663462981611884,
      "ci95_high": 0.4203769377585047,
      "achieved_mde80_one_sided": 0.027816019969896803
    },
    "external_penetration": {
      "n": 170,
      "mean": 0.20130247549431216,
      "sd": 0.12157968772844799,
      "se": 0.009324736384271589,
      "ci95_low": 0.18333941588067562,
      "ci95_high": 0.22026190316233485,
      "achieved_mde80_one_sided": 0.023185722600508368
    },
    "module_score": {
      "n": 170,
      "mean": 0.19715229970985704,
      "sd": 0.1404191138386659,
      "se": 0.010769654407923003,
      "ci95_low": 0.17582658318816458,
      "ci95_high": 0.21878676957297435,
      "achieved_mde80_one_sided": 0.02677847494183619
    }
  },
  "3": {
    "internal_retention": {
      "n": 192,
      "mean": 0.6838484947804119,
      "sd": 0.12242081577408676,
      "se": 0.008834961367697822,
      "ci95_low": 0.6669048214702409,
      "ci95_high": 0.7009524395852288,
      "achieved_mde80_one_sided": 0.021967909334484784
    },
    "external_penetration": {
      "n": 192,
      "mean": 0.30982028059792044,
      "sd": 0.1028695582426854,
      "se": 0.007423970892854038,
      "ci95_low": 0.295444203794049,
      "ci95_high": 0.3248798537178577,
      "achieved_mde80_one_sided": 0.01845951699034635
    },
    "module_score": {
      "n": 192,
      "mean": 0.3740282141824915,
      "sd": 0.14708291869468443,
      "se": 0.010614795337696487,
      "ci95_low": 0.3533099990849779,
      "ci95_high": 0.3943330841136429,
      "achieved_mde80_one_sided": 0.026393421756793777
    }
  },
  "4": {
    "internal_retention": {
      "n": 192,
      "mean": 0.7755433652328604,
      "sd": 0.12484573806310367,
      "se": 0.009009965059738802,
      "ci95_low": 0.7575914707550887,
      "ci95_high": 0.7933186125377293,
      "achieved_mde80_one_sided": 0.022403051615243634
    },
    "external_penetration": {
      "n": 192,
      "mean": 0.3353348053429466,
      "sd": 0.1133706106424294,
      "se": 0.008181819071574859,
      "ci95_low": 0.31963853883338667,
      "ci95_high": 0.351695901700746,
      "achieved_mde80_one_sided": 0.02034388743482986
    },
    "module_score": {
      "n": 192,
      "mean": 0.4402085598899139,
      "sd": 0.14924454599771653,
      "se": 0.010770797350858142,
      "ci95_low": 0.4192057325475149,
      "ci95_high": 0.46091907739061455,
      "achieved_mde80_one_sided": 0.026781316840711427
    }
  },
  "5": {
    "internal_retention": {
      "n": 192,
      "mean": 0.8064391225565278,
      "sd": 0.12210958936103435,
      "se": 0.008812500536028481,
      "ci95_low": 0.7884477392553441,
      "ci95_high": 0.8240648939673977,
      "achieved_mde80_one_sided": 0.021912061041192497
    },
    "external_penetration": {
      "n": 192,
      "mean": 0.30260936280937184,
      "sd": 0.10003910184651625,
      "se": 0.007219700297571819,
      "ci95_low": 0.28866762180305633,
      "ci95_high": 0.31671314906090015,
      "achieved_mde80_one_sided": 0.017951603290432758
    },
    "module_score": {
      "n": 192,
      "mean": 0.503829759747156,
      "sd": 0.1482116503175301,
      "se": 0.010696254525983087,
      "ci95_low": 0.4826599066148461,
      "ci95_high": 0.5243023194499038,
      "achieved_mde80_one_sided": 0.026595967980627133
    }
  }
}
```

---

## Stage 5 — Structural Controls

```json
{
  "far_zero": {
    "max_abs_expected_effect": 0.0,
    "status": "PASS",
    "role": "STRUCTURAL_ASSERTION_NOT_FINDING"
  },
  "region_geometry": {
    "selection_uses_module_score": false,
    "selection_uses_outcomes": false,
    "selection_basis": "occupancy fraction closeness to 0.50, radial distance, axial coordinates"
  },
  "note": "Matched-region geometric null is reserved as secondary follow-up if primary support and runtime justify it; V1 does not promote visual geometry into individuality evidence."
}
```

---

## Stage 6 — Chapter 28 V1 Verdict

```json
{
  "validity": {
    "primary_radius": 4,
    "group_coverage_fraction": 1.0,
    "required_group_coverage": 0.9,
    "mean_regions_per_covered_group": 3.0,
    "required_mean_regions_per_covered_group": 2.0,
    "far_expected_effect_max_abs": 0.0,
    "far_assertion_tolerance": 1e-12,
    "far_zero_assertion_pass": true,
    "outcome_dependent_region_selection": false,
    "scientific_valid": true,
    "status": "PASS"
  },
  "primary_status": "SUPPORTED",
  "overall_status": "CAUSAL_MODULARITY_SUPPORTED",
  "bounded_claim": "At the frozen radius-4 scale, internally initiated perturbations were retained inside predeclared regions more strongly than equivalently local externally initiated perturbations penetrated those regions, by more than the frozen 0.15 module-score margin.",
  "claim_boundary": {
    "supported_if_positive": "causally modular spatial region under this operational test",
    "not_established": [
      "organism",
      "self",
      "agent",
      "autonomy",
      "homeostasis",
      "life"
    ]
  },
  "stop_rule": "No radius or metric rescue. Increase independent groups only if UNRESOLVED solely because MDE exceeds SEI."
}
```
