# Chapter 27 V1 Construct-Validity / Mechanism Audit

## Scientific boundary

This audit analyzes the existing V1 sample only.

The intended 12-step primary intervention is invalid because PREVENT did not explicitly prevent x from attaching.

The immediate pre-growth E1 result remains interpretable.

## A. PREVENT-x confound

```json
{
  "by_arm": {
    "accessible": {
      "p_prevent_x": {
        "n": 763,
        "mean": 0.4280071094245735,
        "sd": 0.0472402636394096,
        "se": 0.001710212371260123,
        "ci95_low": 0.42453504983220375,
        "ci95_high": 0.4312930598604055,
        "achieved_mde80_one_sided": 0.004252400067296094
      },
      "realized_prevent_x_attachment_rate": {
        "n": 763,
        "mean": 0.42070773263433814,
        "sd": 0.4939965276429886,
        "se": 0.017883875064359,
        "ci95_low": 0.38663171690694625,
        "ci95_high": 0.45609436435124506,
        "achieved_mde80_one_sided": 0.044467805756287594
      }
    },
    "remote": {
      "p_prevent_x": {
        "n": 763,
        "mean": 0.3774086505982059,
        "sd": 0.04462227623571123,
        "se": 0.0016154348636707502,
        "ci95_low": 0.37419159016963566,
        "ci95_high": 0.3805372849354791,
        "achieved_mde80_one_sided": 0.00401673817733196
      },
      "realized_prevent_x_attachment_rate": {
        "n": 763,
        "mean": 0.36828309305373524,
        "sd": 0.48265512764974167,
        "se": 0.01747328881691733,
        "ci95_low": 0.3354849279161206,
        "ci95_high": 0.40235910878112713,
        "achieved_mde80_one_sided": 0.04344689337394683
      }
    },
    "erased": {
      "p_prevent_x": {
        "n": 763,
        "mean": 0.3781227384922913,
        "sd": 0.04467955272145028,
        "se": 0.0016175084116771907,
        "ci95_low": 0.37495650803003683,
        "ci95_high": 0.381280342933583,
        "achieved_mde80_one_sided": 0.004021894002322064
      },
      "realized_prevent_x_attachment_rate": {
        "n": 763,
        "mean": 0.36959370904325034,
        "sd": 0.4830113517761502,
        "se": 0.017486184996171862,
        "ci95_low": 0.33551769331585846,
        "ci95_high": 0.4036697247706422,
        "achieved_mde80_one_sided": 0.043478959399460046
      }
    }
  },
  "paired_group_contrasts": {
    "accessible_minus_remote": {
      "n": 192,
      "mean": 0.05059352905674137,
      "sd": 0.0026736765858808987,
      "se": 0.00019295598707304206,
      "ci95_low": 0.05020691156347983,
      "ci95_high": 0.05095150692641612,
      "achieved_mde80_one_sided": 0.00047978021104478757
    },
    "accessible_minus_erased": {
      "n": 192,
      "mean": 0.04987910612789568,
      "sd": 0.0026150445717737646,
      "se": 0.0001887245859320566,
      "ci95_low": 0.04950883316357739,
      "ci95_high": 0.05023582589461497,
      "achieved_mde80_one_sided": 0.000469258938482933
    },
    "remote_minus_erased": {
      "n": 192,
      "mean": -0.000714422928845689,
      "sd": 0.00010932266526030134,
      "se": 7.889683777070291e-06,
      "ci95_low": -0.000730085455270155,
      "ci95_high": -0.0006992297977179587,
      "achieved_mde80_one_sided": 1.9617500369172364e-05
    }
  },
  "identity_assertion": "p_prevent(x) = E1_global - (force_expected - prevent_expected)"
}
```

## B. Immediate E1 saturation/channel audit

```json
{
  "accessible": {
    "force_only": {
      "n": 763,
      "mean": 0.6733978814203792,
      "sd": 0.4620917974164989,
      "se": 0.016728846278923935,
      "ci95_low": 0.6403123188186077,
      "ci95_high": 0.7065503795798322,
      "achieved_mde80_one_sided": 0.041595855718121286
    },
    "prevent_only": {
      "n": 763,
      "mean": 0.0,
      "sd": 0.0,
      "se": 0.0,
      "ci95_low": 0.0,
      "ci95_high": 0.0,
      "achieved_mde80_one_sided": 0.0
    },
    "shared": {
      "n": 763,
      "mean": 0.45253760948037786,
      "sd": 0.5564716764847749,
      "se": 0.020145627311575626,
      "ci95_low": 0.4134151942131526,
      "ci95_high": 0.4929695928200604,
      "achieved_mde80_one_sided": 0.05009159585972627
    },
    "total": {
      "n": 763,
      "mean": 1.125935490900757,
      "sd": 0.430204035306817,
      "se": 0.015574431780561932,
      "ci95_low": 1.0951790870664704,
      "ci95_high": 1.1573304734311076,
      "achieved_mde80_one_sided": 0.0387254330893193
    }
  },
  "remote": {
    "force_only": {
      "n": 763,
      "mean": 0.6732967134102782,
      "sd": 0.46202641693693314,
      "se": 0.016726479346642488,
      "ci95_low": 0.6403618830438933,
      "ci95_high": 0.7057709944884349,
      "achieved_mde80_one_sided": 0.04158997040050691
    },
    "prevent_only": {
      "n": 763,
      "mean": 0.0,
      "sd": 0.0,
      "se": 0.0,
      "ci95_low": 0.0,
      "ci95_high": 0.0,
      "achieved_mde80_one_sided": 0.0
    },
    "shared": {
      "n": 763,
      "mean": 0.47085745234535015,
      "sd": 0.5601965558493837,
      "se": 0.02028047699868641,
      "ci95_low": 0.4312635292296388,
      "ci95_high": 0.5093027374304137,
      "achieved_mde80_one_sided": 0.050426896216676814
    },
    "total": {
      "n": 763,
      "mean": 1.1441541657556282,
      "sd": 0.42834658126021774,
      "se": 0.015507187429137714,
      "ci95_low": 1.113910671585815,
      "ci95_high": 1.1737008332417898,
      "achieved_mde80_one_sided": 0.03855823169999071
    }
  },
  "erased": {
    "force_only": {
      "n": 763,
      "mean": 0.6745606189834858,
      "sd": 0.46287744188819724,
      "se": 0.01675728851847549,
      "ci95_low": 0.6411201360194592,
      "ci95_high": 0.7074852615730186,
      "achieved_mde80_one_sided": 0.041666576631743245
    },
    "prevent_only": {
      "n": 763,
      "mean": 0.0,
      "sd": 0.0,
      "se": 0.0,
      "ci95_low": 0.0,
      "ci95_high": 0.0,
      "achieved_mde80_one_sided": 0.0
    },
    "shared": {
      "n": 763,
      "mean": 0.470678897116112,
      "sd": 0.5602396479402731,
      "se": 0.020282037037121108,
      "ci95_low": 0.43140910107484143,
      "ci95_high": 0.5092381933265477,
      "achieved_mde80_one_sided": 0.05043077521302614
    },
    "total": {
      "n": 763,
      "mean": 1.1452395160995976,
      "sd": 0.42861167462173244,
      "se": 0.015516784453190373,
      "ci95_low": 1.1152776694294801,
      "ci95_high": 1.1760220089350575,
      "achieved_mde80_one_sided": 0.038582094459033496
    }
  },
  "accessible_minus_erased": {
    "shared_saturation_delta_sum": {
      "n": 763,
      "mean": -0.018141287635734058,
      "sd": 0.02459154709649418,
      "se": 0.0008902737798813843,
      "ci95_low": -0.019887428436706787,
      "ci95_high": -0.016400691870852996,
      "achieved_mde80_one_sided": 0.0022136433726590832
    },
    "E1_total_difference": {
      "n": 763,
      "mean": -0.019304025198840686,
      "sd": 0.024471426338290903,
      "se": 0.0008859251164553612,
      "ci95_low": -0.02105622734376052,
      "ci95_high": -0.017593873375011632,
      "achieved_mde80_one_sided": 0.0022028305303733947
    }
  },
  "accessible_minus_remote": {
    "E1_total_difference": {
      "n": 763,
      "mean": -0.018218674854871244,
      "sd": 0.024962170903272525,
      "se": 0.0009036912625667914,
      "ci95_low": -0.019980307485869656,
      "ci95_high": -0.016470530495307417,
      "achieved_mde80_one_sided": 0.0022470056060478693
    }
  }
}
```

## C. Remote calibration channel

```json
{
  "remote_offset": {
    "n": 192,
    "mean": -0.0030613225596365368,
    "sd": 0.0003988207798711397,
    "se": 2.8782410577127374e-05,
    "ci95_low": -0.003118192259586531,
    "ci95_high": -0.0030052955492647936,
    "achieved_mde80_one_sided": 7.156674032531841e-05
  },
  "calibration_channel": {
    "n": 192,
    "mean": -0.0010844318512218281,
    "sd": 0.0003978125605277886,
    "se": 2.8709648613466633e-05,
    "ci95_low": -0.0011412550040866977,
    "ci95_high": -0.0010290079243847562,
    "achieved_mde80_one_sided": 7.138581953187358e-05
  },
  "direct_remote_minus_erased_at_offset0": {
    "n": 192,
    "mean": 0.0,
    "sd": 0.0,
    "se": 0.0,
    "ci95_low": 0.0,
    "ci95_high": 0.0,
    "achieved_mde80_one_sided": 0.0
  },
  "total_remote_minus_erased": {
    "n": 192,
    "mean": -0.0010844318512218281,
    "sd": 0.0003978125605277886,
    "se": 2.8709648613466633e-05,
    "ci95_low": -0.0011397925930911436,
    "ci95_high": -0.001028228084969333,
    "achieved_mde80_one_sided": 7.138581953187358e-05
  }
}
```

## D. Material-mass trajectory

```json
{
  "1": {
    "prevent_material_mass": {
      "n": 192,
      "mean": 0.02843571813998845,
      "sd": 0.18846470499421614,
      "se": 0.013601268520144262,
      "ci95_low": 0.0013671018336532802,
      "ci95_high": 0.05577775481305428,
      "achieved_mde80_one_sided": 0.03381921224658043
    },
    "prevent_local_material_mass": {
      "n": 192,
      "mean": 1.1642239215391426,
      "sd": 0.12071788399225329,
      "se": 0.008712062852366182,
      "ci95_low": 1.1464515977016498,
      "ci95_high": 1.180909399418881,
      "achieved_mde80_one_sided": 0.02166232526571689
    }
  },
  "2": {
    "prevent_material_mass": {
      "n": 192,
      "mean": 0.017294879650600146,
      "sd": 0.21027095526959647,
      "se": 0.01517499907845766,
      "ci95_low": -0.012179492711690248,
      "ci95_high": 0.04750002157559196,
      "achieved_mde80_one_sided": 0.0377322537170657
    },
    "prevent_local_material_mass": {
      "n": 192,
      "mean": 0.9536542793253462,
      "sd": 0.13992782813440138,
      "se": 0.01009842115506454,
      "ci95_low": 0.9339235011324081,
      "ci95_high": 0.9731414676640506,
      "achieved_mde80_one_sided": 0.025109470333055616
    }
  },
  "3": {
    "prevent_material_mass": {
      "n": 192,
      "mean": 0.03125,
      "sd": 0.20952972357420324,
      "se": 0.015121505288599265,
      "ci95_low": 0.0032552083333333335,
      "ci95_high": 0.060118272569444374,
      "achieved_mde80_one_sided": 0.03759924275338863
    },
    "prevent_local_material_mass": {
      "n": 192,
      "mean": 0.7864583333333334,
      "sd": 0.14487186169787833,
      "se": 0.010455226043659036,
      "ci95_low": 0.7660590277777777,
      "ci95_high": 0.806423611111111,
      "achieved_mde80_one_sided": 0.025996656718658032
    }
  },
  "4": {
    "prevent_material_mass": {
      "n": 192,
      "mean": 0.029193946709893934,
      "sd": 0.21363549195842937,
      "se": 0.015417813598832167,
      "ci95_low": -0.001353361768008321,
      "ci95_high": 0.05955275122725211,
      "achieved_mde80_one_sided": 0.0383360059177472
    },
    "prevent_local_material_mass": {
      "n": 192,
      "mean": 0.6438135267811046,
      "sd": 0.1439264586297404,
      "se": 0.01038699745417377,
      "ci95_low": 0.6233197628655499,
      "ci95_high": 0.66372727851037,
      "achieved_mde80_one_sided": 0.02582700804613388
    }
  },
  "5": {
    "prevent_material_mass": {
      "n": 192,
      "mean": 0.019291332228780197,
      "sd": 0.20806967483497493,
      "se": 0.015016135347021335,
      "ci95_low": -0.010162398227660999,
      "ci95_high": 0.049089550760735325,
      "achieved_mde80_one_sided": 0.03733724304260018
    },
    "prevent_local_material_mass": {
      "n": 192,
      "mean": 0.5196602619127667,
      "sd": 0.1406184885290459,
      "se": 0.01014826527566037,
      "ci95_low": 0.4991632214196877,
      "ci95_high": 0.5393003883180046,
      "achieved_mde80_one_sided": 0.02523340648586209
    }
  },
  "6": {
    "prevent_material_mass": {
      "n": 192,
      "mean": 0.008900215561809838,
      "sd": 0.19137430238232886,
      "se": 0.013811250624551802,
      "ci95_low": -0.019185335355435783,
      "ci95_high": 0.03606121822457436,
      "achieved_mde80_one_sided": 0.034341327470349785
    },
    "prevent_local_material_mass": {
      "n": 192,
      "mean": 0.42245333520107753,
      "sd": 0.13032217609099087,
      "se": 0.009405192930938925,
      "ci95_low": 0.4038856441152328,
      "ci95_high": 0.44102102628692225,
      "achieved_mde80_one_sided": 0.023385775781161307
    }
  },
  "7": {
    "prevent_material_mass": {
      "n": 192,
      "mean": 0.006972219351631778,
      "sd": 0.1770237954883377,
      "se": 0.012775591997270129,
      "ci95_low": -0.018045744204223443,
      "ci95_high": 0.032263603274217664,
      "achieved_mde80_one_sided": 0.03176618832952871
    },
    "prevent_local_material_mass": {
      "n": 192,
      "mean": 0.34136532786322676,
      "sd": 0.12236620890240776,
      "se": 0.008831020456189888,
      "ci95_low": 0.3237297142090993,
      "ci95_high": 0.3588642313339889,
      "achieved_mde80_one_sided": 0.021958110357092754
    }
  },
  "8": {
    "prevent_material_mass": {
      "n": 192,
      "mean": 0.013032057201508554,
      "sd": 0.1584520772328854,
      "se": 0.01143529368050772,
      "ci95_low": -0.009500004315118387,
      "ci95_high": 0.03568895851843029,
      "achieved_mde80_one_sided": 0.02843357025929583
    },
    "prevent_local_material_mass": {
      "n": 192,
      "mean": 0.28244243598409674,
      "sd": 0.11131373299247475,
      "se": 0.008033376713463429,
      "ci95_low": 0.26709627516736706,
      "ci95_high": 0.29815398158217715,
      "achieved_mde80_one_sided": 0.01997478924314883
    }
  },
  "9": {
    "prevent_material_mass": {
      "n": 192,
      "mean": 0.013454861111111107,
      "sd": 0.14394278074923914,
      "se": 0.010388175401684562,
      "ci95_low": -0.006618923611111113,
      "ci95_high": 0.03407389322916662,
      "achieved_mde80_one_sided": 0.02582993698300648
    },
    "prevent_local_material_mass": {
      "n": 192,
      "mean": 0.23090277777777776,
      "sd": 0.09610689513159987,
      "se": 0.0069359177219010405,
      "ci95_low": 0.21744791666666663,
      "ci95_high": 0.24468315972222218,
      "achieved_mde80_one_sided": 0.017245985050172507
    }
  },
  "10": {
    "prevent_material_mass": {
      "n": 192,
      "mean": 0.010053544562347574,
      "sd": 0.12390182884308094,
      "se": 0.008941844279454965,
      "ci95_low": -0.007639243836918436,
      "ci95_high": 0.02774391624417071,
      "achieved_mde80_one_sided": 0.022233671007588565
    },
    "prevent_local_material_mass": {
      "n": 192,
      "mean": 0.18850396054401705,
      "sd": 0.08221108291657343,
      "se": 0.00593307385653179,
      "ci95_low": 0.17700038551594624,
      "ci95_high": 0.20039421036294733,
      "achieved_mde80_one_sided": 0.014752438989900763
    }
  },
  "11": {
    "prevent_material_mass": {
      "n": 192,
      "mean": 0.00878444592560527,
      "sd": 0.10422143352716833,
      "se": 0.007521534087779915,
      "ci95_low": -0.005942419302615329,
      "ci95_high": 0.023425189134947382,
      "achieved_mde80_one_sided": 0.01870210542184198
    },
    "prevent_local_material_mass": {
      "n": 192,
      "mean": 0.15493351196239097,
      "sd": 0.06886407797010848,
      "se": 0.004969836744192189,
      "ci95_low": 0.14537396786687934,
      "ci95_high": 0.16483754413341647,
      "achieved_mde80_one_sided": 0.012357374125344243
    }
  },
  "12": {
    "prevent_material_mass": {
      "n": 192,
      "mean": 0.005907901709132394,
      "sd": 0.0908611769230593,
      "se": 0.006557340619426813,
      "ci95_low": -0.007214161794820432,
      "ci95_high": 0.01879786907451216,
      "achieved_mde80_one_sided": 0.016304662602100176
    },
    "prevent_local_material_mass": {
      "n": 192,
      "mean": 0.12460301786533777,
      "sd": 0.06124825131163956,
      "se": 0.0044202117977711185,
      "ci95_low": 0.11593298029219541,
      "ci95_high": 0.1331963294422576,
      "achieved_mde80_one_sided": 0.01099074551335119
    }
  },
  "group_level_G_vs_mean_mass_difference": {
    "model": "Delta_G = alpha + beta * mean_12lag_material_mass_difference",
    "alpha": -0.21909622145690105,
    "beta": 0.6706854903228633,
    "alpha_HC1_SE": 0.14994042134600225,
    "beta_HC1_SE": 0.9738293546299873,
    "corr_DeltaG_massdiff": 0.04430069929480247
  }
}
```

## E. Rao-Blackwellized implemented-protocol diagnostic

```json
{
  "role": "DIAGNOSTIC_OF_IMPLEMENTED_V1_PROTOCOL_NOT_PRIMARY_REPAIR",
  "accessible_minus_remote_RB": {
    "n": 192,
    "mean": -0.158349916998777,
    "sd": 1.674154960924157,
    "se": 0.12082172716933869,
    "ci95_low": -0.39791977248408866,
    "ci95_high": 0.0761121331328212,
    "achieved_mde80_one_sided": 0.30042018721169683
  },
  "realized_accessible_minus_remote": {
    "n": 192,
    "mean": -0.20833333333333334,
    "sd": 2.041312698596097,
    "se": 0.14731905450433225,
    "ci95_low": -0.5048068576388888,
    "ci95_high": 0.07855902777777778,
    "achieved_mde80_one_sided": 0.366305125501244
  },
  "note": "Only lag-1 direct p(x) is explicitly removed. Later states remain contaminated by natural x attachment/re-entry. This estimator cannot rescue V1 construct validity."
}
```

## F. Common-random-number pairing

```json
{
  "accessible_vs_remote": {
    "arm_a": "accessible",
    "arm_b": "remote",
    "n_groups": 192,
    "corr_G_local": 0.9327487152586896,
    "sd_arm_a": 5.527010453757382,
    "sd_arm_b": 5.598430127316066,
    "sd_difference": 2.041312698596097,
    "mean_difference": -0.20833333333333334
  },
  "accessible_vs_erased": {
    "arm_a": "accessible",
    "arm_b": "erased",
    "n_groups": 192,
    "corr_G_local": 0.9384315349110968,
    "sd_arm_a": 5.527010453757382,
    "sd_arm_b": 5.613548121129917,
    "sd_difference": 1.9565153456713764,
    "mean_difference": -0.20833333333333334
  },
  "remote_vs_erased": {
    "arm_a": "remote",
    "arm_b": "erased",
    "n_groups": 192,
    "corr_G_local": 0.9894456548485503,
    "sd_arm_a": 5.598430127316066,
    "sd_arm_b": 5.613548121129917,
    "sd_difference": 0.8146241866314958,
    "mean_difference": 0.0
  }
}
```

## G. Structural assertions

```json
{
  "erased_offset_zero": {
    "status": "PASS",
    "max_abs": 0.0,
    "role": "DEFINITION_ASSERTION_NOT_FINDING"
  },
  "remote_direct_ring1_material_exposure_zero": {
    "status": "PASS",
    "max_abs": 0.0,
    "role": "PLACEMENT_ASSERTION_NOT_FINDING"
  },
  "erased_direct_ring1_material_exposure_zero": {
    "status": "PASS",
    "max_abs": 0.0,
    "role": "DEFINITION_ASSERTION_NOT_FINDING"
  }
}
```
