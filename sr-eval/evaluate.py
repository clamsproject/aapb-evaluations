import argparse
from collections import defaultdict, Counter
import pathlib

import mmif.vocabulary.document_types
import pandas as pd
from clams_utils.aapb import goldretriever
from mmif import Mmif

# constant:
GOLD_URL = "https://github.com/clamsproject/aapb-annotations/tree/bebd93af0882b8cf942ba827917938b49570d6d9/scene-recognition/golds"
# note that you must first have output mmif files to compare against

# parse SWT output into dictionary to extract label-timepoint pairs


def convert_iso_milliseconds(timestamp):
    """
    convert ISO timestamp strings (hours:minutes:seconds.ms) back to milliseconds
    """
    ms = 0

    ms += int(timestamp.split(":")[0]) * 3600000    # add hours
    ms += int(timestamp.split(":")[1]) * 60000      # add minutes
    ms += float(timestamp.split(":")[2]) * 1000     # add seconds and milliseconds
    ms = int(ms)
    return ms


def extract_gold_labels(goldpath, count_subtypes=False):
    """
    extract gold pairs from each csv. note goldpath is fed in as a path object
    """
    df = pd.read_csv(goldpath)
    # convert timestamps (iso) back to ms
    df['timestamp'] = df['timestamp'].apply(convert_iso_milliseconds)
    if count_subtypes:
        # fill empty subtype rows with '' then concatenate with type label
        df['subtype label'] = df['subtype label'].fillna("")
        df['combined'] = df['type label'] + ":" + df['subtype label']
        # trim extra ":"
        df['combined'] = df['combined'].apply(lambda row: row[:-1] if row[-1] == ':' else row)
        # create dictionary of 'timestamp':'combined' from dataframe
        gold_dict = df.set_index('timestamp')['combined'].to_dict()
    else:
        # ignore subtype label column
        gold_dict = df.set_index('timestamp')['type label'].to_dict()
    # return dictionary that maps timestamps to label
    return gold_dict


def closest_gold_timestamp(pred_stamp, gold_dict, good_range = 5):
    """
    method to match a given predicted timestamp (key) with the closest gold timestamp:
    acceptable range is default +/- 5 ms. if nothing matches, return None
    """
    if pred_stamp in gold_dict:
        return pred_stamp
    for i in range(good_range, 0, -1):
        if pred_stamp - i in gold_dict:
            return pred_stamp - i
    for i in range(1, good_range + 1):
        if pred_stamp + i in gold_dict:
            return pred_stamp + i
    return None


def combine_pred_and_gold_labels(pred_path, gold_dict, count_subtypes = False):
    """
    extract predicted label pairs from output mmif and match with gold pairs
    note that pred_path is already a filepath, not a string
    returns a dictionary with timestamps as keys and tuples of labels as values.
    """
    combined_dict = {}
    with open(pred_path, "r") as file:
        json_data = file.read()
        pred_mmif = Mmif(json_data)
        view = pred_mmif.get_view_contains(mmif.AnnotationTypes.TimePoint)
        if "annotations" in view:
            for annotation in view["annotations"]:
                if "timePoint" in annotation['properties']:
                    # match pred timestamp to closest gold timestamp using default range (+/- 5ms)
                    curr_timestamp = closest_gold_timestamp(annotation['properties']['timePoint'], gold_dict)
                    # check if closest_gold_timestamp returned None (not within acceptable range)
                    if not curr_timestamp:
                        continue
                    # truncate label if count_subtypes is false
                    pred_label = annotation['properties']['label'] if count_subtypes else annotation['properties']['label'][0]
                    # if NEG set to '-'
                    if annotation['properties']['label'] == 'NEG':
                        pred_label = '-'
                    # put gold and pred labels into combined dictionary
                    combined_dict[annotation['id']] = (pred_label, gold_dict[curr_timestamp])
    return combined_dict


def filter_remapped_labels(pred_path, combined_dict):
    """
    Returns a dict that stores filtered raw and gold remapped labels.
    Labels that cannot be remapped and timepoints with no raw or gold label are filtered out.
    """
    filtered_combined_dict = {}
    with open(pred_path, "r") as file:
        json_data = file.read()
        pred_mmif = Mmif(json_data)
        tp_view = pred_mmif.get_view_contains(mmif.AnnotationTypes.TimePoint)
        map_schema = pred_mmif.views[str(tp_view['id'])]['metadata']['appConfiguration']['map']
        for timepoint in combined_dict:
            raw_remap = "-"
            gold_remap = "-"
            if combined_dict[timepoint][0] in map_schema:
                raw_remap = map_schema[combined_dict[timepoint][0]]
            if combined_dict[timepoint][1] in map_schema:
                gold_remap = map_schema[combined_dict[timepoint][1]]
            if raw_remap != "-" or gold_remap != "-":
                filtered_combined_dict[timepoint] = (raw_remap, gold_remap)
    return filtered_combined_dict


def stitched_labels(pred_path, combined_dict):
    """
    Returns a dict that stores raw and gold remapped labels corresponding to the TF targets generated by the stitcher.
    """
    stitched_dict = {}
    with open(pred_path, "r") as file:
        json_data = file.read()
        pred_mmif = Mmif(json_data)
        tp_view = pred_mmif.get_view_contains(mmif.AnnotationTypes.TimePoint)
        map_schema = pred_mmif.views[str(tp_view['id'])]['metadata']['appConfiguration']['map']
        tf_view = pred_mmif.get_view_contains(mmif.AnnotationTypes.TimeFrame)
        if "annotations" in tf_view:
            for annotation in tf_view["annotations"]:
                if "TimeFrame" in annotation["@type"]:
                    for target in annotation["targets"]:
                        target = target.split(":")[1] if target.find(":") > -1 else target
                        stitched = annotation["properties"]["label"]
                        gold_remap = "-"
                        if combined_dict[target][1] in map_schema:
                            gold_remap = map_schema[combined_dict[target][1]]
                        stitched_dict[target] = (stitched, gold_remap)
    return stitched_dict


def document_evaluation(combined_dict):
    """
    calculate document-level p, r, f1 for each label and macro avg.
    also returns total counts of tp, fp, fn for each label to calculate micro avg later.
    """
    # count up tp, fp, fn for each label
    total_counts = defaultdict(Counter)
    for annotation_id in combined_dict:
        pred, gold = combined_dict[annotation_id][0], combined_dict[annotation_id][1]
        if pred == gold:
            total_counts[pred]["tp"] += 1
        else:
            total_counts[pred]["fp"] += 1
            total_counts[gold]["fn"] += 1
    # calculate P, R, F1 for each label, store in nested dictionary
    scores_by_label = defaultdict(lambda: defaultdict(float))
    # running total for (macro) averaged scores per document
    average_p = 0
    average_r = 0
    average_f1 = 0
    # counter to account for unseen labels
    unseen = 0
    for label in total_counts:
        tp, fp, fn = total_counts[label]["tp"], total_counts[label]["fp"], total_counts[label]["fn"]
        # if no instances are present/predicted, account for this when taking average of scores
        if tp + fp + fn == 0:
            unseen += 1
        precision = float(tp/(tp + fp)) if (tp + fp) > 0 else 0
        recall = float(tp/(tp + fn)) if (tp + fn) > 0 else 0
        f1 = float(2*(precision*recall)/(precision + recall)) if (precision + recall) > 0 else 0
        # add individual scores to dict and then add to running sum
        scores_by_label[label]["precision"] = precision
        scores_by_label[label]["recall"] = recall
        scores_by_label[label]["f1"] = f1
        average_p += precision
        average_r += recall
        average_f1 += f1
    # calculate macro averages for document and add to scores_by_label
    # make sure to account for unseen unpredicted labels
    denominator = len(scores_by_label) - unseen
    scores_by_label["average"]["precision"] = float(average_p / denominator)
    scores_by_label["average"]["recall"] = float(average_r / denominator)
    scores_by_label["average"]["f1"] = float(average_f1 / denominator)
    # return both scores_by_label and total_counts (to calculate micro avg later)
    return scores_by_label, total_counts


def total_evaluation(total_counts_list):
    """
    once you have processed every document, this method runs to calculate the micro-averaged scores.
    the input is a list of total_counts dictionaries, each obtained from running document_evaluation.
    """
    # create dict to hold total tp, fp, fn for all labels
    total_instances_by_label = defaultdict(Counter)
    # iterate through total_counts_list to get complete count of tp, fp, fn by label
    for doc_dict in total_counts_list:
        for label in doc_dict:
            total_instances_by_label[label]["tp"] += doc_dict[label]["tp"]
            total_instances_by_label[label]["fp"] += doc_dict[label]["fp"]
            total_instances_by_label[label]["fn"] += doc_dict[label]["fn"]
            # include a section for total tp/fp/fn for all labels
            total_instances_by_label["all"]["tp"] += doc_dict[label]["tp"]
            total_instances_by_label["all"]["fp"] += doc_dict[label]["fp"]
            total_instances_by_label["all"]["fn"] += doc_dict[label]["fn"]
    # create complete_micro_scores to store micro avg scores for entire dataset
    complete_micro_scores = defaultdict(lambda: defaultdict(float))
    # fill in micro scores
    for label in total_instances_by_label:
        tp, fp, fn = (total_instances_by_label[label]["tp"], total_instances_by_label[label]["fp"],
                      total_instances_by_label[label]["fn"])
        precision = float(tp/(tp + fp)) if (tp + fp) > 0 else 0
        recall = float(tp/ (tp + fn)) if (tp + fn) > 0 else 0
        f1 = float(2*precision*recall/(precision + recall)) if (precision + recall) > 0 else 0
        complete_micro_scores[label]["precision"] = precision
        complete_micro_scores[label]["recall"] = recall
        complete_micro_scores[label]["f1"] = f1
    return complete_micro_scores


def run_dataset_eval(mmif_dir, gold_dir, count_subtypes):
    """
    run the evaluation on each predicted-gold pair of files, and then the entire dataset for micro average
    scores are stored in document_scores and counts are stored in document_counts
    """
    # create dicts of guid -> scores to store each dict of document-level scores
    doc_scores = {"unfiltered": {}, "filtered": {}, "stitched": {}}
    # create lists to store each dict of document-level counts
    document_counts = {"unfiltered": [], "filtered": [], "stitched": []}
    mmif_files = pathlib.Path(mmif_dir).glob("*.mmif")
    # get each mmif file
    for mmif_file in mmif_files:
        with open(mmif_file, "r") as f:
            json_data = f.read()
            curr_mmif = Mmif(json_data)
            # get guid
            location = curr_mmif.get_document_location("http://mmif.clams.ai/vocabulary/VideoDocument/v1")
            guid = location.split("/")[-1].split(".")[0]
        # match guid with gold file
        gold_file = next(pathlib.Path(gold_dir).glob(f"*{guid}*"))
        # process gold
        gold_dict = extract_gold_labels(gold_file, count_subtypes)

        # create three dicts whose label values are: raw & gold, raw-remap & gold-remap, stitched & gold-remap
        combined_dict = combine_pred_and_gold_labels(mmif_file, gold_dict, count_subtypes)
        filtered_combined_dict = filter_remapped_labels(mmif_file, combined_dict)
        stitched_dict = stitched_labels(mmif_file, combined_dict)

        # evaluate raw and gold labels on document level
        combined_eval_result = document_evaluation(combined_dict)
        doc_scores["unfiltered"][guid] = combined_eval_result[0]
        document_counts["unfiltered"].append(combined_eval_result[1])

        # evaluate raw-remap and gold-remap labels
        filtered_eval_result = document_evaluation(filtered_combined_dict)
        doc_scores["filtered"][guid] = filtered_eval_result[0]
        document_counts["filtered"].append(filtered_eval_result[1])

        # evaluate stitcher and gold-remap labels
        stitched_eval_result = document_evaluation(stitched_dict)
        doc_scores["stitched"][guid] = stitched_eval_result[0]
        document_counts["stitched"].append(stitched_eval_result[1])

    # after processing each document and storing the relevant scores, we can evaluate the dataset performance as a whole
    data_scores = {}
    for eval_type in document_counts:
        data_scores[eval_type] = total_evaluation(document_counts[eval_type])
    return doc_scores, data_scores


def separate_score_outputs(doc_scores, dataset_scores, mmif_dir):
    # get name for new directory
    # with our standard, this results in "scores@" appended to the batch name
    batch_score_name = "scores@" + mmif_dir.split('@')[-1].strip('/')
    # create new dir for scores based on batch name
    new_dir = pathlib.Path.cwd() / batch_score_name
    new_dir.mkdir(parents = True, exist_ok = True)

    for eval_type in doc_scores:
        # iterate through nested dict, output separate scores for each guid
        for guid in doc_scores[eval_type]:
            doc_df = pd.DataFrame(doc_scores[eval_type][guid])
            doc_df = doc_df.transpose()
            out_path = new_dir / f"{guid}-{eval_type}.csv"
            doc_df.to_csv(out_path)
        # output total dataset scores
        dataset_df = pd.DataFrame(dataset_scores[eval_type])
        dataset_df = dataset_df.transpose()
        dataset_df.to_csv(new_dir/f"dataset_scores-{eval_type}.csv")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mmif_dir', type=str, required=True,
                        help='directory containing machine-annotated files in MMIF format')
    parser.add_argument('-g', '--gold_dir', type=str, default=None,
                        help='directory containing gold labels in csv format')
    parser.add_argument('-s', '--count_subtypes', type=bool, default=False,
                        help='bool flag whether to consider subtypes for evaluation')
    args = parser.parse_args()
    mmif_dir = args.mmif_dir
    gold_dir = goldretriever.download_golds(GOLD_URL) if args.gold_dir is None else args.gold_dir
    count_subtypes = args.count_subtypes
    document_scores, dataset_scores = run_dataset_eval(mmif_dir, gold_dir, count_subtypes)
    # document scores are for each doc, dataset scores are for overall (micro avg)
    # call method to output scores for each doc and then for total scores
    separate_score_outputs(document_scores, dataset_scores, mmif_dir)
