
import ee
import folium
import geemap
import json
import requests

# Trigger the authentication flow.
ee.Authenticate()

# Initialize the Earth Engine library.
ee.Initialize(project='ee-msingh8')
# --------------------------------------------------------


# Define AOI (For example, a region in India)
lon_min = 77.0   # Western boundary (longitude)
lat_min = 28.0   # Southern boundary (latitude)
lon_max = 78.0   # Eastern boundary (longitude)
lat_max = 29.0   # Northern boundary (latitude)

# Define the Area of Interest (AOI) using the rectangle geometry
aoi = ee.Geometry.Rectangle([lon_min, lat_min, lon_max, lat_max])

# Load Sentinel-2 Image Collection, filter, and get median image
collection = ee.ImageCollection("COPERNICUS/S2_HARMONIZED") \
    .filterBounds(aoi) \
    .filterDate('2024-01-01', '2024-12-31') \
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))

image = collection.median().clip(aoi)

# Compute NDVI, EVI, and SAVI
ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')
evi = image.expression(
    '2.5 * ((NIR - RED) / (NIR + 6 * RED - 7.5 * BLUE + 1))', {
        'NIR': image.select('B8'),
        'RED': image.select('B4'),
        'BLUE': image.select('B2')
    }).rename('EVI')

savi = image.expression(
    '((NIR - RED) / (NIR + RED + 0.5)) * (1 + 0.5)', {
        'NIR': image.select('B8'),
        'RED': image.select('B4')
    }).rename('SAVI')

# Create a Folium map centered on AOI
lat_center = (lat_min + lat_max) / 2
lon_center = (lon_min + lon_max) / 2
map_gee = folium.Map(location=[lat_center, lon_center], zoom_start=10)

# Add the NDVI, EVI, SAVI layers and original image
def add_ee_layer(self, ee_image_object, vis_params, name):
    map_id_dict = ee.Image(ee_image_object).getMapId(vis_params)
    folium.raster_layers.TileLayer(
        tiles=map_id_dict['tile_fetcher'].url_format,
        attr='Google Earth Engine',
        name=name,
        overlay=True,
        control=True
    ).add_to(self)

folium.Map.add_ee_layer = add_ee_layer

# Visualization parameters
vis_params_ndvi = {'min': 0, 'max': 1, 'palette': ['blue', 'white', 'green']}
vis_params_evi = {'min': 0, 'max': 1, 'palette': ['blue', 'white', 'green']}
vis_params_savi = {'min': 0, 'max': 1, 'palette': ['brown', 'white', 'green']}
vis_params_rgb = {'min': 0, 'max': 3000, 'bands': ['B4', 'B3', 'B2']}  # RGB bands

# Add layers to map
map_gee.add_ee_layer(ndvi, vis_params_ndvi, 'NDVI')
map_gee.add_ee_layer(evi, vis_params_evi, 'EVI')
map_gee.add_ee_layer(savi, vis_params_savi, 'SAVI')
map_gee.add_ee_layer(image, vis_params_rgb, 'Sentinel-2 RGB')

# Add a layer control panel
map_gee.add_child(folium.LayerControl())
# Create a composite image with NDVI, EVI, and SAVI
composite = ee.Image.cat([ndvi, evi, savi])

# Reduce the region to get statistics (mean, sum, etc.)
# You can specify the reducer type like mean, median, sum, etc.
stats = composite.reduceRegion(
    reducer=ee.Reducer.mean(),  # or ee.Reducer.median(), ee.Reducer.sum(), etc.
    geometry=aoi,
    scale=10,  # 10 meters for Sentinel-2
    bestEffort=True
)

# Get the numerical results as a dictionary
result = stats.getInfo()
print("NDVI, EVI, SAVI Stats:", result)

# To export the result as a CSV (optional)
export_task = ee.batch.Export.table.toDrive(
    collection=ee.FeatureCollection([ee.Feature(None, result)]),
    description='NDVI_EVI_SAVI_Export',
    fileFormat='CSV'
)
export_task.start()
map_gee.save("map_output.html")

