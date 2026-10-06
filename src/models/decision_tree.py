from sklearn.tree import DecisionTreeClassifier


class DecisionTreeModel:

    def __init__(self):
        self.model = DecisionTreeClassifier(
            random_state=42
        )

    def train(self, X_train, y_train) -> None:
        """Train the Decision Tree model."""

        self.model.fit(X_train, y_train)

        print("Decision Tree model trained successfully.")

    def predict(self, X_test):
        """Generate predictions using the trained model."""

        return self.model.predict(X_test)