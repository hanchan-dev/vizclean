# app/ml/model_trainer.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

from sklearn.pipeline import Pipeline

from app.ml.model_prepocessor import ModelPreprocessor
from app.ml.metrics import Metrics


class ModelTrainer:

    @staticmethod
    def get_model(model_name: str):
        model_name = model_name.lower()

        models = {
            "randomforest": RandomForestClassifier(),
            "logisticregression": LogisticRegression(max_iter=200),
            "svm": SVC(),
            "knn": KNeighborsClassifier(),
        }

        if model_name not in models:
            raise ValueError(f"Model '{model_name}' tidak dikenal.")

        return models[model_name]

    @staticmethod
    def train(df: pd.DataFrame, target_col: str, model_name="randomforest", test_size=0.2):
        # Pisahkan fitur dan target
        X, y = ModelPreprocessor.split_features_target(df, target_col)

        # Siapkan preprocessor
        preprocessor, num_cols, cat_cols = ModelPreprocessor.build_preprocessor(X)

        # Pilih model
        model = ModelTrainer.get_model(model_name)

        # Build pipeline
        clf = Pipeline(steps=[
            ("preprocessor", preprocessor),
            ("model", model)
        ])

        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )

        # Training
        clf.fit(X_train, y_train)

        # Evaluate
        predictions = clf.predict(X_test)
        accuracy = Metrics.accuracy(y_test, predictions)

        return {
            "pipeline": clf,
            "accuracy": accuracy,
            "X_test": X_test,
            "y_test": y_test,
            "predictions": predictions
        }
