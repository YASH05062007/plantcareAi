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

---

## Deploy on Render

### Backend — Web Service

1. Go to [render.com](https://render.com) → **New → Web Service**
2. Connect your GitHub repo
3. Set these fields:

| Field | Value |
|---|---|
| **Root Directory** | `plantcare-ai/backend` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn main:app --host 0.0.0.0 --port $PORT` |

4. Under **Environment Variables**, add:

| Key | Value | Notes |
|---|---|---|
| `MODEL_PATH` | `models/plant_model.h5` | Path to model file inside `backend/` |
| `HOST` | `0.0.0.0` | Required for Render |
| `PORT` | `10000` | Render sets this automatically — you can leave it unset |

> **Note:** Render injects `$PORT` automatically. The start command above uses it directly, so you do **not** need to set `PORT` manually.

After deploy, Render gives you a URL like:
```
https://plantcare-api.onrender.com
```

---

### Frontend — Static Site

1. Go to **New → Static Site**
2. Connect the same repo
3. Set these fields:

| Field | Value |
|---|---|
| **Root Directory** | `plantcare-ai/frontend` |
| **Build Command** | *(leave empty)* |
| **Publish Directory** | `.` |

4. Under **Environment Variables**, add:

| Key | Value | Notes |
|---|---|---|
| `API_BASE_URL` | `https://plantcare-api.onrender.com` | Your backend URL from the step above |

> **Important:** The frontend reads `API_BASE_URL` from a `.env` file at runtime via `fetch("./.env")`. Render Static Sites do **not** automatically write env vars to a `.env` file — you have two options:
>
> **Option A (recommended):** Manually create `frontend/.env` with your live backend URL and commit it:
> ```env
> API_BASE_URL=https://plantcare-api.onrender.com
> ```
>
> **Option B:** Leave `.env` empty — the `app.js` auto-detection will use `localhost:8000` as fallback when not in Codespaces, so you must use Option A for production.

---

## Local Development

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

API runs at `http://localhost:8000`

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Frontend

```bash
cd frontend
python -m http.server 5500
```

Open `http://localhost:5500`

Configure `frontend/.env`:

```env
API_BASE_URL=http://localhost:8000
```

### API Reference

`POST /predict`

| | |
|---|---|
| Form field | `image` (file) |
| Response | `{ "prediction": "...", "confidence": 0.94 }` |

