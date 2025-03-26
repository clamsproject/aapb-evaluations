"""
Module to provide some evaluation metrics commonly used in AAPB-CLAMS 
collaboration. Usually providing wrappers around existing libraries, such
as scipy, jiwer, etc. to provide a common interface for evaluation.

"""
from sklearn.metrics import precision_recall_fscore_support as skprecision_recall_fscore_support

def precision_recall_fscore(y_true, y_pred, **kwargs):
    """
    Wrapper for sklearn.metrics.precision_recall_fscore_support
    See https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_recall_fscore_support.html#sklearn.metrics.precision_recall_fscore_support
    for more information.
    """
    p, r, f, s = skprecision_recall_fscore_support(y_true, y_pred, **kwargs)
    return p, r, f

