import pandas as pd

from src.visualitation.excel_reporter import ExcelVisualizer


class DataAnalyzer:

    def __init__(self, file_path: str, excel_visualizer: ExcelVisualizer):
        self.file_path = file_path
        self.excel_visualizer = excel_visualizer
        self.data = None

    def load_data(self) -> pd.DataFrame:
        """Load the dataset from a CSV file."""

        self.data = pd.read_csv(self.file_path)

        print("\nDataset loaded successfully.")
        print(f"Shape: {self.data.shape}")

        return self.data

    def get_summary(self) -> dict:
        """Return general dataset information."""

        self._validate_data()

        return {
            "Rows": self.data.shape[0],
            "Columns": self.data.shape[1],
            "Duplicate Rows": self.data.duplicated().sum(),
            "Numeric Columns": len(self.get_numeric_columns()),
            "Non-Numeric Columns": len(self.get_non_numeric_columns()),
        }

    def get_columns(self) -> pd.DataFrame:
        """Return dataset columns and their data types."""

        self._validate_data()

        return pd.DataFrame(
            {
                "Column": self.data.columns,
                "Data Type": self.data.dtypes.astype(str).values,
            }
        )

    def get_missing_values(self) -> pd.DataFrame:
        """Return missing values information."""

        self._validate_data()

        missing_count = self.data.isnull().sum()

        return pd.DataFrame(
            {
                "Column": missing_count.index,
                "Missing Values": missing_count.values,
                "Percentage": (self.data.isnull().mean().mul(100).round(2).values),
            }
        )

    def get_duplicates(self) -> pd.DataFrame:
        """Return duplicate rows information."""

        self._validate_data()

        duplicate_count = self.data.duplicated().sum()

        return pd.DataFrame({"Metric": ["Duplicate Rows"], "Value": [duplicate_count]})

    def get_statistics(self) -> pd.DataFrame:
        """Return descriptive statistics."""

        self._validate_data()

        return self.data.describe().transpose()

    def get_unique_values(self) -> pd.DataFrame:
        """Return unique values per column."""

        self._validate_data()

        unique_values = self.data.nunique()

        return pd.DataFrame(
            {"Column": unique_values.index, "Unique Values": unique_values.values}
        )

    def get_target_distribution(self, target_column: str) -> pd.DataFrame:
        """Return target class distribution."""

        self._validate_target_column(target_column)

        counts = self.data[target_column].value_counts()

        percentages = (
            self.data[target_column].value_counts(normalize=True).mul(100).round(2)
        )

        return pd.DataFrame(
            {
                "Class": counts.index.astype(str),
                "Count": counts.values,
                "Percentage": percentages.values,
            }
        )

    def get_numeric_columns(self) -> list:
        """Return numeric columns."""

        self._validate_data()

        return self.data.select_dtypes(include="number").columns.tolist()

    def get_non_numeric_columns(self) -> list:
        """Return non-numeric columns."""

        self._validate_data()

        return self.data.select_dtypes(exclude="number").columns.tolist()

    def export_analysis(self, target_column: str = None) -> None:
        """Export dataset analysis to Excel."""

        self._validate_data()

        print("Generating Excel analysis...")

        self.excel_visualizer.write_dict(
            data=self.get_summary(), sheet_name="Dataset Summary"
        )

        self.excel_visualizer.write_dataframe(
            data=self.get_columns(), sheet_name="Columns", index=False
        )

        self.excel_visualizer.write_dataframe(
            data=self.get_missing_values(), sheet_name="Missing Values", index=False
        )

        self.excel_visualizer.write_dataframe(
            data=self.get_duplicates(), sheet_name="Duplicates", index=False
        )

        self.excel_visualizer.write_dataframe(
            data=self.get_unique_values(), sheet_name="Unique Values", index=False
        )

        self.excel_visualizer.write_dataframe(
            data=self.get_statistics(), sheet_name="Statistics"
        )

        if target_column is not None:
            self.excel_visualizer.write_dataframe(
                data=self.get_target_distribution(target_column),
                sheet_name="Target Analysis",
                index=False,
            )

        print("Excel analysis completed successfully.")

    def _validate_data(self) -> None:
        """Validate that the dataset has been loaded."""

        if self.data is None:
            raise RuntimeError(
                "Dataset has not been loaded. " "Call load_data() first."
            )

    def _validate_target_column(self, target_column: str) -> None:
        """Validate that the target column exists."""

        self._validate_data()

        if target_column not in self.data.columns:
            raise ValueError(
                f"Target column '{target_column}' " "was not found in the dataset."
            )
