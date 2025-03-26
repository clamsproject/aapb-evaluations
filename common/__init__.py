"""
Provides common classes and functions for writing new evaluations for CLAMS 
apps. Mainly, 

1. This abstract base class and subclasses for writing the new evaluation 
code for various evaluation tasks/scenarios.

2. `write_report` method to create a markdown report file for the 
evaluation with skeleton template.

Moving forward, common accuracy metrics from known libraries will be 
included here via `metrics.py` modules. 
"""
import argparse
import bisect
import datetime
import io
import json
import logging
import os
import sys
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union, Iterable, Any, Tuple

from clams_utils.aapb import guidhandler, goldretriever

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s %(name)s %(levelname)-8s %(thread)d %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S")

# this might be too "magic", but as a fallback option for no internet connection
# read local directory if LOCAL_AAPB_ANNOTATIONS is set
local_aaapb_annotations = None
if 'LOCAL_AAPB_ANNOTATIONS' in os.environ:
    local_aaapb_annotations = Path(os.environ['LOCAL_AAPB_ANNOTATIONS'])
    # validate that it exists and a dir 
    if not local_aaapb_annotations.is_dir():
        raise FileNotFoundError(
            f"Cannot access `aapb-annotations` locally. If you intend to use online files, unset the `LOCAL_AAPB_ANNOTATIONS` environment variable.")


class ClamsAAPBEvaluationTask(ABC):

    def __init__(self, batchname: str):
        """
        Initialize the evaluation task with a batch name. A "batch" is a 
        collection of AAPB GUIDs that are used for evaluation. The batch
        name can be found in the aapb-annotations repository. (see 
        `batches` directory in the repository)
        """
        self._taskname = Path(__file__).parent.name  # use the name of the directory as the name
        self.pairs = {}  # guid: [gold, pred] pairs
        if batchname is not None:
            self.set_guids_from_batchname(batchname)
        self.logger = logging.getLogger(self._taskname)
        self._results = None
        self._calculations = None

    @property
    def taskname(self) -> str:
        """
        The name of the evaluation task.
        """
        return self._taskname

    @property
    def results(self) -> Union[dict, str]:
        """
        The results of the evaluation task. This could be a dictionary of 
        metrics or a string of human-readable report for serialization 
        into the report file.
        """
        return self._results
    
    @results.setter
    def results(self, value):
        self._results = value

    def set_guids_from_batchname(self, batchname: str, aapb_ann_commit='main'):
        """
        Set the list of GUIDs from a batch name, for convenience.
        Batch names are available in aapb-annotations repo. 
        """
        if 'LOCAL_AAPB_ANNOTATIONS' in os.environ:
            all_batches = local_aaapb_annotations / 'batches'
        else:
            all_batches = Path(goldretriever.download_golds(
                f'https://github.com/clamsproject/aapb-annotations/tree/{aapb_ann_commit}/batches'))
        guids = []
        batch_file = all_batches / f'{batchname}.txt'
        with open(batch_file, 'r') as f:
            for line in f:
                if line.startswith('#'):
                    continue
                guid = line.strip()
                bisect.insort(guids, guid)
        for guid in guids:
            self.pairs[guid] = [None, None]

    @staticmethod
    def prep_argparser():
        """
        Prepares the argument parser for the evaluation task. The default
        arguments are defined in this super class. 
        """
        parser = argparse.ArgumentParser()  # TODO (krim @ 3/23/25): auto-generate description from docstring when inheriting
        parser.add_argument('-p', '--preds', type=str, help='directory containing prediction files (MMIF)')
        parser.add_argument('-g', '--golds', type=str, help='directory containing gold files (non-MMIF)')
        parser.add_argument('-e', '--export', help='filename to export the results/report (default to stdout)',
                            type=argparse.FileType('w'), nargs='?', default=sys.stdout)
        parser.add_argument('-b', '--batchname', type=str, help='Batch name (set of AAPB GUIDs) for the task')
        parser.add_argument('--source-directory', nargs='?',
                            help="directory that contains original source files without annotations. Only use when information only in the source is needed for calculating evaluation metrics.",
                            default=None)
        return parser

    def get_gold_files(self, gold_uri: str) -> Iterable[Union[str, Path]]:
        """
        Read files under the gold "directory". If the directory location 
        is given as a URL (http, https, ftp, etc.), download the files 
        under the remote directory to a temporary location and return the
        list of file paths.
        """
        # a URL to a directory containing gold files look like this 
        # "https://github.com/clamsproject/aapb-annotations/tree/main/newshour-transcript-sync/221101-aapb-collaboration-21"
        # TODO (krim @ 3/24/25): should we support falling back to LOCAL_AAPB_ANNOTATIONS var for no internet connection?
        # even though this method already supports `file://` scheme? 
        if gold_uri.startswith(('http://', 'https://')):  # maybe ftp:// too?
            gold_dir = Path(goldretriever.download_golds(gold_uri))
        elif gold_uri.startswith('file://'):
            gold_dir = Path(gold_uri.replace('file://', ''))
        else:
            gold_dir = Path(gold_uri)
        if len(self.pairs) == 0:
            # meaning the pairs are not set yet, so read all files
            # and assume all guids in the gold set is the "target" guids
            set_targets = True
        else:
            set_targets = False
        for f in gold_dir.iterdir():
            if not f.is_file():
                continue
            guid = guidhandler.get_aapb_guid_from(f.name)
            if set_targets:
                self.pairs[guid] = [f, None]
            else:
                if guid in self.pairs:
                    self.pairs[guid][0] = f
            
    @abstractmethod
    def _read_gold(self, gold_file: Union[str, Path]) -> Any:
        """
        Read the pred file and return the processed data. The data should be ready for comparing and calculating metrics.
        """
        raise NotImplementedError

    def get_pred_files(self, pred_uri: str) -> Iterable[Union[str, Path]]:
        """
        For now, the only way to pass pred files are through local directories.
        """
        # TODO (krim @ 3/23/25): update when mmif-storage server fully implements search/mmif and retrieval APIs
        pred_dir = Path(pred_uri)
        if len(self.pairs) == 0:
            # meaning either batch wasn't specified or gold files are not 
            # set yet, and can't proceed with just preds
            raise ValueError("Target GUIDs must be set before reading "
                             "prediction files. Use a batch name or "
                             "gold_dir to set the target GUIDs.")
        
        for f in pred_dir.iterdir():
            if not f.is_file():
                continue
            guid = guidhandler.get_aapb_guid_from(f.name)
            if guid in self.pairs:
                self.pairs[guid][1] = f

    @abstractmethod
    def _read_pred(self, pred_file: Union[str, Path], gold) -> Any:
        """
        Read the pred file and return the processed data. The data should be ready for comparing and calculating metrics.
        For some cases, gold data might be needed to process the pred data.
        If not, pass None to the gold argument.
        """
        raise NotImplementedError

    def _read_data_pairs(self) -> Iterable[Tuple[str, Any, Any]]:
        """
        Iterate through the GUIDs and read the corresponding pred and gold files.
        Must be called after golds and preds are set by calling get_[gold|pred]_files methods.

        :return: iterator of (guid, gold, pred) tuples, where gold and pred are essential data ready to compare.
        """
        for guid in self.pairs:
            gold_f, pred_f = self.pairs[guid]
            gold = self._read_gold(gold_f)
            pred = self._read_pred(pred_f, gold)
            yield guid, gold, pred

    @abstractmethod
    def _compare(self, guid: str, gold: Any, pred: Any) -> Any:
        """
        Main calculation of the evaluation metric(s).
        guid string is passed for logging purposes.
        """
        raise NotImplementedError
    
    def calculate_metrics(self, by_guid: bool):
        """
        Match and Compare the entries together. And add results to the results variable.
        """
        if by_guid:
            results = {}
            for guid, gold, pred in self._read_data_pairs():
                a_score = self._compare(guid, gold, pred)
                results[guid] = a_score
        else:
            golds = []
            preds = []
            for guid, gold, pred in self._read_data_pairs():
                golds.append(gold)
                preds.append(pred)
            # passing asterisk to indicate that the comparison is for all guids
            results = self._compare('*', golds, preds)
        self._calculations = results

    @abstractmethod
    def finalize_results(self):
        """
        If any aggregation or finalization is needed, do it here.
        If no such step is needed, just `pass`.
        """
        raise NotImplementedError

    def write_report(self) -> io.StringIO:
        """
        Create a report file using a markdown template. First section of 
        the report should be just a "dumps" of raw calculated results.
        """
        self.finalize_results()
        report = io.StringIO()
        report.write(
            f"# Evaluation Report for `{self.taskname}` task as of {datetime.datetime.now()}\n")  # TODO (krim @ 3/23/25): more human-readable date format
        report.write("## Raw Results\n")
        if isinstance(self.results, dict):
            report.write("```json\n")
            json.dump(self.results, report, indent=2)
            report.write("\n```\n")
        elif isinstance(self.results, str):
            report.write("```\n")
            report.write(self.results)
            report.write("\n```\n")
        else:
            report.write("No results available in a serializable format.\n")
        # TODO (krim @ 3/23/25): and continue templating the report
        return report
    
