import joblib
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
ARTIFACT_DIR = BASE_DIR / "artifacts"

MODEL_PATH = ARTIFACT_DIR / "final_crop_yield_model.pkl"
FEATURE_PATH = ARTIFACT_DIR / "model_features.pkl"


class ModelLoader:
    def __init__(self):
        self.model = None
        self.feature_columns = None

    def load(self):
        print("Loading model artifacts...")

        self.model = joblib.load(MODEL_PATH)
        self.feature_columns = joblib.load(FEATURE_PATH)

        print("Model loaded successfully")
        print(f"Features: {len(self.feature_columns)}")

    def get_model(self):
        return self.model

    def get_feature_columns(self):
        return self.feature_columns


loader = ModelLoader()
loader.load()