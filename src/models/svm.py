from sklearn.svm import SVC


class SVMModel:

    def __init__(self):
        self.model = SVC(
            random_state=42
        )

    def train(self, X_train, y_train) -> None:
        """Train the SVM model."""

        self.model.fit(X_train, y_train)

        print("SVM model trained successfully.")

    def predict(self, X_test):
        """Generate predictions using the trained model."""

        return self.model.predict(X_test)