import argparse
import goldretriever
from mmif import Mmif, Document, DocumentTypes
from torchmetrics import WordErrorRate
import json
import os

def get_text_from_mmif(mmif): 
    with open(mmif, 'r') as f:
        mmif_str = f.read()
        data = Mmif(mmif_str)

        annotation: Document = data.get_documents_by_type(DocumentTypes.TextDocument)[0]
        text = annotation.text_value

    return text

def get_text_from_txt(txt):
    with open(txt, 'r') as f:
        text = f.read()
    return text

# for now, we only care about casing, more processing steps might be added in the future
def process_text(text, ignore_case):
    if ignore_case:
        text = text.upper()
    return text

def calculateWer(hyp_file, gold_file, exact_case):
    # if we want to ignore casing
    hyp = process_text(get_text_from_mmif(hyp_file), not exact_case)
    gold = process_text(get_text_from_txt(gold_file), not exact_case)
    wer = WordErrorRate()
    return wer(hyp, gold).item()

# check file id in preds and gold paths, and find the matching ids
def batch_run_wer(hyp_dir, gold_dir): 
    hyp_files = os.listdir(hyp_dir)
    gold_files = os.listdir(gold_dir)
    gold_files_dict = {x.rsplit('-transcript.txt', 1)[0]: x for x in gold_files if x.endswith('-transcript.txt')}
    result = {}
    
    for hyp_file in hyp_files:
        id = hyp_file.split('.')[0]
        gold_file = gold_files_dict.get(id)
        print("Processing file: ", hyp_file, gold_file)

        if gold_file:
            hyp_file_path = os.path.join(hyp_dir, hyp_file)
            gold_file_path = os.path.join(gold_dir, gold_file)
            try:
                wer_result_exact_case = calculateWer(hyp_file_path, gold_file_path, True)
                wer_result_ignore_case = calculateWer(hyp_file_path, gold_file_path, False)
                result[id] = [
                        {
                            "wer_result": wer_result_exact_case,
                            "exact_case": True
                        },
                        {
                            "wer_result": wer_result_ignore_case,
                            "exact_case": False
                        }
                    ]
            except Exception as wer_exception:
                print(wer_exception)
    
    with open('results.json', 'w') as fp:
        fp.write(json.dumps(result))

# constant:
GOLD_URL = "https://github.com/clamsproject/aapb-collaboration/tree/89b8b123abbd4a9a67c525cc480173b52e0d05f0/21"

if __name__ == "__main__":
    # get the absolute path of video-file-dir and hypothesis-file-dir
    parser = argparse.ArgumentParser(description='Process some directories.')
    parser.add_argument('-m', '--mmif-dir', type=str, required=True,
                        help='directory containing machine annotated files (MMIF)')
    parser.add_argument('-g', '--gold-dir', help='directory containing gold standard', default=None)
    args = parser.parse_args()

    ref_dir = goldretriever.download_golds(GOLD_URL) if args.gold_dir is None else args.gold_dir

    try: 
        batch_run_wer(args.mmif_dir, ref_dir)
    except Exception as batch_run_error:
        print(batch_run_error)