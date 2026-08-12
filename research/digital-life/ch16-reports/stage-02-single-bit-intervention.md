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
