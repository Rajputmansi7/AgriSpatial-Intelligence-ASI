from backend.services.soil_service import soil_service
from backend.services.gee_service import gee_service
from backend.services.districts_service import district_service
from backend.utils.validation_utils import validate_farm
import math


def build_features(
    latitude: float,
    longitude: float,
    crop: str,
    area_ha: float
):

    # ----------------------------------
    # DISTRICT + AGRO ZONE
    # ----------------------------------

    location = district_service.get_location_info(
        latitude=latitude,
        longitude=longitude
    )


    is_valid, message = validate_farm(
    area_ha=area_ha,
    district=location["district"])

    if not is_valid:
       raise ValueError(message)

    district = location["district"]
    agro_zone = location["agro_zone"]

    # ----------------------------------
    # SOIL DATA
    # ----------------------------------

    soil = soil_service.get_soil_data(
        latitude=latitude,
        longitude=longitude
    )

    # ----------------------------------
    # GEE DATA
    # ----------------------------------

    gee = gee_service.get_gee_features(
        latitude=latitude,
        longitude=longitude
    )

    # ----------------------------------
    # SAFE DEFAULTS
    # ----------------------------------

    sand_pct = soil.get("sand_pct") or 35.0
    silt_pct = soil.get("silt_pct") or 35.0
    clay_pct = soil.get("clay_pct") or 30.0

    ph_h2o = soil.get("ph_h2o") or 7.1

    organic_matter_pct = (
        soil.get("organic_matter_pct") or 0.85
    )

    nitrogen_g_kg = (
        soil.get("nitrogen_g_kg") or 0.55
    )

    cec_cmol_kg = (
        soil.get("cec_cmol_kg") or 18.0
    )

    capacity_field_vol_pct = (
        soil.get("capacity_field_vol_pct") or 29.0
    )

    capacity_wilt_vol_pct = (
        soil.get("capacity_wilt_vol_pct") or 14.0
    )

    texture_class = (
        soil.get("texture_class") or "Loam"
    )

    fao_classification = (
        soil.get("fao_classification")
        or "Calcisols"
    )

    rainfall_mm = (
        gee.get("Rainfall_mm") or 0.0
    )

    temperature_c = (
        gee.get("Temperature_C") or 0.0
    )

    ndvi = (
        gee.get("NDVI") or 0.0
    )

    evi = (
        gee.get("EVI") or 0.0
    )

    # ----------------------------------
    # FEATURE ENGINEERING
    # ----------------------------------

    log_area_ha = math.log1p(area_ha)

    water_retention_index = (
        capacity_field_vol_pct
        - capacity_wilt_vol_pct
    )

    soil_fertility_index = (
        organic_matter_pct
        + nitrogen_g_kg
        + cec_cmol_kg
    ) / 3

    # ----------------------------------
    # FINAL FEATURES
    # ----------------------------------

    features = {

        "district":
            district,

        "crop":
            crop,

        "year":
            "2022-23",

        "area_ha":
            area_ha,

        "sand_pct":
            sand_pct,

        "silt_pct":
            silt_pct,

        "clay_pct":
            clay_pct,

        "ph_h2o":
            ph_h2o,

        "organic_matter_pct":
            organic_matter_pct,

        "nitrogen_g_kg":
            nitrogen_g_kg,

        "cec_cmol_kg":
            cec_cmol_kg,

        "capacity_field_vol_pct":
            capacity_field_vol_pct,

        "texture_class":
            texture_class,

        "fao_classification":
            fao_classification,

        "Rainfall_mm":
            rainfall_mm,

        "Temperature_C":
            temperature_c,

        "NDVI":
            ndvi,

        "EVI":
            evi,

        "log_area_ha":
            log_area_ha,

        "water_retention_index":
            water_retention_index,

        "soil_fertility_index":
            soil_fertility_index,

        "agro_zone":
            agro_zone
    }

    return features