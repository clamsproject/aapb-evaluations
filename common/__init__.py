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

import pandas as pd
from clams_utils.aapb import guidhandler, goldretriever
from mmif import Mmif
from mmif.utils import workflow_helper as wfh


logging.basicConfig(
    #level=logging.INFO,
    level=logging.ERROR,
    format="%(asctime)s %(name)s %(levelname)-8s %(thread)d %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S")


EVAL_OTHER_PREFIX = '_eval_other_'

ANNOTATIONS_REPO = 'https://github.com/clamsproject/aapb-annotations'
EVALUATIONS_REPO = 'https://github.com/clamsproject/aapb-evaluations'
ANNOTATION_BATCHES_TREE = f'{ANNOTATIONS_REPO}/tree/main/batches'


# this might be too "magic", but as a fallback option for no internet connection
# read local directory if LOCAL_AAPB_ANNOTATIONS is set
local_aapb_annotations = None
if 'LOCAL_AAPB_ANNOTATIONS' in os.environ:
    local_aapb_annotations = Path(os.environ['LOCAL_AAPB_ANNOTATIONS'])
    # validate that it exists and a dir 
    if not local_aapb_annotations.is_dir():
        raise FileNotFoundError(
            f"Cannot access `aapb-annotations` locally. If you intend to use online "
            "files, unset the `LOCAL_AAPB_ANNOTATIONS` environment variable.")


class ClamsAAPBEvaluationTask(ABC):

    def __init__(
            self,
            batchname: str,
            gold_loc: Union[str, Path] = None,
            pred_loc: Union[str, Path] = None,
            aapb_ann_commit='main',
            **kwargs):
        """
        Initialize the evaluation task with a batch name. A "batch" is a
        collection of AAPB GUIDs that are used for evaluation. The batch
        name can be found in the aapb-annotations repository (see
        ``batches`` directory in the repository).

        :param batchname: Name of the AAPB GUID batch to evaluate.
        :param gold_loc: Path to directory containing gold files.
        :param pred_loc: Path to directory containing prediction MMIFs.
        :param kwargs: Additional options:

            - ``sbs`` (bool): Include a side-by-side view section in the
              report by calling ``write_side_by_side_view()``.
              Default ``False``.
            - ``cf`` (bool): Include a confusion matrix section in the
              report by calling ``write_confusion_matrix()``.
              Default ``False``.

        Subclasses may also set ``self._eval_config`` (a dict) in
        their ``__init__`` to surface task-specific settings (e.g.,
        tolerance thresholds) in the report's "Data and Evaluation
        Specs" section.
        """
        self._taskname = 'NO-TASK' if self.__class__ == ClamsAAPBEvaluationTask else \
            Path(inspect.getfile(self.__class__)).parent.name  # use the name of the directory as the name
        self.logger = logging.getLogger(self._taskname)
        self._batchname = batchname  # store batchname for report generation
        self.pairs = {}  # guid: [gold, pred] pairs
        if batchname is not None:
            self._set_guids_from_batchname(batchname, aapb_ann_commit)

        # read data file paths
        self._gold_loc = gold_loc
        self._pred_loc = pred_loc
        self._get_gold_files(gold_loc)
        #print('>>> read gold files')
        self._get_pred_files(pred_loc)
        #print('>>> read pred files')

        # the primary workflow from the predictions summary
        self._wfsummary = self.validate_pred_mmifs(pred_loc)
        #print('>>> created summary')
        #print(self._wfsummary)
        #print(json.dumps(self._wfsummary, indent=2))
        # variable to store scores for each guid, and overall scores under '*' key
        self._calculations = {}
        # a pandas.DataFrame with the results, populated from the calculations,
        # currently done as the first step when writing the report
        self._results = None
        # decide if "side-by-side" view is needed (e.g., for visualization)
        self._do_sbs = kwargs.get('sbs', False)
        self._do_cf = kwargs.get('cf', False)
        # use a separate variable to store side-by-side results, if needed
        # then use `self._write_side_by_side_view` to "pretty-print" the results

    @staticmethod
    def validate_pred_mmifs(pred_loc):
        collection_summ = wfh.describe_mmif_collection(pred_loc)
        logging.debug(collection_summ)
        # valid preds
        # 1. must have at least one successful MMIF file
        if collection_summ['mmifCountByStatus']['successful'] == 0:
            raise ValueError("No successful MMIF files found in the prediction location.")
        # 2. must be from the same workflow (or at least, we assume the user wants
        #    to evaluate the most frequent one)
        workflows = collection_summ.get('workflows', [])
        if not workflows:
            raise ValueError("No workflow information found in the prediction MMIFs.")

        sorted_workflows = sorted(workflows, key=lambda w: w.get('mmifCount', 0), reverse=True)
        primary_workflow = sorted_workflows[0]
        
        logging.info(f"Primary workflow for evaluation selected: {primary_workflow['workflowId']}")
        logging.info(f"Number of MMIF files from this workflow: {primary_workflow['mmifCount']}")

        if len(sorted_workflows) > 1:
            other_wf_ids = [wf['workflowId'] for wf in sorted_workflows[1:]]
            warnings.warn(f"Multiple workflows found in the prediction set. "
                          f"The primary workflow was chosen for evaluation. "
                          f"Other workflows found: {', '.join(other_wf_ids)}", RuntimeWarning)

        return primary_workflow

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
        Batch names are available in the aapb-annotations repo.
        """
        logging.debug(f'BATCH {batchname}')
        if 'LOCAL_AAPB_ANNOTATIONS' in os.environ:
            all_batches = local_aapb_annotations / 'batches'
            logging.debug('batch files are local')
        else:
            logging.debug('batch files are downloaded from github')
            logging.debug(f'... {ANNOTATIONS_REPO}/tree/{aapb_ann_commit}/batches')
            all_batches = Path(goldretriever.download_batches(
                f'{ANNOTATIONS_REPO}/tree/{aapb_ann_commit}/batches'))
        logging.debug(f'... {all_batches}')
        guids = []
        batch_file = all_batches / f'{batchname}.txt'
        batch_file = all_batches / f'{batchname}'
        for line in batch_file.read_text().splitlines():
            if line.strip() and not line.startswith('#'):
                guids.append(line.strip())
        for guid in sorted(guids):
            # initialize the pairs with None for gold and pred
            self.pairs[guid] = [None, None]

    @classmethod
    def prep_argparser(cls):
        """
        Prepares the argument parser for the evaluation task. The default
        arguments are defined in this super class.
        """
        # basic I/O arguments
        parser = argparse.ArgumentParser(description=cls.__doc__)
        parser.add_argument(
            '-p', '--preds', type=str, required=True,
            help='directory containing prediction files (MMIF)')
        parser.add_argument(
            '-g', '--golds', type=str, required=True,
            help='directory containing gold files (non-MMIF)')
        parser.add_argument(
            '-e', '--export', type=argparse.FileType('w'), nargs='?',
            default=sys.stdout,
            help='filename to export the results/report (default to stdout)')
        parser.add_argument(
            '-b', '--batchname', type=str,
            help='Batch name (set of AAPB GUIDs) for the task')
        parser.add_argument(
            '--source-directory', nargs='?', default=None,
            help='directory that contains original source files without annotations. '
                 'Only use when information only in the source is needed for '
                 'calculating evaluation metrics.')

        # Label mapping arguments (used by classification tasks)
        label_group = parser.add_mutually_exclusive_group()
        label_group.add_argument(
            '--label-map', nargs='+', default=None,
            help='Label mappings for remapping predicted/gold labels before '
                 'evaluation. Use when you want to group multiple labels '
                 'into broader categories (e.g., map "I", "S", "B" to "slate") '
                 'or rename labels. Supports two formats: (1) Identity mapping '
                 '- just list labels to keep them distinct: "I S B"; (2) '
                 'Explicit mapping - use colon notation to remap: "I:slate '
                 'S:slate B:bars". Space-separated arguments only. Target values '
                 'are automatically identity-mapped (e.g., "b:bc c:bc" adds '
                 '"bc:bc"), allowing predictions with pre-collapsed labels. '
                 'Unmapped labels replaced with --default-label value.')
        label_group.add_argument(
            '--label-map-json', type=str, default=None,
            help='Label mapping as JSON string (alternative to --label-map). '
                 'Use this to copy mappings directly from MMIF metadata. '
                 'Format: \'{"IN1": "OUT1", "IN2": "OUT2"}\'. Target values '
                 'are automatically identity-mapped to support pre-collapsed '
                 'prediction labels. Convenient for replicating app '
                 'configuration in evaluation.')
        parser.add_argument(
            '--default-label', type=str, default='-',
            help='Label to use for unmapped entries (default: "-")')

        return parser

    @staticmethod
    def parse_label_map_args(args) -> Optional[dict]:
        """
        Parse label mapping from args and normalize it.

        Normalization adds identity mappings for all target values (e.g., if
        you map "b:bc c:bc", then "bc:bc" is automatically added). This allows
        predictions that already use collapsed labels to be preserved.

        Supports both space-separated and comma-separated formats:
        - Identity mappings: ["eng", "spa", "fre"] → eng:eng, spa:spa, fre:fre
        - Explicit mappings: ["eng:english", "spa:spanish"]
        - Mixed: ["eng", "spa", "kor:asian", "jpn:asian"]

        :param args: Parsed argparse namespace
        :return: Label mapping dict (normalized) or None
        :rtype: Optional[dict]
        """
        label_map = None

        if args.label_map_json:
            label_map = json.loads(args.label_map_json)
        elif args.label_map:
            label_map = {}
            for mapping in args.label_map:
                mapping = mapping.strip()
                if ':' in mapping:
                    # Explicit mapping: IN:OUT
                    in_label, out_label = mapping.split(':', 1)
                    label_map[in_label.strip()] = out_label.strip()
                else:
                    # Identity mapping: IN → IN:IN
                    label = mapping.strip()
                    if label:  # ignore empty strings
                        label_map[label] = label

        # Normalize: add identity mappings for target values
        if label_map:
            target_values = set(label_map.values())
            for target in target_values:
                if target not in label_map:
                    label_map[target] = target

        return label_map

    def _get_gold_files(self, gold_uri: str) -> Iterable[Union[str, Path]]:
        """
        Read files under the gold directory. For now, the only way to pass gold
        files is via local directories.
        """
        # Previously: If the directory location is given as a URL (http, https, ftp, etc.),
        # download the files under the remote directory to a temporary location
        # and return the list of file paths.
        # a URL to a directory containing gold files look like this 
        # "https://github.com/clamsproject/aapb-annotations/tree/main/newshour-transcript-sync/221101-aapb-collaboration-21"
        # TODO (krim @ 3/24/25): should we support falling back to LOCAL_AAPB_ANNOTATIONS
        # var for no internet connection?
        # even though this method already supports `file://` scheme?

        # goldretriever functionality disabled until gold annotation repo is made fully available
        if gold_uri.startswith(('http://', 'https://')):  # maybe ftp:// too?
            logging.debug('downloading golds from GitHub')
            gold_dir = Path(goldretriever.download_golds(gold_uri))
            logging.debug('... {gold_uri}')
            logging.debug('... {gold_dir}')
        # as with _get_pred_files, the system will throw an error if it's anything besides a valid path
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
        Read a prediction file and return processed data ready for
        metric calculation by ``_compare_pair`` or ``_compare_all``.

        Must return a tuple ``(pred, updated_gold)``. The ``gold``
        parameter is the output of ``_read_gold`` for the same GUID.
        When your implementation needs to transform or align the gold
        data based on prediction structure (e.g., aligning label lists
        by timestamp matching, or padding dummy tokens to match data
        size), return the updated gold as the second element — it will
        replace the original gold passed to ``_compare_pair``. Return
        ``None`` as the second element if gold needs no modification.
        """
        raise NotImplementedError

    def _read_data_pairs(self) -> Iterable[Tuple[str, Any, Any]]:
        """
        Iterate through the GUIDs and read the corresponding pred and gold files.
        Must be called after golds and preds are collected in the pairs variable
        with get_gold_files() and get_pred_files().

        :return: iterator of (guid, gold, pred) tuples, where gold and pred are
        essential data ready to be compared.
        """
        for guid in self.pairs:
            gold_f, pred_f = self.pairs[guid]
            # Allow for the case where the gold file is None (this used to raise
            # errors for some tasks).
            gold = gold_f if gold_f is None else self._read_gold(gold_f)
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
                        RuntimeWarning)
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
        Calculate metrics for each gold-pred pair for a guid and add them to the
        _calculations dictionary.
        """
        data_pairs = self._read_data_pairs()
        if by_guid:
            for guid, gold, pred in data_pairs:
                #print(f'[{guid}] {len(gold)} {pred}')
                if gold is None:
                    self.logger.warning(
                        f"Skipping evaluation for {guid} due to missing gold data.")
                    continue
                elif pred is None:
                    if self.pairs[guid][1] is not None:
                        # file is there, but no data was read for any reason
                        # (e.g., missing target annotations)
                        self._calculations[guid] = None
                    else:
                        # no prediction file was found for the guid, so skip
                        continue
                else:
                    self._calculations[guid] = self._compare_pair(guid, gold, pred)
        else:
            # This will fail since _compare_all() is not implemented.
            golds = []
            preds = []
            for guid, gold, pred in data_pairs:
                if pred is not None:  # when no match found, pred is None
                    golds.append(gold)
                    preds.append(pred)
            # passing asterisk to indicate that the comparison is for all guids
            self._calculations['*'] = self._compare_all(golds, preds)

        self._finalize_results()

    @abstractmethod
    def _finalize_results(self):
        """
        Aggregate per-GUID scores from ``self._calculations`` and
        store the final output in ``self._results``. Called
        automatically by ``write_report()`` before rendering.

        ``self._calculations`` is a dict keyed by GUID, populated by
        ``_compare_pair`` during ``calculate_metrics(by_guid=True)``.
        A value of ``False`` indicates a GUID whose prediction file
        existed but could not be read.

        The type of ``self._results`` determines how the "Raw Results"
        section of the report is rendered:

        - ``pd.DataFrame``: Rendered as CSV and a Markdown table.
        - ``dict``: Rendered as JSON.
        - ``str``: Rendered as a plain code block.
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

    def print_pairs(self):
        """Debugging method."""
        print()
        for guid in sorted(self.pairs):
            print(f'[{guid}]')
            print(f'    {self.pairs[guid][0]}')
            print(f'    {self.pairs[guid][1]}')
        print()

    def save_results(self, directory=None):
        """Currently for debugging, but eventually intended for writing evaluation
        data to json files, which can then be used to display various kinds of
        results to the shack. Could also be used as input to the report writing."""
        directory = Path(os.getcwd() if directory is None else directory)
        with open(directory / 'eval-wfsummary.json', 'w') as fh:
            fh.write(json.dumps(self._wfsummary, indent=2))
        with open(directory / 'eval-calculations.json', 'w') as fh:
            for guid, val in self._calculations.items():
                fh.write(f'{guid}  -->  {val}\n')
        with open(directory / 'eval-results.json', 'w') as fh:
            fh.write(str(self._results))
            #fh.write(json.dumps(self._results.to_dict(), indent=2))
        with open(directory / 'eval-report-long.md', 'w') as fh:
            fh.write(self.write_report().getvalue())
        with open(directory / 'eval-report-short.md', 'w') as fh:
            fh.write(self.write_short_report().getvalue())


    def write_report(self) -> io.StringIO:
        """
        Create a Markdown report from evaluation results. Calls
        ``_finalize_results()`` first, then renders a template that
        includes: evaluation method (class docstring), data specs,
        workflow specs, raw results, and optional sections.

        The "Raw Results" format depends on the type of
        ``self._results`` — see ``_finalize_results`` docstring.

        When ``self._do_cf`` is truthy, appends a confusion matrix
        via ``write_confusion_matrix()``. When ``self._do_sbs`` is
        truthy, appends a side-by-side view via
        ``write_side_by_side_view()``.

        If ``self.label_map`` is set, the mapping is included in the
        "Data and Evaluation Specs" section. If ``self._eval_config``
        (a dict) is set, each key-value pair is rendered as an
        additional bullet in the same section.

        :return: Report contents.
        :rtype: io.StringIO
        """
        #self._finalize_results()
        report = io.StringIO()
        report.write(f"# Evaluation Report for `{self.taskname}` task as of {datetime.datetime.now()}\n\n")
        report.write(f"## Evaluation method\n{inspect.cleandoc(self.__doc__)}\n")

        # Build batch name info with link to aapb-annotations
        batch_info = self._get_batch_info()

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

        report.write(f"\n## Data and Evaluation Specs\n"
                     f"- Batch name: HOPPA {batch_info}\n"
                     f"- Groundtruth data location: {self._gold_loc}\n"
                     # f"- System prediction (MMIF) location: {self._pred_loc}\n"  # expose local file paths, is it ok?
                     f"- Evaluation code version: {code_version_info}\n")

        # Add evaluation configuration if label mapping is used
        eval_configs = False
        if hasattr(self, 'label_map') and self.label_map:
            eval_configs = True
            report.write("- Label mapping:\n")
            for key, val in self.label_map.items():
                report.write(f"  - `{key}` : `{val}`\n")
            if hasattr(self, 'default_label'):
                report.write(f"- Default label for unmapped entries: `{self.default_label}`\n")

        # Add other evaluation-time configurations
        if hasattr(self, '_eval_config') and self._eval_config:
            eval_configs = True
            for config_name, config_value in self._eval_config.items():
                report.write(f"- {config_name}: {config_value}\n")
        # just for formatting
        if eval_configs:
            report.write("\n")

        report.write(f"\n## Workflow Specs\n")
        report.write(f"- Workflow ID: `{self._wfsummary.get('workflowId', 'N/A')}`\n")
        report.write(f"- MMIFs in workflow: {self._wfsummary.get('mmifCount', 'N/A')}\n")

        self._write_app_info(report)

        report.write(f"\n## Raw Results\n")
        if isinstance(self.results, dict):
            report.write("```json\n")
            json.dump(self.results, report, indent=2)
            report.write("\n```\n")
        elif isinstance(self.results, str):
            report.write("```\n")
            report.write(self.results)
            report.write("\n```\n")
        elif isinstance(self.results, pd.DataFrame):
            report.write("```\n")
            report.write(self.results.to_csv(index=False, sep=',', header=True))
            report.write("\n```\n")
            report.write(f"\n## Table view\n")
            report.write(self.results.to_markdown(index=True))
            report.write("\n")
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


    def write_short_report(self) -> io.StringIO:
        """
        Create a Markdown report from evaluation results including data specs,
        workflow specs, raw results, and optional sections.

        The "Raw Results" format depends on the type of
        ``self._results`` — see ``_finalize_results`` docstring.

        When ``self._do_cf`` is truthy, appends a confusion matrix
        via ``write_confusion_matrix()``. When ``self._do_sbs`` is
        truthy, appends a side-by-side view via
        ``write_side_by_side_view()``.

        If ``self.label_map`` is set, the mapping is included in the
        "Data and Evaluation Specs" section. If ``self._eval_config``
        (a dict) is set, each key-value pair is rendered as an
        additional bullet in the same section.

        This is meant to be used in the ClamShack which displays the report
        using the markdown in the rich module, which benefits from a simpler
        markdown.

        :return: Report contents.
        :rtype: io.StringIO
        """

        report = io.StringIO()

        batch_info = self._get_batch_info()

        # Get code version and build link to aapb-evaluations
        code_version = self._get_code_version()
        code_version_info = self._get_code_version_info(code_version)

        report.write('\n### Data and Evaluation Specs\n\n')
        report.write('| property                 | value |\n')
        report.write('| ------------------------ | ----- |\n')
        report.write(f'| timestamp               | {datetime.datetime.now()} |\n')
        report.write(f'| task                    | {self.taskname} |\n')
        report.write(f'| batch                   | {batch_info} |\n')
        report.write(f'| Gold data location      | {self._gold_loc} |\n')
        report.write(f'| Evaluation code version | {code_version_info} |\n')

        # Add other evaluation-time configurations to the table
        if hasattr(self, '_eval_config') and self._eval_config:
            for config_name, config_value in self._eval_config.items():
                #report.write(f"- {config_name}: {config_value}\n")
                report.write(f'| {config_name} | {config_value} |\n')
        report.write("\n")

        # Add evaluation configuration if label mapping is used
        eval_configs = False
        if hasattr(self, 'label_map') and self.label_map:
            eval_configs = True
            report.write("- Label mapping:\n")
            # TODO: this needs to be written to the table instead
            # TODO: write this to a separate table
            for key, val in self.label_map.items():
                report.write(f"  - `{key}` : `{val}`\n")
            if hasattr(self, 'default_label'):
                report.write(f"- Default label for unmapped entries: `{self.default_label}`\n")

        workflow_id = self._wfsummary.get('workflowId', 'N/A')
        mmif_count = self._wfsummary.get('mmifCount', 'N/A')
        report.write('\n### Workflow Specs\n\n')
        report.write('| property                 | value |\n')
        report.write('| ------------------------ | ----- |\n')
        report.write(f'| Workflow ID             | {workflow_id} |\n')
        report.write(f'| MMIFs in workflow:      | {mmif_count}  |\n')
        for app_info in self._wfsummary.get('apps', []):
            report.write(f"| app | {app_info.get('app')} |\n")

        # Write the results, but do not print the oo info for the short report.
        # self._write_app_info(report)
        self._write_results(report)

        return report


    def _get_batch_info(self) -> str:
        """Return batch name info with link to aapb-annotations."""
        if self._batchname:
            batch_url = f"{ANNOTATION_BATCHES_TREE}/{self._batchname}"
            batch_info = f"[{self._batchname}]({batch_url})"
        else:
            guids = sorted(self.pairs.keys())
            batch_info = f"unspecified (GUIDs: {', '.join(guids)})"
        return batch_info


    def _get_code_version_info(self, code_version: str) -> str:
        #if code_version not in ('dirty', ) and not code_version.startswith('unknown'):
        if code_version in ('dirty', ) or code_version.startswith('unknown'):
            # Get relative path of eval file from repo root
            eval_file = Path(inspect.getfile(self.__class__))
            try:
                result = subprocess.run(
                    ['git', 'rev-parse', '--show-toplevel'],
                    capture_output=True, text=True, cwd=eval_file.parent)
                if result.returncode == 0:
                    repo_root = Path(result.stdout.strip())
                    rel_path = eval_file.relative_to(repo_root)
                    code_url = f"{EVALUATIONS_REPO}/blob/{code_version}/{rel_path}"
                    code_version_info = f"[{code_version}]({code_url})"
                else:
                    code_version_info = code_version
            except Exception:
                code_version_info = code_version
        else:
            code_version_info = code_version
        return code_version_info


    def _write_app_info(self, report):
        for app_info in self._wfsummary.get('apps', []):
            report.write(f"#### {app_info.get('app')}\n\n")
            report.write("Configuration\n\n```json\n")
            json.dump(app_info.get('appConfiguration', {}), report, indent=2)
            report.write("\n```\n\n")
            report.write("Profiling\n\n```json\n")
            json.dump(app_info.get('appProfiling', {}), report, indent=2)
            report.write("\n```\n\n")


    def _write_results(self, report):
        report.write(f"\n### Results\n")
        # Results are always a DataFrame so not sure why the first two are there,
        # maybe this is because it is a DataFrame only for TimePointLabeling
        if isinstance(self.results, dict):
            report.write("```json\n")
            json.dump(self.results, report, indent=2)
            report.write("\n```\n")
        elif isinstance(self.results, str):
            report.write("```\n")
            report.write(self.results)
            report.write("\n```\n")
        elif isinstance(self.results, pd.DataFrame):
            # CSV
            report.write("```\n")
            report.write(self.results.to_csv(index=False, sep=',', header=True))
            report.write("\n```\n\n")
            # str
            report.write("```\n")
            report.write(str(self.results))
            report.write("\n```\n\n")
            # table view, has problems with the underscores
            report.write(self.results.to_markdown(index=True))
            report.write("\n")
        else:
            report.write("No results available in a serializable format.\n")
        if self._do_sbs:
            report.write(f"\nSide-by-side view\n")
            # TODO (krim @ 3/23/25): add side-by-side view of the results
            report.write(self.write_side_by_side_view())
        # TODO (krim @ 3/23/25): and continue templating the report
        if self._do_cf:
            report.write(f"\nConfusion Matrix\n\n")
            report.write(self.write_confusion_matrix())
