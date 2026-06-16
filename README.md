
<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/0165d766-e3f3-4f36-99a0-f1010a0d7b46" />



AgriSpatial Intelligence (ASI) V1

AI-powered geospatial crop yield prediction platform combining satellite intelligence, environmental data, and machine learning.

Live Demo

Web Application

https://agrispatial-intelligence-asi.streamlit.app

API Documentation

https://agrispatial-intelligence-asi.onrender.com/docs

AgriSpatial Intelligence (ASI) is a geospatial crop yield prediction platform that combines satellite-derived environmental indicators, soil intelligence, agro-climatic zoning, and machine learning to estimate agricultural yield at the farm level.

Users can draw a farm boundary on an interactive map, select a crop, and receive:

* Predicted crop yield (kg/ha)
* Estimated total production
* Soil intelligence
* Weather indicators
* Vegetation health indicators
* Agro-climatic zone classification
* Field interpretation and decision-support insights

⸻

Key Features

Interactive Farm Mapping

* Draw farm boundaries directly on a satellite map
* Automatic centroid extraction
* Automatic farm area calculation (hectares)

Yield Prediction Engine

* Crop-specific yield estimation
* XGBoost machine learning model
* Farm-level yield density prediction (kg/ha)
* Estimated production calculation

Geospatial Intelligence

* District identification from coordinates
* Agro-zone classification
* Gujarat district boundary lookup
* Spatial validation rules

Environmental Intelligence

Soil Indicators

* Soil pH
* Organic Matter
* Nitrogen
* CEC (Cation Exchange Capacity)
* Texture Classification
* FAO Soil Classification
* Water Retention Index

Weather Indicators

* Rainfall
* Temperature

Vegetation Indicators

* NDVI
* EVI

Decision Support Dashboard

* Field Intelligence Report
* Positive indicators
* Risk indicators
* Soil profile assessment
* Weather profile assessment
* Vegetation profile assessment

⸻

System Architecture

User

↓

Streamlit Frontend

↓

FastAPI Backend

↓

Feature Engineering Layer

↓

Google Earth Engine + Soil Intelligence

↓

XGBoost Yield Prediction Model

↓

Prediction Response

⸻

Machine Learning Pipeline

Model

* XGBoost Regressor

Input Features

* Farm Area
* District
* Agro Zone
* Crop Type
* Rainfall
* Temperature
* NDVI
* EVI
* Soil pH
* Organic Matter
* Nitrogen
* CEC
* Texture Class
* FAO Soil Class
* Water Retention Index

Output

* Yield Prediction (kg/ha)

⸻

Technology Stack

Frontend

* Streamlit
* Folium
* Streamlit-Folium

Backend

* FastAPI
* Pydantic

Geospatial

* GeoPandas
* Shapely
* Google Earth Engine

Machine Learning

* XGBoost
* Scikit-Learn
* Joblib

Data Processing

* Pandas
* NumPy

⸻

Project Structure

artifacts/
├── final_crop_yield_model.pkl
├── model_features.pkl
└── model_metadata.json
backend/
├── data/
├── models/
├── schemas/
├── services/
├── utils/
└── main.py
frontend/
├── app.py
└── map_component.py
docs/
└── DATA_PREP_REPORT.md

Local Development

Clone Repository

git clone https://github.com/Rajputmansi7/AgriSpatial-Intelligence-ASI.git
cd AgriSpatial-Intelligence-ASI

Install Dependencies

pip install -r requirements.txt

Start Backend

uvicorn backend.main:app --reload

Backend:

http://127.0.0.1:8000

API Documentation:

http://127.0.0.1:8000/docs

Start Frontend

streamlit run frontend/app.py

Frontend:

http://localhost:8501

⸻

Deployment

Backend

Deployed on Render.

Frontend

Deployed on Streamlit Community Cloud.

⸻

Live Demo

API

https://agrispatial-intelligence-asi.onrender.com/docs

Application

Add Streamlit deployment URL here.

⸻

Current Scope

ASI V1 is focused on:

* Gujarat district coverage
* Farm-level yield estimation
* Geospatial feature engineering
* Satellite-derived environmental indicators
* Decision-support dashboards

⸻

Future Roadmap

ASI V2

* Multi-state support
* Historical yield analytics
* SHAP explainability
* Crop recommendation engine
* Irrigation intelligence
* Fertilizer recommendation system
* Time-series vegetation monitoring
* Farm portfolio analytics

⸻

Author

Mansi Singh

Founder, AgriSpatial Intelligence (ASI)

Building AI-powered geospatial intelligence systems for agriculture.
