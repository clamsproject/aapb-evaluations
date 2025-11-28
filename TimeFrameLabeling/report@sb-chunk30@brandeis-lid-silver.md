# Evaluation Report for `TimeFrameLabeling` task as of 2025-11-28 11:23:22.848673

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
- Evaluation code version: [662973a](https://github.com/clamsproject/aapb-evaluations/blob/662973a/TimeFrameLabeling/evaluate.py)

## Workflow specs
- Workflow ID: `AudioDocument-1/voxlingua-lid/unversioned/d41d8cd98f00b204e9800998ecf8427e`
- MMIFs in workflow: 60
### App: `https://apps.clams.ai/voxlingua-lid/unresolvable`
#### Configuration
```json
{
  "chunk": 30.0,
  "top": 3,
  "device": "auto",
  "pretty": false,
  "runningTime": false,
  "hwFetch": false
}
```
#### Profiling
```json
{}
```

## Raw Results
```
GUID,Error-Rate,Purity,Coverage
cpb-aacip-lid-silver-054,0.23327622239376425,0.9134774774774775,0.8116656938979158
cpb-aacip-lid-silver-055,0.14484947831290823,0.9489629629629629,0.9089324278614732
cpb-aacip-lid-silver-056,0.036585365853658534,0.9647058823529412,1.0
cpb-aacip-lid-silver-057,0.04956730102778377,0.9527735849056604,1.0
cpb-aacip-lid-silver-058,0.41389904205448697,0.6457790849673206,0.8207894558054216
cpb-aacip-lid-silver-059,0.45419799301645225,0.5721925925925926,0.8178929818490673
cpb-aacip-lid-silver-060,0.202141048385874,0.8964680851063831,0.866866821331635
cpb-aacip-lid-silver-010,0.37692538520228075,0.671757004830918,0.7786749452323186
cpb-aacip-lid-silver-011,0.3958401035953186,0.6235917647058822,0.7214143730256267
cpb-aacip-lid-silver-012,0.18362718560245805,0.8975438596491229,0.8588777525788281
cpb-aacip-lid-silver-013,0.18041070508370524,0.9505980676328503,0.871558611969683
cpb-aacip-lid-silver-014,0.036036036036036036,0.9652173913043478,1.0
cpb-aacip-lid-silver-015,0.03350898133861245,0.9675774647887324,1.0
cpb-aacip-lid-silver-016,0.3482213652418371,0.6856883116883113,0.7927629207813739
cpb-aacip-lid-silver-045,0.06531481889648083,0.9386896551724138,1.0
cpb-aacip-lid-silver-024,0.20694643283225958,0.9111914893617019,0.8444136244333096
cpb-aacip-lid-silver-025,0.1971660070196401,0.9397192982456141,0.8669815547755956
cpb-aacip-lid-silver-026,0.026306476347764576,0.974367816091954,1.0
cpb-aacip-lid-silver-027,0.04916683809915658,0.9531372549019608,1.0
cpb-aacip-lid-silver-028,0.36890735655441514,0.6679717592592596,0.8792214674567617
cpb-aacip-lid-silver-029,0.4582904492398547,0.573771641791045,0.797055708309707
cpb-aacip-lid-silver-030,0.19358081034459337,0.9216078431372549,0.8454966518615107
cpb-aacip-lid-silver-031,0.14432956691527152,0.9466969696969698,0.9119746486988253
cpb-aacip-lid-silver-032,0.03571339439466925,0.9655180722891565,1.0
cpb-aacip-lid-silver-017,0.376769770165645,0.6410148550724638,0.7952785847922972
cpb-aacip-lid-silver-018,0.2565083301538853,0.9370785087719299,0.7790833197071274
cpb-aacip-lid-silver-019,0.22242455477294842,0.9542622950819671,0.8255053541774038
cpb-aacip-lid-silver-020,0.04204531685447712,0.9596511627906977,1.0
cpb-aacip-lid-silver-021,0.06564364876385344,0.9383999999999999,1.0
cpb-aacip-lid-silver-022,0.3529743327453211,0.6856616915422886,0.7903927851946182
cpb-aacip-lid-silver-023,0.3923330336895011,0.6289173913043475,0.7554191268106318
cpb-aacip-lid-silver-038,0.06307583274273568,0.9406666666666667,1.0
cpb-aacip-lid-silver-039,0.056555628650598974,0.9464716981132076,1.0
cpb-aacip-lid-silver-040,0.37071993326771674,0.6614660606060606,0.798385216704276
cpb-aacip-lid-silver-041,0.3983585513737915,0.6260128205128205,0.6889441197356203
cpb-aacip-lid-silver-042,0.2407313141596674,0.8639393939393939,0.8091541528802918
cpb-aacip-lid-silver-043,0.154419402487254,0.9453603603603603,0.9033782817934913
cpb-aacip-lid-silver-044,0.04200236330432921,0.9596907216494844,1.0
cpb-aacip-lid-silver-036,0.21401897830295466,0.9218109452736319,0.849146822668176
cpb-aacip-lid-silver-037,0.1241377686748123,0.9599322033898304,0.917602467217553
cpb-aacip-lid-silver-001,0.15069453388425902,0.947254,0.9049885247251529
cpb-aacip-lid-silver-002,0.02965864577504197,0.971195652173913,1.0
cpb-aacip-lid-silver-003,0.04059366394080183,0.960989898989899,1.0
cpb-aacip-lid-silver-004,0.3741489187864265,0.6676354166666664,0.7615011710877498
cpb-aacip-lid-silver-005,0.4931632643423966,0.5388578231292518,0.8032345268046097
cpb-aacip-lid-silver-006,0.20801746537730037,0.8918589743589743,0.8366906860250192
cpb-aacip-lid-silver-007,0.1200472908856151,0.9739848484848486,0.9066627257595321
cpb-aacip-lid-silver-008,0.037689922877860146,0.9636790123456789,1.0
cpb-aacip-lid-silver-009,0.06208030697546934,0.9415483870967742,1.0
cpb-aacip-lid-silver-033,0.053352962079293305,0.9493493975903616,1.0
cpb-aacip-lid-silver-034,0.33501298201750135,0.7053427230046951,0.7812289643234926
cpb-aacip-lid-silver-035,0.3991496181035704,0.6115094339622645,0.7544489964718197
cpb-aacip-lid-silver-046,0.34995603057566094,0.6843974358974361,0.8246228776297098
cpb-aacip-lid-silver-047,0.33565993330394933,0.679665873015873,0.7121832561311301
cpb-aacip-lid-silver-048,0.22674138559639612,0.8907437158469946,0.833992282727836
cpb-aacip-lid-silver-049,0.16198095484874,0.9573333333333334,0.8825872902766082
cpb-aacip-lid-silver-050,0.05755064456721916,0.9456326530612245,0.9999424493554329
cpb-aacip-lid-silver-051,0.04759441282979828,0.9545679012345679,1.0
cpb-aacip-lid-silver-052,0.3663060278207107,0.6531707317073173,0.8239738966168642
cpb-aacip-lid-silver-053,0.3600663916656628,0.6456733333333335,0.7967602071540407
Average,0.2069498746692075,0.8425622109203565,0.8821614621106589

### Per Class Metrics
,Error-Rate,Purity,Coverage
en,0.3685608353966988,0.9248756379264033,0.6872631048280456
ceb,0.3386209760973015,0.7529492842535788,0.9843571294090778
es,0.20458201808765128,0.8410382677165352,0.980794569033797

```

## Confusion Matrix
|     | en           | ko           | mn           | vi           | tl           | ka           | pl           | fa           | ar           | es           | pa           | sw           | war          | pt           | cs           | bg           | nn           | ceb          | fo           | jw           | te           | su           | hy           | bs           | so           | cy           | gl           | sd           |
|:----|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|
| en  | 09:33:53.120 | 00:20:49.380 | 00:22:24.001 | 00:09:23.440 | 01:32:41.103 | 00:02:55.380 | 00:09:41.700 | 00:09:23.599 | 00:05:18.740 | 01:17:26.140 | 00:00:24.240 | 00:00:22.320 | 00:04:26.160 | 00:00:20.320 | 00:01:04.440 | 00:00:20.000 | 00:00:23.880 | 00:00:33.799 | 00:00:01.640 | 00:00:58.560 | 00:00:44.500 | 00:00:02.880 | 00:00:42.460 | 00:00:19.000 | 00:00:21.000 | 00:00:00.000 | 00:00:00.000 | 00:00:00.000 |
| ceb | 00:08:46.600 | 00:00:09.760 | 00:00:45.600 | 00:00:55.700 | 06:53:12.277 | 00:00:00.000 | 00:00:30.460 | 00:00:00.000 | 00:00:10.880 | 00:00:00.000 | 00:00:00.000 | 00:00:00.000 | 02:12:27.900 | 00:00:00.000 | 00:00:10.560 | 00:00:00.000 | 00:00:00.000 | 00:03:29.341 | 00:00:00.000 | 00:00:00.000 | 00:00:00.000 | 00:00:00.000 | 00:00:00.000 | 00:00:11.000 | 00:00:09.000 | 00:00:04.820 | 00:00:00.000 | 00:00:00.000 |
| es  | 00:08:44.261 | 00:00:07.320 | 00:00:09.940 | 00:00:28.720 | 00:00:00.000 | 00:00:00.000 | 00:00:08.060 | 00:00:00.000 | 00:00:15.380 | 08:54:03.558 | 00:00:05.760 | 00:00:02.680 | 00:00:00.000 | 00:00:09.680 | 00:00:00.000 | 00:00:00.000 | 00:00:06.780 | 00:00:00.000 | 00:00:00.000 | 00:00:00.000 | 00:00:05.500 | 00:00:00.000 | 00:00:00.000 | 00:00:00.000 | 00:00:00.000 | 00:00:00.000 | 00:00:03.300 | 00:00:00.080 |