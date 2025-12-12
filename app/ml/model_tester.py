import pandas as pd
from app.ml.metrics import Metrics


class ModelTester:

    @staticmethod
    def run_test(model_pipeline, df: pd.DataFrame, target_col: str):
        if target_col not in df.columns:
            raise ValueError("Target column missing in test data.")

        X_test = df.drop(columns=[target_col])
        y_test = df[target_col]

        predictions = model_pipeline.predict(X_test)
        accuracy = Metrics.accuracy(y_test, predictions)
        report = Metrics.classification_report_text(y_test, predictions)
        matrix = Metrics.confusion_matrix_data(y_test, predictions)

        return {
            "accuracy": accuracy,
            "predictions": predictions,
            "report": report,
            "confusion_matrix": matrix
        }
