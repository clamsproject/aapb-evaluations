from collections import defaultdict
from pathlib import Path
from typing import Any, Union, Optional, Tuple, List

import numpy as np
import pandas as pd
from mmif import Mmif, AnnotationTypes
from mmif.utils import timeunit_helper as tuh

from common import ClamsAAPBEvaluationTask
from common.metrics import MACRO_AVG_PRECISION, MACRO_AVG_RECALL, MACRO_AVG_F1

# column name in the confusion matrix for scored time without a prediction
NO_PRED = '(none)'

# (start_ms, end_ms, label)
Segment = Tuple[int, int, str]


class TimeFrameLabelingEvaluator(ClamsAAPBEvaluationTask):
    """
    Evaluates labeled time segments (chyron detection, slate detection,
    spoken language identification, ...) against gold time segments, by
    comparing labels at points on a fixed time grid.

    ## Point-wise comparison
    The timeline is cut into points every `--resolution` ms (default 10). A
    point stands for the time from it to the next point. Each point takes the
    gold label and the predicted label of the segments that contain it.

    Only points inside a gold segment are scored, so time outside the gold
    annotation does not count. Points in gold segments with a label given in
    `--exclude-labels` are not scored either. A scored point with no
    predicted label counts against the recall of its gold label. When every
    segment boundary is a multiple of the resolution, the counts are exact
    durations.

    Labels are compared as strings, after `--label-map` is applied to both
    gold and predicted labels. No mapping between the gold and the predicted
    label sets is searched for, so a prediction is correct only when it has
    the gold label.

    Predictions come from the last view of the MMIF with TimeFrame
    annotations. Where predicted TimeFrames overlap, the one that starts
    later is used.

    ## Metrics
    Per label: precision, recall and F1, over durations. Macro averages are
    over the gold labels. Accuracy is the share of scored time with the
    correct label; with one label per point, it equals the micro-averaged
    precision, recall and F1. The `Overall` row pools the time of all
    documents; the `Mean` row is the mean of the per-document scores.

    ## Confusion Matrix
    Seconds of scored time, pooled over all documents. Rows are gold labels
    and columns are predicted labels; `(none)` is scored time with no
    prediction.
    """

    def __init__(self, batchname: str, **kwargs):
        self.label_map = kwargs.get('label_map', None)
        self.default_label = kwargs.get('default_label', '-')
        self.resolution = kwargs.get('resolution', 10)
        self.exclude_labels = set(kwargs.get('exclude_labels') or [])
        self.target_labels = set()  # gold labels seen in scored time
        self._confusion_durations = defaultdict(lambda: defaultdict(int))
        # label ids for the time grids, shared by all documents
        self._labels = []
        self._label_ids = {}

        super().__init__(batchname, cf=True, **kwargs)

        # Store evaluation-time configurations for report generation
        self._eval_config = {
            'Time grid resolution': f'{self.resolution}ms',
            'Gold labels not scored': ', '.join(
                f'`{label}`' for label in sorted(self.exclude_labels))
                or 'none',
            'Prediction view': 'last view with TimeFrames',
        }

    def _map_label(self, label: str) -> str:
        if not self.label_map:
            return label
        return self.label_map.get(label, self.default_label)

    def _label_id(self, label: str) -> int:
        if label not in self._label_ids:
            self._label_ids[label] = len(self._labels)
            self._labels.append(label)
        return self._label_ids[label]

    def _read_gold(self, gold_file: Union[str, Path],
                   **kwargs) -> List[Segment]:
        """
        Read gold CSV file and return the gold segments.

        :param gold_file: Path to CSV file with 'start' and 'end' columns
                          (ISO format) and a label column matching pattern
                          '*-label' (e.g., 'scene-label')
        :return: List of (start_ms, end_ms, label) tuples, sorted, with
                 label mapping applied and excluded labels left out
        :rtype: List[Segment]
        """
        df = pd.read_csv(gold_file, dtype=str, keep_default_na=False)

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

        segments = []
        for _, row in df.iterrows():
            # 'NO' marks a gold file without any segment
            if row['start'] == 'NO' or row[label_col] in self.exclude_labels:
                continue
            start, end = (int(tuh.convert(row[col], 'iso', 'milliseconds', 1))
                          for col in ('start', 'end'))
            segments.append((start, end, self._map_label(row[label_col])))
        return sorted(segments)

    def _select_view(self, pred_mmif: Mmif, pred_file: Union[str, Path]):
        """
        Pick the view to evaluate: the last view with TimeFrame annotations.
        """
        views = list(
            pred_mmif.get_all_views_contain(AnnotationTypes.TimeFrame))
        if not views:
            self.logger.warning(
                f"No TimeFrame view to evaluate in {pred_file}")
            return None
        if len(views) > 1:
            self.logger.warning(
                f"{len(views)} TimeFrame views in {pred_file}; using the "
                f"last, {views[-1].id} from {views[-1].metadata.app}")
        return views[-1]

    @staticmethod
    def _to_ms(pred_mmif: Mmif, annotation, t: Union[int, float]) -> int:
        unit = annotation.get('timeUnit', 'milliseconds')
        fps = 1
        if tuh.UNIT_NORMALIZATION.get(unit) == 'frame':
            fps = pred_mmif[annotation.get('document')].get('fps')
            if fps is None:
                raise ValueError(
                    f"{annotation.long_id} is in frames, but its document "
                    f"has no fps property")
        return int(tuh.convert(t, unit, 'milliseconds', fps))

    def _read_pred(self, pred_file: Union[str, Path], gold: Optional[Any],
                   **kwargs) -> Tuple[Optional[List[Segment]], None]:
        """
        Read prediction MMIF and return the predicted segments.

        :param pred_file: Path to MMIF file containing TimeFrame annotations
        :param gold: Gold segments (passed through unchanged)
        :return: Tuple of (predicted segments, None); the segments are None
                 when the MMIF has no view to evaluate
        :rtype: Tuple[Optional[List[Segment]], None]
        """
        mmif_f = open(pred_file, "r")
        pred_mmif = Mmif(mmif_f.read())
        mmif_f.close()

        view = self._select_view(pred_mmif, pred_file)
        if view is None:
            return None, None
        segments = []
        for annotation in view.get_annotations(AnnotationTypes.TimeFrame):
            start, end = (self._to_ms(pred_mmif, annotation, t)
                          for t in (pred_mmif.get_start(annotation),
                                    pred_mmif.get_end(annotation)))
            segments.append(
                (start, end, self._map_label(annotation.get('label'))))
        return sorted(segments), None

    def _rasterize(self, segments: List[Segment], n_points: int, guid: str,
                   source: str) -> np.ndarray:
        """
        Label the points of the time grid.

        :param segments: Sorted (start_ms, end_ms, label) tuples
        :param n_points: Number of points in the grid
        :param guid: Document identifier, for logging
        :param source: 'gold' or 'pred', for logging
        :return: Label id per point, -1 for a point outside all segments.
                 Point i covers [i * resolution, (i + 1) * resolution) ms;
                 where segments overlap, the one that starts later is used.
        :rtype: np.ndarray
        """
        res = self.resolution
        labels = np.full(n_points, -1, dtype=np.int64)
        overlap = 0
        misaligned = 0
        covered_until = None
        for start, end, label in segments:
            if covered_until is not None and start < covered_until:
                overlap += min(end, covered_until) - start
            covered_until = (end if covered_until is None
                             else max(covered_until, end))
            misaligned += (start % res != 0) + (end % res != 0)
            # points i with start <= i * res < end
            labels[-(-start // res):-(-end // res)] = self._label_id(label)
        if overlap:
            self.logger.warning(
                f"{guid}: {source} segments overlap for {overlap} ms in "
                f"total; the segment that starts later is used")
        if misaligned:
            self.logger.info(
                f"{guid}: {misaligned} {source} boundaries are not multiples "
                f"of {res} ms, so durations are approximate")
        return labels

    def _scores(self, confusion: dict) -> dict:
        """
        Duration-based metrics from a confusion table.

        :param confusion: Dict of gold label -> predicted label -> ms
        :return: Dict with per-label metrics ("{label}_P", "{label}_R",
                 "{label}_F", "{label}_GoldSec" for each gold label) plus
                 macro-averaged metrics (MACRO_AVG_PRECISION,
                 MACRO_AVG_RECALL, MACRO_AVG_F1 constants from
                 common.metrics), 'Accuracy' and 'Total_GoldSec'
        :rtype: dict
        """
        pred_totals = defaultdict(int)
        for row in confusion.values():
            for pred_label, duration in row.items():
                pred_totals[pred_label] += duration

        metrics_dict = {}
        per_label = []
        correct = 0
        for label in sorted(confusion):
            gold_total = sum(confusion[label].values())
            tp = confusion[label].get(label, 0)
            correct += tp
            precision = tp / pred_totals[label] if pred_totals[label] else 0.0
            recall = tp / gold_total
            f1 = (2 * precision * recall / (precision + recall)
                  if precision + recall else 0.0)
            metrics_dict[f"{label}_P"] = precision
            metrics_dict[f"{label}_R"] = recall
            metrics_dict[f"{label}_F"] = f1
            metrics_dict[f"{label}_GoldSec"] = gold_total / 1000
            per_label.append((precision, recall, f1))
            self.target_labels.add(label)

        total = sum(pred_totals.values())
        macro_p, macro_r, macro_f1 = np.mean(per_label, axis=0)
        metrics_dict[MACRO_AVG_PRECISION] = float(macro_p)
        metrics_dict[MACRO_AVG_RECALL] = float(macro_r)
        metrics_dict[MACRO_AVG_F1] = float(macro_f1)
        metrics_dict['Accuracy'] = correct / total
        metrics_dict['Total_GoldSec'] = total / 1000
        return metrics_dict

    def _compare_pair(self, guid: str, gold: Any,
                      pred: Any) -> Union[dict, bool]:
        """
        Calculate evaluation metrics for a single document.

        :param guid: Document identifier
        :param gold: Gold segments
        :param pred: Predicted segments
        :return: Dict of metrics (see ``_scores``), or False when the
                 document has no scored time
        :rtype: Union[dict, bool]
        """
        if not gold:
            self.logger.warning(f"{guid}: no gold time to score")
            return False
        last_end = max(end for _, end, _ in gold + pred)
        n_points = -(-last_end // self.resolution)
        gold_ids = self._rasterize(gold, n_points, guid, 'gold')
        pred_ids = self._rasterize(pred, n_points, guid, 'pred')

        # count (gold, pred) label pairs over the scored points
        scored = gold_ids >= 0
        n_labels = len(self._labels) + 1  # +1 for "no prediction"
        pair_codes = gold_ids[scored] * n_labels + pred_ids[scored] + 1
        codes, counts = np.unique(pair_codes, return_counts=True)
        confusion = defaultdict(dict)
        for code, count in zip(codes.tolist(), counts.tolist()):
            gold_id, pred_id = divmod(code, n_labels)
            gold_label = self._labels[gold_id]
            pred_label = NO_PRED if pred_id == 0 else self._labels[pred_id - 1]
            duration = count * self.resolution
            confusion[gold_label][pred_label] = duration
            self._confusion_durations[gold_label][pred_label] += duration
        if not confusion:
            self.logger.warning(f"{guid}: no gold time to score")
            return False
        return self._scores(confusion)

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
        Generate a DataFrame with per-document metrics.

        Rows: Overall (pooled time of all documents) + Mean (mean of
        per-document scores) + GUIDs
        Columns: GUID + macro-averaged metrics + accuracy + per-label
        metrics (P/R/F and gold duration)

        A per-label cell is empty for a document without that gold label,
        and the Mean row averages only the documents that have it.

        :return: None (sets self._results)
        """
        overall = (self._scores(self._confusion_durations)
                   if self._confusion_durations else {})

        all_columns = [MACRO_AVG_PRECISION, MACRO_AVG_RECALL, MACRO_AVG_F1,
                       'Accuracy', 'Total_GoldSec']
        for label in sorted(self.target_labels):
            for metric_suffix in "PRF":
                all_columns.append(f"{label}_{metric_suffix}")
            all_columns.append(f"{label}_GoldSec")

        rows = []
        for guid, results in self._calculations.items():
            if results:
                rows.append([guid] + [results.get(col, np.nan)
                                      for col in all_columns])
        df = pd.DataFrame(rows, columns=['GUID'] + all_columns)

        # durations are summed in the Overall row, and not averaged
        mean_row = ['Mean'] + [
            np.nan if col.endswith('GoldSec') else df[col].mean()
            for col in all_columns]
        overall_row = ['Overall'] + [overall.get(col, np.nan)
                                     for col in all_columns]
        summary_df = pd.DataFrame([overall_row, mean_row], columns=df.columns)
        self._results = pd.concat([summary_df, df], ignore_index=True)

    def write_confusion_matrix(self) -> str:
        """
        Create confusion matrix with duration-based entries.

        Rows are reference (gold) labels, columns are predicted labels, and
        entries are seconds of scored time, pooled over all documents.

        :return: Markdown-formatted confusion matrix
        :rtype: str
        """
        if not self._confusion_durations:
            return "No confusion matrix data available.\n"

        df = pd.DataFrame.from_dict(
            self._confusion_durations, orient='index'
        )
        df = df.fillna(0) / 1000

        # Sort for consistent output, with the "no prediction" column last
        columns = sorted(col for col in df.columns if col != NO_PRED)
        if NO_PRED in df.columns:
            columns.append(NO_PRED)
        df = df.sort_index()[columns]

        df.index.name = 'gold\\pred'
        return df.to_markdown(index=True, floatfmt='.2f')

    def write_side_by_side_view(self):
        """
        Side-by-side view not implemented for TimeFrameLabeling.

        :raises NotImplementedError: Always raises
        """
        raise NotImplementedError(
            "Side-by-side view not implemented for TimeFrameLabeling")


if __name__ == "__main__":
    parser = TimeFrameLabelingEvaluator.prep_argparser()
    parser.add_argument(
        '--resolution',
        type=int,
        default=10,
        help='Spacing of the time grid in milliseconds (default: 10ms). '
             'Use a value that divides all segment boundaries, so that the '
             'counts are exact durations.'
    )
    parser.add_argument(
        '--exclude-labels',
        nargs='+',
        default=[],
        help='Gold labels, as written in the gold files and before label '
             'mapping, whose time is not scored (e.g. "Mixed" "No Label").'
    )
    args = parser.parse_args()

    # Parse label map using common helper
    label_map = TimeFrameLabelingEvaluator.parse_label_map_args(args)

    evaluator = TimeFrameLabelingEvaluator(
        batchname=args.batchname,
        gold_loc=args.golds,
        pred_loc=args.preds,
        label_map=label_map,
        default_label=args.default_label,
        resolution=args.resolution,
        exclude_labels=args.exclude_labels
    )

    evaluator.calculate_metrics(by_guid=True)
    report = evaluator.write_report()
    args.export.write(report.getvalue())
