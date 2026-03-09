import json
from pathlib import Path
from typing import Tuple

import numpy as np
from tensorflow.keras.models import load_model

from utils.image_processing import prepare_image

BASE_DIR = Path(__file__).resolve().parents[1]
MODELS_DIR = BASE_DIR / "models"
MODEL_PATH = MODELS_DIR / "plant_model.h5"
CLASS_MAP_PATH = MODELS_DIR / "class_indices.json"


class ModelService:
    def __init__(self) -> None:
        self.model = None
        self.class_map = None
        self._load_assets()

    def _load_assets(self) -> None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(f"Missing model file: {MODEL_PATH}")
        if not CLASS_MAP_PATH.exists():
            raise FileNotFoundError(f"Missing class map file: {CLASS_MAP_PATH}")

        self.model = load_model(MODEL_PATH)

        with CLASS_MAP_PATH.open("r", encoding="utf-8") as file:
            raw_mapping = json.load(file)

        # Keras class index JSON is name -> id, convert to id -> name.
        self.class_map = {int(idx): name for name, idx in raw_mapping.items()}

    def predict(self, image_bytes: bytes) -> Tuple[str, float]:
        if self.model is None or self.class_map is None:
            raise RuntimeError("Model service is not initialized")

        input_tensor = prepare_image(image_bytes)
        probs = self.model.predict(input_tensor, verbose=0)[0]

        class_idx = int(np.argmax(probs))
        prediction = self.class_map.get(class_idx, "Unknown")
        confidence = float(probs[class_idx])
        return prediction, confidence
