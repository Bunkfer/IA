class DatasetSplit:

    def __init__(
        self,
        X_train,
        X_train_balanced,
        X_test,
        X_test_balanced,
        y_train,
        y_train_balanced,
        y_test,
        y_test_balanced,
    ):
        self.X_train = X_train
        self.X_train_balanced = X_train_balanced

        self.X_test = X_test
        self.X_test_balanced = X_test_balanced

        self.y_train = y_train
        self.y_train_balanced = y_train_balanced

        self.y_test = y_test
        self.y_test_balanced = y_test_balanced