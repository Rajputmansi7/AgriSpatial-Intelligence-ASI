from fastapi import FastAPI
from pydantic import BaseModel

from backend.services.feature_builder import (
    build_features
)

from backend.predict import (
    predict_yield
)

app = FastAPI(
    title="ASI Yield Prediction API",
    version="1.0"
)


# ----------------------------------
# REQUEST MODEL
# ----------------------------------

class PredictionRequest(BaseModel):

    latitude: float
    longitude: float

    crop: str

    area_ha: float


# ----------------------------------
# HEALTH CHECK
# ----------------------------------

@app.get("/")
def home():

    return {
        "status": "running",
        "service": "ASI Yield Prediction API"
    }


# ----------------------------------
# PREDICT
# ----------------------------------

@app.post("/predict")
def predict(
    request: PredictionRequest
):

    features = build_features(
        latitude=request.latitude,
        longitude=request.longitude,
        crop=request.crop,
        area_ha=request.area_ha
    )

    prediction = predict_yield(
        features
    )

    return {

        "success": True,

        "location": {

            "district":
                features["district"],

            "agro_zone":
                features["agro_zone"],
                
            "features": features
        },

        "input": {

            "latitude":
                request.latitude,

            "longitude":
                request.longitude,

            "crop":
                request.crop,

            "area_ha":
                request.area_ha
        },

        "prediction": {

            "yield_kg_ha":
                prediction
        }
    }