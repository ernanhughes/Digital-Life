# Stage 5 — Can the Pulse Travel?

Six independently evolving Digital Crystals are connected in a one-way nearest-
neighbour chain. A receiver's own growth can subsequently produce another pulse.

```json
{
  "length": 6,
  "replicates": 30,
  "requested_steps": 90,
  "real_safe_horizon_summary": {
    "n": 30,
    "mean": 74.56666666666666,
    "std": 0.8825468196582487,
    "median": 75.0,
    "q05": 73.0,
    "q25": 74.0,
    "q75": 75.0,
    "q95": 76.0,
    "min": 72.0,
    "max": 76.0
  },
  "shuffled_safe_horizon_summary": {
    "n": 30,
    "mean": 74.63333333333334,
    "std": 1.0482790129010926,
    "median": 75.0,
    "q05": 73.0,
    "q25": 74.0,
    "q75": 75.0,
    "q95": 76.0,
    "min": 72.0,
    "max": 76.0
  },
  "real": {
    "mean_source_to_node_pulse_corr": [
      1.0,
      0.5373421448225714,
      0.476502004766455,
      0.46214947215469776,
      0.4620092356556393,
      0.4578017794000673
    ],
    "mean_pulse_rate_by_node": [
      0.6365765949799835,
      0.6831460912967764,
      0.6858317235764967,
      0.6848233734816288,
      0.6892351471875624,
      0.6790754810325826
    ]
  },
  "shuffled_edges": {
    "mean_source_to_node_pulse_corr": [
      1.0,
      0.498432926495073,
      0.4613941972108385,
      0.47830574608798854,
      0.4710790008158445,
      0.46055232546783
    ],
    "mean_pulse_rate_by_node": [
      0.6369220821398182,
      0.6866187907446017,
      0.6738499050600708,
      0.6734587370355213,
      0.6801793061987726,
      0.662360659145086
    ]
  },
  "topology_contrast": {
    "mean_absolute_real_minus_shuffled_by_distance": 0.016398722208874707
  },
  "interpretation": "Exploratory propagation test. High source-to-node correlations are not treated as topology-specific propagation unless they separate from the shuffled-edge control. No coordination claim is made.",
  "figure": "static\\images\\books\\digital-life\\ch16-05-chain-propagation.png"
}
```

Figure: `static\images\books\digital-life\ch16-05-chain-propagation.png`

This stage asks only whether measurable causal influence propagates with
distance. It does not test cooperation or a shared task.
