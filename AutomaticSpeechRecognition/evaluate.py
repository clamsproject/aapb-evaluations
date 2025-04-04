"""

"""
import tempfile
from pathlib import Path
from typing import Any, Union

import pandas as pd
from clams_utils.aapb import goldretriever, newshour_transcript_cleanup
from jiwer import wer
from mmif import Mmif, DocumentTypes

from common import ClamsAAPBEvaluationTask

# constant:
## note that this repository is a private one and the files are not available to the public (due to IP concerns)
## hence using goldretriever to download the gold files WILL NOT work (goldretreiver is only for public repositories)
GOLD_URL = "https://github.com/clamsproject/aapb-collaboration/tree/89b8b123abbd4a9a67c525cc480173b52e0d05f0/21"


class AutomaticSpeechRecognitionEvaluator(ClamsAAPBEvaluationTask):

    def _read_gold(self, gold_file: Union[str, Path]) -> Any:
        return newshour_transcript_cleanup.file_cleaner(str(gold_file))

    def _read_pred(self, pred_file: Union[str, Path], gold) -> Any:
        f = open(pred_file, 'r')
        mmif_str = f.read()
        f.close()
        data = Mmif(mmif_str)
        td_views = data.get_all_views_contain(DocumentTypes.TextDocument)
        if not td_views:
            for view in reversed(data.views):
                if view.has_error():
                    raise Exception("Error in the MMIF file: " + view.get_error().split('\n')[0])
                raise Exception("No TextDocument found in the MMIF file")
        annotation = next(td_views[-1].get_annotations(DocumentTypes.TextDocument))
        text = annotation.text_value

        return text

    def _compare_pair(self, guid: str, gold: Any, pred: Any) -> Any:
        """
        returns WER scores one for cased and another for uncased (ignore case)
        """
        cased_wer = wer(pred, gold)
        uncased_wer = wer(pred.upper(), gold.upper())
        return cased_wer, uncased_wer
    
    def _compare_all(self, golds, preds) -> Any:
        """
        Compare all golds and preds is NOT implemented, hence do not 
        call ``calculate_metrics`` with ``by_guid=False``.
        """
        raise NotImplementedError("Comparing all golds and preds is not implemented. ")

    def finalize_results(self):
        cols = 'GUID WER-cased WER-uncased'.split()

        df = pd.DataFrame(
            [[guid] + list(results) for guid, results in self._calculations.items() if results],
            columns=cols
        )
        # then add the average row
        df.loc[len(df)] = ['Average'] + [df[col].mean() for col in df.columns[1:]]
        self._results = df.to_csv(index=False, sep=',', header=True)


if __name__ == "__main__":
    # get the absolute path of video-file-dir and hypothesis-file-dir
    parser = AutomaticSpeechRecognitionEvaluator.prep_argparser()
    args = parser.parse_args()
    
    evaluator = AutomaticSpeechRecognitionEvaluator(args.batchname)
    evaluator.get_gold_files(args.golds)
    evaluator.get_pred_files(args.preds)
    evaluator.calculate_metrics(by_guid=True)
    report = evaluator.write_report()
    args.export.write(report.getvalue())
