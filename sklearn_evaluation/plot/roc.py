import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
from sklearn.preprocessing import label_binarize


def roc(y_true, y_score, ax=None):
    """
    Plot ROC curve.

    Parameters
    ----------
    y_true : array-like, shape = [n_samples]
        Correct target values (ground truth).
    y_score : array-like, shape = [n_samples, n_classes]
        Target scores (estimator predictions).
    ax: matplotlib Axes
        Axes object to draw the plot onto, otherwise uses current Axes

    Returns
    -------
    ax: matplotlib Axes
        Axes containing the plot

    """
    if ax is None:
        ax = plt.gca()

    # get the number of classes from y_score
    _, n_classes = y_score.shape

    # check data shape?

    if n_classes > 2:
        # convert y_true to binary format
        y_true_bin = label_binarize(y_true, classes=np.unique(y_true))
        _roc_multi(y_true_bin, y_score, ax=ax)
        for i in range(n_classes):
            _roc(y_true_bin[:, i], y_score[:, i], ax=ax)
    else:
        _roc(y_true, y_score, ax)

    # raise error if n_classes = 1?
    return ax


def _roc(y_true, y_score, ax=None):
    """
    Plot ROC curve for binary classification.

    Parameters
    ----------
    y_true : array-like, shape = [n_samples]
        Correct target values (ground truth).
    y_score : array-like, shape = [n_samples]
        Target scores (estimator predictions).
    ax: matplotlib Axes
        Axes object to draw the plot onto, otherwise uses current Axes

    Returns
    -------
    ax: matplotlib Axes
        Axes containing the plot

    """
    # check dimensions

    fpr, tpr, _ = roc_curve(y_true, y_score)
    roc_auc = auc(fpr, tpr)

    ax.plot(fpr, tpr, label=('ROC curve (area = {0:0.2f})'.format(roc_auc)))

    ax.plot([0, 1], [0, 1], 'k--')
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])
    ax.set_xlabel('False Positive Rate')
    ax.set_ylabel('True Positive Rate')
    ax.set_title('ROC')
    ax.legend(loc="best")
    return ax


def _roc_multi(y_true, y_score, ax=None):
    """
    Plot ROC curve for multi classification.

    Parameters
    ----------
    y_true : array-like, shape = [n_samples, n_classes]
        Correct target values (ground truth).
    y_score : array-like, shape = [n_samples, n_classes]
        Target scores (estimator predictions).
    ax: matplotlib Axes
        Axes object to draw the plot onto, otherwise uses current Axes

    Returns
    -------
    ax: matplotlib Axes
        Axes containing the plot

    """
    # Compute micro-average ROC curve and ROC area
    fpr, tpr, _ = roc_curve(y_true.ravel(), y_score.ravel())
    roc_auc = auc(fpr, tpr)

    if ax is None:
        ax = plt.gca()

    ax.plot(fpr, tpr, label=('micro-average ROC curve (area = {0:0.2f})'
                             .format(roc_auc)))

    ax.plot([0, 1], [0, 1], 'k--')
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])
    ax.set_xlabel('False Positive Rate')
    ax.set_ylabel('True Positive Rate')
    ax.set_title('ROC')
    ax.legend(loc="lower right")
    return ax