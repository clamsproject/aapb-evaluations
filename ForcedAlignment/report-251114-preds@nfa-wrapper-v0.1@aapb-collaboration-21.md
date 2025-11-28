# Evaluation Report for `ForcedAlignment` task as of 2025-11-14 09:15:46.385856

## Evaluation method
Evaluating Forced Alignment results using Diarization Error Rate (DER).

DER = (False Alarm + Missed Detection + Confusion) / Total Reference Duration

Each text segment from gold annotations is treated as a unique "speaker"
labeled by its character start index (alignment-start). The evaluation uses
character-index based alignment to match predicted tokens to gold segments,
then compares temporal boundaries.

DER captures all boundary misalignment errors:
- Confusion: Time where hypothesis has wrong segment label
- Missed Detection: Reference time not covered by hypothesis
- False Alarm: Hypothesis time extending beyond reference

OUTPUT METRICS:
-  `DER`: Diarization Error Rate as described above
-  `evaluation_ratio`: Fraction of gold segments successfully evaluated, calculated as (total_segments - skipped_segments) / total_segments.  A value of 1.0 means all segments were evaluated; lower values indicate some segments were skipped due to character offset mismatches.

CAVEAT: Due to tokenization mismatches between the original NewsHour
transcripts and the gold annotations (see
https://github.com/clamsproject/aapb-annotations/issues/5), some segments
from the FA app may not properly align to gold annotations based on
character indices. These segments will be skipped with a warning, which
may result in incomplete evaluation coverage for affected files.

We use `pyannote.metrics` library for the implementation. More details at:
https://pyannote.github.io/pyannote-metrics/reference.html#diarization

## Data specs
- Groundtruth data location: https://github.com/clamsproject/aapb-annotations/tree/a9ca6951ce4482a3c5f6bc4d3da2c5adf00b823b/newshour-transcript-sync/golds'
- System prediction (MMIF) location: /llc_data/clams/mmif-storage/nfa-wrapper/v0.1/06c73ba6897773572e65d6235cc09e4f/'

## Pipeline specs

## Raw Results
```
Individual file results (total: 19 files):
                    GUID      DER  evaluation_ratio
cpb-aacip-507-154dn40c26 0.107832          0.997783
cpb-aacip-507-1v5bc3tf81 0.163319          1.000000
cpb-aacip-507-4746q1t25k 0.188727          1.000000
cpb-aacip-507-4t6f18t178 0.078370          1.000000
cpb-aacip-507-6h4cn6zk04 0.099348          0.997765
cpb-aacip-507-6w96689725 0.107617          1.000000
cpb-aacip-507-7659c6sk7z 0.101461          0.974684
cpb-aacip-507-9882j68s35 0.128373          0.992172
cpb-aacip-507-cf9j38m509 0.058876          0.995455
cpb-aacip-507-n29p26qt59 0.148595          1.000000
cpb-aacip-507-nk3610wp6s 0.096706          0.991257
cpb-aacip-507-pc2t43js98 0.105202          0.991416
cpb-aacip-507-pr7mp4wf25 0.159541          0.992727
cpb-aacip-507-r785h7cp0z 0.080771          0.997725
cpb-aacip-507-v11vd6pz5w 0.072561          0.997653
cpb-aacip-507-v40js9j432 0.092635          0.995842
cpb-aacip-507-vm42r3pt6h 0.101276          1.000000
cpb-aacip-507-zk55d8pd1h 0.094935          1.000000
cpb-aacip-507-zw18k75z4h 0.103995          1.000000


Average DER: 0.1100
Average evaluation ratio: 0.9960



```
