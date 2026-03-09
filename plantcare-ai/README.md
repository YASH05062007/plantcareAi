# plantcare-ai

Cleanly separated PlantCare project with a FastAPI backend and static frontend.

## Structure

```text
plantcare-ai/
├── backend/
│   ├── .env
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
    ├── .env
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

Configure backend environment (`backend/.env`):

```env
MODEL_PATH=models/plant_model.h5
HOST=0.0.0.0
PORT=8000
```

Run API server:

```bash
uvicorn main:app --reload
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

FastAPI docs:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Frontend

Configure frontend environment (`frontend/.env`):

```env
API_BASE_URL=http://localhost:8000
```

Run a static file server from `frontend` so `.env` can be loaded by the browser:

```bash
cd frontend
python -m http.server 5500
```

Then open:

- `http://localhost:5500`
