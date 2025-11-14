import re
from pathlib import Path
from typing import Any, Union

import pandas as pd
from clams_utils.aapb import guidhandler
from mmif.serialize import Mmif
from mmif.utils import timeunit_helper as tuh
from mmif.vocabulary import AnnotationTypes
from pyannote.core import Segment, Annotation
from pyannote.metrics.diarization import DiarizationErrorRate

from common import ClamsAAPBEvaluationTask


class ForcedAlignmentEvaluator(ClamsAAPBEvaluationTask):
    """
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
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.regex_timestamp = re.compile(r"(\d{2}):(\d{2}):(\d{2})[.,](\d{1,3})")

    @property
    def results(self) -> Union[dict, str]:
        return self._results

    def _read_gold(self, gold_file: Union[str, Path], **kwargs) -> Annotation:
        """Read gold file and return Annotation with alignment-start-end as labels."""
        gold = Annotation()
        df = pd.read_csv(gold_file, sep="\t")

        for _, row in df.iterrows():
            segment = Segment(
                tuh.convert(row["start"], 'iso', 'ms', 0),
                tuh.convert(row["end"], 'iso', 'ms', 0)
            )
            # Use alignment-start and alignment-end as label
            gold[segment] = f"{row['alignment-start']}-{row['alignment-end']}"

        return gold

    def _read_pred(self, pred_file: Union[str, Path], gold: Annotation, **kwargs):
        """Read prediction using character-index alignment."""
        pred = Annotation()
        guid = guidhandler.get_aapb_guid_from(str(pred_file))
        mmif = Mmif(open(pred_file, 'r').read())
        # pick the last view with required annotations
        fa_view = mmif.get_views_contain(AnnotationTypes.Token, AnnotationTypes.TimeFrame, AnnotationTypes.Alignment)[-1]
        pred_charstart_to_timestart = {}
        pred_charend_to_timeend = {}
        for token in fa_view.get_annotations(AnnotationTypes.Token):
            token_start = int(token.get("start"))
            token_end = int(token.get("end"))
            found_timeframe = False
            for aligned in token.get_all_aligned():
                if aligned.at_type == AnnotationTypes.TimeFrame:
                    time_start = aligned.get("start")
                    time_end = aligned.get("end")
                    pred_charstart_to_timestart[token_start] = time_start
                    pred_charend_to_timeend[token_end] = time_end
                    found_timeframe = True
                    break
            # if TF is not found, there must be a problem
            if not found_timeframe:
                raise ValueError(f"{guid} :: No TimeFrame aligned with Token [{token_start}, {token_end}]")

        # Build hypothesis annotation from gold labels and predicted times
        for segment, _, label in gold.itertracks(yield_label=True):
            # Split label to get alignment-start and alignment-end
            char_start, char_end = map(int, label.split('-'))

            # Lookup predicted time boundaries
            try:
                time_start = pred_charstart_to_timestart[char_start]
                time_end = pred_charend_to_timeend[char_end]

                # Create hypothesis segment with matching label
                pred[Segment(time_start, time_end)] = label
            except KeyError as e:
                self.logger.warning(
                    f"{guid} :: Character position {e} not found in prediction. "
                    f"Skipping gold segment [{char_start}, {char_end}]"
                )
        return pred, None  # return None gold since nothing should have changed in gold

    def _compare_pair(self, guid: str, reference: Annotation, hypothesis: Annotation) -> float:
        """Compute DER for a single file."""
        if len(hypothesis) == 0:
            self.logger.warning(f'{guid} :: no hypothesis segments found')
            return 1.0  # Maximum error

        if len(reference) != len(hypothesis):
            self.logger.warning(
                f'{guid} :: reference ({len(reference)}) and hypothesis ({len(hypothesis)}) have different number of segments')

        try:
            # Create UEM (Un-Evaluated Map) to specify evaluation boundaries.
            # UEM defines which temporal regions should be included in metric
            # calculation. We use the union of reference and hypothesis extents
            # to ensure all annotated segments are evaluated, avoiding pyannote's
            # automatic approximation warning.
            uem = reference.get_timeline().union(hypothesis.get_timeline())

            der = DiarizationErrorRate()
            der_score = der(reference, hypothesis, uem=uem)
            return der_score
        except Exception as e:
            self.logger.error(f'{guid} :: Error computing DER: {e}')
            return 1.0
    
    def write_side_by_side_view(self):
        pass
            
    def _compare_all(self, golds, preds) -> Any:
        raise NotImplementedError("Comparing all golds and preds is not implemented. ")

    def _finalize_results(self):
        """Aggregate DER results and calculate average."""
        cols = ['GUID', 'DER']
        data = []

        for guid, result in self._calculations.items():
            if result is False:  # File exists but no data read
                continue
            data.append([guid, result])

        if not data:
            self._results = "No valid results to report.\n"
            return

        df = pd.DataFrame(data, columns=cols)
        res_str = (
            f'Individual file results:\n{df.to_string(index=False)}\n\n\n'
            f'Average DER: {df["DER"].mean():.4f}\n\n\n'
        )
        self._results = res_str


if __name__ == "__main__":
    parser = ForcedAlignmentEvaluator.prep_argparser()
    args = parser.parse_args()

    evaluator = ForcedAlignmentEvaluator(batchname=args.batchname, gold_loc=args.golds, pred_loc=args.preds)
    evaluator.calculate_metrics(by_guid=True)
    report = evaluator.write_report()
    args.export.write(report.getvalue())
