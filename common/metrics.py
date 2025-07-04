"""
Module to provide some evaluation metrics commonly used in AAPB-CLAMS 
collaboration. Usually providing wrappers around existing libraries, such
as scipy, jiwer, etc. to provide a common interface for evaluation.

"""
from sklearn.metrics import precision_recall_fscore_support as skprecision_recall_fscore_support
from sklearn.metrics import classification_report as skclassification_report
import jiwer 


def casing_text(text, ignore_case):
    """Includes any text preprocessing we would like to add, currently only casing"""
    if ignore_case:
        text = text.upper()
    return text


def wer(pred_text, gold_text, exact_case):
    pred = casing_text(pred_text, not exact_case)
    gold = casing_text(gold_text, not exact_case)
    return jiwer.wer(pred, gold)


def cer(pred_text, gold_text, exact_case):
    pred = casing_text(pred_text, not exact_case)
    gold = casing_text(gold_text, not exact_case)
    return jiwer.cer(pred, gold)


def precision_recall_fscore(y_true, y_pred, **kwargs):
    """
    Wrapper for sklearn.metrics.precision_recall_fscore_support
    See https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_recall_fscore_support.html#sklearn.metrics.precision_recall_fscore_support
    for more information.
    """
    p, r, f, s = skprecision_recall_fscore_support(y_true, y_pred, **kwargs)
    return p, r, f


def classification_report(y_true, y_pred, **kwargs):
    """
    Wrapper for sklearn.metrics.classification_report
    See https://scikit-learn.org/stable/modules/generated/sklearn.metrics.classification_report.html#sklearn.metrics.classification_report
    for more information.
    """
    return skclassification_report(y_true, y_pred, **kwargs)