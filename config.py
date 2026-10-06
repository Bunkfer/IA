# -----------------------
# Datos del Archivo DNS
# -----------------------
columns_to_remove = ["SourceIP", "DestinationIP", "TimeStamp"]
target_column = "DoH"
file_path = "data/all_benign.csv"


# -----------------------
# Parametros generales
# -----------------------
# Preprocessing
test_size = 0.2
random_state = 42

# Dataset balancing
balance_dataset = True
smote_alg = True
preprocessor_report_enable = False
balance_ratio = 3
minimum_minority_samples = 2000


# -----------------------
# Reportes Resultados
# -----------------------
analizer_report = "results/analysis_results.xlsx"
preprocessor_report = "results/preprocessor_result.xlsx"
