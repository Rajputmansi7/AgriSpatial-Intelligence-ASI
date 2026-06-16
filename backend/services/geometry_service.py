from shapely.geometry import Polygon
from shapely.geometry import Point
from pyproj import Geod


geod = Geod(ellps="WGS84")


def polygon_area_hectares(coordinates):
    """
    coordinates:
    [
        [lon, lat],
        [lon, lat],
        ...
    ]
    """

    lons = [p[0] for p in coordinates]
    lats = [p[1] for p in coordinates]

    area_m2, _ = geod.polygon_area_perimeter(
        lons,
        lats
    )

    area_m2 = abs(area_m2)

    area_ha = area_m2 / 10000

    return round(area_ha, 4)


def polygon_centroid(coordinates):

    polygon = Polygon(coordinates)

    centroid = polygon.centroid

    return {
        "longitude": centroid.x,
        "latitude": centroid.y
    }


def build_geometry_features(coordinates):

    centroid = polygon_centroid(coordinates)

    area_ha = polygon_area_hectares(coordinates)

    return {
        "latitude": centroid["latitude"],
        "longitude": centroid["longitude"],
        "area_ha": area_ha
    }