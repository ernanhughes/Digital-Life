# Stage 1 — Start With the Simplest Distinction

The ladder does not begin with eight hard codewords.

It begins with one early pulse versus one late pulse and increases difficulty
only after simpler distinctions are measured.

```json
{
  "levels": [
    {
      "level": "L1",
      "title": "One pulse: early vs late",
      "n_codewords": 2,
      "encoded_bits": 1.0,
      "length": 16,
      "weight_each": [
        1,
        1
      ],
      "equal_weight_within_level": true,
      "pairwise_hamming_min": 2,
      "pairwise_hamming_mean": 2.0,
      "pairwise_hamming_max": 2,
      "codewords": [
        "0010000000000000",
        "0000000000000100"
      ],
      "interpretation": "Same pulse count and energy; only coarse pulse timing differs."
    },
    {
      "level": "L2",
      "title": "Two-pulse burst: early vs late",
      "n_codewords": 2,
      "encoded_bits": 1.0,
      "length": 16,
      "weight_each": [
        2,
        2
      ],
      "equal_weight_within_level": true,
      "pairwise_hamming_min": 4,
      "pairwise_hamming_mean": 4.0,
      "pairwise_hamming_max": 4,
      "codewords": [
        "0011000000000000",
        "0000000000001100"
      ],
      "interpretation": "Same two adjacent pulses; only burst location differs."
    },
    {
      "level": "L3",
      "title": "Four pulses: clustered vs dispersed",
      "n_codewords": 2,
      "encoded_bits": 1.0,
      "length": 16,
      "weight_each": [
        4,
        4
      ],
      "equal_weight_within_level": true,
      "pairwise_hamming_min": 4,
      "pairwise_hamming_mean": 4.0,
      "pairwise_hamming_max": 4,
      "codewords": [
        "0011110000000000",
        "0010010010010000"
      ],
      "interpretation": "Same four pulses; temporal concentration differs strongly."
    },
    {
      "level": "L4",
      "title": "Two hard constant-weight temporal words",
      "n_codewords": 2,
      "encoded_bits": 1.0,
      "length": 16,
      "weight_each": [
        6,
        6
      ],
      "equal_weight_within_level": true,
      "pairwise_hamming_min": 8,
      "pairwise_hamming_mean": 8.0,
      "pairwise_hamming_max": 8,
      "codewords": [
        "1000000010001111",
        "1111100000000001"
      ],
      "interpretation": "Same length, weight, first bit and last bit; finer chronology differs."
    },
    {
      "level": "L5",
      "title": "Four hard constant-weight temporal words",
      "n_codewords": 4,
      "encoded_bits": 2.0,
      "length": 16,
      "weight_each": [
        6,
        6,
        6,
        6
      ],
      "equal_weight_within_level": true,
      "pairwise_hamming_min": 6,
      "pairwise_hamming_mean": 7.333333333333333,
      "pairwise_hamming_max": 8,
      "codewords": [
        "1000000010001111",
        "1111100000000001",
        "1000011101000001",
        "1100010000110001"
      ],
      "interpretation": "Two encoded bits in a constant-weight temporal codebook."
    },
    {
      "level": "L6",
      "title": "Eight hard constant-weight temporal words",
      "n_codewords": 8,
      "encoded_bits": 3.0,
      "length": 16,
      "weight_each": [
        6,
        6,
        6,
        6,
        6,
        6,
        6,
        6
      ],
      "equal_weight_within_level": true,
      "pairwise_hamming_min": 6,
      "pairwise_hamming_mean": 6.428571428571429,
      "pairwise_hamming_max": 8,
      "codewords": [
        "1000000010001111",
        "1111100000000001",
        "1000011101000001",
        "1100010000110001",
        "1010001010100001",
        "1001000100011001",
        "1000100001100101",
        "1010000001010011"
      ],
      "interpretation": "Three encoded bits in the hard constant-weight codebook from v1."
    }
  ],
  "figure": "static\\images\\books\\digital-life\\ch17-v2-01-information-ladder.png"
}
```

Figure: `static\images\books\digital-life\ch17-v2-01-information-ladder.png`
