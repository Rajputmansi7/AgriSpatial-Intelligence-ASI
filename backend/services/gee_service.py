import ee
from datetime import datetime, timedelta


# -----------------------------------
# GEE AUTH
# -----------------------------------
import os
import json
import tempfile
import ee

service_account_info = json.loads(
    os.environ["GEE_SERVICE_ACCOUNT_JSON"]
)

with tempfile.NamedTemporaryFile(
    mode="w",
    suffix=".json",
    delete=False
) as f:

    json.dump(service_account_info, f)

    credential_path = f.name

credentials = ee.ServiceAccountCredentials(
    service_account_info["client_email"],
    credential_path
)

ee.Initialize(
    credentials=credentials,
    project=os.environ["GEE_PROJECT_ID"]
)
# -----------------------------------
# GEE SERVICE
# -----------------------------------

class GEEService:

    def get_gee_features(
        self,
        latitude: float,
        longitude: float
    ):

        point = ee.Geometry.Point(
            [longitude, latitude]
        )

        # -----------------------------------
        # LAST 12 MONTHS
        # -----------------------------------

        end_date = datetime.today()
        start_date = end_date - timedelta(days=365)

        start_date = start_date.strftime("%Y-%m-%d")
        end_date = end_date.strftime("%Y-%m-%d")

        # -----------------------------------
        # SENTINEL-2
        # -----------------------------------

        s2 = (
            ee.ImageCollection(
                "COPERNICUS/S2_SR_HARMONIZED"
            )
            .filterDate(start_date, end_date)
            .filterBounds(point)
            .filter(
                ee.Filter.lt(
                    "CLOUDY_PIXEL_PERCENTAGE",
                    10
                )
            )
        )

        def add_indices(image):

            scaled = (
                image.select(
                    ["B2", "B4", "B8"]
                )
                .multiply(0.0001)
            )

            ndvi = (
                scaled.normalizedDifference(
                    ["B8", "B4"]
                )
                .rename("NDVI")
            )

            evi = (
                scaled.expression(
                    "2.5*((NIR-RED)/(NIR+6*RED-7.5*BLUE+1))",
                    {
                        "NIR": scaled.select("B8"),
                        "RED": scaled.select("B4"),
                        "BLUE": scaled.select("B2")
                    }
                )
                .rename("EVI")
            )

            savi = (
                scaled.expression(
                    "(1+L)*((NIR-RED)/(NIR+RED+L))",
                    {
                        "NIR": scaled.select("B8"),
                        "RED": scaled.select("B4"),
                        "L": 0.5
                    }
                )
                .rename("SAVI")
            )

            return image.addBands(
                [ndvi, evi, savi]
            )

        indices = s2.map(
            add_indices
        )

        median_indices = (
            indices.select(
                ["NDVI", "EVI", "SAVI"]
            )
            .median()
        )

        ndvi = (
            median_indices.select("NDVI")
            .reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=point,
                scale=100
            )
            .get("NDVI")
        )

        evi = (
            median_indices.select("EVI")
            .reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=point,
                scale=100
            )
            .get("EVI")
        )

        savi = (
            median_indices.select("SAVI")
            .reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=point,
                scale=100
            )
            .get("SAVI")
        )

        # -----------------------------------
        # ERA5
        # -----------------------------------

        era5 = (
            ee.ImageCollection(
                "ECMWF/ERA5_LAND/HOURLY"
            )
            .filterDate(
                start_date,
                end_date
            )
        )

        temperature = (
            era5.select(
                "temperature_2m"
            )
            .mean()
            .subtract(273.15)
            .rename(
                "Temperature_C"
            )
        )

        rainfall = (
            era5.select(
                "total_precipitation_hourly"
            )
            .sum()
            .multiply(1000)
            .rename(
                "Rainfall_mm"
            )
        )

        temp_value = (
            temperature.reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=point,
                scale=10000
            )
            .get(
                "Temperature_C"
            )
        )

        rainfall_value = (
            rainfall.reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=point,
                scale=10000
            )
            .get(
                "Rainfall_mm"
            )
        )

        return {
            "Rainfall_mm":
                ee.Number(
                    rainfall_value
                ).getInfo(),

            "Temperature_C":
                ee.Number(
                    temp_value
                ).getInfo(),

            "NDVI":
                ee.Number(
                    ndvi
                ).getInfo(),

            "EVI":
                ee.Number(
                    evi
                ).getInfo(),

            "SAVI":
                ee.Number(
                    savi
                ).getInfo()
        }


gee_service = GEEService()
