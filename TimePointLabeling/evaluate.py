from collections import defaultdict
from pathlib import Path
from typing import Any, Union, Optional, Tuple, List

import pandas as pd
from mmif import Mmif, AnnotationTypes
from mmif.utils import timeunit_helper as tuh

from common import ClamsAAPBEvaluationTask
from common.helpers import match_nearest_points
from common.metrics import (precision_recall_fscore, MACRO_AVG_PRECISION,
                            MACRO_AVG_RECALL, MACRO_AVG_F1)


class TimePointLabelingEvaluator(ClamsAAPBEvaluationTask):
    """
    Evaluates TimePoint classification predictions against gold standard
    annotations.

    ## Timestamp Matching
    Uses fuzzy timestamp matching with configurable tolerance (default ±5ms)
    to align predictions with gold timestamps. Each prediction is matched to
    its nearest gold timestamp. Only matched pairs are included in evaluation.
    Use --tolerance to adjust the matching threshold.

    ## Metrics
    Calculates per-label Precision, Recall, and F1 score using
    `sklearn.metrics.precision_recall_fscore_support`. Metrics are computed
    per-document and macro-averaged across labels. An overall average across
    all documents is also reported.

    ## Confusion Matrix
    A confusion matrix is generated showing per-label classification counts.
    Rows represent gold labels (reference), columns represent predicted labels.
    When `--label-map` is provided, labels are shown after mapping.
    """

    def __init__(self, batchname: str, **kwargs):
        self.label_map = kwargs.get('label_map', None)
        self.default_label = kwargs.get('default_label', '-')
        self.tolerance = kwargs.get('tolerance', 5)
        self.target_labels = set()  # to collect labels actually seen in data
        self._confusion_counts = defaultdict(lambda: defaultdict(int))
        # Temporary storage for per-document counts (used during evaluation)
        self._current_doc_gold_counts = {}
        self._current_doc_matched_counts = {}

        super().__init__(batchname, cf=True, **kwargs)

        # Store evaluation-time configurations for report generation
        self._eval_config = {
            'Timestamp matching tolerance': f'{self.tolerance}ms'
        }

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

        # Count gold points per label for this document
        self._current_doc_gold_counts = defaultdict(int)
        for label in gold_dict.values():
            mapped_label = self.label_map.get(label, self.default_label) if self.label_map else label
            self._current_doc_gold_counts[mapped_label] += 1

        return gold_dict

    def _read_pred(self, pred_file: Union[str, Path], gold: Optional[Any],
                   **kwargs) -> Tuple[List[str], List[str]]:
        """
        Read prediction MMIF and return aligned predicted labels.

        Performs fuzzy timestamp matching with configurable tolerance
        (set via --tolerance argument) to align predictions with gold timestamps.

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
        matches = match_nearest_points(list(pred.keys()), list(gold.keys()), tolerance=self.tolerance)

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

        # Count matched points per label for this document
        self._current_doc_matched_counts = defaultdict(int)
        for gold_label in gold_list:
            self._current_doc_matched_counts[gold_label] += 1

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

        # Collect confusion matrix data
        for gold_label, pred_label in zip(gold_labels, pred_labels):
            self._confusion_counts[gold_label][pred_label] += 1

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
            self.target_labels.add(label)

        metrics_dict[MACRO_AVG_PRECISION] = float(macro_p)
        metrics_dict[MACRO_AVG_RECALL] = float(macro_r)
        metrics_dict[MACRO_AVG_F1] = float(macro_f1)

        # Add per-label count data to metrics (from instance variables)
        for label, count in self._current_doc_gold_counts.items():
            metrics_dict[f"{label}_TotalGold"] = count
        for label, count in self._current_doc_matched_counts.items():
            metrics_dict[f"{label}_Matched"] = count

        # Add total counts across all labels
        metrics_dict['Total_GoldCount'] = sum(self._current_doc_gold_counts.values())
        metrics_dict['Total_Matched'] = sum(self._current_doc_matched_counts.values())

        # Clear temporary counts after use
        self._current_doc_gold_counts = {}
        self._current_doc_matched_counts = {}

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
        # keeping order of first appearance
        all_columns = [MACRO_AVG_PRECISION, MACRO_AVG_RECALL, MACRO_AVG_F1,
                       'Total_GoldCount', 'Total_Matched']
        for label in sorted(self.target_labels):
            for metric_suffixes in "PRF":
                col_name = f"{label}_{metric_suffixes}"
                all_columns.append(col_name)
            # Add count columns after metrics for each label
            all_columns.append(f"{label}_TotalGold")
            all_columns.append(f"{label}_Matched")

        # Build DataFrame with consistent columns, filling missing with 0
        rows = []
        for guid, results in self._calculations.items():
            if results:
                row = [guid] + [results.get(col, 0) for col in all_columns]
                rows.append(row)

        df = pd.DataFrame(rows, columns=['GUID'] + all_columns)

        # Build aggregation row (mean for metrics, sum for counts)
        agg_row = ['Overall']
        for col in all_columns:
            if col.endswith(('_TotalGold', '_Matched')) or col in ('Total_GoldCount', 'Total_Matched'):
                # For count columns, sum across documents
                agg_row.append(df[col].sum())
            else:
                # For metric columns (P/R/F), take mean
                agg_row.append(df[col].mean())

        # Insert aggregation row at the beginning
        df.loc[-1] = agg_row
        df.index = df.index + 1
        df = df.sort_index()

        self._results = df

    def write_confusion_matrix(self) -> str:
        """
        Create confusion matrix with count-based entries.

        Rows are reference (gold) labels, columns are predicted labels,
        and entries are the counts of time points.

        :return: Markdown-formatted confusion matrix
        :rtype: str
        """
        if not self._confusion_counts:
            return "No confusion matrix data available.\n"

        df = pd.DataFrame.from_dict(
            self._confusion_counts, orient='index'
        )
        df = df.fillna(0).astype(int)

        # Sort for consistent output
        df = df.sort_index().sort_index(axis=1)

        df.index.name = 'gold\\pred'
        return df.to_markdown(index=True)

    def write_side_by_side_view(self):
        """
        Side-by-side view not implemented for TimePointLabeling.

        :raises NotImplementedError: Always raises
        """
        raise NotImplementedError(
            "Side-by-side view not implemented for TimePointLabeling")


if __name__ == "__main__":
    parser = TimePointLabelingEvaluator.prep_argparser()
    parser.add_argument(
        '--tolerance',
        type=int,
        default=5,
        help='Timestamp matching tolerance in milliseconds (default: 5ms)'
    )
    args = parser.parse_args()

    # Parse label map using common helper
    label_map = TimePointLabelingEvaluator.parse_label_map_args(args)

    evaluator = TimePointLabelingEvaluator(
        batchname=args.batchname,
        gold_loc=args.golds,
        pred_loc=args.preds,
        label_map=label_map,
        default_label=args.default_label,
        tolerance=args.tolerance
    )

    evaluator.calculate_metrics(by_guid=True)
    report = evaluator.write_report()
    args.export.write(report.getvalue())
