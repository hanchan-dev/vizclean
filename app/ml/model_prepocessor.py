import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline


class ModelPreprocessor:
    """
    Mengubah DataFrame cleaned → X, y, dan preprocessing pipeline.
    """

    @staticmethod
    def split_features_target(df: pd.DataFrame, target_col: str):
        if target_col not in df.columns:
            raise ValueError(f"Target column '{target_col}' not found in dataframe.")

        X = df.drop(columns=[target_col])
        y = df[target_col]

        return X, y

    @staticmethod
    def build_preprocessor(X: pd.DataFrame):
        numeric_features = X.select_dtypes(include=["int64", "float64"]).columns.tolist()
        categorical_features = X.select_dtypes(include=["object"]).columns.tolist()

        numeric_pipeline = Pipeline(steps=[
            ("scaler", StandardScaler())
        ])

        categorical_pipeline = Pipeline(steps=[
            ("onehot", OneHotEncoder(handle_unknown="ignore"))
        ])

        preprocessor = ColumnTransformer(
            transformers=[
                ("num", numeric_pipeline, numeric_features),
                ("cat", categorical_pipeline, categorical_features)
            ]
        )

        return preprocessor, numeric_features, categorical_features
