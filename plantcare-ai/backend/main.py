import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.predict import router as predict_router
from services.model_service import ModelService

load_dotenv(Path(__file__).resolve().parent / ".env")

MODEL_PATH = os.getenv("MODEL_PATH", "models/plant_model.h5")
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))

app = FastAPI(title="PlantCare API", version="1.0.0")

# Allow local frontend apps to call this API during development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.model_service = ModelService(model_path=MODEL_PATH)


@app.get("/")
def health_check() -> dict:
    return {
        "status": "ok",
        "service": "plantcare-api",
        "host": HOST,
        "port": PORT,
        "model_path": MODEL_PATH,
    }


app.include_router(predict_router)
