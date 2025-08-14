import collections
import json
from pathlib import Path
from typing import Any, Union, Tuple, Dict

import numpy
import pandas as pd
from mmif import AnnotationTypes, DocumentTypes, Mmif
from mmif.utils import timeunit_helper as tuh

from TextRecognition.evaluate import TextRecognitionEvaluator
from common.metrics import cer


class KeyedInformationExtractionEvaluator(TextRecognitionEvaluator):
    """
    Evaluating Keyed Information Extraction (KIE) results, a task that extends
    general text recognition (OCR) by constructing structured mappings from
    predefined category sets to portions of recognized text. Specifically,
    KIE extends basic OCR by adding semantic categorization - instead of just
    extracting raw text, the system must organize recognized content into
    meaningful, predefined categories. This structured approach enables
    downstream applications to directly access specific information types.

    Example: Chyron Text Processing
    From chyron images, KIE can extract a three-key dictionary:
    - `name-as-written`: Person's name exactly as displayed in source
    - `name-normalized`: Standardized name format
    - `attributes`: Role/title/location information

    For valid KIE evaluation, both gold standard annotations and system
    predictions must use identical category schemas. Mismatched categories
    will result in invalid comparisons and unreliable metrics. Performance
    is measured using Character Error Rate calculated separately
    for each information category, as reported for both case-sensitive
    and case-insensitive variants, and overall averaged across all categories.
    """

    def _read_gold(self, gold_file: Union[str, Path], **kwargs) -> Dict[Tuple[int, int], Dict[str, Any]]:
        """
        To handle both timepoint-wise gold annotations (transcribed-X series) and 
        timeframe-wise gold annotations (newshour-chyron) 
        this will read csv data and 
        
        :return: a dict from (start, end) tuple to text, where start (inclusive) and end (exclusive) are in milliseconds. For timepoint-wise annotation (with `at` column in the gold data), start will be the `at` value, end will be `at`+1. 
        
        """
        df = super()._get_gold_data(gold_file)

        return {(row['start'], row['end']): row['keyed-information'] for _, row in df.iterrows()}

    def _read_pred(self, pred_file: Union[str, Path], gold, **kwargs) -> Any:
        f = open(pred_file, 'r')
        mmif_str = f.read()
        f.close()
        data = Mmif(mmif_str)
        cand_views = data.get_all_views_contain(
            DocumentTypes.TextDocument, AnnotationTypes.Alignment)
        if not cand_views:
            raise Exception("No TR view found in the MMIF file. A TR view should contain TextDocument and Alignment annotations")
        # pick the last 
        tr_view = cand_views[-1]
        # get chyron parsed view
        # TODO (ledibr @ 7/21/25): correctly raise an exception if not found
        text_views = data.get_all_views_contain(DocumentTypes.TextDocument)
        hcu_view = text_views[-1]
        hcu_texts = {}
        for doc in hcu_view.get_annotations(DocumentTypes.TextDocument):
            source = doc.get_property('origin')
            hcu_texts[source] = json.loads(doc.text_value)
        # NOTE that we're also dealing with video scenario
        fps = next(doc.get_property('fps') for doc in data.documents if doc.get_property('fps'))
        preds = {}
        for td in tr_view.get_annotations(DocumentTypes.TextDocument):
            for ali in td.get_all_aligned():
                # TD is aligned directly to the representative frame, 
                # while sub-structures (paragraph, sents, tokens) can be aligned to individual bounding boxes
                if ali.at_type == AnnotationTypes.TimePoint:
                    in_unit = 'milliseconds' if 'timeunit' not in ali.properties else ali.get_property('timeunit')
                    timestamp = tuh.convert(data.get_start(ali), in_unit, 'milliseconds', fps)
                    # link the timestamp and correct text value by original doc id
                    preds[timestamp] = hcu_texts[td.long_id]
        return preds, gold

    @staticmethod
    def _aggregate_cers(cased_cers, uncased_cers):
        """
        Aggregates the results from cased and uncased dictionaries.
        Returns two dicts (case sensitive and case insensitive) with 
        three float scores (for each key)
        """
        cased_score_collection = collections.defaultdict(list)
        uncased_score_collection = collections.defaultdict(list)
        for cer in cased_cers:
            for key, score in cer.items():
                cased_score_collection[key].append(score)
        for cer in uncased_cers:
            for key, score in cer.items():
                uncased_score_collection[key].append(score)
        
        cased_means = {key: float(numpy.mean(scores)) if scores else 0.0 for key, scores in cased_score_collection.items()}
        uncased_means = {key: float(numpy.mean(scores)) if scores else 0.0 for key, scores in uncased_score_collection.items()}
        
        return cased_means, uncased_means

    @staticmethod
    def _compute_cer(gold_datum, pred_datum):
        """
        Computes CER score for each key in the gold and pred dictionaries.
        Returns CER scores under the same keys.
        """
        # validate that both gold and pred are dictionaries with the same keys
        if not isinstance(gold_datum, dict) or not isinstance(pred_datum, dict):
            raise ValueError("Both gold and pred must be dictionaries with the same keys.")
        if set(gold_datum.keys()) != set(pred_datum.keys()):
            raise ValueError("Gold and pred dictionaries must have the same keys.")
        cased_cers = {}
        uncased_cers = {}
        for key in gold_datum:
            gold_value = gold_datum[key]
            pred_value = pred_datum[key]
            gold_value = ''.join(gold_value) if isinstance(gold_value, list) else gold_value
            pred_value = ''.join(pred_value) if isinstance(pred_value, list) else pred_value
            if isinstance(gold_value, str) and isinstance(pred_value, str):
                if (len(gold_value) == 0 and len(pred_value) > 0) or (len(pred_value) == 0 and len(gold_value) > 0):
                    cased_cers[key] = 1.0
                    uncased_cers[key] = 1.0
                else:
                    cased_cers[key] = cer(pred_value, gold_value, exact_case=True)
                    uncased_cers[key] = cer(pred_value, gold_value, exact_case=False)
        return cased_cers, uncased_cers

    def _compare_all(self, golds, preds) -> Any:
        """
        Compare all golds and preds is NOT implemented, hence do not 
        call ``calculate_metrics`` with ``by_guid=False``.
        """
        raise NotImplementedError("Comparing all golds and preds is not implemented. ")

    @staticmethod
    def _average_results_over_guids(results: pd.DataFrame):
        average_lists = []

        for col in results.columns[1:]:
            col_df = pd.DataFrame(results[results[col] != False][col].tolist())
            col_avg = [col_df[col_df[c] > 0][c].mean() for c in col_df.columns]
            average_lists.append(col_avg)
        return ['Average'] + average_lists


if __name__ == "__main__":
    parser = KeyedInformationExtractionEvaluator.prep_argparser()
    parser.add_argument('-s', '--sbs', action='store_true',
                        help='include side-by-side comparison of text pieces in the report for visualization', )
    args = parser.parse_args()

    evaluator = KeyedInformationExtractionEvaluator(batchname=args.batchname, gold_loc=args.golds, pred_loc=args.preds, sbs=args.sbs)
    evaluator.calculate_metrics(by_guid=True)
    report = evaluator.write_report()
    args.export.write(report.getvalue())
