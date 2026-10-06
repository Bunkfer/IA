"""CNN 1D para clasificar las caracteristicas numericas del dataset.

Uso en main.py:
    from src.models.cnn import CNNModel
    model_CNN = Base_Model(CNNModel(), dataset)

Dependencia adicional: python -m pip install tensorflow
El orden de las columnas debe ser el mismo al entrenar y predecir.
"""

import numpy as np
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder, StandardScaler


class CNNModel:

    def __init__(self, epochs=20, batch_size=64, random_state=42, verbose=1):
        if epochs < 1 or batch_size < 1:
            raise ValueError("epochs y batch_size deben ser positivos.")
        self.epochs = epochs
        self.batch_size = batch_size
        self.random_state = random_state
        self.verbose = verbose
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.history = None
        self.feature_names = None

    def train(self, X_train, y_train) -> None:
        """Entrenar una nueva red en cada llamada, como los otros modelos."""
        features = self._numeric_features(X_train)
        labels = np.asarray(y_train)
        if labels.ndim != 1 or len(labels) != len(features):
            raise ValueError("y_train debe tener una etiqueta por fila de X_train.")
        encoder = LabelEncoder()
        encoded_labels = encoder.fit_transform(labels)
        if len(encoder.classes_) < 2:
            raise ValueError("Se necesitan al menos dos clases para entrenar.")

        # Ajustar el escalado solamente con los datos de entrenamiento.
        self.model = None
        self.history = None
        self.label_encoder = encoder
        self.scaler = StandardScaler()
        scaled_features = self.scaler.fit_transform(features).astype(np.float32)
        inputs = scaled_features[..., np.newaxis]
        self.feature_names = (
            list(X_train.columns) if hasattr(X_train, "columns") else None
        )

        tf.keras.utils.set_random_seed(self.random_state)
        model = tf.keras.Sequential(
            [
                tf.keras.layers.Input(shape=(features.shape[1], 1)),
                tf.keras.layers.Conv1D(32, 3, padding="same", activation="relu"),
                tf.keras.layers.Conv1D(64, 3, padding="same", activation="relu"),
                tf.keras.layers.GlobalAveragePooling1D(),
                tf.keras.layers.Dense(32, activation="relu"),
                tf.keras.layers.Dropout(0.2),
                tf.keras.layers.Dense(len(encoder.classes_), activation="softmax"),
            ]
        )
        model.compile(
            optimizer="adam",
            loss="sparse_categorical_crossentropy",
            metrics=["accuracy"],
        )
        self.history = model.fit(
            inputs,
            encoded_labels,
            epochs=self.epochs,
            batch_size=self.batch_size,
            verbose=self.verbose,
        )
        self.model = model
        print("CNN model trained successfully.")

    def predict(self, X_test):
        """Devolver etiquetas originales compatibles con ModelEvaluator."""
        if self.model is None:
            raise RuntimeError("Entrena el modelo con train antes de predecir.")
        if self.feature_names is not None and hasattr(X_test, "columns"):
            if list(X_test.columns) != self.feature_names:
                raise ValueError("Las columnas deben coincidir con el entrenamiento.")
        features = self._numeric_features(X_test)
        if features.shape[1] != self.scaler.n_features_in_:
            raise ValueError("El numero de caracteristicas no coincide.")
        inputs = self.scaler.transform(features).astype(np.float32)[..., np.newaxis]
        probabilities = self.model.predict(
            inputs, batch_size=self.batch_size, verbose=0
        )
        return self.label_encoder.inverse_transform(probabilities.argmax(axis=1))

    @staticmethod
    def _numeric_features(X):
        features = np.asarray(X, dtype=np.float32)
        if features.ndim != 2 or 0 in features.shape:
            raise ValueError(
                "X debe ser una matriz no vacia de filas y caracteristicas."
            )
        if not np.isfinite(features).all():
            raise ValueError("X contiene valores faltantes o infinitos.")
        return features
