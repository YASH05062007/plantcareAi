import os
import json
import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam

# --- System Hyperparameters ---
TRAINING_CORPUS = "dataset"
ARTIFACT_DESTINATION = os.path.join("models", "plant_disease_model.h5")
BATCH_PROCESSING_CAPACITY = 32
IMAGE_TARGET_RESOLUTION = (224, 224)
TRAINING_CYCLES = 10

def construct_topological_architecture(target_categories):
    """
    Assembles the deep learning network by importing a foundational MobileNetV2 structure
    and appending specialized dense layers tuned for our specific botanical classification task.
    """
    # Initialize the base extraction mechanism with transfer learning weights
    foundation_network = MobileNetV2(
        weights='imagenet', 
        include_top=False, 
        input_shape=(IMAGE_TARGET_RESOLUTION[0], IMAGE_TARGET_RESOLUTION[1], 3)
    )
    
    # Isolate base weights to prevent catastrophic forgetting during backpropagation
    for component in foundation_network.layers:
        component.trainable = False
        
    # Append the custom classification head
    tensor_flow = foundation_network.output
    tensor_flow = GlobalAveragePooling2D()(tensor_flow)
    tensor_flow = Dense(128, activation='relu')(tensor_flow)
    tensor_flow = Dropout(0.5)(tensor_flow)
    final_output = Dense(target_categories, activation='softmax')(tensor_flow)
    
    # Synthesize the final computational graph
    neural_system = Model(inputs=foundation_network.input, outputs=final_output)
    
    # Configure the gradient descent optimization and error calculation
    neural_system.compile(
        optimizer=Adam(learning_rate=0.001), 
        loss='categorical_crossentropy', 
        metrics=['accuracy']
    )
    
    return neural_system

def execute_training_pipeline():
    if not os.path.exists(TRAINING_CORPUS):
        print(f"Critical Error: Corpus directory '{TRAINING_CORPUS}' missing. Please ensure dataset is provisioned.")
        return

    # Image Pipeline: Augmentation & Structural Pre-processing
    # Employs 20% holdout distribution for unbiased validation checks
    asset_pipeline = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        validation_split=0.2
    )
    
    # Initialize the ingestion stream for weight updates
    ingestion_stream = asset_pipeline.flow_from_directory(
        TRAINING_CORPUS,
        target_size=IMAGE_TARGET_RESOLUTION,
        batch_size=BATCH_PROCESSING_CAPACITY,
        class_mode='categorical',
        subset='training'
    )
    
    # Initialize the verification stream
    verification_stream = asset_pipeline.flow_from_directory(
        TRAINING_CORPUS,
        target_size=IMAGE_TARGET_RESOLUTION,
        batch_size=BATCH_PROCESSING_CAPACITY,
        class_mode='categorical',
        subset='validation'
    )
    
    category_count = len(ingestion_stream.class_indices)
    print(f"System identified {category_count} unique diagnostic targets.")
    
    # Ensure deployment directory exists
    os.makedirs("models", exist_ok=True)
    
    # Export the label mapping array for production diagnostics
    with open(os.path.join("models", "class_indices.json"), "w") as dictionary_file:
        json.dump(ingestion_stream.class_indices, dictionary_file)
        
    print("Synthesizing neural architecture...")
    diagnostic_model = construct_topological_architecture(category_count)
    
    print("Initiating gradient descent optimization...")
    training_metrics = diagnostic_model.fit(
        ingestion_stream,
        steps_per_epoch=ingestion_stream.samples // BATCH_PROCESSING_CAPACITY,
        validation_data=verification_stream,
        validation_steps=verification_stream.samples // BATCH_PROCESSING_CAPACITY,
        epochs=TRAINING_CYCLES
    )
    
    # Final architectural assessment
    print("Executing final network validation...")
    val_error, val_precision = diagnostic_model.evaluate(verification_stream)
    print(f"Network Validation Precision: {val_precision:.4f}")
    
    # Commit optimal weights to disk
    diagnostic_model.save(ARTIFACT_DESTINATION)
    print(f"Deployment artifact secured at '{ARTIFACT_DESTINATION}'.")
    
    # Generate visualization telemetry
    precision_metric = training_metrics.history['accuracy']
    val_precision_metric = training_metrics.history['val_accuracy']
    error_metric = training_metrics.history['loss']
    val_error_metric = training_metrics.history['val_loss']
    
    plt.figure(figsize=(10, 5))
    
    # Precision Telemetry
    plt.subplot(1, 2, 1)
    plt.plot(precision_metric, label='Optimization Precision')
    plt.plot(val_precision_metric, label='Validation Precision')
    plt.legend(loc='lower right')
    plt.title('Network Precision Metrics')
    
    # Error Telemetry
    plt.subplot(1, 2, 2)
    plt.plot(error_metric, label='Optimization Error')
    plt.plot(val_error_metric, label='Validation Error')
    plt.legend(loc='upper right')
    plt.title('Network Error Metrics')
    
    plt.savefig('optimization_telemetry.png')
    plt.show()

if __name__ == "__main__":
    execute_training_pipeline()
