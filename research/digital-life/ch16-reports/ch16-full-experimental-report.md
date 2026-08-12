# Chapter 16 — Before There Are Messages: Full Experimental Report

## Run metadata

```json
{
  "model_version": "digital-crystal-v1-frozen",
  "signalling_version": "digital-crystal-signalling-v3.4",
  "schema_version": 3,
  "profile": "full",
  "profile_config": {
    "pair_steps": 90,
    "crystal_radius": 56,
    "pair_replicates": 60,
    "intervention_replicates": 120,
    "impulse_horizon": 12,
    "message_gain": 0.65,
    "pulse_window": 12,
    "pulse_sigma": 0.75,
    "min_pulse_attachments": 3,
    "chain_length": 6,
    "chain_steps": 90,
    "chain_replicates": 30,
    "board_width": 6,
    "board_height": 6,
    "board_steps": 90,
    "board_replicates": 15,
    "max_capacity_fraction": 0.85
  },
  "seed": 20260812,
  "started_at_unix": 1786497121.2757924,
  "scientific_boundary": "Primitive causal transmission only. No semantics, coordination, agency, individuality, or life claim.",
  "message_definition": "One bit emitted by sender growth when attachment activity exceeds a threshold derived from the sender's own recent history.",
  "receiver_coupling": "Received bit directly perturbs the Digital Crystal environmental forcing used by the frozen attachment rule.",
  "saturation_policy": "Stages 1, 2, 3, 5, and 6 guard against hard-radius saturation. Stages comparing controls use matched/common horizons so endpoint morphology remains informative.",
  "sender_specificity_controls": [
    "shuffled chronology",
    "count-matched unrelated sender replay",
    "exact inter-pulse-interval multiset permutation",
    "rate-matched random timing"
  ],
  "finished_at_unix": 1786497909.6615794,
  "final_verdict": "CAUSAL_TRANSMISSION_SUPPORTED",
  "stage0_reproducibility_passed": true,
  "stage1_message_count": 49
}
```

# Stage 0 — Freeze the Substrate

Digital Crystal v1 is unchanged from Chapter 15. RNG-consuming frontier
traversal remains canonicalized with `sorted(frontier)`.

```json
{
  "canonical_rng_traversal": "sorted(frontier)",
  "repeat_from_identical_state_exact": true,
  "morphology_hash_a": "5fd54c923adbc247272c7ada",
  "morphology_hash_b": "5fd54c923adbc247272c7ada"
}
```

This stage must pass before any message experiment is interpreted.


# Stage 1 — Before There Are Messages, There Are Pulses

A sender Digital Crystal emits one bit only when its own current attachment
activity exceeds a threshold derived from its recent attachment history.

The sender and receiver are advanced together and the stage stops at the
longest **common** horizon for which both remain below the hard-radius
saturation guard of `0.85`.

```json
{
  "pulse_rule": {
    "window": 12,
    "sigma": 0.75,
    "min_attachments": 3
  },
  "requested_steps": 90,
  "common_safe_horizon": 76,
  "first_unsafe_step": 77,
  "sender_final_population": 7723,
  "sender_capacity_fraction": 0.8064111934843897,
  "message_count": 49,
  "message_rate": 0.6447368421052632,
  "message_structure": {
    "length": 76,
    "pulse_count": 49,
    "pulse_rate": 0.6447368421052632,
    "first_pulse": 12,
    "last_pulse": 73,
    "ipi_mean": 1.2708333333333333,
    "ipi_std": 1.0555327117411168,
    "ipi_median": 1.0,
    "lag1_autocorrelation": 0.5879120879120885
  },
  "receiver_final_population": 8026,
  "receiver_capacity_fraction": 0.8380494935783648,
  "saturation_guard": 0.85,
  "figure": "static\\images\\books\\digital-life\\ch16-01-sender-pulses-receiver.png"
}
```

Figure: `static\images\books\digital-life\ch16-01-sender-pulses-receiver.png`

The pulse has no semantics. It means only: an endogenous sender event occurred.


# Stage 2 — Does One Received Bit Actually Matter?

Every replicate forks an exact receiver checkpoint.

```text
same receiver state
same RNG state
same external environment
same future horizon

ONLY DIFFERENCE:
one branch receives one bit
```

```json
{
  "definition": "same receiver checkpoint + same RNG state + same external forcing; only one received bit differs at the intervention step",
  "replicates": 120,
  "message_gain": 0.65,
  "horizon": 12,
  "environment_length_policy": "checkpoint_step + horizon",
  "saturation_guard": 0.85,
  "max_capacity_fraction_observed": 0.13480213010337266,
  "capacity_diagnostics": [
    {
      "replicate": 0,
      "checkpoint_step": 12,
      "environment_steps": 24,
      "pulse_capacity_fraction": 0.07131669625143573,
      "no_pulse_capacity_fraction": 0.07319619922731545
    },
    {
      "replicate": 1,
      "checkpoint_step": 13,
      "environment_steps": 25,
      "pulse_capacity_fraction": 0.0777905398350214,
      "no_pulse_capacity_fraction": 0.07726845567505482
    },
    {
      "replicate": 2,
      "checkpoint_step": 14,
      "environment_steps": 26,
      "pulse_capacity_fraction": 0.08102746162681425,
      "no_pulse_capacity_fraction": 0.08102746162681425
    },
    {
      "replicate": 3,
      "checkpoint_step": 15,
      "environment_steps": 27,
      "pulse_capacity_fraction": 0.08697922105043333,
      "no_pulse_capacity_fraction": 0.08896314085830635
    },
    {
      "replicate": 4,
      "checkpoint_step": 16,
      "environment_steps": 28,
      "pulse_capacity_fraction": 0.09742090424976506,
      "no_pulse_capacity_fraction": 0.09324423097003237
    },
    {
      "replicate": 5,
      "checkpoint_step": 17,
      "environment_steps": 29,
      "pulse_capacity_fraction": 0.1121436775608228,
      "no_pulse_capacity_fraction": 0.10922000626500993
    },
    {
      "replicate": 6,
      "checkpoint_step": 18,
      "environment_steps": 30,
      "pulse_capacity_fraction": 0.09595906860185861,
      "no_pulse_capacity_fraction": 0.09668998642581184
    },
    {
      "replicate": 7,
      "checkpoint_step": 19,
      "environment_steps": 31,
      "pulse_capacity_fraction": 0.13365354495144618,
      "no_pulse_capacity_fraction": 0.13480213010337266
    },
    {
      "replicate": 8,
      "checkpoint_step": 12,
      "environment_steps": 24,
      "pulse_capacity_fraction": 0.06118826354808395,
      "no_pulse_capacity_fraction": 0.06275451602798371
    },
    {
      "replicate": 9,
      "checkpoint_step": 13,
      "environment_steps": 25,
      "pulse_capacity_fraction": 0.0693327764435627,
      "no_pulse_capacity_fraction": 0.06546935365980996
    },
    {
      "replicate": 10,
      "checkpoint_step": 14,
      "environment_steps": 26,
      "pulse_capacity_fraction": 0.08165396261877414,
      "no_pulse_capacity_fraction": 0.08583063589850684
    },
    {
      "replicate": 11,
      "checkpoint_step": 15,
      "environment_steps": 27,
      "pulse_capacity_fraction": 0.10107549336953117,
      "no_pulse_capacity_fraction": 0.10044899237757127
    },
    {
      "replicate": 12,
      "checkpoint_step": 16,
      "environment_steps": 28,
      "pulse_capacity_fraction": 0.09094706066617939,
      "no_pulse_capacity_fraction": 0.09167797849013261
    },
    {
      "replicate": 13,
      "checkpoint_step": 17,
      "environment_steps": 29,
      "pulse_capacity_fraction": 0.12133235877623473,
      "no_pulse_capacity_fraction": 0.12279419442414118
    },
    {
      "replicate": 14,
      "checkpoint_step": 18,
      "environment_steps": 30,
      "pulse_capacity_fraction": 0.13323587762347291,
      "no_pulse_capacity_fraction": 0.1337579617834395
    },
    {
      "replicate": 15,
      "checkpoint_step": 19,
      "environment_steps": 31,
      "pulse_capacity_fraction": 0.12550903205596742,
      "no_pulse_capacity_fraction": 0.13334029445546622
    },
    {
      "replicate": 16,
      "checkpoint_step": 12,
      "environment_steps": 24,
      "pulse_capacity_fraction": 0.06661793881173646,
      "no_pulse_capacity_fraction": 0.06348543385193693
    },
    {
      "replicate": 17,
      "checkpoint_step": 13,
      "environment_steps": 25,
      "pulse_capacity_fraction": 0.08603946956249348,
      "no_pulse_capacity_fraction": 0.08718805471441997
    },
    {
      "replicate": 18,
      "checkpoint_step": 14,
      "environment_steps": 26,
      "pulse_capacity_fraction": 0.09512373394591209,
      "no_pulse_capacity_fraction": 0.09188681215411924
    },
    {
      "replicate": 19,
      "checkpoint_step": 15,
      "environment_steps": 27,
      "pulse_capacity_fraction": 0.07737287250704813,
      "no_pulse_capacity_fraction": 0.07904354181894122
    },
    {
      "replicate": 20,
      "checkpoint_step": 16,
      "environment_steps": 28,
      "pulse_capacity_fraction": 0.08938080818627962,
      "no_pulse_capacity_fraction": 0.09032055967421948
    },
    {
      "replicate": 21,
      "checkpoint_step": 17,
      "environment_steps": 29,
      "pulse_capacity_fraction": 0.08645713689046675,
      "no_pulse_capacity_fraction": 0.08645713689046675
    },
    {
      "replicate": 22,
      "checkpoint_step": 18,
      "environment_steps": 30,
      "pulse_capacity_fraction": 0.11705126866450871,
      "no_pulse_capacity_fraction": 0.11600710034457555
    },
    {
      "replicate": 23,
      "checkpoint_step": 19,
      "environment_steps": 31,
      "pulse_capacity_fraction": 0.10410358149733737,
      "no_pulse_capacity_fraction": 0.1060875013052104
    },
    {
      "replicate": 24,
      "checkpoint_step": 12,
      "environment_steps": 24,
      "pulse_capacity_fraction": 0.06473843583585674,
      "no_pulse_capacity_fraction": 0.06306776652396366
    },
    {
      "replicate": 25,
      "checkpoint_step": 13,
      "environment_steps": 25,
      "pulse_capacity_fraction": 0.07789495666701472,
      "no_pulse_capacity_fraction": 0.07225644773937559
    },
    {
      "replicate": 26,
      "checkpoint_step": 14,
      "environment_steps": 26,
      "pulse_capacity_fraction": 0.08384671609063381,
      "no_pulse_capacity_fraction": 0.08551738540252689
    },
    {
      "replicate": 27,
      "checkpoint_step": 15,
      "environment_steps": 27,
      "pulse_capacity_fraction": 0.07183878041140232,
      "no_pulse_capacity_fraction": 0.07152552991542237
    },
    {
      "replicate": 28,
      "checkpoint_step": 16,
      "environment_steps": 28,
      "pulse_capacity_fraction": 0.09261772997807247,
      "no_pulse_capacity_fraction": 0.09700323692179179
    },
    {
      "replicate": 29,
      "checkpoint_step": 17,
      "environment_steps": 29,
      "pulse_capacity_fraction": 0.11861752114440847,
      "no_pulse_capacity_fraction": 0.11412759736869584
    },
    {
      "replicate": 30,
      "checkpoint_step": 18,
      "environment_steps": 30,
      "pulse_capacity_fraction": 0.10723608645713689,
      "no_pulse_capacity_fraction": 0.11089067557690299
    },
    {
      "replicate": 31,
      "checkpoint_step": 19,
      "environment_steps": 31,
      "pulse_capacity_fraction": 0.11976610629633497,
      "no_pulse_capacity_fraction": 0.12279419442414118
    },
    {
      "replicate": 32,
      "checkpoint_step": 12,
      "environment_steps": 24,
      "pulse_capacity_fraction": 0.07027252793150256,
      "no_pulse_capacity_fraction": 0.07162994674741568
    },
    {
      "replicate": 33,
      "checkpoint_step": 13,
      "environment_steps": 25,
      "pulse_capacity_fraction": 0.08812780620235983,
      "no_pulse_capacity_fraction": 0.08635272005847343
    },
    {
      "replicate": 34,
      "checkpoint_step": 14,
      "environment_steps": 26,
      "pulse_capacity_fraction": 0.08802338937036651,
      "no_pulse_capacity_fraction": 0.08363788242664717
    },
    {
      "replicate": 35,
      "checkpoint_step": 15,
      "environment_steps": 27,
      "pulse_capacity_fraction": 0.08958964185026626,
      "no_pulse_capacity_fraction": 0.09209564581810588
    },
    {
      "replicate": 36,
      "checkpoint_step": 16,
      "environment_steps": 28,
      "pulse_capacity_fraction": 0.09355748146601232,
      "no_pulse_capacity_fraction": 0.09303539730604574
    },
    {
      "replicate": 37,
      "checkpoint_step": 17,
      "environment_steps": 29,
      "pulse_capacity_fraction": 0.11370993004072256,
      "no_pulse_capacity_fraction": 0.10807142111308343
    },
    {
      "replicate": 38,
      "checkpoint_step": 18,
      "environment_steps": 30,
      "pulse_capacity_fraction": 0.12582228255194738,
      "no_pulse_capacity_fraction": 0.12206327660018795
    },
    {
      "replicate": 39,
      "checkpoint_step": 19,
      "environment_steps": 31,
      "pulse_capacity_fraction": 0.11694685183251541,
      "no_pulse_capacity_fraction": 0.12498694789600083
    },
    {
      "replicate": 40,
      "checkpoint_step": 12,
      "environment_steps": 24,
      "pulse_capacity_fraction": 0.07424036754724862,
      "no_pulse_capacity_fraction": 0.07079461209146914
    },
    {
      "replicate": 41,
      "checkpoint_step": 13,
      "environment_steps": 25,
      "pulse_capacity_fraction": 0.071734363579409,
      "no_pulse_capacity_fraction": 0.07215203090738227
    },
    {
      "replicate": 42,
      "checkpoint_step": 14,
      "environment_steps": 26,
      "pulse_capacity_fraction": 0.08457763391458703,
      "no_pulse_capacity_fraction": 0.08457763391458703
    },
    {
      "replicate": 43,
      "checkpoint_step": 15,
      "environment_steps": 27,
      "pulse_capacity_fraction": 0.0765375378511016,
      "no_pulse_capacity_fraction": 0.07204761407538895
    },
    {
      "replicate": 44,
      "checkpoint_step": 16,
      "environment_steps": 28,
      "pulse_capacity_fraction": 0.08635272005847343,
      "no_pulse_capacity_fraction": 0.08217604677874073
    },
    {
      "replicate": 45,
      "checkpoint_step": 17,
      "environment_steps": 29,
      "pulse_capacity_fraction": 0.10138874386551112,
      "no_pulse_capacity_fraction": 0.10420799832933068
    },
    {
      "replicate": 46,
      "checkpoint_step": 18,
      "environment_steps": 30,
      "pulse_capacity_fraction": 0.1284327033517803,
      "no_pulse_capacity_fraction": 0.1284327033517803
    },
    {
      "replicate": 47,
      "checkpoint_step": 19,
      "environment_steps": 31,
      "pulse_capacity_fraction": 0.10880233893703666,
      "no_pulse_capacity_fraction": 0.11120392607288294
    },
    {
      "replicate": 48,
      "checkpoint_step": 12,
      "environment_steps": 24,
      "pulse_capacity_fraction": 0.07831262399498799,
      "no_pulse_capacity_fraction": 0.07737287250704813
    },
    {
      "replicate": 49,
      "checkpoint_step": 13,
      "environment_steps": 25,
      "pulse_capacity_fraction": 0.08415996658661376,
      "no_pulse_capacity_fraction": 0.08384671609063381
    },
    {
      "replicate": 50,
      "checkpoint_step": 14,
      "environment_steps": 26,
      "pulse_capacity_fraction": 0.08718805471441997,
      "no_pulse_capacity_fraction": 0.0971076537537851
    },
    {
      "replicate": 51,
      "checkpoint_step": 15,
      "environment_steps": 27,
      "pulse_capacity_fraction": 0.08645713689046675,
      "no_pulse_capacity_fraction": 0.0867703873864467
    },
    {
      "replicate": 52,
      "checkpoint_step": 16,
      "environment_steps": 28,
      "pulse_capacity_fraction": 0.09971807455361804,
      "no_pulse_capacity_fraction": 0.09961365772162473
    },
    {
      "replicate": 53,
      "checkpoint_step": 17,
      "environment_steps": 29,
      "pulse_capacity_fraction": 0.08457763391458703,
      "no_pulse_capacity_fraction": 0.08844105669833978
    },
    {
      "replicate": 54,
      "checkpoint_step": 18,
      "environment_steps": 30,
      "pulse_capacity_fraction": 0.1295812885037068,
      "no_pulse_capacity_fraction": 0.12686645087188056
    },
    {
      "replicate": 55,
      "checkpoint_step": 19,
      "environment_steps": 31,
      "pulse_capacity_fraction": 0.11987052312832829,
      "no_pulse_capacity_fraction": 0.12425603007204761
    },
    {
      "replicate": 56,
      "checkpoint_step": 12,
      "environment_steps": 24,
      "pulse_capacity_fraction": 0.054505586300511645,
      "no_pulse_capacity_fraction": 0.0548188367964916
    },
    {
      "replicate": 57,
      "checkpoint_step": 13,
      "environment_steps": 25,
      "pulse_capacity_fraction": 0.07069019525947583,
      "no_pulse_capacity_fraction": 0.07069019525947583
    },
    {
      "replicate": 58,
      "checkpoint_step": 14,
      "environment_steps": 26,
      "pulse_capacity_fraction": 0.0971076537537851,
      "no_pulse_capacity_fraction": 0.09021614284222616
    },
    {
      "replicate": 59,
      "checkpoint_step": 15,
      "environment_steps": 27,
      "pulse_capacity_fraction": 0.07382270021927535,
      "no_pulse_capacity_fraction": 0.07194319724339564
    },
    {
      "replicate": 60,
      "checkpoint_step": 16,
      "environment_steps": 28,
      "pulse_capacity_fraction": 0.08541296857053357,
      "no_pulse_capacity_fraction": 0.0904249765062128
    },
    {
      "replicate": 61,
      "checkpoint_step": 17,
      "environment_steps": 29,
      "pulse_capacity_fraction": 0.08875430719431972,
      "no_pulse_capacity_fraction": 0.09021614284222616
    },
    {
      "replicate": 62,
      "checkpoint_step": 18,
      "environment_steps": 30,
      "pulse_capacity_fraction": 0.11538059935261565,
      "no_pulse_capacity_fraction": 0.11548501618460896
    },
    {
      "replicate": 63,
      "checkpoint_step": 19,
      "environment_steps": 31,
      "pulse_capacity_fraction": 0.11485851519264906,
      "no_pulse_capacity_fraction": 0.12049702412028819
    },
    {
      "replicate": 64,
      "checkpoint_step": 12,
      "environment_steps": 24,
      "pulse_capacity_fraction": 0.07977445964289444,
      "no_pulse_capacity_fraction": 0.07340503289130208
    },
    {
      "replicate": 65,
      "checkpoint_step": 13,
      "environment_steps": 25,
      "pulse_capacity_fraction": 0.07831262399498799,
      "no_pulse_capacity_fraction": 0.082593714106714
    },
    {
      "replicate": 66,
      "checkpoint_step": 14,
      "environment_steps": 26,
      "pulse_capacity_fraction": 0.07497128537120183,
      "no_pulse_capacity_fraction": 0.08290696460269395
    },
    {
      "replicate": 67,
      "checkpoint_step": 15,
      "environment_steps": 27,
      "pulse_capacity_fraction": 0.08760572204239324,
      "no_pulse_capacity_fraction": 0.08771013887438656
    },
    {
      "replicate": 68,
      "checkpoint_step": 16,
      "environment_steps": 28,
      "pulse_capacity_fraction": 0.10734050328913021,
      "no_pulse_capacity_fraction": 0.10692283596115694
    },
    {
      "replicate": 69,
      "checkpoint_step": 17,
      "environment_steps": 29,
      "pulse_capacity_fraction": 0.10713166962514357,
      "no_pulse_capacity_fraction": 0.10159757752949776
    },
    {
      "replicate": 70,
      "checkpoint_step": 18,
      "environment_steps": 30,
      "pulse_capacity_fraction": 0.11308342904876266,
      "no_pulse_capacity_fraction": 0.10953325676098988
    },
    {
      "replicate": 71,
      "checkpoint_step": 19,
      "environment_steps": 31,
      "pulse_capacity_fraction": 0.12436044690404092,
      "no_pulse_capacity_fraction": 0.121750026104208
    },
    {
      "replicate": 72,
      "checkpoint_step": 12,
      "environment_steps": 24,
      "pulse_capacity_fraction": 0.0728829487313355,
      "no_pulse_capacity_fraction": 0.06661793881173646
    },
    {
      "replicate": 73,
      "checkpoint_step": 13,
      "environment_steps": 25,
      "pulse_capacity_fraction": 0.06661793881173646,
      "no_pulse_capacity_fraction": 0.06661793881173646
    },
    {
      "replicate": 74,
      "checkpoint_step": 14,
      "environment_steps": 26,
      "pulse_capacity_fraction": 0.08708363788242665,
      "no_pulse_capacity_fraction": 0.08990289234624621
    },
    {
      "replicate": 75,
      "checkpoint_step": 15,
      "environment_steps": 27,
      "pulse_capacity_fraction": 0.07987887647488776,
      "no_pulse_capacity_fraction": 0.08040096063485434
    },
    {
      "replicate": 76,
      "checkpoint_step": 16,
      "environment_steps": 28,
      "pulse_capacity_fraction": 0.1036859141693641,
      "no_pulse_capacity_fraction": 0.10504333298527722
    },
    {
      "replicate": 77,
      "checkpoint_step": 17,
      "environment_steps": 29,
      "pulse_capacity_fraction": 0.08697922105043333,
      "no_pulse_capacity_fraction": 0.09146914482614597
    },
    {
      "replicate": 78,
      "checkpoint_step": 18,
      "environment_steps": 30,
      "pulse_capacity_fraction": 0.10984650725696983,
      "no_pulse_capacity_fraction": 0.10995092408896313
    },
    {
      "replicate": 79,
      "checkpoint_step": 19,
      "environment_steps": 31,
      "pulse_capacity_fraction": 0.12060144095228151,
      "no_pulse_capacity_fraction": 0.11652918450454214
    },
    {
      "replicate": 80,
      "checkpoint_step": 12,
      "environment_steps": 24,
      "pulse_capacity_fraction": 0.06839302495562284,
      "no_pulse_capacity_fraction": 0.06839302495562284
    },
    {
      "replicate": 81,
      "checkpoint_step": 13,
      "environment_steps": 25,
      "pulse_capacity_fraction": 0.07131669625143573,
      "no_pulse_capacity_fraction": 0.0687062754516028
    },
    {
      "replicate": 82,
      "checkpoint_step": 14,
      "environment_steps": 26,
      "pulse_capacity_fraction": 0.0735094497232954,
      "no_pulse_capacity_fraction": 0.07507570220319515
    },
    {
      "replicate": 83,
      "checkpoint_step": 15,
      "environment_steps": 27,
      "pulse_capacity_fraction": 0.10170199436149108,
      "no_pulse_capacity_fraction": 0.09428839928996555
    },
    {
      "replicate": 84,
      "checkpoint_step": 16,
      "environment_steps": 28,
      "pulse_capacity_fraction": 0.09658556959381852,
      "no_pulse_capacity_fraction": 0.09554140127388536
    },
    {
      "replicate": 85,
      "checkpoint_step": 17,
      "environment_steps": 29,
      "pulse_capacity_fraction": 0.09836065573770492,
      "no_pulse_capacity_fraction": 0.10034457554557795
    },
    {
      "replicate": 86,
      "checkpoint_step": 18,
      "environment_steps": 30,
      "pulse_capacity_fraction": 0.1132922627127493,
      "no_pulse_capacity_fraction": 0.11089067557690299
    },
    {
      "replicate": 87,
      "checkpoint_step": 19,
      "environment_steps": 31,
      "pulse_capacity_fraction": 0.12874595384776025,
      "no_pulse_capacity_fraction": 0.13104312415161323
    },
    {
      "replicate": 88,
      "checkpoint_step": 12,
      "environment_steps": 24,
      "pulse_capacity_fraction": 0.0771640388430615,
      "no_pulse_capacity_fraction": 0.08395113292262713
    },
    {
      "replicate": 89,
      "checkpoint_step": 13,
      "environment_steps": 25,
      "pulse_capacity_fraction": 0.0753889526991751,
      "no_pulse_capacity_fraction": 0.07726845567505482
    },
    {
      "replicate": 90,
      "checkpoint_step": 14,
      "environment_steps": 26,
      "pulse_capacity_fraction": 0.08844105669833978,
      "no_pulse_capacity_fraction": 0.09407956562597891
    },
    {
      "replicate": 91,
      "checkpoint_step": 15,
      "environment_steps": 27,
      "pulse_capacity_fraction": 0.08635272005847343,
      "no_pulse_capacity_fraction": 0.08583063589850684
    },
    {
      "replicate": 92,
      "checkpoint_step": 16,
      "environment_steps": 28,
      "pulse_capacity_fraction": 0.0807142111308343,
      "no_pulse_capacity_fraction": 0.07977445964289444
    },
    {
      "replicate": 93,
      "checkpoint_step": 17,
      "environment_steps": 29,
      "pulse_capacity_fraction": 0.11287459538477602,
      "no_pulse_capacity_fraction": 0.11579826668058892
    },
    {
      "replicate": 94,
      "checkpoint_step": 18,
      "environment_steps": 30,
      "pulse_capacity_fraction": 0.11955727263234833,
      "no_pulse_capacity_fraction": 0.12133235877623473
    },
    {
      "replicate": 95,
      "checkpoint_step": 19,
      "environment_steps": 31,
      "pulse_capacity_fraction": 0.11830427064842852,
      "no_pulse_capacity_fraction": 0.11903518847238174
    },
    {
      "replicate": 96,
      "checkpoint_step": 12,
      "environment_steps": 24,
      "pulse_capacity_fraction": 0.06693118930771641,
      "no_pulse_capacity_fraction": 0.06849744178761616
    },
    {
      "replicate": 97,
      "checkpoint_step": 13,
      "environment_steps": 25,
      "pulse_capacity_fraction": 0.07392711705126867,
      "no_pulse_capacity_fraction": 0.08019212697086771
    },
    {
      "replicate": 98,
      "checkpoint_step": 14,
      "environment_steps": 26,
      "pulse_capacity_fraction": 0.0789391249869479,
      "no_pulse_capacity_fraction": 0.08081862796282761
    },
    {
      "replicate": 99,
      "checkpoint_step": 15,
      "environment_steps": 27,
      "pulse_capacity_fraction": 0.08520413490654694,
      "no_pulse_capacity_fraction": 0.08520413490654694
    },
    {
      "replicate": 100,
      "checkpoint_step": 16,
      "environment_steps": 28,
      "pulse_capacity_fraction": 0.09481048344993213,
      "no_pulse_capacity_fraction": 0.09387073196199228
    },
    {
      "replicate": 101,
      "checkpoint_step": 17,
      "environment_steps": 29,
      "pulse_capacity_fraction": 0.09084264383418607,
      "no_pulse_capacity_fraction": 0.09084264383418607
    },
    {
      "replicate": 102,
      "checkpoint_step": 18,
      "environment_steps": 30,
      "pulse_capacity_fraction": 0.11809543698444189,
      "no_pulse_capacity_fraction": 0.11402318053670252
    },
    {
      "replicate": 103,
      "checkpoint_step": 19,
      "environment_steps": 31,
      "pulse_capacity_fraction": 0.1175733528244753,
      "no_pulse_capacity_fraction": 0.11579826668058892
    },
    {
      "replicate": 104,
      "checkpoint_step": 12,
      "environment_steps": 24,
      "pulse_capacity_fraction": 0.08384671609063381,
      "no_pulse_capacity_fraction": 0.08269813093870731
    },
    {
      "replicate": 105,
      "checkpoint_step": 13,
      "environment_steps": 25,
      "pulse_capacity_fraction": 0.08353346559465386,
      "no_pulse_capacity_fraction": 0.07591103685914169
    },
    {
      "replicate": 106,
      "checkpoint_step": 14,
      "environment_steps": 26,
      "pulse_capacity_fraction": 0.0964811527618252,
      "no_pulse_capacity_fraction": 0.0958546517698653
    },
    {
      "replicate": 107,
      "checkpoint_step": 15,
      "environment_steps": 27,
      "pulse_capacity_fraction": 0.08635272005847343,
      "no_pulse_capacity_fraction": 0.0849953012425603
    },
    {
      "replicate": 108,
      "checkpoint_step": 16,
      "environment_steps": 28,
      "pulse_capacity_fraction": 0.08833663986634646,
      "no_pulse_capacity_fraction": 0.08864989036232641
    },
    {
      "replicate": 109,
      "checkpoint_step": 17,
      "environment_steps": 29,
      "pulse_capacity_fraction": 0.10379033100135741,
      "no_pulse_capacity_fraction": 0.10723608645713689
    },
    {
      "replicate": 110,
      "checkpoint_step": 18,
      "environment_steps": 30,
      "pulse_capacity_fraction": 0.10932442309700324,
      "no_pulse_capacity_fraction": 0.10932442309700324
    },
    {
      "replicate": 111,
      "checkpoint_step": 19,
      "environment_steps": 31,
      "pulse_capacity_fraction": 0.12394277957606767,
      "no_pulse_capacity_fraction": 0.12091469144826146
    },
    {
      "replicate": 112,
      "checkpoint_step": 12,
      "environment_steps": 24,
      "pulse_capacity_fraction": 0.06839302495562284,
      "no_pulse_capacity_fraction": 0.06494726949984338
    },
    {
      "replicate": 113,
      "checkpoint_step": 13,
      "environment_steps": 25,
      "pulse_capacity_fraction": 0.06265009919599039,
      "no_pulse_capacity_fraction": 0.06338101701994361
    },
    {
      "replicate": 114,
      "checkpoint_step": 14,
      "environment_steps": 26,
      "pulse_capacity_fraction": 0.07591103685914169,
      "no_pulse_capacity_fraction": 0.0795656259789078
    },
    {
      "replicate": 115,
      "checkpoint_step": 15,
      "environment_steps": 27,
      "pulse_capacity_fraction": 0.07862587449096795,
      "no_pulse_capacity_fraction": 0.08019212697086771
    },
    {
      "replicate": 116,
      "checkpoint_step": 16,
      "environment_steps": 28,
      "pulse_capacity_fraction": 0.0958546517698653,
      "no_pulse_capacity_fraction": 0.0982562389057116
    },
    {
      "replicate": 117,
      "checkpoint_step": 17,
      "environment_steps": 29,
      "pulse_capacity_fraction": 0.09689882008979847,
      "no_pulse_capacity_fraction": 0.09439281612195886
    },
    {
      "replicate": 118,
      "checkpoint_step": 18,
      "environment_steps": 30,
      "pulse_capacity_fraction": 0.10911558943301661,
      "no_pulse_capacity_fraction": 0.11558943301660228
    },
    {
      "replicate": 119,
      "checkpoint_step": 19,
      "environment_steps": 31,
      "pulse_capacity_fraction": 0.1139187637047092,
      "no_pulse_capacity_fraction": 0.11527618252062233
    }
  ],
  "normalized_final_difference": {
    "n": 120,
    "mean": 0.16328068044830893,
    "std": 0.04058248108548066,
    "median": 0.16673169267707083,
    "q05": 0.12941170785933792,
    "q25": 0.15055192046009977,
    "q75": 0.18629797834823258,
    "q95": 0.20410377203367533,
    "min": 0.0,
    "max": 0.24843161856963614
  },
  "symmetric_difference_cells": {
    "n": 120,
    "mean": 157.81666666666666,
    "std": 41.341057745969145,
    "median": 162.5,
    "q05": 106.9,
    "q25": 144.25,
    "q75": 177.75,
    "q95": 208.05,
    "min": 0.0,
    "max": 245.0
  },
  "fraction_with_any_morphology_change": 0.9583333333333334,
  "mean_attachment_impulse_response": [
    1.8083333333333333,
    0.0,
    -0.3416666666666667,
    -0.075,
    -0.3,
    -0.31666666666666665,
    -0.39166666666666666,
    -0.35,
    -0.6083333333333333,
    -0.25833333333333336,
    -0.25,
    -0.75
  ],
  "figure": "static\\images\\books\\digital-life\\ch16-02-single-bit-impulse-response.png"
}
```

Figure: `static\images\books\digital-life\ch16-02-single-bit-impulse-response.png`

If this stage does not produce repeatable receiver differences, the channel is
decorative and no stronger signalling claim is allowed.


# Stage 3 — Correlation Is Not Communication

The receiver is tested against six streams:

```text
REAL sender events

SHUFFLED
same bits, chronology destroyed

UNRELATED REPLAY — COUNT MATCHED
different sender of the same Digital Crystal class,
forced to exactly the same pulse count as the real stream

IPI-PERMUTATION SURROGATE
same pulse count and exact multiset of inter-pulse intervals,
but interval order is permuted

RATE-MATCHED RANDOM
same number of bits, random times

NO CHANNEL
```

Every replicate first finds the longest **common** receiver horizon for which
all six conditions remain below the predeclared hard-radius saturation guard of
`0.85`. Every condition in that replicate is then evaluated
at exactly that same horizon. Saturation therefore cannot make one control run
for less time than another or collapse all endpoint morphologies onto the same
filled disk.

```json
{
  "replicates": 60,
  "message_gain": 0.65,
  "saturation_guard": 0.85,
  "hard_radius_capacity": 9577,
  "requested_steps": 90,
  "common_safe_horizon_summary": {
    "n": 60,
    "mean": 75.5,
    "std": 1.1761519176251567,
    "median": 76.0,
    "q05": 73.95,
    "q25": 75.0,
    "q75": 76.0,
    "q95": 77.0,
    "min": 73.0,
    "max": 78.0
  },
  "all_replicates_used_equal_horizon_across_conditions": true,
  "control_summary": {
    "real": {
      "peak_lagged_corr": {
        "n": 60,
        "mean": 0.3672576243656597,
        "std": 0.08830823801523097,
        "median": 0.36823195150536003,
        "q05": 0.20610711012075747,
        "q25": 0.31692903422462015,
        "q75": 0.41832914893351564,
        "q95": 0.5002644280510793,
        "min": 0.17097560675968193,
        "max": 0.5678506771802312
      },
      "post_message_growth": {
        "n": 60,
        "mean": 118.33456671747186,
        "std": 4.793864829417774,
        "median": 118.04217076901682,
        "q05": 111.21161067193674,
        "q25": 114.83195200395843,
        "q75": 121.42276324289406,
        "q95": 125.26300366300366,
        "min": 109.59259259259258,
        "max": 131.04761904761907
      },
      "final_difference_vs_no_channel": {
        "n": 60,
        "mean": 0.09942738025111161,
        "std": 0.010460074526400957,
        "median": 0.0989472445274697,
        "q05": 0.08608343600893557,
        "q25": 0.09181040830674139,
        "q75": 0.10740292432368564,
        "q95": 0.11572561137915068,
        "min": 0.07956356503616525,
        "max": 0.12840285080032715
      },
      "capacity_fraction": {
        "n": 60,
        "mean": 0.8176481848874038,
        "std": 0.026547748294444902,
        "median": 0.827921060875013,
        "q05": 0.7788921374125509,
        "q25": 0.8032525843165919,
        "q75": 0.8365354495144617,
        "q95": 0.847248616476976,
        "min": 0.7300824892972747,
        "max": 0.8498485955936097
      },
      "pulse_count": {
        "n": 60,
        "mean": 47.46666666666667,
        "std": 2.4729649321321876,
        "median": 48.0,
        "q05": 43.0,
        "q25": 46.0,
        "q75": 49.0,
        "q95": 51.05,
        "min": 42.0,
        "max": 52.0
      },
      "peak_lag": {
        "n": 60,
        "mean": 7.883333333333334,
        "std": 3.979496059664953,
        "median": 9.0,
        "q05": 0.0,
        "q25": 5.75,
        "q75": 11.25,
        "q95": 12.0,
        "min": 0.0,
        "max": 12.0
      }
    },
    "shuffled": {
      "peak_lagged_corr": {
        "n": 60,
        "mean": 0.07330226093493512,
        "std": 0.1202878632956531,
        "median": 0.0889440798346463,
        "q05": -0.13842222981098137,
        "q25": -0.0010428130187523162,
        "q75": 0.1617040741938104,
        "q95": 0.2484407616239922,
        "min": -0.19606859976570434,
        "max": 0.26696862931348997
      },
      "post_message_growth": {
        "n": 60,
        "mean": 106.3279892473885,
        "std": 7.28577419699968,
        "median": 107.33430458430458,
        "q05": 93.53242242242241,
        "q25": 101.80148809523808,
        "q75": 112.49166666666667,
        "q95": 117.14910287081341,
        "min": 85.41085271317829,
        "max": 119.03875968992247
      },
      "final_difference_vs_no_channel": {
        "n": 60,
        "mean": 0.10862395180180859,
        "std": 0.016727631403359585,
        "median": 0.1053072602884958,
        "q05": 0.08660292456065675,
        "q25": 0.0969966766828286,
        "q75": 0.12085432347851761,
        "q95": 0.13183992113992277,
        "min": 0.06987237334020885,
        "max": 0.16908884114747882
      },
      "capacity_fraction": {
        "n": 60,
        "mean": 0.8166649263861334,
        "std": 0.023797462699489593,
        "median": 0.823170095019317,
        "q05": 0.7729925864049285,
        "q25": 0.8017124360446903,
        "q75": 0.8357784274825102,
        "q95": 0.844110890675577,
        "min": 0.7593192022554036,
        "max": 0.8466116738018169
      },
      "pulse_count": {
        "n": 60,
        "mean": 41.3,
        "std": 2.9737742572921255,
        "median": 41.0,
        "q05": 35.95,
        "q25": 40.0,
        "q75": 43.0,
        "q95": 46.0,
        "min": 35.0,
        "max": 48.0
      },
      "peak_lag": {
        "n": 60,
        "mean": 4.833333333333333,
        "std": 4.879093722768149,
        "median": 4.0,
        "q05": 0.0,
        "q25": 0.0,
        "q75": 9.25,
        "q95": 12.0,
        "min": 0.0,
        "max": 12.0
      }
    },
    "unrelated_replay_count_matched": {
      "peak_lagged_corr": {
        "n": 60,
        "mean": 0.38233599859631373,
        "std": 0.08721820539751232,
        "median": 0.37006883165601523,
        "q05": 0.22310898441264745,
        "q25": 0.3298002587747973,
        "q75": 0.44682529747433514,
        "q95": 0.5167164460816047,
        "min": 0.17500858815082412,
        "max": 0.5841725831914119
      },
      "post_message_growth": {
        "n": 60,
        "mean": 118.28250048225715,
        "std": 5.7588731374962014,
        "median": 118.48731884057969,
        "q05": 108.49634259259257,
        "q25": 114.93720147633522,
        "q75": 121.5656429238362,
        "q95": 128.53387295713847,
        "min": 106.00694444444444,
        "max": 129.12015503875966
      },
      "final_difference_vs_no_channel": {
        "n": 60,
        "mean": 0.09739943211326677,
        "std": 0.011345830424237225,
        "median": 0.09549240927002622,
        "q05": 0.08164266896189828,
        "q25": 0.0880656233347802,
        "q75": 0.10540727886528789,
        "q95": 0.11981249724843343,
        "min": 0.07269179168191243,
        "max": 0.12265178328341955
      },
      "capacity_fraction": {
        "n": 60,
        "mean": 0.814780202568654,
        "std": 0.022831624964018325,
        "median": 0.8175837945076747,
        "q05": 0.7688942257491908,
        "q25": 0.8036963558525634,
        "q75": 0.8305053774668476,
        "q95": 0.8439699279523859,
        "min": 0.7420904249765062,
        "max": 0.84828234311371
      },
      "pulse_count": {
        "n": 60,
        "mean": 47.333333333333336,
        "std": 2.7426669907632286,
        "median": 47.0,
        "q05": 43.0,
        "q25": 45.75,
        "q75": 49.0,
        "q95": 51.05,
        "min": 43.0,
        "max": 56.0
      },
      "peak_lag": {
        "n": 60,
        "mean": 7.6,
        "std": 4.131989028704376,
        "median": 9.0,
        "q05": 0.0,
        "q25": 4.0,
        "q75": 11.0,
        "q95": 12.0,
        "min": 0.0,
        "max": 12.0
      }
    },
    "ipi_permutation_surrogate": {
      "peak_lagged_corr": {
        "n": 60,
        "mean": 0.3568837829278093,
        "std": 0.24906804992006232,
        "median": 0.39908724952423164,
        "q05": -0.04662407700122897,
        "q25": 0.18517475041604387,
        "q75": 0.5352533331507222,
        "q95": 0.7149744304522527,
        "min": -0.28686194011280447,
        "max": 0.760898571184882
      },
      "post_message_growth": {
        "n": 60,
        "mean": 116.77985379986605,
        "std": 17.19332719166506,
        "median": 116.11307919394172,
        "q05": 88.89274231678488,
        "q25": 103.51444444444445,
        "q75": 129.1187510811278,
        "q95": 144.81104166666665,
        "min": 83.17307692307693,
        "max": 151.70731707317074
      },
      "final_difference_vs_no_channel": {
        "n": 60,
        "mean": 0.09901520137424781,
        "std": 0.012682144519349096,
        "median": 0.09503778947432479,
        "q05": 0.08118215758814697,
        "q25": 0.09095302937505673,
        "q75": 0.1063123981387548,
        "q95": 0.12025246660196375,
        "min": 0.07818088911599387,
        "max": 0.1383890834440285
      },
      "capacity_fraction": {
        "n": 60,
        "mean": 0.8161236991403015,
        "std": 0.025122521185842912,
        "median": 0.8191500469875744,
        "q05": 0.7665552887125404,
        "q25": 0.8056280672444398,
        "q75": 0.8392241829382896,
        "q95": 0.8462984233058369,
        "min": 0.7439699279523859,
        "max": 0.8485955936096898
      },
      "pulse_count": {
        "n": 60,
        "mean": 46.583333333333336,
        "std": 4.375277768959996,
        "median": 47.0,
        "q05": 39.0,
        "q25": 44.0,
        "q75": 50.0,
        "q95": 53.0,
        "min": 34.0,
        "max": 56.0
      },
      "peak_lag": {
        "n": 60,
        "mean": 7.35,
        "std": 4.05308524460071,
        "median": 8.0,
        "q05": 0.0,
        "q25": 3.75,
        "q75": 11.0,
        "q95": 12.0,
        "min": 0.0,
        "max": 12.0
      }
    },
    "rate_matched_random": {
      "peak_lagged_corr": {
        "n": 60,
        "mean": 0.09737060379589658,
        "std": 0.10691832357113344,
        "median": 0.11082465742557349,
        "q05": -0.07262456915797011,
        "q25": 0.02081175934988306,
        "q75": 0.1750820537841149,
        "q95": 0.26444665033916187,
        "min": -0.16792758465860294,
        "max": 0.28060997237438867
      },
      "post_message_growth": {
        "n": 60,
        "mean": 108.41278488548718,
        "std": 6.827834030544102,
        "median": 108.95670045045044,
        "q05": 97.46068665377176,
        "q25": 103.5093984962406,
        "q75": 113.91948621553885,
        "q95": 117.89989233419466,
        "min": 94.31818181818181,
        "max": 122.02916666666665
      },
      "final_difference_vs_no_channel": {
        "n": 60,
        "mean": 0.10580153987731428,
        "std": 0.017390779759052528,
        "median": 0.10202646276910096,
        "q05": 0.08543835697295755,
        "q25": 0.09259653574805683,
        "q75": 0.1144357053484759,
        "q95": 0.13731105766024143,
        "min": 0.07899440009531752,
        "max": 0.16606045403235922
      },
      "capacity_fraction": {
        "n": 60,
        "mean": 0.8185496502036129,
        "std": 0.02005882061839006,
        "median": 0.823639970763287,
        "q05": 0.7810692283596116,
        "q25": 0.8033308969405868,
        "q75": 0.8338728202986322,
        "q95": 0.8456614806306777,
        "min": 0.7652709616790226,
        "max": 0.8499530124256031
      },
      "pulse_count": {
        "n": 60,
        "mean": 41.05,
        "std": 3.106042498099471,
        "median": 41.5,
        "q05": 35.0,
        "q25": 39.0,
        "q75": 44.0,
        "q95": 46.0,
        "min": 35.0,
        "max": 47.0
      },
      "peak_lag": {
        "n": 60,
        "mean": 4.683333333333334,
        "std": 4.720493147495879,
        "median": 4.0,
        "q05": 0.0,
        "q25": 0.0,
        "q75": 9.0,
        "q95": 12.0,
        "min": 0.0,
        "max": 12.0
      }
    },
    "no_channel": {
      "peak_lagged_corr": {
        "n": 60,
        "mean": 0.0,
        "std": 0.0,
        "median": 0.0,
        "q05": 0.0,
        "q25": 0.0,
        "q75": 0.0,
        "q95": 0.0,
        "min": 0.0,
        "max": 0.0
      },
      "post_message_growth": {
        "n": 60,
        "mean": 0.0,
        "std": 0.0,
        "median": 0.0,
        "q05": 0.0,
        "q25": 0.0,
        "q75": 0.0,
        "q95": 0.0,
        "min": 0.0,
        "max": 0.0
      },
      "final_difference_vs_no_channel": {
        "n": 60,
        "mean": 0.0,
        "std": 0.0,
        "median": 0.0,
        "q05": 0.0,
        "q25": 0.0,
        "q75": 0.0,
        "q95": 0.0,
        "min": 0.0,
        "max": 0.0
      },
      "capacity_fraction": {
        "n": 60,
        "mean": 0.7982109916118478,
        "std": 0.026298745840089177,
        "median": 0.7976923880129477,
        "q05": 0.7630259997911664,
        "q25": 0.7856844523337162,
        "q75": 0.8139292053879085,
        "q95": 0.8363892659496711,
        "min": 0.697922105043333,
        "max": 0.8481779262817166
      },
      "pulse_count": {
        "n": 60,
        "mean": 0.0,
        "std": 0.0,
        "median": 0.0,
        "q05": 0.0,
        "q25": 0.0,
        "q75": 0.0,
        "q95": 0.0,
        "min": 0.0,
        "max": 0.0
      },
      "peak_lag": {
        "n": 60,
        "mean": 0.0,
        "std": 0.0,
        "median": 0.0,
        "q05": 0.0,
        "q25": 0.0,
        "q75": 0.0,
        "q95": 0.0,
        "min": 0.0,
        "max": 0.0
      }
    }
  },
  "real_vs_controls": {
    "shuffled": {
      "real_minus_control_mean": 0.29395536343072454,
      "pairwise_superiority_probability": 0.9802777777777778
    },
    "unrelated_replay_count_matched": {
      "real_minus_control_mean": -0.015078374230654057,
      "pairwise_superiority_probability": 0.45694444444444443
    },
    "ipi_permutation_surrogate": {
      "real_minus_control_mean": 0.010373841437850362,
      "pairwise_superiority_probability": 0.4725
    },
    "rate_matched_random": {
      "real_minus_control_mean": 0.2698870205697631,
      "pairwise_superiority_probability": 0.9772222222222222
    }
  },
  "figure": "static\\images\\books\\digital-life\\ch16-03-message-controls.png"
}
```

Figure: `static\images\books\digital-life\ch16-03-message-controls.png`

The real stream must beat not only naive timing controls but also a count-matched
unrelated sender and an exact-IPI-distribution surrogate before sender-specific
signalling is supported.


# Stage 4 — How Fast Does One Bit Matter?

The exact checkpoint intervention from Stage 2 gives an impulse response.

```json
{
  "impulse_response": [
    1.8083333333333333,
    0.0,
    -0.3416666666666667,
    -0.075,
    -0.3,
    -0.31666666666666665,
    -0.39166666666666666,
    -0.35,
    -0.6083333333333333,
    -0.25833333333333336,
    -0.25,
    -0.75
  ],
  "peak_effect_lag_steps": 0,
  "peak_effect": 1.8083333333333333,
  "lag_containing_90pct_absolute_effect_mass": 11,
  "interpretation": "Finite-horizon impulse-response description only. The peak lag is not claimed as a stable characteristic latency, and this is not a channel-capacity result."
}
```

This describes the finite-horizon response of growth to a one-bit causal
perturbation. The largest observed lag is not yet treated as a stable latency
law, and this does not establish information-theoretic capacity.


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


# Stage 7 — Experimental Verdict

**Verdict: `CAUSAL_TRANSMISSION_SUPPORTED`**

> Within this protocol, inserting one received bit into an otherwise identical Digital Crystal continuation reliably changed receiver growth, but the real sender-generated event stream did not clear all controls required for a sender-specific signalling claim.

```json
{
  "verdict": "CAUSAL_TRANSMISSION_SUPPORTED",
  "bounded_claim": "Within this protocol, inserting one received bit into an otherwise identical Digital Crystal continuation reliably changed receiver growth, but the real sender-generated event stream did not clear all controls required for a sender-specific signalling claim.",
  "checks": {
    "single_bit_changes_receiver_reliably": true,
    "real_stream_beats_all_message_controls": false
  },
  "headline_metrics": {
    "single_bit_fraction_with_any_morphology_change": 0.9583333333333334,
    "single_bit_mean_normalized_final_difference": 0.16328068044830893,
    "real_vs_shuffled": {
      "real_minus_control_mean": 0.29395536343072454,
      "pairwise_superiority_probability": 0.9802777777777778
    },
    "real_vs_unrelated_replay_count_matched": {
      "real_minus_control_mean": -0.015078374230654057,
      "pairwise_superiority_probability": 0.45694444444444443
    },
    "real_vs_ipi_permutation_surrogate": {
      "real_minus_control_mean": 0.010373841437850362,
      "pairwise_superiority_probability": 0.4725
    },
    "real_vs_rate_matched_random": {
      "real_minus_control_mean": 0.2698870205697631,
      "pairwise_superiority_probability": 0.9772222222222222
    },
    "impulse_peak_lag": 0,
    "chain_real_source_to_node_corr": [
      1.0,
      0.5373421448225714,
      0.476502004766455,
      0.46214947215469776,
      0.4620092356556393,
      0.4578017794000673
    ],
    "board_real_minus_shuffled_neighbor_corr": 0.004826701878735018
  },
  "kill_conditions": {
    "decorative_channel": "Triggered if exact pulse/no-pulse checkpoint interventions do not reliably change the receiver.",
    "not_sender_specific": "Triggered if real sender timing does not beat shuffled, count-matched unrelated replay, exact-IPI surrogate, and rate-matched-random controls."
  },
  "explicit_nonclaims": [
    "language",
    "semantics",
    "meaning",
    "cooperation",
    "coordination",
    "planning",
    "learning",
    "intelligence",
    "agency",
    "individuality",
    "selfhood",
    "life",
    "channel capacity"
  ]
}
```

