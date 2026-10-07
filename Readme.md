# IA - Classification Algorithms

Este repositorio contiene un proyecto desarrollado en **Python** para implementar, probar y comparar diferentes algoritmos de **clasificación de Inteligencia Artificial y Machine Learning**.

El objetivo principal es disponer de una estructura modular que permita experimentar con diferentes modelos, técnicas de preprocesamiento y métodos de balanceo de datasets sin modificar la arquitectura general del proyecto.

## Objetivos

- Implementar diferentes algoritmos de clasificación.
- Comparar el desempeño de los modelos utilizando las mismas condiciones de evaluación.
- Aplicar técnicas de preprocesamiento de datos.
- Incorporar métodos para trabajar con datasets desbalanceados.
- Generar métricas y resultados para facilitar la comparación entre modelos.
- Mantener una arquitectura modular basada en clases.
- Facilitar la incorporación de nuevos modelos y métodos de procesamiento.

## Modelos

El proyecto está diseñado para trabajar con diferentes algoritmos de clasificación, entre ellos:

- Naive Bayes
- Decision Tree
- Random Forest
- Support Vector Machine (SVM)
- Redes Neuronales / CNN

La estructura permite incorporar posteriormente otros modelos manteniendo una interfaz común.

## Base de datos

En power sheel intalamos el cli de aws, e instalamos la dependencia. 

```bash
irm https://awscli.amazonaws.com/v2/install.ps1 | iex
```

Cuando se finalize la instalacion, cerramos el powershell y lo abimos nuevmante, y confirmamos si la instalacion fue hecha correctamente.

```bash
aws --version
```

Ahora revisamos los archivos disponibles.

```bash
aws s3 ls "s3://cse-cic-ids2018/Processed Traffic Data for ML Algorithms/" --no-sign-request
```

Podemos descargar todos los archivos, en este caso solo descargaremos uno de ellos en la carptea de data.

```bash
aws s3 cp "s3://cse-cic-ids2018/Processed Traffic Data for ML Algorithms/Wednesday-14-02-2018_TrafficForML_CICFlowMeter.csv" "C:\OnedriveOut\Doctorado\Tesis\Programming\Test\data\" --no-sign-request
```

## Estructura

El código está organizado de forma modular utilizando clases y separando las principales responsabilidades:

```text
IA/
│
├── main.py
├── config.py
├── requirements.txt
│
├── src/
│   ├── data/
│   │   ├── dataset.py
│   │   ├── preprocessor.py
│   │   └── analizer.py
│   │
│   ├── models/
│   │   ├── base_model.py
│   │   ├── naive_bayes.py
│   │   ├── decision_tree.py
│   │   ├── random_forest.py
│   │   ├── svm.py
│   │   └── cnn.py
│   │
│   ├── evaluation/
│   │   └── evaluator.py
│   │
│   └── visualitation/
│       ├── excel_reporter.py
│       └── plots.py
│
└── results/
```

## Flujo general

El proyecto sigue de forma general el siguiente flujo:

```text
Dataset
   ↓
Análisis de datos
   ↓
Preprocesamiento
   ↓
Balanceo del Dataset
   ↓
Entrenamiento del Modelo
   ↓
Predicción
   ↓
Evaluación
   ↓
Resultados
```

Esta arquitectura busca mantener separados el manejo de datos, los modelos y la evaluación, permitiendo modificar o agregar componentes de manera independiente.

## Instalación

Crear un ambiente virtual:

```bash
python -m venv .venv
```

Activarlo en Linux / WSL:

```bash
source .venv/bin/activate
```

Activarlo en Windows:

```cmd
.venv\Scripts\activate
```

Instalar las dependencias:

```bash
pip install -r requirements.txt
```

## Ejecución

```bash
python main.py
```

## Estado del proyecto

Proyecto en desarrollo.

Se continuarán incorporando modelos, técnicas de balanceo, métodos de evaluación y herramientas para el análisis y comparación de resultados.