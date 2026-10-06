from sklearn.ensemble import RandomForestClassifier


class RandomForestModel:

    def __init__(self):
        self.model = RandomForestClassifier(
            random_state=42
        )

    def train(self, X_train, y_train) -> None:
        """Train the Random Forest model."""

        self.model.fit(X_train, y_train)

        print("Random Forest model trained successfully.")

    def predict(self, X_test):
        """Generate predictions using the trained model."""

        return self.model.predict(X_test)