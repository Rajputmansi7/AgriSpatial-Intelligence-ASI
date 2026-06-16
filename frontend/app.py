import streamlit as st
import requests

from shapely.geometry import Polygon
from pyproj import Geod

from map_component import render_map

API_URL = st.secrets.get(
    "API_URL",
    "http://127.0.0.1:8000/predict"
)


st.info(
    """
    ASI V1 estimates yield for a selected crop.

    This is a yield prediction system,
    not a crop suitability recommendation system.
    """
)

st.set_page_config(
    page_title="ASI Yield Predictor",
    page_icon="🌾",
    layout="wide"
)

st.title("🌾 Agricultural Spatial Intelligence")
st.subheader("Yield Prediction from Farm Boundary")

# --------------------------------------------------
# DRAW FARM
# --------------------------------------------------

st.subheader("Draw Farm Boundary")

polygon_data = render_map()

latitude = None
longitude = None
area_ha = None

# Prediction placeholders
result = None
yield_density = None
total_production = None
features = None

if polygon_data:

    coordinates = (
        polygon_data["geometry"]["coordinates"][0]
    )

    polygon = Polygon(coordinates)

    centroid = polygon.centroid

    longitude = centroid.x
    latitude = centroid.y

    geod = Geod(
        ellps="WGS84"
    )

    area_m2, _ = geod.geometry_area_perimeter(
        polygon
    )

    area_ha = abs(area_m2) / 10000

    st.success(
        f"Detected Area: {area_ha:.2f} ha"
    )

    st.success(
        f"Centroid: {latitude:.6f}, {longitude:.6f}"
    )

# --------------------------------------------------
# CROP
# --------------------------------------------------

crop = st.selectbox(
    "Select Crop",
    [
        "RABI ONION",
        "SUMMER ONION",
        "WHEAT IRRIGATED",
        "WHEAT UNIRRIGATED",
        "RABI MAIZE",
        "KHARIF MAIZE",
        "KHARIF GROUNDNUT",
        "SUMMER GROUNDNUT"
    ]
)

# --------------------------------------------------
# PREDICT
# --------------------------------------------------

if st.button("Predict Yield"):

 with st.spinner(
    "ASI is estimating yield for the selected crop..."):

    if area_ha is None:

        st.error(
            "Please draw a farm boundary first."
        )

    else:

        payload = {
            "latitude": latitude,
            "longitude": longitude,
            "crop": crop,
            "area_ha": area_ha
        }

        try:

            response = requests.post(
                API_URL,
                json=payload,
                timeout=120
            )

            result = response.json()

            if result["success"]:

                st.success(
                    "Prediction Generated"
                )

                yield_density = result["prediction"]["yield_kg_ha"]

                st.metric( "Yield Density (kg/ha)",f"{yield_density:,.2f}")
                total_production = (yield_density * area_ha)

                st.metric("Estimated Production (kg)",f"{total_production:,.2f}")

                st.write("### Location")

                st.write(
                    f"District: {result['location']['district']}"
                )

                st.write(
                    f"Agro Zone: {result['location']['agro_zone']}"
                )

                st.write("### Farm")

                st.write(
                    f"Area: {area_ha:.2f} ha"
                )

            else:

                st.error(result)

        except Exception as e:

            st.error(str(e))

# ==================================================
# DECISION SUPPORT DASHBOARD
# ==================================================

if result and result.get("success"):

    features = result.get("location", {}).get("features", {})

    st.divider()

    st.header("📊 Field Intelligence Report")

    # ----------------------------------
    # FARM SUMMARY
    # ----------------------------------

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Yield Density (kg/ha)",
            f"{yield_density:,.2f}"
        )

    with col2:
        st.metric(
            "Estimated Production (kg)",
            f"{total_production:,.2f}"
        )

    # ----------------------------------
    # ENVIRONMENT PROFILE
    # ----------------------------------

    st.subheader("🌱 Soil Profile")

    soil_col1, soil_col2, soil_col3 = st.columns(3)

    with soil_col1:
        st.metric(
            "Soil pH",
            round(features.get("ph_h2o", 0), 2)
        )

        st.metric(
            "Organic Matter %",
            round(
                features.get("organic_matter_pct", 0),
                2
            )
        )

    with soil_col2:
        st.metric(
            "Nitrogen",
            round(
                features.get("nitrogen_g_kg", 0),
                2
            )
        )

        st.metric(
            "CEC",
            round(
                features.get("cec_cmol_kg", 0),
                2
            )
        )

    with soil_col3:
        st.metric(
            "Texture",
            features.get("texture_class", "-")
        )

        st.metric(
            "Water Retention",
            round(
                features.get("water_retention_index", 0),
                2
            )
        )

    # ----------------------------------
    # WEATHER
    # ----------------------------------

    st.subheader("☁️ Weather Profile")

    weather_col1, weather_col2 = st.columns(2)

    with weather_col1:
        st.metric(
            "Rainfall (mm)",
            round(
                features.get("Rainfall_mm", 0),
                2
            )
        )

    with weather_col2:
        st.metric(
            "Temperature (°C)",
            round(
                features.get("Temperature_C", 0),
                2
            )
        )

    # ----------------------------------
    # VEGETATION
    # ----------------------------------

    st.subheader("🛰 Vegetation Profile")

    veg_col1, veg_col2 = st.columns(2)

    with veg_col1:
        st.metric(
            "NDVI",
            round(
                features.get("NDVI", 0),
                3
            )
        )

    with veg_col2:
        st.metric(
            "EVI",
            round(
                features.get("EVI", 0),
                3
            )
        )

    # ----------------------------------
    # INTERPRETATION
    # ----------------------------------

    st.subheader("🧠 Field Interpretation")

    soil_fertility = features.get(
        "soil_fertility_index", 0
    )

    ndvi = features.get("NDVI", 0)

    rainfall = features.get("Rainfall_mm", 0)

    positive = []
    negative = []

    if soil_fertility > 5:
        positive.append(
            "Good soil fertility"
        )
    else:
        negative.append(
            "Lower soil fertility"
        )

    if ndvi > 0.3:
        positive.append(
            "Healthy vegetation detected"
        )
    else:
        negative.append(
            "Weak vegetation signal"
        )

    if rainfall > 800:
        positive.append(
            "Adequate rainfall"
        )
    else:
        negative.append(
            "Lower rainfall availability"
        )

    col1, col2 = st.columns(2)

    with col1:

        st.success(
            "Positive Indicators"
        )

        for item in positive:
            st.write(f"✅ {item}")

    with col2:

        st.warning(
            "Risk Indicators"
        )

        for item in negative:
            st.write(f"⚠️ {item}")

else:
    st.info("Run a prediction to view the Field Intelligence Report.")
