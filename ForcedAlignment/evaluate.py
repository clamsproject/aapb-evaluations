import re
from pathlib import Path
from typing import Any, Union

import pandas as pd
import pyannote.metrics.base
from lapps.discriminators import Uri
from mmif.serialize import Mmif
from mmif.vocabulary import AnnotationTypes
from pyannote.core import Segment, Annotation
from pyannote.metrics.segmentation import SegmentationCoverage, SegmentationPurity
from clams_utils.aapb import guidhandler

from common import ClamsAAPBEvaluationTask


class ForcedAlignmentEvaluator(ClamsAAPBEvaluationTask):
    """
    Evaluating Forced Alignment results using precision, recall, coverage, 
    and purity metrics. The evaluation is done on the segment level, where
    each segment is treated as a separate entity. The following metrics 
    are used; 
    
    - Coverage: The percentage of the reference segments that are covered by
         the hypothesis segments. Think of it as recall-like for interval data
    - Purity: The percentage of the hypothesis segments that are covered by
            the reference segments. Think of it as precision-like for interval data
            
    We use `pyannote.metrics` library for the implementation of these metrics, 
    and hence more details can be found in `pyannote.metrics` documentation at 
    https://pyannote.github.io/pyannote-metrics/reference.html#segmentation 
    
    This script was originally written to evaluate gentle-forced-aligner-wrapper, 
    but DO NOT USE THIS MODULE with gentle predictions: 
        Due to gentle's unexpected behavior of seemingly randomly "re-writes" original text, it is not possible to 
        robustly and consistently "align" the (non-)gold text and pred text in a scalabel way. This class contains some
        early attempts to normalize the text to make it more consistent, but it is not perfect, and I realized that it 
        is not possible to do this way. We should probably just drop using gentle after all, not because we know its 
        performance is not good (last time we reported numbers, they looked very good actually), but because of the 
        unauthorized, arbitrary text alteration. 
        
        There's another issue with the gold text, which is that the gold text is not the original text, but a modified 
        version for cadet annotation. See https://github.com/clamsproject/aapb-annotations/issues/5#issuecomment-1693697601
    """

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

    def _read_gold(self, gold_file: Union[str, Path], **kwargs) -> Any:
        gold_timeframes = Annotation()
        df = pd.read_csv(gold_file, sep='\t')
        for index, row in df[['start', 'end', 'speech-transcript']].iterrows():
            segment = Segment(self.cadettime_to_ms(row['start']) / 1000, self.cadettime_to_ms(row['end']) / 1000)
            # self.logger.debug(f'({segment.start} - {segment.end}): {row["speech-transcript"]}')
            gold_timeframes[segment] = row['speech-transcript']
        return gold_timeframes
    
    def normalize_token(self, text):
        """
        """
        # text = text.replace("%", " percent")
        # text = text.replace("’", "'")  # There’s
        # just remove all kinds of quotes
        text = text.replace("'", "")
        text = text.replace("’", "")
        text = text.replace("\"", "")
        text = text.replace("`", "")  # that`s
        
        text = text.replace("&", " ")  # AT&T
        text = text.replace("--", " ")
        text = text.replace(",", " ")
        text = text.replace("..", " ")
        text = text.replace("...", " ")
        # text = text.replace("'re", " re")
        return text

    def normalize_cadet_tokens(self, text):
        """
        kaldi/gentle does not return the same text as the original and 
        does its own normalization/tokenization. This function tries to
        reverse-engineer the original text from the kaldi/gentle output
        """
        self.logger.debug(f'orig: {text}')
        from string import punctuation
        text = self.normalize_token(text)
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
        self.logger.debug(f'norm: {tokens}')
        return tokens

    def _read_pred(self, pred_file: Union[str, Path], reference, **kwargs) -> Any:
        pred = Annotation()
        guid = guidhandler.get_aapb_guid_from(str(pred_file))
        self.logger.debug(guid)
        with (open(pred_file, 'r') as file):
            mmif = Mmif(file.read())
            ref_segs = reference.itertracks(yield_label=True)
            ref_segment_text = self.normalize_cadet_tokens(next(ref_segs)[2])
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
                w = token.get_property('word')
                token_from_pred = self.normalize_token(w)
                self.logger.debug(' '.join(map(str, (guid, token.id, 'in_seg?', in_segment, f'word: "{w}" > "{token_from_pred}"', ref_segment_text[0], w.lower() == ref_segment_text[0].lower(), ref_segment_text[-1], w.lower() == ref_segment_text[-1].lower()))))
                hyp_length += 1
                if token.id in t2tf_alignments:
                    s = t2tf_alignments[token.id].get_property('start')
                    e = t2tf_alignments[token.id].get_property('end')
                    # self.logger.debug(f'found token {token.id} aligned to {s} - {e}')
                # just in case gentle (kaldi) removed the first token during alignment 
                # (happens with some stopwords and symbols)
                if not in_segment and (token_from_pred.lower() == ref_segment_text[0].lower()
                                       or token_from_pred.lower() == ref_segment_text[1].lower()):
                    in_segment = True
                    start = s / 1000 if timeunit.startswith('mill') else s
                elif in_segment and \
                    token_from_pred.lower() == ref_segment_text[-1].lower() or token_from_pred.lower() == "".join(ref_segment_text[-2:]).lower():  # stargazing vs. star gazing
                    end = e / 1000 if timeunit.startswith('mill') else e
                    pred[Segment(start, end)] = ' '.join(ref_segment_text)
                    try:
                        ref_segment_text = self.normalize_cadet_tokens(next(ref_segs)[2])
                    except StopIteration:
                        break
                    in_segment = False
            self.logger.debug(f'system token iteration is done , last timeframe {start}, {e}')
            end = e / 1000 if timeunit.startswith('mill') else e
            pred[Segment(start, end)] = ' '.join(ref_segment_text)
        return pred, reference

    def _compare_pair(self, guid, reference: Any, hypothesis: Any) -> Any:
        
        # krim: used to use more metrics in the past, but I think only 
        # segmentation-based metrics are relevant. Also, for p/r metrics, 
        # since they are based on segment boundaries, the scores are hard 
        # to interpret without a clear definition of what a "near miss" is.
        # (implemented as "tolerance" parameter)
        
        # coverage = DiarizationCoverage()
        # purity = DiarizationPurity()
        scoverage = SegmentationCoverage()
        spurity = SegmentationPurity()
        # precision = SegmentationPrecision()
        # recall = SegmentationRecall()

        if len(hypothesis) == 0:
            self.logger.warning(f'{guid} :: no hypothesis found')
            return []
        if len(reference) != len(hypothesis):
            self.logger.warning(
                f'{guid} :: reference ({len(reference)}) and hypothesis ({len(hypothesis)}) have different number of segments')
        try:
            # coverage, purity, f1, precision, recall, f1
            cpfprf = []
            for met in scoverage, spurity:
                comps = met.compute_components(reference, hypothesis)
                cpfprf.append(met.compute_metric(comps))
            cpfprf.append(pyannote.metrics.base.f_measure(cpfprf[-2], cpfprf[-1]))
            return cpfprf
        except KeyError:
            print(f"Error: Issue with keys in results for file {guid}")
            
    def _compare_all(self, golds, preds) -> Any:
        raise NotImplementedError("Comparing all golds and preds is not implemented. ")

    def _finalize_results(self):
        """
        Aggregate the results from all files and calculate the average
        The results should be a dict from guid to a list of results which 
        is the output from the _compare method.
        """
        cols = 'GUID segmentation-coverage segmentation-purity S-C-P-F1'.split()
        for threshold in self.thresholds:  # self.thresholds will always be empty (leave here for historical reason)
            cols.extend(f'Precision@{threshold} Recall@{threshold} P-R-F1@{threshold}-sec-tolerance'.split())
        data = []
        for guid, results in self._calculations.items():
            if not results:
                continue
            data.append([guid] + results)
        data = pd.DataFrame(data, columns=cols)
        res_str = (f'Individual file results:\n{data.to_string(index=False)}\n\n\n'
                   f'Average results:\n{data.loc[:, data.columns != "GUID"].mean(axis=0).to_frame().T.to_string(index=False)}\n\n\n')
        self._results = res_str


if __name__ == "__main__":
    parser = ForcedAlignmentEvaluator.prep_argparser()
    args = parser.parse_args()
    
    evaluator = ForcedAlignmentEvaluator(batchname=args.batchname, gold_loc=args.golds, pred_loc=args.preds)
    evaluator.thresholds = [] if 'thresholds' not in args or not args.thresholds else [float(t) for t in args.thresholds.split(',')]
    evaluator.calculate_metrics(by_guid=True)
    report = evaluator.write_report()
    args.export.write(report.getvalue())
