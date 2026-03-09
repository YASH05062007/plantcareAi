import json
from pathlib import Path
from typing import Tuple

import numpy as np
from tensorflow.keras.models import load_model

from utils.image_processing import prepare_image

BASE_DIR = Path(__file__).resolve().parents[1]


class ModelService:
    def __init__(self, model_path: str) -> None:
        self.model = None
        self.class_map = None
        self.model_path = (BASE_DIR / model_path).resolve()
        self.class_map_path = self.model_path.with_name("class_indices.json")
        self._load_assets()

    def _load_assets(self) -> None:
        if not self.model_path.exists():
            raise FileNotFoundError(f"Missing model file: {self.model_path}")
        if not self.class_map_path.exists():
            raise FileNotFoundError(f"Missing class map file: {self.class_map_path}")

        self.model = load_model(self.model_path)

        with self.class_map_path.open("r", encoding="utf-8") as file:
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
