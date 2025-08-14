import base64
import collections
from pathlib import Path
from typing import Any, Union, Tuple, Dict

import numpy
import pandas as pd
from mmif import AnnotationTypes, DocumentTypes, Mmif
from mmif.utils import timeunit_helper as tuh

from common import ClamsAAPBEvaluationTask
from common.helpers import find_range_index
from common.metrics import cer


class TextRecognitionEvaluator(ClamsAAPBEvaluationTask):
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
    TIMING_MS_THRESHOLD = 10  # threshold for matching gold and pred time points, in milliseconds
    
    def __init__(self, batchname: str, **kwargs):

        super().__init__(batchname, **kwargs)
        self._source_images_loc = kwargs.get('source_images_loc')
        if self._source_images_loc is not None:
            self._source_image_timestamps = collections.defaultdict(dict)
            for source_image in Path(self._source_images_loc).glob('*.jpg'):
                # source image files are named as <guid>_<totalms>_<targetms>_<foundms>.jpg
                parts = source_image.stem.split('_')
                if len(parts) < 3:
                    continue
                self._source_image_timestamps[parts[0]][int(parts[2])] = source_image.name
        if self._do_sbs:
            # empty dataframe for side-by-side comparison
            self._sbs = pd.DataFrame(
                columns=['guid', 'at', 'gold', 'pred', 'cased_cer', 'uncased_cer']
            )
            if self._source_images_loc:
                # add source image column
                self._sbs['source_image'] = None

    def _read_gold(self, gold_file: Union[str, Path], **kwargs) -> Dict[Tuple[int, int], str]:
        """
        To handle both timepoint-wise gold annotations (transcribed-X series) and 
        timeframe-wise gold annotations (newshour-chyron) 
        this will read csv data and 
        
        :return: a dict from (start, end) tuple to text, where start (inclusive) and end (exclusive) are in milliseconds. For timepoint-wise annotation (with `at` column in the gold data), start will be the `at` value, end will be `at`+1. 
        
        """
        df = self._get_gold_data(gold_file)

        # then "un"-escape newlines
        df['text-transcript'] = df['text-transcript'].apply(lambda x: x.replace('\\n', '\n'))
        return {(row['start'], row['end']): row['text-transcript'] for _, row in df.iterrows()}

    @staticmethod
    def _get_gold_data(gold_file: Union[str, Path]) -> pd.DataFrame:
        """
        Reads csv data from timepoint-/timeframe-wise gold annotation file and

        :return: a pandas.DataFrame containing gold data where start (inclusive) and end (exclusive) are in milliseconds.

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

        return df

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
        for i, (pred_tp, pred_datum) in enumerate(pred.items()):
            range_idx = find_range_index(gold_ranges, pred_tp, threshold=self.TIMING_MS_THRESHOLD)
            if range_idx == -1:
                # this means the prediction is outside of any gold range
                # TODO (krim @ 5/1/25): how to handle this?
                continue
            # otherwise, we have a valid range
            gold_range = gold_ranges[range_idx]
            gold_ms = gold_range[0]  # start of the range
            # print('===', guid, gold_ms)
            gold_datum = gold[gold_range]
            # print(f'comparing\n---\n{pred_str}\n===\n{gold_str}\n---')
            ci_cer, cs_cer = self._compute_cer(gold_datum, pred_datum)
            # print(f'CER cased: {cs_cers}, uncased: {ci_cers}\n\n')
            if self._do_sbs:
                # add to side-by-side comparison
                row = [f'{guid} ({len(gold)} rows)', pred_tp, gold_datum, pred_datum, cs_cer, ci_cer]
                if self._source_images_loc:
                    # find the source image
                    img_tss = sorted(list(self._source_image_timestamps[guid].keys()))
                    img_ts_ranges = [(ts, ts + 1) for ts in img_tss]
                    img_ts_idx = find_range_index(img_ts_ranges, gold_ms, threshold=self.TIMING_MS_THRESHOLD)
                    if img_ts_idx == -1:
                        # if we could not find the image, just add an empty string
                        row.append('')
                    else:
                        source_image_fname = self._source_image_timestamps[guid][img_tss[img_ts_idx]]
                        source_image = Path(self._source_images_loc) / source_image_fname
                        # encode with base64 string for html embedding
                        b64str = base64.b64encode(open(source_image, 'rb').read()).decode('utf-8')
                        row.append(f'<img src="data:image/jpeg;base64,{b64str}" alt="{gold_ms} milliseconds in {guid} video"/>')
                self._sbs.loc[len(self._sbs)] = row
            cased_cers.append(cs_cer)
            uncased_cers.append(ci_cer)
        if len(cased_cers) == 0:
            return -1, -1
        return self._aggregate_cers(cased_cers, uncased_cers)
    
    @staticmethod
    def _aggregate_cers(cased_cers, uncased_cers):
        """
        Aggregate CERs by taking the mean, returns two scores (case sensitive and case insensitive) as floats.
        """
        return numpy.mean(cased_cers), numpy.mean(uncased_cers)

    @staticmethod
    def _compute_cer(gold_datum, pred_datum):
        if not pred_datum or not gold_datum:
            cs_cer = 1.0  # if either is empty, we assume 100% error
            ci_cer = 1.0
        else:
            cs_cer = cer(pred_datum, gold_datum, exact_case=True)
            ci_cer = cer(pred_datum, gold_datum, exact_case=False)
        return ci_cer, cs_cer

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
        df.loc[len(df)] = self._average_results_over_guids(df)
        self._results = df.to_csv(index=False, sep=',', header=True)
    
    @staticmethod
    def _average_results_over_guids(results: pd.DataFrame):
        return ['Average'] + [results[results[col] > 0][col].mean() for col in results.columns[1:]]
        
    def write_side_by_side_view(self):
        if self._do_sbs:
            
            def replace_newlines_with_br(text):
                if isinstance(text, str):
                    return text.replace('\n', '<br>')
                elif isinstance(text, dict):
                    s = '<ul>'
                    for k, v in text.items():
                        s += f'  <li>{k}: {v}</li>'
                    s += '</ul>'
                    return s
                return text
            
            def score_dict_to_str(scores) -> str:
                if isinstance(scores, dict):
                    s = '<ul>'
                    for k, v in scores.items():
                        s += f'  <li>{k}: {v:.6f}</li>'
                    s += '</ul>'
                    return s
                return scores
            
            for col in ['gold', 'pred']:
                self._sbs[col] = self._sbs[col].apply(replace_newlines_with_br)
            for col in ['cased_cer', 'uncased_cer']:
                self._sbs[col] = self._sbs[col].apply(score_dict_to_str)
            return self._sbs.to_html(index=False, escape=False,
                                     table_id='sbs-table', 
                                     classes='table table-striped')


if __name__ == "__main__":
    parser = TextRecognitionEvaluator.prep_argparser()
    parser.add_argument('-s', '--sbs', action='store_true',
                        help='include side-by-side comparison of text pieces in the report for visualization', )
    args = parser.parse_args()

    evaluator = TextRecognitionEvaluator(batchname=args.batchname, gold_loc=args.golds, pred_loc=args.preds, sbs=args.sbs, source_images_loc=args.source_directory)
    evaluator.calculate_metrics(by_guid=True)
    report = evaluator.write_report()
    args.export.write(report.getvalue())
