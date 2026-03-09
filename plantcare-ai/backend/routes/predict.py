from fastapi import APIRouter, File, HTTPException, UploadFile

from services.model_service import ModelService

router = APIRouter()
model_service = ModelService()


@router.post("/predict")
async def predict(image: UploadFile = File(...)) -> dict:
    if not image.content_type or not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be an image")

    image_bytes = await image.read()
    if not image_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    try:
        prediction, confidence = model_service.predict(image_bytes)
    except FileNotFoundError as err:
        raise HTTPException(status_code=500, detail=str(err)) from err
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {err}") from err

    return {
        "prediction": prediction,
        "confidence": confidence,
    }
