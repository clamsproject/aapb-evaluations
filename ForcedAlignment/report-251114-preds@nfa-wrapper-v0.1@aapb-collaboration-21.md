# Evaluation Report for `ForcedAlignment` task as of 2025-11-14 07:40:08.781012

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

We use `pyannote.metrics` library for the implementation. More details at:
https://pyannote.github.io/pyannote-metrics/reference.html#diarization

## Data specs
- Groundtruth data location: ../aapb-annotations/newshour-transcript-sync/golds'
- System prediction (MMIF) location: /llc_data/clams/mmif-storage/nfa-wrapper/v0.1/06c73ba6897773572e65d6235cc09e4f/'

## Pipeline specs

## Raw Results
```
Individual file results:
                    GUID      DER
cpb-aacip-507-6h4cn6zk04 0.099348
cpb-aacip-507-cf9j38m509 0.058876
cpb-aacip-507-154dn40c26 0.107832
cpb-aacip-507-zk55d8pd1h 0.094935
cpb-aacip-507-6w96689725 0.107617
cpb-aacip-507-nk3610wp6s 0.096706
cpb-aacip-507-4746q1t25k 0.188727
cpb-aacip-507-1v5bc3tf81 0.163319
cpb-aacip-507-vm42r3pt6h 0.101276
cpb-aacip-507-pr7mp4wf25 0.159541
cpb-aacip-507-v40js9j432 0.092635
cpb-aacip-507-pc2t43js98 0.105202
cpb-aacip-507-4t6f18t178 0.078370
cpb-aacip-507-zw18k75z4h 0.103995
cpb-aacip-507-r785h7cp0z 0.080771
cpb-aacip-507-9882j68s35 0.128373
cpb-aacip-507-v11vd6pz5w 0.072561
cpb-aacip-507-n29p26qt59 0.148595
cpb-aacip-507-7659c6sk7z 0.101461


Average DER: 0.1100



```
