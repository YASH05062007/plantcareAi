# GreenInsight: Enterprise Botanical Diagnostic System

GreenInsight is an advanced computer vision platform engineered to autonomously detect and classify phytopathology present in agricultural leaf tissue. Leveraging a robust MobileNetV2-based topological architecture and transfer learning, this system evaluates incoming visual anomalies against a high-dimensional diagnostic matrix to verify crop health. It features an integrated diagnostic terminal (CLI) and a fully authenticated web portal.

## Core System Capabilities
* **Deep Feature Extraction**: Employs transfer learning via an ImageNet-primed MobileNetV2 foundation, achieving high classification precision without catastrophic forgetting.
* **Resilient Data Augmentation Pipeline**: Features automated preprocessing arrays (shear, zoom, multidirectional flips, normalization) mitigating network overfitting on limited diagnostic inputs.
* **Standalone Inference Engine**: Decoupled `predict.py` module capable of executing offline diagnostic propagation independently of the web framework.
* **Authentication Portal**: A streamlined, fully authenticated user deployment dashboard with rate-limited complementary diagnostic quotas.

---

## Architectural Topology
```bash
greeninsight_core/
│
├── dataset/                  # Primary training corpus injection point
├── models/                   # Compiled computational graphs and mappings
│   ├── plant_disease_model.h5
│   ├── plant_disease_model.onnx
│   └── class_indices.json
├── static/                   # Static server endpoints
│   └── uploads/              # Volatile image cache
├── templates/                # Frontend application views
│   ├── index.html            # Main diagnostic dashboard
│   └── login.html            # User authentication gateway
│
├── train_model.py            # Automated network optimization pipeline
├── predict.py                # Standalone inference evaluator
├── app.py                    # Web framework orchestration
├── requirements.txt          # System dependencies
└── README.md                 # Technical specification
```

---

## Environment Provisioning

1. **Initialize the Repository**
   Establish the repository locally and navigate to the project root directory.

2. **Isolate Python Dependencies (Recommended)**
   ```bash
   python -m venv venv
   # Execute activation sequence (Windows)
   venv\Scripts\activate
   # Execute activation sequence (Mac/Linux)
   source venv/bin/activate
   ```

3. **Install System Requisites**
   ```bash
   pip install -r requirements.txt
   ```

---

## Managing the Training Corpus

The neural architecture requires a rigorously sorted image corpus. The accepted standard for initial evaluation is derived from segmented PlantVillage categorizations.

1. Ensure target category directories are extracted and injected into the `dataset/` root directory.
2. Ensure consistent hierarchical structures:
```
dataset/
    ├── Apple_scab_pathology/
    ├── Healthy_Apple_tissue/
    ├── Tomato_Bacterial_Spot/
    └── ...
```

---

## Executing the Optimization Pipeline

Once the corpus is securely provisioned:

1. Initiate the neural synthesis sequence:
   ```bash
   python train_model.py
   ```
2. The compilation logic will automatically deduce class maps, inject the topological configurations, and commence gradient descent across 10 validation cycles. 
3. Upon conclusion, the optimal weights are stored at `models/plant_disease_model.h5` and telemetry graphs will be generated.
4. If required, serialize the network for edge capabilities utilizing ONNX:
   ```bash
   python -m tf2onnx.convert --saved-model models/plant_disease_model.h5 --output models/plant_disease_model.onnx
   ```

---

## Launching the Diagnostic Portal

To expose the web application functionality globally or locally:

1. Guarantee active deployment within the project directory, then instantiate the server:
   ```bash
   python app.py
   ```
2. The authentication server will initialize locally. Access the system securely at:
   ```
   http://127.0.0.1:5000/
   ```
3. Provide valid contact credentials to clear the authentication gateway, submit a high-fidelity image crop, and trigger the remote diagnostic protocol.
