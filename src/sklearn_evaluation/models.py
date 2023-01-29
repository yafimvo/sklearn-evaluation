from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix, auc
import numpy as np
import re
from sklearn_evaluation.evaluator import _gen_ax
from sklearn_evaluation import plot
from sklearn_evaluation.model_heuristics.utils import (
    check_array_balance,
    get_model_computation_time,
    get_roc_auc,
    Range,
)
from sklearn_evaluation.model_heuristics.model_heuristics import ModelHeuristics


class ReportSection:
    """
    Section to include in report
    """

    def __init__(self, key, include_in_report=True):
        self.report_section = dict(
            {
                "guidelines": [],
                "title": key.replace("_", " "),
                "include_in_report": include_in_report,
                "is_ok": False,
            }
        )
        self.key = key

    def append_guideline(self, guideline):
        """
        Add guideline to section

        Parameters
        ----------
        guideline : str
            The guideline to add
        """
        self.report_section["guidelines"].append(guideline)

    def get_dict(self) -> dict:
        """
        Return dict of the section
        """
        return self.report_section

    def set_is_ok(self, is_ok):
        """
        Set if the reported test is valid
        """
        self.report_section["is_ok"] = is_ok

    def set_include_in_report(self, include):
        """
        Set if should include this section in the report
        """
        self.report_section["include_in_report"] = include


class ModelEvaluator(ModelHeuristics):
    """
    Generates model evaluation report
    """

    def __init__(self, model):
        self.model = model
        super().__init__()

    def evaluate_balance(self, y_true):
        """
        Checks if model is balanced
        """
        balance_section = ReportSection("balance")

        is_balanced = check_array_balance(y_true)

        if is_balanced:
            balance_section.set_is_ok(True)
            balance_section.append_guideline("your model is balanced")
        else:
            balance_section.set_is_ok(False)
            p = plot.target_analysis(y_true)
            balance_section.append_guideline("Your test set is highly imbalanced")
            balance_section.append_guideline(p)
            balance_section.append_guideline(
                "To tackle this, check out this "
                "<a href='https://ploomber.io/blog/' target='_blank'>guide</a>"
            )

        self._add_section_to_report(balance_section)

    def evaluate_accuracy(self, y_true, y_pred_test):
        """
        Measures how many labels the
        model got right out of the total number of predictions
        """
        accuracy_threshold = 0.9
        accuracy_section = ReportSection("accuracy")
        accuracy = accuracy_score(y_true, y_pred_test)

        balance = self.evaluation_state["balance"]

        accuracy_section.append_guideline(f"Accuracy is {accuracy}")
        if accuracy >= accuracy_threshold:
            if balance["is_ok"]:
                accuracy_section.append_guideline["is_ok"] = True
                accuracy_section.append_guideline("You model is accurate")
            else:
                accuracy_section.set_is_ok(False)
                accuracy_section.append_guideline(
                    "Please note your model is unbalanced, "
                    "so high accuracy could be misleading"
                )

        self._add_section_to_report(accuracy_section)

    def evaluate_confusion_matrix(y_true, y_pred):
        """
        Checks how many of a classifier's predictions were correct,
        and when incorrect, where the classifier got confused
        """
        # TODO: Implement
        cm = confusion_matrix(y_true, y_pred)

        # normalize
        cm = cm.astype("float") / cm.sum(axis=1)[:, np.newaxis]

        # TODO: Evaluate model by confusion matrix
        diagonal = np.diagonal(cm)  # noqa

    def evaluate_auc(self, y_true, y_score):
        """
        Checks if roc auc is in acceptable range
        """
        auc_section = ReportSection("auc")

        auc_threshold_low_range = Range(0, 0.6)
        auc_threshold_acceptable_range = Range(0.7, 0.8)

        # auc - roc
        roc = plot.ROC.from_raw_data(y_true, y_score)
        for i in range(len(roc.fpr)):
            roc_auc = auc(roc.fpr[i], roc.tpr[i])

            # todo: better check
            label = roc.label[i] if len(roc.label) > 0 else f"class {i}"
            r = re.match(r"^\(class (.)*\)", label)
            if r:
                class_name = r[0].replace("(", "").replace(")", "")
            else:
                class_name = label

            if auc_threshold_low_range.in_range(roc_auc):
                auc_section.append_guideline(
                    f"Area under curve is low for {class_name}"
                )
                class_roc = plot.ROC(roc.fpr[i], roc.tpr[i], label=[label]).plot().ax
                auc_section.append_guideline(class_roc)

                auc_section.append_guideline(
                    "To tackle this, check out this "
                    "<a href='https://ploomber.io/blog/' target='_blank'>guide</a>"
                )
            elif auc_threshold_acceptable_range.in_range(roc_auc):
                auc_section.set_is_ok(True)
                auc_section.set_include_in_report(False)
            else:
                auc_section.set_is_ok(True)
                auc_section.set_include_in_report(False)

        self._add_section_to_report(auc_section)

    def generate_general_stats(self, y_true, y_pred, y_score):
        """
        Include general stats in the report
        """
        general_section = ReportSection("general_stats")

        general_section.append_guideline(
            plot.confusion_matrix(y_true, y_pred, ax=_gen_ax())
        )
        general_section.append_guideline(plot.roc(y_true, y_score, ax=_gen_ax()))
        self._add_section_to_report(general_section)


class ModelComparer(ModelHeuristics):
    """
    Compares models and generate report
    """

    def __init__(self, model_a, model_b):
        self.model_a = model_a
        self.model_b = model_b
        super().__init__()

    def precision_and_recall(self, X_test, y_true):
        """
        Calculates precision and recall for each of the models
        """
        percision_recall_section = ReportSection("percision_recall")

        try:
            y_prob_a = self.model_a.predict_proba(X_test)
            p = plot.precision_recall(y_true, y_prob_a, ax=_gen_ax())
            percision_recall_section.append_guideline(p)

        except Exception as exc:
            percision_recall_section.append_guideline(
                self._get_calculate_failed_error("percision_recall", "model A", exc=exc)
            )

        try:
            y_prob_b = self.model_b.predict_proba(X_test)
            p = plot.precision_recall(y_true, y_prob_b, ax=_gen_ax())
            percision_recall_section.append_guideline(p)

        except Exception as exc:
            percision_recall_section.append_guideline(
                self._get_calculate_failed_error("percision_recall", "model B", exc=exc)
            )

        self._add_section_to_report(percision_recall_section)

    def auc(self, X_test, y_true):
        """
        Compares models roc auc
        """
        auc_section = ReportSection("auc")

        try:
            y_score_a = self.model_a.predict_proba(X_test)
            roc_auc_model_a = get_roc_auc(y_true, y_score_a)

            if len(roc_auc_model_a) > 1:
                auc_section.append_guideline(f"Model A AUC (ROC) are {roc_auc_model_a}")
            else:
                auc_section.append_guideline(
                    f"Model A AUC (ROC) is {roc_auc_model_a[0]}"
                )
        except Exception as exc:
            auc_section.append_guideline(
                self._get_calculate_failed_error("auc", "model A", exc=exc)
            )

        try:
            y_score_b = self.model_b.predict_proba(X_test)
            roc_auc_model_b = get_roc_auc(y_true, y_score_b)

            if len(roc_auc_model_b) > 1:
                auc_section.append_guideline(f"Model B AUC (ROC) are {roc_auc_model_b}")
            else:
                auc_section.append_guideline(
                    f"Model B AUC (ROC) is {roc_auc_model_b[0]}"
                )
        except Exception as exc:
            auc_section.append_guideline(
                self._get_calculate_failed_error("auc", "model B", exc=exc)
            )

        self._add_section_to_report(auc_section)

    def computation(self, X_test):
        """
        Compares models compute time
        """
        computation_section = ReportSection("computation")

        model_a_compute_time = get_model_computation_time(self.model_a, X_test)
        model_b_compute_time = get_model_computation_time(self.model_b, X_test)

        compute_time_diff_threshold = 1  # 1 second
        is_significant_time_diff = (
            abs(model_a_compute_time - model_b_compute_time)
            >= compute_time_diff_threshold
        )
        if is_significant_time_diff:
            if model_a_compute_time > model_b_compute_time:
                computation_section.append_guideline(
                    "Model A is a lot more computational expensive"
                )
            else:
                computation_section.append_guideline(
                    "Model B is a lot more computational expensive"
                )

        computation_section.append_guideline(
            f"Model A compute time is {model_a_compute_time} (seconds)"
        )
        computation_section.append_guideline(
            f"Model B compute time is {model_b_compute_time} (seconds)"
        )

        self._add_section_to_report(computation_section)

    def calibration(self, X_test, y_true):
        """
        Compares models calibration
        """
        calibration_section = ReportSection("calibration")

        try:
            y_prob_a = self.model_a.predict_proba(X_test)
            p = plot.calibration_curve([y_true], [y_prob_a], ax=_gen_ax())
            calibration_section.append_guideline(p)
        except Exception as exc:
            calibration_section.append_guideline(
                self._get_calculate_failed_error("calibration", "model A", exc=exc)
            )

        try:
            y_prob_b = self.model_b.predict_proba(X_test)
            p = plot.calibration_curve([y_true], [y_prob_b], ax=_gen_ax())
            calibration_section.append_guideline(p)
        except Exception as exc:
            calibration_section.append_guideline(
                self._get_calculate_failed_error("calibration", "model B", exc=exc)
            )

        self._add_section_to_report(calibration_section)

    def add_combined_cm(self, X_test, y_true):
        combined_confusion_matrix_section = ReportSection("combined_confusion_matrix")

        y_score_a = self.model_a.predict(X_test)
        y_score_b = self.model_b.predict(X_test)

        model_a_cm = plot.ConfusionMatrix.from_raw_data(y_true, y_score_a)
        model_b_cm = plot.ConfusionMatrix.from_raw_data(y_true, y_score_b)

        combined = model_a_cm + model_b_cm
        combined_confusion_matrix_section.append_guideline(combined.plot())
        self._add_section_to_report(combined_confusion_matrix_section)


def evaluate_model(y_true, y_pred, model, y_score=None):
    _check_model(model)
    _check_inputs(y_true, y_pred)
    me = ModelEvaluator(model)

    # check imbalance
    me.evaluate_balance(y_true)

    # accuracy score
    me.evaluate_accuracy(y_true, y_pred)

    # auc
    me.evaluate_auc(y_true, y_score)

    # add general stats
    me.generate_general_stats(y_true, y_pred, y_score)

    report = me.create_report("Model evaluation")
    return report


def compare_models(model_a, model_b, X_train, X_test, y_true):
    _check_model(model_a)
    _check_model(model_b)

    mc = ModelComparer(model_a, model_b)

    mc.precision_and_recall(X_test, y_true)

    mc.auc(X_test, y_true)

    mc.computation(X_test)

    mc.calibration(X_test, y_true)

    mc.add_combined_cm(X_test, y_true)

    report = mc.create_report("Compare models")
    return report


def _check_model(model) -> None:
    """
    Validate if model supported

    Raises
    ~~~~~~
    ModelNotSupported or ValueError?
    """
    # TODO: Implement
    pass


def _check_inputs(y_true, y_pred) -> None:
    """
    Validate if inputs supported

    Raises
    ~~~~~~
    ModelNotSupported or ValueError?
    """
    # TODO: Implement
    # TODO: If optional args given test them
    pass