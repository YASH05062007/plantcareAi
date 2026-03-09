# plantcare-ai

Cleanly separated PlantCare project with a FastAPI backend and static frontend.

## Structure

```text
plantcare-ai/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── models/
│   │   ├── plant_model.h5
│   │   └── class_indices.json
│   ├── routes/
│   │   └── predict.py
│   ├── services/
│   │   └── model_service.py
│   └── utils/
│       └── image_processing.py
└── frontend/
    ├── index.html
    ├── css/
    │   └── style.css
    └── js/
        └── app.js
```

## Backend

Install dependencies:

```bash
cd backend
pip install -r requirements.txt
```

Run API server:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

API endpoint:

- `POST /predict`
- Form field: `image` (file)
- JSON response:

```json
{
  "prediction": "Plant Disease Name",
  "confidence": 0.94
}
```

## Frontend

Open `frontend/index.html` in a browser. It sends image uploads to:

- `http://localhost:8000/predict`
