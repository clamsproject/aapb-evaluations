from collections import defaultdict
from pathlib import Path
from typing import Any, Union, Optional, Tuple
import json

import pandas as pd
from mmif import Mmif, AnnotationTypes
from mmif.utils import timeunit_helper as tuh
from pyannote.core import Segment, Annotation
from pyannote.metrics.detection import DetectionErrorRate, DetectionPrecisionRecallFMeasure
from pyannote.metrics.diarization import (DiarizationErrorRate, DiarizationPurity,
                                          DiarizationCoverage)
from pyannote.metrics.errors.identification import IdentificationErrorAnalysis

import goldretriever

from common import ClamsAAPBEvaluationTask

# Constants
GOLD_CHYRON_URL = "https://github.com/clamsproject/aapb-annotations/tree/106-chyronunderstanding/newshour-chyron/golds"
GOLD_SLATES_URL = "https://github.com/clamsproject/aapb-annotations/tree/106-chyronunderstanding/january-slates/golds"


class TimeFrameLabelingEvaluator(ClamsAAPBEvaluationTask):
    """
    Evaluating tasks that label time frames which are currently
    Chyron and Slate Detection (CSD) and Language Identification (LID).

    CSD uses Detection Error Rate and Detection Precision, Recall, and F1.
    LID uses Diarization Error Rate and Diarization Purity and Coverage.
        - When evaluating LID, a confusion matrix is also provided after
        the raw results

    Note that for error rate, lower is better and can be greater than 100%.
    For all metrics, we use the `pyannote` library.
    More details can be found at https://pyannote.github.io/pyannote-metrics/reference.html
    """

    def __init__(self, batchname: str, **kwargs):
        super().__init__(batchname, **kwargs)
        self.task = kwargs.get('task')

        task_dict = {'chyron': 'Chyron Detection',
                     'slate': 'Slate Detection',
                     'lid': 'Language Identification',
                     }
        self._taskname = task_dict[self.task]
        self._confusion_durations = defaultdict(lambda: defaultdict(float))
        self._lr_gold = None
        self._lr_preds = {}
        self._lr_idx = 0

    def _read_gold(self, gold_file: Union[str, Path], **kwargs) -> Any:
        """
        :param gold_file: A CSV file containing the gold annotations
        :return: Annotation object from pyannote library holding gold annotations
        """
        gold_annotation = Annotation()
        col_name = 'scene-label'
        for _, row in pd.read_csv(gold_file).iterrows():
            if row['start'] != 'NO':
                label = row[col_name]
                # Currently sets 'ceb' to 'lr' because cebuano cannot be predicted by the whisper model
                if self.task == 'lid' and label != 'en' and label != 'es':
                    self._lr_gold = label
                    label = 'lr0'
                gold_annotation[Segment(tuh.convert(row['start'], 'iso', 'seconds', 1),
                                        tuh.convert(row['end'], 'iso', 'seconds', 1))] = label

        return gold_annotation

    def _read_pred(self, pred_file: Union[str, Path], gold: Optional[Any], **kwargs) -> Tuple[Any, Optional[Any]]:
        pred_annotation = Annotation()
        f = open(pred_file, 'r')
        mmif_str = f.read()
        f.close()
        data = Mmif(mmif_str)
        fps = 29.97
        lr_idx = 0

        if self.task == 'lid':
            property_name = 'label'
        else:
            property_name = 'frameType'

        tf_view = data.get_view_contains(AnnotationTypes.TimeFrame)
        for ann in reversed(list(tf_view.get_annotations(AnnotationTypes.TimeFrame))):
            if ann.get_property('fps'):
                fps = ann.get_property('fps')
            else:
                in_unit = ann.get_property('timeUnit')
                s = data.get_start(ann)
                e = data.get_end(ann)
                label = ann.get_property(property_name)
                if self.task == 'lid':
                    label = label[2:4]
                # If a label is not predicted as en or es, it is relabeled as 'lr'
                if self.task == 'lid' and label != 'en' and label != 'es':
                    if label not in self._lr_preds:
                        lr_label = f'lr{self._lr_idx}'
                        self._lr_preds[label] = lr_label
                        self._lr_idx += 1
                        label = lr_label
                    else:                          
                        label = self._lr_preds[label]
                pred_annotation[Segment(*(tuh.convert(t, in_unit, 'sec', fps) for t in (s, e)))] = label

        return pred_annotation, gold

    def _compare_pair(self, guid: str, gold: Any, pred: Any) -> Any:
        """
        If evaluating CSD, detection error rate, precision, recall, and f1 are returned;
        however, pyannote's implementation of precision and recall is incorrect where if
        one timeline is empty but the other is not, one of the two will be 1.0 when
        both should be 0.0. This is corrected here. 

        If evaluating LID, diarization error rate, purity, and coverage are returned.
        """

        #Calculate the metrics
        if self.task == 'lid':
            err_rate = DiarizationErrorRate()(gold, pred)
            p = DiarizationPurity()(gold, pred)
            c = DiarizationCoverage()(gold, pred)
            metrics = (err_rate, p, c)

        else:
            err_rate = DetectionErrorRate()(gold, pred)
            prf1 = DetectionPrecisionRecallFMeasure()
            results_dict = prf1.compute_components(gold, pred)
            p, r, f1 = prf1.compute_metrics(results_dict)

            # Correcting precision and recall to 0.0 when one timeline is empty but the other is not
            if bool(gold.get_timeline().duration()) != bool(pred.get_timeline().duration()):
                p, r = (0.0, 0.0)

            metrics = (err_rate, p, r, f1)

        #Aggregrating results for confusion matrix
        err = IdentificationErrorAnalysis()
        for segment, track, label in err.difference(gold, pred).itertracks(yield_label=True):
            if track == 'confusion0' or track == 'correct0':
                self._confusion_durations[label[1]][label[2]] += segment.duration

        return metrics

    def _compare_all(self, golds, preds) -> Any:
        """
        Compare all golds and preds is NOT implemented, hence do not
        call ``calculate_metrics`` with ``by_guid=False``.
        """
        raise NotImplementedError("Comparing all golds and preds is not implemented. ")

    def write_side_by_side_view(self):
        """
        Side by side view is NOT yet implemented, hence do not
        instantiate with ``sbs=True``
        """
        raise NotImplementedError("Writing side by side view not yet implemented. ")

    def _make_confusion_matrix(self) -> str:
        """
        Creates a confusion matrix where the rows are the reference labels
        and the columns are the predicted labels, and the entries are
        the durations of the confusion in seconds

        :return: The confusion matrix string to be added to self._results
        """
        df = pd.read_json(json.dumps(self._confusion_durations), orient='index')
        df = df.fillna(0.0)
        df = df.map(lambda x: tuh.convert(x, 'sec', 'iso', 1))
        #Rename lr0 with gold lr label
        idx_list = list(df.index.array)
        idx_list[idx_list.index('lr0')] = self._lr_gold
        df.index = idx_list
        
        #Rename col names with original labels
        df.rename(columns={val:key for key,val in self._lr_preds.items()}, inplace=True)
        return df.to_csv(index=True, sep=',', header=True)


    def _finalize_results(self):
        if self.task != 'lid':
            cols = 'GUID Error-Rate Precision Recall F1'.split()
        else:
            cols = 'GUID Error-Rate Purity Coverage'.split()

        df = pd.DataFrame(
            [[guid] + list(results) for guid, results in self._calculations.items() if results],
            columns=cols
        )
        # then add the average row
        df.loc[len(df)] = ['Average'] + [df[col].mean() for col in df.columns[1:]]
        self._results = df.to_csv(index=False, sep=',', header=True)
        # add confusion matrix after Raw Results if evaluating LID
        if self.task == 'lid':
            self._results += '\n### Confusion Matrix\n'
            self._make_confusion_matrix()
            self.results += self._make_confusion_matrix()


if __name__ == "__main__":
    parser = TimeFrameLabelingEvaluator.prep_argparser()
    parser.add_argument('-t', '--task', choices=['chyron', 'slate', 'lid'], default='chyron')

    args = parser.parse_args()
    ref_dir = None
    if args.golds:
        ref_dir = args.golds
    else:
        if args.task == 'slate':
            ref_dir = goldretriever.download_golds(GOLD_SLATES_URL)
        elif args.task == 'chyron':
            ref_dir = goldretriever.download_golds(GOLD_CHYRON_URL)

    evaluator = TimeFrameLabelingEvaluator(batchname=args.batchname, gold_loc=ref_dir,
                                           pred_loc=args.preds, task=args.task)
    evaluator.calculate_metrics(by_guid=True)
    report = evaluator.write_report()
    args.export.write(report.getvalue())
