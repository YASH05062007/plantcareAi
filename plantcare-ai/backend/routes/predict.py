from fastapi import APIRouter, File, HTTPException, Request, UploadFile

router = APIRouter()


@router.post("/predict")
async def predict(request: Request, image: UploadFile = File(...)) -> dict:
    if not image.content_type or not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be an image")

    image_bytes = await image.read()
    if not image_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    model_service = request.app.state.model_service

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
