# Chapter 16 — Digital Crystal Signalling: Full Experimental Report

## Run metadata

```json
{
  "model_version": "digital-crystal-v1-frozen",
  "signalling_version": "digital-crystal-signalling-v1",
  "profile": "quick",
  "profile_config": {
    "population": 36,
    "steps": 120,
    "grid_width": 6,
    "grid_height": 6,
    "crystal_radius": 14,
    "replicates": 4,
    "coupling_values": [
      0.0,
      0.03,
      0.06,
      0.1
    ],
    "delay_values": [
      0,
      1,
      3
    ],
    "noise_values": [
      0.0,
      0.03
    ]
  },
  "seed": 20260811,
  "started_at_unix": 1786483328.575716,
  "finished_at_unix": 1786483447.5105999,
  "final_verdict": "NOT_SUPPORTED_AS_TESTED",
  "selected_coupling_strength": 0.1
}
```

## Stage 1 — Independent Crystals

Uncoupled population baseline.

```json
{
  "mean_global_r_tail": {
    "mean": 0.1367673424390756,
    "std": 0.03979157868532482,
    "min": 0.09434314269750668,
    "max": 0.1772831670727232
  },
  "mean_local_r_tail": {
    "mean": 0.33417461752059785,
    "std": 0.024950178249415193,
    "min": 0.30963393452811877,
    "max": 0.37588234093264733
  },
  "final_global_r": {
    "mean": 0.11865277381118483,
    "std": 0.029208828221722778,
    "min": 0.07362088725971741,
    "max": 0.14469435211312212
  },
  "final_local_r": {
    "mean": 0.33559665761123575,
    "std": 0.03788708975753272,
    "min": 0.2783653860654268,
    "max": 0.38432097322530545
  },
  "mean_pairwise_growth_correlation": {
    "mean": 0.9320984341760075,
    "std": 0.00389135878916766
  }
}
```

Figure: `static\images\books\digital-life\ch16-01-uncoupled-baseline.png`

## Stage 2 — One-Bit Global Pulse Coupling

Each process emits only a pulse when its phase wraps.

```json
{
  "0.0": {
    "mean_global_r_tail": {
      "mean": 0.12935595484992182,
      "std": 0.06924354064317449,
      "min": 0.04171536303365121,
      "max": 0.2309483088186151
    },
    "mean_local_r_tail": {
      "mean": 0.3329955892532124,
      "std": 0.0321975597006061,
      "min": 0.30056641966815845,
      "max": 0.36555211569088647
    },
    "final_global_r": {
      "mean": 0.08474209121289215,
      "std": 0.04430195290680658,
      "min": 0.05201421811870278,
      "max": 0.16070882088204644
    },
    "final_local_r": {
      "mean": 0.3150301282776439,
      "std": 0.021300878547478735,
      "min": 0.2913094933662816,
      "max": 0.3468151000162804
    },
    "mean_pairwise_growth_correlation": {
      "mean": 0.9306422589197751,
      "std": 0.002635695067032497
    }
  },
  "0.03": {
    "mean_global_r_tail": {
      "mean": 0.11022481742820892,
      "std": 0.01832491345027032,
      "min": 0.0912780649456853,
      "max": 0.12994480804434347
    },
    "mean_local_r_tail": {
      "mean": 0.299833460388465,
      "std": 0.014953186532901577,
      "min": 0.28023368737528426,
      "max": 0.31851814466609885
    },
    "final_global_r": {
      "mean": 0.0933815196135856,
      "std": 0.030995681422401358,
      "min": 0.04819453819104474,
      "max": 0.1293462444322395
    },
    "final_local_r": {
      "mean": 0.2881525196366757,
      "std": 0.020596063758000042,
      "min": 0.26648068942791253,
      "max": 0.31470589414620087
    },
    "mean_pairwise_growth_correlation": {
      "mean": 0.9365277948323687,
      "std": 0.004790080113798826
    }
  },
  "0.06": {
    "mean_global_r_tail": {
      "mean": 0.172254428866155,
      "std": 0.002353526343192901,
      "min": 0.1695477354366523,
      "max": 0.17488419167464542
    },
    "mean_local_r_tail": {
      "mean": 0.32674719207405817,
      "std": 0.006324209825343346,
      "min": 0.3213296121610201,
      "max": 0.33701111883742585
    },
    "final_global_r": {
      "mean": 0.14786395410267664,
      "std": 0.03175265372897461,
      "min": 0.10937859139974265,
      "max": 0.19378016548986846
    },
    "final_local_r": {
      "mean": 0.3013184482693576,
      "std": 0.024441647098515006,
      "min": 0.2692372654000533,
      "max": 0.33632515361390736
    },
    "mean_pairwise_growth_correlation": {
      "mean": 0.9336066277771442,
      "std": 0.0031756456292334075
    }
  },
  "0.1": {
    "mean_global_r_tail": {
      "mean": 0.27344932874812544,
      "std": 0.0022796411766570907,
      "min": 0.270407200956394,
      "max": 0.27641641524999055
    },
    "mean_local_r_tail": {
      "mean": 0.40038115283384024,
      "std": 0.026414324443517368,
      "min": 0.38417680604189947,
      "max": 0.4461077287493276
    },
    "final_global_r": {
      "mean": 0.26553491423739584,
      "std": 0.05165262007149977,
      "min": 0.21307533611543183,
      "max": 0.34572205727929217
    },
    "final_local_r": {
      "mean": 0.3834482185127192,
      "std": 0.04247116626720843,
      "min": 0.3248689743984247,
      "max": 0.44403494481821587
    },
    "mean_pairwise_growth_correlation": {
      "mean": 0.929080822682844,
      "std": 0.006136040929514594
    }
  }
}
```

Figure: `static\images\books\digital-life\ch16-02-global-coupling-sweep.png`

## Stage 3 — Local Pulse Coupling

Local-neighbour coupling at K=0.100.

```json
{
  "mean_global_r_tail": {
    "mean": 0.1099097313054116,
    "std": 0.030143685633116316,
    "min": 0.06784739352287134,
    "max": 0.14961116941003544
  },
  "mean_local_r_tail": {
    "mean": 0.2585633049204601,
    "std": 0.006984513648476857,
    "min": 0.24898373286264872,
    "max": 0.26537735137308227
  },
  "final_global_r": {
    "mean": 0.08793060757786506,
    "std": 0.03690490713353342,
    "min": 0.041025815723255046,
    "max": 0.12447800976794043
  },
  "final_local_r": {
    "mean": 0.255121273890098,
    "std": 0.03618765880169851,
    "min": 0.21100627652617496,
    "max": 0.2921761747517919
  },
  "mean_pairwise_growth_correlation": {
    "mean": 0.9331922722192021,
    "std": 0.00710349119685239
  }
}
```

## Stage 4 — Break the Communication Topology

Real and topology-broken event delivery are compared.

```json
{
  "uncoupled": {
    "mean_global_r_tail": {
      "mean": 0.10415154810922946,
      "std": 0.04328097623907279,
      "min": 0.039430515836376794,
      "max": 0.15542315934178777
    },
    "mean_local_r_tail": {
      "mean": 0.34530158918745135,
      "std": 0.022587833038049718,
      "min": 0.3193081319407795,
      "max": 0.3806584769808359
    },
    "final_global_r": {
      "mean": 0.10544844917134254,
      "std": 0.0503069755500342,
      "min": 0.04288058911792106,
      "max": 0.1676309642482003
    },
    "final_local_r": {
      "mean": 0.3318063825922791,
      "std": 0.03196573082834555,
      "min": 0.278414143891353,
      "max": 0.36327015791746614
    },
    "mean_pairwise_growth_correlation": {
      "mean": 0.933707547655631,
      "std": 0.012158461071808336
    }
  },
  "global": {
    "mean_global_r_tail": {
      "mean": 0.27084559486008775,
      "std": 0.003526514906716871,
      "min": 0.2669270426287173,
      "max": 0.27649766156131156
    },
    "mean_local_r_tail": {
      "mean": 0.37757677740092593,
      "std": 0.010763376737679305,
      "min": 0.36149821355081624,
      "max": 0.38909862648256827
    },
    "final_global_r": {
      "mean": 0.24061625458892388,
      "std": 0.02509507828661846,
      "min": 0.21548447336257393,
      "max": 0.2732638561108562
    },
    "final_local_r": {
      "mean": 0.3785695318481695,
      "std": 0.03480822698741425,
      "min": 0.3196433108366468,
      "max": 0.40509964758225303
    },
    "mean_pairwise_growth_correlation": {
      "mean": 0.9274971526753123,
      "std": 0.005602601374025318
    }
  },
  "local": {
    "mean_global_r_tail": {
      "mean": 0.1099097313054116,
      "std": 0.030143685633116316,
      "min": 0.06784739352287134,
      "max": 0.14961116941003544
    },
    "mean_local_r_tail": {
      "mean": 0.2585633049204601,
      "std": 0.006984513648476857,
      "min": 0.24898373286264872,
      "max": 0.26537735137308227
    },
    "final_global_r": {
      "mean": 0.08793060757786506,
      "std": 0.03690490713353342,
      "min": 0.041025815723255046,
      "max": 0.12447800976794043
    },
    "final_local_r": {
      "mean": 0.255121273890098,
      "std": 0.03618765880169851,
      "min": 0.21100627652617496,
      "max": 0.2921761747517919
    },
    "mean_pairwise_growth_correlation": {
      "mean": 0.9331922722192021,
      "std": 0.00710349119685239
    }
  },
  "shuffled": {
    "mean_global_r_tail": {
      "mean": 0.08190437567271183,
      "std": 0.010348765494750849,
      "min": 0.06687356714118828,
      "max": 0.09593144992787338
    },
    "mean_local_r_tail": {
      "mean": 0.2771978138207253,
      "std": 0.03699923644520257,
      "min": 0.2148937914532249,
      "max": 0.3094758066631753
    },
    "final_global_r": {
      "mean": 0.08086866020278011,
      "std": 0.02451196629517453,
      "min": 0.05072339518524646,
      "max": 0.11509629225581601
    },
    "final_local_r": {
      "mean": 0.26245910684651,
      "std": 0.041325091220047835,
      "min": 0.22013628058244492,
      "max": 0.32835802001861825
    },
    "mean_pairwise_growth_correlation": {
      "mean": 0.9248525008732227,
      "std": 0.0054792882330217205
    }
  }
}
```

Figure: `static\images\books\digital-life\ch16-04-mode-comparison.png`

## Stage 5 — Delay and Noise

Robustness sweep.

```json
[
  {
    "pulse_delay": 0,
    "phase_noise": 0.0,
    "mean_global_r_tail": 0.10178137064640866,
    "mean_local_r_tail": 0.27528692545606276
  },
  {
    "pulse_delay": 1,
    "phase_noise": 0.0,
    "mean_global_r_tail": 0.11387869222449784,
    "mean_local_r_tail": 0.30175003509251047
  },
  {
    "pulse_delay": 3,
    "phase_noise": 0.0,
    "mean_global_r_tail": 0.12687704051745452,
    "mean_local_r_tail": 0.31007482852107293
  },
  {
    "pulse_delay": 0,
    "phase_noise": 0.03,
    "mean_global_r_tail": 0.06367806251449193,
    "mean_local_r_tail": 0.23641188785960948
  },
  {
    "pulse_delay": 1,
    "phase_noise": 0.03,
    "mean_global_r_tail": 0.12591461365412254,
    "mean_local_r_tail": 0.26883708499193126
  },
  {
    "pulse_delay": 3,
    "phase_noise": 0.03,
    "mean_global_r_tail": 0.2116525402461264,
    "mean_local_r_tail": 0.3362857300812996
  }
]
```

Figure: `static\images\books\digital-life\ch16-05-delay-noise-robustness.png`

## Stage 6 — Does Signalling Reach the Crystal?

Mean pairwise growth-activity correlation:

```json
{
  "uncoupled": {
    "mean": 0.933707547655631,
    "std": 0.012158461071808336
  },
  "global": {
    "mean": 0.9274971526753123,
    "std": 0.005602601374025318
  },
  "local": {
    "mean": 0.9331922722192021,
    "std": 0.00710349119685239
  },
  "shuffled": {
    "mean": 0.9248525008732227,
    "std": 0.0054792882330217205
  }
}
```

Figures:
- `static\images\books\digital-life\ch16-06-growth-correlation.png`
- `static\images\books\digital-life\ch16-06-crystal-gallery.png`

## Stage 7 — Experimental Verdict

**Verdict: `NOT_SUPPORTED_AS_TESTED`**

> This one-bit pulse mechanism did not establish robust inter-crystal synchronization above the uncoupled controls.

```json
{
  "verdict": "NOT_SUPPORTED_AS_TESTED",
  "bounded_claim": "This one-bit pulse mechanism did not establish robust inter-crystal synchronization above the uncoupled controls.",
  "selected_coupling_strength": 0.1,
  "checks": {
    "global_coupling_increases_coherence": true,
    "local_coupling_increases_local_coherence": false,
    "real_local_topology_beats_shuffled_control": false,
    "coupling_reaches_crystal_growth": false
  },
  "headline_metrics": {
    "uncoupled_global_r": 0.10415154810922946,
    "best_global_r": 0.27344932874812544,
    "uncoupled_local_r": 0.34530158918745135,
    "local_local_r": 0.2585633049204601,
    "shuffled_local_r": 0.2771978138207253,
    "uncoupled_growth_correlation": 0.933707547655631,
    "local_growth_correlation": 0.9331922722192021
  },
  "explicit_nonclaims": [
    "language",
    "semantics",
    "cooperation",
    "coordination",
    "planning",
    "learning",
    "intelligence",
    "agency",
    "life"
  ]
}
```
