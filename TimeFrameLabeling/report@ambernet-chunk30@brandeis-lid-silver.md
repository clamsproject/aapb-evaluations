# Evaluation Report for `TimeFrameLabeling` task as of 2025-11-28 05:36:39.325400

## Evaluation method
Evaluating tasks that label time frames such as chyron detection, slate detection, 
and language identification using diarization error rate, purity, and coverage. 

- Diarization Error Rate (DER) is the sum of three types of errors divided by the total duration:
    - False Alarm: A segment is predicted with a label when there is none in the gold
    - Missed Detection: A segment in the gold is not predicted
    - Confusion: A segment is predicted with an incorrect label
- Purity can be understood to be precision-like and measures how much of the predicted
  segments are correctly labeled.
- Coverage can be understood to be recall-like and measures how much of the gold
  segments are labeled underneath a single label. 

Note that for DER, lower is better and can be greater than 100%.
For all metrics, we use the `pyannote` library.
More details can be found at https://pyannote.github.io/pyannote-metrics/reference.html

## Data specs
- Batch name: unspecified (GUIDs: cpb-aacip-lid-silver-001, cpb-aacip-lid-silver-002, cpb-aacip-lid-silver-003, cpb-aacip-lid-silver-004, cpb-aacip-lid-silver-005, cpb-aacip-lid-silver-006, cpb-aacip-lid-silver-007, cpb-aacip-lid-silver-008, cpb-aacip-lid-silver-009, cpb-aacip-lid-silver-010, cpb-aacip-lid-silver-011, cpb-aacip-lid-silver-012, cpb-aacip-lid-silver-013, cpb-aacip-lid-silver-014, cpb-aacip-lid-silver-015, cpb-aacip-lid-silver-016, cpb-aacip-lid-silver-017, cpb-aacip-lid-silver-018, cpb-aacip-lid-silver-019, cpb-aacip-lid-silver-020, cpb-aacip-lid-silver-021, cpb-aacip-lid-silver-022, cpb-aacip-lid-silver-023, cpb-aacip-lid-silver-024, cpb-aacip-lid-silver-025, cpb-aacip-lid-silver-026, cpb-aacip-lid-silver-027, cpb-aacip-lid-silver-028, cpb-aacip-lid-silver-029, cpb-aacip-lid-silver-030, cpb-aacip-lid-silver-031, cpb-aacip-lid-silver-032, cpb-aacip-lid-silver-033, cpb-aacip-lid-silver-034, cpb-aacip-lid-silver-035, cpb-aacip-lid-silver-036, cpb-aacip-lid-silver-037, cpb-aacip-lid-silver-038, cpb-aacip-lid-silver-039, cpb-aacip-lid-silver-040, cpb-aacip-lid-silver-041, cpb-aacip-lid-silver-042, cpb-aacip-lid-silver-043, cpb-aacip-lid-silver-044, cpb-aacip-lid-silver-045, cpb-aacip-lid-silver-046, cpb-aacip-lid-silver-047, cpb-aacip-lid-silver-048, cpb-aacip-lid-silver-049, cpb-aacip-lid-silver-050, cpb-aacip-lid-silver-051, cpb-aacip-lid-silver-052, cpb-aacip-lid-silver-053, cpb-aacip-lid-silver-054, cpb-aacip-lid-silver-055, cpb-aacip-lid-silver-056, cpb-aacip-lid-silver-057, cpb-aacip-lid-silver-058, cpb-aacip-lid-silver-059, cpb-aacip-lid-silver-060)
- Groundtruth data location: /mnt/llc/llc_data/clams/lrslid/prototype-eval-r2-synthetic-data/lid-annotations
- Evaluation code version: [c6ccffc](https://github.com/clamsproject/aapb-evaluations/blob/c6ccffc/TimeFrameLabeling/evaluate.py)

## Workflow specs
- Workflow ID: AudioDocument-1/spoken-lid-ambernet/unversioned/4aadf11365ab150e600472be322a3493
- Workflow App Profilings:
```json
{}
```

## Raw Results
```
GUID,Error-Rate,Purity,Coverage
cpb-aacip-lid-silver-054,0.11162992111159226,0.9178102031210399,0.9283791162239
cpb-aacip-lid-silver-055,0.0780579189758801,0.9594338209596086,0.9642234538027216
cpb-aacip-lid-silver-056,0.03048780487804878,0.9704142011834319,1.0
cpb-aacip-lid-silver-057,0.04125657629826194,0.960378088131811,1.0
cpb-aacip-lid-silver-058,0.39926489571302365,0.6262258553629116,0.8581561247367349
cpb-aacip-lid-silver-059,0.44768630658403835,0.5692514906625504,0.8021642706596622
cpb-aacip-lid-silver-060,0.21261884183232502,0.9035297145062833,0.8480340869459734
cpb-aacip-lid-silver-010,0.3528090698185863,0.6703104077315689,0.8212567235375539
cpb-aacip-lid-silver-011,0.3761602923103574,0.6422802393894467,0.6753899258501658
cpb-aacip-lid-silver-012,0.1780915453459166,0.9107091996582172,0.8493427951325383
cpb-aacip-lid-silver-013,0.10672254131393494,0.9539437835112522,0.9415572601637007
cpb-aacip-lid-silver-014,0.028153153153153154,0.9726177437020811,1.0
cpb-aacip-lid-silver-015,0.0291129290517919,0.9717106565956604,1.0
cpb-aacip-lid-silver-016,0.36473725942478247,0.6708894738665092,0.8328768110718662
cpb-aacip-lid-silver-045,0.05510249063257659,0.9477752245665344,1.0
cpb-aacip-lid-silver-024,0.31346933905989033,0.916966426858513,0.7312693867811977
cpb-aacip-lid-silver-025,0.15920207602120823,0.9427957897701271,0.9014730042565903
cpb-aacip-lid-silver-026,0.02555935669065314,0.975077642728423,1.0
cpb-aacip-lid-silver-027,0.03942947267366111,0.9620662356511414,1.0
cpb-aacip-lid-silver-028,0.3577776171893818,0.6530859064791892,0.9370332899744666
cpb-aacip-lid-silver-029,0.3893585038889896,0.634127718183555,0.7268506135724143
cpb-aacip-lid-silver-030,0.1280849734457982,0.9231403768347453,0.9092674843459245
cpb-aacip-lid-silver-031,0.1320380269517621,0.961527807700594,0.9079734963669537
cpb-aacip-lid-silver-032,0.027036695034398997,0.973675044752424,1.0
cpb-aacip-lid-silver-017,0.39634599881356175,0.621638859847825,0.8219734420394567
cpb-aacip-lid-silver-018,0.19253783543176906,0.9488812598816864,0.8301725077669374
cpb-aacip-lid-silver-019,0.1513829238962377,0.9561955867053605,0.8944282196644334
cpb-aacip-lid-silver-020,0.03433095036148471,0.9668085438712952,1.0
cpb-aacip-lid-silver-021,0.05032206119162641,0.9520889229589881,1.0
cpb-aacip-lid-silver-022,0.3469411187541099,0.6793265898566593,0.8190975230420758
cpb-aacip-lid-silver-023,0.3750490326271276,0.6423069054206771,0.7562159070014507
cpb-aacip-lid-silver-038,0.04662613301503227,0.9554510139349228,1.0
cpb-aacip-lid-silver-039,0.04983752965333014,0.9525283405806734,1.0
cpb-aacip-lid-silver-040,0.35691105151249425,0.6696966155284623,0.8175464772341868
cpb-aacip-lid-silver-041,0.39882285464576395,0.620605887396399,0.6780193368656798
cpb-aacip-lid-silver-042,0.16520318995503536,0.8772307692307691,0.8692627470942562
cpb-aacip-lid-silver-043,0.1526087578024491,0.9523528610972455,0.89742221375137
cpb-aacip-lid-silver-044,0.03759802341819744,0.9637643648410809,1.0
cpb-aacip-lid-silver-036,0.1873075987263168,0.9308040872509521,0.8666335198722085
cpb-aacip-lid-silver-037,0.09122583986628058,0.9741984312646209,0.9352590813852202
cpb-aacip-lid-silver-001,0.1829843597035923,0.9530485350933676,0.8662801459094744
cpb-aacip-lid-silver-002,0.026114530871106136,0.9745500818033085,1.0
cpb-aacip-lid-silver-003,0.03153314133153945,0.969430801524384,1.0
cpb-aacip-lid-silver-004,0.40062094885342364,0.6697948744715274,0.7751184705049295
cpb-aacip-lid-silver-005,0.47731101716648694,0.549526868591567,0.8250295504195178
cpb-aacip-lid-silver-006,0.24197048029787593,0.9074247997704208,0.7848169081996192
cpb-aacip-lid-silver-007,0.058335796400292454,0.98468207649771,0.9572204159731189
cpb-aacip-lid-silver-008,0.036297795656221446,0.9649735859630616,1.0
cpb-aacip-lid-silver-009,0.05900446149863719,0.9442830850635532,1.0
cpb-aacip-lid-silver-033,0.042303331810413375,0.9594136078055752,1.0
cpb-aacip-lid-silver-034,0.33192614674487914,0.6860033885542169,0.8365227425714011
cpb-aacip-lid-silver-035,0.3866523643976889,0.6218989725378193,0.7156777853884229
cpb-aacip-lid-silver-046,0.3183656903199618,0.6961971006955733,0.8246228776297098
cpb-aacip-lid-silver-047,0.3261461824411418,0.68687393710029,0.7154348965046947
cpb-aacip-lid-silver-048,0.20806551740327764,0.8930764510579545,0.8498974913938562
cpb-aacip-lid-silver-049,0.1255101379801775,0.9686264667126812,0.906879575046965
cpb-aacip-lid-silver-050,0.03602670349907914,0.9652777777777778,0.9999424493554329
cpb-aacip-lid-silver-051,0.045266425245732024,0.9566938876515714,1.0
cpb-aacip-lid-silver-052,0.3774858320453371,0.6614523299851807,0.8239738966168642
cpb-aacip-lid-silver-053,0.3589222269059374,0.6464011331276699,0.7967602071540407
Average,0.1914623599607272,0.8485541975560075,0.8916576038634615

### Per Class Metrics
,Error-Rate,Purity,Coverage
en,0.34579838066503066,0.9331771728718509,0.7046608822572887
ceb,0.31571810252039134,0.7688210224620498,0.9785140746327116
es,0.20563977511690093,0.8369523862446611,0.986551383659016

```

## Confusion Matrix
|     | en           | ar           | fa           | tl           | ko           | ru           | es           | nn           | war          | mn           | sw           | iw           | ceb          | pl           | sco          | it           | yo           | ha           | uz           | bg           | ur           | ms           | da           | la           | lt           | lv           | si           | bn           | hr           | haw          | sv           | gl           |
|:----|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|
| en  | 09:48:24.780 | 00:01:30.000 | 00:14:38.380 | 01:37:33.402 | 00:18:23.660 | 00:01:10.140 | 01:23:52.099 | 00:02:52.500 | 00:02:35.780 | 00:03:29.561 | 00:00:44.520 | 00:00:24.720 | 00:01:50.040 | 00:09:35.620 | 00:01:16.040 | 00:00:25.160 | 00:00:24.680 | 00:00:20.000 | 00:00:25.000 | 00:00:25.000 | 00:00:30.000 | 00:00:25.000 | 00:00:21.640 | 00:00:19.920 | 00:00:30.000 | 00:00:25.000 | 00:00:21.180 | 00:00:00.660 | 00:01:00.000 | 00:00:25.000 | 00:00:22.320 | 00:00:00.000 |
| ceb | 00:12:02.380 | 00:00:00.000 | 00:00:03.020 | 08:57:36.458 | 00:00:00.000 | 00:00:00.000 | 00:00:00.000 | 00:00:00.000 | 00:08:48.600 | 00:00:00.060 | 00:00:02.460 | 00:00:00.000 | 00:02:10.500 | 00:00:09.420 | 00:00:00.000 | 00:00:00.000 | 00:00:00.000 | 00:00:00.000 | 00:00:00.000 | 00:00:00.000 | 00:00:00.000 | 00:00:00.000 | 00:00:00.000 | 00:00:10.080 | 00:00:00.000 | 00:00:00.000 | 00:00:00.000 | 00:00:00.000 | 00:00:00.000 | 00:00:00.000 | 00:00:00.000 | 00:00:00.000 |
| es  | 00:06:12.780 | 00:00:00.000 | 00:00:12.120 | 00:00:00.000 | 00:00:16.900 | 00:00:00.000 | 08:57:11.639 | 00:00:15.260 | 00:00:00.000 | 00:00:00.000 | 00:00:00.000 | 00:00:05.280 | 00:00:00.000 | 00:00:00.000 | 00:00:00.000 | 00:00:04.840 | 00:00:00.000 | 00:00:00.000 | 00:00:00.000 | 00:00:00.000 | 00:00:00.000 | 00:00:00.000 | 00:00:00.000 | 00:00:00.000 | 00:00:00.000 | 00:00:00.000 | 00:00:08.820 | 00:00:00.000 | 00:00:00.000 | 00:00:00.000 | 00:00:00.000 | 00:00:03.300 |