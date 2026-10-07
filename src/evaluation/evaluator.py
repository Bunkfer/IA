# src/evaluation/model_evaluator.py

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)


class ModelEvaluator:

    def __init__(self, y_true, y_pred):
        self.y_true = y_true
        self.y_pred = y_pred

    def evaluate(self) -> dict:
        """Calculate classification performance metrics."""

        results = {
            "accuracy": accuracy_score(self.y_true, self.y_pred),
            "precision": precision_score(
                self.y_true, self.y_pred, average="weighted", zero_division=0
            ),
            "recall": recall_score(
                self.y_true, self.y_pred, average="weighted", zero_division=0
            ),
            "f1_score": f1_score(
                self.y_true, self.y_pred, average="weighted", zero_division=0
            ),
        }

        return results

    def confusion_matrix(self):
        """Generate the confusion matrix."""

        return confusion_matrix(self.y_true, self.y_pred)

    def print_results(self) -> None:
        """Print evaluation metrics."""

        results = self.evaluate()

        print("\nModel Evaluation")
        print("----------------")
        print(f"Accuracy : {results['accuracy']:.4f}")
        print(f"Precision: {results['precision']:.4f}")
        print(f"Recall   : {results['recall']:.4f}")
        print(f"F1-score : {results['f1_score']:.4f}")

        print("\nConfusion Matrix")
        print("----------------")
        print(self.confusion_matrix())
