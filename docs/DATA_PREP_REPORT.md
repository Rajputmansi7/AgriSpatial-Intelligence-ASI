Agricultural Spatial Intelligence (ASI) V1

Data Preparation Report

Project Overview

Agricultural Spatial Intelligence (ASI) is a geospatial machine learning platform designed to estimate crop yield using environmental, soil, weather, and location-based intelligence.

The system combines:

* Historical crop yield records
* Satellite-derived vegetation indicators
* Soil characteristics
* Weather variables
* Geospatial district information

to generate field-level yield predictions and decision-support insights.

⸻

Study Area

State: Gujarat, India

District Coverage: All Gujarat districts included in the training dataset.

Geospatial Reference:

* Gujarat district boundaries (GeoJSON)
* District centroids
* Agro-climatic zone mapping

⸻

Data Sources

Crop Yield Data

Target Variable:

Yield (kg/ha)

Primary Inputs:

* District
* Crop
* Agricultural Year
* Cultivated Area (ha)
* Production (kg)

Derived:

Yield = Production / Area

⸻

Soil Data

Source:

Kaegro Soil API

Variables:

* Sand Percentage
* Silt Percentage
* Clay Percentage
* Soil pH
* Organic Matter
* Nitrogen
* Cation Exchange Capacity (CEC)
* Field Capacity
* Wilting Capacity
* Soil Texture
* FAO Soil Classification

Purpose:

Provide information about soil fertility, structure, and water retention capability.

⸻

Weather Data

Source:

Google Earth Engine
ERA5-Land Hourly Dataset

Variables:

* Mean Temperature (°C)
* Total Rainfall (mm)

Purpose:

Capture climatic conditions affecting crop productivity.

⸻

Vegetation Data

Source:

Google Earth Engine
Sentinel-2 SR Harmonized

Vegetation Indices:

NDVI

Normalized Difference Vegetation Index

Measures vegetation vigor and greenness.

EVI

Enhanced Vegetation Index

Improves vegetation monitoring under dense canopy conditions.

SAVI

Soil Adjusted Vegetation Index

Reduces soil brightness effects.

Purpose:

Provide crop health and vegetation condition indicators.

⸻

Data Processing Pipeline

District Mapping

Latitude and longitude coordinates are mapped to:

* District
* Agro-climatic Zone

using Gujarat district boundaries.

⸻

Soil Feature Processing

Missing soil values are replaced using predefined defaults derived from domain knowledge.

Example:

pH = 7.1
Organic Matter = 0.85

Purpose:

Ensure prediction continuity when external APIs fail.

⸻

Weather Aggregation

ERA5 hourly observations are aggregated into:

* Mean Temperature
* Total Rainfall

at district level.

⸻

Vegetation Aggregation

Sentinel-2 imagery is processed to calculate:

* NDVI
* EVI
* SAVI

Cloud filtering is applied before aggregation.

Median compositing is used to reduce noise.

⸻

Feature Engineering

Log Area

log_area_ha = log(1 + area_ha)

Purpose:

Reduce skew caused by large farm sizes.

⸻

Water Retention Index

Field Capacity - Wilting Capacity

Purpose:

Estimate plant-available water.

⸻

Soil Fertility Index

(
Organic Matter +
Nitrogen +
CEC
) / 3

Purpose:

Represent overall soil productivity.

⸻

Final Model Features

Location Features

* District
* Agro Zone

Farm Features

* Area (ha)
* Log Area

Soil Features

* Sand %
* Silt %
* Clay %
* pH
* Organic Matter
* Nitrogen
* CEC
* Texture Class
* FAO Classification
* Water Retention Index
* Soil Fertility Index

Weather Features

* Rainfall
* Temperature

Vegetation Features

* NDVI
* EVI

Crop Features

* Crop
* Year

⸻

Machine Learning Model

Algorithm:

XGBoost Regressor

Prediction Target:

Yield Density (kg/ha)

Model Output:

Estimated crop yield per hectare.

⸻

Production Inference Pipeline

User Workflow:

Draw Farm Boundary
        ↓
Calculate Area
        ↓
Extract Coordinates
        ↓
Identify District
        ↓
Fetch Soil Data
        ↓
Fetch Weather Data
        ↓
Fetch Vegetation Data
        ↓
Build Features
        ↓
Predict Yield Density
        ↓
Generate Field Intelligence Report

⸻

Decision Support Outputs

ASI V1 provides:

* Yield Density (kg/ha)
* Estimated Production (kg)
* Soil Profile
* Weather Profile
* Vegetation Profile
* District Information
* Agro Zone Information
* Field Intelligence Summary

⸻

Current Limitations

* Historical weather windows are used during inference.
* Soil information depends on external API availability.
* Prediction confidence intervals are not yet implemented.
* Crop suitability analysis is not yet implemented.
* Real-time environmental monitoring is planned for future versions.

⸻

Version

ASI V1

Status:

Deployment Ready