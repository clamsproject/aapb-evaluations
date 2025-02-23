import json
import re
from pathlib import Path
from mmif import Mmif, View, AnnotationTypes, DocumentTypes
from typing import Dict, List, Tuple
from jiwer import wer, cer
from collections import defaultdict, Counter
from dateutil import parser
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np


# Define the fields we want to extract from transcriptions
FIELDS_OF_INTEREST = {
    "PROGRAM-TITLE",
    "EPISODE-TITLE",
    "SERIES-TITLE",
    "TITLE",
    "EPISODE-NO",
    "CREATE-DATE",
    "AIR-DATE",
    "DATE",
    "DIRECTOR",
    "PRODUCER",
    "CAMERA"
}

def load_gold_standard(file_path):
    """
    Load and parse the gold standard data from img_arr_prog.js
    Returns a dictionary mapping image filenames to their raw and structured annotations
    """
    # Read the file content
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Extract just the array content
    content = content.strip()
    content = content.replace('imgArray = ', '')
    content = content.rstrip(';')
    
    # Parse each row into a list
    gold_standard = {}
    
    try:
        # Use json.loads to parse the array
        data = json.loads(content)
        
        # Process each entry
        for entry in data:
            filename = entry[0]  # First element is filename
            raw_transcription = entry[5]  # Sixth element is raw transcription
            structured_text = entry[6]  # Seventh element is structured transcription
            
            # Parse the structured text into key-value pairs for fields of interest
            structured_transcription = {}
            for line in structured_text.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip().upper()  # Convert key to uppercase
                    value = value.strip()
                    if key in FIELDS_OF_INTEREST:
                        structured_transcription[key] = value
            
            gold_standard[filename] = {
                "raw_transcription": raw_transcription,
                "structured_transcription": structured_transcription
            }
            
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None
        
    return gold_standard

def parse_llava_text(text: str) -> Dict[str, str]:
    """
    Parse LLaVA output text to extract prompt and response
    Returns a dictionary with 'prompt' and 'response' keys
    """
    # Find content between 
    prompt_match = re.search(r'\[INST\](.*?)\[/INST\]', text, re.DOTALL)
    prompt = prompt_match.group(1).strip() if prompt_match else ""
    
    # Get everything after 
    response_match = re.search(r'\[/INST\](.*?)$', text, re.DOTALL)
    response = response_match.group(1).strip() if response_match else ""
    
    return {
        "prompt": prompt,
        "response": response
    }

def load_predictions(predictions_dir: str) -> Dict[str, List[Dict[str, str]]]:
    """
    Load prediction MMIF files and extract TextDocument annotation from last relevant view
    Returns a dictionary mapping image filenames to lists of prediction dictionaries
    """
    predictions = {}
    pred_dir = Path(predictions_dir)
    
    print(f"\nLoading predictions from {predictions_dir}")
    
    # Create set of keys to preserve (including "series")
    preserve_keys = {key.lower() for key in FIELDS_OF_INTEREST}
    preserve_keys.add("series")
    
    for mmif_file in pred_dir.glob("*.mmif"):
        # Get corresponding image filename (replace .mmif with .jpg)
        image_filename = mmif_file.name.replace('.mmif', '.jpg')
        
        # Load and parse MMIF file
        with open(mmif_file, 'r') as f:
            try:
                mmif_data = Mmif(f.read())
            except Exception as e:
                print(f"Error loading MMIF file {mmif_file}: {e}")
                continue
        
        # Extract and parse text value from last TextDocument view
        parsed_predictions = []
        text_views = mmif_data.get_all_views_contain(DocumentTypes.TextDocument)
        if text_views:
            last_view = text_views[-1]
            for annotation in last_view.annotations:
                if annotation.at_type == "http://mmif.clams.ai/vocabulary/TextDocument/v1":
                    raw_text = annotation.properties.text_value
                    print(f"\nFile: {image_filename}")
                    print(f"Raw text starts with: {raw_text[:100]}...")
                    
                    # Check if this is JANUS output (based on directory name)
                    if "janus" in str(predictions_dir).lower():
                        if ":" in raw_text:
                            # Check if text before colon is a key we want to preserve
                            prefix = raw_text.split(":", 1)[0].strip().lower()
                            if prefix in preserve_keys:
                                text = raw_text
                            else:
                                text = raw_text.split(":", 1)[1].strip()
                        else:
                            text = raw_text
                        
                        # Remove various types of quotation marks
                        text = text.strip('`"\'')
                        parsed_predictions.append({"response": text})
                    else:
                        parsed_text = parse_llava_text(raw_text)
                        # Remove quotation marks from response
                        if "response" in parsed_text:
                            parsed_text["response"] = parsed_text["response"].strip('`"\'')
                        parsed_predictions.append(parsed_text)
                    
                    print(f"Processed text starts with: {parsed_predictions[0]['response'][:100]}...")
                    break  # Only take the first TextDocument from last view
        
        if parsed_predictions:
            predictions[image_filename] = parsed_predictions
    
    return predictions

def evaluate_raw_transcription(gold_text: str, pred_text: str) -> Dict[str, float]:
    """
    Evaluate raw transcription using CER and WER metrics
    """
    # Clean up texts - remove extra whitespace and normalize
    gold_text = ' '.join(gold_text.split())
    pred_text = ' '.join(pred_text.split())
    
    return {
        "cer": cer(gold_text, pred_text),
        "wer": wer(gold_text, pred_text)
    }

def parse_structured_prediction(text: str) -> Dict[str, str]:
    """
    Parse the JSON prediction from the model's response
    """
    if not text:
        return {}
        
    # Remove ```json and ``` markers and any surrounding whitespace/newlines
    text = re.sub(r'^```json\s*', '', text)
    text = re.sub(r'\s*```\s*$', '', text)
    text = re.sub(r'\s*`+\s*$', '', text)  # Remove any trailing backticks
    text = text.strip()
    
    try:
        result = json.loads(text)
        # Ensure all values are strings or None
        return {k: str(v) if v is not None else None for k, v in result.items()}
    except json.JSONDecodeError as e:
        print(f"Warning: Skipping invalid JSON prediction: {e}")
        return {}

def normalize_date(date_str: str) -> str:
    """
    Normalize date strings to a standard format (YYYY-MM-DD)
    Returns original string if it can't be parsed
    """
    if not date_str:
        return date_str
        
    try:
        # Parse the date string using dateutil
        parsed_date = parser.parse(date_str)
        # Return standardized format
        return parsed_date.strftime('%Y-%m-%d')
    except (ValueError, TypeError):
        # Return original if parsing fails
        return date_str

def evaluate_structured_fields(gold_dict: Dict[str, str], 
                             pred_dict: Dict[str, str]) -> Dict[str, float]:
    """
    Evaluate structured field extraction using accuracy
    """
    correct = 0
    total = 0
    
    # Check each field in the gold standard
    for field in FIELDS_OF_INTEREST:
        if field in gold_dict:
            total += 1
            gold_value = gold_dict[field]
            pred_value = pred_dict.get(field.lower(), '')
            
            # Normalize dates for date-related fields
            if field in {'CREATE-DATE', 'AIR-DATE', 'DATE'}:
                gold_value = normalize_date(gold_value)
                pred_value = normalize_date(pred_value)
            
            if field.lower() in pred_dict and pred_value and gold_value.lower() == pred_value.lower():
                correct += 1
    
    accuracy = correct / total if total > 0 else 0
    
    return {
        "accuracy": accuracy,
        "correct": correct,
        "total": total
    }

def evaluate_dates(gold_dict: Dict[str, str], pred_dict: Dict[str, str]) -> Dict[str, int]:
    """
    Evaluate date matching across all fields, regardless of field names
    """
    # Extract and normalize all dates from gold standard
    gold_dates = set()
    for value in gold_dict.values():
        normalized_date = normalize_date(value)
        try:
            # Only add if it's actually a date
            datetime.strptime(normalized_date, '%Y-%m-%d')
            gold_dates.add(normalized_date)
        except (ValueError, TypeError):
            continue

    # Extract and normalize all dates from predictions
    pred_dates = set()
    incorrect_dates = set()  # Track incorrect dates
    for value in pred_dict.values():
        normalized_date = normalize_date(value)
        try:
            datetime.strptime(normalized_date, '%Y-%m-%d')
            pred_dates.add(normalized_date)
            if normalized_date not in gold_dates:
                incorrect_dates.add(normalized_date)
        except (ValueError, TypeError):
            continue

    return {
        "correct_dates": len(gold_dates & pred_dates),  # intersection
        "total_gold_dates": len(gold_dates),
        "incorrect_pred_dates": len(pred_dates - gold_dates),  # dates in pred but not in gold
        "incorrect_dates_examples": list(incorrect_dates)  # Add examples of incorrect dates
    }

def evaluate_non_date_fields(gold_dict: Dict[str, str], pred_dict: Dict[str, str]) -> Dict[str, int]:
    """
    Evaluate non-date field matching across all fields, regardless of field names
    """
    # Extract all non-date values from gold standard
    gold_values = set()
    date_fields = {'CREATE-DATE', 'AIR-DATE', 'DATE'}
    
    for field, value in gold_dict.items():
        if field not in date_fields and value and isinstance(value, str):
            cleaned_value = value.strip()
            if cleaned_value:
                gold_values.add(cleaned_value.lower())
    
    # Extract all non-date values from predictions
    pred_values = set()
    incorrect_values = set()
    
    for field, value in pred_dict.items():
        if value and isinstance(value, str):
            cleaned_value = value.strip()
            if cleaned_value:
                # Skip if it looks like a date
                try:
                    datetime.strptime(normalize_date(cleaned_value), '%Y-%m-%d')
                    continue
                except (ValueError, TypeError):
                    normalized_value = cleaned_value.lower()
                    pred_values.add(normalized_value)
                    if normalized_value not in gold_values:
                        incorrect_values.add(cleaned_value)  # Keep original case for display
    
    return {
        "correct_values": len(gold_values & {v.lower() for v in pred_values}),  # intersection
        "total_gold_values": len(gold_values),
        "total_pred_values": len(pred_values),
        "incorrect_values": len(incorrect_values),
        "incorrect_values_examples": list(incorrect_values)
    }

def evaluate_predictions(gold_data: Dict, pred_data: Dict) -> Dict:
    """
    Evaluate all predictions against gold standard
    """
    results = {
        "raw_transcription": defaultdict(list),
        "structured_fields": defaultdict(list),
        "dates": defaultdict(list),
        "non_date_fields": defaultdict(list),
        "overall": {},
        "incorrect_dates_all": set(),
        "incorrect_values_all": set()
    }
    
    print("\nDebugging evaluation process:")
    print(f"Number of gold entries: {len(gold_data)}")
    print(f"Number of pred entries: {len(pred_data)}")
    
    # Evaluate each image
    for image_file in set(gold_data.keys()) & set(pred_data.keys()):
        gold = gold_data[image_file]
        preds = pred_data[image_file]
        
        print(f"\nProcessing file: {image_file}")
        print(f"Number of predictions: {len(preds)}")
        
        if len(preds) >= 1:
            raw_metrics = evaluate_raw_transcription(
                gold["raw_transcription"],
                preds[0]["response"]
            )
            for metric, value in raw_metrics.items():
                results["raw_transcription"][metric].append(value)
        
        if len(preds) >= 2:
            pred_struct = parse_structured_prediction(preds[1]["response"])
            print(f"Structured prediction keys: {list(pred_struct.keys())}")
            
            struct_metrics = evaluate_structured_fields(
                gold["structured_transcription"],
                pred_struct
            )
            print(f"Structured metrics: {struct_metrics}")
            
            for metric, value in struct_metrics.items():
                results["structured_fields"][metric].append(value)
            
            date_metrics = evaluate_dates(
                gold["structured_transcription"],
                pred_struct
            )
            for metric, value in date_metrics.items():
                if metric != "incorrect_dates_examples":
                    results["dates"][metric].append(value)
                else:
                    results["incorrect_dates_all"].update(value)
            
            # Add non-date field evaluation
            non_date_metrics = evaluate_non_date_fields(
                gold["structured_transcription"],
                pred_struct
            )
            for metric, value in non_date_metrics.items():
                if metric != "incorrect_values_examples":
                    results["non_date_fields"][metric].append(value)
                else:
                    results["incorrect_values_all"].update(value)
    
    print("\nFinal results structure:")
    for key, value in results.items():
        if key != "overall":
            print(f"{key}: {dict(value)}")
    
    # Calculate averages
    for eval_type in ["raw_transcription", "structured_fields"]:
        for metric, values in results[eval_type].items():
            results["overall"][f"{eval_type}_{metric}_avg"] = sum(values) / len(values) if values else 0
    
    print("\nOverall metrics:")
    print(results["overall"])
    
    return results

def create_dataset_visualizations(gold_data: Dict, pred_data: Dict, output_dir: str = "evaluation_plots"):
    """
    Create and save visualizations of the dataset and evaluation results
    """
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # 1. Key Distribution Pie Chart
    key_counts = Counter()
    for image_data in gold_data.values():
        for key in image_data["structured_transcription"].keys():
            key_counts[key] += 1
    
    plt.figure(figsize=(12, 8))
    plt.pie(key_counts.values(), labels=key_counts.keys(), autopct='%1.1f%%')
    plt.title('Distribution of Keys in Dataset')
    plt.axis('equal')
    plt.savefig(f'{output_dir}/key_distribution_pie.png')
    plt.close()
    
    # 2. Value Lengths Box Plot
    value_lengths = defaultdict(list)
    for image_data in gold_data.values():
        for key, value in image_data["structured_transcription"].items():
            if value:  # Only include non-empty values
                value_lengths[key].append(len(value))
    
    plt.figure(figsize=(15, 8))
    plt.boxplot([lengths for lengths in value_lengths.values()], 
                labels=value_lengths.keys(),
                vert=False)
    plt.title('Distribution of Value Lengths by Key')
    plt.xlabel('Number of Characters')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/value_lengths_box.png')
    plt.close()
    
    # 3. CER by Key Bar Chart
    cer_by_key = defaultdict(list)
    for image_file in set(gold_data.keys()) & set(pred_data.keys()):
        if len(pred_data[image_file]) < 2:
            continue
            
        gold_struct = gold_data[image_file]["structured_transcription"]
        try:
            pred_struct = parse_structured_prediction(pred_data[image_file][1]["response"])
            for key, gold_value in gold_struct.items():
                if gold_value and key.lower() in pred_struct and pred_struct[key.lower()]:
                    error = cer(gold_value, pred_struct[key.lower()])
                    cer_by_key[key].append(error)
        except (json.JSONDecodeError, KeyError):
            continue
    
    # Calculate average CER for each key
    avg_cer_by_key = {k: np.mean(v) for k, v in cer_by_key.items() if v}
    
    plt.figure(figsize=(15, 8))
    keys = list(avg_cer_by_key.keys())
    values = list(avg_cer_by_key.values())
    
    plt.bar(keys, values)
    plt.title('Character Error Rate by Key')
    plt.xlabel('Key')
    plt.ylabel('CER')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/cer_by_key_bar.png')
    plt.close()
    
    return {
        "key_counts": dict(key_counts),
        "avg_value_lengths": {k: np.mean(v) for k, v in value_lengths.items()},
        "cer_by_key": avg_cer_by_key
    }

def evaluate_date_extraction(gold_dict: Dict[str, str], pred_text: str) -> Dict[str, int]:
    """
    Evaluate date extraction from llava_output
    Returns counts of correct and incorrect dates
    """
    # Extract all dates from gold standard
    gold_dates = set()
    for value in gold_dict.values():
        normalized_date = normalize_date(value)
        try:
            datetime.strptime(normalized_date, '%Y-%m-%d')
            gold_dates.add(normalized_date)
        except (ValueError, TypeError):
            continue

    # Extract dates from prediction
    # Split by comma and clean up each date
    pred_dates = set()
    incorrect_dates = set()
    for date_str in pred_text.split(','):
        normalized_date = normalize_date(date_str.strip())
        try:
            datetime.strptime(normalized_date, '%Y-%m-%d')
            pred_dates.add(normalized_date)
            if normalized_date not in gold_dates:
                incorrect_dates.add(normalized_date)
        except (ValueError, TypeError):
            continue

    return {
        "correct_dates": len(gold_dates & pred_dates),  # intersection
        "total_gold_dates": len(gold_dates),
        "incorrect_dates": len(incorrect_dates),
        "incorrect_dates_examples": list(incorrect_dates)
    }

if __name__ == "__main__":
    # Load data
    gold_data = load_gold_standard("madison_slates_annotation_omitted_removed/img_arr_prog.js")
    llava_dates = load_predictions("llava_output")
    llava_struct = load_predictions("llava_output_2")
    llava_trans = load_predictions("llava_output_3")
    janus_data = load_predictions("janus_output")
    
    if gold_data and llava_dates and llava_struct and llava_trans and janus_data:
        print("\nEvaluating date extraction (llava_output)...")
        date_results = defaultdict(list)
        for image_file in set(gold_data.keys()) & set(llava_dates.keys()):
            if len(llava_dates[image_file]) >= 1:
                metrics = evaluate_date_extraction(
                    gold_data[image_file]["structured_transcription"],
                    llava_dates[image_file][0]["response"]
                )
                for key, value in metrics.items():
                    if key != "incorrect_dates_examples":
                        date_results[key].append(value)
        
        print("\nEvaluating structured fields (llava_output_2)...")
        results_2 = evaluate_predictions(gold_data, llava_struct)
        
        print("\nEvaluating transcription quality...")
        # Evaluate CER/WER for llava_output_3 and janus_output
        cer_wer_3 = {"cer": [], "wer": []}
        cer_wer_janus = {"cer": [], "wer": []}
        
        # Compare transcriptions
        for image_file in set(gold_data.keys()) & set(llava_trans.keys()) & set(janus_data.keys()):
            gold = gold_data[image_file]["raw_transcription"]
            
            if len(llava_trans[image_file]) >= 1:
                metrics = evaluate_raw_transcription(
                    gold,
                    llava_trans[image_file][0]["response"]
                )
                cer_wer_3["cer"].append(metrics["cer"])
                cer_wer_3["wer"].append(metrics["wer"])
            
            if len(janus_data[image_file]) >= 1:
                metrics = evaluate_raw_transcription(
                    gold,
                    janus_data[image_file][0]["response"]
                )
                cer_wer_janus["cer"].append(metrics["cer"])
                cer_wer_janus["wer"].append(metrics["wer"])

        # Calculate averages
        avg_cer_3 = sum(cer_wer_3["cer"]) / len(cer_wer_3["cer"]) if cer_wer_3["cer"] else 0
        avg_wer_3 = sum(cer_wer_3["wer"]) / len(cer_wer_3["wer"]) if cer_wer_3["wer"] else 0
        avg_cer_janus = sum(cer_wer_janus["cer"]) / len(cer_wer_janus["cer"]) if cer_wer_janus["cer"] else 0
        avg_wer_janus = sum(cer_wer_janus["wer"]) / len(cer_wer_janus["wer"]) if cer_wer_janus["wer"] else 0
        
        # Print results
        print("\nDetailed Evaluation Report:")
        
        print("\n1. Date Extraction Metrics (llava_output):")
        total_gold_dates = sum(date_results["total_gold_dates"])
        total_correct_dates = sum(date_results["correct_dates"])
        total_incorrect_dates = sum(date_results["incorrect_dates"])
        print(f"  - Total dates in gold standard: {total_gold_dates}")
        if total_gold_dates > 0:
            recall = (total_correct_dates/total_gold_dates)*100
            print(f"  - Dates correctly identified: {total_correct_dates} ({recall:.1f}% recall)")
        print(f"  - Incorrect dates in predictions: {total_incorrect_dates}")
        
        print("\n2. Structured Field Metrics (llava_output_2):")
        total_gold_fields = sum(results_2["structured_fields"]["total"])
        total_correct_fields = sum(results_2["structured_fields"]["correct"])
        print(f"  - Total fields in gold standard: {total_gold_fields}")
        if total_gold_fields > 0:
            accuracy = (total_correct_fields/total_gold_fields)*100
            print(f"  - Fields correctly identified: {total_correct_fields} ({accuracy:.1f}% accuracy)")
        
        # Date matching regardless of field
        total_gold_dates = sum(results_2["dates"]["total_gold_dates"])
        total_correct_dates = sum(results_2["dates"]["correct_dates"])
        total_incorrect_dates = sum(results_2["dates"]["incorrect_pred_dates"])
        print("\n  Date matching (regardless of field):")
        print(f"    - Total dates in gold: {total_gold_dates}")
        if total_gold_dates > 0:
            recall = (total_correct_dates/total_gold_dates)*100
            print(f"    - Dates correctly identified: {total_correct_dates} ({recall:.1f}% recall)")
        print(f"    - Incorrect dates in predictions: {total_incorrect_dates}")
        
        # Non-date value matching regardless of field
        total_gold_values = sum(results_2["non_date_fields"]["total_gold_values"])
        total_correct_values = sum(results_2["non_date_fields"]["correct_values"])
        total_pred_values = sum(results_2["non_date_fields"]["total_pred_values"])
        print("\n  Non-date value matching (regardless of field):")
        print(f"    - Total values in gold: {total_gold_values}")
        if total_gold_values > 0:
            recall = (total_correct_values/total_gold_values)*100
            print(f"    - Values correctly identified: {total_correct_values} ({recall:.1f}% recall)")
        if total_pred_values > 0:
            precision = (total_correct_values/total_pred_values)*100
            print(f"    - Precision: {precision:.1f}%")
        
        print("\n3. Raw Transcription Metrics:")
        print("\nLLaVA Output 3:")
        print(f"  - Character Error Rate (CER): {avg_cer_3:.3f}")
        print(f"  - Word Error Rate (WER): {avg_wer_3:.3f}")
        
        print("\nJANUS Output:")
        print(f"  - Character Error Rate (CER): {avg_cer_janus:.3f}")
        print(f"  - Word Error Rate (WER): {avg_wer_janus:.3f}")
