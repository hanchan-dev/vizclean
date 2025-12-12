import pickle


class ModelSaver:

    @staticmethod
    def save(model_pipeline, path: str):
        with open(path, "wb") as f:
            pickle.dump(model_pipeline, f)

    @staticmethod
    def load(path: str):
        with open(path, "rb") as f:
            return pickle.load(f)
