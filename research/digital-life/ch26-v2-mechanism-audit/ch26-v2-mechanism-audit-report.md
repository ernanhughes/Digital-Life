# Chapter 26 V2 Mechanism Audit

## Scientific boundary

This is an analysis-only audit of the original V2 sample.
The frozen V2 primary verdict remains unchanged.

## A. Zero-inflation accounting

```json
{
  "reference": "P(active) = P(x survives) * [1 - C(F-k,B)/C(F,B)]",
  "by_arm": {
    "f=0.10": {
      "budget_label": "f=0.10",
      "predicted_active_fraction": 0.3628578447446997,
      "observed_abs_E1_gt_epsilon_fraction": 0.4010416666666667,
      "observed_minus_predicted": 0.03818382192196701,
      "realized_x_survival_fraction": 0.9140625,
      "expected_x_survival_fraction": 0.92,
      "G_nonzero_fraction": 0.16927083333333334,
      "epsilon": 0.001
    },
    "f=0.25": {
      "budget_label": "f=0.25",
      "predicted_active_fraction": 0.6793740120773212,
      "observed_abs_E1_gt_epsilon_fraction": 0.6979166666666666,
      "observed_minus_predicted": 0.018542654589345453,
      "realized_x_survival_fraction": 0.9140625,
      "expected_x_survival_fraction": 0.92,
      "G_nonzero_fraction": 0.12760416666666666,
      "epsilon": 0.001
    },
    "f=0.50": {
      "budget_label": "f=0.50",
      "predicted_active_fraction": 0.8762859943610738,
      "observed_abs_E1_gt_epsilon_fraction": 0.8802083333333334,
      "observed_minus_predicted": 0.003922338972259576,
      "realized_x_survival_fraction": 0.9140625,
      "expected_x_survival_fraction": 0.92,
      "G_nonzero_fraction": 0.13541666666666666,
      "epsilon": 0.001
    },
    "f=0.75": {
      "budget_label": "f=0.75",
      "predicted_active_fraction": 0.9138284623186856,
      "observed_abs_E1_gt_epsilon_fraction": 0.9127604166666666,
      "observed_minus_predicted": -0.0010680456520190118,
      "realized_x_survival_fraction": 0.9140625,
      "expected_x_survival_fraction": 0.92,
      "G_nonzero_fraction": 0.14713541666666666,
      "epsilon": 0.001
    },
    "f=1.00": {
      "budget_label": "f=1.00",
      "predicted_active_fraction": 0.9176041666666667,
      "observed_abs_E1_gt_epsilon_fraction": 0.91015625,
      "observed_minus_predicted": -0.007447916666666665,
      "realized_x_survival_fraction": 0.9140625,
      "expected_x_survival_fraction": 0.92,
      "G_nonzero_fraction": 0.13671875,
      "epsilon": 0.001
    },
    "unbounded": {
      "budget_label": "unbounded",
      "predicted_active_fraction": 0.9176041666666667,
      "observed_abs_E1_gt_epsilon_fraction": 0.91015625,
      "observed_minus_predicted": -0.007447916666666665,
      "realized_x_survival_fraction": 0.9140625,
      "expected_x_survival_fraction": 0.92,
      "G_nonzero_fraction": 0.12890625,
      "epsilon": 0.001
    }
  },
  "notes": [
    "Observed activity uses |E1_ring1| > 1e-3.",
    "Finite-selection combinatorial prediction is parameter-free at the protocol level.",
    "x-loss produces a structural null when FORCE/PREVENT states collapse."
  ]
}
```

## B. Exact ring-1 channel accounting

```json
{
  "identity": "E1_ring1 = force_only + prevent_only + shared_probability_shift",
  "conditioned_summary_x_survives": {
    "f=0.10": {
      "n_surviving_probes": 702,
      "force_only_ring1": {
        "n": 702,
        "mean": 0.06942904481646242,
        "sd": 0.16338061661768163,
        "ci95_low": 0.0579021580811849,
        "ci95_high": 0.0820370120416827
      },
      "prevent_only_ring1": {
        "n": 702,
        "mean": 0.0,
        "sd": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0
      },
      "shared_probability_shift_ring1": {
        "n": 702,
        "mean": 0.05424619175407153,
        "sd": 0.18106565784485493,
        "ci95_low": 0.040951819104617024,
        "ci95_high": 0.06784437422691011
      },
      "E1_ring1": {
        "n": 702,
        "mean": 0.12367523657053398,
        "sd": 0.23325599825537963,
        "ci95_low": 0.10702766830738235,
        "ci95_high": 0.14111769081044873
      },
      "mean_n_promoted": 1.868945868945869,
      "mean_n_shared_empty": 3.131054131054131
    },
    "f=0.25": {
      "n_surviving_probes": 702,
      "force_only_ring1": {
        "n": 702,
        "mean": 0.04332141328079958,
        "sd": 0.06318400497432644,
        "ci95_low": 0.03886738762883817,
        "ci95_high": 0.04813791372589214
      },
      "prevent_only_ring1": {
        "n": 702,
        "mean": -0.0005814660226735789,
        "sd": 0.011837173782075171,
        "ci95_low": -0.0015776513349028884,
        "ci95_high": 0.0
      },
      "shared_probability_shift_ring1": {
        "n": 702,
        "mean": 0.07607185167079253,
        "sd": 0.15796562246024945,
        "ci95_low": 0.06425672156347846,
        "ci95_high": 0.08778479704109515
      },
      "E1_ring1": {
        "n": 702,
        "mean": 0.11881179892891852,
        "sd": 0.16176310124577906,
        "ci95_low": 0.10686452918754574,
        "ci95_high": 0.1306568998377305
      },
      "mean_n_promoted": 1.868945868945869,
      "mean_n_shared_empty": 3.131054131054131
    },
    "f=0.50": {
      "n_surviving_probes": 702,
      "force_only_ring1": {
        "n": 702,
        "mean": 0.03606854560573321,
        "sd": 0.03693982796271446,
        "ci95_low": 0.033343624344262614,
        "ci95_high": 0.03889111115604882
      },
      "prevent_only_ring1": {
        "n": 702,
        "mean": -0.0001906654814558429,
        "sd": 0.005051735813043813,
        "ci95_low": -0.0005719964443675287,
        "ci95_high": 0.0
      },
      "shared_probability_shift_ring1": {
        "n": 702,
        "mean": 0.07978878277099039,
        "sd": 0.12147376552802515,
        "ci95_low": 0.0707497038912786,
        "ci95_high": 0.08893076754014535
      },
      "E1_ring1": {
        "n": 702,
        "mean": 0.11566666289526774,
        "sd": 0.11587707958016157,
        "ci95_low": 0.10705090415909069,
        "ci95_high": 0.12445138376688948
      },
      "mean_n_promoted": 1.868945868945869,
      "mean_n_shared_empty": 3.131054131054131
    },
    "f=0.75": {
      "n_surviving_probes": 702,
      "force_only_ring1": {
        "n": 702,
        "mean": 0.03372256298492796,
        "sd": 0.027413584056798286,
        "ci95_low": 0.031709144151589666,
        "ci95_high": 0.03570763593452371
      },
      "prevent_only_ring1": {
        "n": 702,
        "mean": 0.0,
        "sd": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0
      },
      "shared_probability_shift_ring1": {
        "n": 702,
        "mean": 0.08395732124849825,
        "sd": 0.10992648649683462,
        "ci95_low": 0.07603947727230394,
        "ci95_high": 0.09204089415326365
      },
      "E1_ring1": {
        "n": 702,
        "mean": 0.11767988423342624,
        "sd": 0.09960863975128094,
        "ci95_low": 0.11032679519629174,
        "ci95_high": 0.1250687142153492
      },
      "mean_n_promoted": 1.868945868945869,
      "mean_n_shared_empty": 3.131054131054131
    },
    "f=1.00": {
      "n_surviving_probes": 702,
      "force_only_ring1": {
        "n": 702,
        "mean": 0.0330201672320762,
        "sd": 0.02299506102717119,
        "ci95_low": 0.03135084334693861,
        "ci95_high": 0.034750696504654316
      },
      "prevent_only_ring1": {
        "n": 702,
        "mean": -2.3464956117515687e-05,
        "sd": 0.0006217106435063261,
        "ci95_low": -7.039486835254706e-05,
        "ci95_high": 0.0
      },
      "shared_probability_shift_ring1": {
        "n": 702,
        "mean": 0.08527176684284184,
        "sd": 0.09846789415442106,
        "ci95_low": 0.07821014646192923,
        "ci95_high": 0.09263542800033456
      },
      "E1_ring1": {
        "n": 702,
        "mean": 0.11826846911880053,
        "sd": 0.08606914325491719,
        "ci95_low": 0.11213336043881117,
        "ci95_high": 0.12479115435371313
      },
      "mean_n_promoted": 1.868945868945869,
      "mean_n_shared_empty": 3.131054131054131
    },
    "unbounded": {
      "n_surviving_probes": 702,
      "force_only_ring1": {
        "n": 702,
        "mean": 0.03315603460465192,
        "sd": 0.02305947051951306,
        "ci95_low": 0.03146187791651286,
        "ci95_high": 0.03484722039067588
      },
      "prevent_only_ring1": {
        "n": 702,
        "mean": 0.0,
        "sd": 0.0,
        "ci95_low": 0.0,
        "ci95_high": 0.0
      },
      "shared_probability_shift_ring1": {
        "n": 702,
        "mean": 0.0852585269615089,
        "sd": 0.09848125150326847,
        "ci95_low": 0.07802822969898575,
        "ci95_high": 0.09253037204048661
      },
      "E1_ring1": {
        "n": 702,
        "mean": 0.11841456156616084,
        "sd": 0.08603298820625632,
        "ci95_low": 0.11195466196475669,
        "ci95_high": 0.12467122505802122
      },
      "mean_n_promoted": 1.868945868945869,
      "mean_n_shared_empty": 3.131054131054131
    }
  },
  "compressed_two_channel_regression": {
    "f=0.10": {
      "model": "E1 ~ a*(n_promoted*C/F) + b*(n_shared_empty*C/F)",
      "conditioned_on_x_survival": true,
      "coefficient_a_promotion_proxy": 0.5802123546543512,
      "coefficient_b_shared_shift_proxy": 0.37922330839275137,
      "n": 702,
      "coef": [
        0.5802123546543512,
        0.37922330839275137
      ],
      "r2_through_origin": 0.2230005020924002,
      "rmse": 0.23259340798869702,
      "mae": 0.18221957798194857
    },
    "f=0.25": {
      "model": "E1 ~ a*(n_promoted*C/F) + b*(n_shared_empty*C/F)",
      "conditioned_on_x_survival": true,
      "coefficient_a_promotion_proxy": 0.22446839192970208,
      "coefficient_b_shared_shift_proxy": 0.5649500120818705,
      "n": 702,
      "coef": [
        0.22446839192970208,
        0.5649500120818705
      ],
      "r2_through_origin": 0.36611509746114024,
      "rmse": 0.15972320553460476,
      "mae": 0.12075068357894489
    },
    "f=0.50": {
      "model": "E1 ~ a*(n_promoted*C/F) + b*(n_shared_empty*C/F)",
      "conditioned_on_x_survival": true,
      "coefficient_a_promotion_proxy": 0.12091009398586595,
      "coefficient_b_shared_shift_proxy": 0.6079457902282203,
      "n": 702,
      "coef": [
        0.12091009398586595,
        0.6079457902282203
      ],
      "r2_through_origin": 0.5411862169703832,
      "rmse": 0.11086168069312864,
      "mae": 0.08387648504634354
    },
    "f=0.75": {
      "model": "E1 ~ a*(n_promoted*C/F) + b*(n_shared_empty*C/F)",
      "conditioned_on_x_survival": true,
      "coefficient_a_promotion_proxy": 0.037889735783625124,
      "coefficient_b_shared_shift_proxy": 0.6693357767857216,
      "n": 702,
      "coef": [
        0.037889735783625124,
        0.6693357767857216
      ],
      "r2_through_origin": 0.6592645308210067,
      "rmse": 0.08997007774462669,
      "mae": 0.06685968545504307
    },
    "f=1.00": {
      "model": "E1 ~ a*(n_promoted*C/F) + b*(n_shared_empty*C/F)",
      "conditioned_on_x_survival": true,
      "coefficient_a_promotion_proxy": 0.015317447034503693,
      "coefficient_b_shared_shift_proxy": 0.686249584249397,
      "n": 702,
      "coef": [
        0.015317447034503693,
        0.686249584249397
      ],
      "r2_through_origin": 0.7491824984375492,
      "rmse": 0.07323712173128322,
      "mae": 0.055719329681933195
    },
    "unbounded": {
      "model": "E1 ~ a*(n_promoted*C/F) + b*(n_shared_empty*C/F)",
      "conditioned_on_x_survival": true,
      "coefficient_a_promotion_proxy": 0.01694800990038953,
      "coefficient_b_shared_shift_proxy": 0.6861386229081498,
      "n": 702,
      "coef": [
        0.01694800990038953,
        0.6861386229081498
      ],
      "r2_through_origin": 0.7493563687799562,
      "rmse": 0.07326026961286193,
      "mae": 0.05574792939636919
    }
  }
}
```

## C. Structural-null contribution

```json
{
  "realized_x_survival_fraction": 0.9140625,
  "realized_x_loss_fraction": 0.0859375,
  "expected_x_loss_fraction": 0.08,
  "primary_arm_E1_zero_fraction": 0.5989583333333334,
  "primary_arm_G_zero_fraction": 0.8307291666666666,
  "frozen_primary_result_unchanged": true,
  "future_design_note": "Do not post-hoc remove x-lost probes from V2. Future experiments should guarantee intervention survival by design if the intended estimand is conditional on an actually delivered perturbation."
}
```

## Assertions

```json
{
  "ring1_channel_accounting": {
    "status": "PASS",
    "tolerance": 1e-12,
    "rows_checked": 4608,
    "role": "ASSERTION_NOT_SCIENTIFIC_FINDING"
  },
  "unbounded_E1_far_zero": {
    "status": "PASS",
    "max_abs": 0.0,
    "tolerance": 1e-12,
    "role": "ASSERTION_NOT_SCIENTIFIC_FINDING"
  },
  "reference_f0p10_offset_zero": {
    "status": "PASS",
    "max_abs": 0.0,
    "tolerance": 1e-12,
    "role": "DEFINITION_ASSERTION_NOT_SCIENTIFIC_FINDING"
  }
}
```
