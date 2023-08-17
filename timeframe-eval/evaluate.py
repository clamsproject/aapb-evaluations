import sys
import json
import csv
import os
import pandas as pd
import mmif
import argparse
import glob
from pyannote.core import Segment, Timeline, Annotation
from pyannote.metrics.detection import DetectionErrorRate, DetectionPrecisionRecallFMeasure
from mmif import Mmif, DocumentTypes, AnnotationTypes
from requests.exceptions import ConnectionError
import pathlib
import math


#####Yao: So for now, if we want to evaluate the slate app, we need to run the code like this:
#python evaluate.py -m /your/preds/path -g /your/gold/path --slate -o /your/output/path -r /your/result/path --slate

########## small tools

#convert time from string in csv to the pyannote-style time format
def convert_time(time_str):
    parts = str(time_str).replace(';', ':').replace(',', '').split(':')
    if len(parts)==4:
        microsecond=int(parts[3].strip())
        seconds = int(parts[2].strip())
        minutes = int(parts[1].strip())
        hours = int(parts[0].strip())
        total_seconds = hours * 3600 + minutes * 60 + seconds+microsecond*0.01
        return total_seconds
    elif len(parts)==3:
        seconds = float(parts[2].strip())
        minutes = int(parts[1].strip())
        hours = int(parts[0].strip())
        total_seconds = hours * 3600 + minutes * 60 + seconds
        return total_seconds
    else:
        return 0

#download the 'goldfile' from github
def get_csv(gold_url):
    df = pd.read_csv(gold_url)
    df.to_csv('goldfiles.csv', index=False)
    return 'goldfiles.csv'

def get_tsv_list(tsv_dir):
    srt_files = os.listdir(tsv_dir)
    return [os.path.join(tsv_dir, file) for file in srt_files if file.endswith(".tsv")]

#adapt the code from Kelley Lynch - 'evaluate_chyrons.py'
def load_slate_gold_standard(tsv_file_list, test_dir):
    gold_timeframes = {}
    valid_files = set(filename.split(".")[0] for filename in os.listdir(test_dir))
    for tsv_file in tsv_file_list:
        df = pd.read_csv(tsv_file, sep=',')
        for index, row in df[["GUID", "Slate Start", "Slate End"]].iterrows():
            video_fileID = row["GUID"]
            start = row["Slate Start"]
            end = row["Slate End"]
            if pd.isna(start) or pd.isna(end):
                continue
            Slate_Start = convert_time(start)
            Slate_End = convert_time(end)
            if video_fileID in valid_files:
                if video_fileID not in gold_timeframes:
                    gold_timeframes[video_fileID] = Timeline()
                gold_timeframes[video_fileID].add(Segment(Slate_Start, Slate_End))
    return gold_timeframes

def load_chyron_gold_standard(file_name, test_dir):
    gold_timeframes = {}
    with open(file_name, 'r') as gold_csv:
        reader = csv.DictReader(gold_csv)
        for row in reader:
            video_fileID = row["video_filename"].split(".")[0]
            chyron_start = float(row["start_time"])
            chyron_end = float(row["end_time"])
            if video_fileID in [filename.split(".")[0] for filename in os.listdir(test_dir)]:
                if video_fileID not in gold_timeframes:
                    gold_timeframes[video_fileID] = Timeline()
                gold_timeframes[video_fileID].add(Segment(chyron_start, chyron_end))
    return gold_timeframes

#give each mmif file an absolute path, return a list
def get_mmif(mmif_dir):
    mmif_files = os.listdir(mmif_dir)
    mmif_file_list = [os.path.join(mmif_dir, file) for file in mmif_files if file.endswith(".mmif")]
    return mmif_file_list

#get info from mmif files
def process_mmif_file(mmif_file_path, gold_timeframe_dict):
    mmif_files = get_mmif(mmif_file_path)
    test_timeframes = {}
    for mmif_file in mmif_files:
        print(mmif_file)
        mmif = Mmif(open(mmif_file).read())
        vds = mmif.get_documents_by_type(DocumentTypes.VideoDocument)
        if vds:
            vd = vds[0]
        else:
            continue
        video_fileID = os.path.basename(vd.location).split(".")[0]
        if video_fileID in gold_timeframe_dict:
            if video_fileID not in test_timeframes:
                test_timeframes[video_fileID] = Timeline()
            #get the slate start and end time
            starts = []
            ends = []
            v = mmif.get_view_contains(AnnotationTypes.TimeFrame)
            if v is None:
                continue
            ann = v.get_annotations(AnnotationTypes.TimeFrame)
            while True:
                try:
                    cur = next(ann)
                    starts.append(float(cur.properties["start"]))
                    ends.append(float(cur.properties["end"]))
                #check if it's been annotated based on the next version of the slate app
                except:
                    break
            result = mmif.get_all_views_contain(at_types=AnnotationTypes.TimeFrame)
            view = result[-1]
            fps = vd.get_property('fps')
            calculated_starts = [round(start/fps, 2) for start in starts]
            calculated_ends = [round(end/fps, 2) for end in ends]
            i = 0
            while i < len(calculated_ends):
                test_timeframes[video_fileID].add(Segment(calculated_starts[i], calculated_ends[i]))
                i += 1
    return test_timeframes

#adapt the code from Kelley Lynch - 'evaluate_chyrons.py'
#add the situation which the mmif file is not in the gold timeframes
def calculate_detection_metrics(gold_timeframes_dict, test_timeframes, result_path):
    metric = DetectionErrorRate()
    final = DetectionPrecisionRecallFMeasure()
    TP = 0
    FP = 0
    FN = 0
    data = pd.DataFrame(columns= ['GUID', 'FN seconds', 'FP seconds', 'Total true seconds'])
    for file_ID in test_timeframes:
        reference = Annotation()
        for segment in gold_timeframes_dict[file_ID]:
            reference[segment] = "aapb"
        hypothesis = Annotation()
        for segment in test_timeframes[file_ID]:
            hypothesis[segment] = "aapb"
        results_dict = metric.compute_components(reference, hypothesis, collar=1.0,detailed=True)
        average = final.compute_components(reference, hypothesis, collar=1.0, detailed=True)
        true_positive = average['relevant retrieved']
        false_negative = average['relevant'] - true_positive
        false_positive = average['retrieved'] - true_positive
        TP += true_positive
        FP += false_positive
        FN += false_negative
        data = pd.concat([data, pd.DataFrame({'GUID': file_ID, 'FN seconds': results_dict['miss'], 'FP seconds': results_dict['false alarm'], 'Total true seconds': results_dict['total']}, index=[0])], ignore_index=True)
    try:
        precision = TP / (TP + FP)
    except ZeroDivisionError:
        precision = 0
    try:
        recall = TP / (TP + FN)
    except ZeroDivisionError:
        recall = 0
    if precision + recall == 0:
        f1 = 0.0
    else:
        f1 = (2 * precision * recall)/ (precision + recall)
    s = 'Total Precision = ' + str(precision) + '\t Total Recall = ' + str(recall) + '\t Total F1 = ' + str(f1) + '\n\n\n' + 'Individual file results: \n' + data.to_string()
    with open(result_path, 'w') as fh_out:
        fh_out.write(s)

def generate_side_by_side(golddir, testdir, outdir):
    for guid in golddir:
        no_detection = False
        path = outdir / f"{guid}.sbs.csv"
        gold_time_chunks = []
        test_time_chunks = []
        for segment in golddir[guid]:
            if segment.end == 0:
                continue
            gold_start = math.floor(segment.start)
            gold_end = math.floor(segment.end)
            gold_time_chunks.extend(range(gold_start, gold_end + 1))
        if guid in testdir:
            for segment in testdir[guid]:
                test_start = math.floor(segment.start)
                test_end = math.ceil(segment.end)
                test_time_chunks.extend(range(test_start, test_end))
        if len(gold_time_chunks) > 0 and len(test_time_chunks) > 0:
            maximum = max(max(gold_time_chunks), max(test_time_chunks))
        elif len(gold_time_chunks) > 0:
            maximum = max(gold_time_chunks)
        elif len(test_time_chunks) > 0:
            maximum = max(test_time_chunks)
        else:
            no_detection = True
        with open(path, "w") as out_f:
            if no_detection:
                out_f.write("no timeframes annotated in gold or predicted by app")
            else:
                i = 0
                while i < maximum + 1:
                    interval = "(" + str(i) + " - " + str(i + 1) + ")"
                    if i in gold_time_chunks:
                        gold = 1
                    else:
                        gold = 0
                    if i in test_time_chunks:
                        test = 1
                    else:
                        test = 0
                    out_f.write(",".join([interval, str(gold), str(test)]))
                    out_f.write("\n")
                    i += 1

if __name__ == "__main__":
    #get the absolute path of video-file-dir and hypothesis-file-dir
    parser = argparse.ArgumentParser(description='Process some directories.')
    parser.add_argument('-m', '--machine_dir', type=str, required=True,
                        help='directory containing machine annotated files')
    parser.add_argument('-o', '--output_dir', help='directory to publish side-by-side results', default=None)
    parser.add_argument('-r', '--result_file', help='file to store evaluation results', default='results.txt')
    parser.add_argument('-g', '--gold_dir', help='file to store gold standard', default=None)
    gold_group = parser.add_mutually_exclusive_group(required=True)
    gold_group.add_argument('--slate', action='store_true', help='slate annotations')
    gold_group.add_argument('--chyron', action='store_true', help='chyron annotations')
    args = parser.parse_args()
    if args.output_dir:
        outdir = pathlib.Path(args.output_dir)
        if not outdir.exists():
            outdir.mkdir()
    else:
        outdir = pathlib.Path(__file__).parent

    if args.slate:
        gold_timeframes_dict = load_slate_gold_standard(get_tsv_list(args.gold_dir), args.machine_dir)
    elif args.chyron:
        gold_url = 'https://raw.githubusercontent.com/clamsproject/aapb-annotations/61bd60e99ef24a1ca369e23de8b2c74bb2cb37d3/newshour-chyron/golds/batch2/2022-jul-chyron.csv'
        gold_timeframes_dict=load_chyron_gold_standard(get_csv(gold_url), args.machine_dir)

    # create the 'test_timeframes'
    test_timeframes=process_mmif_file(args.machine_dir, gold_timeframes_dict)

    #final calculation
    calculate_detection_metrics(gold_timeframes_dict, test_timeframes, args.result_file)
    generate_side_by_side(gold_timeframes_dict, test_timeframes, outdir)
    
