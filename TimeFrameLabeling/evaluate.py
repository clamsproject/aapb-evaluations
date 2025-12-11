import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Union, Optional, Tuple

import pandas as pd
from mmif import Mmif, AnnotationTypes
from mmif.utils import timeunit_helper as tuh
from pyannote.core import Segment, Annotation
from pyannote.metrics.diarization import (DiarizationErrorRate, DiarizationPurity,
                                          DiarizationCoverage)
from pyannote.metrics.errors.identification import IdentificationErrorAnalysis

from common import ClamsAAPBEvaluationTask, EVAL_OTHER_PREFIX
from common.helpers import parse_label_map


class TimeFrameLabelingEvaluator(ClamsAAPBEvaluationTask):
    """
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
    """

    def __init__(self, batchname: str, **kwargs):
        self.label_map = kwargs.get('label_map', {})
        self.default_label = kwargs.get('default_label', '-')
        # Derive target labels (distinct output labels from the mapping)
        self.target_labels = set(v for v in self.label_map.values())
        self.target_labels.discard(self.default_label)
        self.target_labels = list(self.target_labels) if self.target_labels else None
        super().__init__(batchname, cf=bool(self.target_labels), **kwargs)

        self._confusion_durations = defaultdict(lambda: defaultdict(float))
        self._per_class_metrics = {}

        # variables for handling "OOV" labels
        self._other_gold_label = None
        self._other_pred_labels = {}
        self._other_idx = 0

    def _read_gold(self, gold_file: Union[str, Path], **kwargs) -> Annotation:
        """
        Read gold CSV file and return pyannote Annotation object.

        :param gold_file: CSV file with columns: start, end, scene-label
        :return: Annotation object from pyannote library holding gold annotations
        :rtype: Annotation
        """
        gold_annotation = Annotation()
        col_name = 'scene-label'
        for _, row in pd.read_csv(gold_file).iterrows():
            if row['start'] != 'NO':
                label = row[col_name]
                if self.label_map and label not in self.target_labels:
                    # Track original "other" label for reporting (this assumes there's only one "other" label in gold)
                    if self._other_gold_label is None:
                        self._other_gold_label = label
                    label = f'{EVAL_OTHER_PREFIX}0'
                elif self.label_map:
                    # for "target" labels, apply label mapping
                    label = self.label_map.get(label, self.default_label)
                    # note that only the first non-target label is tracked as "other0"
                    # and the rest are mapped to default_label (`-` by default)
                    # this design choice is made to handle silver-based LID evaluation
                    # and may need to be revisited for other tasks
                gold_annotation[Segment(tuh.convert(row['start'], 'iso', 'seconds', 1),
                                        tuh.convert(row['end'], 'iso', 'seconds', 1))] = label
                # Set up per-class metrics dict
                if label not in self._per_class_metrics:
                    self._per_class_metrics[label] = {
                        'Error-Rate': DiarizationErrorRate(),
                        'Purity': DiarizationPurity(),
                        'Coverage': DiarizationCoverage()
                    }

        return gold_annotation

    def _read_pred(self, pred_file: Union[str, Path], gold: Optional[Any],
                   **kwargs) -> Tuple[Any, Optional[Any]]:
        """
        Read prediction MMIF and return pyannote Annotation object.

        :param pred_file: Path to MMIF file containing TimeFrame annotations
        :param gold: Gold annotation object (passed through unchanged)
        :return: Tuple of (predicted Annotation, gold Annotation)
        :rtype: Tuple[Annotation, Optional[Any]]
        """
        pred_annotation = Annotation()
        f = open(pred_file, 'r')
        mmif_str = f.read()
        f.close()
        data = Mmif(mmif_str)
        fps = 29.97

        tf_view = data.get_view_contains(AnnotationTypes.TimeFrame)
        for ann in reversed(list(tf_view.get_annotations(AnnotationTypes.TimeFrame))):
            if ann.get_property('fps'):
                fps = ann.get_property('fps')
            else:
                in_unit = ann.get_property('timeUnit')
                s = data.get_start(ann)
                e = data.get_end(ann)
                label = ann.get_property('label')
                if self.label_map:
                    mapped_label = self.label_map.get(label, self.default_label)
                    if mapped_label == self.default_label:
                        # for pred, we need
                        # 1. "collapse" unmapped labels into distinct other labels to compute DER
                        # 2. distinguish them in the confusion matrix
                        # so we remap the labels into {common_prefix}{distinct_idx}
                        if label not in self._other_pred_labels:
                            other_label = f'{EVAL_OTHER_PREFIX}{self._other_idx}'
                            self._other_pred_labels[label] = other_label
                            self._other_idx += 1
                            label = other_label
                        else:
                            label = self._other_pred_labels[label]
                    else:
                        label = mapped_label
                pred_annotation[Segment(*(tuh.convert(t, in_unit, 'sec', fps) for t in (s, e)))] = label

        return pred_annotation, gold

    def _compare_pair(self, guid: str, gold: Any, pred: Any) -> Any:
        """
        Calculate diarization metrics for a single document.

        When evaluating LID, all low-resource languages are collapsed under
        a single label. Computes overall DER, purity, and coverage, plus
        per-class metrics for each gold label and confusion matrix data.

        :param guid: Document identifier
        :param gold: Gold Annotation object from pyannote
        :param pred: Predicted Annotation object from pyannote
        :return: Generator yielding (error_rate, purity, coverage) values
        :rtype: Generator[float, None, None]
        """

        metrics = [DiarizationErrorRate(), DiarizationPurity(), DiarizationCoverage()]
        metric_names = ['Error-Rate', 'Purity', 'Coverage']

        # Calculate per-class metrics if task is not binary like chyron/slate detection
        if len(self._per_class_metrics) > 1:
            for label in set(gold.labels()):
                filtered_gold = gold.subset([label])
                if self.target_labels and label == f'{EVAL_OTHER_PREFIX}0':
                    filtered_pred = self._collapse_other(pred).subset([label])
                else:
                    filtered_pred = pred.subset([label])
                for name in metric_names:
                    self._per_class_metrics[label][name](filtered_gold, filtered_pred)

        # Aggregating results for confusion matrix
        if self.target_labels:
            err = IdentificationErrorAnalysis()
            for segment, track, label in err.difference(gold, pred).itertracks(yield_label=True):
                if track == 'confusion0' or track == 'correct0':
                    self._confusion_durations[label[1]][label[2]] += segment.duration

        # Calculate and return overall metrics
        if self.target_labels:
            pred = self._collapse_other(pred)
        return (metric(gold, pred) for metric in metrics)

    def _compare_all(self, golds, preds) -> Any:
        """
        Compare all golds and preds is NOT implemented.

        Do not call ``calculate_metrics`` with ``by_guid=False``.

        :param golds: Not used
        :param preds: Not used
        :raises NotImplementedError: Always raises
        """
        raise NotImplementedError("Comparing all golds and preds is not implemented. ")

    def write_side_by_side_view(self):
        """
        Side by side view is NOT yet implemented.

        Do not instantiate with ``sbs=True``.

        :raises NotImplementedError: Always raises
        """
        raise NotImplementedError("Writing side by side view not yet implemented. ")

    def write_confusion_matrix(self) -> str:
        """
        Create confusion matrix with duration-based entries.

        Rows are reference (gold) labels, columns are predicted labels,
        and entries are the durations of confusion in ISO format.

        :return: The confusion matrix string to be added to self._results
        :rtype: str
        """
        df = pd.read_json(json.dumps(self._confusion_durations), orient='index')
        df = df.fillna(0.0)
        df = df.map(lambda x: tuh.convert(x, 'sec', 'iso', 1))
        # Rename other0 with gold "other" label
        if self.target_labels and self._other_gold_label:
            if f'{EVAL_OTHER_PREFIX}0' in df.index:
                idx_list = list(df.index.array)
                idx_list[idx_list.index(f'{EVAL_OTHER_PREFIX}0')] = self._other_gold_label
                df.index = idx_list

            # Rename col names with original labels
            df.rename(columns={val: key for key, val in self._other_pred_labels.items()}, inplace=True)
        return df.to_markdown(index=True)

    def _collapse_other(self, annotation: Annotation) -> Annotation:
        """
        Collapse all "other" labels into a single label for evaluation.

        Collapses all labels starting with EVAL_OTHER_PREFIX into
        f'{EVAL_OTHER_PREFIX}0'. Used when evaluating multi-class tasks
        where the primary goal is to distinguish a set of positive labels
        from all other labels.

        :param annotation: The Annotation object to collapse
        :return: The collapsed Annotation object
        :rtype: Annotation
        """
        collapsed_annotation = Annotation()
        for segment, _, label in annotation.itertracks(yield_label=True):
            if label.startswith(EVAL_OTHER_PREFIX):
                collapsed_annotation[segment] = f'{EVAL_OTHER_PREFIX}0'
            else:
                collapsed_annotation[segment] = label
        return collapsed_annotation

    def _finalize_results(self):
        """
        Generate CSV results with per-document and average metrics.

        Creates a DataFrame with Error-Rate, Purity, and Coverage for each
        GUID plus an average row. If multi-class evaluation, also includes
        per-class metrics section.

        :return: None (sets self._results)
        """
        cols = 'GUID Error-Rate Purity Coverage'.split()

        df = pd.DataFrame(
            [[guid] + list(results) for guid, results in self._calculations.items() if results],
            columns=cols
        )
        # then add the average row
        df.loc[len(df)] = ['Average'] + [df[col].mean() for col in df.columns[1:]]
        self._results = df.to_csv(index=False, sep=',', header=True)

        # add per class metrics if not binary classification
        if len(self._per_class_metrics) > 1:
            self._results += '\n### Per Class Metrics\n'
            per_class_df = pd.DataFrame(self._per_class_metrics).T
            if self.target_labels and self._other_gold_label:
                per_class_df = per_class_df.rename(index={f'{EVAL_OTHER_PREFIX}0': self._other_gold_label})
                per_class_df = per_class_df.map(lambda x: abs(x))
            self._results += per_class_df.to_csv(index=True, sep=',', header=True)


if __name__ == "__main__":
    parser = TimeFrameLabelingEvaluator.prep_argparser()
    parser.add_argument('--label-map', nargs='+', default=None,
                        help='Label mappings. Supports: '
                             '(1) Identity: "eng spa fre" → keep distinct, '
                             '(2) Binning: "eng spa kor:asian jpn:asian", '
                             '(3) Renaming: "english:eng spanish:spa". '
                             'Comma-separated also works. '
                             'Unmapped labels use --default-label value.')
    parser.add_argument('--default-label', type=str, default='-',
                        help='Label to use for unmapped entries (default: "-")')

    args = parser.parse_args()

    # Parse label map
    label_map = None
    if args.label_map:
        label_map = parse_label_map(args.label_map)

    evaluator = TimeFrameLabelingEvaluator(
        batchname=args.batchname,
        gold_loc=args.golds,
        pred_loc=args.preds,
        label_map=label_map,
        default_label=args.default_label
    )
    evaluator.calculate_metrics(by_guid=True)
    report = evaluator.write_report()
    args.export.write(report.getvalue())
