# -----------------------
# Datos del Archivo DNS
# https://www.unb.ca/cic/datasets/dohbrw-2020.html
# -----------------------
columns_to_remove = ["SourceIP", "DestinationIP", "TimeStamp"]
target_column = "DoH"
file_path = "data/all_benign.csv"


# -----------------------
# Datos del archivo de aws
# https://www.unb.ca/cic/datasets/ids-2018.html
# -----------------------
"""columns_to_remove = ["Timestamp"]
target_column = "Label"
file_path = "data/Wednesday-14-02-2018_TrafficForML_CICFlowMeter.csv"
"""
# -----------------------
# Parametros generales
# -----------------------
# Preprocessing
test_size = 0.2
random_state = 42

# Dataset balancing
balance_dataset = False
smote_alg = True
preprocessor_report_enable = False
balance_ratio = 3
minimum_minority_samples = 2000


# -----------------------
# Reportes Resultados
# -----------------------
analizer_report = "results/analysis_results.xlsx"
preprocessor_report = "results/preprocessor_result.xlsx"


# -----------------------
# Algoritmos habilitados
# -----------------------
naive_enable = False
desicion_enable = False
random_enable = False
svm_enable = False
cnn_enable = True
