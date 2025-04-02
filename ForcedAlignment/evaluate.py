import re
from pathlib import Path
from typing import Any, Union

import pandas as pd
import pyannote.metrics.base
from lapps.discriminators import Uri
from mmif.serialize import Mmif
from mmif.vocabulary import AnnotationTypes
from pyannote.core import Segment, Annotation
from pyannote.metrics.diarization import DiarizationCoverage, DiarizationPurity
from pyannote.metrics.segmentation import SegmentationCoverage, SegmentationRecall, SegmentationPrecision, \
    SegmentationPurity

from common import ClamsAAPBEvaluationTask


class ForcedAlignerEvaluator(ClamsAAPBEvaluationTask):

    @property
    def results(self) -> Union[dict, str]:
        return self._results

    @staticmethod
    def cadettime_to_ms(time_str):
        try:
            h, m, s = time_str.split(':')
            s, ms = s.split('.')
            return int(h) * 3600000 + int(m) * 60000 + int(s) * 1000 + int(ms)
        except ValueError:
            raise ValueError("Invalid time format. Expected format: hh:mm:ss.mmm")

    def _read_gold(self, gold_file: Union[str, Path]) -> Any:
        gold_timeframes = Annotation()
        df = pd.read_csv(gold_file, sep='\t')
        for index, row in df[['starts', 'ends', 'content']].iterrows():
            segment = Segment(self.cadettime_to_ms(row['starts']) / 1000, self.cadettime_to_ms(row['ends']) / 1000)
            gold_timeframes[segment] = row['content']
        return gold_timeframes

    def tokenize_cadet_silver_text(self, text):
        """
        kaldi/gentle does not return the same text as the original and 
        does its own normalization/tokenization. This function tries to
        reverse-engineer the original text from the kaldi/gentle output
        """
        self.logger.debug(f'original: {text}')
        from string import punctuation
        # text = text.replace("%", " percent")
        # text = text.replace("’", "'")
        text = text.replace("`", " ")  # that`s
        text = text.replace("&", " ")  # AT&T
        text = text.replace("--", " ")
        text = text.replace("..", " ")
        text = text.replace("...", " ")
        # text = text.replace("'re", " re")
        punc_tokens = []
        tokens = []
        for token in text.split():
            # just skip single letter punctuations
            if not token or token in punctuation:
                continue
            # o'clock
            if re.search(r'\d\:\d\d', token):
                punc_tokens.extend(token.split(':'))
            # fractions
            elif re.match(r'\d+\/\d+', token):
                punc_tokens.extend(token.split('/'))
            # decimal numbers
            elif re.search(r'\d\.\d', token):
                punc_tokens.extend(token.split('.'))
            # comma separated large numbers
            elif re.search(r'\d,\d', token):
                punc_tokens.extend(token.split(','))
            # abbreviations (U.S.)
            elif re.match(r'[A-Z]\.([A-Z]\.?)+', token):
                punc_tokens.extend(token.split('.'))
            else:
                # hyphenated words
                punc_tokens.extend(token.split('-'))
        for token in punc_tokens:
            if re.match(r'\'[0-9][0-9]s?', token):
                while token[-1] in punctuation:
                    token = token[:-1]
                tokens.append(token)
            else:
                while token and token[-1] in punctuation:
                    token = token[:-1]
                while token and token[0] in punctuation:
                    token = token[1:]
                if token:
                    tokens.append(token)
        self.logger.debug(f'normaliz: {tokens}')
        return tokens

    def _read_pred(self, pred_file: Union[str, Path], reference) -> Any:
        pred = Annotation()
        with open(pred_file, 'r') as file:
            mmif = Mmif(file.read())
            ref_segs = reference.itertracks(yield_label=True)
            ref_segment_text = self.tokenize_cadet_silver_text(next(ref_segs)[2])
            in_segment = False
            view = mmif.get_view_contains(Uri.TOKEN)
            if view is None:
                return pred
            timeunit = view.metadata.contains[AnnotationTypes.TimeFrame]['timeUnit']
            t2tf_alignments = {}
            for alignment in view.get_annotations(AnnotationTypes.Alignment):
                s = view[alignment.get_property('source')]
                t = view[alignment.get_property('target')]
                if s.at_type == Uri.TOKEN and t.at_type == AnnotationTypes.TimeFrame:
                    t2tf_alignments[s.id] = t
                elif t.at_type == Uri.TOKEN and s.at_type == AnnotationTypes.TimeFrame:
                    t2tf_alignments[t.id] = s
            s, e = 0, 0
            hyp_length = 0
            for i, token in enumerate(view.get_annotations(Uri.TOKEN)):
                # because gentle app returns disfluency tokens that are not in the reference without start/end
                if 'start' not in token.properties:
                    continue
                if i < 300000000:
                    first = ref_segment_text[0]
                    final = ref_segment_text[-1]
                    w = token.get_property('word')
                    self.logger.debug(' '.join(map(str, (token.id, in_segment, w,
                                                    first, w.lower() == first.lower(),
                                                    final, w.lower() == final.lower()))))
                hyp_length += 1
                if token.id in t2tf_alignments:
                    s = t2tf_alignments[token.id].get_property('start')
                    e = t2tf_alignments[token.id].get_property('end')
                # just in case gentle (kaldi) removed the first token during alignment 
                # (happens with some stopwords and symbols)
                if not in_segment and (token.get_property('word').lower() == ref_segment_text[0].lower()
                                       or token.get_property('word').lower() == ref_segment_text[1].lower()):
                    in_segment = True
                    start = s / 1000 if timeunit.startswith('mill') else s
                if in_segment and token.get_property('word').lower() == ref_segment_text[-1].lower():
                    end = e / 1000 if timeunit.startswith('mill') else e
                    pred[Segment(start, end)] = ' '.join(ref_segment_text)
                    try:
                        ref_segment_text = self.tokenize_cadet_silver_text(next(ref_segs)[2])
                        hyp_length = 0
                    except StopIteration:
                        break
                    in_segment = False
                # self.logger.debug(f'system token iteration is done , last timeframe {start}, {e}')
                # if in_segment:
            end = e / 1000 if timeunit.startswith('mill') else e
            pred[Segment(start, end)] = ' '.join(ref_segment_text)
        return pred

    def _compare(self, guid, reference: Any, hypothesis: Any) -> Any:
        """
        Compares a pair of reference (e.g, cadet annotation) and hypothesis
        annotations (from MMIF) and returns a list-like record of 
        evaluation results.
        """
        coverage = DiarizationCoverage()
        purity = DiarizationPurity()
        scoverage = SegmentationCoverage()
        spurity = SegmentationPurity()
        precision = SegmentationPrecision()
        recall = SegmentationRecall()

        if len(hypothesis) == 0:
            self.logger.warning(f'{guid} :: no hypothesis found')
            return []
        if len(reference) != len(hypothesis):
            self.logger.warning(
                f'{guid} :: reference ({len(reference)}) and hypothesis ({len(hypothesis)}) have different number of segments')
        try:
            # coverage, purity, f1, precision, recall, f1
            cpfprf = []
            for met in coverage, purity:
                comps = met.compute_components(reference, hypothesis)
                cpfprf.append(met.compute_metric(comps))
            cpfprf.append(pyannote.metrics.base.f_measure(cpfprf[-2], cpfprf[-1]))
            for met in scoverage, spurity:
                comps = met.compute_components(reference, hypothesis)
                cpfprf.append(met.compute_metric(comps))
            cpfprf.append(pyannote.metrics.base.f_measure(cpfprf[-2], cpfprf[-1]))
            for threshold in self.thresholds:
                for met in precision, recall:
                    comps = met.compute_components(reference, hypothesis, tolerance=threshold)
                    cpfprf.append(met.compute_metric(comps))
                cpfprf.append(pyannote.metrics.base.f_measure(cpfprf[-2], cpfprf[-1]))
            return cpfprf
        except KeyError:
            print(f"Error: Issue with keys in results for file {guid}")

    def finalize_results(self):
        """
        Aggregate the results from all files and calculate the average
        The results should be a dict from guid to a list of results which 
        is the output from the _compare method.
        """
        cols = 'GUID DiaCov DiaPur D-C-P-F1 SegCov SegPur S-C-P-F1'.split()
        for threshold in self.thresholds:
            cols.extend(f'Precision@{threshold} Recall@{threshold} P-R-F1@{threshold}-sec-tolerance'.split())
        data = []
        for guid, results in self._calculations.items():
            if not results:
                continue
            data.append([guid] + results)
        data = pd.DataFrame(data, columns=cols)
        res_str = (f'Individual file results:\n{data.to_string(index=False)}\n\n\n'
                   f'Average results:\n{data.loc[:, data.columns != "GUID"].mean(axis=0)}')
        self._results = res_str


if __name__ == "__main__":
    parser = ForcedAlignerEvaluator.prep_argparser()
    parser.add_argument('-t', '--thresholds',
                        help='comma-separated thresholds in seconds to count as "near-miss", use decimals ', type=str,
                        default="")
    args = parser.parse_args()
    
    evaluator = ForcedAlignerEvaluator(args.batchname)
    evaluator.thresholds = [] if not args.thresholds else [float(t) for t in args.thresholds.split(',')]
    evaluator.get_gold_files(args.golds)
    evaluator.get_pred_files(args.preds)
    evaluator.calculate_metrics(by_guid=True)
    report = evaluator.write_report()
    args.export.write(report.getvalue())
