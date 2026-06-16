import pandas as pd

from backend.models.model_loader import loader

def predict_yield(features: dict):

    # -------------------------------
    # CREATE DATAFRAME
    # -------------------------------

    df = pd.DataFrame([features])

    # -------------------------------
    # COLUMN ORDER
    # -------------------------------

    df = df[
        loader.feature_columns
    ]

    # -------------------------------
    # PREDICTION
    # -------------------------------

    prediction = loader.model.predict(df)

    return round(
        float(prediction[0]),
        2
    )