"""Description
This script is to complete evaluation process for the app RFB(role-filler-binding).
Used evaluation metrics include:
    + Intersection Over Union (IOU)
"""

from abc import ABC, abstractmethod
import json
import os
from typing import Dict, Set, Optional, Tuple, Union, List
from collections import defaultdict
from io import StringIO
from argparse import ArgumentParser, Namespace
import logging
import multiprocessing as mp
import time

from thefuzz import fuzz
from mmif import Mmif, AnnotationTypes, View, Annotation
from mmif.utils import video_document_helper as vdh
from clams_utils.aapb import guidhandler, goldretriever
import pandas as pd
import numpy as np

# GOLD_URL = 'https://github.com/clamsproject/aapb-annotations/tree/main/role-filler-binding/golds'
# GOLD_URL = 'https://github.com/clamsproject/aapb-annotations/tree/107-standard-field-names/role-filler-binding/golds'

SWT_APP = 'http://apps.clams.ai/swt-detection/v6.1'
RFB_APP = 'http://apps.clams.ai/role-filler-binder/v1.0'

# --------------------------------------------------------------------
# Functions needed to load predictions made by RFB
# --------------------------------------------------------------------


def csv_string_to_pair(csv_string: str) -> Set[Tuple[str, str]]:
    """
    Convert csv-string to a set of pairs represeted by tuples

    :param: csv_string: the csv-formatted string
    :return: a set of tuples of (role, filler) string
    """
    # Optimize this function since profiling showed it's slow
    if not csv_string.strip():
        return set()
        
    # Use pandas only if we have a substantial amount of data
    if len(csv_string) > 1000 or csv_string.count('\n') > 10:
        return set(pd.read_csv(StringIO(csv_string), index_col=0).fillna('nan').itertuples(index=False, name=None))
    
    # For smaller strings, use a faster direct approach
    result = set()
    for line in csv_string.split('\n'):
        if not line.strip():
            continue
        parts = line.split(',')
        if len(parts) >= 3:  # Ensure we have at least 3 parts: index, role, filler
            role = parts[1].strip()
            filler = ','.join(parts[2:]).strip()  # Rejoin if there were commas in the filler
            result.add((role, filler or 'nan'))
    
    return result


def find_timepoint_in_alignments(annotation, max_depth=5, current_depth=0):
    """
    Recursively search for a TimePoint annotation in the alignment chain.
    
    :param annotation: The annotation to start the search from
    :param max_depth: Maximum recursion depth to prevent infinite loops
    :param current_depth: Current recursion depth
    :return: TimePoint annotation if found, None otherwise
    """
    if current_depth >= max_depth:
        logging.debug(f"Max recursion depth reached for annotation {annotation.id}")
        return None
    
    logging.debug(f"Checking annotation {annotation.id} (type: {annotation.at_type}) at depth {current_depth}")
    
    # Check if this annotation is a TimePoint
    if annotation.at_type == AnnotationTypes.TimePoint:
        logging.debug(f"Found TimePoint directly: {annotation.id}")
        return annotation
    
    # Get all aligned annotations
    # print (annotation)
    # print ("!!!")
    # we need to iterate over the aligned annotations twice
    aligned_anns = list(annotation.get_all_aligned()) 
    logging.debug(f"Found {len(list(aligned_anns))} aligned annotations for {annotation.id}")
    
    # First, check for any direct TimePoints
    for ann in aligned_anns:
        if ann.at_type == AnnotationTypes.TimePoint:
            logging.debug(f"Found direct TimePoint {ann.id} aligned to {annotation.id}")
            return ann
    
    # If no TimePoints found, recursively check aligned annotations
    for ann in aligned_anns:
        logging.debug(f"Recursively checking {ann.id} (type: {ann.at_type})")
        timepoint = find_timepoint_in_alignments(ann, max_depth, current_depth + 1)
        if timepoint:
            logging.debug(f"Found TimePoint {timepoint.id} via {ann.id}")
            return timepoint
    
    logging.debug(f"No TimePoint found for {annotation.id} at depth {current_depth}")
    return None


def load_pred(file: Union[str, os.PathLike]) -> Dict[str, Dict]:
    """
    Load the predicted role-filler pair made by RFB

    :param: file: the file path or name of the RFB MMIF
    :return: a nested dictionary data structure that indexes GUID -> frame_num -> (role, filler)
    """
    guid = guidhandler.get_aapb_guid_from(file)
    logging.debug("Loading prediction data for %s...", guid)
    
    try:
        # Load MMIF file
        t_start = time.time()
        with open(file, encoding='utf-8') as f:
            mmif_json = json.load(f)
        logging.debug(f"File loading time: {time.time() - t_start:.4f} seconds")
        
        # Parse MMIF
        t_start = time.time()
        rfb_mmif = Mmif(mmif_json)
        
        # Get RFB view
        t_start = time.time()
        rfb_view = rfb_mmif.views.get_last_contentful_view()
        
        # Process documents
        t_start = time.time()
        frames_dict = {}
        
        total_docs = 0
        docs_with_timepoints = 0
        
        print ("pre-loop")
        for rfb_td in rfb_view.get_documents():
            total_docs += 1
            # Find TimePoint in the document's alignment chain
            timepoint = find_timepoint_in_alignments(rfb_td)
            print ("post-find_timepoint_in_alignments")
            # Convert timepoint to frame if found
            if timepoint:
                print ("post-timepoint")
                docs_with_timepoints += 1
                # Check if the timeUnit is already 'frame'
                if timepoint.get_property('timeUnit') == 'frame':
                    aligned_frame = timepoint.get_property('timePoint')
                else:
                    aligned_frame = vdh.convert_timepoint(rfb_mmif, timepoint, 'frames')
                frames_dict[aligned_frame] = csv_string_to_pair(rfb_td.text_value)
        
        logging.debug(f"Document processing time: {time.time() - t_start:.4f} seconds")
        percentage = 0 if total_docs == 0 else (docs_with_timepoints/total_docs*100)
        logging.info(f"Processed {total_docs} documents, found timepoints for {docs_with_timepoints} documents ({percentage:.1f}%)")
        
        return {guid: frames_dict}
    except Exception as e:
        logging.error(f"Error loading file {file}: {e}")
        return {guid: {}}

# --------------------------------------------------------------------
# Functions needed to load gold standard data
# --------------------------------------------------------------------


def conll_string_to_set(conll_string: str) -> Set[Tuple[str, str]]:
    """
    Convert pipe-separated key=value string to a set of (key, value) tuples.

    :param conll_string: The input string, e.g., "role1=filler1|role2=filler2"
    :return: A set of tuples, e.g., {("role1", "filler1"), ("role2", "filler2")}
    """
    rf_set = set()
    if not conll_string or pd.isna(conll_string): # Handle empty or NaN strings
        return rf_set
    pairs = conll_string.split('|')
    for pair in pairs:
        if '=' in pair:
            try:
                role, filler = pair.split('=', maxsplit=1)
                # Add stripping to handle potential whitespace
                rf_set.add((role.strip(), filler.strip()))
            except ValueError:
                # Handle cases where split might fail unexpectedly
                logging.warning(f"Could not parse pair: '{pair}' in ANNOTATIONS string: '{conll_string}'")
        elif pair.strip(): # Handle cases where a part might not have '=' like empty strings between ||
             logging.warning(f"Skipping invalid pair (no '='): '{pair}' in ANNOTATIONS string: '{conll_string}'")
    return rf_set


def load_gold(gold_csv: Union[str, os.PathLike]) -> Dict[str, Dict]:
    """
    Load gold-standard csv data for RFB

    Its format looks like:
    GUID | FRAME | SWT-TYPE | SKIPPED | ANNOTATIONS
    -----------------------------------------------
    str  | int   |   str    |  T/F    | pipe-separated key=value string
    """
    guid = guidhandler.get_aapb_guid_from(gold_csv)
    logging.debug("Loading gold-standard data for %s...", guid)
    frames_dict = {}
    
    try:
        df = pd.read_csv(gold_csv)
        # Keep rows with valid annotations
        df = df.dropna(subset=['ANNOTATIONS'])
        logging.debug(f"Loaded gold CSV with {len(df)} valid annotation rows")
    except FileNotFoundError:
        logging.error(f"Gold file not found: {gold_csv}")
        return {guid: {}}
    except Exception as e:
        logging.error(f"Error reading gold CSV {gold_csv}: {e}")
        return {guid: {}}
    
    if len(df) == 0:
        logging.warning(f"No valid annotations found in {gold_csv}")
        return {guid: {}}
    
    # Process each row as a separate frame annotation
    for _, row in df.iterrows():
        if pd.notna(row['ANNOTATIONS']) and row['ANNOTATIONS'] != 'DUPLICATE':
            # Convert frame to int if possible, handling leading zeros
            try:
                frame = int(str(row['FRAME']).lstrip('0')) if pd.notna(row['FRAME']) else 0
            except ValueError:
                frame = 0
                
            # Create a frame span with just this frame
            frame_span = (frame, frame)
            
            # Parse annotations
            annotations = conll_string_to_set(row['ANNOTATIONS'])
            
            if annotations:  # Only add if we have actual annotations
                frames_dict[frame_span] = annotations
                logging.debug(f"Added annotations for frame {frame}: {annotations}")
    
    logging.info(f"Loaded {len(frames_dict)} frame entries for {guid}")
    return {guid: frames_dict}

# --------------------------------------------------------------------
# Class of evaluation metrics
# --------------------------------------------------------------------


class RFBMetrics(ABC):
    """
    The abstract class of evaluation metrics for evaluating a single video run by RFB
    """
    def __init__(self, gold: Dict[str, Dict], pred: Dict[str, Dict]) -> None:
        self.gold = gold
        self.pred = pred
        self.frame_score: Dict[int, Tuple] = {}

        # Check if the gold and pred data refer to the same video
        if list(self.gold.keys())[0] != list(self.pred.keys())[0]:
            raise ValueError('The prediction file and the gold file refer to different video.')

        # Find intersected frames between pred and gold
        self.guid = next(iter(self.pred.keys()))
        self.frames = self._align_frames_between(self.pred, self.gold)

    def _align_frames_between(self,
                              pred: Dict[str, Dict[int, set]],
                              gold: Dict[str, Dict[Tuple[int, int], set]]
                              ) -> Dict[int, Tuple[int, int]]:
        """Help aligning frames from predictions with span from golds"""
        alignments = defaultdict(tuple)
        
        for frame in pred[self.guid]:
            for span in gold[self.guid]:
                if span[0] <= frame <= span[1]:
                    alignments[frame] = span
                    break
        
        if not alignments:
            logging.warning(f"No frames were aligned for {self.guid}")
            
        return alignments

    @abstractmethod
    def calculate(self) -> Dict[int, Tuple[int, Tuple[int, int, int]]]:
        pass


class StringList:
    """
    The class that represents a list of strings and it enables the "outer product" operation
    """
    def __init__(self, strs: List[str]) -> None:
        self.strs = strs

    def __matmul__(self, other: List[str]) -> np.ndarray:
        if not isinstance(other, StringList):
            raise ValueError("The right-hand operand must be an instance of StringList")

        # Perform the "outer product" operation and store results in a list of lists
        result_matrix = []
        for str1 in self.strs:
            row = []
            for str2 in other.strs:
                distance = fuzz.ratio(str1, str2)
                row.append(distance)
            result_matrix.append(row)

        # Convert the result matrix to a NumPy array
        return np.array(result_matrix)


class IOU(RFBMetrics):
    """
    The class of Intersection Over Union (IOU) evaluation metric
    """
    def _iou(self, p: set, g: set) -> float:
        try:
            val = len(set.intersection(p, g)) / len(set.union(p, g))
        except ZeroDivisionError:
            val = 0
        return val

    def _organize(self, frame_data: Set[Tuple[str, str]]) -> Tuple[Set, Set, Dict]:
        role_set, filler_set, binding = set(), set(), defaultdict(list)
        for role, filler in frame_data:
            role_set.add(role)
            filler_set.add(filler)
            binding[role].append(filler)
        return role_set, filler_set, binding

    def _fuzzy_match(self, gold_list: StringList, pred_list: StringList) -> List[int]:
        match_matrix = gold_list @ pred_list
        max_indices = np.argmax(match_matrix, axis=0)
        
        valid_indices = [row
                         for col, row in enumerate(max_indices)
                         if match_matrix[row, col] == 100
                         ]
        
        return valid_indices

    def _intersect_between_binding(self, gold: Dict, pred: Dict) -> int:
        # Index the roles in gold first
        gold_roles = {idx: role for idx, role in enumerate(gold.keys())}

        # Fuzzy match the roles in pred with the roles in gold
        gold_array = StringList(list(gold_roles.values()))
        pred_array = StringList(list(pred.keys()))
        
        matched_roles = [gold_roles[idx] for idx in self._fuzzy_match(gold_array, pred_array)]

        # Fuzzy match the fillers between gold and pred sharing the same role
        num_intersect = 0
        for role in matched_roles:
            gold_fillers, pred_fillers = StringList(gold[role]), StringList(pred[role])
            matched_fillers = self._fuzzy_match(gold_fillers, pred_fillers)
            num_intersect += len(matched_fillers)

        return num_intersect

    def _union_between_binding(self, gold: Dict, pred: Dict) -> int:
        gold_bindings = [(role, f) for role, fillers in gold.items() for f in fillers]
        pred_bindings = [(role, f) for role, fillers in pred.items() for f in fillers]
        return len(set(gold_bindings).union(set(pred_bindings)))

    def calculate(self) -> Dict[int, Tuple[int, Tuple[int, int, int]]]:
        if self.frames:
            for frame, span in self.frames.items():
                gold_roles, gold_fillers, gold_binding = self._organize(self.gold[self.guid][span])
                pred_roles, pred_fillers, pred_binding = self._organize(self.pred[self.guid][frame])
                role_iou = round(self._iou(pred_roles, gold_roles), 2)
                filler_iou = round(self._iou(pred_fillers, gold_fillers), 2)
                binding_iou = round(
                                    self._intersect_between_binding(gold_binding, pred_binding) / self._union_between_binding(gold_binding, pred_binding),
                                    2
                                    )
                self.frame_score[frame] = (role_iou, filler_iou, binding_iou)
        else:
            logging.warning("No overlap frames are found between gold and prediction data")
            self.frame_score = {-1: (-1, -1, -1)}
        return self.frame_score

# --------------------------------------------------------------------
# Run evaluation in parallel
# --------------------------------------------------------------------

def _load_file(args):
    """Helper function to load a single file for parallel processing"""
    file_path, label = args
    start_time = time.time()
    result = None
    if label == 'gold':
        result = load_gold(file_path)
    else:
        result = load_pred(file_path)
    elapsed = time.time() - start_time
    logging.debug(f"Loaded {label} file {file_path} in {elapsed:.2f} seconds")
    return result

# Define process-safe evaluation function moved outside for pickling
def process_video(guid_data):
    """Process a single video for evaluation
    
    :param guid_data: A tuple of (guid, gold_data, pred_data)
    :return: Dictionary with evaluation results
    """
    guid, gold_data, pred_data = guid_data
    try:
        logging.info(f"Evaluating {guid}...")
        iou = IOU({guid: gold_data}, {guid: pred_data})
        return {guid: iou.calculate()}
    except Exception as e:
        logging.error(f"Error evaluating {guid}: {e}")
        return {guid: {-1: (-1, -1, -1)}}

def _load_data_from_dir_parallel(directory: Union[str, os.PathLike],
                                label: str,
                                num_processes: int = 4) -> Dict[str, Dict]:
    """
    Load data from a directory using parallel processing
    
    :param directory: the directory path of data
    :param label: the label of either gold or prediction data
    :param num_processes: number of processes to use
    :return: a dictionary whose key is a GUID and value is a dictionary of frame data
    """
    logging.info(f"Loading {label} data from {directory} in parallel...")
    
    # Get list of all files in directory
    file_paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_paths.append((os.path.join(root, file), label))
    
    # Use exactly 4 processes as requested
    num_processes = min(4, len(file_paths))
    
    logging.info(f"Loading {len(file_paths)} {label} files using {num_processes} processes")
    
    # Use a pool to process files in parallel
    out = {}
    with mp.Pool(num_processes) as pool:
        results = pool.map(_load_file, file_paths)
        
        # Combine results
        for result in results:
            if result:  # Skip empty results
                out.update(result)
    
    logging.info(f"Loaded {len(out)} {label} videos")
    return out

def _load_data_from_dir(directory: Union[str, os.PathLike],
                        label: str) -> Dict[str, Dict]:
    """
    Load data from a directory (sequential version)

    :param directory: the directory path of data
    :param label: the label of either gold or prediction data
    :return: a dictionary whose key is a GUID and value is a dictionary of frame data
    """
    logging.info(f"Loading {label} data from {directory}...")
    out = {}
    file_count = 0
    
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_count += 1
            
            if label == 'gold':
                try:
                    result = load_gold(file_path)
                    out.update(result)
                except Exception as e:
                    logging.error(f"Error loading gold file {file_path}: {e}")
            else:
                try:
                    result = load_pred(file_path)
                    out.update(result)
                except Exception as e:
                    logging.error(f"Error loading prediction file {file_path}: {e}")
    
    logging.info(f"Loaded {len(out)} {label} videos from {file_count} files")
    return out


def write_out(results: List[Dict[str, Dict[int, Tuple]]],
              output_dir: Union[str, os.PathLike] = None,
              pred_dir_name: str = None) -> None:
    """Write out evaluation results to disk
    
    :param results: List of evaluation results
    :param output_dir: Directory to write results to
    :param pred_dir_name: Name of the predictions directory to use in output directory name
    :return: None
    """
    # Extract app name and dataset from prediction directory name
    if pred_dir_name is None:
        pred_dir_name = "preds@default@default"
    
    # Strip trailing slashes and get directory name
    pred_dir_clean = pred_dir_name.rstrip('/')
    dir_name_only = os.path.basename(pred_dir_clean) or pred_dir_clean.split('/')[-1]
    
    # Debug info
    logging.debug(f"Prediction directory: {pred_dir_name}")
    logging.debug(f"Extracted directory name: {dir_name_only}")
    
    # Parse directory name to extract app and dataset info
    if '@' in dir_name_only:
        parts = dir_name_only.split('@')
        app_name = parts[1] if len(parts) > 1 else "default"
        dataset = parts[2] if len(parts) > 2 else "default"
    else:
        app_name = dir_name_only or "default"
        dataset = "default"
    
    # Build output filenames
    results_dir_name = f"results@{app_name}@{dataset}"
    report_name = f"report@{app_name}@{dataset}.md"
    
    logging.info(f"Creating results in directory: {results_dir_name}")
    results_dir = os.path.join(output_dir if output_dir else os.getcwd(), results_dir_name)
    
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    
    # Calculate overall metrics for summary
    overall_metrics = {
        'role_iou': [],
        'filler_iou': [],
        'binding_iou': []
    }
    
    valid_guids = []
    
    # Process and write individual results files
    for result in results:
        for guid, frame_scores in result.items():
            # Skip entries with no frames
            if list(frame_scores.keys()) == [-1]:
                continue
                
            valid_guids.append(guid)
            
            # Calculate metrics for this guid
            role_ious, filler_ious, binding_ious = [], [], []
            json_data = {'frame_scores': {}, 'mean_scores': {}}
            
            # Process individual frame scores
            for frame, (role_iou, filler_iou, binding_iou) in frame_scores.items():
                json_data['frame_scores'][str(frame)] = {
                    'role_iou': role_iou,
                    'filler_iou': filler_iou,
                    'binding_iou': binding_iou
                }
                role_ious.append(role_iou)
                filler_ious.append(filler_iou)
                binding_ious.append(binding_iou)
            
            # Calculate and store mean scores
            json_data['mean_scores'] = {
                'role_iou': round(sum(role_ious) / len(role_ious), 3) if role_ious else 0,
                'filler_iou': round(sum(filler_ious) / len(filler_ious), 3) if filler_ious else 0,
                'binding_iou': round(sum(binding_ious) / len(binding_ious), 3) if binding_ious else 0
            }
            
            # Add to overall metrics
            for metric in overall_metrics:
                overall_metrics[metric].append(json_data['mean_scores'][metric])
            
            # Write individual JSON file
            with open(os.path.join(results_dir, f"{guid}.json"), 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2)
    
    # Calculate overall mean scores
    overall_means = {}
    for metric, values in overall_metrics.items():
        overall_means[metric] = round(sum(values) / len(values), 3) if values else 0
    
    # Write results.txt summary
    results_txt_path = os.path.join(results_dir, 'results.txt')
    with open(results_txt_path, 'w', encoding='utf-8') as f:
        # Individual results
        for result in results:
            for guid, frame_scores in result.items():
                if list(frame_scores.keys()) == [-1]:
                    continue
                
                # Calculate mean scores for this guid
                role_ious = [score[0] for score in frame_scores.values()]
                filler_ious = [score[1] for score in frame_scores.values()]
                binding_ious = [score[2] for score in frame_scores.values()]
                
                mean_role_iou = round(sum(role_ious) / len(role_ious), 3) if role_ious else 0
                mean_filler_iou = round(sum(filler_ious) / len(filler_ious), 3) if filler_ious else 0
                mean_binding_iou = round(sum(binding_ious) / len(binding_ious), 3) if binding_ious else 0
                
                f.write(f"{guid}:\tRole IOU={mean_role_iou}\tFiller IOU={mean_filler_iou}\tBinding IOU={mean_binding_iou}\n")
        
        # Overall mean scores
        f.write("\n")
        f.write(f"Overall Mean Role IOU: {overall_means['role_iou']}\n")
        f.write(f"Overall Mean Filler IOU: {overall_means['filler_iou']}\n")
        f.write(f"Overall Mean Binding IOU: {overall_means['binding_iou']}\n")
    
    # Create markdown report
    report_path = os.path.join(output_dir if output_dir else os.getcwd(), report_name)
    with open(report_path, 'w', encoding='utf-8') as f:
        # Report header
        f.write(f"# Evaluation Report for {app_name}" + (f" on {dataset}" if dataset != "default" else "") + "\n\n")
        
        # Summary section
        f.write("## Summary\n\n")
        f.write(f"Total videos evaluated: {len(valid_guids)}\n\n")
        
        # Overall metrics table
        f.write("### Overall Metrics\n\n")
        f.write("| Metric | Value |\n")
        f.write("|--------|-------|\n")
        f.write(f"| Role IOU | {overall_means['role_iou']} |\n")
        f.write(f"| Filler IOU | {overall_means['filler_iou']} |\n")
        f.write(f"| Binding IOU | {overall_means['binding_iou']} |\n\n")
        
        # Individual video metrics table
        f.write("### Individual Video Metrics\n\n")
        f.write("| GUID | Role IOU | Filler IOU | Binding IOU |\n")
        f.write("|------|----------|------------|-------------|\n")
        
        for result in results:
            for guid, frame_scores in result.items():
                if list(frame_scores.keys()) == [-1]:
                    continue
                
                # Calculate mean scores for this guid
                role_ious = [score[0] for score in frame_scores.values()]
                filler_ious = [score[1] for score in frame_scores.values()]
                binding_ious = [score[2] for score in frame_scores.values()]
                
                mean_role_iou = round(sum(role_ious) / len(role_ious), 3) if role_ious else 0
                mean_filler_iou = round(sum(filler_ious) / len(filler_ious), 3) if filler_ious else 0
                mean_binding_iou = round(sum(binding_ious) / len(binding_ious), 3) if binding_ious else 0
                
                f.write(f"| {guid} | {mean_role_iou} | {mean_filler_iou} | {mean_binding_iou} |\n")
    
    logging.info(f"Results written to {results_dir}")
    logging.info(f"Report written to {report_path}")


# --------------------------------------------------------------------
# Arguments setting
# --------------------------------------------------------------------


def parse_args() -> Namespace:
    """Provide arguments of the script
    """
    parser = ArgumentParser(
        description='Evaluation script for RFB (Role-Filler-Binding)'
    )

    parser.add_argument(
        '-p',
        '--preds',
        help='The directory path of RFB predictions',
        required=False
    )

    parser.add_argument(
        '--debug',
        action='store_true',
        help='Set the debug mode'
    )

    parser.add_argument(
        '--in_seq',
        action='store_true',
        help='Run evaluation in sequence'
    )
    
    parser.add_argument(
        '-o',
        '--output-dir',
        help='Directory to store results',
        default=None
    )
    
    parser.add_argument(
        '-g',
        '--gold-dir',
        help='Local directory containing gold standard files (instead of downloading)',
        default=None
    )

    return parser.parse_args()


# --------------------------------------------------------------------
# Debug functions
# --------------------------------------------------------------------

def debug_single_pair(gold_dir: Union[str, os.PathLike], pred_dir: Union[str, os.PathLike], output_dir: Union[str, os.PathLike] = None) -> None:
    """
    Debug function to compare a single gold to its matching prediction file
    
    :param gold_dir: Directory containing gold standard files
    :param pred_dir: Directory containing prediction files
    :param output_dir: Directory to write output results
    """
    golds = _load_data_from_dir(gold_dir, 'gold')
    preds = _load_data_from_dir(pred_dir, 'pred')
    
    overlap_videos = list(golds.keys() & preds.keys())
    print(f"Found {len(overlap_videos)} overlapping videos: {overlap_videos}")
    
    if not overlap_videos:
        print("No matching gold-prediction pairs found!")
        return
    
    # Choose the first matching pair for debugging
    guid = overlap_videos[0]
    print(f"\n\nDEBUGGING SINGLE PAIR: {guid}")
    
    # Log gold data
    gold_data = golds[guid]
    print(f"\nGOLD DATA for {guid}:")
    for span, annotations in gold_data.items():
        print(f"  Frame span {span} has {len(annotations)} annotations:")
        for role, filler in annotations:
            print(f"    Role: '{role}', Filler: '{filler}'")
    
    # Log prediction data
    pred_data = preds[guid]
    print(f"\nPREDICTION DATA for {guid}:")
    for frame, annotations in pred_data.items():
        print(f"  Frame {frame} has {len(annotations)} annotations:")
        for role, filler in annotations:
            print(f"    Role: '{role}', Filler: '{filler}'")
    
    # Create IOU calculator and check frame alignment
    iou = IOU({guid: gold_data}, {guid: pred_data})
    print(f"\nFRAME ALIGNMENT:")
    for pred_frame, gold_span in iou.frames.items():
        print(f"  Prediction frame {pred_frame} aligns with gold span {gold_span}")
    
    # Calculate IOU for this pair
    scores = iou.calculate()
    print(f"\nIOU SCORES:")
    for frame, (role_iou, filler_iou, binding_iou) in scores.items():
        print(f"  Frame {frame}: Role IOU={role_iou}, Filler IOU={filler_iou}, Binding IOU={binding_iou}")
    
    # Write the results to disk
    if output_dir:
        write_out([{guid: scores}], output_dir)
        print(f"\nResults written to {output_dir}/{guid}.json")
        print(f"Summary results written to {output_dir}/results.txt")


def main():
    """Main function for running the evaluation task for the RFB app
    """
    args = parse_args()
    
    # Configure logging
    logging_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=logging_level, format='%(levelname)s: %(message)s')
    
    # Ensure predictions directory is provided
    if not args.preds:
        logging.error("Predictions directory is required")
        return

    # Record total time
    total_start_time = time.time()

    # Use local gold directory if specified, otherwise download
    golds_dir = None
    if args.gold_dir:
        if args.gold_dir.startswith('http://') or args.gold_dir.startswith('https://'):
            logging.info(f"Attempting to download golds from URL: {args.gold_dir}")
            try:
                golds_dir = goldretriever.download_golds(args.gold_dir)
            except Exception as e: # Catch potential download errors
                logging.error(f"Failed to download golds from {args.gold_dir}: {e}")
                return
        elif os.path.isdir(args.gold_dir):
            golds_dir = args.gold_dir
            logging.info(f"Using local gold directory: {golds_dir}")
        else:
            logging.error(f"Provided gold path is neither a valid URL nor an existing directory: {args.gold_dir}")
            return
    else:
        logging.error("Gold standard location (-g or --gold-dir) is required (either a URL or a local directory path).")
        return

    # Ensure golds_dir was successfully set
    if not golds_dir:
        logging.error("Could not determine gold standard directory.")
        return

    # Debug mode: compare a single gold-prediction pair
    if args.debug:
        logging.info("Running in debug mode - comparing a single gold-prediction pair")
        debug_single_pair(golds_dir, args.preds, args.output_dir)
        return

    # Run evaluation (sequential or parallel)
    is_parallel = not args.in_seq
    mode = "sequential" if args.in_seq else "parallel"
    logging.info(f"Running evaluation in {mode} mode")
    
    # Call run_evaluation directly without wrapper functions
    results, pred_dir_name = run_evaluation(
        golds_dir, 
        args.preds,
        parallel=is_parallel, 
        num_processes=4 if is_parallel else 1
    )
    
    # Write results
    write_out(results, args.output_dir, pred_dir_name)
    
    # Report total time
    total_time = time.time() - total_start_time
    logging.info(f"Total execution time: {total_time:.2f} seconds")


def run_evaluation(gold_dir: Union[str, os.PathLike],
                  pred_dir: Union[str, os.PathLike],
                  parallel: bool = True,
                  num_processes: int = 4) -> Tuple[List[Dict[str, Dict[int, Tuple]]], str]:
    """
    Run evaluation either in parallel or sequential mode
    
    :param gold_dir: Directory containing gold standard data
    :param pred_dir: Directory containing prediction data
    :param parallel: Whether to use parallel processing
    :param num_processes: Number of processes to use in parallel mode
    :return: Tuple of (results, prediction directory name)
    """
    mode = "parallel" if parallel else "sequential"
    logging.info(f"Starting evaluation in {mode} mode...")
    
    # Load gold data sequentially (always)
    start_time = time.time()
    golds = _load_data_from_dir(gold_dir, 'gold')
    gold_loading_time = time.time() - start_time
    logging.info(f"Gold data loading completed in {gold_loading_time:.2f} seconds")
    
    # Load prediction data (either in parallel or sequentially)
    start_time = time.time()
    if parallel:
        logging.info(f"Using {num_processes} processes for parallel evaluation")
        preds = _load_data_from_dir_parallel(pred_dir, 'pred', num_processes)
    else:
        preds = _load_data_from_dir(pred_dir, 'pred')
    pred_loading_time = time.time() - start_time
    logging.info(f"{mode.capitalize()} prediction data loading completed in {pred_loading_time:.2f} seconds")
    
    total_loading_time = gold_loading_time + pred_loading_time
    logging.info(f"Total data loading completed in {total_loading_time:.2f} seconds")
    
    # Find overlapping videos
    overlap_videos = list(golds.keys() & preds.keys())
    logging.info(f"Found {len(overlap_videos)} overlapping videos")
    
    if not overlap_videos:
        logging.warning("No overlap videos found between gold and prediction data")
        return [], pred_dir
    
    # Evaluate videos (parallel or sequential)
    start_time = time.time()
    results = []
    
    if parallel:
        # Prepare data for parallel processing
        process_data = [(guid, golds[guid], preds[guid]) for guid in overlap_videos]
        
        # Run in parallel
        with mp.Pool(num_processes) as pool:
            results = pool.map(process_video, process_data)
    else:
        # Sequential evaluation
        for video in overlap_videos:
            logging.info(f"Evaluating {video}...")
            iou = IOU({video: golds[video]}, {video: preds[video]})
            results.append({video: iou.calculate()})
    
    eval_time = time.time() - start_time
    logging.info(f"Evaluation completed in {eval_time:.2f} seconds")
    
    return results, pred_dir


if __name__ == "__main__":
    main()
