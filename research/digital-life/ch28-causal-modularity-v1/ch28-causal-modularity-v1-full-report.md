# Chapter 28 — Does a Causal Individual Emerge? (V1)

## Run metadata

```json
{
  "experiment_version": "digital-crystal-causal-modularity-v1",
  "schema_version": 1,
  "chapter": 28,
  "chapter_title": "Does a Causal Individual Emerge?",
  "profile": "smoke",
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
  "started_at_unix": 1786652391.0207157,
  "finished_at_unix": 1786652417.4293861,
  "final_status": "ENGINEERING_SMOKE_ONLY"
}
```

---

## Stage 0 — Frozen Chapter 28 V1 Protocol

```json
{
  "status": "ENGINEERING_SMOKE_ONLY",
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
    "groups_with_regions": 8,
    "coverage_fraction": 1.0,
    "regions": 8,
    "mean_regions_per_requested_group": 1.0
  },
  "3": {
    "groups_with_regions": 8,
    "coverage_fraction": 1.0,
    "regions": 8,
    "mean_regions_per_requested_group": 1.0
  },
  "4": {
    "groups_with_regions": 8,
    "coverage_fraction": 1.0,
    "regions": 8,
    "mean_regions_per_requested_group": 1.0
  },
  "5": {
    "groups_with_regions": 8,
    "coverage_fraction": 1.0,
    "regions": 8,
    "mean_regions_per_requested_group": 1.0
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
  "mean_regions_per_covered_group": 1.0,
  "required_mean_regions_per_covered_group": 2.0,
  "far_expected_effect_max_abs": 0.0,
  "far_assertion_tolerance": 1e-12,
  "far_zero_assertion_pass": true,
  "outcome_dependent_region_selection": false,
  "scientific_valid": false,
  "status": "FAIL"
}
```

---

## Stage 3 — Primary Causal Modularity Test

```json
{
  "primary_radius": 4,
  "module_score": {
    "n": 8,
    "mean": 0.23246999769379778,
    "sd": 0.3282495070525104,
    "se": 0.11605372617898577,
    "ci95_low": 0.03735984641632997,
    "ci95_high": 0.45890564557611824,
    "achieved_mde80_one_sided": 0.28856467261422897
  },
  "status": "ENGINEERING_SMOKE_ONLY",
  "internal_retention": {
    "n": 8,
    "mean": 0.5125296682425597,
    "sd": 0.27385766642574716,
    "se": 0.09682330650478466,
    "ci95_low": 0.3415982623985618,
    "ci95_high": 0.710826872503087,
    "achieved_mde80_one_sided": 0.24074871753699434
  },
  "external_penetration": {
    "n": 8,
    "mean": 0.280059670548762,
    "sd": 0.12227576868703968,
    "se": 0.04323101260670173,
    "ci95_low": 0.2102938261471885,
    "ci95_high": 0.36354608787294673,
    "achieved_mde80_one_sided": 0.10749282604157667
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
      "n": 8,
      "mean": 0.38467209424227966,
      "sd": 0.17436726334855426,
      "se": 0.06164813716535163,
      "ci95_low": 0.2784673383360166,
      "ci95_high": 0.4850613468716746,
      "achieved_mde80_one_sided": 0.15328654325980592
    },
    "external_penetration": {
      "n": 8,
      "mean": 0.1728692562015241,
      "sd": 0.08653472629024861,
      "se": 0.0305946458839783,
      "ci95_low": 0.11434030839173533,
      "ci95_high": 0.22165857030025554,
      "achieved_mde80_one_sided": 0.07607281785715793
    },
    "module_score": {
      "n": 8,
      "mean": 0.21180283804075556,
      "sd": 0.11407442366161456,
      "se": 0.0403313992655374,
      "ci95_low": 0.14144432837510948,
      "ci95_high": 0.28194330923796584,
      "achieved_mde80_one_sided": 0.10028301036353045
    }
  },
  "3": {
    "internal_retention": {
      "n": 8,
      "mean": 0.47811348528091624,
      "sd": 0.28861140981355193,
      "se": 0.10203954250348612,
      "ci95_low": 0.3105747334919042,
      "ci95_high": 0.6628596462772309,
      "achieved_mde80_one_sided": 0.25371875721432785
    },
    "external_penetration": {
      "n": 8,
      "mean": 0.2517544577017452,
      "sd": 0.16988144712044612,
      "se": 0.060062161628325665,
      "ci95_low": 0.1418538034086901,
      "ci95_high": 0.3600185328682294,
      "achieved_mde80_one_sided": 0.1493430549575842
    },
    "module_score": {
      "n": 8,
      "mean": 0.226359027579171,
      "sd": 0.16580818472962452,
      "se": 0.058622045899274625,
      "ci95_low": 0.12343659163588193,
      "ci95_high": 0.3450421036407349,
      "achieved_mde80_one_sided": 0.14576224340105304
    }
  },
  "4": {
    "internal_retention": {
      "n": 8,
      "mean": 0.5125296682425597,
      "sd": 0.27385766642574716,
      "se": 0.09682330650478466,
      "ci95_low": 0.3414211590909111,
      "ci95_high": 0.7023431221971603,
      "achieved_mde80_one_sided": 0.24074871753699434
    },
    "external_penetration": {
      "n": 8,
      "mean": 0.280059670548762,
      "sd": 0.12227576868703968,
      "se": 0.04323101260670173,
      "ci95_low": 0.20696564095880823,
      "ci95_high": 0.36682762756785936,
      "achieved_mde80_one_sided": 0.10749282604157667
    },
    "module_score": {
      "n": 8,
      "mean": 0.23246999769379778,
      "sd": 0.3282495070525104,
      "se": 0.11605372617898577,
      "ci95_low": 0.018724526477825975,
      "ci95_high": 0.4515510780913731,
      "achieved_mde80_one_sided": 0.28856467261422897
    }
  },
  "5": {
    "internal_retention": {
      "n": 8,
      "mean": 0.6119024440609631,
      "sd": 0.2259992559084821,
      "se": 0.0799028031980008,
      "ci95_low": 0.4616112213268374,
      "ci95_high": 0.7624201304011129,
      "achieved_mde80_one_sided": 0.19867631143725653
    },
    "external_penetration": {
      "n": 8,
      "mean": 0.17754725490674,
      "sd": 0.10418400401005852,
      "se": 0.03683460786333942,
      "ci95_low": 0.11349165241258619,
      "ci95_high": 0.24398508781621125,
      "achieved_mde80_one_sided": 0.09158832644946735
    },
    "module_score": {
      "n": 8,
      "mean": 0.4343551891542231,
      "sd": 0.1875523315777048,
      "se": 0.06630976274297146,
      "ci95_low": 0.2952674074897825,
      "ci95_high": 0.556317268169343,
      "achieved_mde80_one_sided": 0.1648775580677351
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
    "mean_regions_per_covered_group": 1.0,
    "required_mean_regions_per_covered_group": 2.0,
    "far_expected_effect_max_abs": 0.0,
    "far_assertion_tolerance": 1e-12,
    "far_zero_assertion_pass": true,
    "outcome_dependent_region_selection": false,
    "scientific_valid": false,
    "status": "FAIL"
  },
  "primary_status": "ENGINEERING_SMOKE_ONLY",
  "overall_status": "ENGINEERING_SMOKE_ONLY",
  "bounded_claim": "Engineering smoke profile only.",
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
