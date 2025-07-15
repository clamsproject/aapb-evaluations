from pathlib import Path
from typing import Any, Union, Tuple, Dict

import numpy
import pandas as pd
from mmif import AnnotationTypes, DocumentTypes, Mmif
from mmif.utils import timeunit_helper as tuh

from common import ClamsAAPBEvaluationTask
from common.helpers import find_range_index
from common.metrics import cer


class AutomaticSpeechRecognitionEvaluator(ClamsAAPBEvaluationTask):
    """
    Evaluating Text Recognition (a.k.a OCR) results, using CER (Character 
    Error Rate) metric. CER calculates the accuracy on the character level,
    using edit distance algorithm. Namely, CER tells "how many edits" it 
    takes to correct the predicted result into the gold standard text. That 
    said, note that 

    1. For CER, the lower the value, the better the performance.
    1. CER can be more that 100%, although it sounds strange. 
    
    (When this evaluator could not find any matching pairs between a gold 
    and a prediction, it will return -1 for CER values.)
    (When this evaluator could not find any predictions at all for a GUID, 
    it will return False for CER values.)

    General information on TR evaluation can be found https://en.wikipedia.org/wiki/Optical_character_recognition#Accuracy
    And more details on the edit distance (Levenshtein algorithm) can be found https://en.wikipedia.org/wiki/Levenshtein_distance
    """
    
    def __init__(self, batchname: str, **kwargs):

        super().__init__(batchname, **kwargs)
        if self._do_sbs:
            # empty dataframe for side-by-side comparison
            self._sbs = pd.DataFrame(
                columns=['guid', 'at', 'gold', 'pred', 'cased_cer', 'uncased_cer']
            )

    def _read_gold(self, gold_file: Union[str, Path], **kwargs) -> Dict[Tuple[int, int], str]:
        """
        To handle both timepoint-wise gold annotations (transcribed-X series) and 
        timeframe-wise gold annotations (newshour-chyron) 
        this will read csv data and 
        
        :return: a dict from (start, end) tuple to text, where start (inclusive) and end (exclusive) are in milliseconds. For timepoint-wise annotation (with `at` column in the gold data), start will be the `at` value, end will be `at`+1. 
        
        """
        if str(gold_file).endswith('.csv'):
            df = pd.read_csv(gold_file) 
        elif str(gold_file).endswith('.json'):
            df = pd.read_json(gold_file)
        # if `at` column? timepoint annotation
        if 'at' in df.columns:
            # rename to start 
            df = df.rename(columns={'at': 'start'})
            # convert value to ms using tuh.convert 
            df['start'] = df['start'].apply(lambda x: tuh.convert(x, 'iso', 'milliseconds', 1))
            # add end column, value is start + 1 
            df['end'] = df['start'] + 1
        elif 'start' in df.columns and 'end' in df.columns:
            df['start'] = df['start'].apply(lambda x: tuh.convert(x, 'iso', 'milliseconds', 1))
            df['end'] = df['end'].apply(lambda x: tuh.convert(x, 'iso', 'milliseconds', 1))
        else:
            raise ValueError(f"Gold file {gold_file} must have either 'at' column or 'start' and 'end' columns.")
        # then "un"-escape newlines
        df['text-transcript'] = df['text-transcript'].apply(lambda x: x.replace('\\n', '\n'))
        # convert to dict by adding some millisecond threshold
        threshold = kwargs.get('threshold', 1)
        return {(row['start']-threshold, row['end']+threshold): row['text-transcript'] for _, row in df.iterrows()}

    def _read_pred(self, pred_file: Union[str, Path], gold, **kwargs) -> Any:
        """
        Assuming a video OCR scenario where 
        1. TR ran on a specific time point (extracted still image)
        1. TR results are stored as `TextDocument` (and ignore all other "sub" types such as `Paragraph`, `Sentence`, `Token`)
        1. TR results are `Aligned` to `BoundingBox` annotations (and bbox has temporal information)
        
        # TODO (krim @ 5/1/25): image OCR scenario for the future?
        
        :return: (a dict from int (millisecond) to TR result text, gold as-is)
        """
        f = open(pred_file, 'r')
        mmif_str = f.read()
        f.close()
        data = Mmif(mmif_str)
        # NOTE that we're also dealing with video scenario
        fps = next(doc.get_property('fps') for doc in data.documents if doc.get_property('fps'))
        preds = {}
        # start from the end 
        found_tr_view = False
        for td_view in reversed(data.get_all_views_contain(DocumentTypes.TextDocument)):
            if found_tr_view:
                # we already found the TR view, so we can stop
                break
            for td in td_view.get_annotations(DocumentTypes.TextDocument):
                for ali in td.get_all_aligned():
                    # TD is aligned directly to the representative frame, 
                    # while sub-structures (paragraph, sents, tokens) can be aligned to individual bounding boxes
                    if ali.at_type == AnnotationTypes.TimePoint:
                        found_tr_view = True
                        in_unit = 'milliseconds' if 'timeunit' not in ali.properties else ali.get_property('timeunit')
                        preds[tuh.convert(data.get_start(ali), in_unit, 'milliseconds', fps)] = td.text_value
        if not preds:
            raise Exception("No TR view found in the MMIF file. A TR view should contain TextDocument with Alignment to TimePoint annotation.")
        return preds, gold

    def _compare_pair(self, guid: str, gold: Any, pred: Any) -> Any:
        """
        returns WER scores one for cased and another for uncased (ignore case)
        """
        cased_cers = []
        uncased_cers = []
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
            # print(f'comparing\n---\n{pred_str}\n===\n{gold_str}\n---')
            if not pred_str or not gold_str:
                cs_cers = 1.0  # if either is empty, we assume 100% error
                ci_cers = 1.0
            else:
                cs_cers = cer(pred_str, gold_str, exact_case=True)
                ci_cers = cer(pred_str, gold_str, exact_case=False)
            # print(f'CER cased: {cs_cers}, uncased: {ci_cers}\n\n')
            if self._do_sbs:
                # add to side-by-side comparison
                self._sbs.loc[len(self._sbs)] = [f'{guid} ({len(gold)} rows)', pred_tp, gold_str, pred_str, cs_cers, ci_cers]
            cased_cers.append(cs_cers)
            uncased_cers.append(ci_cers)
        if len(cased_cers) == 0:
            return -1, -1
        return numpy.mean(cased_cers), numpy.mean(uncased_cers)

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
        df.loc[len(df)] = ['Average'] + [df[df[col] > 0][col].mean() for col in df.columns[1:]]
        self._results = df.to_csv(index=False, sep=',', header=True)
    
    def write_side_by_side_view(self):
        if self._do_sbs:
            def replace_newlines_with_br(text):
                if isinstance(text, str):
                    return text.replace('\n', '<br>')
                return text
            for col in ['gold', 'pred']:
                self._sbs[col] = self._sbs[col].apply(replace_newlines_with_br)
            return self._sbs.to_html(index=False, escape=False,
                                     table_id='sbs-table', 
                                     classes='table table-striped')


if __name__ == "__main__":
    parser = AutomaticSpeechRecognitionEvaluator.prep_argparser()
    parser.add_argument('-s', '--sbs', action='store_true',
                        help='include side-by-side comparison of text pieces in the report for visualization', )
    args = parser.parse_args()

    evaluator = AutomaticSpeechRecognitionEvaluator(batchname=args.batchname, gold_loc=args.golds, pred_loc=args.preds, sbs=args.sbs)
    evaluator.calculate_metrics(by_guid=True)
    report = evaluator.write_report()
    args.export.write(report.getvalue())
