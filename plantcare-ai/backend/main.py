from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.predict import router as predict_router

app = FastAPI(title="PlantCare API", version="1.0.0")

# Allow local frontend apps to call this API during development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health_check() -> dict:
    return {"status": "ok", "service": "plantcare-api"}


app.include_router(predict_router)
