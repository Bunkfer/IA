from sklearn.naive_bayes import GaussianNB


class NaiveBayesModel:

    def __init__(self):
        self.model = GaussianNB()

    def train(self, X_train, y_train) -> None:
        """Train the Naive Bayes model."""

        self.model.fit(X_train, y_train)

        print("Naive Bayes model trained successfully.")

    def predict(self, X_test):
        """Generate predictions using the trained model."""

        return self.model.predict(X_test)
