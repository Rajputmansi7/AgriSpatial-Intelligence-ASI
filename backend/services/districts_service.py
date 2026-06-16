import geopandas as gpd
from shapely.geometry import Point


AGRO_ZONE_MAPPING = {
    "ANAND": "MIDDLE_GUJARAT",
    "KHEDA": "MIDDLE_GUJARAT",
    "VADODARA": "MIDDLE_GUJARAT",

    "AMRELI": "SOUTH_SAURASHTRA",
    "BHAVNAGAR": "SOUTH_SAURASHTRA",
    "JUNAGADH": "SOUTH_SAURASHTRA",
    "PORBANDAR": "SOUTH_SAURASHTRA",
    "RAJKOT": "SOUTH_SAURASHTRA",

    "JAMNAGAR": "NORTH_SAURASHTRA",
    "SURENDRANAGAR": "NORTH_SAURASHTRA",

    "BANASKANTHA": "NORTH_GUJARAT",
    "GANDHINAGAR": "NORTH_GUJARAT",
    "PATAN": "NORTH_GUJARAT",

    "KACHCHH": "NORTH_WEST_ARID",

    "BHARUCH": "SOUTH_GUJARAT",
    "NARMADA": "SOUTH_GUJARAT",
    "SURAT": "SOUTH_GUJARAT",

    "NAVSARI": "SOUTH_GUJARAT_HEAVY",
    "VALSAD": "SOUTH_GUJARAT_HEAVY",
    "DAHOD": "SOUTH_GUJARAT"
}


class DistrictService:

    def __init__(self):

        self.districts = gpd.read_file(
            "backend/data/gujarat_districts.geojson"
        )

    def get_location_info(
        self,
        latitude: float,
        longitude: float
    ):

        point = Point(
            longitude,
            latitude
        )

        match = self.districts[
            self.districts.contains(point)
        ]

        if len(match) == 0:

            return {
                "district": "UNKNOWN",
                "agro_zone": "UNKNOWN"
            }

        district = str(
        match.iloc[0]["NAME_2"]).upper().strip()

        agro_zone = AGRO_ZONE_MAPPING.get(
            district,
            "UNKNOWN"
        )

        return {
            "district": district,
            "agro_zone": agro_zone
        }


district_service = DistrictService()