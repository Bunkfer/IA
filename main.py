"""
El preproceso nos termina dando datos X y Y
X: son las caracteristicas que vamos a considerar
Y: son las variables objetivo
"""

from config import *

from src.data.analizer import DataAnalyzer
from src.data.preprocessor import DataPreprocessor
from src.visualitation.excel_reporter import ExcelVisualizer

from src.data.dataset import DatasetSplit

from src.models.base_model import Base_Model
from src.models.naive_bayes import NaiveBayesModel
from src.models.decision_tree import DecisionTreeModel
from src.models.random_forest import RandomForestModel
from src.models.svm import SVMModel
from src.models.cnn import CNNModel


def main():

    # --------------------------------------
    # Carga de datos
    # --------------------------------------
    excel_visualizer = ExcelVisualizer(analizer_report)
    analyzer = DataAnalyzer(file_path=file_path, excel_visualizer=excel_visualizer)
    data = analyzer.load_data()
    analyzer.export_analysis(target_column=target_column)

    # --------------------------------------
    # Preprocesamiento de datos
    # --------------------------------------
    print("\nStarting Preprocessing")
    preprocessor_visualizer = ExcelVisualizer(preprocessor_report)
    preprocessor = DataPreprocessor(
        data=data,
        target_column=target_column,
        test_size=test_size,
        random_state=random_state,
        preprocessor_visualizer=preprocessor_visualizer,
        balance_dataset=balance_dataset,
        smote_alg=smote_alg,
        balance_ratio=balance_ratio,
        minimum_minority_samples=minimum_minority_samples,
        preprocessor_report_enable=preprocessor_report_enable,
    )
    (
        X_train,
        X_train_balanced,
        X_test,
        X_test_balanced,
        y_train,
        y_train_balanced,
        y_test,
        y_test_balanced,
    ) = preprocessor.prepare(columns_to_remove=columns_to_remove, scale=False)

    dataset = DatasetSplit(
        X_train=X_train,
        X_train_balanced=X_train_balanced,
        X_test=X_test,
        X_test_balanced=X_test_balanced,
        y_train=y_train,
        y_train_balanced=y_train_balanced,
        y_test=y_test,
        y_test_balanced=y_test_balanced,
    )

    print("Preprocessing completed.")

    # --------------------------------------
    # Naive-bayes
    # --------------------------------------
    model_NBayes = Base_Model(NaiveBayesModel(), dataset)

    # --------------------------------------
    # Desicion Tree
    # --------------------------------------
    # model_DTree = Base_Model(DecisionTreeModel(), dataset)

    # --------------------------------------
    # Random Forest
    # --------------------------------------
    # model_RForest = Base_Model(RandomForestModel(), dataset)

    # --------------------------------------
    # SVM
    # --------------------------------------
    # model_SVM = Base_Model(SVMModel(), dataset)

    # --------------------------------------
    # Redes Neuronales
    # --------------------------------------
    # model_CNN = Base_Model(CNNModel(), dataset)


if __name__ == "__main__":
    main()
