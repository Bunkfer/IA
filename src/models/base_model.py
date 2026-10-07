from config import balance_dataset
from src.evaluation.evaluator import ModelEvaluator


class Base_Model:

    def __init__(self, model, dataset):

        self.model = model
        self.dataset = dataset

        print("\nRaw data")
        self.base_train(dataset.X_train, dataset.y_train)
        self.base_evaluator()

        if balance_dataset:

            print("\nBalanced data")
            self.base_train(dataset.X_train_balanced, dataset.y_train_balanced)
            self.base_evaluator()

    def base_train(self, X_train, y_train):

        self.model.train(X_train, y_train)

        self.predictions = self.model.predict(self.dataset.X_test)

        print("Predictions generated.")
        print(f"Predictions: {len(self.predictions)}")

    def base_evaluator(self):

        evaluator = ModelEvaluator(y_true=self.dataset.y_test, y_pred=self.predictions)

        evaluator.print_results()
