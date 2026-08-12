# Stage 6 — Where Does Recoverable Information Live?

The decoder is split into receiver-only measurement families.

```json
{
  "eight_codeword_feature_comparison": {
    "0": {
      "morphology": {
        "primary_accuracy": 0.13020833333333334,
        "primary_decoder_mi_bits": 0.13108394353780084,
        "secondary_accuracy": 0.109375
      },
      "recent_growth": {
        "primary_accuracy": 0.23958333333333334,
        "primary_decoder_mi_bits": 0.32160486702317753,
        "secondary_accuracy": 0.1875
      },
      "combined": {
        "primary_accuracy": 0.18229166666666666,
        "primary_decoder_mi_bits": 0.22448462072054043,
        "secondary_accuracy": 0.16145833333333334
      }
    },
    "4": {
      "morphology": {
        "primary_accuracy": 0.09895833333333333,
        "primary_decoder_mi_bits": 0.16097842643270618,
        "secondary_accuracy": 0.16145833333333334
      },
      "recent_growth": {
        "primary_accuracy": 0.19270833333333334,
        "primary_decoder_mi_bits": 0.19086932496539435,
        "secondary_accuracy": 0.15104166666666666
      },
      "combined": {
        "primary_accuracy": 0.15104166666666666,
        "primary_decoder_mi_bits": 0.1375711284532423,
        "secondary_accuracy": 0.15625
      }
    },
    "8": {
      "morphology": {
        "primary_accuracy": 0.125,
        "primary_decoder_mi_bits": 0.21371486544040524,
        "secondary_accuracy": 0.125
      },
      "recent_growth": {
        "primary_accuracy": 0.125,
        "primary_decoder_mi_bits": 0.24345595725853558,
        "secondary_accuracy": 0.08854166666666667
      },
      "combined": {
        "primary_accuracy": 0.15104166666666666,
        "primary_decoder_mi_bits": 0.211345496655308,
        "secondary_accuracy": 0.125
      }
    },
    "16": {
      "morphology": {
        "primary_accuracy": 0.078125,
        "primary_decoder_mi_bits": 0.16518489228786418,
        "secondary_accuracy": 0.08333333333333333
      },
      "recent_growth": {
        "primary_accuracy": 0.14583333333333334,
        "primary_decoder_mi_bits": 0.1579516178141817,
        "secondary_accuracy": 0.10416666666666667
      },
      "combined": {
        "primary_accuracy": 0.11979166666666667,
        "primary_decoder_mi_bits": 0.19299492663265155,
        "secondary_accuracy": 0.11458333333333333
      }
    },
    "24": {
      "morphology": {
        "primary_accuracy": 0.16145833333333334,
        "primary_decoder_mi_bits": 0.18577024309833967,
        "secondary_accuracy": 0.09375
      },
      "recent_growth": {
        "primary_accuracy": 0.11979166666666667,
        "primary_decoder_mi_bits": 0.1557530791867636,
        "secondary_accuracy": 0.09895833333333333
      },
      "combined": {
        "primary_accuracy": 0.13541666666666666,
        "primary_decoder_mi_bits": 0.20319936822552126,
        "secondary_accuracy": 0.125
      }
    }
  },
  "feature_definitions": {
    "morphology": "current occupied-cell geometry only; no birth-time history",
    "recent_growth": "recent receiver attachment and population window only",
    "combined": "morphology + recent growth"
  },
  "figure": "static\\images\\books\\digital-life\\ch17-06-feature-location.png"
}
```

Figure: `static\images\books\digital-life\ch17-06-feature-location.png`

Birth-time metadata is deliberately excluded from the morphology features.
