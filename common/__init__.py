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
import inspect
import io
import json
import logging
import os
import subprocess
import sys
import traceback
import warnings
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union, Iterable, Any, Tuple, Optional, List

from clams_utils.aapb import guidhandler, goldretriever
from mmif import Mmif
from mmif.utils import workflow_helper as wfh

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)-8s %(thread)d %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S")

# this might be too "magic", but as a fallback option for no internet connection
# read local directory if LOCAL_AAPB_ANNOTATIONS is set
local_aapb_annotations = None
if 'LOCAL_AAPB_ANNOTATIONS' in os.environ:
    local_aapb_annotations = Path(os.environ['LOCAL_AAPB_ANNOTATIONS'])
    # validate that it exists and a dir 
    if not local_aapb_annotations.is_dir():
        raise FileNotFoundError(
            f"Cannot access `aapb-annotations` locally. If you intend to use online files, unset the `LOCAL_AAPB_ANNOTATIONS` environment variable.")


class ClamsAAPBEvaluationTask(ABC):

    def __init__(self, batchname: str, gold_loc: Union[str, Path] = None, pred_loc: Union[str, Path] = None, **kwargs):
        """
        Initialize the evaluation task with a batch name. A "batch" is a 
        collection of AAPB GUIDs that are used for evaluation. The batch
        name can be found in the aapb-annotations repository. (see 
        `batches` directory in the repository)
        """
        self._taskname = 'NO-TASK' if self.__class__ == ClamsAAPBEvaluationTask else \
            Path(inspect.getfile(self.__class__)).parent.name  # use the name of the directory as the name
        self.logger = logging.getLogger(self._taskname)
        self._batchname = batchname  # store batchname for report generation
        self.pairs = {}  # guid: [gold, pred] pairs
        if batchname is not None:
            self._set_guids_from_batchname(batchname)

        # read data file paths
        self._gold_loc = gold_loc
        self._pred_loc = pred_loc
        self._get_gold_files(gold_loc)
        self._get_pred_files(pred_loc)
        self._wfid, self._wfprofilings = self.validate_pred_mmifs(pred_loc)
        self._results = None
        # variable to store scores for each guid, and overall scores under '*' key
        self._calculations = {}
        # decide if "side-by-side" view is needed (e.g., for visualization)
        self._do_sbs = kwargs.get('sbs', False)
        self._do_cf = kwargs.get('cf', False)
        # use a separate variable to store side-by-side results, if needed
        # then use `self._write_side_by_side_view` to "pretty-print" the results

    @staticmethod
    def validate_pred_mmifs(pred_loc):
        collection_summ = wfh.describe_mmif_collection(pred_loc)
        # valid preds
        # 1. must be from the same workflow
        # 2. must have at least one MMIF file with annotations (no empty MMIFs)
        workflows = collection_summ['mmifCountByWorkflow']
        if len(workflows) == 0:
            raise ValueError("No valid MMIF files found in the prediction location.")
        # TODO (krim @ 2025-11-27): eventually we need better support from the wfh implementation
        # to handle multiple workflows in the same collection properly
        # for example, the "mmifCountByWorkflow" should not count empty or error MMIFs
        else:
            # but for now...
            # pick the most frequent workflow from the workflows dict
            wfid = max(workflows, key=lambda k: workflows[k])
            logging.info(f"Prediction MMIFs are from workflow {wfid}.")
            mmif_num = workflows[wfid]
            logging.info(f"Number of MMIF files from workflow {wfid}: {mmif_num}.")
            if mmif_num == 0:
                raise ValueError(f"Prediction MMIFs for workflow {wfid} contain no annotations.")
        return wfid, collection_summ['appProfilings']

    @property
    def taskname(self) -> str:
        """
        The name of the evaluation task. Should be automatically set from 
        the directory name, and stay read-only. 
        """
        return self._taskname
    
    @property
    def results(self) -> Union[dict, str]:
        """
        The results of the evaluation task, after `calculate_metrics` is 
        called. The value could be a dictionary of metrics or a string of 
        human-readable report for serialization into the report file.
        """
        return self._results
    
    @results.setter
    def results(self, value):
        self._results = value

    def _set_guids_from_batchname(self, batchname: str, aapb_ann_commit='main'):
        """
        Set the list of GUIDs from a batch name, for convenience.
        Batch names are available in aapb-annotations repo. 
        """
        if 'LOCAL_AAPB_ANNOTATIONS' in os.environ:
            all_batches = local_aapb_annotations / 'batches'
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
            # initialize the pairs with None for gold and pred
            self.pairs[guid] = [None, None]

    @classmethod
    def prep_argparser(cls):
        """
        Prepares the argument parser for the evaluation task. The default
        arguments are defined in this super class. 
        """
        parser = argparse.ArgumentParser(description=cls.__doc__)
        parser.add_argument('-p', '--preds', type=str, required=True, help='directory containing prediction files (MMIF)')
        parser.add_argument('-g', '--golds', type=str, required=True, help='directory containing gold files (non-MMIF)')
        parser.add_argument('-e', '--export', help='filename to export the results/report (default to stdout)',
                            type=argparse.FileType('w'), nargs='?', default=sys.stdout)
        parser.add_argument('-b', '--batchname', type=str, help='Batch name (set of AAPB GUIDs) for the task')
        parser.add_argument('--source-directory', nargs='?',
                            help='directory that contains original source files without annotations. Only use when information only in the source is needed for calculating evaluation metrics.',
                            default=None)
        return parser

    def _get_gold_files(self, gold_uri: str) -> Iterable[Union[str, Path]]:
        """
        Read files under the gold directory. For now, the only way to pass gold files is via local directories.
        """
        # Previously: If the directory location is given as a URL (http, https, ftp, etc.),
        # download the files under the remote directory to a temporary location
        # and return the list of file paths.
        # a URL to a directory containing gold files look like this 
        # "https://github.com/clamsproject/aapb-annotations/tree/main/newshour-transcript-sync/221101-aapb-collaboration-21"
        # TODO (krim @ 3/24/25): should we support falling back to LOCAL_AAPB_ANNOTATIONS var for no internet connection?
        # even though this method already supports `file://` scheme?

        # goldretriever functionality disabled until gold annotation repo is made fully available
        # if gold_uri.startswith(('http://', 'https://')):  # maybe ftp:// too?
        #     gold_dir = Path(goldretriever.download_golds(gold_uri))
        # as with _get_pred_files, the system will throw an error if it's anything besides a valid path
        if gold_uri.startswith('file://'):
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
            if guid is None:
                self.logger.warning(f"Skipping file {f.name} as it does not have a valid AAPB GUID.")
            elif set_targets:
                # set "setting" mode, each entry needs to be initialized from [None, None]
                self.pairs[guid] = [f, None]
            else:
                # if not in setting mode, ignore GUID that's not already "set"
                if guid in self.pairs:
                    self.pairs[guid][0] = f
            
    @abstractmethod
    def _read_gold(self, gold_file: Union[str, Path], **kwargs) -> Any:
        """
        Read the pred file and return the processed data. The data should 
        be ready for comparing and calculating metrics by `_compareXXX` 
        methods. 
        """
        raise NotImplementedError

    def _get_pred_files(self, pred_uri: str) -> Iterable[Union[str, Path]]:
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
        

        matched = 0
        for f in pred_dir.iterdir():
            if not f.is_file():
                continue
            guid = guidhandler.get_aapb_guid_from(f.name)
            if guid is not None and guid in self.pairs:
                self.logger.debug(f'found a pair to include in the evaluation: {guid}')
                matched += 1
                self.pairs[guid][1] = f
        self.logger.debug(f'#gold instances: {len(self.pairs)}, #matched instances: {matched}')

    @abstractmethod
    def _read_pred(self, pred_file: Union[str, Path], gold: Optional[Any], **kwargs) -> Tuple[Any, Optional[Any]]:
        """
        Read the pred file and return the processed data. The data should 
        be ready for comparing and calculating metrics. For some cases, 
        gold data might be needed to process the pred data, or gold data
        might need to be updated based on the pred data (e.g., pad dummy 
        tokens to match data size). If gold data is not needed in this 
        process, just pass None. 
        The method must return a tuple of (pred, gold) data. When the 
        passed gold data is just None, return None for the second element.
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
            if pred_f is not None:
                try:
                    pred, new_gold = self._read_pred(pred_f, gold)
                    if new_gold is not None:
                        gold = new_gold
                except Exception as e:
                    tb = traceback.format_exc()
                    warnings.warn(
                        f"Error reading pred file {pred_f}:\n"
                        f"Exception type: {type(e).__name__}\n"
                        f"Error message: {e}\n"
                        f"Traceback:\n{tb}",
                        RuntimeWarning
                    )
                    pred = None
            else:
                pred = None
            yield guid, gold, pred

    @abstractmethod
    def _compare_pair(self, guid: str, gold: Any, pred: Any) -> Any:
        """
        Main calculation of the evaluation metric(s) for a pair of 
        gold and pred instances, a.k.a. per-guid evaluation.
        guid string is passed for logging purposes, and the returned value
        will be stored under the guid key in the ``self._calculations``.
        """
        raise NotImplementedError
    
    @abstractmethod
    def _compare_all(self, golds, preds) -> Any:
        """
        Main calculation of the evaluation metric(s) for the entire set of
        gold and pred instances. The returned value will be stored under 
        ``*`` key in the ``self._calculations``.
        """
        raise NotImplementedError
    
    def calculate_metrics(self, by_guid: bool):
        """
        Match and Compare the entries together. And add results to the 
        results attribute.
        """
        if by_guid:
            for guid, gold, pred in self._read_data_pairs():
                if gold is None:
                    warnings.warn(f"Skipping evaluation for {guid} due to missing gold data.", RuntimeWarning)
                    continue
                elif pred is None:
                    if self.pairs[guid][1] is not None:
                        # meaning file is there, but no data was read for any reason (e.g., missing target annotations)
                        self._calculations[guid] = False
                    else:
                        # meaning no file was found for the guid, so skip
                        continue
                else:
                    self._calculations[guid] = self._compare_pair(guid, gold, pred)
        else:
            golds = []
            preds = []
            for guid, gold, pred in self._read_data_pairs():
                if pred is not None:  # when no match found, pred is None
                    golds.append(gold)
                    preds.append(pred)
            # passing asterisk to indicate that the comparison is for all guids
            self._calculations['*'] = self._compare_all(golds, preds)

    @abstractmethod
    def _finalize_results(self):
        """
        Use this method to aggregate scores from `self._calculations` 
        value and put it in the `self._results` attribute. Note that this 
        method WILL always be called within report generation method, and
        only values from `self._results` will be used. 
        """
        raise NotImplementedError

    @abstractmethod
    def write_confusion_matrix(self):
        """
        Write confusion matrix of the results.
        This method will be called from inside the `write_report` method
        when `self._do_cf` has any non-false value, which is optional. This
        could also be called independently to draw the confusion matrix
        without the full report.
        """
        raise NotImplementedError

    @abstractmethod
    def write_side_by_side_view(self):
        """
        Write side-by-side view of the results.
        This method will be called from inside the `write_report` method 
        when `self._do_sbs` has any non-false value, which is optional. This 
        could also be called independently to write the side-by-side 
        without the full report. 
        """
        raise NotImplementedError

    def _get_code_version(self) -> str:
        """
        Get the version of the evaluation code file. Uses git to determine
        if the file has uncommitted changes. If clean, returns the last
        commit hash for the file; otherwise returns 'dirty'.
        """
        # Get the file path of the subclass (the actual evaluation script)
        eval_file = Path(inspect.getfile(self.__class__))
        try:
            # Check if the file has uncommitted changes
            result = subprocess.run(
                ['git', 'status', '--porcelain', str(eval_file)],
                capture_output=True,
                text=True,
                cwd=eval_file.parent
            )
            if result.returncode != 0:
                return 'unknown (git error)'

            # If there's output, the file has changes (modified, staged, etc.)
            if result.stdout.strip():
                return 'dirty'

            # File is clean, get the last commit hash for this file
            result = subprocess.run(
                ['git', 'log', '-1', '--format=%h', '--', str(eval_file)],
                capture_output=True,
                text=True,
                cwd=eval_file.parent
            )
            if result.returncode != 0 or not result.stdout.strip():
                return 'unknown (no commits)'

            return result.stdout.strip()
        except FileNotFoundError:
            # git command not found
            return 'unknown (git not available)'
        except Exception as e:
            return f'unknown ({e})'

    def write_report(self) -> io.StringIO:
        """
        Create a report file using a markdown template. First section of 
        the report should be just a "dumps" of raw calculated results.
        """
        self._finalize_results()
        report = io.StringIO()
        report.write(f"# Evaluation Report for `{self.taskname}` task as of {datetime.datetime.now()}\n")
        report.write(f"\n## Evaluation method\n{inspect.cleandoc(self.__doc__)}\n")

        # Build batch name info with link to aapb-annotations
        if self._batchname:
            batch_url = f"https://github.com/clamsproject/aapb-annotations/tree/main/batches/{self._batchname}.txt"
            batch_info = f"[{self._batchname}]({batch_url})"
        else:
            guids = sorted(self.pairs.keys())
            batch_info = f"unspecified (GUIDs: {', '.join(guids)})"

        # Get code version and build link to aapb-evaluations
        code_version = self._get_code_version()
        if code_version not in ('dirty', ) and not code_version.startswith('unknown'):
            # Get relative path of eval file from repo root
            eval_file = Path(inspect.getfile(self.__class__))
            try:
                result = subprocess.run(
                    ['git', 'rev-parse', '--show-toplevel'],
                    capture_output=True,
                    text=True,
                    cwd=eval_file.parent
                )
                if result.returncode == 0:
                    repo_root = Path(result.stdout.strip())
                    rel_path = eval_file.relative_to(repo_root)
                    code_url = f"https://github.com/clamsproject/aapb-evaluations/blob/{code_version}/{rel_path}"
                    code_version_info = f"[{code_version}]({code_url})"
                else:
                    code_version_info = code_version
            except Exception:
                code_version_info = code_version
        else:
            code_version_info = code_version

        report.write(f"\n## Data specs\n"
                     f"- Batch name: {batch_info}\n"
                     f"- Groundtruth data location: {self._gold_loc}\n"
                     # f"- System prediction (MMIF) location: {self._pred_loc}\n"  # expose local file paths, is it ok?
                     f"- Evaluation code version: {code_version_info}\n")
        report.write(f"\n## Workflow specs\n")
        report.write(f"- Workflow ID: {self._wfid}\n")
        report.write(f"- Workflow App Profilings:\n")
        report.write("```json\n")
        json.dump(self._wfprofilings, report, indent=2)
        report.write("\n```\n")

        report.write(f"\n## Raw Results\n")
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
        if self._do_sbs:
            report.write(f"\n## Side-by-side view\n")
            # TODO (krim @ 3/23/25): add side-by-side view of the results
            report.write(self.write_side_by_side_view())
        # TODO (krim @ 3/23/25): and continue templating the report
        if self._do_cf:
            report.write(f"\n## Confusion Matrix\n")
            report.write(self.write_confusion_matrix())
        return report
