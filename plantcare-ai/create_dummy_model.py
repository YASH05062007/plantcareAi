import os
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, GlobalAveragePooling2D

IMG_SIZE = (224, 224, 3)
num_classes = 3

inputs = Input(shape=IMG_SIZE)
x = GlobalAveragePooling2D()(inputs)
outputs = Dense(num_classes, activation='softmax')(x)
model = Model(inputs=inputs, outputs=outputs)

os.makedirs('models', exist_ok=True)
model.save('models/plant_disease_model.h5')

class_indices = {'Healthy': 0, 'Powdery Mildew': 1, 'Rust': 2}
with open('models/class_indices.json', 'w') as f:
    json.dump(class_indices, f)

print("Dummy model created in models/ directory.")
