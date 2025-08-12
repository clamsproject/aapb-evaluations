from pathlib import Path
from typing import Any, Union, Tuple, Dict

import numpy
import pandas as pd
import json
from mmif import AnnotationTypes, DocumentTypes, Mmif
from mmif.utils import timeunit_helper as tuh

from common.helpers import find_range_index
from common.metrics import cer
from TextRecognition.evaluate import TextRecognitionEvaluator


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
    
    def __init__(self, batchname: str, **kwargs):

        super().__init__(batchname, **kwargs)

    def _read_gold(self, gold_file: Union[str, Path], **kwargs) -> Dict[Tuple[int, int], Dict[str, Any]]:
        """
        To handle both timepoint-wise gold annotations (transcribed-X series) and 
        timeframe-wise gold annotations (newshour-chyron) 
        this will read csv data and 
        
        :return: a dict from (start, end) tuple to text, where start (inclusive) and end (exclusive) are in milliseconds. For timepoint-wise annotation (with `at` column in the gold data), start will be the `at` value, end will be `at`+1. 
        
        """
        df = super()._get_gold_data(gold_file)

        # convert to dict by adding some millisecond threshold
        threshold = kwargs.get('threshold', 1)
        return {(row['start']-threshold, row['end']+threshold): row['keyed-information'] for _, row in df.iterrows()}

    def _read_pred(self, pred_file: Union[str, Path], gold, **kwargs) -> Any:
        """
        Assuming a video OCR scenario where 
        1. TR ran on a specific time point (extracted still image)
        2. TR results are stored as `TextDocument` (and ignore all other "sub" types such as `Paragraph`, `Sentence`, `Token`)
        3. TR results are `Aligned` to `BoundingBox` annotations (and bbox has temporal information)
        4. TR results have been processed by the HCU application
        
        # TODO (krim @ 5/1/25): image OCR scenario for the future?
        
        :return: (a dict from int (millisecond) to TR result text, gold as-is)
        """
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

    def _compare_pair(self, guid: str, gold: Any, pred: Any) -> Any:
        """
        returns WER scores one for cased and another for uncased (ignore case)
        """
        cased_cers = {'attributes': [], 'name-as-written': [], 'name-normalized': []}
        uncased_cers = {'attributes': [], 'name-as-written': [], 'name-normalized': []}
        # keys of the gold dict is (s, e) range, extract and sort by the start
        gold_ranges = sorted(list(gold.keys()), key=lambda x: x[0])
        for i, (pred_tp, pred_str) in enumerate(pred.items()):
            range_idx = find_range_index(gold_ranges, pred_tp)
            if range_idx == -1:
                # this means the prediction is outside of any gold range
                # TODO (krim @ 5/1/25): how to handle this?
                continue
            # otherwise, we have a valid range
            gold_str = gold[gold_ranges[range_idx]]
            # store original attributes dict for ease of printing side by side
            pred_attr = pred_str['attributes']
            gold_attr = gold_str['attributes']
            # then join for ease of computing CER
            pred_str['attributes'] = ''.join(pred_str['attributes'])
            gold_str['attributes'] = ''.join(gold_str['attributes'])
            # print(f'comparing\n---\n{pred_str}\n===\n{gold_str}\n---')
            cs_cers = {}
            ci_cers = {}
            for k in pred_str:
                if (len(gold_str[k]) == 0 and len(pred_str[k]) > 0) or (len(pred_str[k]) == 0 and len(gold_str[k]) > 0):
                    cs_cers[k] = 1.0
                    ci_cers[k] = 1.0
                else:
                    cs_cers[k] = cer(pred_str[k], gold_str[k], exact_case=True)
                    ci_cers[k] = cer(pred_str[k], gold_str[k], exact_case=False)
            # print(f'CER cased: {cs_cers}, uncased: {ci_cers}\n\n')
            if self._do_sbs:
                # add to side-by-side comparison
                pred_str['attributes'] = pred_attr
                gold_str['attributes'] = gold_attr
                self._sbs.loc[len(self._sbs)] = [f'{guid} ({len(gold)} rows)', pred_tp, gold_str, pred_str, cs_cers, ci_cers]
            for k in cs_cers:
                cased_cers[k].append(cs_cers[k])
                uncased_cers[k].append(ci_cers[k])
        if len(cased_cers['attributes']) == 0:
            return -1, -1
        cased_means = [numpy.mean(cased_cers[key]) for key in cased_cers]
        uncased_means = [numpy.mean(uncased_cers[key]) for key in uncased_cers]

        return cased_means, uncased_means

    def _compare_all(self, golds, preds) -> Any:
        """
        Compare all golds and preds is NOT implemented, hence do not 
        call ``calculate_metrics`` with ``by_guid=False``.
        """
        raise NotImplementedError("Comparing all golds and preds is not implemented. ")

    def _finalize_results(self):
        cols = 'GUID mean-CER-cased mean-CER-uncased'.split()

        # create a DataFrame from the calculations
        ress = []
        for guid, results in self._calculations.items():
            if not results:
                # when pred file was not properly read, we set the results to False
                ress.append([guid, False, False])
            else:
                ress.append([guid] + list(results))
        df = pd.DataFrame(ress, columns=cols)
        # then add the average row, ignoring negative values
        df = self._average_results(df)
        self._results = df.to_csv(index=False, sep=',', header=True)

    def _average_results(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Averages lists within each dataframe column by index.

        :return: the original dataframe with a new averaged results row at the end.
        """
        average_lists = []

        for col in df.columns[1:]:
            col_df = pd.DataFrame(df[df[col] != False][col].tolist())
            col_avg = [col_df[col_df[c] > 0][c].mean() for c in col_df.columns]
            average_lists.append(col_avg)

        df.loc[len(df)] = ['Average'] + average_lists

        return df
    
    def write_side_by_side_view(self):

        super().write_side_by_side_view()


if __name__ == "__main__":
    parser = KeyedInformationExtractionEvaluator.prep_argparser()
    parser.add_argument('-s', '--sbs', action='store_true',
                        help='include side-by-side comparison of text pieces in the report for visualization', )
    args = parser.parse_args()

    evaluator = KeyedInformationExtractionEvaluator(batchname=args.batchname, gold_loc=args.golds, pred_loc=args.preds, sbs=args.sbs)
    evaluator.calculate_metrics(by_guid=True)
    report = evaluator.write_report()
    args.export.write(report.getvalue())
