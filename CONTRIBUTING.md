# Contributing to AAPB Evaluations

Welcome to the AAPB Evaluations repository! This guide will help you understand how to contribute new evaluation tasks for CLAMS applications.

## Purpose of This Repository

This repository provides a framework for evaluating the performance of CLAMS apps in various metadata extraction tasks on AAPB-based datasets. Primary component you can contribute is `evaluate.py` scripts within each evaluation task directory. Each script is responsible for processing gold standard annotations and CLAMS app outputs, calculating relevant metrics, and generating comprehensive reports.

## Core Concepts: `ClamsAAPBEvaluationTask`

At the heart of every `evaluate.py` is the `ClamsAAPBEvaluationTask` abstract base class (ABC) defined in `common/__init__.py`. This class provides the foundational structure and common utilities needed to develop new evaluation tasks, including:

* Standardized Input Handling: Mechanisms to locate and process gold standard (human-annotated) files and prediction (CLAMS app/workflow output) files.
* Metric Calculation Orchestration: A workflow for comparing gold and prediction data, calculating relevant metrics.
* Report Generation: Tools to automatically generate formatted Markdown reports summarizing evaluation results.

The `common` package also provides shared utilities:

* `common/metrics.py`: Wrappers around evaluation metrics from `sklearn` and `jiwer`, including `precision_recall_fscore`, `wer`/`cer`, and metric key constants (`MACRO_AVG_PRECISION`, `MACRO_AVG_RECALL`, `MACRO_AVG_F1`).
* `common/helpers.py`: Utility functions for timestamp and range matching, such as `match_nearest_points` and `find_range_index`.

See the docstrings in each module for detailed signatures and usage.

## Implementing a New Evaluation Task

To contribute a new evaluation, create a new Python module (e.g., `YourEvaluationTask/evaluate.py`) that subclasses `ClamsAAPBEvaluationTask` and implements its abstract methods. See `TimePointLabeling/evaluate.py` as a reference implementation.

### 1. Subclassing `ClamsAAPBEvaluationTask`

```python
from common import ClamsAAPBEvaluationTask

class YourEvaluationTask(ClamsAAPBEvaluationTask):
    """
    Describe what this evaluation task assesses, the metrics
    used, and any configurable behavior.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
```

The class docstring is rendered verbatim in the "Evaluation method" section of the generated Markdown report. Write it as user-facing documentation using Markdown formatting — describe the methodology, metrics, and any configurable behavior.

### 2. Implementing Core Abstract Methods

You **must** implement the following methods. See the docstrings in `common/__init__.py` for detailed parameter and return type documentation.

*   `_read_gold(self, gold_file, **kwargs)`: Read a single gold standard file and return processed data suitable for comparison.
*   `_read_pred(self, pred_file, gold, **kwargs)`: Read a prediction MMIF file and return a `(pred, updated_gold)` tuple. The `gold` parameter is the output of `_read_gold` for the same GUID. When your task requires aligning gold and prediction data (e.g., matching timestamps), return the aligned gold as the second element — it will replace the original gold passed to `_compare_pair`. Return `None` as the second element if gold needs no modification.
*   `_compare_pair(self, guid, gold, pred)`: Calculate evaluation metrics for a single document.
*   `_compare_all(self, golds, preds)`: Calculate aggregate metrics across all documents (used when `by_guid=False`). Raise `NotImplementedError` if your task only supports per-GUID evaluation.

### 3. Finalizing Scores

You **must** implement `_finalize_results(self)`, which is called automatically by `write_report()` before rendering. This method aggregates per-GUID results into a final form suitable for the report.

The data flow is:

1. `_compare_pair` stores per-GUID metrics in `self._calculations` (a `dict` keyed by GUID).
1. `_finalize_results` reads from `self._calculations`, computes aggregates (e.g., an overall average row), and writes the final output to `self._results`.
1. `write_report()` renders `self._results` in the report. The type of `self._results` determines the rendering format — see the `_finalize_results` and `write_report` docstrings for supported types.

### 4. Additional, Human-Friendly Report Formats

The base class supports two optional report sections — a confusion matrix and a side-by-side view — controlled by constructor kwargs `cf` and `sbs`. Pass these in your `__init__` before calling `super().__init__()`:

```python
def __init__(self, batchname, **kwargs):
    # enable confusion matrix in the report
    super().__init__(batchname, cf=True, **kwargs)
```

* `cf=True`: Appends a "Confusion Matrix" section by calling `write_confusion_matrix()`.
* `sbs=True`: Appends a "Side-by-side view" section by calling `write_side_by_side_view()`.

Both methods are **abstract**. Every subclass must implement them, even when the evaluation doesn't use that format — in which case, raise `NotImplementedError`. Each method should return a Markdown-formatted string.

### 5. Complex Label Remapping at Evaluation Time

For classification tasks where gold and prediction label vocabularies differ, the base class provides label mapping infrastructure through CLI arguments, a parsing helper, and automatic report rendering.

The `prep_argparser()` method adds three label-related CLI arguments:

* `--label-map`: Space-separated mappings. Supports identity format (`A B C`) and explicit mapping (`A:x B:x C:y`). Target values are automatically identity-mapped to handle predictions using pre-collapsed labels.
* `--label-map-json`: JSON string alternative, mutually exclusive with `--label-map`.
* `--default-label`: Fallback label for unmapped entries (default: `"-"`).

Use `parse_label_map_args(args)` to convert parsed CLI args into a normalized `dict`, then pass it to your evaluator's constructor:

```python
args = parser.parse_args()
label_map = YourEvaluationTask.parse_label_map_args(args)
evaluator = YourEvaluationTask(
    batchname=args.batchname,
    label_map=label_map,
    default_label=args.default_label,
    ...
)
```

When a label map is present, `write_report()` automatically includes the full mapping table in the report.

To surface other task-specific settings in the report (e.g., matching tolerance, thresholds), populate a `self._eval_config` dict in your `__init__`:

```python
self._eval_config = {'Timestamp matching tolerance': '5ms'}
```

Each key-value pair is rendered as a bullet in the "Data and Evaluation Specs" section.

### 6. Command-Line Interface (`prep_argparser`)

The `ClamsAAPBEvaluationTask` provides a default argument parser via `prep_argparser()`. Call this method and add task-specific arguments:

```python
if __name__ == '__main__':
    parser = YourEvaluationTask.prep_argparser()
    parser.add_argument('--my-param', type=int, help='...')
    args = parser.parse_args()

    label_map = YourEvaluationTask.parse_label_map_args(args)

    eval_task = YourEvaluationTask(
        batchname=args.batchname,
        gold_loc=args.golds,
        pred_loc=args.preds,
        label_map=label_map,
        default_label=args.default_label,
    )
    eval_task.calculate_metrics(by_guid=True)
    report = eval_task.write_report()
    args.export.write(report.getvalue())
```

Common arguments provided by the base class:

*   `-p`, `--preds`: Directory containing prediction MMIF files.
*   `-g`, `--golds`: Directory containing gold standard files.
*   `-e`, `--export`: Filename to export the Markdown report (defaults to stdout).
*   `-b`, `--batchname`: Batch name from the `aapb-annotations` repository.
*   `--source-directory`: Optional directory for original source files.
*   `--label-map`, `--label-map-json`, `--default-label`: Label remapping options (see Section 5).

### 7. Input Data Format

*   Gold files: Typically `.tsv`, `.csv`, or `.txt` files. The `_read_gold` method in your subclass will interpret these.
*   Prediction files: Always `.mmif` files (or rarely `.json`) generated by CLAMS workflows. The `_read_pred` method will parse these.

### 8. Report Generation

The `write_report()` method automatically generates a Markdown report including:

*   Evaluation task name and timestamp.
*   Class docstring as the evaluation method description.
*   Data and evaluation specs (batch name, gold location, code version, label mapping, `_eval_config` entries).
*   Workflow specs (CLAMS workflow ID and app profilings).
*   Raw results (rendering depends on `self._results` type — see Section 3).
*   Optional confusion matrix and/or side-by-side view (see Section 4).

### 9. Code Versioning

The framework automatically includes the git commit hash of your evaluation script in the report, indicating whether the code is "dirty" (has uncommitted changes) or a specific commit. Ensure your evaluation scripts are part of a git repository for accurate version tracking.

## General Guidelines

*   Modularity: Keep your `_read_gold`, `_read_pred`, `_compare_pair`, and `_compare_all` methods focused on their specific tasks.
*   Error handling: Implement robust error handling within your `_read_pred` method, especially for parsing potentially malformed MMIF files. Warnings for skipped GUIDs are automatically handled by the framework.
*   Documentation: Write your class docstring as user-facing methodology documentation. Document `_read_gold` and `_read_pred` to explain expected data formats.
*   Testing: Ensure you write unit tests for your custom `_read_gold`, `_read_pred`, and `_compare` methods.

By following these guidelines, you can effectively contribute new and robust evaluation tasks to the AAPB Evaluations project.
