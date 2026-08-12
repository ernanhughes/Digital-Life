# Stage 4 — Could the Decoder Be Inventing the Signal?

Two nulls attack the decoding result.

1. Labels are permuted independently inside each receiver group.
2. The no-channel receiver outcome is duplicated across all codeword labels.

```json
{
  "groupwise_label_permutation": {
    "2": {
      "0": {
        "n": 100,
        "mean": 0.49875,
        "std": 0.07469963000057112,
        "q95": 0.6052083333333332,
        "q99": 0.6460416666666668,
        "max": 0.6666666666666666
      },
      "4": {
        "n": 100,
        "mean": 0.48687499999999995,
        "std": 0.07340047825684336,
        "q95": 0.6052083333333332,
        "q99": 0.6666666666666666,
        "max": 0.6666666666666666
      },
      "8": {
        "n": 100,
        "mean": 0.49458333333333343,
        "std": 0.07474609800295041,
        "q95": 0.6052083333333332,
        "q99": 0.6668750000000001,
        "max": 0.6875
      },
      "16": {
        "n": 100,
        "mean": 0.5122916666666666,
        "std": 0.07694779751017354,
        "q95": 0.6458333333333334,
        "q99": 0.6881250000000003,
        "max": 0.75
      },
      "24": {
        "n": 100,
        "mean": 0.5035416666666667,
        "std": 0.07342412703298253,
        "q95": 0.6041666666666666,
        "q99": 0.6472916666666675,
        "max": 0.7916666666666666
      }
    },
    "4": {
      "0": {
        "n": 100,
        "mean": 0.25354166666666667,
        "std": 0.04861850142235521,
        "q95": 0.3229166666666667,
        "q99": 0.34447916666666706,
        "max": 0.4166666666666667
      },
      "4": {
        "n": 100,
        "mean": 0.25322916666666667,
        "std": 0.043418760945970504,
        "q95": 0.3229166666666667,
        "q99": 0.3650000000000002,
        "max": 0.40625
      },
      "8": {
        "n": 100,
        "mean": 0.25031250000000005,
        "std": 0.04459635226581504,
        "q95": 0.3229166666666667,
        "q99": 0.3337500000000002,
        "max": 0.375
      },
      "16": {
        "n": 100,
        "mean": 0.2594791666666667,
        "std": 0.05122405762784818,
        "q95": 0.34375,
        "q99": 0.3545833333333336,
        "max": 0.3958333333333333
      },
      "24": {
        "n": 100,
        "mean": 0.251875,
        "std": 0.04803834189131289,
        "q95": 0.3333333333333333,
        "q99": 0.3542708333333334,
        "max": 0.3645833333333333
      }
    },
    "8": {
      "0": {
        "n": 100,
        "mean": 0.12760416666666669,
        "std": 0.024356964481437336,
        "q95": 0.17213541666666665,
        "q99": 0.1875,
        "max": 0.1875
      },
      "4": {
        "n": 100,
        "mean": 0.1221875,
        "std": 0.021148911926963155,
        "q95": 0.15625,
        "q99": 0.1719791666666667,
        "max": 0.18229166666666666
      },
      "8": {
        "n": 100,
        "mean": 0.12390624999999998,
        "std": 0.024231851295092994,
        "q95": 0.16666666666666666,
        "q99": 0.18239583333333337,
        "max": 0.19270833333333334
      },
      "16": {
        "n": 100,
        "mean": 0.12114583333333333,
        "std": 0.023715023587380212,
        "q95": 0.15625,
        "q99": 0.17723958333333342,
        "max": 0.19270833333333334
      },
      "24": {
        "n": 100,
        "mean": 0.12114583333333334,
        "std": 0.024044455716327715,
        "q95": 0.16145833333333334,
        "q99": 0.1668750000000001,
        "max": 0.1875
      }
    }
  },
  "no_channel": {
    "2": {
      "0": {
        "accuracy": 0.5,
        "chance_accuracy": 0.5,
        "decoder_mi_bits": 0.0
      },
      "4": {
        "accuracy": 0.5,
        "chance_accuracy": 0.5,
        "decoder_mi_bits": 0.0
      },
      "8": {
        "accuracy": 0.5,
        "chance_accuracy": 0.5,
        "decoder_mi_bits": 0.0
      },
      "16": {
        "accuracy": 0.5,
        "chance_accuracy": 0.5,
        "decoder_mi_bits": 0.0
      },
      "24": {
        "accuracy": 0.5,
        "chance_accuracy": 0.5,
        "decoder_mi_bits": 0.0
      }
    },
    "4": {
      "0": {
        "accuracy": 0.25,
        "chance_accuracy": 0.25,
        "decoder_mi_bits": 0.0
      },
      "4": {
        "accuracy": 0.25,
        "chance_accuracy": 0.25,
        "decoder_mi_bits": 0.0
      },
      "8": {
        "accuracy": 0.25,
        "chance_accuracy": 0.25,
        "decoder_mi_bits": 0.0
      },
      "16": {
        "accuracy": 0.25,
        "chance_accuracy": 0.25,
        "decoder_mi_bits": 0.0
      },
      "24": {
        "accuracy": 0.25,
        "chance_accuracy": 0.25,
        "decoder_mi_bits": 0.0
      }
    },
    "8": {
      "0": {
        "accuracy": 0.125,
        "chance_accuracy": 0.125,
        "decoder_mi_bits": 0.0
      },
      "4": {
        "accuracy": 0.125,
        "chance_accuracy": 0.125,
        "decoder_mi_bits": 0.0
      },
      "8": {
        "accuracy": 0.125,
        "chance_accuracy": 0.125,
        "decoder_mi_bits": 0.0
      },
      "16": {
        "accuracy": 0.125,
        "chance_accuracy": 0.125,
        "decoder_mi_bits": 0.0
      },
      "24": {
        "accuracy": 0.125,
        "chance_accuracy": 0.125,
        "decoder_mi_bits": 0.0
      }
    }
  },
  "observed_vs_null": {
    "2:0": {
      "accuracy": 0.4583333333333333,
      "chance": 0.5,
      "null_q95": 0.6052083333333332,
      "beats_null_q95": false
    },
    "2:4": {
      "accuracy": 0.5833333333333334,
      "chance": 0.5,
      "null_q95": 0.6052083333333332,
      "beats_null_q95": false
    },
    "2:8": {
      "accuracy": 0.4791666666666667,
      "chance": 0.5,
      "null_q95": 0.6052083333333332,
      "beats_null_q95": false
    },
    "2:16": {
      "accuracy": 0.3958333333333333,
      "chance": 0.5,
      "null_q95": 0.6458333333333334,
      "beats_null_q95": false
    },
    "2:24": {
      "accuracy": 0.4583333333333333,
      "chance": 0.5,
      "null_q95": 0.6041666666666666,
      "beats_null_q95": false
    },
    "4:0": {
      "accuracy": 0.25,
      "chance": 0.25,
      "null_q95": 0.3229166666666667,
      "beats_null_q95": false
    },
    "4:4": {
      "accuracy": 0.2604166666666667,
      "chance": 0.25,
      "null_q95": 0.3229166666666667,
      "beats_null_q95": false
    },
    "4:8": {
      "accuracy": 0.2604166666666667,
      "chance": 0.25,
      "null_q95": 0.3229166666666667,
      "beats_null_q95": false
    },
    "4:16": {
      "accuracy": 0.2604166666666667,
      "chance": 0.25,
      "null_q95": 0.34375,
      "beats_null_q95": false
    },
    "4:24": {
      "accuracy": 0.3020833333333333,
      "chance": 0.25,
      "null_q95": 0.3333333333333333,
      "beats_null_q95": false
    },
    "8:0": {
      "accuracy": 0.18229166666666666,
      "chance": 0.125,
      "null_q95": 0.17213541666666665,
      "beats_null_q95": true
    },
    "8:4": {
      "accuracy": 0.15104166666666666,
      "chance": 0.125,
      "null_q95": 0.15625,
      "beats_null_q95": false
    },
    "8:8": {
      "accuracy": 0.15104166666666666,
      "chance": 0.125,
      "null_q95": 0.16666666666666666,
      "beats_null_q95": false
    },
    "8:16": {
      "accuracy": 0.11979166666666667,
      "chance": 0.125,
      "null_q95": 0.15625,
      "beats_null_q95": false
    },
    "8:24": {
      "accuracy": 0.13541666666666666,
      "chance": 0.125,
      "null_q95": 0.16145833333333334,
      "beats_null_q95": false
    }
  }
}
```

A surviving claim requires the primary decoder to beat the 95th percentile of
the grouped label-permutation null.
