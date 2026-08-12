# Stage 6 — The Crystal Board

A 6×6 board of separate Digital Crystal processes is connected by
local one-bit neighbour events.

Real and shuffled topologies are advanced in lockstep from identical crystal
seeds and environmental inputs. Each replicate stops at the longest **common**
horizon for which every crystal in both topologies remains below the saturation
guard of `0.85`.

This prevents topology comparisons from being contaminated by one condition
running longer or by endpoint morphologies collapsing onto the same filled disk.

```json
{
  "board_shape": [
    6,
    6
  ],
  "replicates": 15,
  "requested_steps": 90,
  "common_safe_horizon_summary": {
    "n": 15,
    "mean": 73.13333333333334,
    "std": 0.7180219742846006,
    "median": 73.0,
    "q05": 72.0,
    "q25": 73.0,
    "q75": 74.0,
    "q95": 74.0,
    "min": 72.0,
    "max": 74.0
  },
  "all_replicates_used_equal_horizon_across_topologies": true,
  "horizon_diagnostics": [
    {
      "replicate": 0,
      "common_safe_horizon": 74,
      "requested_steps": 90,
      "first_unsafe_step": 75,
      "max_capacity_fraction_at_safe_horizon": {
        "real": 0.8408687480421844,
        "shuffled": 0.8360655737704918
      }
    },
    {
      "replicate": 1,
      "common_safe_horizon": 72,
      "requested_steps": 90,
      "first_unsafe_step": 73,
      "max_capacity_fraction_at_safe_horizon": {
        "real": 0.8331419024746789,
        "shuffled": 0.8273989767150465
      }
    },
    {
      "replicate": 2,
      "common_safe_horizon": 73,
      "requested_steps": 90,
      "first_unsafe_step": 74,
      "max_capacity_fraction_at_safe_horizon": {
        "real": 0.8471337579617835,
        "shuffled": 0.8471337579617835
      }
    },
    {
      "replicate": 3,
      "common_safe_horizon": 73,
      "requested_steps": 90,
      "first_unsafe_step": 74,
      "max_capacity_fraction_at_safe_horizon": {
        "real": 0.8302182311788661,
        "shuffled": 0.8302182311788661
      }
    },
    {
      "replicate": 4,
      "common_safe_horizon": 73,
      "requested_steps": 90,
      "first_unsafe_step": 74,
      "max_capacity_fraction_at_safe_horizon": {
        "real": 0.8414952490341443,
        "shuffled": 0.8414952490341443
      }
    },
    {
      "replicate": 5,
      "common_safe_horizon": 74,
      "requested_steps": 90,
      "first_unsafe_step": 75,
      "max_capacity_fraction_at_safe_horizon": {
        "real": 0.8447321708259371,
        "shuffled": 0.8447321708259371
      }
    },
    {
      "replicate": 6,
      "common_safe_horizon": 73,
      "requested_steps": 90,
      "first_unsafe_step": 74,
      "max_capacity_fraction_at_safe_horizon": {
        "real": 0.8352302391145453,
        "shuffled": 0.8352302391145453
      }
    },
    {
      "replicate": 7,
      "common_safe_horizon": 72,
      "requested_steps": 90,
      "first_unsafe_step": 73,
      "max_capacity_fraction_at_safe_horizon": {
        "real": 0.8208207162994675,
        "shuffled": 0.8295917301869061
      }
    },
    {
      "replicate": 8,
      "common_safe_horizon": 73,
      "requested_steps": 90,
      "first_unsafe_step": 74,
      "max_capacity_fraction_at_safe_horizon": {
        "real": 0.8419129163621176,
        "shuffled": 0.8419129163621176
      }
    },
    {
      "replicate": 9,
      "common_safe_horizon": 74,
      "requested_steps": 90,
      "first_unsafe_step": 75,
      "max_capacity_fraction_at_safe_horizon": {
        "real": 0.8437924193379973,
        "shuffled": 0.8437924193379973
      }
    },
    {
      "replicate": 10,
      "common_safe_horizon": 73,
      "requested_steps": 90,
      "first_unsafe_step": 74,
      "max_capacity_fraction_at_safe_horizon": {
        "real": 0.8311579826668059,
        "shuffled": 0.8311579826668059
      }
    },
    {
      "replicate": 11,
      "common_safe_horizon": 73,
      "requested_steps": 90,
      "first_unsafe_step": 74,
      "max_capacity_fraction_at_safe_horizon": {
        "real": 0.8327242351467057,
        "shuffled": 0.8298005638508927
      }
    },
    {
      "replicate": 12,
      "common_safe_horizon": 74,
      "requested_steps": 90,
      "first_unsafe_step": 75,
      "max_capacity_fraction_at_safe_horizon": {
        "real": 0.8350214054505586,
        "shuffled": 0.8395113292262713
      }
    },
    {
      "replicate": 13,
      "common_safe_horizon": 74,
      "requested_steps": 90,
      "first_unsafe_step": 75,
      "max_capacity_fraction_at_safe_horizon": {
        "real": 0.8490132609376632,
        "shuffled": 0.8490132609376632
      }
    },
    {
      "replicate": 14,
      "common_safe_horizon": 72,
      "requested_steps": 90,
      "first_unsafe_step": 73,
      "max_capacity_fraction_at_safe_horizon": {
        "real": 0.830531481674846,
        "shuffled": 0.8351258222825519
      }
    }
  ],
  "real_topology_neighbor_pulse_corr": {
    "n": 15,
    "mean": 0.4970474796115515,
    "std": 0.014461334583800575,
    "median": 0.4976521627408683,
    "q05": 0.47877292036384017,
    "q25": 0.4848890736107516,
    "q75": 0.5028931739381911,
    "q95": 0.5214185900870915,
    "min": 0.4779201142624082,
    "max": 0.5268244470385874
  },
  "shuffled_topology_neighbor_pulse_corr": {
    "n": 15,
    "mean": 0.4922207777328165,
    "std": 0.015220084283624619,
    "median": 0.4893128637613229,
    "q05": 0.4717806441925401,
    "q25": 0.47807391941847255,
    "q75": 0.5047710791171247,
    "q95": 0.5134406798976298,
    "min": 0.465202671977659,
    "max": 0.5186012174441624
  },
  "real_minus_shuffled_mean": 0.004826701878735018,
  "pairwise_superiority_probability": 0.5777777777777777,
  "mean_pulse_rate_by_crystal": [
    0.6891651925898501,
    0.7173419995337805,
    0.6891768480809577,
    0.6935702826113785,
    0.6908302137754192,
    0.7045802651967036,
    0.6937464862122397,
    0.6945479726301644,
    0.7091855554184323,
    0.712887202270764,
    0.7120853730442771,
    0.7037554677965636,
    0.6974347635306539,
    0.70297832078654,
    0.7027534383698767,
    0.7038809357302507,
    0.7074444307321018,
    0.6863497058702539,
    0.7036306854800005,
    0.7045939775391831,
    0.7054811660976044,
    0.6891411959905109,
    0.6962729853140812,
    0.6927571407023462,
    0.7036413125454222,
    0.6965105516475381,
    0.7026653365694461,
    0.6963473747720322,
    0.7009780328273479,
    0.7028662223867703,
    0.7082589438753822,
    0.7028672508124563,
    0.6819477011257834,
    0.6947848533464972,
    0.7000767891178851,
    0.6909817351598172
  ],
  "mean_growth_activity_by_crystal": [
    100.29000575918384,
    101.77613366791448,
    100.86608971985683,
    101.70168044757085,
    100.37409498539634,
    101.1075781260713,
    101.54875251964293,
    100.40759663773362,
    100.72568047499554,
    103.37239774020597,
    102.61487034980182,
    99.53632536646234,
    100.84101121669615,
    101.43804866510344,
    100.56634922593828,
    101.84699288329425,
    100.82506101992404,
    100.90279868910007,
    100.01935839949539,
    103.0545806080053,
    103.28019012162848,
    103.24840182648401,
    102.45751984861572,
    101.3766691348883,
    99.99004895306265,
    101.76030928188464,
    101.72737189244036,
    102.39321718979254,
    99.99106229517187,
    102.57578983092681,
    101.10431287451837,
    102.10195503722899,
    102.3909693940516,
    101.34406495536632,
    102.14858831434172,
    101.65995995995995
  ],
  "max_capacity_fraction_observed_at_safe_horizon": 0.8490132609376632,
  "saturation_guard": 0.85,
  "figure": "static\\images\\books\\digital-life\\ch16-06-crystal-board.png",
  "explicit_nonclaim": "The board has no shared target and does not test coordination."
}
```

Figure: `static\images\books\digital-life\ch16-06-crystal-board.png`

The board exists only to observe local propagation and topology effects.
No coordination claim is made.
