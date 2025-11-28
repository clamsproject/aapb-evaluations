# Contributing to AAPB Evaluations

Welcome to the AAPB Evaluations repository! This guide will help you understand how to contribute new evaluation tasks for CLAMS applications.

## Purpose of This Repository

This repository provides a framework for evaluating the performance of CLAMS apps in various metadata extraction tasks on AAPB-based datasets. Primary component you can contribute is `evaluate.py` scripts within each evaluation task directory. Each script is responsible for processing gold standard annotations and CLAMS app outputs, calculating relevant metrics, and generating comprehensive reports.

## Core Concepts: `ClamsAAPBEvaluationTask`

At the heart of every `evaluate.py` is the `ClamsAAPBEvaluationTask` abstract base class (ABC) defined in `common/__init__.py`. This class provides the foundational structure and common utilities needed to develop new evaluation tasks, including:

* Standardized Input Handling: Mechanisms to locate and process gold standard (human-annotated) files and prediction (CLAMS app/workflow output) files.
* Metric Calculation Orchestration: A workflow for comparing gold and prediction data, calculating relevant metrics.
* Report Generation: Tools to automatically generate formatted Markdown reports summarizing evaluation results.

## Implementing a New Evaluation Task

To contribute a new evaluation, you will typically create a new Python module (e.g., `YourEvaluationTask/evaluate.py`) that subclasses `ClamsAAPBEvaluationTask` and implements its abstract methods.

### 1. Subclassing `ClamsAAPBEvaluationTask`

Your evaluation script should start by importing `ClamsAAPBEvaluationTask` and defining a new class that inherits from it:

```python
from common import ClamsAAPBEvaluationTask
# ... other imports ...

class YourEvaluationTask(ClamsAAPBEvaluationTask):
    """
    A brief description of what this evaluation task assesses.
    This docstring will appear in the generated report.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialize any task-specific variables here
```

### 2. Implementing Abstract Methods

You **must** implement the following abstract methods:

*   **`_read_gold(self, gold_file: Union[str, Path], **kwargs) -> Any`**:
    *   **Purpose**: Reads and processes a single gold standard file into a format suitable for comparison.
    *   **Return**: The processed gold data.
*   **`_read_pred(self, pred_file: Union[str, Path], gold: Optional[Any], **kwargs) -> Tuple[Any, Optional[Any]]`**:
    *   **Purpose**: Reads and processes a single prediction file (an MMIF file from a CLAMS app). It may use the processed `gold` data for context or to modify the `gold` data (e.g., padding).
    *   **Return**: A tuple `(processed_pred_data, potentially_modified_gold_data)`. If `gold` was not modified or used, return `None` for the second element.
*   **`_compare_pair(self, guid: str, gold: Any, pred: Any) -> Any`**:
    *   **Purpose**: Performs the main calculation of evaluation metric(s) for a single pair of gold and prediction instances (identified by their GUID).
    *   **Return**: The per-GUID evaluation result, which will be stored internally.
*   **`_compare_all(self, golds: Iterable[Any], preds: Iterable[Any]) -> Any`**:
    *   **Purpose**: Performs the main calculation of evaluation metric(s) across the entire collection of gold and prediction instances. This is for aggregated, overall metrics.
    *   **Return**: The aggregated evaluation result.
*   **`_finalize_results(self)`**:
    *   **Purpose**: Aggregates the scores calculated by `_compare_pair` and `_compare_all` and stores them in `self._results`. This method is always called just before report generation.
*   **`write_side_by_side_view(self) -> str`**:
    *   **Purpose**: Generates a human-readable, side-by-side comparison of gold and prediction data for visualization purposes. This is optional and only included in the report if `sbs=True` is passed during initialization.
    *   **Return**: A string containing the Markdown-formatted side-by-side view.

### 3. Command-Line Interface (`prep_argparser`)

The `ClamsAAPBEvaluationTask` provides a default argument parser via `prep_argparser()`. You should call this method and potentially add task-specific arguments:

```python
if __name__ == '__main__':
    parser = YourEvaluationTask.prep_argparser()
    # Add any task-specific arguments here, e.g.:
    # parser.add_argument('--my-custom-param', type=str, help='A custom parameter for this task.')
    args = parser.parse_args()

    # Initialize and run the evaluation
    eval_task = YourEvaluationTask(
        batchname=args.batchname,
        gold_loc=args.golds,
        pred_loc=args.preds,
        # Pass custom arguments to __init__ if needed
        # my_custom_param=args.my_custom_param
    )
    eval_task.calculate_metrics(by_guid=True) # or False, depending on your evaluation
    # ... further processing ...
    report = eval_task.write_report()
    args.export.write(report.getvalue())
```

Common command-line arguments (handled by `ClamsAAPBEvaluationTask`):
*   `-p`, `--preds`: Directory containing prediction MMIF files.
*   `-g`, `--golds`: Directory containing gold standard files.
*   `-e`, `--export`: Filename to export the Markdown report (defaults to stdout).
*   `-b`, `--batchname`: Batch name from the `aapb-annotations` repository.
*   `--source-directory`: Optional directory for original source files (e.g., large video files) if needed for evaluation.

### 4. Input Data Format

*   **Gold Files**: Typically `.tsv`, `.csv`, or `.txt` files. The `_read_gold` method in your subclass will interpret these.
*   **Prediction Files**: Always `.mmif` files (or rarely `.json`) generated by CLAMS workflows. The `_read_pred` method will parse these.

### 5. Report Generation

The `write_report()` method automatically generates a Markdown report including:
*   Evaluation task name and timestamp.
*   Docstring of your `YourEvaluationTask` class as the evaluation method description.
*   Data specifications (batch name, gold location, evaluation code version).
*   Workflow specifications (CLAMS workflow ID and app profilings).
*   Raw results (dumped as JSON or a custom string from `self._results`).
*   (Optional) Side-by-side view from `write_side_by_side_view()`.

### 6. Code Versioning

The framework automatically attempts to include the git commit hash of your evaluation script in the report, indicating whether the code is "dirty" (has uncommitted changes) or a specific commit. Ensure your evaluation scripts are part of a git repository for accurate version tracking.

## General Guidelines

*   **Modularity**: Keep your `_read_gold`, `_read_pred`, `_compare_pair`, and `_compare_all` methods focused on their specific tasks.
*   **Error Handling**: Implement robust error handling within your `_read_pred` method, especially for parsing potentially malformed MMIF files. Warnings for skipped GUIDs are automatically handled by the framework.
*   **Documentation**: Clearly document your `YourEvaluationTask` class and its methods, especially `_read_gold` and `_read_pred`, to explain the expected data formats and processing logic.
*   **Testing**: While not explicitly covered here, ensure you write unit tests for your custom `_read_gold`, `_read_pred`, and `_compare` methods.

By following these guidelines, you can effectively contribute new and robust evaluation tasks to the AAPB Evaluations project.
