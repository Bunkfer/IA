import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

from imblearn.over_sampling import SMOTE

class DataPreprocessor:

    def __init__(
        self,
        data: pd.DataFrame,
        target_column: str,
        test_size: float = 0.2,
        random_state: int = 42,
        preprocessor_visualizer=None,
        preprocessor_report_enable=False,
        balance_dataset: bool = False,
        smote_alg:bool= False,
        balance_ratio: int = 3,
        minimum_minority_samples: int = 0,
    ):
        self.data = data.copy()
        self.target_column = target_column
        self.test_size = test_size
        self.random_state = random_state

        self.preprocessor_visualizer = preprocessor_visualizer
        self.preprocessor_report_enable = preprocessor_report_enable

        self.balance_dataset = balance_dataset
        self.smote_alg = smote_alg
        self.balance_ratio = balance_ratio
        self.minimum_minority_samples = minimum_minority_samples

        self.X = None
        self.y = None

        self.X_train = None
        self.X_test = None

        self.y_train = None
        self.y_test = None

        self.X_train_balanced = None
        self.y_train_balanced = None

        self.X_test_balanced = None
        self.y_test_balanced = None

        self.scaler = None
        self.imputer = None

    def remove_columns(self, columns: list) -> None:
        """Remove specified columns from the dataset."""

        columns_to_remove = [
            column for column in columns if column in self.data.columns
        ]

        self.data.drop(columns=columns_to_remove, inplace=True)

        print(f"Columns removed: " f"{len(columns_to_remove)}")

    def separate_features_and_target(self) -> None:
        """Separate features and target."""

        self._validate_target_column()

        self.X = self.data.drop(columns=[self.target_column])

        self.y = self.data[self.target_column]

        self._validate_numeric_features()

    def _validate_numeric_features(self) -> None:
        """Validate that all features are numeric."""

        non_numeric_columns = self.X.select_dtypes(exclude="number").columns.tolist()

        if non_numeric_columns:
            raise TypeError(
                "The following features are not numeric: " f"{non_numeric_columns}"
            )

    def split_data(self) -> None:
        """Split the data into training and testing sets."""

        self._validate_features_and_target()

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X,
            self.y,
            test_size=self.test_size,
            random_state=self.random_state,
            stratify=self.y,  #Esta propiedad permite hacer una separacion por clases
        )

    def scale_data(self) -> None:
        """Scale training and testing data."""

        self._validate_split_data()

        self.scaler = StandardScaler()

        # Fit only with raw training data
        self.scaler.fit(self.X_train)

        # Raw training
        self.X_train = pd.DataFrame(
            self.scaler.transform(self.X_train),
            columns=self.X_train.columns,
            index=self.X_train.index,
        )

        # Raw testing
        self.X_test = pd.DataFrame(
            self.scaler.transform(self.X_test),
            columns=self.X_test.columns,
            index=self.X_test.index,
        )

    def prepare(
        self,
        columns_to_remove: list = None,
        scale: bool = False
    ) -> tuple:

        if columns_to_remove:
            self.remove_columns(columns_to_remove)

        self.separate_features_and_target()

        self.split_data()

        self.impute_missing_values()

        if scale:
            self.scale_data()

        self.balance_training_data()

        self.balance_testing_data()

        if self.preprocessor_report_enable:
            self.export_preprocessing_results()

        return (
            self.X_train,
            self.X_train_balanced,
            self.X_test,
            self.X_test_balanced,
            self.y_train,
            self.y_train_balanced,
            self.y_test,
            self.y_test_balanced,
        )

    def _validate_target_column(self) -> None:
        """Validate that the target column exists."""

        if self.target_column not in self.data.columns:
            raise ValueError(
                f"Target column " f"'{self.target_column}' " f"was not found."
            )

    def _validate_features_and_target(self) -> None:
        """Validate that features and target exist."""

        if self.X is None or self.y is None:
            raise RuntimeError("Features and target have not " "been separated.")

    def _validate_split_data(self) -> None:
        """Validate that the data has been split."""

        if self.X_train is None:
            raise RuntimeError("Data has not been split.")

    def impute_missing_values(self) -> None:
        """Replace missing numerical values with the median."""

        self._validate_features_and_target()

        self.imputer = SimpleImputer(strategy="median")

        # Fit only with raw training data
        self.imputer.fit(self.X_train)

        # Raw training
        self.X_train = pd.DataFrame(
            self.imputer.transform(self.X_train),
            columns=self.X_train.columns,
            index=self.X_train.index,
        )

        # Raw testing
        self.X_test = pd.DataFrame(
            self.imputer.transform(self.X_test),
            columns=self.X_test.columns,
            index=self.X_test.index,
        )
    
    def export_preprocessing_results(self) -> None:
        """Export preprocessing results to Excel."""

        if self.preprocessor_visualizer is None:
            return

        if self.balance_dataset:

            self.preprocessor_visualizer.write_dataframe(
                self.X_train_balanced,
                sheet_name="X_train_balanced"
            )

            self.preprocessor_visualizer.write_dataframe(
                self.y_train_balanced.to_frame(),
                sheet_name="y_train_balanced"
            )

            self.preprocessor_visualizer.write_dataframe(
                self.X_test_balanced,
                sheet_name="X_test_balanced"
            )

            self.preprocessor_visualizer.write_dataframe(
                self.y_test_balanced.to_frame(),
                sheet_name="y_test_balanced"
            )

    def balance_training_data(self) -> None:
        """Create a balanced version of the training dataset."""

        self._validate_split_data()

        self.X_train_balanced = self.X_train.copy()
        self.y_train_balanced = self.y_train.copy()

        if not self.balance_dataset:
            print("Dataset balancing disabled.")
            return

        print("\nClass distribution before balancing:")
        print(self.y_train.value_counts())

        if self.smote_alg:
            self._apply_smote_training()
        else:
            self._apply_undersampling_training()

        print("\nClass distribution after balancing:")
        print(self.y_train_balanced.value_counts())

    def _apply_undersampling_training(self) -> None:
        train_data = self.X_train.copy()

        train_data[self.target_column] = self.y_train.values

        class_counts = self.y_train.value_counts()

        minority_class = class_counts.idxmin()
        majority_class = class_counts.idxmax()

        minority_count = class_counts[minority_class]
        majority_count = class_counts[majority_class]

        if minority_count < self.minimum_minority_samples:
            raise ValueError(
                "\nIt is not possible to create a balanced training dataset.\n"
                f"Required minimum minority samples: "
                f"{self.minimum_minority_samples}\n"
                f"Available minority samples: {minority_count}"
            )

        desired_majority_count = minority_count * self.balance_ratio

        if desired_majority_count >= majority_count:
            raise ValueError(
                "\nIt is not possible to create a balanced training dataset "
                "with the requested ratio.\n"
                f"Minority samples: {minority_count}\n"
                f"Majority samples: {majority_count}\n"
                f"Requested ratio: 1:{self.balance_ratio}"
            )

        minority_data = train_data[
            train_data[self.target_column] == minority_class
        ]

        majority_data = train_data[
            train_data[self.target_column] == majority_class
        ]

        majority_data = majority_data.sample(
            n=desired_majority_count,
            random_state=self.random_state,
        )

        balanced_data = pd.concat(
            [minority_data, majority_data]
        )

        balanced_data = balanced_data.sample(
            frac=1,
            random_state=self.random_state,
        )

        self.X_train_balanced = balanced_data.drop(
            columns=[self.target_column]
        )

        self.y_train_balanced = balanced_data[self.target_column]

    def _apply_smote_training(self) -> None:
        class_counts = self.y_train.value_counts()

        minority_class = class_counts.idxmin()
        majority_class = class_counts.idxmax()

        minority_count = class_counts[minority_class]
        majority_count = class_counts[majority_class]

        if minority_count < self.minimum_minority_samples:
            raise ValueError(
                "\nIt is not possible to create a SMOTE training dataset.\n"
                f"Required minimum minority samples: "
                f"{self.minimum_minority_samples}\n"
                f"Available minority samples: {minority_count}"
            )

        smote = SMOTE(
            sampling_strategy=1.0,
            random_state=self.random_state,
        )

        X_resampled, y_resampled = smote.fit_resample(
            self.X_train,
            self.y_train
        )

        self.X_train_balanced = pd.DataFrame(
            X_resampled,
            columns=self.X_train.columns
        )

        self.y_train_balanced = pd.Series(
            y_resampled,
            name=self.target_column
        )

        balanced_data = pd.concat(
            [
                self.X_train_balanced,
                self.y_train_balanced
            ],
            axis=1
        )

        balanced_data = balanced_data.sample(
            frac=1,
            random_state=self.random_state
        )

        self.X_train_balanced = balanced_data.drop(
            columns=[self.target_column]
        )

        self.y_train_balanced = balanced_data[
            self.target_column
        ]

    def balance_testing_data(self) -> None:
        """Create a balanced version of the testing dataset."""

        self._validate_split_data()

        self.X_test_balanced = self.X_test.copy()
        self.y_test_balanced = self.y_test.copy()

        if not self.balance_dataset:
            return

        print("\nTest class distribution before balancing:")
        print(self.y_test.value_counts())

        if self.smote_alg:
            self._apply_smote_testing()
        else:
            self._apply_undersampling_testing()

        print("\nTest class distribution after balancing:")
        print(self.y_test_balanced.value_counts())

    def _apply_undersampling_testing(self) -> None:
        test_data = self.X_test.copy()

        test_data[self.target_column] = self.y_test.values

        class_counts = self.y_test.value_counts()

        minority_class = class_counts.idxmin()
        majority_class = class_counts.idxmax()

        minority_count = class_counts[minority_class]
        majority_count = class_counts[majority_class]

        desired_majority_count = minority_count * self.balance_ratio

        if desired_majority_count >= majority_count:
            print("\nRequested ratio cannot be applied.")
            print("Balanced test dataset was not created.")
            return

        minority_data = test_data[
            test_data[self.target_column] == minority_class
        ]

        majority_data = test_data[
            test_data[self.target_column] == majority_class
        ]

        majority_data = majority_data.sample(
            n=desired_majority_count,
            random_state=self.random_state,
        )

        balanced_data = pd.concat(
            [minority_data, majority_data]
        )

        balanced_data = balanced_data.sample(
            frac=1,
            random_state=self.random_state,
        )

        self.X_test_balanced = balanced_data.drop(
            columns=[self.target_column]
        )

        self.y_test_balanced = balanced_data[
            self.target_column
        ]

    def _apply_smote_testing(self) -> None:
        smote = SMOTE(
            sampling_strategy=1.0,
            random_state=self.random_state,
        )

        X_resampled, y_resampled = smote.fit_resample(
            self.X_test,
            self.y_test
        )

        self.X_test_balanced = pd.DataFrame(
            X_resampled,
            columns=self.X_test.columns
        )

        self.y_test_balanced = pd.Series(
            y_resampled,
            name=self.target_column
        )

        balanced_data = pd.concat(
            [
                self.X_test_balanced,
                self.y_test_balanced
            ],
            axis=1
        )

        balanced_data = balanced_data.sample(
            frac=1,
            random_state=self.random_state
        )

        self.X_test_balanced = balanced_data.drop(
            columns=[self.target_column]
        )

        self.y_test_balanced = balanced_data[
            self.target_column
        ]