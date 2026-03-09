from io import BytesIO

import numpy as np
from PIL import Image

TARGET_SIZE = (224, 224)


def prepare_image(image_bytes: bytes) -> np.ndarray:
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    image = image.resize(TARGET_SIZE)

    arr = np.asarray(image, dtype=np.float32) / 255.0
    arr = np.expand_dims(arr, axis=0)
    return arr
