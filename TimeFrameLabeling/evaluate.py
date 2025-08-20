from pathlib import Path
from typing import Any, Union, Optional, Tuple

import pandas as pd
from mmif import Mmif, AnnotationTypes
from mmif.utils import timeunit_helper as tuh
from pyannote.core import Segment, Annotation
from pyannote.metrics.detection import DetectionErrorRate, DetectionPrecisionRecallFMeasure
from pyannote.metrics.identification import (IdentificationErrorRate, IdentificationPrecision,
                                             IdentificationRecall)

import goldretriever

"""
NOTICE: Currently only evaluates chyron and slate detection
"""

from common import ClamsAAPBEvaluationTask

# Constants
GOLD_CHYRON_URL = "https://github.com/clamsproject/aapb-annotations/tree/106-chyronunderstanding/newshour-chyron/golds"
GOLD_SLATES_URL = "https://github.com/clamsproject/aapb-annotations/tree/106-chyronunderstanding/january-slates/golds"

class TimeFrameLabelingEvaluator(ClamsAAPBEvaluationTask):
    """
    Evaluating tasks that label time frames which are currently
    Chyron and Slate Detection (CSD) and Language Identification (LID).

    CSD uses Detection Error Rate and Detection Precision, Recall, and F1.
    LID uses Identification Error Rate and Identification Precision, Recall, and F1.

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

    def _read_gold(self, gold_file: Union[str, Path], **kwargs) -> Any:
        """
        :param gold_file: A CSV file containing the gold annotations
        :return: Annotation object from pyannote library holding gold annotations
        """
        gold_annotation = Annotation()
        col_name = 'scene-label'
        if self.task == 'slate':
            col_name = 'scene-type'
        for _, row in pd.read_csv(gold_file).iterrows():
            if row['start'] != 'NO':
                label = row[col_name]
                #Currently sets 'ceb' to 'lr' because cebuano cannot be predicted by the whisper model
                if self.task == 'lid' and (label != 'en' or label != 'es'):
                    label = 'lr'
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
                #If a label is not predicted as en or es, it is relabeled as 'lr'
                if self.task == 'lid' and (label != 'en' or label != 'es'):
                    label = 'lr'
                pred_annotation[Segment(*(tuh.convert(t, in_unit, 'sec', fps) for t in (s, e)))] = label

        return pred_annotation, gold
    
    def _compare_pair(self, guid: str, gold: Any, pred: Any) -> Any:
        """
        If evaluating CSD, detection error rate, precision, recall, and f1 are returned;
        however, pyannote's implementation of precision and recall is incorrect where if
        one timeline is empty but the other is not, one of the two will be 1.0 when
        both should be 0.0.

        If evaluating LID, identification error rate, precision, recall, and f1 are returned;
        however, because pyannote does not have a method that calculates f1, it is calculated here.
        """
        if self.task == 'lid':
            err_rate = IdentificationErrorRate()
            p = IdentificationPrecision()(gold, pred)
            r = IdentificationRecall()(gold, pred)

            if p+r == 0:
                f1 = 0.0
            else:
                f1 = (2*p*r)/(p+r)
        else:
            err_rate = DetectionErrorRate()
            prf1 = DetectionPrecisionRecallFMeasure()
            results_dict = prf1.compute_components(gold, pred)
            p, r, f1 = prf1.compute_metrics(results_dict)

            #Correcting precision and recall to 0.0 when one timeline is empty but the other is not
            if bool(gold.get_timeline().duration()) != bool(pred.get_timeline().duration()):
                p, r = (0.0, 0.0)

        return err_rate(gold, pred), p, r, f1

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

    def _finalize_results(self):
        cols = 'GUID Error-Rate Precision Recall F1'.split()

        df = pd.DataFrame(
            [[guid] + list(results) for guid, results in self._calculations.items() if results],
            columns=cols
        )
        # then add the average row
        df.loc[len(df)] = ['Average'] + [df[col].mean() for col in df.columns[1:]]
        self._results = df.to_csv(index=False, sep=',', header=True)


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
