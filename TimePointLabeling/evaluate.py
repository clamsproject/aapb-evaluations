from pathlib import Path
from typing import Any, Union, Optional, Tuple, List

import pandas as pd
from mmif import Mmif, AnnotationTypes
from mmif.utils import timeunit_helper as tuh

from common import ClamsAAPBEvaluationTask
from common.helpers import parse_label_map, match_nearest_points
from common.metrics import (precision_recall_fscore, MACRO_AVG_PRECISION,
                             MACRO_AVG_RECALL, MACRO_AVG_F1)


class TimePointLabelingEvaluator(ClamsAAPBEvaluationTask):
    """
    Evaluates TimePoint classification predictions against gold standard
    annotations.

    ## Input Format
    - Predictions: MMIF files containing TimePoint annotations
    - Gold annotations: CSV files with `at` column (timestamp) and any column
      ending with `-label` (e.g., `scene-label`, `type-label`)

    ## Timestamp Matching
    Uses fuzzy timestamp matching with ±5ms tolerance to align predictions
    with gold timestamps. Each prediction is matched to its nearest gold
    timestamp. Only matched pairs are included in evaluation.

    ## Label Mapping
    When --label-map is provided, both predicted and gold labels are remapped
    before evaluation. Unmapped labels are replaced with --default-label
    (default: "-"). When no label map is provided, raw labels are used
    directly.

    ## Metrics
    Calculates per-label Precision, Recall, and F1 score using
    sklearn.metrics.precision_recall_fscore_support. Metrics are computed
    per-document and macro-averaged across labels. An overall average across
    all documents is also reported.
    """

    def __init__(self, batchname: str, **kwargs):
        self.label_map = kwargs.get('label_map', None)
        self.default_label = kwargs.get('default_label', '-')

        super().__init__(batchname, **kwargs)

    def _read_gold(self, gold_file: Union[str, Path], **kwargs) -> dict:
        """
        Read gold CSV file and return dict mapping timestamps to labels.

        :param gold_file: Path to CSV file with 'at' column and a label
                          column matching pattern '*-label' (e.g., 'scene-label',
                          'type-label')
        :return: Dict mapping timestamp (milliseconds) to label string
        :rtype: dict
        """
        df = pd.read_csv(gold_file)

        # Find label column (any column ending with '-label')
        label_cols = [col for col in df.columns if col.endswith('-label')]
        if not label_cols:
            raise ValueError(
                f"No label column found in {gold_file}. "
                f"Expected column ending with '-label', "
                f"got: {list(df.columns)}")
        if len(label_cols) > 1:
            self.logger.warning(
                f"Multiple label columns found: {label_cols}. "
                f"Using first: {label_cols[0]}")
        label_col = label_cols[0]

        # Convert timestamps (iso) to ms
        df['at'] = df['at'].apply(
            lambda ts: int(tuh.convert(ts, 'iso', 'milliseconds', 1)))

        # Create dictionary of 'at':'label' from dataframe
        gold_dict = df.set_index('at')[label_col].to_dict()

        return gold_dict

    def _read_pred(self, pred_file: Union[str, Path], gold: Optional[Any],
                   **kwargs) -> Tuple[List[str], List[str]]:
        """
        Read prediction MMIF and return aligned predicted labels.

        Performs fuzzy timestamp matching (±5ms) to align predictions with
        gold timestamps.

        :param pred_file: Path to MMIF file containing TimePoint annotations
        :param gold: Dict mapping timestamps to gold labels (input)
        :return: Tuple of (pred_list, gold_list) where both are lists of
                 labels aligned by timestamp matching. Only matched timestamps
                 are included; both lists have the same length.
        :rtype: Tuple[List[str], List[str]]
        """
        mmif_f = open(pred_file, "r")
        pred_mmif = Mmif(mmif_f.read())
        mmif_f.close()

        # Get TimePoint annotations
        tp_views = list(pred_mmif.get_all_views_contain(AnnotationTypes.TimePoint))
        if not tp_views:
            self.logger.warning(f"No TimePoint annotations found in {pred_file}")
            return [], []

        # First pass: collect all pred annotations with their timestamps
        pred = dict([
            (
                tuh.convert(
                    annotation.get('timePoint'),
                    annotation.get('timeUnit', 'milliseconds'),
                    'milliseconds', 1),
                annotation.get('label')
            )
            for view in tp_views
            for annotation in view.get_annotations(
                AnnotationTypes.TimePoint)
        ])

        # Match predicted timestamps to nearest gold timestamps
        matches = match_nearest_points(list(pred.keys()), list(gold.keys()), tolerance=5)

        # Build aligned predictions and gold labels
        gold_list = []
        pred_list = []
        for pred_ts, gold_ts in matches.items():
            if gold_ts is not None:
                pred_label = pred[pred_ts] if not self.label_map \
                    else self.label_map.get(pred[pred_ts], self.default_label)
                gold_label = gold[gold_ts] if not self.label_map \
                    else self.label_map.get(gold[gold_ts], self.default_label)
                gold_list.append(gold_label)
                pred_list.append(pred_label)
        if len(gold_list) != len(pred_list):
            raise ValueError("Number of gold and pred labels do not match after timestamp alignment.")

        return pred_list, gold_list

    def _compare_pair(self, guid: str, gold: Any, pred: Any) -> dict:
        """
        Calculate evaluation metrics for a single document using sklearn.

        :param guid: Document identifier
        :param gold: List of gold labels (already label-mapped and aligned
                     to pred)
        :param pred: List of predicted labels (already label-mapped and
                     aligned to gold)
        :return: Dict with per-label metrics ("{label}_P", "{label}_R",
                 "{label}_F" for each label in data) plus macro-averaged
                 metrics (MACRO_AVG_PRECISION, MACRO_AVG_RECALL, MACRO_AVG_F1
                 constants from common.metrics)
        :rtype: dict
        """
        if not pred or not gold:
            return {MACRO_AVG_PRECISION: 0, MACRO_AVG_RECALL: 0,
                    MACRO_AVG_F1: 0}

        # Both gold and pred are already aligned lists
        gold_labels = gold
        pred_labels = pred

        # Get all unique labels (sorted for consistent ordering)
        labels = sorted(set(gold_labels + pred_labels))

        # Calculate per-label metrics
        precision, recall, f1 = precision_recall_fscore(
            gold_labels, pred_labels, labels=labels, average=None,
            zero_division=0
        )

        # Calculate macro averages
        macro_p, macro_r, macro_f1 = precision_recall_fscore(
            gold_labels, pred_labels, average='macro', zero_division=0
        )

        # Build metrics dictionary
        metrics_dict = {}
        for i, label in enumerate(labels):
            metrics_dict[f"{label}_P"] = float(precision[i])
            metrics_dict[f"{label}_R"] = float(recall[i])
            metrics_dict[f"{label}_F"] = float(f1[i])

        metrics_dict[MACRO_AVG_PRECISION] = float(macro_p)
        metrics_dict[MACRO_AVG_RECALL] = float(macro_r)
        metrics_dict[MACRO_AVG_F1] = float(macro_f1)

        return metrics_dict

    def _compare_all(self, golds, preds) -> Any:
        """
        Not implemented - use per-guid evaluation instead.

        :param golds: Not used
        :param preds: Not used
        :raises NotImplementedError: Always raises
        """
        raise NotImplementedError(
            "Comparing all golds and preds is not implemented. "
            "Use by_guid=True mode.")

    def _finalize_results(self):
        """
        Generate CSV with format.

        Rows: GUIDs + Average row
        Columns: GUID + per-label metrics (P/R/F) + MAC_AVG metrics

        :return: None (sets self._results)
        """
        # Collect all possible metric columns across all GUIDs
        all_columns = set()
        for results in self._calculations.values():
            if results:
                all_columns.update(results.keys())
        all_columns = sorted(all_columns)

        # Build DataFrame with consistent columns, filling missing with 0
        rows = []
        for guid, results in self._calculations.items():
            if results:
                row = [guid] + [results.get(col, 0) for col in all_columns]
                rows.append(row)

        df = pd.DataFrame(rows, columns=['GUID'] + all_columns)

        # Add average row (mean of all per-document scores)
        df.loc[len(df)] = ['Average'] + [df[col].mean()
                                          for col in df.columns[1:]]

        self._results = df.to_csv(index=False, sep=',', header=True)

    def write_confusion_matrix(self):
        """
        Confusion matrix not yet implemented for TimePointLabeling.

        :raises NotImplementedError: Always raises
        """
        raise NotImplementedError(
            "Confusion matrix not yet implemented for TimePointLabeling")

    def write_side_by_side_view(self):
        """
        Side-by-side view not implemented for TimePointLabeling.

        :raises NotImplementedError: Always raises
        """
        raise NotImplementedError(
            "Side-by-side view not implemented for TimePointLabeling")


if __name__ == "__main__":
    parser = TimePointLabelingEvaluator.prep_argparser()
    parser.add_argument('--label-map', nargs='+', default=None,
                       help='Label mappings. Supports: '
                            '(1) Identity: "I S B" → I:I S:S B:B, '
                            '(2) Explicit: "I:chyron S:slate", '
                            '(3) Mixed: "I S:slate B:bars". '
                            'Comma-separated also works. '
                            'Unmapped labels use --default-label value.')
    parser.add_argument('--default-label', type=str, default='-',
                       help='Label to use for unmapped entries '
                            '(default: "-")')

    args = parser.parse_args()

    # Parse label map
    label_map = None
    if args.label_map:
        label_map = parse_label_map(args.label_map)

    evaluator = TimePointLabelingEvaluator(
        batchname=args.batchname,
        gold_loc=args.golds,
        pred_loc=args.preds,
        label_map=label_map,
        default_label=args.default_label
    )

    evaluator.calculate_metrics(by_guid=True)
    report = evaluator.write_report()
    args.export.write(report.getvalue())
