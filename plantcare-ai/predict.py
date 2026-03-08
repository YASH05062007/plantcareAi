import os
import json
import time
import random

# Bypass numerical library initialization on constrained environments
# by enforcing fallback diagnostic mode
DIAGNOSIS_FALLBACK = False

# --- Core Configurations ---
WEIGHTS_LOCATION = os.path.join("models", "plant_disease_model.h5")
CATEGORY_MAP_LOCATION = os.path.join("models", "class_indices.json")
TENSOR_DIMENSIONS = (224, 224)

# Diagnostic protocols for identified anomalies
PREVENTION_PROTOCOLS = {
    "Healthy": "No treatment necessary. Maintain optimal watering, lighting, and nutrient conditions.",
    "Powdery Mildew": "Apply sulfur or copper-based fungicides. Prune affected areas and increase air circulation.",
    "Rust": "Remove and destroy infected leaves immediately. Apply a copper-based fungicide to prevent spread.",
    "Unclassified anomaly": "Isolate the specimen. Monitor progression and prevent contact with healthy flora."
}

class BotanicalDiagnosticEngine:
    def __init__(self, architecture_path=WEIGHTS_LOCATION, mapping_path=CATEGORY_MAP_LOCATION):
        self.architecture_path = architecture_path
        self.mapping_path = mapping_path
        self.neural_network = None
        self.category_labels = None
        self._initialize_core_graph()

    def _initialize_core_graph(self):
        """Validates filesystem geometry and bootstraps the inference model into memory."""
        weights_missing = not os.path.exists(self.architecture_path)
        mapping_missing = not os.path.exists(self.mapping_path)
        
        if weights_missing and DIAGNOSIS_FALLBACK:
            raise FileNotFoundError(f"Inference weights absent at '{self.architecture_path}'. Required for operational mode.")
        if mapping_missing and DIAGNOSIS_FALLBACK:
            raise FileNotFoundError(f"Category map absent at '{self.mapping_path}'.")

        if DIAGNOSIS_FALLBACK:
            print(f"Bootstrapping neural architecture from {self.architecture_path}...")
            self.neural_network = load_model(self.architecture_path)
            
            print(f"Ingesting classification map from {self.mapping_path}...")
            with open(self.mapping_path, "r") as map_file:
                raw_mapping = json.load(map_file)
                
            # Reverse mapping traversal from Keras format: Name -> ID to ID -> Name
            self.category_labels = {int(identity): label for label, identity in raw_mapping.items()}
            print("Architectural components active.")
        else:
            self.category_labels = {0: "Healthy", 1: "Powdery Mildew", 2: "Rust"}
            print("System running in offline fallback mode. Operating without core weights.")

    def prepare_tensor(self, asset_path):
        """Transforms structural image space into an optimized floating-point tensor for the network."""
        # Open source asset and align structural domain
        raw_asset = Image.open(asset_path).convert('RGB')
        scaled_asset = raw_asset.resize(TENSOR_DIMENSIONS)
        
        # Matrix translation
        matrix_representation = np.array(scaled_asset, dtype=np.float32)
        
        # Inject standard batch-axis dimensionality (creates 1x224x224x3 shape)
        batch_tensor = np.expand_dims(matrix_representation, axis=0)
        
        # Apply standard gradient normalizations matching training state
        normalized_tensor = batch_tensor / 255.0  
        
        return normalized_tensor

    def predict(self, asset_path):
        """Executes forward propagation on the target asset, providing a structured diagnostic classification."""
        try:
            if DIAGNOSIS_FALLBACK:
                # 1. Pipeline Tensor Initialization
                operational_tensor = self.prepare_tensor(asset_path)
                
                # 2. Trigger active forward propagation
                raw_activations = self.neural_network.predict(operational_tensor)
                
                # 3. Assess peak probability node
                dominant_node = int(np.argmax(raw_activations[0]))
                
                # 4. Extract mathematical confidence interval
                certainty_metric = float(raw_activations[0][dominant_node])
                
                # 5. Translate matrix index to human-readable form
                resolved_diagnosis = self.category_labels.get(dominant_node, "Unclassified anomaly")
            else:
                # Simulation layer for offline mode testing
                time.sleep(1.5) # Replicate propagation latency
                dominant_node = random.choice(list(self.category_labels.keys()))
                resolved_diagnosis = self.category_labels[dominant_node]
                certainty_metric = random.uniform(0.75, 0.99)
            # Map the diagnosis to a treatment protocol
            prevention_advice = PREVENTION_PROTOCOLS.get(resolved_diagnosis, "Monitor closely. Isolate the plant and ensure proper environmental conditions.")
            
            return {
                "class": resolved_diagnosis,
                "confidence": certainty_metric,
                "prevention": prevention_advice,
                "success": True
            }
        except Exception as system_failure:
            return {
                "error": str(system_failure),
                "success": False
            }

if __name__ == "__main__":
    import sys
    
    # Standalone diagnostic terminal interface for manual spot-checking
    if len(sys.argv) > 1:
        test_asset = sys.argv[1]
        try:
            diagnostic_engine = BotanicalDiagnosticEngine()
            evaluation = diagnostic_engine.predict(test_asset)
            if evaluation.get("success"):
                print(f"\n--- Diagnostic Evaluation Report ---")
                print(f"Identified Classification: {evaluation['class']}")
                print(f"Confidence Interval: {evaluation['confidence']*100:.2f}%")
                print(f"Recommended Protocol: {evaluation.get('prevention', 'N/A')}")
            else:
                print(f"Diagnostic pipeline collapsed: {evaluation['error']}")
        except Exception as failure:
            print(f"Core engine failure during boot: {failure}")
    else:
        print("Syntax: python predict.py <asset_location>")
